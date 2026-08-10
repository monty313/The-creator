"""L2L Proposals 2–10 unit pins (process curriculum + freeze + dual helpers)."""
from __future__ import annotations

import numpy as np

from evidence_court.meta_rl.brain import MetaBrain
from evidence_court.meta_rl.l2l_process import (
    process_target_from_senses,
    sample_l2l_process_episode,
    train_l2l_process_curriculum,
)
from evidence_court.meta_rl.policy import MetaPolicy
from evidence_court.meta_rl.senses import MarketSenseInput, probe_all_senses
from evidence_court.meta_rl.state import META_RL_DIM, extract_sense_pack


def test_p2_p3_load_wait_not_fire():
    """P2/P3: load building → process wait (not fire)."""
    inp = MarketSenseInput(
        htf_force=[0.8, 0.7, 0.75, 0.7, 0.6, 0.65, 0.5, 0.55],
        ltf_velocity=[-0.5, -0.4, -0.45, -0.3],
        inertia=[0.7, 0.65, 0.6, 0.55],
        inertia_baseline=[0.4] * 4,
        velocity_baseline=[0.1] * 4,
        full_body_outside_rails=True,
        ltf_inside_tight=True,
        efficiency=0.6,
        regime="bull",
        g_fixed=True,
        composition_has_force=True,
        composition_has_velocity=True,
        cross_family_agree=True,
        target_percent=15.0,
        max_daily_risk_percent=2.0,
    )
    pt = process_target_from_senses(probe_all_senses(inp))
    assert pt.teacher_act == "wait"
    assert "P3_feel_load" in pt.proposal_tags or "feel_load" in pt.reason


def test_p2_p4_launch_fire_process():
    """P2/P4: launch + allow_fire → process fire with force side."""
    inp = MarketSenseInput(
        htf_force=[0.8] * 8,
        ltf_velocity=[0.55] * 4,
        inertia=[0.7] * 4,
        inertia_baseline=[0.35] * 4,
        velocity_baseline=[0.2] * 4,
        efficiency=0.75,
        regime="bull",
        g_fixed=True,
        composition_has_force=True,
        composition_has_velocity=True,
        cross_family_agree=True,
        target_percent=15.0,
        max_daily_risk_percent=2.0,
        progress_to_target=0.2,
        realized_risk_percent=0.1,
    )
    pt = process_target_from_senses(probe_all_senses(inp))
    assert pt.teacher_act in ("long", "short", "wait")
    # should not be collapse
    assert "collapse" not in pt.reason


def test_p5_conflict_wait():
    st, pt, rep = sample_l2l_process_episode(
        np.random.default_rng(0), scenario="conflict_wait"
    )
    assert st.shape == (META_RL_DIM,)
    assert float(np.max(np.abs(extract_sense_pack(st)))) >= 0.0
    assert pt.teacher_act == "wait"


def test_p6_p7_curriculum_trains_and_p8_freezes():
    brain = MetaBrain.create(seed=3)
    before = brain.meta_train_steps
    out = train_l2l_process_curriculum(brain, steps=40, seed=3, holdout_frac=0.25)
    assert out["train_steps"] >= 1
    assert out["holdout_steps"] >= 1
    assert brain.meta_train_steps > before
    pol = MetaPolicy(brain=brain, trained=True)
    pol.freeze_for_inference()
    pol.assert_frozen()
    # P8: meta_update forbidden
    st, pt, _ = sample_l2l_process_episode(np.random.default_rng(1))
    try:
        pol.brain.meta_update(st, teacher_act=pt.teacher_act)
        raised = False
    except RuntimeError as e:
        raised = "NO_RETRAIN" in str(e) or "forbidden" in str(e).lower()
    assert raised


def test_p8_fingerprint_stable_across_target_risk_context():
    brain = MetaBrain.create(seed=9)
    train_l2l_process_curriculum(brain, steps=30, seed=9, holdout_frac=0.2)
    pol = MetaPolicy(brain=brain, trained=True)
    pol.freeze_for_inference()
    fp0 = pol.weight_fingerprint()
    for t, r in ((5.0, 1.0), (50.0, 2.0), (90.0, 3.0)):
        st, _, _ = sample_l2l_process_episode(
            np.random.default_rng(9), target=t, risk=r
        )
        pol.forward(st)
        assert pol.weight_fingerprint() == fp0
