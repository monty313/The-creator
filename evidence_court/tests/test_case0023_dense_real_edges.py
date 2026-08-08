"""CASE-0023 NEW tests: 15m production cadence + multi-set cont window (A13 density)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    CONT_EXTENDED_FORCE_MIN,
    PRODUCTION_SCALPING_SLOTS,
    PRODUCTION_SCALPING_SLOTS_15M,
    SCALPING_CADENCE_SLOTS,
    SCALPING_TRADES_PER_DAY_MAX,
    SCALPING_TRADES_PER_DAY_MIN,
    allows_empty_slot_skip,
    build_scalping_cadence_slots,
    continuation_session_ok,
    entry_quality_ok,
    production_symbols_per_slot,
)


def test_creator_new_production_15m_a13_capacity():
    """Creator NEW: 15m pin denser than 30m; capacity in [8,400] (CASE-0023 law pin)."""
    pin15 = PRODUCTION_SCALPING_SLOTS_15M
    lab30 = SCALPING_CADENCE_SLOTS
    assert pin15 == build_scalping_cadence_slots(interval_minutes=15)
    assert len(pin15) > len(lab30)
    assert len(pin15) >= SCALPING_TRADES_PER_DAY_MIN
    assert len(pin15) <= SCALPING_TRADES_PER_DAY_MAX
    assert pin15[0] == "07:00:00"
    # denser: 15m step present on pin; production may be denser still (CASE-0027)
    assert "07:15:00" in pin15
    assert "07:15:00" not in lab30
    assert len(PRODUCTION_SCALPING_SLOTS) >= len(pin15)


def test_mark_new_multiset_cont_opens_active_band_not_thin():
    """Mark NEW: multi-set agree + strong force opens mid-band cont; thin/late still blocked."""
    # Non-prime mid band without multi-set: blocked
    assert continuation_session_ok("11:00:00", multi_set_agree=False, force=0.5) is False
    # With multi-set + strong force: ok
    assert continuation_session_ok(
        "11:00:00", multi_set_agree=True, force=CONT_EXTENDED_FORCE_MIN
    ) is True
    # Weak force even with multi-set: blocked
    assert continuation_session_ok("11:00:00", multi_set_agree=True, force=0.20) is False
    # Late thin (19:00) blocked even with multi-set + strong force
    assert continuation_session_ok("19:00:00", multi_set_agree=True, force=0.60) is False
    # Prime always session-ok
    assert continuation_session_ok("13:00:00", multi_set_agree=False, force=0.1) is True


def test_creator_new_entry_quality_extended_cont_and_no_pad():
    """Creator counter NEW: entry_quality honors extended cont; empty-skip; 1-sym."""
    # Extended cont mid-band multi-set
    assert entry_quality_ok(
        slot="11:00:00",
        topology="continuation",
        n_fills=1,
        force=0.40,
        multi_set_agree=True,
    ) is True
    # Without multi-set still blocked at 11:00
    assert entry_quality_ok(
        slot="11:00:00",
        topology="continuation",
        n_fills=1,
        force=0.50,
        multi_set_agree=False,
    ) is False
    # Pullback any slot
    assert entry_quality_ok(
        slot="07:00:00", topology="pullback_resume", n_fills=0, force=0.15
    ) is True
    assert allows_empty_slot_skip() is True
    assert production_symbols_per_slot() == 1


def test_mark_new_lab_30m_pin_preserved():
    """Mark counter NEW: CASE-0011 30m SCALPING_CADENCE_SLOTS pin unchanged."""
    assert SCALPING_CADENCE_SLOTS == build_scalping_cadence_slots(interval_minutes=30)
    assert "07:15:00" not in SCALPING_CADENCE_SLOTS
    assert len(SCALPING_CADENCE_SLOTS) < len(PRODUCTION_SCALPING_SLOTS_15M)
    assert len(SCALPING_CADENCE_SLOTS) < len(PRODUCTION_SCALPING_SLOTS)
