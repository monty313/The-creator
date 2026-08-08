"""CASE-0028 NEW tests: continuation min hold-R (30m path) on A25 10m grid."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    CONT_HOLD_MIN_MINUTES,
    PRODUCTION_SCALPING_SLOTS,
    PRODUCTION_SCALPING_SLOTS_10M,
    SCALPING_CADENCE_SLOTS,
    allows_empty_slot_skip,
    fill_hold_end_time,
    next_slot_end_after_minutes,
    production_symbols_per_slot,
)


def test_creator_new_cont_min_hold_30m_on_10m_grid():
    """Creator NEW: cont holds ≥30m path on dense grids (not bare next tick)."""
    assert CONT_HOLD_MIN_MINUTES == 30
    # A25 10m pin
    slots10 = PRODUCTION_SCALPING_SLOTS_10M
    assert fill_hold_end_time("continuation", "07:00:00", slots10) == "07:30:00"
    assert next_slot_end_after_minutes("07:00:00", slots10, 30) == "07:30:00"
    assert fill_hold_end_time("continuation", "13:00:00", slots10) == "13:30:00"
    assert fill_hold_end_time("continuation", "07:00:00", slots10) != "07:10:00"
    # Production default (may be 5m CASE-0029) still ≥30m cont
    slots = PRODUCTION_SCALPING_SLOTS
    assert fill_hold_end_time("continuation", "07:00:00", slots) == "07:30:00"


def test_mark_new_pullback_eod_last_slot_eod_preserved():
    """Mark NEW: pullback still EOD; last slot EOD for both topologies."""
    slots = PRODUCTION_SCALPING_SLOTS
    assert fill_hold_end_time("pullback_resume", "07:00:00", slots) == "23:59:59"
    assert fill_hold_end_time("pullback_resume", "13:00:00", slots) == "23:59:59"
    last = slots[-1]
    assert fill_hold_end_time("continuation", last, slots) == "23:59:59"
    assert fill_hold_end_time("pullback_resume", last, slots) == "23:59:59"


def test_creator_new_30m_lab_cont_still_next_slot():
    """Creator counter NEW: on 30m lab grid, +30m equals next slot (0012 class)."""
    slots = SCALPING_CADENCE_SLOTS
    assert slots[0] == "07:00:00"
    assert slots[1] == "07:30:00"
    assert fill_hold_end_time("continuation", "07:00:00", slots) == "07:30:00"
    # mid
    mid = "13:00:00"
    assert mid in slots
    assert fill_hold_end_time("continuation", mid, slots) == "13:30:00"


def test_mark_new_a25_geometry_preserved():
    """Mark counter NEW: A25 10m pin + 1-sym + empty skip preserved."""
    assert "07:10:00" in PRODUCTION_SCALPING_SLOTS_10M
    assert production_symbols_per_slot() == 1
    assert allows_empty_slot_skip() is True
    assert len(PRODUCTION_SCALPING_SLOTS) >= len(PRODUCTION_SCALPING_SLOTS_10M)
