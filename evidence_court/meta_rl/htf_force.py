"""HTF force: Court slope + optional Monty CCI/RSI+BB blend (lab / shadow).

Production default remains slope-only until Court PROMOTE.
When blend is on:
  - Cond1: CCI(10,30,100) each vs BB mid(10, 0.5) on BOTH HTFs
  - Cond2: RSI(5,15) each vs BB mid on BOTH HTFs
  - Strong Monty side = Cond1 OR Cond2 (conflict → 0)
  - Blend force with slope (see combine_htf_force)
  - Source flags slope_on / cci_on / rsi_on for doctrine pack (indices 12–14)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

import numpy as np

from .indicators import (
    cci,
    rsi,
    series_above_bb_mid,
    series_below_bb_mid,
    trend_dir,
)

SLOPE_LOOKBACK = 5
SLOPE_AGREE_MIN = 0.12
SLOPE_AGREE_MIN_CACHE = 0.10  # evaluate_set_edge_from_cache legacy
BB_PERIOD = 10
BB_DEV = 0.5
BB_SHIFT = 0
CCI_PERIODS = (10, 30, 100)
RSI_PERIODS = (5, 15)

# Doctrine indices (Mark doctrine 16-dim at state[32:48])
IDX_HTF_SLOPE_ON = 12
IDX_HTF_CCI_ON = 13
IDX_HTF_RSI_ON = 14
# 15 still pad


@dataclass(frozen=True)
class HtfForceResult:
    force: float
    htf_agree: bool
    slope_force: float
    slope_agree: bool
    slope_on: float  # 0 or 1 — slope permission active
    cci_on: float  # 0 or 1 — Cond1 active (either side)
    rsi_on: float  # 0 or 1 — Cond2 active
    cci_side: int  # -1, 0, +1
    rsi_side: int
    monty_side: int
    mode: str  # slope | blend
    reason: str


def _closes(bars: Sequence[dict]) -> np.ndarray:
    return np.array([float(b["close"]) for b in bars], dtype=np.float64)


def _ohlc(
    bars: Sequence[dict],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    h = np.array([float(b["high"]) for b in bars], dtype=np.float64)
    l = np.array([float(b["low"]) for b in bars], dtype=np.float64)
    c = np.array([float(b["close"]) for b in bars], dtype=np.float64)
    return h, l, c


def slope_pair_force(
    closes1: np.ndarray,
    closes2: np.ndarray,
    *,
    lookback: int = SLOPE_LOOKBACK,
    agree_min: float = SLOPE_AGREE_MIN,
    incomplete_scale: float = 0.35,
) -> Tuple[float, bool, float, float]:
    """Court slope pair → (force, agree, f1, f2)."""
    f1 = trend_dir(closes1, lookback=lookback) if closes1.size >= lookback + 1 else 0.0
    f2 = trend_dir(closes2, lookback=lookback) if closes2.size >= lookback + 1 else 0.0
    agree = (f1 * f2 > 0) and abs(f1) >= agree_min and abs(f2) >= agree_min
    force = float(np.clip(0.5 * (f1 + f2), -1.0, 1.0))
    if not agree:
        force *= float(incomplete_scale)
    return force, bool(agree), float(f1), float(f2)


def _last_all_above(series_list: List[np.ndarray]) -> bool:
    for s in series_list:
        if s.size == 0 or not np.isfinite(s[-1]):
            return False
        ab = series_above_bb_mid(s, BB_PERIOD, BB_DEV, BB_SHIFT)
        if not bool(ab[-1]):
            return False
    return True


def _last_all_below(series_list: List[np.ndarray]) -> bool:
    for s in series_list:
        if s.size == 0 or not np.isfinite(s[-1]):
            return False
        be = series_below_bb_mid(s, BB_PERIOD, BB_DEV, BB_SHIFT)
        if not bool(be[-1]):
            return False
    return True


def cci_bb_side_last(high: np.ndarray, low: np.ndarray, close: np.ndarray) -> int:
    """+1 all CCI > BB mid, -1 all < mid, else 0 (one HTF)."""
    if close.size < max(CCI_PERIODS) + BB_PERIOD + 2:
        return 0
    series = [cci(high, low, close, period=p) for p in CCI_PERIODS]
    if _last_all_above(series):
        return 1
    if _last_all_below(series):
        return -1
    return 0


def rsi_bb_side_last(close: np.ndarray) -> int:
    """+1 both RSI > BB mid, -1 both < mid, else 0 (one HTF)."""
    if close.size < max(RSI_PERIODS) + BB_PERIOD + 2:
        return 0
    series = [rsi(close, period=p) for p in RSI_PERIODS]
    if _last_all_above(series):
        return 1
    if _last_all_below(series):
        return -1
    return 0


def monty_pair_sides(
    h1: np.ndarray,
    l1: np.ndarray,
    c1: np.ndarray,
    h2: np.ndarray,
    l2: np.ndarray,
    c2: np.ndarray,
) -> Tuple[int, int, int]:
    """Return (cci_side, rsi_side, monty_side) requiring BOTH HTFs.

    monty_side = Cond1 OR Cond2 same side; Cond1 vs Cond2 conflict → 0.
    """
    cci_a = cci_bb_side_last(h1, l1, c1)
    cci_b = cci_bb_side_last(h2, l2, c2)
    cci_side = cci_a if (cci_a != 0 and cci_a == cci_b) else 0

    rsi_a = rsi_bb_side_last(c1)
    rsi_b = rsi_bb_side_last(c2)
    rsi_side = rsi_a if (rsi_a != 0 and rsi_a == rsi_b) else 0

    if cci_side != 0 and rsi_side != 0 and cci_side != rsi_side:
        monty = 0
    elif cci_side != 0:
        monty = cci_side
    elif rsi_side != 0:
        monty = rsi_side
    else:
        monty = 0
    return int(cci_side), int(rsi_side), int(monty)


def combine_htf_force(
    *,
    slope_force: float,
    slope_agree: bool,
    monty_side: int,
    cci_side: int,
    rsi_side: int,
    mode: str = "blend",
) -> HtfForceResult:
    """Blend slope + Monty into production-shaped force/agree + source flags."""
    slope_on = 1.0 if slope_agree else 0.0
    cci_on = 1.0 if cci_side != 0 else 0.0
    rsi_on = 1.0 if rsi_side != 0 else 0.0
    ms = int(monty_side)

    if mode != "blend":
        # slope-only (still report flags if computed)
        return HtfForceResult(
            force=float(np.clip(slope_force, -1.0, 1.0)),
            htf_agree=bool(slope_agree),
            slope_force=float(slope_force),
            slope_agree=bool(slope_agree),
            slope_on=slope_on,
            cci_on=cci_on,
            rsi_on=rsi_on,
            cci_side=int(cci_side),
            rsi_side=int(rsi_side),
            monty_side=ms,
            mode="slope",
            reason="slope_only",
        )

    sf = float(slope_force)
    sign_s = 1 if sf > 1e-9 else (-1 if sf < -1e-9 else 0)

    # Conflict Monty vs slope → weak / no permission
    if ms != 0 and slope_agree and sign_s != 0 and ms != sign_s:
        return HtfForceResult(
            force=float(np.clip(sf * 0.15, -1.0, 1.0)),
            htf_agree=False,
            slope_force=sf,
            slope_agree=True,
            slope_on=slope_on,
            cci_on=cci_on,
            rsi_on=rsi_on,
            cci_side=int(cci_side),
            rsi_side=int(rsi_side),
            monty_side=ms,
            mode="blend",
            reason="monty_slope_conflict",
        )

    if ms != 0 and slope_agree and (sign_s == 0 or ms == sign_s):
        force = float(np.clip(0.5 * sf + 0.5 * float(ms), -1.0, 1.0))
        return HtfForceResult(
            force=force,
            htf_agree=True,
            slope_force=sf,
            slope_agree=True,
            slope_on=slope_on,
            cci_on=cci_on,
            rsi_on=rsi_on,
            cci_side=int(cci_side),
            rsi_side=int(rsi_side),
            monty_side=ms,
            mode="blend",
            reason="monty_slope_agree",
        )

    if ms != 0:
        return HtfForceResult(
            force=float(0.65 * ms),
            htf_agree=True,
            slope_force=sf,
            slope_agree=bool(slope_agree),
            slope_on=slope_on,
            cci_on=cci_on,
            rsi_on=rsi_on,
            cci_side=int(cci_side),
            rsi_side=int(rsi_side),
            monty_side=ms,
            mode="blend",
            reason="monty_only",
        )

    if slope_agree:
        return HtfForceResult(
            force=float(np.clip(sf, -1.0, 1.0)),
            htf_agree=True,
            slope_force=sf,
            slope_agree=True,
            slope_on=1.0,
            cci_on=cci_on,
            rsi_on=rsi_on,
            cci_side=int(cci_side),
            rsi_side=int(rsi_side),
            monty_side=0,
            mode="blend",
            reason="slope_only_in_blend",
        )

    return HtfForceResult(
        force=float(np.clip(sf, -1.0, 1.0)),
        htf_agree=False,
        slope_force=sf,
        slope_agree=False,
        slope_on=0.0,
        cci_on=cci_on,
        rsi_on=rsi_on,
        cci_side=int(cci_side),
        rsi_side=int(rsi_side),
        monty_side=0,
        mode="blend",
        reason="incomplete",
    )


def compute_htf_force_from_bars(
    h1_bars: Sequence[dict],
    h2_bars: Sequence[dict],
    *,
    monty_htf_blend: bool = False,
    agree_min: float = SLOPE_AGREE_MIN,
    incomplete_scale: float = 0.35,
    # cache path extras (dual lookback) applied before blend
    dual_lookback: bool = False,
) -> HtfForceResult:
    """Main entry: two HTF bar lists → force + source flags."""
    c1 = _closes(h1_bars)
    c2 = _closes(h2_bars)
    if dual_lookback and c1.size >= 8 and c2.size >= 8:
        f1 = trend_dir(c1, lookback=5)
        f2 = trend_dir(c2, lookback=5)
        f1b = trend_dir(c1, lookback=min(10, max(c1.size - 1, 5)))
        f2b = trend_dir(c2, lookback=min(10, max(c2.size - 1, 5)))
        f1 = 0.6 * f1 + 0.4 * f1b
        f2 = 0.6 * f2 + 0.4 * f2b
        slope_agree = (f1 * f2 > 0) and abs(f1) >= agree_min and abs(f2) >= agree_min
        slope_force = float(np.clip(0.5 * (f1 + f2), -1.0, 1.0))
        if not slope_agree:
            slope_force *= float(incomplete_scale)
    else:
        slope_force, slope_agree, _, _ = slope_pair_force(
            c1,
            c2,
            lookback=SLOPE_LOOKBACK,
            agree_min=agree_min,
            incomplete_scale=incomplete_scale,
        )

    cci_side = rsi_side = monty_side = 0
    if monty_htf_blend:
        if len(h1_bars) >= 40 and len(h2_bars) >= 40:
            hh1, ll1, cc1 = _ohlc(h1_bars)
            hh2, ll2, cc2 = _ohlc(h2_bars)
            cci_side, rsi_side, monty_side = monty_pair_sides(hh1, ll1, cc1, hh2, ll2, cc2)
        return combine_htf_force(
            slope_force=slope_force,
            slope_agree=slope_agree,
            monty_side=monty_side,
            cci_side=cci_side,
            rsi_side=rsi_side,
            mode="blend",
        )

    # Slope-only: still zero Monty flags (cheap; no CCI/RSI unless blend)
    return combine_htf_force(
        slope_force=slope_force,
        slope_agree=slope_agree,
        monty_side=0,
        cci_side=0,
        rsi_side=0,
        mode="slope",
    )


def aggregate_source_flags(edges: Sequence[object]) -> Tuple[float, float, float]:
    """OR source flags across set edges (any set on → 1)."""
    slope = cci = rsi = 0.0
    for e in edges:
        slope = max(slope, float(getattr(e, "slope_on", 0.0) or 0.0))
        cci = max(cci, float(getattr(e, "cci_on", 0.0) or 0.0))
        rsi = max(rsi, float(getattr(e, "rsi_on", 0.0) or 0.0))
    return slope, cci, rsi
