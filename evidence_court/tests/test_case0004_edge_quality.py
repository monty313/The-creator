"""CASE-0004 NEW tests: completed HTF force + multi-day momentum + goal lock."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.edge import (
    _htf_completed_only,
    multi_day_momentum,
    scan_all_sets,
    build_tf_cache,
)
from evidence_court.meta_rl.goal_path import simulate_fill_m1_path


def test_creator_new_htf_excludes_same_day_when_asof_time():
    """Creator NEW: HTF confirmation must not use incomplete same-day bars."""
    bars = [
        {"date": "2026-01-01", "time": "00:00:00", "open": 1, "high": 2, "low": 0.5, "close": 1.5},
        {"date": "2026-01-02", "time": "00:00:00", "open": 1.5, "high": 2, "low": 1, "close": 1.8},
        {"date": "2026-01-03", "time": "10:00:00", "open": 1.8, "high": 2.2, "low": 1.7, "close": 2.0},
    ]
    closed = _htf_completed_only(
        bars, asof_date="2026-01-03", asof_time="12:00:00", tf="1d"
    )
    assert all(b["date"] < "2026-01-03" for b in closed)
    assert len(closed) == 2


def test_mark_new_multi_day_momentum_signed():
    """Mark NEW: multi-day completed closes produce signed tide."""
    daily = []
    px = 100.0
    for i, ret in enumerate([0.01, 0.01, 0.01, -0.02]):
        o = px
        c = px * (1 + ret)
        daily.append(
            {
                "date": f"2026-02-{i+1:02d}",
                "time": "00:00:00",
                "open": o,
                "high": max(o, c),
                "low": min(o, c),
                "close": c,
            }
        )
        px = c
    mom = multi_day_momentum(daily, asof_date="2026-02-05", n=3)
    # last 3 closed days before 02-05 include up/up/down — mixed or slight bias
    assert isinstance(mom, float)
    # strong 3-up series
    daily2 = []
    px = 100.0
    for i in range(5):
        o, c = px, px * 1.01
        daily2.append(
            {
                "date": f"2026-03-{i+1:02d}",
                "time": "00:00:00",
                "open": o,
                "high": c,
                "low": o,
                "close": c,
            }
        )
        px = c
    mom_up = multi_day_momentum(daily2, asof_date="2026-03-06", n=3)
    assert mom_up > 0


def test_creator_new_goal_lock_exits_at_remaining_target():
    """Creator NEW (counter): path exits when floating PnL reaches goal lock."""
    # strong up path: 1% move with 0.45 stop ≈ 2.2R
    bars = [
        {"open": 100.0, "high": 100.3, "low": 99.95, "close": 100.2},
        {"open": 100.2, "high": 101.0, "low": 100.1, "close": 100.9},
    ]
    pnl = simulate_fill_m1_path(
        side=1,
        bars=bars,
        size_risk_percent=2.5,
        stop_distance_pct=0.45,
        friction_pct=0.04,
        goal_lock_pnl_percent=5.0,
    )
    assert abs(pnl - 5.0) < 1e-6


def test_mark_new_goal_lock_respects_stop_before_lock():
    """Mark NEW (counter): stop hits before goal-lock → loss, not phantom hit."""
    bars = [
        {"open": 100.0, "high": 100.1, "low": 99.0, "close": 99.5},  # stop ~0.45% → ~99.55
    ]
    pnl = simulate_fill_m1_path(
        side=1,
        bars=bars,
        size_risk_percent=2.0,
        stop_distance_pct=0.45,
        friction_pct=0.04,
        goal_lock_pnl_percent=5.0,
    )
    assert pnl < 0
    assert pnl <= -2.0 + 1e-6  # full risk loss (+ friction more negative)
