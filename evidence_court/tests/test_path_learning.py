"""PATH LEARNING unit pins — drive shipped helpers (not reimplemented fakes)."""
from __future__ import annotations

import numpy as np

from evidence_court.meta_rl.brain import MetaBrain
from evidence_court.meta_rl.path_learning import (
    apply_outcome_shaped_update,
    compose_method_goal_reward,
    conversion_teacher_from_context,
    outcome_scale,
    outcome_score_from_fields,
    path_learning_promote_guard,
    sample_conversion_episode,
    train_path_learning_curriculum,
)
from evidence_court.meta_rl.policy import MetaPolicy


def test_step1_outcome_scale_clear_beats_breach():
    good = outcome_score_from_fields(hit_target=True, progress_to_target=0.8, r_capture=0.5)
    bad = outcome_score_from_fields(breach=True)
    dead = outcome_score_from_fields(dead_fire=True)
    assert good > dead > bad
    assert outcome_scale(good) > outcome_scale(bad)
    assert outcome_scale(bad) >= 0.3  # still trains lightly


def test_method_first_goal_second_blocks_candy_on_broken_method():
    """Broken method: huge positive outcome must not raise total above method base."""
    method = 1.40  # thrash/dip-chase WAIT teacher strength
    broken_clear = compose_method_goal_reward(
        method, outcome_score=1.0, method_ok=False
    )
    broken_flat = compose_method_goal_reward(
        method, outcome_score=0.0, method_ok=False
    )
    ok_clear = compose_method_goal_reward(method, outcome_score=1.0, method_ok=True)
    ok_flat = compose_method_goal_reward(method, outcome_score=0.0, method_ok=True)

    assert broken_clear["method_first"] is True
    assert broken_clear["goal_reward"] <= 0.0 + 1e-12
    # no goal candy when method broken
    assert broken_clear["total"] <= broken_flat["total"] + 1e-9
    # method ok: clear outcome nudges above flat
    assert ok_clear["total"] > ok_flat["total"]
    # goal second: |goal| < |method|
    assert abs(ok_clear["goal_reward"]) < abs(ok_clear["method_reward"])
    # method term is what dominates the total
    assert abs(ok_clear["method_reward"]) > abs(ok_clear["goal_reward"]) * 2


def test_method_first_risk_penalty_always_applies():
    clean = compose_method_goal_reward(1.55, outcome_score=0.5, method_ok=True)
    blown = compose_method_goal_reward(
        1.55, outcome_score=0.5, method_ok=True, risk_blown=True
    )
    assert blown["total"] < clean["total"]
    assert blown["risk_penalty"] < 0


def test_apply_outcome_shaped_update_method_broken_no_goal_candy():
    brain = MetaBrain.create(seed=3)
    st = np.zeros(176, dtype=np.float64)
    st[0] = 0.15
    # method broken + perfect outcome still trains (does not explode / NaN)
    loss = apply_outcome_shaped_update(
        brain,
        st,
        teacher_act="wait",
        outcome_score=1.0,
        base_reward=1.4,
        method_ok=False,
        lr=0.02,
    )
    assert np.isfinite(loss)
    assert brain.meta_train_steps >= 1


def test_step1_outcome_shaped_update_runs_on_brain():
    brain = MetaBrain.create(seed=1)
    st = np.zeros(176, dtype=np.float64)
    st[0] = 0.2
    before = brain.meta_train_steps
    loss = apply_outcome_shaped_update(
        brain, st, teacher_act="long", outcome_score=0.6, lr=0.02
    )
    assert brain.meta_train_steps > before
    assert np.isfinite(loss)


def test_step4_conversion_load_wait_and_hold_fire():
    w = conversion_teacher_from_context(
        progress_to_target=0.1,
        risk_remaining_frac=0.8,
        topology="slingshot_load",
        force_side=1,
        load_building=True,
    )
    assert w.teacher_act == "wait"
    assert w.class_name == "wait_pullback"

    h = conversion_teacher_from_context(
        progress_to_target=0.5,
        risk_remaining_frac=0.55,
        topology="continuation",
        force_side=-1,
        outcome_score=0.4,
    )
    assert h.teacher_act == "short"
    assert h.class_name == "hold_convert"

    r = conversion_teacher_from_context(
        progress_to_target=0.2,
        risk_remaining_frac=0.1,
        topology="pullback_resume",
        force_side=1,
    )
    assert r.teacher_act == "wait"
    assert r.class_name == "wait_risk"


def test_step4_sample_conversion_episode_shapes():
    st, ct, oc = sample_conversion_episode(np.random.default_rng(0))
    assert st.shape[0] == 176
    assert ct.teacher_act in ("wait", "long", "short")
    assert -1.0 <= oc <= 1.0


def test_steps_2_3_curriculum_mix_not_path_only_clone():
    brain = MetaBrain.create(seed=4)
    # synthetic path-like examples (fire only) — still must mix conversion
    fake_path = [
        {
            "state": [0.01 * (i % 7) for i in range(176)],
            "teacher_act": "long",
            "topology": "pullback_resume",
            "source": "path_state_htf_active",
            "n_htf_active": 2,
            "teacher_size_frac": 0.6,
        }
        for _ in range(20)
    ]
    out = train_path_learning_curriculum(
        brain,
        steps=60,
        seed=4,
        path_examples=fake_path,
        path_anchor_frac=0.2,
        holdout_frac=0.2,
        process_frac=0.1,
    )
    assert out["has_conversion"] is True
    assert out["has_outcome_shaping"] is True
    assert out["has_holdout"] is True
    assert out["path_only_clone"] is False
    assert out["counts"]["conversion"] >= 1


def test_step6_promote_guard_rejects_washout_and_clone():
    lab_wash = {
        "a13_frac": 0.12,
        "hits": 1,
        "n_zero": 20,
        "breach_count": 0,
        "weights_frozen": True,
    }
    champ = {"a13_frac": 0.4, "hits": 3, "n_zero": 10, "breach_count": 0}
    g = path_learning_promote_guard(
        lab_wash,
        champ,
        path_only_clone=False,
        has_outcome_conversion_mix=True,
        court_promote=False,
    )
    assert g["promote_lab"] is False
    assert g["production_replace"] is False
    assert g["process_washout"] is True

    g2 = path_learning_promote_guard(
        {
            "a13_frac": 0.5,
            "hits": 4,
            "n_zero": 8,
            "breach_count": 0,
            "weights_frozen": True,
        },
        champ,
        path_only_clone=True,
        has_outcome_conversion_mix=False,
        court_promote=True,
    )
    assert g2["production_replace"] is False
    assert g2["promote_lab"] is False


def test_step6_promote_guard_blocks_production_without_floor():
    lab = {
        "a13_frac": 0.45,
        "hits": 7,
        "n_zero": 12,
        "breach_count": 0,
        "weights_frozen": True,
    }
    champ = {"a13_frac": 0.40, "hits": 6, "n_zero": 14, "breach_count": 0}
    g = path_learning_promote_guard(
        lab,
        champ,
        path_only_clone=False,
        has_outcome_conversion_mix=True,
        court_promote=True,  # even with court flag, floor not held
    )
    assert g["floor_hold"] is False
    assert g["production_replace"] is False


def test_step3_freeze_fingerprint_stable_across_target_risk():
    brain = MetaBrain.create(seed=8)
    train_path_learning_curriculum(brain, steps=40, seed=8, path_examples=None)
    pol = MetaPolicy(brain=brain, trained=True)
    pol.freeze_for_inference()
    fp0 = pol.weight_fingerprint()
    st, _, _ = sample_conversion_episode(np.random.default_rng(1), holdout_mode=True)
    pol.forward(st)
    assert pol.weight_fingerprint() == fp0
