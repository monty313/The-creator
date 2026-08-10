"""Mark-rational accuracy tweaks applied after base family signals.

Goal: raise Win Rate [%] while keeping non-empty trade books.
Physics: HTF force before LTF timing; session weight; small continuation TP
(first unit of progress) with wider invalidation SL (thesis fail).
"""
from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd

from . import indicators as ind
from .mtf import SetBars


# Shared FX window defaults (EURUSD-scale)
DEFAULT_TP_STOP = 0.00035  # ~3.5 pips: take first breath of move
DEFAULT_SL_STOP = 0.00090  # ~9 pips: cut when structure fails
DEFAULT_MAX_HOLD = 8  # LTF bars


def session_mask(index: pd.DatetimeIndex) -> pd.Series:
    """London + NY cash hours (UTC) — highest activity / cleanest structure."""
    h = index.hour
    # London open ~07–16, NY ~13–21 → union 07–21 UTC
    return pd.Series((h >= 7) & (h <= 21), index=index)


def htf_strength_mask(sb: SetBars, min_frac: float = 0.00015) -> Tuple[pd.Series, pd.Series]:
    """Require HTF closes away from their SMA(50) in force direction (not flat mass)."""
    m1 = ind.sma(sb.h1_close, 50)
    m2 = ind.sma(sb.h2_close, 50)
    d1 = (sb.h1_close - m1) / sb.h1_close.replace(0, np.nan)
    d2 = (sb.h2_close - m2) / sb.h2_close.replace(0, np.nan)
    bull = (d1 > min_frac) & (d2 > min_frac)
    bear = (d1 < -min_frac) & (d2 < -min_frac)
    return bull.fillna(False), bear.fillna(False)


def bar_confirms(sb: SetBars) -> Tuple[pd.Series, pd.Series]:
    """Entry bar must print with the tide (close vs open)."""
    long_ok = sb.close > sb.open
    short_ok = sb.close < sb.open
    return long_ok.fillna(False), short_ok.fillna(False)


def structure_filter(sb: SetBars) -> Tuple[pd.Series, pd.Series]:
    """Long: higher low vs prior 2; Short: lower high vs prior 2 (micro structure)."""
    hl = (sb.low >= sb.low.shift(1)) | (sb.low >= sb.low.shift(2))
    lh = (sb.high <= sb.high.shift(1)) | (sb.high <= sb.high.shift(2))
    return hl.fillna(False), lh.fillna(False)


def apply_entry_tweaks(
    sb: SetBars,
    long_e: pd.Series,
    short_e: pd.Series,
    *,
    use_session: bool = True,
    use_strength: bool = True,
    use_bar_confirm: bool = True,
    use_structure: bool = True,
) -> Tuple[pd.Series, pd.Series]:
    """Filter raw entries. Returns cleaned long/short entry masks."""
    long_e = long_e.reindex(sb.close.index).fillna(False).astype(bool)
    short_e = short_e.reindex(sb.close.index).fillna(False).astype(bool)

    mask = pd.Series(True, index=sb.close.index)
    if use_session:
        mask &= session_mask(sb.close.index)

    if use_strength:
        bull_s, bear_s = htf_strength_mask(sb)
        long_e = long_e & bull_s
        short_e = short_e & bear_s

    if use_bar_confirm:
        lc, sc = bar_confirms(sb)
        long_e = long_e & lc
        short_e = short_e & sc

    if use_structure:
        hl, lh = structure_filter(sb)
        long_e = long_e & hl
        short_e = short_e & lh

    long_e = long_e & mask
    short_e = short_e & mask
    return long_e.astype(bool), short_e.astype(bool)


def exit_masks_with_hold(
    close: pd.Series,
    long_e: pd.Series,
    short_e: pd.Series,
    max_hold: int = DEFAULT_MAX_HOLD,
) -> Tuple[pd.Series, pd.Series]:
    """Time stop + opposite signal (TP/SL handled by vectorbt stops)."""
    long_x = long_e.shift(max_hold).fillna(False) | short_e
    short_x = short_e.shift(max_hold).fillna(False) | long_e
    return long_x.astype(bool), short_x.astype(bool)


TWEAK_RATIONALE = """
### Accuracy tweaks (Mark knowledge)

1. **HTF strength filter** — dual HTF closes must sit away from SMA(50) in the trade direction.
   Flat "mass" without distance is fake permission; killed thrash entries that lose more often.

2. **Session mask (07–21 UTC)** — London/NY concentration. Off-session prints are noisier;
   removing them raises hit rate of structure-based fires.

3. **Bar confirmation** — entry bar close must agree with side (close>open for long).
   Avoids firing into a bar that already failed the release candle.

4. **Micro structure** — long only if recent higher-low texture; short if lower-high.
   Aligns with pullback-resume physics: eddy ends with constructive structure.

5. **Exit: tight TP / wider SL via vectorbt stops (no time-stop thrash)** — take the *first unit*
   of continuation (small TP), invalidate with a larger SL if thesis fails. Probability of
   tagging TP first rises when TP distance << SL distance (barrier math), *when* entries are
   not anti-edge. This is an accuracy-first scalp policy (H001-style "first breath"), not a
   claim of better expectancy under all costs.

6. **Optional time hold** — only used if configured; default accuracy path uses pure TP/SL
   so random mid-hold flats do not destroy hit rate.
"""
