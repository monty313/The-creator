"""CASE-0030 NEW tests: dual-symbol only on multi-set agree (A13 density, anti thrash)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import production_symbols_per_slot


def test_creator_new_dual_on_agree_long_short():
    """Creator NEW: multi-set agree → 2 symbols capacity."""
    assert production_symbols_per_slot(multi_set_consensus="agree_long") == 2
    assert production_symbols_per_slot(multi_set_consensus="agree_short") == 2


def test_mark_new_one_sym_when_incomplete_chop_conflict():
    """Mark NEW: weak eyes stay 1-sym (no thrash dual)."""
    assert production_symbols_per_slot(multi_set_consensus="incomplete") == 1
    assert production_symbols_per_slot(multi_set_consensus="chop") == 1
    assert production_symbols_per_slot(multi_set_consensus="conflict") == 1


def test_creator_new_dual_can_be_disabled():
    """Creator counter NEW: dual_on_agree=False restores A21 always-1."""
    assert (
        production_symbols_per_slot(
            multi_set_consensus="agree_long", dual_on_agree=False
        )
        == 1
    )


def test_mark_new_default_still_one_without_agree():
    """Mark counter NEW: default incomplete → 1 (production safe default)."""
    assert production_symbols_per_slot() == 1
