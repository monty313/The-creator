"""CASE-0017 NEW tests: regime-aware meta curriculum (ISSUE-ROAD)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.policy import (
    sample_training_state,
    teacher_action_for_state,
    train_goal_conditioned_meta_policy,
)
from evidence_court.meta_rl.regimes import (
    RegimeId,
    all_curriculum_regimes,
    build_official_for_regime,
    curriculum_regime_self_check,
    regime_allows_fire,
    regime_kill_new_risk,
    regime_sensor_template,
    sample_curriculum_regime,
    teacher_action_under_regime,
)
from evidence_court.meta_rl.state import META_RL_DIM, build_meta_rl_state


def test_creator_new_curriculum_covers_all_a17_regimes():
    """Creator NEW: meta curriculum samples every Court regime (balanced road coverage)."""
    rng = np.random.default_rng(17)
    seen = set()
    for _ in range(400):
        rid = sample_curriculum_regime(rng)
        seen.add(rid)
        st, teacher, topo, r2 = sample_training_state(
            rng, target=15.0, risk=2.0, regime=rid, return_regime=True
        )
        assert r2 == rid
        assert st.shape == (META_RL_DIM,)
        assert teacher in ("wait", "long", "short")
        assert isinstance(topo, str)
    assert seen == set(all_curriculum_regimes())
    assert len(seen) == 8


def test_mark_new_teacher_obeys_a17_fire_kill_playbook():
    """Mark NEW: kill/no-fire regimes always teach wait; trend can teach directed fire."""
    # Kill regimes: never thrash labels even with strong mean_dir
    for rid in (RegimeId.CONFLICT, RegimeId.VOL_COMPRESSION):
        assert regime_kill_new_risk(rid)
        act = teacher_action_under_regime(
            rid,
            mean_dir=0.95,
            allow=True,
            risk_rem=1.0,
            hardness=0.1,
            pressure=0.8,
            topology="launch",
        )
        assert act == "wait", rid

    # Non-allow (chop / incomplete): also wait
    for rid in (RegimeId.RANGE_CHOP, RegimeId.INCOMPLETE):
        assert not regime_allows_fire(rid)
        assert (
            teacher_action_under_regime(
                rid,
                mean_dir=0.9,
                allow=True,
                risk_rem=1.0,
                hardness=0.1,
                pressure=0.8,
                topology="launch",
            )
            == "wait"
        )

    # Trend bull with strong dir → long
    assert (
        teacher_action_under_regime(
            RegimeId.TREND_BULL,
            mean_dir=0.9,
            allow=True,
            risk_rem=1.0,
            hardness=0.15,
            pressure=0.6,
            topology="launch",
        )
        == "long"
    )
    # Trend bear → short
    assert (
        teacher_action_under_regime(
            RegimeId.TREND_BEAR,
            mean_dir=-0.9,
            allow=True,
            risk_rem=1.0,
            hardness=0.15,
            pressure=0.6,
            topology="launch",
        )
        == "short"
    )


def test_creator_new_sensor_templates_classify_to_declared_regime():
    """Creator counter NEW: each curriculum sensor template round-trips classify_regime_court."""
    assert curriculum_regime_self_check()["ok"] is True
    for rid in all_curriculum_regimes():
        tpl = regime_sensor_template(rid)
        from evidence_court.meta_rl.regimes import classify_regime_court

        got = classify_regime_court(
            multi_set_consensus=str(tpl["multi_set_consensus"]),
            force=float(tpl["force"]),
            efficiency=float(tpl["efficiency"]),
        )
        assert got == rid, (rid, got, tpl)


def test_mark_new_meta_train_uses_regime_labels_without_dim_change():
    """Mark counter NEW: train path stays META_RL_DIM; conflict samples label wait."""
    assert META_RL_DIM == 176
    rng = np.random.default_rng(42)
    st, teacher, _topo = sample_training_state(
        rng, target=30.0, risk=2.0, regime=RegimeId.CONFLICT
    )
    assert st.shape == (META_RL_DIM,)
    assert teacher == "wait"
    # Wired teacher_action_for_state with regime
    assert teacher_action_for_state(st, topology="launch", regime=RegimeId.CONFLICT) == "wait"
    # Short meta-train still produces trained champion (no dim cliff)
    pol = train_goal_conditioned_meta_policy(seed=17, n_steps=80, freeze=True)
    assert pol.trained is True
    assert pol.weights.shape == (META_RL_DIM,)
    assert pol.meta_train_steps >= 80
    # Official builder covers 4 Mark sets for every regime
    for rid in all_curriculum_regimes():
        off = build_official_for_regime(rid, side=1, strength=0.75)
        assert set(off.keys()) == {1, 2, 3, 4}
        s = build_meta_rl_state(
            target_percent=10.0,
            max_daily_risk_percent=2.0,
            official=off,
        )
        assert s.shape == (META_RL_DIM,)
