"""CASE-0006 NEW tests: R-capture BE trail + pullback 1R clear sizing (A10)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    clear_expect_r,
    goal_path_size_for_clear,
    simulate_fill_m1_path,
)
from evidence_court.meta_rl.risk import DailyRiskLedger


def _bars_up_then_crash(*, peak_pct: float, entry: float = 100.0) -> list:
    """First bar open=entry; second bar high reaches peak; then reverse below entry to stop zone."""
    peak = entry * (1.0 + peak_pct / 100.0)
    crash_low = entry * 0.99  # well below entry
    return [
        {"open": entry, "high": entry, "low": entry, "close": entry, "date": "2026-01-02", "time": "10:00:00"},
        {
            "open": entry,
            "high": peak,
            "low": entry * 0.999,
            "close": entry * 1.001,
            "date": "2026-01-02",
            "time": "10:01:00",
        },
        {
            "open": entry * 1.001,
            "high": entry * 1.001,
            "low": crash_low,
            "close": crash_low,
            "date": "2026-01-02",
            "time": "10:02:00",
        },
    ]


def test_creator_new_be_trail_after_1p5r_saves_reversal():
    """Creator NEW: peak ≥1.5R then reverse → trail ~0, no-trail full −size."""
    stop_pct = 0.45
    # 1.5R = 1.5 * 0.45 = 0.675% move
    peak_1p6r = 1.6 * stop_pct  # 0.72%
    bars = _bars_up_then_crash(peak_pct=peak_1p6r)
    size = 1.0
    fr = 0.04
    no_trail = simulate_fill_m1_path(
        side=1,
        bars=bars,
        size_risk_percent=size,
        stop_distance_pct=stop_pct,
        friction_pct=fr,
        trail=False,
    )
    with_trail = simulate_fill_m1_path(
        side=1,
        bars=bars,
        size_risk_percent=size,
        stop_distance_pct=stop_pct,
        friction_pct=fr,
        trail=True,
        be_arm_r=1.5,
    )
    # No trail: reverse hits hard stop → −size − friction
    assert no_trail <= -size + 1e-9
    # Trail armed at 1.5R: BE exit near 0 (allow small friction loss only)
    assert with_trail > -0.25
    assert with_trail > no_trail + 0.5


def test_mark_new_pullback_expect_r_one_sizes_for_1r_clear():
    """Mark NEW: pullback_resume expect_r=1.0 → larger size than continuation for same goal."""
    assert clear_expect_r("pullback_resume", target_percent=10.0) == 1.0
    assert clear_expect_r("pullback_resume", target_percent=50.0) == 1.0
    assert clear_expect_r("continuation", target_percent=10.0) == 1.35
    assert clear_expect_r("continuation", target_percent=50.0) == 1.9

    led = DailyRiskLedger(max_daily_risk_percent=3.0, equity=100_000.0)
    # Low target so envelope does not fully bind both the same way
    pb = goal_path_size_for_clear(
        ledger=led,
        target_percent=2.0,
        topology="pullback_resume",
        wounded=False,
    )
    ct = goal_path_size_for_clear(
        ledger=led,
        target_percent=2.0,
        topology="continuation",
        wounded=False,
    )
    assert pb > 0 and ct > 0
    assert pb > ct  # pullback 1.0R more aggressive than cont 1.35R
    # 1R clear: size ≈ rem_goal when envelope allows
    rem_goal = 2.0
    expected = min(rem_goal / 1.0, led.remaining_risk_budget_percent() * 0.95, 3.0 * 0.80)
    assert abs(pb - expected) < 0.15


def test_creator_new_be_not_armed_at_1r_only():
    """Creator counter NEW: peak only +1.0R then reverse → still full stop (not premature BE)."""
    stop_pct = 0.45
    peak_1r = 1.0 * stop_pct  # 0.45%
    bars = _bars_up_then_crash(peak_pct=peak_1r)
    size = 1.0
    fr = 0.04
    pnl = simulate_fill_m1_path(
        side=1,
        bars=bars,
        size_risk_percent=size,
        stop_distance_pct=stop_pct,
        friction_pct=fr,
        trail=True,
        be_arm_r=1.5,
    )
    assert pnl <= -size + 1e-9


def test_mark_new_pullback_size_respects_risk_envelope():
    """Mark counter NEW: high rem_goal vs tiny risk → size capped by envelope."""
    led = DailyRiskLedger(max_daily_risk_percent=2.0, equity=100_000.0)
    size = goal_path_size_for_clear(
        ledger=led,
        target_percent=50.0,
        topology="pullback_resume",
        wounded=False,
    )
    rem = led.remaining_risk_budget_percent()
    assert size <= rem * 0.95 + 1e-9
    assert size <= 2.0 * 0.95 + 1e-9
    assert size > 0.0
