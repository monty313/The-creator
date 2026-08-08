"""Gating tests: trained brain; no inference retrain when target/risk changes."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_risk import (
    IDX_RISK_NORM,
    IDX_TARGET_NORM,
    encode_goal_risk_context,
)
from evidence_court.meta_rl.policy import MetaPolicy, train_goal_conditioned_meta_policy
from evidence_court.meta_rl.state import (
    META_RL_DIM,
    build_meta_rl_state,
    extract_goal_risk_context,
)


def test_context_channels_reflect_supplied_pairs():
    s1 = build_meta_rl_state(target_percent=10.0, max_daily_risk_percent=1.0)
    s2 = build_meta_rl_state(target_percent=80.0, max_daily_risk_percent=3.0)
    assert s1.shape == (META_RL_DIM,)
    c1 = extract_goal_risk_context(s1)
    c2 = extract_goal_risk_context(s2)
    assert c1[IDX_TARGET_NORM] < c2[IDX_TARGET_NORM]
    assert c1[IDX_RISK_NORM] < c2[IDX_RISK_NORM]


def test_legacy_self_state_saturates_but_context_does_not():
    s_low = build_meta_rl_state(target_percent=5.0, max_daily_risk_percent=2.0)
    s_high = build_meta_rl_state(target_percent=90.0, max_daily_risk_percent=2.0)
    assert float(s_low[158]) == pytest.approx(1.0)
    assert float(s_high[158]) == pytest.approx(1.0)
    assert extract_goal_risk_context(s_high)[IDX_TARGET_NORM] > extract_goal_risk_context(s_low)[
        IDX_TARGET_NORM
    ]


def test_trained_policy_no_retrain_between_pairs():
    policy = train_goal_conditioned_meta_policy(seed=7, n_steps=800, freeze=True)
    assert policy.trained is True
    assert policy.meta_train_steps >= 800
    fp0 = policy.weight_fingerprint()
    assert policy.inference_updates == 0

    for t, r in [(5.0, 1.0), (45.0, 2.0), (90.0, 3.0)]:
        st = build_meta_rl_state(target_percent=t, max_daily_risk_percent=r)
        policy.forward(st)
        policy.assert_frozen()

    assert policy.weight_fingerprint() == fp0
    with pytest.raises(RuntimeError, match="NO_RETRAIN"):
        policy.train_step(None)


def test_untrained_cannot_freeze_or_forward():
    prior = MetaPolicy.untrained_prior(1)
    assert prior.trained is False
    with pytest.raises(RuntimeError):
        prior.freeze_for_inference()
    with pytest.raises(RuntimeError):
        prior.forward(build_meta_rl_state(target_percent=10.0, max_daily_risk_percent=2.0))


def test_encode_rejects_out_of_band():
    with pytest.raises(ValueError):
        encode_goal_risk_context(4.0, 2.0)
    with pytest.raises(ValueError):
        encode_goal_risk_context(50.0, 0.5)
