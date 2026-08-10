"""CASE-0028 hold windows — UPDATED Monty scalp law (2026-08-10).

Was: cont ≥30m / pullback EOD (swing-like conversion).
Now: cont **10m** / pullback **15m** — scalping meta-RL identity (A13).
Conversion = short quality legs + progressive size-up, not multi-hour holds.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    CONT_HOLD_MIN_MINUTES,
    PB_HOLD_MIN_MINUTES,
    PRODUCTION_SCALPING_SLOTS,
    PRODUCTION_SCALPING_SLOTS_10M,
    PRODUCTION_SCALPING_SLOTS_15M,
    SCALPING_CADENCE_SLOTS,
    allows_empty_slot_skip,
    fill_hold_end_time,
    next_slot_end_after_minutes,
    production_symbols_per_slot,
)


def test_creator_scalp_cont_hold_10m():
    """Monty scalp: continuation hold is 10m — not 30m."""
    assert CONT_HOLD_MIN_MINUTES == 10
    slots10 = PRODUCTION_SCALPING_SLOTS_10M
    assert fill_hold_end_time("continuation", "07:00:00", slots10) == "07:10:00"
    assert next_slot_end_after_minutes("07:00:00", slots10, 10) == "07:10:00"
    # Must NOT be 30m swing hold
    assert fill_hold_end_time("continuation", "07:00:00", slots10) != "07:30:00"
    slots15 = PRODUCTION_SCALPING_SLOTS_15M
    # 15m grid: first slot ≥ +10m is 07:15
    assert fill_hold_end_time("continuation", "07:00:00", slots15) == "07:15:00"


def _mins(t: str) -> int:
    p = str(t).split(":")
    return int(p[0]) * 60 + int(p[1])


def test_mark_scalp_pullback_not_eod():
    """Monty scalp: pullback is short runner (15m), not EOD bag-hold."""
    assert PB_HOLD_MIN_MINUTES == 15
    slots = PRODUCTION_SCALPING_SLOTS_15M
    end = fill_hold_end_time("pullback_resume", "07:00:00", slots)
    assert end != "23:59:59"
    assert _mins(end) <= _mins("07:00:00") + 20
    last = slots[-1]
    # last slot still EOD (no look-ahead past day)
    assert fill_hold_end_time("continuation", last, slots) == "23:59:59"
    assert fill_hold_end_time("pullback_resume", last, slots) == "23:59:59"


def test_creator_30m_lab_cont_next_slot_class():
    """On 30m lab grid, 10m hold still advances to next listed slot ≥ +10m."""
    slots = SCALPING_CADENCE_SLOTS
    assert slots[0] == "07:00:00"
    assert slots[1] == "07:30:00"
    # +10m from 07:00 → first slot ≥ 07:10 → 07:30 on 30m grid
    assert fill_hold_end_time("continuation", "07:00:00", slots) == "07:30:00"


def test_mark_a25_geometry_preserved():
    """1-sym + empty skip + dense clocks preserved (hold length is separate)."""
    assert "07:10:00" in PRODUCTION_SCALPING_SLOTS_10M
    assert production_symbols_per_slot() == 1
    assert allows_empty_slot_skip() is True
    assert len(PRODUCTION_SCALPING_SLOTS) >= len(PRODUCTION_SCALPING_SLOTS_10M)
