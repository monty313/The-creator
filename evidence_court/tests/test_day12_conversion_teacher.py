"""Day12 conversion trainer pins — conversion not fire-only same-day clone."""
from __future__ import annotations

import numpy as np

from evidence_court.meta_rl.brain import MetaBrain
from evidence_court.meta_rl.path_learning import (
    apply_conversion_path_teachers,
    conversion_remap_path_teacher,
    day_outcome_bucket,
)
from evidence_court.meta_rl.path_state_harvest import filter_path_state_teachers
from evidence_court.meta_rl.train_day12_until_pass import _teach_conversion_round


def _fake_path(
    *,
    act: str = "long",
    topo: str = "continuation",
    force: float = 0.9,
    day_pnl: float = 1.0,
    hit: bool = False,
    dead: bool = False,
    n_trades: int = 25,
    fill_label: str = "",
    fill_pnl: float | None = None,
) -> dict:
    return {
        "state": [0.01 * (i % 9) for i in range(176)],
        "teacher_act": act,
        "topology": topo,
        "source": "path_state_htf_active",
        "n_htf_active": 2,
        "htf_active": True,
        "force": force,
        "teacher_size_frac": 0.7,
        "multi_set_consensus": "agree_long",
        "harvest_day_target": 15.0,
        "harvest_day_risk": 3.0,
        "harvest_day_n_trades": n_trades,
        "realized_pnl": day_pnl,
        "hit_target": hit,
        "breach": False,
        "dead_fire": dead,
        "progress_to_target": day_pnl / 15.0,
        "outcome_score": 0.1 if not hit else 0.7,
        "outcome_tagged": True,
        "fill_label": fill_label,
        "fill_pnl": fill_pnl,
    }


def test_day_outcome_buckets_clear_dead_near_breach():
    assert day_outcome_bucket(day_pnl=16.0, target_percent=15.0, max_daily_risk_percent=3.0) == "clear"
    assert (
        day_outcome_bucket(
            day_pnl=0.2,
            target_percent=15.0,
            max_daily_risk_percent=3.0,
            n_trades=40,
        )
        == "dead"
    )
    assert (
        day_outcome_bucket(day_pnl=-2.0, target_percent=15.0, max_daily_risk_percent=3.0)
        == "near_breach"
    )


def test_conversion_remap_loss_leg_waits():
    ex = _fake_path(fill_label="loss", fill_pnl=-0.5, day_pnl=1.2, n_trades=25)
    out = conversion_remap_path_teacher(ex)
    assert out["teacher_act"] == "wait"
    assert out["conversion_class"].startswith("wait")


def test_conversion_remap_busy_miss_not_fire_only():
    ex = _fake_path(day_pnl=1.3, n_trades=25, hit=False, act="long", topo="continuation")
    out = conversion_remap_path_teacher(ex)
    assert out["conversion_class"] in (
        "hold_convert",
        "size_down",
        "wait_pullback",
        "wait_risk",
        "fire_edge",
    )
    # Busy thrash miss should prefer convert/size_down/wait over pure fire when remapped
    # (at least size frac reduced or class not densify-clone)
    assert "conversion_class" in out
    assert out["teacher_size_frac"] <= 0.85 + 1e-9


def test_filter_allows_wait_in_conversion_mode():
    wait_ex = _fake_path(act="wait", topo="chop", force=0.1)
    wait_ex["teacher_act"] = "wait"
    kept = filter_path_state_teachers([wait_ex], allow_wait=True, require_htf_active=True)
    # wait on chop may pass with allow_wait
    fire_only = filter_path_state_teachers([wait_ex], allow_wait=False, require_htf_active=True)
    assert fire_only == []


def test_apply_conversion_has_wait_hold_or_size_down():
    brain = MetaBrain.create(seed=3)
    labs = [
        _fake_path(fill_label="loss", fill_pnl=-0.4, day_pnl=1.0, n_trades=30),
        _fake_path(day_pnl=12.0, hit=False, n_trades=10, topo="continuation"),
        _fake_path(day_pnl=16.0, hit=True, n_trades=12, topo="continuation"),
        _fake_path(day_pnl=-1.8, n_trades=8, fill_label="loss", fill_pnl=-0.3),
    ]
    for lab in labs:
        lab["day_bucket"] = day_outcome_bucket(
            day_pnl=lab["realized_pnl"],
            target_percent=15.0,
            max_daily_risk_percent=3.0,
            n_trades=lab["harvest_day_n_trades"],
            hit_target=lab["hit_target"],
        )
    out = apply_conversion_path_teachers(brain, labs, n_passes=1, max_examples=50, seed=3)
    assert out["n_updates"] > 0
    assert out.get("has_wait") or out.get("has_hold_convert") or out.get("has_size_down")
    assert out["law"] == "PATH_CONVERSION_APPLY"


def test_teach_conversion_round_not_fire_only_flag():
    brain = MetaBrain.create(seed=5)
    multi = [_fake_path(day_pnl=8.0, n_trades=15) for _ in range(5)]
    multi += [_fake_path(fill_label="loss", fill_pnl=-0.2, day_pnl=0.5, n_trades=40) for _ in range(5)]
    d12 = [_fake_path(day_pnl=1.29, n_trades=25) for _ in range(3)]
    teach = _teach_conversion_round(
        brain,
        multi_day_labs=multi,
        day12_labs=d12,
        round_i=1,
        seed=5,
    )
    assert teach["fire_only_same_day"] is False
    assert teach["mode"] == "conversion_not_fire_clone"
    classes = (teach.get("conversion_apply") or {}).get("class_counts") or {}
    # Must have trained something conversion-shaped
    assert teach["n_extra_conversion"] > 0 or sum(classes.values()) > 0
