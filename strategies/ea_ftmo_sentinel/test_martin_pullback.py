"""Test the 'Martin pullback' idea (YouTube USIC interview, 2026-08-13).

Faithful translation of the interviewed method to our instruments:
  * trend permission: rising EMA stack 9>21>50 on H1, price above EMA21
  * setup: trigger-TF bar pulls back INTO the rising EMA21
  * trigger: reversal bar (close > open, closes back above the EMA)
  * stop: TIGHT — just under the pullback low (floored at 0.3*ATR)
  * target: high R multiple (3R / 4R / 6R) — the payoff asymmetry IS the edge
  * no chasing: entry bar must not be stretched > 1 ATR above the EMA
  * risk: 0.5%/trade flat (his stated average)

Note what the source actually claims: win rate 22-25%, NOT 90%. This test
measures what the style does on FX/gold through the honest harness.

Usage: python3 test_martin_pullback.py
"""

from __future__ import annotations

import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from backtest_sentinel import Config, run_backtest, resample, map_htf, atr  # noqa: E402
from strategy_lab import ema                                                 # noqa: E402
from grid_search import split_stats                                          # noqa: E402


def sig_martin_pullback(m1, trig="15min", rr=4.0, sl_floor_atr=0.3,
                        sl_buffer_atr=0.10, chase_atr=1.0):
    t = resample(m1, trig)
    h1 = resample(m1, "1h")
    a = atr(t.high, t.low, t.close, 14)

    e9, e21, e50 = (map_htf(ema(h1.close, n), t.index) for n in (9, 21, 50))
    up_h1 = (e9 > e21) & (e21 > e50)
    dn_h1 = (e9 < e21) & (e21 < e50)

    e21_t = ema(t.close, 21)
    touched_l = (t.low <= e21_t) & (t.low.shift(1) > e21_t.shift(1))
    touched_s = (t.high >= e21_t) & (t.high.shift(1) < e21_t.shift(1))
    recent_touch_l = touched_l.rolling(3, min_periods=1).max().astype(bool)
    recent_touch_s = touched_s.rolling(3, min_periods=1).max().astype(bool)

    resume_l = (t.close > t.open) & (t.close > e21_t)
    resume_s = (t.close < t.open) & (t.close < e21_t)
    no_chase_l = (t.close - e21_t) < chase_atr * a      # don't buy stretched
    no_chase_s = (e21_t - t.close) < chase_atr * a

    sig_l = up_h1 & recent_touch_l & resume_l & no_chase_l
    sig_s = dn_h1 & recent_touch_s & resume_s & no_chase_s
    sig_l &= ~sig_l.shift(1).fillna(False)
    sig_s &= ~sig_s.shift(1).fillna(False)

    # tight stop: under the 3-bar pullback low (long), floored
    swing_lo = t.low.rolling(3, min_periods=1).min()
    swing_hi = t.high.rolling(3, min_periods=1).max()
    sl_l = (t.close - swing_lo) + sl_buffer_atr * a
    sl_s = (swing_hi - t.close) + sl_buffer_atr * a
    sl_dist = sl_l.where(sig_l, sl_s.where(sig_s))
    sl_dist = sl_dist.clip(lower=sl_floor_atr * a)
    tp_dist = sl_dist * rr

    conc = pd.Series(False, t.index)
    diag = {"raw_l": int(sig_l.sum()), "raw_s": int(sig_s.sum())}
    return t, sig_l.fillna(False), sig_s.fillna(False), conc, tp_dist, sl_dist, None, diag


def main():
    datasets = [
        ("EURUSD", "EURUSD_M1.parquet", None, 0.00007, date(2026, 6, 1)),
        ("GBPUSD", "GBPUSD_M1.parquet", "2026-04-05", 0.00010, date(2026, 3, 1)),
        ("GOLD(GC=F)", "GC=F_Y_M1.parquet", None, 0.30, date(2026, 7, 10)),
    ]
    for name, fn, cut, spread, split in datasets:
        path = Path(__file__).parent / "data" / fn
        if not path.exists():
            continue
        m1 = pd.read_parquet(path)
        if m1.index.tz is not None:
            m1.index = m1.index.tz_convert("UTC").tz_localize(None)
        if cut:
            m1 = m1[m1.index < cut]
        print(f"\n=== {name}  {m1.index[0]} -> {m1.index[-1]}  (split {split}) ===")
        for trig in ["15min", "30min"]:
            for rr in [3.0, 4.0, 6.0]:
                built = sig_martin_pullback(m1, trig=trig, rr=rr)
                cfg = replace(Config(), name="martin", spread=spread, base_risk=0.5)
                trades, daily, _ = run_backtest(m1, cfg, signals=built)
                if not trades:
                    print(f"  {trig} {rr:.0f}R: no trades")
                    continue
                st = split_stats(trades, daily, split)
                wins = sum(1 for x in trades if x["win"])
                avg_w = np.mean([x["pnl"] for x in trades if x["win"]]) if wins else 0
                avg_l = np.mean([x["pnl"] for x in trades if not x["win"]]) if wins < len(trades) else 0
                print(f"  {trig} {rr:.0f}R: n={len(trades)} WR {wins/len(trades):5.1%} "
                      f"avgW {avg_w:+.2f}% avgL {avg_l:+.2f}% "
                      f"| train {st['tr_total']:+.2f}% (n={st['tr_n']}) "
                      f"| test {st['te_total']:+.2f}% (n={st['te_n']})")


if __name__ == "__main__":
    main()
