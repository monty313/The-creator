"""Aaron Force+state curriculum pins — process shapes (pullback/continuation), not copy-only."""
from __future__ import annotations

import numpy as np

from evidence_court.meta_rl.aaron_reason_curriculum import (
    aaron_force_state_from_senses,
    sample_aaron_episode,
    train_aaron_reason_curriculum,
)
from evidence_court.meta_rl.brain import MetaBrain
from evidence_court.meta_rl.senses import MarketSenseInput, probe_all_senses


def test_no_force_is_wait():
    inp = MarketSenseInput(
        htf_force=[0.2, -0.2, 0.1, -0.1, 0, 0, 0, 0],
        ltf_velocity=[0, 0, 0, 0],
        inertia=[0, 0, 0, 0],
        inertia_baseline=[0, 0, 0, 0],
        velocity_baseline=[0, 0, 0, 0],
        set_conflict=True,
        cross_family_agree=False,
        composition_has_force=False,
        target_percent=15.0,
        max_daily_risk_percent=2.0,
    )
    lab = aaron_force_state_from_senses(probe_all_senses(inp))
    assert lab.teacher_act == "wait"
    assert lab.shape == "force_wait"


def test_pullback_wait_not_fire():
    inp = MarketSenseInput(
        htf_force=[0.8] * 8,
        ltf_velocity=[-0.5] * 4,
        inertia=[0.7] * 4,
        inertia_baseline=[0.4] * 4,
        velocity_baseline=[0.1] * 4,
        full_body_outside_rails=True,
        ltf_inside_tight=True,
        regime="bull",
        g_fixed=True,
        composition_has_force=True,
        composition_has_velocity=True,
        cross_family_agree=True,
        target_percent=15.0,
        max_daily_risk_percent=2.0,
    )
    lab = aaron_force_state_from_senses(probe_all_senses(inp))
    assert lab.teacher_act == "wait"
    assert lab.shape in ("pullback_wait", "force_wait", "kill_wait", "dip_chase_wait")


def test_sample_and_train_steps():
    st, lab = sample_aaron_episode(np.random.default_rng(0), scenario="continuation_fire")
    assert st.shape[0] == 176
    assert lab.teacher_act in ("wait", "long", "short")
    brain = MetaBrain.create(seed=2)
    before = brain.meta_train_steps
    out = train_aaron_reason_curriculum(brain, steps=40, seed=2)
    assert brain.meta_train_steps > before
    assert out["shape_counts"]
    assert "continuation_fire" in out["shape_counts"] or "pullback_wait" in out["shape_counts"] or "force_wait" in out["shape_counts"]


def test_staged_curriculum_runs_all_stages():
    brain = MetaBrain.create(seed=5)
    out = train_aaron_reason_curriculum(brain, steps=80, seed=5, staged=True)
    assert out["staged"] is True
    st = out["stages"]
    assert st.get("force_wait_steps", 0) >= 1
    assert st.get("pullback_wait_steps", 0) >= 1
    assert st.get("continuation_fire_steps", 0) >= 1
    assert st["continuation_fire_steps"] >= st["force_wait_steps"]
    assert sum(out["shape_counts"].values()) >= 80


def test_hold_while_force_shape_and_reward():
    from evidence_court.meta_rl.aaron_reason_curriculum import (
        METHOD_REWARD,
        sample_aaron_episode,
    )

    st, lab = sample_aaron_episode(
        np.random.default_rng(11), scenario="hold_while_force"
    )
    assert st.shape[0] == 176
    assert lab.teacher_act in ("long", "short")
    assert lab.shape == "hold_while_force"
    assert lab.process_reward >= METHOD_REWARD["continuation_fire"] - 1e-9
    assert lab.teacher_size_frac > 0.3


def test_dip_chase_teaches_wait_not_fire():
    from evidence_court.meta_rl.aaron_reason_curriculum import sample_aaron_episode

    _, lab = sample_aaron_episode(np.random.default_rng(3), scenario="dip_chase")
    assert lab.teacher_act == "wait"
    assert lab.method_ok is False or lab.shape in (
        "dip_chase_wait",
        "pullback_wait",
        "thrash_wait",
    )


def test_method_first_goal_second_compose_on_aaron_labels():
    """Aaron process labels: method dominates; broken method zeros goal candy."""
    from evidence_court.meta_rl.aaron_reason_curriculum import (
        METHOD_REWARD,
        sample_aaron_episode,
    )
    from evidence_court.meta_rl.path_learning import compose_method_goal_reward

    _, good = sample_aaron_episode(
        np.random.default_rng(7), scenario="continuation_fire"
    )
    c_good = compose_method_goal_reward(
        good.process_reward,
        outcome_score=float(good.outcome_score),
        method_ok=bool(good.method_ok),
    )
    assert c_good["method_reward"] >= METHOD_REWARD["continuation_fire"] - 1e-9
    assert abs(c_good["goal_reward"]) < abs(c_good["method_reward"])

    _, pen = sample_aaron_episode(np.random.default_rng(8), scenario="dip_chase")
    if not pen.method_ok:
        c_pen = compose_method_goal_reward(
            max(pen.process_reward, 1.25),
            outcome_score=1.0,  # fake huge goal progress
            method_ok=False,
        )
        assert c_pen["goal_reward"] <= 0.0 + 1e-12
        assert c_pen["total"] <= c_pen["method_reward"] + 1e-9


def test_method_rich_curriculum_has_hold_and_penalties():
    brain = MetaBrain.create(seed=12)
    out = train_aaron_reason_curriculum(
        brain, steps=100, seed=12, method_rich=True
    )
    assert out["method_rich"] is True
    assert out.get("has_hold_shape") is True or "hold_while_force" in out["shape_counts"]
    st = out["stages"]
    assert st.get("hold_while_force_steps", 0) >= 1
    assert st.get("force_wait_steps", 0) >= 1
    assert st.get("continuation_fire_steps", 0) >= 1


def test_continuation_heavy_curriculum_prefers_fire_shapes():
    brain = MetaBrain.create(seed=9)
    out = train_aaron_reason_curriculum(
        brain, steps=60, seed=9, staged=True, continuation_heavy=True
    )
    assert out["stages"].get("continuation_heavy") is True
    assert out["stages"].get("continuation_fire_steps", 0) >= out["stages"].get(
        "force_wait_steps", 0
    )
    sc = out["shape_counts"]
    assert sc.get("continuation_fire", 0) >= sc.get("force_wait", 0)


def test_dethrone_decision_logic():
    from evidence_court.meta_rl.train_aaron_reason import dethrone_decision

    fail = dethrone_decision(
        {"hits": 13, "a13_frac": 0.61, "n_zero": 18, "breach_count": 0, "weights_frozen": True}
    )
    assert fail["dethrone"] is False
    assert fail["beats_hits"] is True
    assert fail["holds_a13"] is False

    ok = dethrone_decision(
        {"hits": 14, "a13_frac": 0.65, "n_zero": 15, "breach_count": 0, "weights_frozen": True}
    )
    assert ok["dethrone"] is True


def test_dethrone_rejects_live_king_dual_numbers_vs_documented_floor():
    """Live king dual (pinned CASE-0037 calendar under current path) is 12/0.61/18.

    Documented FLOOR_100D still requires a13>=0.64 — so even the king fails
    that stale a13 bar. Challenger matching live king must not auto-promote.
    """
    from evidence_court.meta_rl.path_learning import FLOOR_100D
    from evidence_court.meta_rl.train_aaron_reason import dethrone_decision

    live_king_lab = {
        "hits": 12,
        "a13_frac": 0.61,
        "n_zero": 18,
        "breach_count": 0,
        "weights_frozen": True,
    }
    dec = dethrone_decision(live_king_lab, FLOOR_100D)
    assert FLOOR_100D["a13_frac"] == 0.64
    assert dec["dethrone"] is False
    assert any("a13" in b for b in dec["blockers"])


def test_dethrone_decision_helper():
    from evidence_court.meta_rl.train_aaron_reason import dethrone_decision

    no = dethrone_decision(
        {
            "hits": 13,
            "a13_frac": 0.61,
            "n_zero": 18,
            "breach_count": 0,
            "weights_frozen": True,
        }
    )
    assert no["dethrone"] is False
    assert no["beats_hits"] is True
    yes = dethrone_decision(
        {
            "hits": 14,
            "a13_frac": 0.65,
            "n_zero": 15,
            "breach_count": 0,
            "weights_frozen": True,
        }
    )
    assert yes["dethrone"] is True
