"""CASE-0011 NEW tests: dense scalping cadence toward A13 (A10)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    DEFAULT_SLOTS,
    SCALPING_CADENCE_SLOTS,
    SCALPING_TRADES_PER_DAY_MAX,
    SCALPING_TRADES_PER_DAY_MIN,
    a13_trade_count_ok,
    build_scalping_cadence_slots,
    max_fills_for_a13,
    allows_empty_slot_skip,
)


def test_creator_new_scalping_slots_a13_capacity():
    """Creator NEW: 30m grid has capacity in [8, 400]; legacy 5-slot does not."""
    slots = build_scalping_cadence_slots(interval_minutes=30)
    assert len(slots) >= SCALPING_TRADES_PER_DAY_MIN
    assert len(slots) <= SCALPING_TRADES_PER_DAY_MAX
    assert slots[0] == "07:00:00"
    assert slots == SCALPING_CADENCE_SLOTS
    # Structural: 5-slot grid cannot be A13-compliant production path
    assert len(DEFAULT_SLOTS) < SCALPING_TRADES_PER_DAY_MIN
    assert not a13_trade_count_ok(len(DEFAULT_SLOTS))


def test_mark_new_max_fills_a13_band():
    """Mark NEW: max fills allows A13 min and hard-caps at 400."""
    assert max_fills_for_a13(target_percent=5.0) >= SCALPING_TRADES_PER_DAY_MIN
    assert max_fills_for_a13(target_percent=90.0) >= SCALPING_TRADES_PER_DAY_MIN
    assert max_fills_for_a13(target_percent=30.0) == SCALPING_TRADES_PER_DAY_MAX


def test_creator_new_max_fills_hard_cap_400():
    """Creator counter NEW: never above 400 even if denser clock requested."""
    dense = build_scalping_cadence_slots(interval_minutes=5)
    # 5m grid may exceed 400 decision points — fill cap still 400
    assert max_fills_for_a13(target_percent=50.0) == 400
    assert max_fills_for_a13(target_percent=50.0) <= SCALPING_TRADES_PER_DAY_MAX
    if len(dense) > 400:
        assert max_fills_for_a13(target_percent=50.0) < len(dense)


def test_mark_new_no_pad_trades_without_edge():
    """Mark counter NEW: empty-slot skip is required (no synthetic pad fills)."""
    assert allows_empty_slot_skip() is True
