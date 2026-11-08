"""ORB regime filter test — train-calibrated, test-verified (no peeking).

Question: do ORB losses concentrate in identifiable overnight-range regimes
(height vs ATR), sessions, or weekdays? Buckets are measured on TRAIN
(Jan-May) only; any filter derived from them is then applied to TEST
(Jun-Aug) untouched.

Usage: python3 orb_regime.py EURUSD
"""

from __future__ import annotations

import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from backtest_sentinel import Config, run_backtest, resample, atr   # noqa: E402
from strategy_lab import sig_orb_london                              # noqa: E402
from grid_search import split_stats                                  # noqa: E402

CUTOFF = date(2026, 6, 1)


def orb_trades(m1, spread, tp_mult=1.25, trig="15min", extra_gate=None):
    built = sig_orb_london(m1, trig=trig, tp_mult=tp_mult, sl_mode="mid")
    t, sl_, ss_, conc, tp_d, sl_d, strength, diag = built
    if extra_gate is not None:
        g = extra_gate.reindex(t.index).fillna(False)
        sl_ = sl_ & g
        ss_ = ss_ & g
    cfg = replace(Config(), name="orb", spread=spread,
                  max_trades_day=1, base_risk=1.0)
    sig = (t, sl_, ss_, conc, tp_d, sl_d, None, diag)
    return run_backtest(m1, cfg, signals=sig), t


def main():
    sym = sys.argv[1] if len(sys.argv) > 1 else "EURUSD"
    m1 = pd.read_parquet(Path(__file__).parent / "data" / f"{sym}_M1.parquet")
    if m1.index.tz is not None:
        m1.index = m1.index.tz_convert("UTC").tz_localize(None)
    spread = {"EURUSD": 0.00007, "GBPUSD": 0.00010}.get(sym, 0.00010)

    (trades, daily, _), t = orb_trades(m1, spread)
    # per-day features known BEFORE the entry window opens (07:00 UTC)
    d_ser = pd.Series(t.index.date, index=t.index)
    hr = pd.Series(t.index.hour, index=t.index)
    in_range = hr < 7
    rng_hi = t.high.where(in_range).groupby(d_ser).max()
    rng_lo = t.low.where(in_range).groupby(d_ser).min()
    height = (rng_hi - rng_lo)
    a_daily = atr(t.high, t.low, t.close, 14).groupby(d_ser).first()  # ATR at day start
    ratio = (height / a_daily).rename("ratio")

    tr = [x for x in trades if x["time"].date() < CUTOFF]
    print(f"{sym} ORB oneshot tp1.25 mid: {len(trades)} trades "
          f"(train {len(tr)}, test {len(trades) - len(tr)})")

    # ---- train buckets --------------------------------------------------
    rows = []
    for x in tr:
        d = x["time"].date()
        rows.append({"pnl": x["pnl"], "ratio": ratio.get(d, np.nan),
                     "dow": x["time"].weekday(), "hour": x["time"].hour})
    df = pd.DataFrame(rows).dropna(subset=["ratio"])
    df["ratio_q"] = pd.qcut(df.ratio, 4, labels=["q1_small", "q2", "q3", "q4_big"])
    print("\nTRAIN P&L by overnight range/ATR quartile:")
    print(df.groupby("ratio_q", observed=True).pnl.agg(["count", "sum", "mean"]).round(3))
    print("\nTRAIN P&L by weekday (0=Mon):")
    print(df.groupby("dow").pnl.agg(["count", "sum", "mean"]).round(3))
    print("\nTRAIN P&L by entry hour:")
    print(df.groupby("hour").pnl.agg(["count", "sum", "mean"]).round(3))

    # ---- candidate gates from train, verified on test -------------------
    q_lo = df.ratio.quantile(0.25)
    q_hi = df.ratio.quantile(0.95)
    print(f"\nratio band from train: [{q_lo:.2f}, {q_hi:.2f}]")

    ratio_by_bar = d_ser.map(ratio)
    gates = {
        "band_ratio": (ratio_by_bar >= q_lo) & (ratio_by_bar <= q_hi),
    }
    # weekday gate only if train shows a clearly toxic day
    dow_pnl = df.groupby("dow").pnl.sum()
    bad_days = dow_pnl[dow_pnl < -1.0].index.tolist()
    if bad_days:
        dow_by_bar = pd.Series([ts.weekday() for ts in t.index], index=t.index)
        gates[f"skip_dow{bad_days}"] = ~dow_by_bar.isin(bad_days)

    base_st = split_stats(trades, daily, CUTOFF)
    print(f"\nbaseline: train {base_st['tr_total']:+.2f}% "
          f"test {base_st['te_total']:+.2f}% (n={len(trades)})")
    for name, gate in gates.items():
        (tr2, dy2, _), _t = orb_trades(m1, spread, extra_gate=gate)
        if not tr2:
            print(f"{name}: no trades")
            continue
        st = split_stats(tr2, dy2, CUTOFF)
        print(f"{name}: train {st['tr_total']:+.2f}% test {st['te_total']:+.2f}% "
              f"(n={len(tr2)})")


if __name__ == "__main__":
    main()
