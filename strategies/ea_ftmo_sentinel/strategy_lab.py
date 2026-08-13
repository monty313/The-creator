"""Strategy lab — hunt for an edge that survives the honest harness.

New families beyond the corpus reclaim engines (each maps to a corpus note
family where one exists), all run through the same bar-accurate engine with
real costs, M1 adjudication and the Day Governor:

  keltner_fade   corpus rank-1 s11: fade closes outside Keltner channel
  zscore_fade    s12: fade |zscore| extremes back to the mean
  orb_london     s02/S3: London opening-range breakout, range-based stops
  donchian_h1    s03 turtle: H1 Donchian breakout w/ trend filter, wide barriers
  ma_pullback    SNAP-8 texture: H1 trend + M15 pullback-to-EMA20 resume

Sizing creativity (lot-size axis):
  flat           fixed base risk (governor ladder on top, as always)
  oneshot        one concentrated attempt/day at higher risk (cost-count play)
  strength       risk scaled by signal strength (stretch/force magnitude)

Selection law: positive on BOTH train (Jan-May) and test (Jun-Aug) splits,
>= 40 trades total, then judged on test-split drawdown. No exceptions.

Usage: python3 strategy_lab.py EURUSD [2026-06-01]
"""

from __future__ import annotations

import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from backtest_sentinel import (Config, run_backtest, resample, map_htf,   # noqa: E402
                               sma, atr, cci)
from grid_search import split_stats                                       # noqa: E402


def ema(s, n):
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


# ---------------------------------------------------------------- families
def sig_keltner_fade(m1, trig, kc_n=20, kc_mult=1.5, tp_atr=1.2, sl_atr=1.8,
                     htf_flat=True):
    """Fade a close outside the Keltner channel back toward the mean.
    htf_flat: only fade when H4 is NOT strongly trending against the fade."""
    t = resample(m1, trig)
    a = atr(t.high, t.low, t.close, 14)
    mid = ema(t.close, kc_n)
    up = mid + kc_mult * a
    dn = mid - kc_mult * a
    sig_l = (t.close < dn)
    sig_s = (t.close > up)
    if htf_flat:
        h4 = resample(m1, "4h")
        slope = (sma(h4.close, 10) - sma(h4.close, 10).shift(3))
        sl4 = map_htf(slope, t.index)
        a4 = map_htf(atr(h4.high, h4.low, h4.close, 14), t.index)
        strong_dn = sl4 < -0.5 * a4
        strong_up = sl4 > 0.5 * a4
        sig_l &= ~strong_dn        # don't catch knives in a strong H4 downtrend
        sig_s &= ~strong_up
    # strength = how far outside the band (in ATR)
    stretch_l = ((dn - t.close) / a).clip(lower=0)
    stretch_s = ((t.close - up) / a).clip(lower=0)
    strength = (1.0 + (stretch_l + stretch_s)).fillna(1.0)
    conc = pd.Series(False, t.index)
    diag = {"raw_l": int(sig_l.sum()), "raw_s": int(sig_s.sum())}
    return (t, sig_l.fillna(False), sig_s.fillna(False), conc,
            a * tp_atr, a * sl_atr, strength, diag)


def sig_zscore_fade(m1, trig, n=48, z_in=2.0, tp_atr=1.2, sl_atr=2.0):
    t = resample(m1, trig)
    a = atr(t.high, t.low, t.close, 14)
    m = t.close.rolling(n, min_periods=n).mean()
    sd = t.close.rolling(n, min_periods=n).std()
    z = (t.close - m) / sd.replace(0.0, np.nan)
    sig_l = z < -z_in
    sig_s = z > z_in
    sig_l &= ~sig_l.shift(1).fillna(False)      # first touch only
    sig_s &= ~sig_s.shift(1).fillna(False)
    strength = (1.0 + (z.abs() - z_in).clip(lower=0)).fillna(1.0)
    conc = pd.Series(False, t.index)
    diag = {"raw_l": int(sig_l.sum()), "raw_s": int(sig_s.sum())}
    return (t, sig_l.fillna(False), sig_s.fillna(False), conc,
            a * tp_atr, a * sl_atr, strength, diag)


def sig_orb_london(m1, trig="15min", range_end=7, entry_until=12,
                   tp_mult=1.5, sl_mode="mid"):
    """London opening-range breakout. Range = 00:00→07:00 UTC high/low.
    First close beyond the range during 07:00-12:00 fires; SL = range mid
    (or far side), TP = tp_mult × range height. One fire per side per day."""
    t = resample(m1, trig)
    d = pd.Series(t.index.date, index=t.index)
    hr = pd.Series(t.index.hour, index=t.index)
    in_range = hr < range_end
    rng_hi = t.high.where(in_range).groupby(d).cummax().groupby(d).ffill()
    rng_lo = t.low.where(in_range).groupby(d).cummin().groupby(d).ffill()
    height = rng_hi - rng_lo
    window = (hr >= range_end) & (hr < entry_until)
    brk_l = window & (t.close > rng_hi) & height.notna()
    brk_s = window & (t.close < rng_lo) & height.notna()
    # first breakout of the day per side
    sig_l = brk_l & ~brk_l.groupby(d).cummax().shift(1).fillna(False)
    sig_s = brk_s & ~brk_s.groupby(d).cummax().shift(1).fillna(False)
    if sl_mode == "mid":
        sl_l = (t.close - (rng_hi + rng_lo) / 2)
        sl_s = ((rng_hi + rng_lo) / 2 - t.close)
    else:                                        # far side of the range
        sl_l = (t.close - rng_lo)
        sl_s = (rng_hi - t.close)
    sl_dist = sl_l.where(sig_l, sl_s.where(sig_s))
    tp_dist = height * tp_mult
    # sanity floor: skip degenerate ranges
    a = atr(t.high, t.low, t.close, 14)
    ok = (height > a) & (sl_dist > 0.2 * a)
    sig_l &= ok
    sig_s &= ok
    conc = pd.Series(False, t.index)
    diag = {"raw_l": int(sig_l.sum()), "raw_s": int(sig_s.sum())}
    return (t, sig_l.fillna(False), sig_s.fillna(False), conc,
            tp_dist, sl_dist, None, diag)[:6] + (None, diag)


def sig_donchian_h1(m1, trig="30min", n_break=24, tp_atr=4.0, sl_atr=2.0):
    """Turtle-style: H1 Donchian(n) breakout in the direction of the H4 trend,
    executed on the trigger TF, wide barriers so cost drag is tiny."""
    t = resample(m1, trig)
    h1 = resample(m1, "1h")
    h4 = resample(m1, "4h")
    hh = h1.high.rolling(n_break, min_periods=n_break).max()
    ll = h1.low.rolling(n_break, min_periods=n_break).min()
    hh_t = map_htf(hh, t.index)
    ll_t = map_htf(ll, t.index)
    trend = map_htf(sma(h4.close, 30), t.index)
    a = atr(t.high, t.low, t.close, 14)
    sig_l = (t.close > hh_t) & (t.close > trend)
    sig_s = (t.close < ll_t) & (t.close < trend)
    sig_l &= ~sig_l.shift(1).fillna(False)
    sig_s &= ~sig_s.shift(1).fillna(False)
    conc = pd.Series(False, t.index)
    diag = {"raw_l": int(sig_l.sum()), "raw_s": int(sig_s.sum())}
    return (t, sig_l.fillna(False), sig_s.fillna(False), conc,
            a * tp_atr, a * sl_atr, None, diag)


def sig_ma_pullback(m1, trig="15min", tp_atr=2.0, sl_atr=1.5):
    """H1 trend + trigger-TF pullback to EMA20 then resume bar."""
    t = resample(m1, trig)
    h1 = resample(m1, "1h")
    up_h1 = map_htf((ema(h1.close, 50) > ema(h1.close, 200)) &
                    (h1.close > ema(h1.close, 50)), t.index).astype(bool)
    dn_h1 = map_htf((ema(h1.close, 50) < ema(h1.close, 200)) &
                    (h1.close < ema(h1.close, 50)), t.index).astype(bool)
    e20 = ema(t.close, 20)
    touched_l = (t.low <= e20) & (t.low.shift(1) > e20.shift(1))
    touched_s = (t.high >= e20) & (t.high.shift(1) < e20.shift(1))
    resume_l = (t.close > t.open) & (t.close > e20)
    resume_s = (t.close < t.open) & (t.close < e20)
    win = 3
    sig_l = up_h1 & resume_l & touched_l.rolling(win, min_periods=1).max().astype(bool)
    sig_s = dn_h1 & resume_s & touched_s.rolling(win, min_periods=1).max().astype(bool)
    sig_l &= ~sig_l.shift(1).fillna(False)
    sig_s &= ~sig_s.shift(1).fillna(False)
    a = atr(t.high, t.low, t.close, 14)
    conc = pd.Series(False, t.index)
    diag = {"raw_l": int(sig_l.sum()), "raw_s": int(sig_s.sum())}
    return (t, sig_l.fillna(False), sig_s.fillna(False), conc,
            a * tp_atr, a * sl_atr, None, diag)


FAMILIES = {
    # name -> (builder, kwargs-grid)
    "keltner_fade": (sig_keltner_fade, [
        {"trig": "15min", "kc_mult": 1.5, "tp_atr": 1.2, "sl_atr": 1.8},
        {"trig": "15min", "kc_mult": 2.0, "tp_atr": 1.5, "sl_atr": 2.0},
        {"trig": "30min", "kc_mult": 1.5, "tp_atr": 1.2, "sl_atr": 1.8},
        {"trig": "30min", "kc_mult": 2.0, "tp_atr": 1.5, "sl_atr": 2.0},
        {"trig": "15min", "kc_mult": 2.0, "tp_atr": 1.5, "sl_atr": 2.0, "htf_flat": False},
    ]),
    "zscore_fade": (sig_zscore_fade, [
        {"trig": "15min", "n": 48, "z_in": 2.0},
        {"trig": "15min", "n": 96, "z_in": 2.5},
        {"trig": "30min", "n": 48, "z_in": 2.0},
    ]),
    "orb_london": (sig_orb_london, [
        {"trig": "15min", "tp_mult": 1.0, "sl_mode": "mid"},
        {"trig": "15min", "tp_mult": 1.5, "sl_mode": "mid"},
        {"trig": "15min", "tp_mult": 1.0, "sl_mode": "far"},
        {"trig": "30min", "tp_mult": 1.5, "sl_mode": "mid"},
    ]),
    "donchian_h1": (sig_donchian_h1, [
        {"trig": "30min", "n_break": 24, "tp_atr": 4.0, "sl_atr": 2.0},
        {"trig": "30min", "n_break": 48, "tp_atr": 4.0, "sl_atr": 2.0},
        {"trig": "1h",    "n_break": 24, "tp_atr": 5.0, "sl_atr": 2.5},
    ]),
    "ma_pullback": (sig_ma_pullback, [
        {"trig": "15min", "tp_atr": 2.0, "sl_atr": 1.5},
        {"trig": "15min", "tp_atr": 1.5, "sl_atr": 1.5},
        {"trig": "30min", "tp_atr": 2.0, "sl_atr": 1.5},
    ]),
}

SIZINGS = {
    "flat":     dict(),
    "oneshot":  dict(max_trades_day=1, base_risk=1.0),
    "strength": dict(),      # strength Series (if provided) scales risk
}


def main():
    sym = sys.argv[1] if len(sys.argv) > 1 else "EURUSD"
    cutoff = date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else date(2026, 6, 1)
    path = Path(__file__).parent / "data" / f"{sym}_M1.parquet"
    m1 = pd.read_parquet(path)
    if m1.index.tz is not None:
        m1.index = m1.index.tz_convert("UTC").tz_localize(None)
    spread = {"EURUSD": 0.00007, "GBPUSD": 0.00010, "EURUSD_Y": 0.00007,
              "GBPUSD_Y": 0.00010}.get(sym, 0.00010)
    print(f"{sym}: {m1.index[0]} -> {m1.index[-1]} · test from {cutoff}\n")

    rows = []
    for fam, (builder, grids) in FAMILIES.items():
        for gi, kw in enumerate(grids):
            built = builder(m1, **kw)
            t, sl_, ss_, conc, tp_d, sl_d, strength, diag = built
            for sz_name, sz_over in SIZINGS.items():
                if sz_name == "strength" and strength is None:
                    continue
                cfg = replace(Config(),
                              name=f"{fam}#{gi}_{sz_name}",
                              trigger=kw.get("trig", "15min"),
                              spread=spread, **sz_over)
                sig = (t, sl_, ss_, conc, tp_d, sl_d,
                       strength if sz_name == "strength" else None, diag)
                trades, daily, _ = run_backtest(m1, cfg, signals=sig)
                if not trades:
                    continue
                st = split_stats(trades, daily, cutoff)
                rows.append({"name": cfg.name, "fam": fam, "kw": str(kw), **st})

    df = pd.DataFrame(rows)
    df["n_tot"] = df.tr_n + df.te_n
    df["ok"] = (df.tr_total > 0) & (df.te_total > 0) & (df.n_tot >= 40)
    df = df.sort_values(["ok", "te_total"], ascending=False)
    pd.set_option("display.width", 260)
    cols = ["name", "tr_n", "tr_wr", "tr_total", "tr_worst",
            "te_n", "te_wr", "te_total", "te_worst", "ok"]
    print(df[cols].head(40).to_string(index=False))
    df.to_csv(Path(__file__).parent / f"LAB_{sym}.csv", index=False)
    print(f"\n[written] LAB_{sym}.csv · survivors (positive both splits, n>=40): "
          f"{int(df.ok.sum())}")
    if df.ok.any():
        print("\nSURVIVORS:")
        print(df[df.ok][cols].to_string(index=False))


if __name__ == "__main__":
    main()
