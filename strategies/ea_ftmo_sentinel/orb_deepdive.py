"""ORB + Keltner-fade robustness deep-dive (anti-overfit gauntlet).

1. Parameter-neighborhood sweep: a real structural effect should be positive
   across a smooth region, not in one lucky cell.
2. Month-by-month P&L of the headline configs.
3. Governor-level day stats + FTMO challenge walk-forward for the pick.

Usage: python3 orb_deepdive.py EURUSD
"""

from __future__ import annotations

import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from backtest_sentinel import Config, run_backtest                       # noqa: E402
from grid_search import split_stats                                       # noqa: E402
from strategy_lab import sig_orb_london, sig_keltner_fade                 # noqa: E402


def run(m1, built, spread, cutoff, sizing):
    t, sl_, ss_, conc, tp_d, sl_d, strength, diag = built
    over = dict(max_trades_day=1, base_risk=1.0) if sizing == "oneshot" else {}
    cfg = replace(Config(), name="x", spread=spread, **over)
    sig = (t, sl_, ss_, conc, tp_d, sl_d,
           strength if sizing == "strength" else None, diag)
    trades, daily, _ = run_backtest(m1, cfg, signals=sig)
    if not trades:
        return None, None, None
    return split_stats(trades, daily, cutoff), trades, daily


def monthly(daily):
    bym = {}
    for d in sorted(daily):
        bym.setdefault(str(d)[:7], []).append(daily[d]["pl"])
    return {m: round(sum(v), 2) for m, v in sorted(bym.items())}


def main():
    sym = sys.argv[1] if len(sys.argv) > 1 else "EURUSD"
    cutoff = date(2026, 6, 1)
    m1 = pd.read_parquet(Path(__file__).parent / "data" / f"{sym}_M1.parquet")
    if m1.index.tz is not None:
        m1.index = m1.index.tz_convert("UTC").tz_localize(None)
    spread = {"EURUSD": 0.00007, "GBPUSD": 0.00010}.get(sym, 0.00010)

    # ---- 1. ORB neighborhood sweep ------------------------------------
    print("== ORB neighborhood (train_total / test_total, oneshot sizing) ==")
    rows = []
    for trig in ["15min", "30min"]:
        for range_end in [6, 7, 8]:
            for entry_until in [10, 12, 14]:
                for tp_mult in [1.0, 1.25, 1.5, 2.0]:
                    for sl_mode in ["mid", "far"]:
                        built = sig_orb_london(m1, trig=trig, range_end=range_end,
                                               entry_until=entry_until,
                                               tp_mult=tp_mult, sl_mode=sl_mode)
                        st, _, _ = run(m1, built, spread, cutoff, "oneshot")
                        if st is None:
                            continue
                        rows.append({"trig": trig, "re": range_end,
                                     "eu": entry_until, "tp": tp_mult,
                                     "slm": sl_mode, **st})
    df = pd.DataFrame(rows)
    df["both_pos"] = (df.tr_total > 0) & (df.te_total > 0)
    pd.set_option("display.width", 250)
    print(f"cells: {len(df)} · positive-both-splits: {int(df.both_pos.sum())} "
          f"({df.both_pos.mean():.0%}) · median train {df.tr_total.median():+.2f}% "
          f"· median test {df.te_total.median():+.2f}%")
    piv = df.pivot_table(index=["trig", "slm"], columns="tp",
                         values="te_total", aggfunc="median")
    print("\nmedian TEST total by trigger/sl_mode x tp_mult:")
    print(piv.round(2).to_string())
    piv2 = df.pivot_table(index="re", columns="eu", values="te_total", aggfunc="median")
    print("\nmedian TEST total by range_end x entry_until:")
    print(piv2.round(2).to_string())
    df.to_csv(Path(__file__).parent / f"ORB_NEIGHBORHOOD_{sym}.csv", index=False)

    # ---- 2. headline configs: monthly + governor stats -----------------
    print("\n== headline configs ==")
    picks = [
        ("orb15_tp1.5_mid_oneshot",
         sig_orb_london(m1, trig="15min", tp_mult=1.5, sl_mode="mid"), "oneshot"),
        ("orb30_tp1.5_mid_oneshot",
         sig_orb_london(m1, trig="30min", tp_mult=1.5, sl_mode="mid"), "oneshot"),
        ("orb15_tp1.5_mid_flat",
         sig_orb_london(m1, trig="15min", tp_mult=1.5, sl_mode="mid"), "flat"),
        ("keltner30_kc2.0_strength",
         sig_keltner_fade(m1, trig="30min", kc_mult=2.0, tp_atr=1.5, sl_atr=2.0),
         "strength"),
    ]
    from grid_search import split_stats as _
    from backtest_sentinel import challenge_walkforward
    from collections import Counter
    for name, built, sizing in picks:
        st, trades, daily = run(m1, built, spread, cutoff, sizing)
        if st is None:
            print(f"{name}: no trades")
            continue
        days = sorted(daily)
        pls = [daily[d]["pl"] for d in days]
        wd = [d for d in days if daily[d]["trades"] > 0]
        red = sum(1 for d in wd if daily[d]["pl"] < -1e-9)
        oc = challenge_walkforward(daily)
        c = Counter(r for r, _k in oc)
        passes = [k for r, k in oc if r == "PASS"]
        med = int(np.median(passes)) if passes else None
        print(f"\n{name}: trades={len(trades)} "
              f"train {st['tr_total']:+.2f}% / test {st['te_total']:+.2f}% "
              f"| mean day {np.mean(pls):+.3f}% worst {min(pls):+.2f}% "
              f"red {red}/{len(wd)} | breaches "
              f"{sum(1 for d in days if daily[d]['min_float'] <= -5.0)}")
        print(f"  monthly: {monthly(daily)}")
        print(f"  challenge ({len(oc)} starts): "
              + ", ".join(f"{k} {v / len(oc):.0%}" for k, v in sorted(c.items()))
              + (f" · median days-to-pass {med}" if med else ""))


if __name__ == "__main__":
    main()
