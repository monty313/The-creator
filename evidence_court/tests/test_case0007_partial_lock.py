"""CASE-0007 NEW tests: partial progressive goal lock (A10 openings + counters)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    progressive_partial_floor,
    simulate_fill_m1_path,
)


def _bars_peak_then_stop(*, peak_pct: float, entry: float = 100.0, stop_pct: float = 0.45) -> list:
    """Peak favorable move then crash through hard stop below entry."""
    peak = entry * (1.0 + peak_pct / 100.0)
    crash_low = entry * (1.0 - stop_pct / 100.0 * 1.5)  # through stop
    return [
        {"open": entry, "high": entry, "low": entry, "close": entry},
        {"open": entry, "high": peak, "low": entry * 0.999, "close": entry * 1.001},
        {"open": entry * 1.001, "high": entry * 1.001, "low": crash_low, "close": crash_low},
    ]


def test_creator_new_partial_floor_saves_after_half_goal():
    """Creator NEW: path reaches ≥50% of goal_lock then stops → PnL = floor, not −size."""
    stop_pct = 0.45
    size = 2.0
    lock = 4.0  # half lock = 2.0 equity-%
    # Need floating >= 2.0: floating ≈ size * (peak_pct/stop_pct) - fr
    # 2.0 ≈ 2.0 * r - 0.0004 → r ≈ 1.0 → peak_pct ≈ 0.45
    # Use r=1.2 → peak_pct = 1.2 * 0.45 = 0.54
    peak_pct = 1.2 * stop_pct
    bars = _bars_peak_then_stop(peak_pct=peak_pct, stop_pct=stop_pct)
    fr = 0.04
    no_partial = simulate_fill_m1_path(
        side=1,
        bars=bars,
        size_risk_percent=size,
        stop_distance_pct=stop_pct,
        friction_pct=fr,
        trail=False,
        goal_lock_pnl_percent=lock,
        partial_lock_frac=None,
    )
    with_partial = simulate_fill_m1_path(
        side=1,
        bars=bars,
        size_risk_percent=size,
        stop_distance_pct=stop_pct,
        friction_pct=fr,
        trail=False,
        goal_lock_pnl_percent=lock,
        partial_lock_frac=0.5,
    )
    assert no_partial <= -size + 1e-9
    # floating at peak: size * 1.2 - fr*0.01 ≈ 2.4 > 2.0 half-lock → floor=2.0
    assert with_partial >= 2.0 - 1e-6
    assert with_partial > no_partial + 1.0


def test_mark_new_progressive_partial_floor_pure():
    """Mark NEW: pure helper arms only when floating ≥ frac×lock; returns that floor."""
    assert progressive_partial_floor(1.0, goal_lock=10.0, partial_frac=0.5) is None
    assert progressive_partial_floor(5.0, goal_lock=10.0, partial_frac=0.5) == 5.0
    assert progressive_partial_floor(9.0, goal_lock=10.0, partial_frac=0.5) == 5.0
    assert progressive_partial_floor(5.0, goal_lock=None, partial_frac=0.5) is None


def test_creator_new_partial_frac_invalid_no_floor():
    """Creator counter NEW: frac=0 or frac>=1 never arms floor."""
    assert progressive_partial_floor(100.0, goal_lock=10.0, partial_frac=0.0) is None
    assert progressive_partial_floor(100.0, goal_lock=10.0, partial_frac=1.0) is None
    assert progressive_partial_floor(100.0, goal_lock=10.0, partial_frac=1.5) is None
    # Path with invalid frac behaves like no partial
    stop_pct = 0.45
    bars = _bars_peak_then_stop(peak_pct=2.0 * stop_pct, stop_pct=stop_pct)
    pnl = simulate_fill_m1_path(
        side=1,
        bars=bars,
        size_risk_percent=1.0,
        stop_distance_pct=stop_pct,
        friction_pct=0.04,
        trail=False,
        goal_lock_pnl_percent=4.0,
        partial_lock_frac=1.0,
    )
    assert pnl <= -1.0 + 1e-9


def test_mark_new_floor_not_above_seen_floating():
    """Mark counter NEW: floor only after floating reaches threshold; never free PnL."""
    # Below threshold
    assert progressive_partial_floor(2.5, goal_lock=10.0, partial_frac=0.5) is None
    # At threshold
    fl = progressive_partial_floor(5.0, goal_lock=10.0, partial_frac=0.5)
    assert fl == 5.0
    assert fl <= 5.0
    # Floor value is threshold, not full lock
    assert fl < 10.0
