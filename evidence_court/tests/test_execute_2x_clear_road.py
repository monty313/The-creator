"""Pins for 2× CLEAR ROAD: outcome tags + outcome-shaped path apply (shipped)."""
from __future__ import annotations

import numpy as np

from evidence_court.meta_rl.brain import MetaBrain
from evidence_court.meta_rl.path_learning import (
    apply_outcome_shaped_update,
    apply_outcome_tagged_path_teachers,
    outcome_scale,
    outcome_score_from_fields,
    outcome_score_from_teacher,
    path_learning_promote_guard,
    stamp_path_teacher_day_outcome,
)


def test_stamp_path_teacher_day_outcome_sets_tags():
    ex = {
        "state": [0.0] * 176,
        "teacher_act": "long",
        "topology": "pullback_resume",
        "source": "path_state_htf_active",
        "n_htf_active": 2,
        "teacher_size_frac": 0.6,
    }
    hit = stamp_path_teacher_day_outcome(
        ex, day_pnl=20.0, target_percent=15.0, max_daily_risk_percent=2.0, n_trades=12
    )
    assert hit["outcome_tagged"] is True
    assert hit["hit_target"] is True
    assert hit["breach"] is False
    assert hit["outcome_score"] > 0.3

    bad = stamp_path_teacher_day_outcome(
        ex, day_pnl=-3.0, target_percent=15.0, max_daily_risk_percent=2.0, n_trades=5
    )
    assert bad["breach"] is True
    assert bad["outcome_score"] < 0.0
    assert outcome_scale(hit["outcome_score"]) > outcome_scale(bad["outcome_score"])


def test_outcome_score_affects_reward_path_not_act_only():
    """Shipped outcome_scale: clear day reward > dead/breach for same act."""
    clear = outcome_score_from_fields(hit_target=True, progress_to_target=0.9, r_capture=0.5)
    dead = outcome_score_from_fields(dead_fire=True)
    breach = outcome_score_from_fields(breach=True)
    assert outcome_scale(clear) > outcome_scale(dead) > outcome_scale(breach) * 0.99


def test_apply_outcome_tagged_path_teachers_uses_shipped_update():
    brain = MetaBrain.create(seed=2)
    before = brain.meta_train_steps
    examples = []
    for i, pnl in enumerate((20.0, -3.0, 1.0)):
        st = [0.01 * ((i + j) % 5) for j in range(176)]
        ex = stamp_path_teacher_day_outcome(
            {
                "state": st,
                "teacher_act": "long" if i % 2 == 0 else "short",
                "topology": "continuation",
                "source": "path_state_htf_active",
                "n_htf_active": 2,
                "teacher_size_frac": 0.55,
            },
            day_pnl=pnl,
            target_percent=15.0,
            max_daily_risk_percent=2.0,
            n_trades=10,
        )
        examples.append(ex)
    out = apply_outcome_tagged_path_teachers(
        brain, examples, lr=0.02, seed=2, max_examples=10, n_passes=1
    )
    assert out["n_updates"] >= 1
    assert brain.meta_train_steps > before
    assert out["n_tagged"] >= 1
    assert np.isfinite(out["mean_outcome_score"])


def test_outcome_score_from_teacher_reads_stamp():
    ex = stamp_path_teacher_day_outcome(
        {
            "state": [0.0] * 176,
            "teacher_act": "short",
            "topology": "pullback_resume",
            "source": "path_state_miss",
            "n_htf_active": 1,
        },
        day_pnl=15.0,
        target_percent=15.0,
        max_daily_risk_percent=2.0,
        n_trades=8,
    )
    assert abs(outcome_score_from_teacher(ex) - float(ex["outcome_score"])) < 1e-9


def test_promote_guard_blocks_production_without_floor():
    dual = {
        "a13_frac": 0.5,
        "hits": 12,
        "n_zero": 15,
        "breach_count": 0,
        "weights_frozen": True,
        "low_hr": 0.25,
    }
    g = path_learning_promote_guard(
        dual,
        None,
        path_only_clone=False,
        has_outcome_conversion_mix=True,
        court_promote=False,
    )
    assert g["production_replace"] is False
