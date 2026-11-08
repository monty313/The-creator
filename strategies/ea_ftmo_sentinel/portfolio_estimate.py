"""Portfolio estimate: combine per-symbol Sentinel day P&L series.

Approximation (labelled): each symbol runs its own governor (as measured);
combined day P&L = sum of per-symbol days, then clipped at the account-level
soft stop (-1.5%) to approximate the EA's shared-governor halt. Challenge
walk-forward on the combined series.

Legs:
  EURUSD  keltner fade 30min kc2.0 strength   (real M1, Jan-Aug)
  GBPUSD  keltner fade 15min kc2.0 flat        (real M1, Jan-Apr partial)
  EURUSD  London ORB oneshot tp1.25 mid        (optional, single-symbol evidence)

Usage: python3 portfolio_estimate.py
"""

from __future__ import annotations

import sys
from collections import Counter
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from backtest_sentinel import Config, run_backtest, challenge_walkforward   # noqa: E402
from strategy_lab import sig_keltner_fade, sig_orb_london                    # noqa: E402


def day_series(sym, builder_kwargs, sizing, fade=True, spread=0.0001):
    m1 = pd.read_parquet(Path(__file__).parent / "data" / f"{sym}_M1.parquet")
    if m1.index.tz is not None:
        m1.index = m1.index.tz_convert("UTC").tz_localize(None)
    if sym == "GBPUSD":
        m1 = m1[m1.index < "2026-04-05"]          # contiguous real portion
    builder = sig_keltner_fade if fade else sig_orb_london
    built = builder(m1, **builder_kwargs)
    t, sl_, ss_, conc, tp_d, sl_d, strength, diag = built
    over = dict(max_trades_day=1, base_risk=1.0) if sizing == "oneshot" else {}
    cfg = replace(Config(), name="leg", spread=spread, **over)
    sig = (t, sl_, ss_, conc, tp_d, sl_d,
           strength if sizing == "strength" else None, diag)
    trades, daily, _ = run_backtest(m1, cfg, signals=sig)
    return {d: daily[d] for d in daily}


def combine(legs):
    all_days = sorted(set().union(*[set(l) for l in legs]))
    out = {}
    for d in all_days:
        pl = sum(l[d]["pl"] for l in legs if d in l)
        pl = max(pl, -1.5)          # shared-governor soft-stop approximation
        tr = sum(l[d]["trades"] for l in legs if d in l)
        mf = min((l[d]["min_float"] for l in legs if d in l), default=0.0)
        out[d] = {"pl": pl, "trades": tr, "banked": False, "halted": False,
                  "min_float": mf}
    return out


def report(name, daily):
    days = sorted(daily)
    pls = [daily[d]["pl"] for d in days]
    wd = [d for d in days if daily[d]["trades"] > 0]
    oc = challenge_walkforward(daily)
    c = Counter(r for r, _ in oc)
    passes = [k for r, k in oc if r == "PASS"]
    med = int(np.median(passes)) if passes else None
    print(f"\n{name}:")
    print(f"  days {len(days)} (traded {len(wd)}) · total {sum(pls):+.2f}% "
          f"· mean day {np.mean(pls):+.3f}% · worst {min(pls):+.2f}% "
          f"· P(day>=2.5) {sum(1 for p in pls if p >= 2.5)/max(len(wd),1):.1%}")
    print(f"  red days {sum(1 for d in wd if daily[d]['pl'] < -1e-9)}/{len(wd)} "
          f"· breaches {sum(1 for d in days if daily[d]['min_float'] <= -5.0)}")
    print("  challenge: " + ", ".join(f"{k} {v/len(oc):.0%}" for k, v in sorted(c.items()))
          + (f" · median days-to-pass {med}" if med else ""))


def main():
    eur_fade = day_series("EURUSD", dict(trig="30min", kc_mult=2.0,
                                         tp_atr=1.5, sl_atr=2.0),
                          "strength", spread=0.00007)
    gbp_fade = day_series("GBPUSD", dict(trig="15min", kc_mult=2.0,
                                         tp_atr=1.5, sl_atr=2.0),
                          "flat", spread=0.00010)
    eur_orb = day_series("EURUSD", dict(trig="15min", tp_mult=1.25,
                                        sl_mode="mid"),
                         "oneshot", fade=False, spread=0.00007)

    report("EURUSD fade alone", eur_fade)
    report("GBPUSD fade alone (Jan-Apr real)", gbp_fade)
    report("EURUSD ORB alone (single-symbol evidence)", eur_orb)
    report("PORTFOLIO fade EUR+GBP", combine([eur_fade, gbp_fade]))
    report("PORTFOLIO fade EUR+GBP + EUR ORB", combine([eur_fade, gbp_fade, eur_orb]))


if __name__ == "__main__":
    main()
