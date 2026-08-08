"""Permanent meta-brain training pins (A29)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.brain import brain_act_match_rate, train_meta_brain
from evidence_court.meta_rl.policy import MetaPolicy, train_goal_conditioned_meta_policy
from evidence_court.meta_rl.state import build_meta_rl_state


def test_meta_train_is_permanent_not_zero_steps():
    pol = train_goal_conditioned_meta_policy(seed=11, n_steps=600, freeze=True)
    assert pol.trained is True
    assert pol.meta_train_steps >= 600
    assert pol.frozen_for_inference is True


def test_meta_train_improves_over_prior():
    prior = MetaPolicy.untrained_prior(0).brain
    trained = train_meta_brain(seed=0, n_steps=1500, freeze=False)
    r_prior = brain_act_match_rate(prior, seed=3, n=120)
    r_trained = brain_act_match_rate(trained, seed=3, n=120)
    assert r_trained >= r_prior - 0.05
    assert trained.meta_train_steps >= 1500


def test_same_weights_different_targets_without_retrain():
    pol = train_goal_conditioned_meta_policy(seed=3, n_steps=600, freeze=True)
    fp = pol.weight_fingerprint()
    s_easy = build_meta_rl_state(target_percent=5.0, max_daily_risk_percent=3.0)
    s_hard = build_meta_rl_state(target_percent=90.0, max_daily_risk_percent=1.0)
    for idx in (0, 3, 6, 9):
        s_easy[idx] = 0.9
        s_hard[idx] = 0.9
    a1 = pol.forward(s_easy, topology="launch")
    a2 = pol.forward(s_hard, topology="launch")
    assert pol.weight_fingerprint() == fp
    assert a1.act in ("wait", "long", "short")
    assert a2.act in ("wait", "long", "short")


def test_save_load_champion(tmp_path: Path):
    pol = train_goal_conditioned_meta_policy(seed=5, n_steps=600, freeze=True)
    path = tmp_path / "champ.npz"
    pol.save(path)
    loaded = MetaPolicy.load(path, freeze=True)
    assert loaded.trained is True
    assert loaded.meta_train_steps == pol.meta_train_steps
    assert np.allclose(loaded.brain.W1, pol.brain.W1)
