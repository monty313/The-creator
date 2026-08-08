"""CASE-0008 NEW tests: size-R progressive floor (A10 openings + counters)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    size_r_partial_floor,
    simulate_fill_m1_path,
)


def _bars_peak_then_stop(*, peak_pct: float, entry: float = 100.0, stop_pct: float = 0.45) -> list:
    peak = entry * (1.0 + peak_pct / 100.0)
    crash_low = entry * (1.0 - stop_pct / 100.0 * 1.5)
    return [
        {"open": entry, "high": entry, "low": entry, "close": entry},
        {"open": entry, "high": peak, "low": entry * 0.999, "close": entry * 1.001},
        {"open": entry * 1.001, "high": entry * 1.001, "low": crash_low, "close": crash_low},
    ]


def test_creator_new_size_r_floor_banks_1r_on_stop():
    """Creator NEW: peak ≥1R then hard stop → bank ~1R size floor, not −size.

    Uses huge goal_lock so rem_goal half-floor cannot arm (F-012 contrast).
    """
    stop_pct = 0.45
    size = 2.0
    # 1.1R peak
    peak_pct = 1.1 * stop_pct
    bars = _bars_peak_then_stop(peak_pct=peak_pct, stop_pct=stop_pct)
    fr = 0.04
    huge_lock = 50.0  # half = 25 unreachable at 1.1R * size ≈ 2.2
    no_r = simulate_fill_m1_path(
        side=1,
        bars=bars,
        size_risk_percent=size,
        stop_distance_pct=stop_pct,
        friction_pct=fr,
        trail=False,
        goal_lock_pnl_percent=huge_lock,
        partial_lock_frac=0.5,
        size_r_arm_r=None,
    )
    with_r = simulate_fill_m1_path(
        side=1,
        bars=bars,
        size_risk_percent=size,
        stop_distance_pct=stop_pct,
        friction_pct=fr,
        trail=False,
        goal_lock_pnl_percent=huge_lock,
        partial_lock_frac=0.5,
        size_r_arm_r=1.0,
    )
    assert no_r <= -size + 1e-9
    # floating ≈ size*1.1 - fr*0.01 ≈ 2.2; floor at 1.0R ≈ size*1.0 - fr*0.01
    assert with_r >= size * 0.9
    assert with_r > no_r + 1.0


def test_mark_new_size_r_partial_floor_pure():
    """Mark NEW: pure helper arms at floating ≥ size×arm_r − fr."""
    size = 2.0
    fr = 0.0004
    assert size_r_partial_floor(1.0, size_risk_percent=size, arm_r=1.0, friction=fr) is None
    fl = size_r_partial_floor(2.0, size_risk_percent=size, arm_r=1.0, friction=fr)
    assert fl is not None
    assert abs(fl - (size * 1.0 - fr)) < 1e-9
    assert size_r_partial_floor(5.0, size_risk_percent=0.0, arm_r=1.0, friction=fr) is None


def test_creator_new_size_r_not_armed_below_1r():
    """Creator counter NEW: peak only 0.6R does not arm when arm_r=1.0."""
    stop_pct = 0.45
    size = 2.0
    peak_pct = 0.6 * stop_pct
    bars = _bars_peak_then_stop(peak_pct=peak_pct, stop_pct=stop_pct)
    pnl = simulate_fill_m1_path(
        side=1,
        bars=bars,
        size_risk_percent=size,
        stop_distance_pct=stop_pct,
        friction_pct=0.04,
        trail=False,
        goal_lock_pnl_percent=50.0,
        partial_lock_frac=None,
        size_r_arm_r=1.0,
    )
    assert pnl <= -size + 1e-9


def test_mark_new_size_r_floor_capped_by_floating():
    """Mark counter NEW: floor equals arm threshold ≤ floating; never free above floating."""
    size = 3.0
    fr = 0.01
    floating = 3.5
    fl = size_r_partial_floor(floating, size_risk_percent=size, arm_r=1.0, friction=fr)
    assert fl is not None
    assert fl <= floating + 1e-12
    assert fl == size * 1.0 - fr
    # Below arm: None
    assert size_r_partial_floor(2.0, size_risk_percent=size, arm_r=1.0, friction=fr) is None
