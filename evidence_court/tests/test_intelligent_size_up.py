"""Monty EO: progressive size-up toward clear + size-down near breach."""
from __future__ import annotations

from evidence_court.meta_rl.goal_path import (
    goal_path_size_for_clear,
    intelligent_size_toward_clear,
)
from evidence_court.meta_rl.risk import DailyRiskLedger


def test_intelligent_size_within_envelope_when_far():
    led = DailyRiskLedger(max_daily_risk_percent=3.0)
    intel = intelligent_size_toward_clear(
        ledger=led,
        target_percent=15.0,
        topology="pullback_resume",
        brain_size=0.25,
        edge_quality=0.9,
        conf=0.75,
    )
    assert intel > 0.05
    assert intel <= led.remaining_risk_budget_percent() + 1e-9
    assert not led.would_breach(intel)


def test_intelligent_size_respects_exhausted_budget():
    led = DailyRiskLedger(max_daily_risk_percent=2.0)
    led.realized_pnl_percent = -1.8
    led.closed_losses_percent = 1.8
    sz = intelligent_size_toward_clear(
        ledger=led,
        target_percent=15.0,
        topology="continuation",
        brain_size=1.0,
        edge_quality=1.0,
        conf=0.9,
    )
    rem = led.remaining_risk_budget_percent()
    if rem <= 0.05:
        assert sz == 0.0
    else:
        assert sz <= rem + 1e-9


def test_progressive_size_up_far_from_target_beats_tiny_brain():
    """Far from target + clean edge → progressive size-up (not stuck on tiny brain)."""
    led = DailyRiskLedger(max_daily_risk_percent=3.0)
    tiny = 0.15
    intel = intelligent_size_toward_clear(
        ledger=led,
        target_percent=15.0,
        topology="pullback_resume",
        brain_size=tiny,
        edge_quality=1.0,
        conf=0.8,
    )
    assert intel > tiny


def test_size_down_near_breach():
    """Near risk floor → hard size-down (Monty)."""
    led = DailyRiskLedger(max_daily_risk_percent=3.0)
    # Spend most of risk skin via closed losses
    led.closed_losses_percent = 2.4  # rem_risk ~0.6 on 3% day
    far = intelligent_size_toward_clear(
        ledger=DailyRiskLedger(max_daily_risk_percent=3.0),
        target_percent=15.0,
        topology="continuation",
        brain_size=1.5,
        edge_quality=1.0,
        conf=0.85,
    )
    near = intelligent_size_toward_clear(
        ledger=led,
        target_percent=15.0,
        topology="continuation",
        brain_size=1.5,
        edge_quality=1.0,
        conf=0.85,
    )
    rem = led.remaining_risk_budget_percent()
    assert near <= rem + 1e-9
    assert near < far
    assert near <= rem * 0.35 + 1e-6  # hard size-down band


def test_progressive_up_when_far_uses_meaningful_budget():
    led = DailyRiskLedger(max_daily_risk_percent=3.0)
    sz = intelligent_size_toward_clear(
        ledger=led,
        target_percent=15.0,
        topology="continuation",
        brain_size=0.4,
        edge_quality=0.95,
        conf=0.8,
    )
    # Should open progressive throttle (not micro)
    assert sz >= 0.5
