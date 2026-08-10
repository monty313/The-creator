"""CASE-0027 NEW tests: production 10m decision clock (A13 structural density)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    CONT_EXTENDED_FORCE_MIN,
    PRODUCTION_SCALPING_SLOTS,
    PRODUCTION_SCALPING_SLOTS_10M,
    PRODUCTION_SCALPING_SLOTS_15M,
    SCALPING_CADENCE_SLOTS,
    SCALPING_TRADES_PER_DAY_MAX,
    SCALPING_TRADES_PER_DAY_MIN,
    allows_empty_slot_skip,
    build_scalping_cadence_slots,
    continuation_session_ok,
    entry_quality_ok,
    fill_hold_end_time,
    production_symbols_per_slot,
)


def test_creator_new_production_10m_a13_capacity():
    """Creator NEW: A25 10m pin denser than 15m; capacity in [8,400] (CASE-0027 law pin)."""
    pin10 = PRODUCTION_SCALPING_SLOTS_10M
    pin15 = PRODUCTION_SCALPING_SLOTS_15M
    assert pin10 == build_scalping_cadence_slots(interval_minutes=10)
    assert len(pin10) > len(pin15)
    assert len(pin10) >= SCALPING_TRADES_PER_DAY_MIN
    assert len(pin10) <= SCALPING_TRADES_PER_DAY_MAX
    assert pin10[0] == "07:00:00"
    assert "07:10:00" in pin10
    assert "07:10:00" not in pin15
    assert "07:15:00" in pin15
    # Production may be denser still (CASE-0029 5m)
    assert len(PRODUCTION_SCALPING_SLOTS) >= len(pin10)


def test_mark_new_15m_and_30m_pins_preserved():
    """Mark NEW: CASE-0023 15m pin + CASE-0011 30m lab preserved."""
    assert PRODUCTION_SCALPING_SLOTS_15M == build_scalping_cadence_slots(
        interval_minutes=15
    )
    assert SCALPING_CADENCE_SLOTS == build_scalping_cadence_slots(interval_minutes=30)
    assert "07:15:00" in PRODUCTION_SCALPING_SLOTS_15M
    assert "07:15:00" not in SCALPING_CADENCE_SLOTS
    assert len(SCALPING_CADENCE_SLOTS) < len(PRODUCTION_SCALPING_SLOTS_15M)
    assert len(PRODUCTION_SCALPING_SLOTS_15M) < len(PRODUCTION_SCALPING_SLOTS_10M)
    assert len(PRODUCTION_SCALPING_SLOTS_10M) <= len(PRODUCTION_SCALPING_SLOTS)


def test_creator_new_10m_still_gated_no_pad_1sym():
    """Creator counter NEW: cont gates + empty skip + 1-sym on 10m path."""
    assert continuation_session_ok("11:00:00", multi_set_agree=False, force=0.5) is False
    assert continuation_session_ok(
        "11:00:00", multi_set_agree=True, force=CONT_EXTENDED_FORCE_MIN
    ) is True
    assert entry_quality_ok(
        slot="07:00:00", topology="pullback_resume", n_fills=0, force=0.15
    ) is True
    assert allows_empty_slot_skip() is True
    assert production_symbols_per_slot() == 1


def test_mark_new_hold_on_10m_grid_scalp():
    """Monty scalp: cont 10m / pb 15m on A25 10m pin grid (not 30m / EOD)."""
    slots = PRODUCTION_SCALPING_SLOTS_10M
    assert "07:00:00" in slots and "07:10:00" in slots
    assert fill_hold_end_time("continuation", "07:00:00", slots) == "07:10:00"
    assert fill_hold_end_time("pullback_resume", "07:00:00", slots) == "07:20:00"
    assert fill_hold_end_time("continuation", "13:00:00", slots) == "13:10:00"
