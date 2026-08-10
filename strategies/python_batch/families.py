"""Strategy family adapters: OHLCV SetBars → long/short entry series for PB and cont.

Each family maps catalog *language* onto shared 2HTF+1LTF + pullback/continuation.
Fidelity notes live in FAMILY_META.
"""
from __future__ import annotations

from typing import Callable, Dict, List, Tuple

import numpy as np
import pandas as pd

from . import indicators as ind
from .mtf import (
    SetBars,
    apply_htf_gate,
    htf_force_bb_mass,
    htf_force_cci,
    htf_force_sma,
    ltf_mark_rsi_bb_modes,
)

# (pb_long, pb_short, cont_long, cont_short) under internal HTF or with external
ModeSignals = Tuple[pd.Series, pd.Series, pd.Series, pd.Series]
FamilyFn = Callable[[SetBars], Tuple[pd.Series, pd.Series, ModeSignals]]
# returns bull, bear, (pb_l, pb_s, cont_l, cont_s)


FAMILY_META: Dict[str, dict] = {}


def _reg(fid: str, **meta):
    def deco(fn):
        FAMILY_META[fid] = meta
        fn.family_id = fid  # type: ignore
        return fn

    return deco


@_reg(
    "mark_rsi_bb_l2l",
    title="Mark RSI(5)+BB on RSI under HTF BB mass",
    sources=[
        "strategies/mark_doctrine_refs/RSI_BB_L2L_SKILL.md",
        "strategies/local_desktop/rsi + bb strategy.txt",
    ],
    collapses=["rsi_bb_extreme (related)", "doctrine shift variants +2/+5"],
    fidelity="high — direct doctrine re-expression",
)
def fam_mark_rsi_bb(sb: SetBars):
    bull, bear = htf_force_bb_mass(sb)
    modes = ltf_mark_rsi_bb_modes(sb)
    return bull, bear, modes


@_reg(
    "truth_s1_cci_slingshot",
    title="S1 Dual CCI shifted-SMA slingshot",
    sources=["strategies/the_truth_main_extra/strategy_S1_cci_slingshot.md"],
    collapses=[],
    fidelity="high — from S1 language",
)
def fam_s1_cci(sb: SetBars):
    def side_above(h, l, c):
        c30 = ind.cci(h, l, c, 30)
        c100 = ind.cci(h, l, c, 100)
        s30 = ind.shifted_sma(c30, 2, 2)
        s100 = ind.shifted_sma(c100, 2, 2)
        return (c30 > s30) & (c100 > s100), (c30 < s30) & (c100 < s100)

    b1, s1 = side_above(sb.h1_high, sb.h1_low, sb.h1_close)
    b2, s2 = side_above(sb.h2_high, sb.h2_low, sb.h2_close)
    bull, bear = b1 & b2, s1 & s2
    c30 = ind.cci(sb.high, sb.low, sb.close, 30)
    c100 = ind.cci(sb.high, sb.low, sb.close, 100)
    s30 = ind.shifted_sma(c30, 2, 2)
    s100 = ind.shifted_sma(c100, 2, 2)
    # pullback: HTF above, LTF fast CCI below its SMA (tension)
    pb_l = (c100 > s100) & (c30 < s30)
    pb_s = (c100 < s100) & (c30 > s30)
    # continuation: all above
    cont_l = (c100 > s100) & (c30 > s30)
    cont_s = (c100 < s100) & (c30 < s30)
    # edge as cross into state
    cont_l = cont_l & ~cont_l.shift(1).fillna(False)
    cont_s = cont_s & ~cont_s.shift(1).fillna(False)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l, pb_s, cont_l, cont_s)


@_reg(
    "truth_s2_bb_trend_reversion",
    title="S2 Dual Bollinger trend reversion / dip inside tunnel",
    sources=["strategies/the_truth_main_extra/strategy_S2_bb_trend_reversion.md"],
    collapses=[],
    fidelity="high",
)
def fam_s2_bb(sb: SetBars):
    def htf_escape(c):
        lo100, m100, hi100 = ind.bollinger(c, 100, 0.5, 2)
        lo10, m10, hi10 = ind.bollinger(c, 10, 0.5, 2)
        bull = (c > hi100) & (c > hi10)
        bear = (c < lo100) & (c < lo10)
        return bull, bear

    b1, s1 = htf_escape(sb.h1_close)
    b2, s2 = htf_escape(sb.h2_close)
    bull, bear = b1 & b2, s1 & s2
    lo100, _, hi100 = ind.bollinger(sb.close, 100, 0.5, 2)
    lo10, _, hi10 = ind.bollinger(sb.close, 10, 0.5, 2)
    # pullback: still extreme vs slow, re-enter inside fast
    pb_l = (sb.close > hi100) & (sb.close < hi10)
    pb_s = (sb.close < lo100) & (sb.close > lo10)
    cont_l = ind.cross_up(sb.close, hi10)
    cont_s = ind.cross_dn(sb.close, lo10)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "truth_s3_envelope_breakout",
    title="S3 Shifted high/low envelope breakout",
    sources=["strategies/the_truth_main_extra/strategy_S3_envelope_breakout.md"],
    collapses=["shifted_sma channel (ATI cousin)"],
    fidelity="high",
)
def fam_s3_env(sb: SetBars):
    def env(h, l, c, sh):
        top = ind.shifted_sma(h, 4, sh)
        bot = ind.shifted_sma(l, 4, sh)
        return (c > top) & (c > bot), (c < top) & (c < bot)

    b1, s1 = env(sb.h1_high, sb.h1_low, sb.h1_close, 4)
    b2, s2 = env(sb.h2_high, sb.h2_low, sb.h2_close, 4)
    bull, bear = b1 & b2, s1 & s2
    top = ind.shifted_sma(sb.high, 4, 2)
    bot = ind.shifted_sma(sb.low, 4, 2)
    above = (sb.close > top) & (sb.close > bot)
    below = (sb.close < top) & (sb.close < bot)
    cont_l = above & ~above.shift(1).fillna(False)
    cont_s = below & ~below.shift(1).fillna(False)
    # pullback: retest of envelope after break
    pb_l = (sb.close > top.shift(1)) & (sb.low <= top) & (sb.close > top)
    pb_s = (sb.close < bot.shift(1)) & (sb.high >= bot) & (sb.close < bot)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l, cont_s)


@_reg(
    "truth_s4_rsi_tension_snap",
    title="S4 RSI Bollinger tension snap",
    sources=["strategies/the_truth_main_extra/strategy_S4_rsi_tension_snap.md"],
    collapses=[],
    fidelity="high",
)
def fam_s4_rsi_snap(sb: SetBars):
    def htf_rsi_extreme(c):
        r2 = ind.rsi(c, 2)
        r20 = ind.rsi(c, 20)
        lo2, m2, hi2 = ind.bollinger(r2, 20, 0.5, 2)
        lo20, m20, hi20 = ind.bollinger(r20, 20, 0.5, 2)
        bull = (r2 > hi2) & (r20 > hi20)
        bear = (r2 < lo2) & (r20 < lo20)
        return bull, bear

    b1, s1 = htf_rsi_extreme(sb.h1_close)
    b2, s2 = htf_rsi_extreme(sb.h2_close)
    bull, bear = b1 & b2, s1 & s2
    r2 = ind.rsi(sb.close, 2)
    r20 = ind.rsi(sb.close, 20)
    lo2, m2, hi2 = ind.bollinger(r2, 20, 0.5, 2)
    lo20, m20, hi20 = ind.bollinger(r20, 20, 0.5, 2)
    pb_l = (r20 > m20) & (r2 < lo2)
    pb_s = (r20 < m20) & (r2 > hi2)
    cont_l = ind.cross_up(r2, m2)
    cont_s = ind.cross_dn(r2, m2)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


def _cci_momentum_line(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    """CCI analogue of McFlurry M-line: smooth CCI then SMA7−SMA21."""
    x = ind.cci(high, low, close, 20)
    x = ind.sma(x, 2)
    return ind.sma(x, 7) - ind.sma(x, 21)


@_reg(
    "cci_gravity_scalp",
    title="CCI gravity scalp (upgraded reclaim M-line)",
    sources=[
        "language/01_METATRADER.md#cci_gravity_scalp_ftmo",
        "MT5 Experts/cci_gravity_scalp_*.mq5",
        "strategies/CCI_VS_MCFLURRY_REPORT.md",
    ],
    collapses=[],
    fidelity="high — CCI M-line dual-HTF force + reclaim-only fire",
)
def fam_cci_gravity(sb: SetBars):
    """CCI gravity (upgraded): dual-HTF CCI-momentum force + LTF reclaim-only fire.

    Never enter on the dip itself — only after load then cross back through 0
    (same eddy physics as H001 McFlurry, on CCI instead of RSI).
    """
    thr = 8.0  # genuine-force filter on HTF1 M-line magnitude
    m1 = _cci_momentum_line(sb.h1_high, sb.h1_low, sb.h1_close)
    m2 = _cci_momentum_line(sb.h2_high, sb.h2_low, sb.h2_close)
    m = _cci_momentum_line(sb.high, sb.low, sb.close)
    bull = (m1 > 0) & (m2 > 0) & (m1 >= thr)
    bear = (m1 < 0) & (m2 < 0) & (m1 <= -thr)
    z = pd.Series(0.0, index=m.index)
    was_neg = m.rolling(8, min_periods=1).min() < 0
    was_pos = m.rolling(8, min_periods=1).max() > 0
    # reclaim-only (both PB and cont labels): fire after load, not into the eddy
    fire_l = was_neg & ind.cross_up(m, z)
    fire_s = was_pos & ind.cross_dn(m, z)
    return (
        bull.fillna(False),
        bear.fillna(False),
        (fire_l.fillna(False), fire_s.fillna(False), fire_l.fillna(False), fire_s.fillna(False)),
    )


@_reg(
    "ftmo_bb_mtf_strategy4",
    title="FTMO BB multi-TF Strategy4 family",
    sources=["language/01_METATRADER.md — FTMO_BB_MTF_EA_Strategy4*"],
    collapses=[
        "FTMO_BB_MTF_EA_Strategy4 v1–v7",
        "fixed_FTMO_BB_MTF_EA_Strategy4_v2",
        "FTMO_CCI_MTF_BB_EA Part2/3",
        "agent teacher",
    ],
    fidelity="medium — BB+CCI MTF tags collapsed",
)
def fam_bb_mtf(sb: SetBars):
    bull, bear = htf_force_bb_mass(sb, n=20, dev=2.0, shift=0)
    lo, mid, hi = ind.bollinger(sb.close, 20, 2.0, 0)
    r = ind.rsi(sb.close, 14)
    pb_l = (sb.close < lo) & (r < 35)
    pb_s = (sb.close > hi) & (r > 65)
    cont_l = ind.cross_up(sb.close, mid) & (r > 50)
    cont_s = ind.cross_dn(sb.close, mid) & (r < 50)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "cool_bollinger_trend",
    title="Cool Bollinger trend / breakout",
    sources=["language CoolBollingerTrendEA / coolboolinger"],
    collapses=["CoolBollingerTrendEA", "coolboolinger"],
    fidelity="medium",
)
def fam_cool_bb(sb: SetBars):
    bull, bear = htf_force_sma(sb, 50)
    lo, mid, hi = ind.bollinger(sb.close, 20, 2.0, 0)
    cont_l = ind.cross_up(sb.close, hi)
    cont_s = ind.cross_dn(sb.close, lo)
    pb_l = (sb.close < mid) & (sb.close > lo) & bull
    pb_s = (sb.close > mid) & (sb.close < hi) & bear
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "ftmo_sma_scalper",
    title="FTMO SMA cascade scalper + RSI exit language",
    sources=["language FTMO_SMA_Scalper"],
    collapses=["FTMO_SMA_Scalper", "SMA_Fan_MTF_BBExit_v1", "TriTF_SMA_Shift_Optimizer_EA"],
    fidelity="medium",
)
def fam_sma_scalp(sb: SetBars):
    bull, bear = htf_force_sma(sb, 100)
    f, s, sl = ind.sma(sb.close, 8), ind.sma(sb.close, 21), ind.sma(sb.close, 50)
    r = ind.rsi(sb.close, 14)
    ribbon_up = (f > s) & (s > sl)
    ribbon_dn = (f < s) & (s < sl)
    pb_l = ribbon_up & (sb.low <= s) & (sb.close > s) & (r < 55)
    pb_s = ribbon_dn & (sb.high >= s) & (sb.close < s) & (r > 45)
    cont_l = ind.cross_up(f, s) & ribbon_up
    cont_s = ind.cross_dn(f, s) & ribbon_dn
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "kinetic_edge_bb_cci",
    title="KineticEdge BB breakout + triple CCI momentum",
    sources=["language KineticEdgeEA"],
    collapses=[],
    fidelity="medium",
)
def fam_kinetic(sb: SetBars):
    bull, bear = htf_force_cci(sb, 14)
    lo, mid, hi = ind.bollinger(sb.close, 20, 2.0, 0)
    c = ind.cci(sb.high, sb.low, sb.close, 14)
    cont_l = ind.cross_up(sb.close, hi) & (c > 0)
    cont_s = ind.cross_dn(sb.close, lo) & (c < 0)
    pb_l = (sb.close < mid) & (c > -100) & (c < 0) & bull
    pb_s = (sb.close > mid) & (c < 100) & (c > 0) & bear
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "jordan_momentum_matrix",
    title="Jordan momentum matrix (CCI / BB / SMA channel)",
    sources=["language JordanMomentumScreener_v2…v11"],
    collapses=[f"JordanMomentumScreener_v{v}" for v in [2, 4, 5, 7, 8, 9, 10, 11]]
    + ["play 4.2", "play 4.3", "Unity Play", "Momentum_Matrix_Screener"],
    fidelity="medium — matrix collapsed to CCI+BB+SMA channel filter stack",
)
def fam_jordan(sb: SetBars):
    bull_c, bear_c = htf_force_cci(sb, 20)
    bull_s, bear_s = htf_force_sma(sb, 50)
    bull, bear = (bull_c | bull_s), (bear_c | bear_s)
    lo, mid, hi = ind.bollinger(sb.close, 20, 2.0, 0)
    c = ind.cci(sb.high, sb.low, sb.close, 20)
    sma20 = ind.sma(sb.close, 20)
    pb_l = (sb.close < sma20) & (sb.close > lo) & (c < 0)
    pb_s = (sb.close > sma20) & (sb.close < hi) & (c > 0)
    cont_l = ind.cross_up(c, pd.Series(0.0, index=c.index)) & (sb.close > mid)
    cont_s = ind.cross_dn(c, pd.Series(0.0, index=c.index)) & (sb.close < mid)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "zero_line_radar_cci",
    title="ZeroLineRadar multi-TF CCI zero-line",
    sources=["language ZeroLineRadar*"],
    collapses=["ZeroLineRadar", "ZeroLineRadar0works", "Zerolineradar1", "Pure_CCI_Screener", "NN_CCI_Screener"],
    fidelity="medium",
)
def fam_zlr(sb: SetBars):
    return fam_cci_gravity(sb)


@_reg(
    "fasg_trendday",
    title="FASG trendday pullback/breakout",
    sources=["language fasg_trendday_ea", "FableAutonomousStrategyGenerator/fasg"],
    collapses=[],
    fidelity="medium",
)
def fam_fasg(sb: SetBars):
    bull, bear = htf_force_sma(sb, 50)
    atrv = ind.atr(sb.high, sb.low, sb.close, 14)
    rng = (sb.high - sb.low)
    cont_l = (sb.close > sb.open) & (rng > atrv) & bull
    cont_s = (sb.close < sb.open) & (rng > atrv) & bear
    pb_l = bull & (sb.close < ind.sma(sb.close, 20)) & (sb.close > ind.sma(sb.close, 50))
    pb_s = bear & (sb.close > ind.sma(sb.close, 20)) & (sb.close < ind.sma(sb.close, 50))
    cont_l = cont_l & ~cont_l.shift(1).fillna(False)
    cont_s = cont_s & ~cont_s.shift(1).fillna(False)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "snap8_nested_pullback",
    title="SNAP-8 nested EMA ribbon + RSI reclaim",
    sources=["strategies/army_snap8/STRATEGY.md"],
    collapses=[],
    fidelity="high — from SNAP-8 doc (mapped onto 2HTF of each official set)",
)
def fam_snap8(sb: SetBars):
    # HTF bias ~ higher SMAs
    bull, bear = htf_force_sma(sb, 50)
    f, s = ind.ema(sb.close, 8), ind.ema(sb.close, 21)
    r = ind.rsi(sb.close, 7)
    pb_l = (f > s) & (sb.low <= f) & (sb.close >= f) & (r < 50)
    pb_s = (f < s) & (sb.high >= f) & (sb.close <= f) & (r > 50)
    cont_l = ind.cross_up(r, pd.Series(50.0, index=r.index)) & (f > s) & (sb.close > f)
    cont_s = ind.cross_dn(r, pd.Series(50.0, index=r.index)) & (f < s) & (sb.close < f)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "gv014_gravity_snap",
    title="GV-014 Gravity Snap (factory)",
    sources=["strategies/local_desktop/factory_full/GV-014-XAU-L1.md"],
    collapses=["gravity_engine strategy language"],
    fidelity="low-medium — name/theme only from notes",
)
def fam_gv014(sb: SetBars):
    bull, bear = htf_force_bb_mass(sb, n=50, dev=0.5, shift=2)
    mid = ind.sma(sb.close, 20)
    # snap: reclaim mid after stretch
    z = (sb.close - mid) / (ind.atr(sb.high, sb.low, sb.close, 14).replace(0, np.nan))
    pb_l = (z < -1.0) & ind.cross_up(sb.close, mid)
    pb_s = (z > 1.0) & ind.cross_dn(sb.close, mid)
    cont_l = ind.cross_up(sb.close, mid) & bull
    cont_s = ind.cross_dn(sb.close, mid) & bear
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "gv015_tunnel_rider",
    title="GV-015 Tunnel Rider (factory)",
    sources=["strategies/local_desktop/factory_full (GV015_tunnel_rider.pine name)"],
    collapses=[],
    fidelity="low-medium — theme: ride BB tunnel",
)
def fam_gv015(sb: SetBars):
    bull, bear = htf_force_sma(sb, 50)
    lo, mid, hi = ind.bollinger(sb.close, 20, 0.5, 0)
    cont_l = (sb.close > mid) & (sb.close < hi) & bull & (sb.close > sb.close.shift(1))
    cont_s = (sb.close < mid) & (sb.close > lo) & bear & (sb.close < sb.close.shift(1))
    pb_l = ind.cross_up(sb.close, lo) & bull
    pb_s = ind.cross_dn(sb.close, hi) & bear
    cont_l = cont_l & ~cont_l.shift(1).fillna(False)
    cont_s = cont_s & ~cont_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "ati_shifted_sma_channel",
    title="ATI shifted SMA channel",
    sources=["language 02_MACHINE ATI shifted_sma"],
    collapses=["shifted_sma.py", "wave_and_cci partial"],
    fidelity="medium",
)
def fam_ati_sma(sb: SetBars):
    bull, bear = htf_force_sma(sb, 50)
    ch = ind.shifted_sma(sb.close, 20, 2)
    pb_l = (sb.low <= ch) & (sb.close > ch) & bull
    pb_s = (sb.high >= ch) & (sb.close < ch) & bear
    cont_l = ind.cross_up(sb.close, ch)
    cont_s = ind.cross_dn(sb.close, ch)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "ati_gold_orb",
    title="Gold / session ORB language",
    sources=["language gold_orb_sc.py"],
    collapses=["London_Breakout public cousin"],
    fidelity="medium — opening range on LTF session proxy",
)
def fam_orb(sb: SetBars):
    bull, bear = htf_force_sma(sb, 50)
    # proxy ORB: first N bars of each UTC day high/low break
    day = sb.close.index.floor("D")
    # rolling session range via group transform is heavy; use 30-bar range break
    hi30 = sb.high.rolling(30).max().shift(1)
    lo30 = sb.low.rolling(30).min().shift(1)
    cont_l = ind.cross_up(sb.close, hi30)
    cont_s = ind.cross_dn(sb.close, lo30)
    pb_l = (sb.close > hi30) & (sb.low <= hi30) & (sb.close > hi30)
    pb_s = (sb.close < lo30) & (sb.high >= lo30) & (sb.close < lo30)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "public_london_breakout",
    title="Public London breakout idea (je-suis-tm)",
    sources=["language/03_PUBLIC_SOURCES.md — je-suis-tm London Breakout", "https://github.com/je-suis-tm/quant-trading"],
    collapses=[],
    fidelity="medium — session range proxy not true London calendar",
)
def fam_london(sb: SetBars):
    return fam_orb(sb)


@_reg(
    "public_dual_thrust",
    title="Public Dual Thrust range breakout",
    sources=["https://github.com/je-suis-tm/quant-trading Dual_Thrust"],
    collapses=[],
    fidelity="medium",
)
def fam_dual_thrust(sb: SetBars):
    bull, bear = htf_force_sma(sb, 50)
    hh = sb.high.rolling(20).max()
    ll = sb.low.rolling(20).min()
    cl = sb.close.rolling(20).max()
    cs = sb.close.rolling(20).min()
    rng = pd.concat([hh - cs, cl - ll], axis=1).max(axis=1)
    buy_line = sb.open + 0.5 * rng.shift(1)
    sell_line = sb.open - 0.5 * rng.shift(1)
    cont_l = ind.cross_up(sb.close, buy_line)
    cont_s = ind.cross_dn(sb.close, sell_line)
    pb_l = (sb.close > buy_line) & (sb.low <= buy_line)
    pb_s = (sb.close < sell_line) & (sb.high >= sell_line)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "public_supertrend",
    title="Public Supertrend filter idea",
    sources=["language/03_PUBLIC_SOURCES.md Supertrend", "freqtrade Supertrend.py", "vectorbt supertrend"],
    collapses=["freqtrade Supertrend"],
    fidelity="medium — ATR channel direction proxy",
)
def fam_supertrend(sb: SetBars):
    a = ind.atr(sb.high, sb.low, sb.close, 10)
    hl2 = (sb.high + sb.low) / 2.0
    upper = hl2 + 3 * a
    lower = hl2 - 3 * a
    # simple: close vs mid ATR band
    mid = hl2
    bull_l = sb.close > mid
    # HTF: both HTF closes above their SMA
    bull, bear = htf_force_sma(sb, 30)
    cont_l = ind.cross_up(sb.close, upper)
    cont_s = ind.cross_dn(sb.close, lower)
    pb_l = bull & (sb.low <= mid) & (sb.close > mid)
    pb_s = bear & (sb.high >= mid) & (sb.close < mid)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "public_donchian",
    title="Public Donchian channel breakout",
    sources=["language/03_PUBLIC_SOURCES.md donchian_backtest", "https://github.com/polakowo/vectorbt"],
    collapses=[],
    fidelity="high-medium — classic Donchian",
)
def fam_donchian(sb: SetBars):
    bull, bear = htf_force_sma(sb, 50)
    lo, hi = ind.donchian(sb.high, sb.low, 20)
    cont_l = ind.cross_up(sb.close, hi.shift(1))
    cont_s = ind.cross_dn(sb.close, lo.shift(1))
    mid = (lo + hi) / 2
    pb_l = bull & (sb.low <= mid) & (sb.close > mid)
    pb_s = bear & (sb.high >= mid) & (sb.close < mid)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "public_bband_rsi",
    title="Public BbandRsi / freqtrade mean-reversion style",
    sources=["language/03_PUBLIC_SOURCES.md BbandRsi", "https://github.com/freqtrade/freqtrade-strategies"],
    collapses=["Bandtastic", "Low_BB", "MultiRSI", "BbandRsi"],
    fidelity="medium — RSI14+BB20 classic not Mark RSI5",
)
def fam_bband_rsi(sb: SetBars):
    bull, bear = htf_force_sma(sb, 100)
    lo, mid, hi = ind.bollinger(sb.close, 20, 2.0, 0)
    r = ind.rsi(sb.close, 14)
    # mean reversion: pb at band, cont as reclaim mid
    pb_l = (sb.close < lo) & (r < 30)
    pb_s = (sb.close > hi) & (r > 70)
    cont_l = ind.cross_up(sb.close, mid) & (r > 40)
    cont_s = ind.cross_dn(sb.close, mid) & (r < 60)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "macd_sample",
    title="MT4 MACD Sample language",
    sources=["language MACD Sample.mq4"],
    collapses=[],
    fidelity="high-medium — classic MACD sample",
)
def fam_macd(sb: SetBars):
    bull, bear = htf_force_sma(sb, 50)
    line, sig, hist = ind.macd(sb.close)
    cont_l = ind.cross_up(line, sig)
    cont_s = ind.cross_dn(line, sig)
    pb_l = bull & (hist < 0) & (hist > hist.shift(1))
    pb_s = bear & (hist > 0) & (hist < hist.shift(1))
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "moving_average_sample",
    title="MT4 Moving Average sample",
    sources=["language Moving Average.mq4"],
    collapses=[],
    fidelity="high-medium",
)
def fam_ma_sample(sb: SetBars):
    bull, bear = htf_force_sma(sb, 100)
    m = ind.sma(sb.close, 12)
    cont_l = ind.cross_up(sb.close, m)
    cont_s = ind.cross_dn(sb.close, m)
    pb_l = bull & (sb.low <= m) & (sb.close > m)
    pb_s = bear & (sb.high >= m) & (sb.close < m)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "linear_regression_rsi",
    title="Linear regression + RSI language",
    sources=["language LinearRegressionRSI_EA", "Linear_Regression_Screener"],
    collapses=["LinearRegressionLine", "RegressionlineEA", "Linear_Regression_Screener"],
    fidelity="medium — linreg slope proxy via SMA slope",
)
def fam_linreg(sb: SetBars):
    bull, bear = htf_force_sma(sb, 50)
    m = ind.sma(sb.close, 20)
    slope = m - m.shift(5)
    r = ind.rsi(sb.close, 14)
    cont_l = (slope > 0) & ind.cross_up(r, pd.Series(50.0, index=r.index))
    cont_s = (slope < 0) & ind.cross_dn(r, pd.Series(50.0, index=r.index))
    pb_l = bull & (slope > 0) & (r < 40)
    pb_s = bear & (slope < 0) & (r > 60)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "ma_ribbon_mt4",
    title="MA ribbon filled alerts (MT4 template)",
    sources=["language MA ribbon filled_Alerts.mq4"],
    collapses=[],
    fidelity="medium",
)
def fam_ma_ribbon(sb: SetBars):
    bull, bear = htf_force_sma(sb, 50)
    e8, e21, e55 = ind.ema(sb.close, 8), ind.ema(sb.close, 21), ind.ema(sb.close, 55)
    up = (e8 > e21) & (e21 > e55)
    dn = (e8 < e21) & (e21 < e55)
    cont_l = up & ~up.shift(1).fillna(False)
    cont_s = dn & ~dn.shift(1).fillna(False)
    pb_l = up & (sb.low <= e21) & (sb.close > e21)
    pb_s = dn & (sb.high >= e21) & (sb.close < e21)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "rl_blackbox_proxy",
    title="RL/NN EA blackbox proxy (RSI+HTF mass)",
    sources=[
        "language @@FTMO_DQN@@, OnlineLearnerEA, MultiTimeframe_NN_EA, PerceptronEA, Q-learning, MetaLearningEA, RL_PropTrader_*",
    ],
    collapses=[
        "@@FTMO_DQN@@",
        "FTMO_DQN",
        "OnlineLearnerEA*",
        "MultiTimeframe_NN_EA*",
        "PerceptronEA",
        "Q-learning",
        "MetaLearningEA",
        "RL_PropTrader_*",
        "MQL5 RL EA",
        "NeuralNetworkScreener*",
        "AutoTradingBot_RF",
        "PDF_MultiStrategy*",
    ],
    fidelity="low — weights unavailable; proxy is Mark-like RSI-BB under mass (teaching baseline only)",
)
def fam_rl_proxy(sb: SetBars):
    return fam_mark_rsi_bb(sb)


@_reg(
    "momentum_mtf_generic",
    title="Generic MTF momentum EA language",
    sources=["language Momentum.mq5", "ftmo_all_assets_momentum_scalper", "ftmo ultra"],
    collapses=["Momentum", "ftmo_all_assets_momentum_scalper", "ftmo ultra", "Simple scalper", "US30_ExpansionTrigger_v1"],
    fidelity="medium",
)
def fam_mom_mtf(sb: SetBars):
    bull, bear = htf_force_sma(sb, 50)
    mom = sb.close - sb.close.shift(10)
    r = ind.rsi(sb.close, 14)
    cont_l = (mom > 0) & ind.cross_up(r, pd.Series(55.0, index=r.index))
    cont_s = (mom < 0) & ind.cross_dn(r, pd.Series(45.0, index=r.index))
    pb_l = bull & (mom > 0) & (r < 45) & (r > r.shift(1))
    pb_s = bear & (mom < 0) & (r > 55) & (r < r.shift(1))
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return bull, bear, (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False))


@_reg(
    "challenge_ea_stack",
    title="FTMO Challenge EA multi-step stack (BB+CCI+SMA)",
    sources=["language FTMO_Challenge_*"],
    collapses=["FTMO_Challenge_EA", "FTMO_Challenge_EA_FULL", "ftmo_challenge_ea_v3", "FTMO_Challenge_v4", "FtmoDecisionTree", "S11_Runner"],
    fidelity="medium — combined stack approximation",
)
def fam_challenge(sb: SetBars):
    # combine mass + cci gate
    b1, s1 = htf_force_bb_mass(sb, 50, 0.5, 2)
    b2, s2 = htf_force_cci(sb, 20)
    bull, bear = b1 & b2, s1 & s2
    modes = ltf_mark_rsi_bb_modes(sb)
    return bull, bear, modes


def _mcflurry_M(close: pd.Series) -> pd.Series:
    """McFlurry momentum line: RSI(13) → SMA7 − SMA21 of RSI (H001; SMA2 smooth optional)."""
    r = ind.rsi(close, 13)
    r = ind.sma(r, 2)  # mild smooth from full stack language
    return ind.sma(r, 7) - ind.sma(r, 21)


@_reg(
    "mcflurry_eddy_scalp",
    title="McFlurry Eddy trend-pullback scalp (H001)",
    sources=[
        "strategies/sauces/H001_mcflurry_eddy_scalp.md",
        "Fable5 MOMENTUM_ONE hypotheses/H001_mcflurry_eddy_scalp.md",
    ],
    collapses=[],
    fidelity="high — H001 rules on official-set HTFs/LTF",
)
def fam_mcflurry(sb: SetBars):
    # H001: context M on both HTFs; genuine filter |M_htf1| >= 1.5; LTF eddy below 0 then reclaim
    m1 = _mcflurry_M(sb.h1_close)
    m2 = _mcflurry_M(sb.h2_close)
    m_ltf = _mcflurry_M(sb.close)
    thr = 1.5
    bull = (m1 > 0) & (m2 > 0) & (m1 >= thr)
    bear = (m1 < 0) & (m2 < 0) & (m1 <= -thr)
    # pullback = dip: M crosses below 0 (long context) / above 0 (short)
    pb_l = ind.cross_dn(m_ltf, pd.Series(0.0, index=m_ltf.index))
    pb_s = ind.cross_up(m_ltf, pd.Series(0.0, index=m_ltf.index))
    # continuation / fire = snap back through 0
    cont_l = ind.cross_up(m_ltf, pd.Series(0.0, index=m_ltf.index))
    cont_s = ind.cross_dn(m_ltf, pd.Series(0.0, index=m_ltf.index))
    return (
        bull.fillna(False),
        bear.fillna(False),
        (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False)),
    )


@_reg(
    "dimension_jump_sauce",
    title="Dimension Jump sauce (CCI + BB-on-CCI) — McFlurry pair",
    sources=[
        "strategies/sauces/DimensionJump_sauce.md",
        "MOMENTUM_ONE OBSERVATIONAL_INDICATOR_UNIVERSE / ML_CONFIRMATION_FLOW",
        "ADR-0004 sauces pair",
    ],
    collapses=[],
    fidelity="high-medium — sauce stack as entry geometry under official sets",
)
def fam_dimension_jump(sb: SetBars):
    def force_side(h, l, c):
        c100 = ind.cci(h, l, c, 100)
        _, mid100, _ = ind.bollinger(c100, 20, 1.0, 2)
        bull = c100 > mid100
        bear = c100 < mid100
        return bull, bear

    b1, s1 = force_side(sb.h1_high, sb.h1_low, sb.h1_close)
    b2, s2 = force_side(sb.h2_high, sb.h2_low, sb.h2_close)
    bull, bear = b1 & b2, s1 & s2
    c30 = ind.cci(sb.high, sb.low, sb.close, 30)
    lo30, mid30, hi30 = ind.bollinger(c30, 20, 1.0, 2)
    # pullback: dimension dips through mid / outside far band
    pb_l = ind.cross_dn(c30, mid30) | ((c30 < lo30) & (c30 > c30.shift(1)))
    pb_s = ind.cross_up(c30, mid30) | ((c30 > hi30) & (c30 < c30.shift(1)))
    # continuation: reclaim mid
    cont_l = ind.cross_up(c30, mid30)
    cont_s = ind.cross_dn(c30, mid30)
    pb_l = pb_l & ~pb_l.shift(1).fillna(False)
    pb_s = pb_s & ~pb_s.shift(1).fillna(False)
    return (
        bull.fillna(False),
        bear.fillna(False),
        (pb_l.fillna(False), pb_s.fillna(False), cont_l.fillna(False), cont_s.fillna(False)),
    )


# Registry list in stable order
ALL_FAMILIES: List[Tuple[str, FamilyFn]] = [
    (fn.family_id, fn)  # type: ignore
    for fn in [
        fam_mark_rsi_bb,
        fam_s1_cci,
        fam_s2_bb,
        fam_s3_env,
        fam_s4_rsi_snap,
        fam_cci_gravity,
        fam_bb_mtf,
        fam_cool_bb,
        fam_sma_scalp,
        fam_kinetic,
        fam_jordan,
        fam_zlr,
        fam_fasg,
        fam_snap8,
        fam_gv014,
        fam_gv015,
        fam_ati_sma,
        fam_orb,
        fam_london,
        fam_dual_thrust,
        fam_supertrend,
        fam_donchian,
        fam_bband_rsi,
        fam_macd,
        fam_ma_sample,
        fam_linreg,
        fam_ma_ribbon,
        fam_rl_proxy,
        fam_mom_mtf,
        fam_challenge,
        fam_mcflurry,
        fam_dimension_jump,
    ]
]


def entries_for_mode(sb: SetBars, fam: FamilyFn, mode: str) -> tuple[pd.Series, pd.Series]:
    bull, bear, modes = fam(sb)
    pb_l, pb_s, cont_l, cont_s = modes
    return apply_htf_gate(bull, bear, pb_l, pb_s, cont_l, cont_s, mode)
