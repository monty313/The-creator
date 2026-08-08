"""CASE-0013 NEW tests: micro-risk residual legs (A10)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    residual_size_scale,
    symbols_per_slot_for_leg,
)


def test_creator_new_residual_size_scale():
    """Creator NEW: first fill full scale; after anchor (≥1 fill) → micro scale."""
    assert residual_size_scale(n_fills_so_far=0) == 1.0
    # default anchor_fills=1: after first fill, residual micro
    assert residual_size_scale(n_fills_so_far=1) == 0.25
    assert residual_size_scale(n_fills_so_far=5) == 0.25


def test_mark_new_residual_multi_symbol_when_micro():
    """Mark NEW: multi-symbol only in residual phase (after anchor)."""
    assert symbols_per_slot_for_leg(0) == 1
    assert symbols_per_slot_for_leg(1) == 3
    assert symbols_per_slot_for_leg(10) == 3


def test_creator_new_micro_scale_strictly_below_one():
    """Creator counter NEW: residual scale is strictly in (0, 1)."""
    s = residual_size_scale(n_fills_so_far=3)
    assert 0.0 < s < 1.0


def test_mark_new_anchor_one_symbol_full_scale():
    """Mark counter NEW: anchor phase (0 fills yet) is 1-symbol and scale 1.0."""
    assert residual_size_scale(n_fills_so_far=0) == 1.0
    assert symbols_per_slot_for_leg(0) == 1
