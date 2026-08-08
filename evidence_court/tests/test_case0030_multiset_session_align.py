"""CASE-0030 NEW tests: multi-set eases same-day session path confirm."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    CONT_HOLD_MIN_MINUTES,
    DEFAULT_SESSION_MIN_ALIGN,
    PRODUCTION_CADENCE_INTERVAL_MIN,
    PRODUCTION_SCALPING_SLOTS,
    allows_empty_slot_skip,
    fill_hold_end_time,
    production_symbols_per_slot,
    session_confirms_side,
    session_min_align_for_path,
)


def _bars_path(date: str, *, up: bool, n: int = 40, entry: float = 2000.0):
    bars = []
    for i in range(n):
        t = f"{8 + i // 60:02d}:{i % 60:02d}:00"
        frac = i / max(n - 1, 1)
        px = entry * (1.0 + (0.0005 if up else -0.0005) * frac)
        bars.append(
            {
                "date": date,
                "time": t,
                "open": entry if i == 0 else bars[-1]["close"],
                "high": px * 1.0001,
                "low": px * 0.9999,
                "close": px,
            }
        )
    return bars


def test_creator_new_multiset_eases_session_min_align():
    """Creator NEW: multi-set agree zeros session min_align; non-multi keeps default."""
    assert session_min_align_for_path(multi_set_agree=True) == 0.0
    assert session_min_align_for_path(multi_set_agree=False) == DEFAULT_SESSION_MIN_ALIGN
    assert DEFAULT_SESSION_MIN_ALIGN > 0.0


def test_mark_new_non_multiset_session_floor_kept():
    """Mark NEW: without multi-set, default align still filters counter-path."""
    down = _bars_path("2026-01-02", up=False)
    # Counter long on down day: blocked at default align
    assert (
        session_confirms_side(
            down,
            date="2026-01-02",
            asof_time="10:00:00",
            side=1,
            min_align=session_min_align_for_path(multi_set_agree=False),
        )
        is False
    )
    # Multi-set ease: min_align 0 still requires non-positive move for short? 
    # side=1 long on down day: move negative → still False even at 0
    assert (
        session_confirms_side(
            down,
            date="2026-01-02",
            asof_time="10:00:00",
            side=1,
            min_align=0.0,
        )
        is False
    )


def test_creator_new_session_confirm_zero_align_still_side_aware():
    """Creator counter NEW: min_align=0 still requires correct sign of session move."""
    up = _bars_path("2026-01-03", up=True)
    down = _bars_path("2026-01-03", up=False)
    assert session_confirms_side(
        up, date="2026-01-03", asof_time="10:00:00", side=1, min_align=0.0
    )
    assert not session_confirms_side(
        up, date="2026-01-03", asof_time="10:00:00", side=-1, min_align=0.0
    )
    assert session_confirms_side(
        down, date="2026-01-03", asof_time="10:00:00", side=-1, min_align=0.0
    )
    # Mild multi-set path: lean almost flat but slightly long — default may fail, 0 passes long
    flatish = _bars_path("2026-01-04", up=True, n=40, entry=100.0)
    # tiny move: rewrite last closes closer to open
    o = float(flatish[0]["open"])
    for i, b in enumerate(flatish):
        # total move ~ 0.5e-4 (below DEFAULT 1.5e-4)
        px = o * (1.0 + 0.5e-4 * (i / max(len(flatish) - 1, 1)))
        b["close"] = px
        b["high"] = px * 1.00001
        b["low"] = px * 0.99999
        if i > 0:
            b["open"] = flatish[i - 1]["close"]
    assert not session_confirms_side(
        flatish,
        date="2026-01-04",
        asof_time="10:00:00",
        side=1,
        min_align=DEFAULT_SESSION_MIN_ALIGN,
    )
    assert session_confirms_side(
        flatish,
        date="2026-01-04",
        asof_time="10:00:00",
        side=1,
        min_align=0.0,
    )


def test_mark_new_a27_a26_geometry_preserved():
    """Mark counter NEW: A27 5m + A26 hold + 1-sym + empty skip preserved."""
    assert PRODUCTION_CADENCE_INTERVAL_MIN == 5
    assert "07:05:00" in PRODUCTION_SCALPING_SLOTS
    assert CONT_HOLD_MIN_MINUTES == 30
    assert fill_hold_end_time(
        "continuation", "07:00:00", PRODUCTION_SCALPING_SLOTS
    ) == "07:30:00"
    assert production_symbols_per_slot() == 1
    assert allows_empty_slot_skip() is True
