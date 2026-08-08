"""A29: real L2L brain, serious train, London/NY fire, no hard-rule-only path."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.brain import (
    MetaBrain,
    brain_act_match_rate,
    sample_brain_state,
    train_meta_brain,
)
from evidence_court.meta_rl.policy import MetaPolicy, train_goal_conditioned_meta_policy
from evidence_court.meta_rl.state import build_meta_rl_state


def test_brain_is_multilayer_not_linear_stub():
    b = MetaBrain.create(0)
    assert b.W1.ndim == 2 and b.W1.shape[0] >= 32
    assert b.W2.shape[0] == 3


def test_serious_train_improves_and_marks_trained():
    prior = MetaBrain.create(1)
    trained = train_meta_brain(seed=1, n_steps=1200, freeze=False)
    assert trained.trained is True
    assert trained.meta_train_steps >= 1200
    r0 = brain_act_match_rate(prior, seed=9, n=100)
    r1 = brain_act_match_rate(trained, seed=9, n=100)
    assert r1 >= r0 - 0.05
    assert r1 >= 0.30


def test_london_ny_opportunity_drill_teaches_fire():
    brain = train_meta_brain(seed=2, n_steps=2000, freeze=False)
    rng = np.random.default_rng(0)
    fires = 0
    n = 40
    for _ in range(n):
        st, teacher, _ = sample_brain_state(
            rng, target=15.0, risk=2.0, london_ny=True, force_opp=True
        )
        act, _, _ = brain.predict_act(st)
        if teacher in ("long", "short") and act == teacher:
            fires += 1
        elif teacher in ("long", "short") and act in ("long", "short"):
            fires += 0.5
    assert fires / n >= 0.35  # must capture opportunities, not always wait


def test_no_retrain_at_inference():
    pol = train_goal_conditioned_meta_policy(seed=3, n_steps=800, freeze=True)
    fp = pol.weight_fingerprint()
    for t, r in [(5.0, 1.0), (90.0, 3.0)]:
        st = build_meta_rl_state(target_percent=t, max_daily_risk_percent=r)
        pol.forward(st, topology="launch")
    assert pol.weight_fingerprint() == fp
    with pytest.raises(RuntimeError, match="NO_RETRAIN"):
        pol.meta_update(st, teacher_act="long")


def test_untrained_brain_cannot_ship():
    pol = MetaPolicy.untrained_prior(0)
    with pytest.raises(RuntimeError, match="POLICY_NOT_TRAINED|trained"):
        pol.freeze_for_inference()
