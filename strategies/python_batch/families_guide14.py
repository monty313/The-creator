"""Adapters for the 14 strategies in Strategies-to-replicate guide.

Source: strategies/algo_guide_14/*.md
Lab contract: 2 HTF + 1 LTF, pullback + continuation modes.
Not Court law.
"""
from __future__ import annotations

import pandas as pd

from strategies.python_batch import indicators as ind
from strategies.python_batch.mtf import SetBars, htf_force_sma


def _edge(s: pd.Series) -> pd.Series:
    s = s.fillna(False)
    return s & ~s.shift(1).fillna(False)


def _htf_ma_side(sb: SetBars, fast: int = 50, slow: int = 200):
    def side(c):
        f, s = ind.sma(c, fast), ind.sma(c, slow)
        slope_ok_up = f > f.shift(3)
        slope_ok_dn = f < f.shift(3)
        bull = (f > s) & slope_ok_up
        bear = (f < s) & slope_ok_dn
        return bull, bear

    b1, s1 = side(sb.h1_close)
    b2, s2 = side(sb.h2_close)
    return (b1 & b2).fillna(False), (s1 & s2).fillna(False)


def fam_guide_s01_ma_cross(sb: SetBars):
    """S1 Moving Average Crossover — Golden/Death cross language on LTF, HTF slope filter."""
    bull, bear = _htf_ma_side(sb, 50, 200)
    f, s = ind.sma(sb.close, 50), ind.sma(sb.close, 200)
    cont_l = _edge(ind.cross_up(f, s) & (f > f.shift(3)))
    cont_s = _edge(ind.cross_dn(f, s) & (f < f.shift(3)))
    pb_l = _edge(bull & (sb.low <= f) & (sb.close > f))
    pb_s = _edge(bear & (sb.high >= f) & (sb.close < f))
    return bull, bear, (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s02_breakout(sb: SetBars):
    """S2 Breakout — close above/below range high/low (Donchian 20 proxy) with retest PB."""
    bull, bear = htf_force_sma(sb, 50)
    lo, hi = ind.donchian(sb.high, sb.low, 20)
    cont_l = _edge(ind.cross_up(sb.close, hi.shift(1)))
    cont_s = _edge(ind.cross_dn(sb.close, lo.shift(1)))
    # retest: touch prior band then close back inside direction
    pb_l = _edge(bull & (sb.low <= hi.shift(1)) & (sb.close > hi.shift(1)))
    pb_s = _edge(bear & (sb.high >= lo.shift(1)) & (sb.close < lo.shift(1)))
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s03_donchian_turtle(sb: SetBars):
    """S3 Donchian Turtle — 20 entry, 10-period exit channel language as cont/pb."""
    bull, bear = htf_force_sma(sb, 50)
    lo20, hi20 = ind.donchian(sb.high, sb.low, 20)
    lo10, hi10 = ind.donchian(sb.high, sb.low, 10)
    cont_l = _edge(ind.cross_up(sb.close, hi20.shift(1)))
    cont_s = _edge(ind.cross_dn(sb.close, lo20.shift(1)))
    # pullback inside 10-channel while HTF trend holds (room to breathe)
    pb_l = _edge(bull & (sb.low <= lo10) & (sb.close > lo10))
    pb_s = _edge(bear & (sb.high >= hi10) & (sb.close < hi10))
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s04_adx_di(sb: SetBars):
    """S4 ADX + DI — trade only when ADX>25; direction from +DI/-DI cross."""
    plus, minus, adx = ind.adx_di(sb.high, sb.low, sb.close, 14)
    strong = adx > 25
    # HTF: ADX strong on both HTFs with DI side
    p1, m1, a1 = ind.adx_di(sb.h1_high, sb.h1_low, sb.h1_close, 14)
    p2, m2, a2 = ind.adx_di(sb.h2_high, sb.h2_low, sb.h2_close, 14)
    bull = (a1 > 20) & (a2 > 20) & (p1 > m1) & (p2 > m2)
    bear = (a1 > 20) & (a2 > 20) & (m1 > p1) & (m2 > p2)
    cont_l = _edge(strong & ind.cross_up(plus, minus))
    cont_s = _edge(strong & ind.cross_up(minus, plus))
    pb_l = _edge(bull & strong & (plus > minus) & (plus < plus.shift(1)) & (plus > minus))
    pb_s = _edge(bear & strong & (minus > plus) & (minus < minus.shift(1)) & (minus > plus))
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s05_roc(sb: SetBars):
    """S5 ROC momentum — zero-line cross with MA50 trend filter."""
    r = ind.roc(sb.close, 12)
    ma50 = ind.sma(sb.close, 50)
    bull = (sb.h1_close > ind.sma(sb.h1_close, 50)) & (sb.h2_close > ind.sma(sb.h2_close, 50))
    bear = (sb.h1_close < ind.sma(sb.h1_close, 50)) & (sb.h2_close < ind.sma(sb.h2_close, 50))
    z = pd.Series(0.0, index=r.index)
    cont_l = _edge(ind.cross_up(r, z) & (sb.close > ma50))
    cont_s = _edge(ind.cross_dn(r, z) & (sb.close < ma50))
    pb_l = _edge(bull & (sb.close > ma50) & (r < 0) & (r > r.shift(1)))
    pb_s = _edge(bear & (sb.close < ma50) & (r > 0) & (r < r.shift(1)))
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s06_psar(sb: SetBars):
    """S6 Parabolic SAR — flip of SAR direction as continuation; pullback to SAR dots."""
    _, d = ind.parabolic_sar(sb.high, sb.low, sb.close)
    sar, _ = ind.parabolic_sar(sb.high, sb.low, sb.close)
    _, d1 = ind.parabolic_sar(sb.h1_high, sb.h1_low, sb.h1_close)
    _, d2 = ind.parabolic_sar(sb.h2_high, sb.h2_low, sb.h2_close)
    bull = (d1 > 0) & (d2 > 0)
    bear = (d1 < 0) & (d2 < 0)
    cont_l = _edge((d > 0) & (d.shift(1) <= 0))
    cont_s = _edge((d < 0) & (d.shift(1) >= 0))
    pb_l = _edge(bull & (d > 0) & (sb.low <= sar) & (sb.close > sar))
    pb_s = _edge(bear & (d < 0) & (sb.high >= sar) & (sb.close < sar))
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s07_ema_ribbon(sb: SetBars):
    """S7 EMA ribbon — stacked EMAs; cont on fan align, pb on touch mid ribbon."""
    bull, bear = htf_force_sma(sb, 50)
    e8, e21, e55 = ind.ema(sb.close, 8), ind.ema(sb.close, 21), ind.ema(sb.close, 55)
    up = (e8 > e21) & (e21 > e55)
    dn = (e8 < e21) & (e21 < e55)
    cont_l = _edge(up)
    cont_s = _edge(dn)
    pb_l = _edge(up & (sb.low <= e21) & (sb.close > e21))
    pb_s = _edge(dn & (sb.high >= e21) & (sb.close < e21))
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s08_bb_mr(sb: SetBars):
    """S8 Bollinger mean reversion — touch outer band, reclaim mid."""
    bull, bear = htf_force_sma(sb, 100)  # mild HTF bias; MR still fires both ways
    lo, mid, hi = ind.bollinger(sb.close, 20, 2.0, 0)
    # cont = reclaim mid from extreme
    cont_l = _edge(ind.cross_up(sb.close, mid) & (sb.close.shift(1) < lo.shift(1)))
    cont_s = _edge(ind.cross_dn(sb.close, mid) & (sb.close.shift(1) > hi.shift(1)))
    pb_l = _edge((sb.close < lo) | ind.cross_dn(sb.close, lo))
    pb_s = _edge((sb.close > hi) | ind.cross_up(sb.close, hi))
    # For MR, allow entries even if HTF flat: OR mild mass
    bull = bull | (sb.close > mid)
    bear = bear | (sb.close < mid)
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s09_rsi_mr(sb: SetBars):
    """S9 RSI oversold/overbought reversion."""
    r = ind.rsi(sb.close, 14)
    bull, bear = htf_force_sma(sb, 100)
    cont_l = _edge(ind.cross_up(r, pd.Series(30.0, index=r.index)))
    cont_s = _edge(ind.cross_dn(r, pd.Series(70.0, index=r.index)))
    pb_l = _edge(r < 30)
    pb_s = _edge(r > 70)
    bull = bull | (r < 40)
    bear = bear | (r > 60)
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s10_vwap_mr(sb: SetBars):
    """S10 VWAP reversion — distance from rolling VWAP proxy."""
    v = ind.vwap_proxy(sb.high, sb.low, sb.close, 48)
    dist = (sb.close - v) / v.replace(0.0, pd.NA)
    bull, bear = htf_force_sma(sb, 50)
    cont_l = _edge(ind.cross_up(sb.close, v) & (dist.shift(1) < -0.0005))
    cont_s = _edge(ind.cross_dn(sb.close, v) & (dist.shift(1) > 0.0005))
    pb_l = _edge(dist < -0.001)
    pb_s = _edge(dist > 0.001)
    bull = bull | (dist < 0)
    bear = bear | (dist > 0)
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s11_keltner_mr(sb: SetBars):
    """S11 Keltner channel reversion."""
    lo, mid, hi = ind.keltner(sb.high, sb.low, sb.close, 20, 1.5)
    bull, bear = htf_force_sma(sb, 100)
    cont_l = _edge(ind.cross_up(sb.close, mid) & (sb.close.shift(1) < lo.shift(1)))
    cont_s = _edge(ind.cross_dn(sb.close, mid) & (sb.close.shift(1) > hi.shift(1)))
    pb_l = _edge(sb.close < lo)
    pb_s = _edge(sb.close > hi)
    bull = bull | (sb.close < mid)
    bear = bear | (sb.close > mid)
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s12_zscore_mr(sb: SetBars):
    """S12 Z-score statistical reversion."""
    z = ind.zscore(sb.close, 20)
    bull, bear = htf_force_sma(sb, 100)
    cont_l = _edge(ind.cross_up(z, pd.Series(-2.0, index=z.index)))
    cont_s = _edge(ind.cross_dn(z, pd.Series(2.0, index=z.index)))
    pb_l = _edge(z < -2.0)
    pb_s = _edge(z > 2.0)
    bull = bull | (z < 0)
    bear = bear | (z > 0)
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s13_stoch_mr(sb: SetBars):
    """S13 Stochastic oscillator reversion."""
    k, d = ind.stochastic(sb.high, sb.low, sb.close, 14, 3)
    bull, bear = htf_force_sma(sb, 100)
    cont_l = _edge(ind.cross_up(k, d) & (k < 30))
    cont_s = _edge(ind.cross_dn(k, d) & (k > 70))
    pb_l = _edge(k < 20)
    pb_s = _edge(k > 80)
    bull = bull | (k < 40)
    bear = bear | (k > 60)
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


def fam_guide_s14_willr_mr(sb: SetBars):
    """S14 Williams %R extreme reversion."""
    w = ind.williams_r(sb.high, sb.low, sb.close, 14)
    bull, bear = htf_force_sma(sb, 100)
    cont_l = _edge(ind.cross_up(w, pd.Series(-80.0, index=w.index)))
    cont_s = _edge(ind.cross_dn(w, pd.Series(-20.0, index=w.index)))
    pb_l = _edge(w < -80)
    pb_s = _edge(w > -20)
    bull = bull | (w < -50)
    bear = bear | (w > -50)
    return bull.fillna(False), bear.fillna(False), (pb_l, pb_s, cont_l, cont_s)


GUIDE14_PROFILES = {
    "guide_s01_ma_cross": fam_guide_s01_ma_cross,
    "guide_s02_breakout": fam_guide_s02_breakout,
    "guide_s03_donchian_turtle": fam_guide_s03_donchian_turtle,
    "guide_s04_adx_di": fam_guide_s04_adx_di,
    "guide_s05_roc": fam_guide_s05_roc,
    "guide_s06_psar": fam_guide_s06_psar,
    "guide_s07_ema_ribbon": fam_guide_s07_ema_ribbon,
    "guide_s08_bb_mr": fam_guide_s08_bb_mr,
    "guide_s09_rsi_mr": fam_guide_s09_rsi_mr,
    "guide_s10_vwap_mr": fam_guide_s10_vwap_mr,
    "guide_s11_keltner_mr": fam_guide_s11_keltner_mr,
    "guide_s12_zscore_mr": fam_guide_s12_zscore_mr,
    "guide_s13_stoch_mr": fam_guide_s13_stoch_mr,
    "guide_s14_willr_mr": fam_guide_s14_willr_mr,
}
