"""CASE-0012 NEW tests: conversion under dense path (A10)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    SCALPING_CADENCE_SLOTS,
    fill_hold_end_time,
    n_symbols_per_slot,
)


def test_creator_new_pullback_scalp_not_eod():
    """Monty scalp: pullback short runner; cont short hold (30m lab → next slot)."""
    slots = SCALPING_CADENCE_SLOTS
    mid = slots[len(slots) // 2]
    nxt = slots[slots.index(mid) + 1]
    # On 30m lab grid, +10m cont and +15m pb both land on next 30m slot
    assert fill_hold_end_time("pullback_resume", mid, slots) == nxt
    assert fill_hold_end_time("continuation", mid, slots) == nxt
    assert fill_hold_end_time("pullback_resume", mid, slots) != "23:59:59"


def test_mark_new_one_symbol_per_slot():
    """Mark NEW: production takes one best symbol per decision slot (anti thrash)."""
    assert n_symbols_per_slot() == 1


def test_creator_new_last_slot_eod_both_topologies():
    """Creator counter NEW: last slot → EOD for pullback and continuation."""
    last = SCALPING_CADENCE_SLOTS[-1]
    assert fill_hold_end_time("pullback_resume", last, SCALPING_CADENCE_SLOTS) == "23:59:59"
    assert fill_hold_end_time("continuation", last, SCALPING_CADENCE_SLOTS) == "23:59:59"


def test_mark_new_later_slots_allow_other_symbols():
    """Mark counter NEW: per-slot cap is 1; not a same-symbol lock for the day."""
    # Pure design pin: function only constrains concurrent take count
    assert n_symbols_per_slot() == 1
    assert n_symbols_per_slot() < 3  # not multi-symbol concurrent
