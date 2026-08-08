"""CASE-0009 NEW tests: slot/entry R quality (A10 openings + counters)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    entry_quality_ok,
    is_prime_session_slot,
    session_confirms_side,
)


def test_creator_new_prime_session_slot_set():
    """Creator NEW: London–NY active slots prime; late/early thin not prime."""
    assert is_prime_session_slot("10:00:00") is True
    assert is_prime_session_slot("13:00:00") is True
    assert is_prime_session_slot("16:00:00") is True
    assert is_prime_session_slot("07:00:00") is False
    assert is_prime_session_slot("19:00:00") is False


def test_mark_new_entry_quality_pullback_first():
    """Mark NEW: first fill pullback always OK; weak continuation non-prime blocked."""
    assert entry_quality_ok(
        slot="07:00:00", topology="pullback_resume", n_fills=0, force=0.20
    )
    assert not entry_quality_ok(
        slot="07:00:00", topology="continuation", n_fills=0, force=0.30
    )
    assert entry_quality_ok(
        slot="13:00:00", topology="continuation", n_fills=0, force=0.45
    )
    assert not entry_quality_ok(
        slot="13:00:00", topology="continuation", n_fills=0, force=0.25
    )


def test_creator_new_later_pullback_any_slot_ok():
    """Creator counter NEW: after first fill, pullback OK on non-prime (residual leg)."""
    assert entry_quality_ok(
        slot="19:00:00", topology="pullback_resume", n_fills=1, force=0.20
    )
    # continuation still prime-gated later
    assert not entry_quality_ok(
        slot="19:00:00", topology="continuation", n_fills=1, force=0.50
    )
    assert entry_quality_ok(
        slot="16:00:00", topology="continuation", n_fills=1, force=0.50
    )


def test_mark_new_session_confirm_min_align():
    """Mark counter NEW: mild min_align passes lean path; fails counter path."""
    entry = 100.0
    # 30 bars lean long +0.0003
    lean = []
    for i in range(30):
        px = entry * (1.0 + 0.0003 * (i / 29.0))
        lean.append(
            {
                "date": "2026-01-02",
                "time": f"09:{i:02d}:00" if i < 60 else "09:59:00",
                "open": entry if i == 0 else lean[-1]["close"],
                "high": px,
                "low": px * 0.9999,
                "close": px,
            }
        )
    # Fix times to be monotonic HH:MM
    lean = []
    for i in range(30):
        t = f"{9 + i // 60:02d}:{i % 60:02d}:00"
        px = entry * (1.0 + 0.0003 * (i / 29.0))
        lean.append(
            {
                "date": "2026-01-02",
                "time": t,
                "open": entry if i == 0 else entry * (1.0 + 0.0003 * ((i - 1) / 29.0)),
                "high": px * 1.0001,
                "low": px * 0.9999,
                "close": px,
            }
        )
    assert session_confirms_side(
        lean, date="2026-01-02", asof_time="10:00:00", side=1, min_align=1.5e-4
    )
    assert not session_confirms_side(
        lean, date="2026-01-02", asof_time="10:00:00", side=-1, min_align=1.5e-4
    )
    # Counter path: down day
    down = []
    for i in range(30):
        t = f"{9 + i // 60:02d}:{i % 60:02d}:00"
        px = entry * (1.0 - 0.0004 * (i / 29.0))
        down.append(
            {
                "date": "2026-01-02",
                "time": t,
                "open": entry if i == 0 else entry * (1.0 - 0.0004 * ((i - 1) / 29.0)),
                "high": px * 1.0001,
                "low": px * 0.9999,
                "close": px,
            }
        )
    assert not session_confirms_side(
        down, date="2026-01-02", asof_time="10:00:00", side=1, min_align=1.5e-4
    )
