"""CASE-0029 NEW tests: production 5m decision clock under A26 cont hold."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    CONT_EXTENDED_FORCE_MIN,
    CONT_HOLD_MIN_MINUTES,
    PRODUCTION_CADENCE_INTERVAL_MIN,
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


def test_creator_new_production_5m_a13_capacity():
    """Creator NEW: production 5m denser than 10m pin; capacity in [8,400]."""
    prod = PRODUCTION_SCALPING_SLOTS
    pin10 = PRODUCTION_SCALPING_SLOTS_10M
    assert PRODUCTION_CADENCE_INTERVAL_MIN == 5
    assert prod == build_scalping_cadence_slots(interval_minutes=5)
    assert len(prod) > len(pin10)
    assert len(prod) >= SCALPING_TRADES_PER_DAY_MIN
    assert len(prod) <= SCALPING_TRADES_PER_DAY_MAX
    assert prod[0] == "07:00:00"
    assert "07:05:00" in prod
    assert "07:05:00" not in pin10
    assert "07:10:00" in pin10


def test_mark_new_10m_15m_30m_pins_and_a26_hold():
    """Mark NEW: A25 10m + A22 15m + 0011 30m pins; A26 hold constant."""
    assert PRODUCTION_SCALPING_SLOTS_10M == build_scalping_cadence_slots(
        interval_minutes=10
    )
    assert PRODUCTION_SCALPING_SLOTS_15M == build_scalping_cadence_slots(
        interval_minutes=15
    )
    assert SCALPING_CADENCE_SLOTS == build_scalping_cadence_slots(interval_minutes=30)
    assert CONT_HOLD_MIN_MINUTES == 30
    assert len(SCALPING_CADENCE_SLOTS) < len(PRODUCTION_SCALPING_SLOTS_15M)
    assert len(PRODUCTION_SCALPING_SLOTS_15M) < len(PRODUCTION_SCALPING_SLOTS_10M)
    assert len(PRODUCTION_SCALPING_SLOTS_10M) < len(PRODUCTION_SCALPING_SLOTS)


def test_creator_new_5m_still_gated_1sym_no_pad():
    """Creator counter NEW: cont gates + empty skip + 1-sym on 5m path."""
    assert continuation_session_ok("11:00:00", multi_set_agree=False, force=0.5) is False
    assert continuation_session_ok(
        "11:00:00", multi_set_agree=True, force=CONT_EXTENDED_FORCE_MIN
    ) is True
    assert entry_quality_ok(
        slot="07:00:00", topology="pullback_resume", n_fills=0, force=0.15
    ) is True
    assert allows_empty_slot_skip() is True
    assert production_symbols_per_slot() == 1


def test_mark_new_cont_hold_30m_on_5m_grid():
    """Mark counter NEW: A26 cont min 30m on 5m production grid; pb EOD."""
    slots = PRODUCTION_SCALPING_SLOTS
    assert "07:05:00" in slots
    assert fill_hold_end_time("continuation", "07:00:00", slots) == "07:30:00"
    assert fill_hold_end_time("continuation", "13:00:00", slots) == "13:30:00"
    assert fill_hold_end_time("pullback_resume", "07:00:00", slots) == "23:59:59"
