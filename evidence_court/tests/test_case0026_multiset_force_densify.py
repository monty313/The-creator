"""CASE-0026 NEW tests: multi-set force densification (real confluence floors)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    CONT_EXTENDED_FORCE_MIN,
    MULTI_SET_CONT_ENTRY_FORCE_MIN,
    PRODUCTION_SCALPING_SLOTS,
    allows_empty_slot_skip,
    continuation_session_ok,
    entry_quality_ok,
    first_entry_cont_force_min,
    production_symbols_per_slot,
    real_edge_force_min,
)


def test_creator_new_multiset_force_floors_denser_than_a21():
    """Creator NEW: multi-set floors denser than CASE-0021 defaults; still positive."""
    pb_a = real_edge_force_min(topology="pullback_resume", multi_set_agree=True)
    ct_a = real_edge_force_min(topology="continuation", multi_set_agree=True)
    fe_a = first_entry_cont_force_min(multi_set_agree=True)
    # denser than A21 multi-set (0.12 / 0.18 / 0.28)
    assert pb_a < 0.12
    assert ct_a < 0.18
    assert fe_a < 0.28
    assert CONT_EXTENDED_FORCE_MIN < 0.35
    assert MULTI_SET_CONT_ENTRY_FORCE_MIN < 0.32
    # still real (no pad)
    assert pb_a > 0.05
    assert ct_a > 0.05
    assert fe_a > 0.05
    assert CONT_EXTENDED_FORCE_MIN > 0.05
    assert MULTI_SET_CONT_ENTRY_FORCE_MIN > 0.05


def test_mark_new_non_multiset_floors_unchanged_chop_blocked():
    """Mark NEW: non-multi floors stay A21; multi still easier; chop never fires."""
    pb_no = real_edge_force_min(topology="pullback_resume", multi_set_agree=False)
    ct_no = real_edge_force_min(topology="continuation", multi_set_agree=False)
    fe_no = first_entry_cont_force_min(multi_set_agree=False)
    assert pb_no == 0.15
    assert ct_no == 0.22
    assert fe_no == 0.35
    assert real_edge_force_min(topology="pullback_resume", multi_set_agree=True) < pb_no
    assert real_edge_force_min(topology="continuation", multi_set_agree=True) < ct_no
    assert first_entry_cont_force_min(multi_set_agree=True) < fe_no
    assert real_edge_force_min(topology="chop", multi_set_agree=True) >= 1.0


def test_creator_new_floors_never_pad_extended_still_gated():
    """Creator counter NEW: extended cont multi-set-only; empty skip; 1-sym; no pad."""
    # Shoulder without multi-set still blocked
    assert continuation_session_ok("09:00:00", multi_set_agree=False, force=0.9) is False
    # Multi-set + denser extended force opens shoulder
    assert continuation_session_ok(
        "09:00:00", multi_set_agree=True, force=CONT_EXTENDED_FORCE_MIN
    ) is True
    assert continuation_session_ok(
        "09:00:00", multi_set_agree=True, force=CONT_EXTENDED_FORCE_MIN - 0.05
    ) is False
    # entry_quality multi-set cont uses denser multi entry floor on prime
    assert entry_quality_ok(
        slot="13:00:00",
        topology="continuation",
        n_fills=1,
        force=MULTI_SET_CONT_ENTRY_FORCE_MIN,
        multi_set_agree=True,
    ) is True
    assert entry_quality_ok(
        slot="13:00:00",
        topology="continuation",
        n_fills=1,
        force=MULTI_SET_CONT_ENTRY_FORCE_MIN - 0.03,
        multi_set_agree=True,
    ) is False
    assert allows_empty_slot_skip() is True
    assert production_symbols_per_slot() == 1


def test_mark_new_a22_a21_geometry_preserved():
    """Mark counter NEW: 15m production grid + 1-sym geometry preserved."""
    # Production default denser than 15m pin (CASE-0027 may be 10m)
    assert len(PRODUCTION_SCALPING_SLOTS) >= 40
    assert production_symbols_per_slot() == 1
    # Thin late cont still blocked
    assert continuation_session_ok("19:00:00", multi_set_agree=True, force=0.9) is False
