"""L2L-P10 residual: density process + promote_decision pins."""
from __future__ import annotations

import numpy as np

from evidence_court.meta_rl.brain import MetaBrain
from evidence_court.meta_rl.l2l_process import (
    process_target_from_senses,
    sample_l2l_process_episode,
    train_l2l_process_curriculum,
)
from evidence_court.meta_rl.senses import MarketSenseInput, probe_all_senses
from evidence_court.meta_rl.train_l2l_p10_residual import promote_decision


def test_density_mode_raises_fire_frac_vs_balanced():
    """Density residual curriculum must teach more fire process than wait flood."""
    b1 = MetaBrain.create(seed=5)
    out_bal = train_l2l_process_curriculum(
        b1, steps=80, seed=5, holdout_frac=0.2, density_mode=False
    )
    b2 = MetaBrain.create(seed=5)
    out_den = train_l2l_process_curriculum(
        b2, steps=80, seed=5, holdout_frac=0.2, density_mode=True
    )
    assert out_den["fire_frac"] >= out_bal["fire_frac"] - 0.05
    assert out_den["fire_frac"] >= 0.25  # not pure wait


def test_density_mode_soft_wait_reward_lower():
    """Wait process_reward is scaled down under density_mode."""
    inp = MarketSenseInput(
        htf_force=[0.0] * 8,
        ltf_velocity=[0.0] * 4,
        inertia=[0.0] * 4,
        inertia_baseline=[0.0] * 4,
        velocity_baseline=[0.0] * 4,
        regime="chop",
        set_conflict=True,
        target_percent=15.0,
        max_daily_risk_percent=2.0,
    )
    rep = probe_all_senses(inp)
    pt0 = process_target_from_senses(rep, density_mode=False)
    pt1 = process_target_from_senses(rep, density_mode=True)
    assert pt0.teacher_act == "wait"
    assert pt1.teacher_act == "wait"
    assert pt1.process_reward <= pt0.process_reward + 1e-9


def test_density_sample_episode_shapes():
    st, pt, rep = sample_l2l_process_episode(
        np.random.default_rng(2), scenario="launch_fire", density_mode=True
    )
    assert st.shape[0] == 176
    assert pt.teacher_act in ("wait", "long", "short")
    assert rep is not None


def test_promote_decision_rejects_washout():
    residual = {
        "a13_frac": 0.13,
        "hits": 1,
        "hit_rate": 0.033,
        "n_zero": 22,
        "breach_count": 0,
        "weights_frozen": True,
        "both_pb_and_cont": True,
    }
    champ = {
        "a13_frac": 0.60,
        "hits": 3,
        "hit_rate": 0.10,
        "n_zero": 8,
        "breach_count": 0,
    }
    dec = promote_decision(residual, champ)
    assert dec["promote"] is False
    assert "reject" in dec["reason"]


def test_promote_decision_accepts_beat():
    residual = {
        "a13_frac": 0.70,
        "hits": 4,
        "hit_rate": 0.13,
        "n_zero": 5,
        "breach_count": 0,
        "weights_frozen": True,
        "both_pb_and_cont": True,
    }
    champ = {
        "a13_frac": 0.60,
        "hits": 3,
        "hit_rate": 0.10,
        "n_zero": 8,
        "breach_count": 0,
    }
    dec = promote_decision(residual, champ)
    assert dec["promote"] is True


def test_load_wait_still_wait_without_density_override():
    """Fail-mode pin: load without launch remains wait in default mode."""
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
    pt = process_target_from_senses(probe_all_senses(inp), density_mode=False)
    assert pt.teacher_act == "wait"
