"""CASE-0021 NEW tests: 1-sym full-scale path + multi-set real edge floors."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    entry_quality_ok,
    first_entry_cont_force_min,
    n_symbols_per_slot,
    production_leg_size_scale,
    production_symbols_per_slot,
    real_edge_force_min,
    residual_size_scale,
)


def test_creator_new_production_one_sym_full_scale_anti_starve():
    """Creator NEW: production path always 1-sym and scale 1.0 (anti F-020 starve)."""
    assert production_symbols_per_slot() == 1
    assert production_symbols_per_slot() == n_symbols_per_slot()
    for n in (0, 1, 5, 20):
        assert production_leg_size_scale(n) == 1.0
    # Must not zero-scale after anchor (F-020 class)
    assert production_leg_size_scale(1) > 0.0


def test_mark_new_multiset_agree_lowers_real_force_floors():
    """Mark NEW: multi-set agree densifies real edge floors; still positive."""
    pb_agree = real_edge_force_min(topology="pullback_resume", multi_set_agree=True)
    pb_no = real_edge_force_min(topology="pullback_resume", multi_set_agree=False)
    ct_agree = real_edge_force_min(topology="continuation", multi_set_agree=True)
    ct_no = real_edge_force_min(topology="continuation", multi_set_agree=False)
    assert 0.0 < pb_agree < pb_no
    assert 0.0 < ct_agree < ct_no
    assert first_entry_cont_force_min(multi_set_agree=True) < first_entry_cont_force_min(
        multi_set_agree=False
    )
    # Mark: chop topology not a fire edge
    assert real_edge_force_min(topology="chop", multi_set_agree=True) >= 1.0


def test_creator_new_floors_never_pad_zero():
    """Creator counter NEW: force floors never zero/negative (no pad-to-fire)."""
    for agree in (True, False):
        for topo in ("pullback_resume", "continuation"):
            m = real_edge_force_min(topology=topo, multi_set_agree=agree)
            assert m > 0.05
    # entry_quality still requires prime for continuation
    assert entry_quality_ok(
        slot="07:00:00",
        topology="continuation",
        n_fills=0,
        force=0.9,
        multi_set_agree=True,
    ) is False  # not prime
    assert entry_quality_ok(
        slot="10:00:00",
        topology="continuation",
        n_fills=1,
        force=0.33,
        multi_set_agree=True,
    ) is True  # prime + multi-set eased floor 0.32


def test_mark_new_a20_helpers_remain_but_production_not_multi():
    """Mark counter NEW: A20 residual API still exists; production is not multi residual."""
    # Ungated residual API still micro after anchor (lab helper)
    assert residual_size_scale(1) == 0.25
    # Production never opens multi residual door
    assert production_symbols_per_slot() < 3
    assert production_leg_size_scale(10) == 1.0
