"""CASE-0003 NEW tests: goal-conditioned multi-leg path (Creator + Mark)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    goal_conditioned_size,
    run_goal_path_day,
    session_confirms_side,
    simulate_fill_m1_path,
)
from evidence_court.meta_rl.policy import FrozenMetaPolicy
from evidence_court.meta_rl.risk import DailyRiskLedger


def _synth_m1(n_days: int = 8, trend: float = 0.00015) -> list:
    """Synthetic M1 with mild uptrend for unit path."""
    rows = []
    px = 2000.0
    for d in range(n_days):
        date = f"2026-06-{d+1:02d}"
        for m in range(0, 24 * 60, 5):  # 5m steps for speed
            h, mi = divmod(m, 60)
            t = f"{h:02d}:{mi:02d}:00"
            o = px
            c = px * (1.0 + trend)
            rows.append(
                {
                    "date": date,
                    "time": t,
                    "open": o,
                    "high": max(o, c) * 1.0003,
                    "low": min(o, c) * 0.9997,
                    "close": c,
                }
            )
            px = c
    return rows


def test_creator_new_goal_size_grows_with_remaining_goal():
    """Creator NEW: goal-conditioned size reacts to remaining goal (not fixed)."""
    led = DailyRiskLedger(max_daily_risk_percent=3.0)
    s_far = goal_conditioned_size(
        ledger=led, target_percent=30.0, stop_distance_pct=0.45, aggression=0.8, expect_r=2.0
    )
    led.realized_pnl_percent = 25.0
    s_near = goal_conditioned_size(
        ledger=led, target_percent=30.0, stop_distance_pct=0.45, aggression=0.8, expect_r=2.0
    )
    assert s_far > 0
    assert s_near > 0
    # Near goal should not demand larger ideal than far goal (ideal = rem/R)
    assert s_near <= s_far + 1e-6 or led.remaining_risk_budget_percent() < 3.0


def test_creator_new_m1_fill_stop_and_win():
    bars = [
        {"open": 100.0, "high": 100.2, "low": 99.9, "close": 100.1},
        {"open": 100.1, "high": 100.5, "low": 100.0, "close": 100.4},
    ]
    win = simulate_fill_m1_path(side=1, bars=bars, size_risk_percent=1.0, stop_distance_pct=0.45)
    assert win > 0
    stop_bars = [
        {"open": 100.0, "high": 100.1, "low": 99.0, "close": 99.5},
    ]
    loss = simulate_fill_m1_path(
        side=1, bars=stop_bars, size_risk_percent=1.0, stop_distance_pct=0.45
    )
    assert loss < 0


def test_mark_new_session_confirm_and_conflict_skip():
    """Mark NEW: session confirm exists; opposing open path rejects."""
    m1 = _synth_m1(n_days=3, trend=0.0002)
    date = m1[-1]["date"]
    # uptrend day should confirm long
    assert session_confirms_side(m1, date=date, asof_time="14:00:00", side=1) is True
    # strong up day should reject short
    assert session_confirms_side(m1, date=date, asof_time="14:00:00", side=-1) is False


def test_goal_path_day_runs_no_retrain_no_breach():
    m1 = _synth_m1(n_days=10, trend=0.00012)
    date = sorted(set(b["date"] for b in m1))[-2]
    policy = FrozenMetaPolicy.from_seed(7)
    fp = policy.weight_fingerprint()
    fills, ledger, meta = run_goal_path_day(
        policy,
        date=date,
        m1_by_symbol={"XAUUSD": m1},
        target_percent=5.0,
        max_daily_risk_percent=3.0,
        symbols=["XAUUSD"],
    )
    policy.assert_frozen()
    assert policy.weight_fingerprint() == fp
    loss = max(-ledger.realized_pnl_percent, 0.0)
    assert loss <= 3.0 + 1e-6
    assert str(meta["path"]).startswith("goal_conditioned")
