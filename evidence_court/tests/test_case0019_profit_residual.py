"""CASE-0019 NEW tests: profit-gated + continuation-only residual (anti F-019)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    residual_leg_allowed,
    residual_size_scale,
    symbols_per_slot_for_leg,
)


def test_creator_new_profit_gate_blocks_residual_on_loss():
    """Creator NEW: residual micro blocked when realized_pnl <= 0 (after anchor)."""
    assert residual_leg_allowed(
        1, realized_pnl_percent=-0.5, topology="continuation", require_profit=True
    ) is False
    assert residual_leg_allowed(
        1, realized_pnl_percent=0.0, topology="continuation", require_profit=True
    ) is False
    assert residual_leg_allowed(
        1, realized_pnl_percent=0.2, topology="continuation", require_profit=True
    ) is True
    # Gated scale API
    assert (
        residual_size_scale(
            1,
            realized_pnl_percent=-0.1,
            topology="continuation",
            profit_gate=True,
            continuation_only=True,
        )
        == 0.0
    )
    assert (
        residual_size_scale(
            1,
            realized_pnl_percent=0.3,
            topology="continuation",
            profit_gate=True,
            continuation_only=True,
        )
        == 0.25
    )


def test_mark_new_continuation_only_residual_protects_pullback_eod():
    """Mark NEW: residual multi/micro not on pullback_resume (protect EOD conversion path)."""
    assert residual_leg_allowed(
        1,
        realized_pnl_percent=1.0,
        topology="pullback_resume",
        require_profit=True,
        continuation_only=True,
    ) is False
    assert residual_leg_allowed(
        1,
        realized_pnl_percent=1.0,
        topology="continuation",
        require_profit=True,
        continuation_only=True,
    ) is True
    assert (
        residual_size_scale(
            1,
            realized_pnl_percent=1.0,
            topology="pullback_resume",
            profit_gate=True,
            continuation_only=True,
        )
        == 0.0
    )
    assert (
        residual_size_scale(
            1,
            realized_pnl_percent=1.0,
            topology="continuation",
            profit_gate=True,
            continuation_only=True,
        )
        == 0.25
    )


def test_creator_new_multi_symbol_only_when_profit_after_anchor():
    """Creator counter NEW: multi-symbol residual only when profit after anchor."""
    assert symbols_per_slot_for_leg(0, profit_gate=True, realized_pnl_percent=0.0) == 1
    assert symbols_per_slot_for_leg(1, profit_gate=True, realized_pnl_percent=-0.2) == 1
    assert symbols_per_slot_for_leg(1, profit_gate=True, realized_pnl_percent=0.0) == 1
    assert symbols_per_slot_for_leg(1, profit_gate=True, realized_pnl_percent=0.5) == 3
    # Anchor still full scale
    assert residual_size_scale(0, profit_gate=True, continuation_only=True) == 1.0


def test_mark_new_ungated_defaults_preserve_case0013_pins():
    """Mark counter NEW: default (ungated) residual API still matches CASE-0013 pins."""
    assert residual_size_scale(n_fills_so_far=0) == 1.0
    assert residual_size_scale(n_fills_so_far=1) == 0.25
    assert residual_size_scale(n_fills_so_far=5) == 0.25
    assert symbols_per_slot_for_leg(0) == 1
    assert symbols_per_slot_for_leg(1) == 3
    s = residual_size_scale(n_fills_so_far=3)
    assert 0.0 < s < 1.0
