"""Regression pins for the day-12 conversion cure."""
from __future__ import annotations

from evidence_court.meta_rl import train_day12_until_pass as day12
from evidence_court.meta_rl.brain import MetaBrain
from evidence_court.meta_rl.path_learning import ConversionTeacher


def test_day12_conversion_round_invokes_conversion_curriculum_and_reanchor(monkeypatch):
    calls = {"outcome": 0, "curriculum": 0, "reanchor": 0, "sample": 0}

    def fake_apply_conversion_path_teachers(brain, labs, *, lr, seed, max_examples, n_passes, bucket_weights):
        calls["outcome"] += 1
        assert brain is not None
        assert labs
        assert max_examples == 1400
        assert n_passes >= 2
        assert "clear" in bucket_weights
        return {"n_updates": 7, "has_wait": True, "has_hold_convert": True, "has_size_down": True, "class_counts": {"hold_convert": 1}}

    def fake_train_path_learning_curriculum(brain, **kwargs):
        calls["curriculum"] += 1
        assert brain is not None
        assert kwargs["path_examples"]
        assert kwargs["steps"] >= 1800
        return {
            "steps": kwargs["steps"],
            "has_conversion": True,
            "has_outcome_shaping": True,
            "path_only_clone": False,
            "class_counts": {"conversion": 3, "path_anchor": 1, "process": 1},
            "path_anchor_frac_realized": 0.12,
        }

    def fake_path_reanchor(brain, labs, *, n_passes, seed, max_examples):
        calls["reanchor"] += 1
        assert brain is not None
        assert labs
        assert n_passes >= 1
        assert max_examples == 400
        return 5

    def fake_sample_conversion_episode(rng, holdout_mode=False):
        calls["sample"] += 1
        st = [0.0] * 176
        ct = ConversionTeacher("long", 0.6, "fire_edge_low_progress", "fire_edge")
        return st, ct, 0.25

    monkeypatch.setattr(day12, "apply_conversion_path_teachers", fake_apply_conversion_path_teachers)
    monkeypatch.setattr(day12, "train_path_learning_curriculum", fake_train_path_learning_curriculum)
    monkeypatch.setattr(day12, "path_reanchor", fake_path_reanchor)
    monkeypatch.setattr(day12, "sample_conversion_episode", fake_sample_conversion_episode)

    brain = MetaBrain.create(seed=3)
    multi_day_labs = [
        {
            "state": [0.0] * 176,
            "teacher_act": "long",
            "topology": "pullback_resume",
            "source": "path_state_htf_active",
            "n_htf_active": 2,
            "day_bucket": "clear",
            "outcome_tagged": True,
        },
        {
            "state": [0.1] * 176,
            "teacher_act": "short",
            "topology": "continuation",
            "source": "path_state_htf_active",
            "n_htf_active": 3,
            "day_bucket": "dead",
            "outcome_tagged": True,
        },
        {
            "state": [0.2] * 176,
            "teacher_act": "short",
            "topology": "pullback_resume",
            "source": "path_state_htf_active",
            "n_htf_active": 2,
            "day_bucket": "near_breach",
            "outcome_tagged": True,
        },
    ]
    day12_labs = multi_day_labs[:2]

    out = day12._teach_conversion_round(
        brain,
        multi_day_labs=multi_day_labs,
        day12_labs=day12_labs,
        round_i=2,
        seed=11,
    )

    assert calls == {"outcome": 1, "curriculum": 1, "reanchor": 1, "sample": 460}
    assert out["mode"] == "conversion_not_fire_clone"
    assert out["day12_labs_used"] == 2
    assert out["multi_day_labs"] == 3
    assert out["conversion_apply"]["has_hold_convert"] is True
    assert out["curriculum"]["has_conversion"] is True
    assert out["n_reanchor"] == 5
    assert out["fire_only_same_day"] is False
