"""CASE-0025 NEW tests: dense NYLON prime band for continuation session-ok."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    CONT_EXTENDED_FORCE_MIN,
    PRIME_BAND_HOUR_END,
    PRIME_BAND_HOUR_START,
    PRIME_SESSION_SLOTS,
    PRODUCTION_SCALPING_SLOTS,
    continuation_session_ok,
    entry_quality_ok,
    is_prime_session_slot,
    production_symbols_per_slot,
    real_edge_force_min,
    allows_empty_slot_skip,
)


def test_creator_new_dense_nylon_prime_band_hours():
    """Creator NEW: hours [12,16] are prime; classic named primes stay; thin open/late not."""
    assert PRIME_BAND_HOUR_START == 12
    assert PRIME_BAND_HOUR_END == 16
    # Classic named primes
    for s in PRIME_SESSION_SLOTS:
        assert is_prime_session_slot(s) is True
    # Dense mid-overlap on 15m grid
    assert is_prime_session_slot("12:00:00") is True
    assert is_prime_session_slot("12:15:00") is True
    assert is_prime_session_slot("14:30:00") is True
    assert is_prime_session_slot("15:45:00") is True
    assert is_prime_session_slot("16:00:00") is True
    # Thin open / late fade not prime
    assert is_prime_session_slot("07:00:00") is False
    assert is_prime_session_slot("19:00:00") is False
    # Pre-band London morning not free-prime (shoulder → multi-set path)
    assert is_prime_session_slot("11:00:00") is False
    assert is_prime_session_slot("11:45:00") is False


def test_mark_new_shoulder_still_multiset_thin_blocked():
    """Mark NEW: 11:00 needs multi-set+force; dense prime free of multi-set; thin blocked."""
    # Shoulder 11:00 — A22 extended, not free prime
    assert continuation_session_ok("11:00:00", multi_set_agree=False, force=0.50) is False
    assert continuation_session_ok(
        "11:00:00", multi_set_agree=True, force=CONT_EXTENDED_FORCE_MIN
    ) is True
    # Dense NYLON hour — session-ok without multi-set (force floor separate)
    assert continuation_session_ok("14:00:00", multi_set_agree=False, force=0.10) is True
    assert continuation_session_ok("12:15:00", multi_set_agree=False, force=0.10) is True
    # Late thin still blocked even with multi-set + strong force
    assert continuation_session_ok("19:00:00", multi_set_agree=True, force=0.60) is False
    # Early open cont blocked without multi-set
    assert continuation_session_ok("07:00:00", multi_set_agree=False, force=0.50) is False


def test_creator_new_dense_prime_still_force_floors_no_pad():
    """Creator counter NEW: dense prime does not pad — force floors + empty skip + 1-sym."""
    # Weak cont force still fails entry_quality even on dense prime
    assert entry_quality_ok(
        slot="14:00:00",
        topology="continuation",
        n_fills=1,
        force=0.20,
        multi_set_agree=False,
    ) is False
    # Strong enough cont on dense prime
    assert entry_quality_ok(
        slot="14:00:00",
        topology="continuation",
        n_fills=1,
        force=0.45,
        multi_set_agree=False,
    ) is True
    # Multi-set eases prime cont floor (A21) still works inside band
    assert entry_quality_ok(
        slot="14:15:00",
        topology="continuation",
        n_fills=1,
        force=0.33,
        multi_set_agree=True,
    ) is True
    assert allows_empty_slot_skip() is True
    assert production_symbols_per_slot() == 1
    assert real_edge_force_min(topology="continuation", multi_set_agree=True) > 0.05


def test_mark_new_a22_production_grid_and_extended_pin():
    """Mark counter NEW: A22 15m production grid + extended force pin preserved."""
    # Production capacity legal (CASE-0027 may densify beyond 15m)
    assert len(PRODUCTION_SCALPING_SLOTS) >= 40
    # CASE-0026 densified CONT_EXTENDED; pin is constant-gated multi-set path, not 0.35 forever
    assert CONT_EXTENDED_FORCE_MIN > 0.05
    assert CONT_EXTENDED_FORCE_MIN < 0.40
    # Extended shoulder still needs multi-set + min force
    assert continuation_session_ok("09:00:00", multi_set_agree=True, force=0.10) is False
    assert continuation_session_ok(
        "09:00:00", multi_set_agree=True, force=CONT_EXTENDED_FORCE_MIN
    ) is True
