"""Risk envelope: sizing path never exceeds declared max daily risk."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.policy import FrozenMetaPolicy
from evidence_court.meta_rl.risk import (
    DailyRiskLedger,
    FrictionAssumptions,
    OpenPosition,
    risk_report,
    size_position_risk_percent,
)
from evidence_court.meta_rl.state import build_meta_rl_state


def test_size_never_exceeds_remaining_budget():
    for target in (5.0, 30.0, 90.0):
        for risk in (1.0, 2.0, 3.0):
            sz = size_position_risk_percent(
                max_daily_risk_percent=risk,
                remaining_budget_percent=risk,
                stop_distance_pct=0.2,
                target_percent=target,
                aggression=1.0,
            )
            assert sz <= risk + 1e-9
            assert sz >= 0.0


def test_ledger_breach_detection_and_safe_open():
    ledger = DailyRiskLedger(max_daily_risk_percent=2.0, friction=FrictionAssumptions())
    assert ledger.can_open(0.5)
    ledger.positions.append(OpenPosition("XAU", 1, risk_percent=1.5, notional_pct=10.0))
    # remaining may be tight after friction
    report = risk_report(ledger)
    assert report["worst_case_daily_loss_percent"] <= 2.0 + ledger.friction.total_pct
    # cannot open another full 2%
    assert ledger.would_breach(2.0) is True


def test_policy_respects_envelope_on_fire():
    policy = FrozenMetaPolicy.from_seed(3)
    for t, r in ((10.0, 1.0), (80.0, 3.0)):
        st = build_meta_rl_state(target_percent=t, max_daily_risk_percent=r)
        ledger = DailyRiskLedger(max_daily_risk_percent=r)
        # Direction only via Channel1 set slots in state (no force_side oracle)
        st = st.copy()
        st[0] = st[3] = st[6] = st[9] = 1.0
        act = policy.forward(st, ledger=ledger, topology="launch")
        if act.act != "wait":
            assert act.size_risk_percent <= r + 1e-9
            assert not ledger.would_breach(act.size_risk_percent)
