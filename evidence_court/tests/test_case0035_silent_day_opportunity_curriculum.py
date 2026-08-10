"""CASE-0035 NEW tests: silent-day unlock via opportunity curriculum (C-002 residual)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import (
    CONT_HOLD_MIN_MINUTES,
    PRODUCTION_CADENCE_INTERVAL_MIN,
    PRODUCTION_SCALPING_SLOTS,
    allows_empty_slot_skip,
    production_symbols_per_slot,
)
from evidence_court.meta_rl.policy import (
    opportunity_label_to_training_example,
    silent_day_opportunity_curriculum,
    train_goal_conditioned_meta_policy,
    train_silent_day_opportunity_policy,
)
from evidence_court.meta_rl.state import META_RL_DIM, build_meta_rl_state


def test_creator_new_silent_day_curriculum_london_ny_fire_teachers():
    """Creator NEW: denser miss curriculum is mostly London/NY fire teachers (not wait)."""
    labs = silent_day_opportunity_curriculum(40)
    assert len(labs) == 40
    fires = [x for x in labs if x["teacher_act"] in ("long", "short")]
    assert len(fires) == 40
    london = [x for x in labs if x.get("session_band") == "london_ny"]
    other = [x for x in labs if x.get("session_band") == "other"]
    assert len(london) >= int(0.6 * len(labs))
    assert other, "need other-band controls for weight contrast"
    assert all(x.get("weight", 0) >= 1.0 for x in labs)
    assert float(london[0]["weight"]) > float(other[0]["weight"])
    st, teacher, sf = opportunity_label_to_training_example(labs[0], target=15.0, risk=2.0)
    assert st.shape == (META_RL_DIM,)
    assert teacher in ("long", "short")
    assert sf > 0


def test_mark_new_curriculum_only_pb_cont_no_chop_teacher():
    """Mark NEW: curriculum teachers are only pullback_resume / continuation (Mark eyes)."""
    labs = silent_day_opportunity_curriculum(48)
    topos = {str(x.get("topology")) for x in labs}
    assert topos <= {"pullback_resume", "continuation"}
    assert "chop" not in topos
    assert "collapse" not in topos
    assert all(x.get("multi_set_agree") is True for x in labs)
    # both sides and both topologies present
    assert {"long", "short"} <= {x["teacher_act"] for x in labs}
    assert {"pullback_resume", "continuation"} <= topos


def test_creator_new_opp_train_freezes_no_retrain_at_prove():
    """Creator counter NEW: shadow opp train freezes; fingerprint stable across pairs."""
    pol = train_silent_day_opportunity_policy(
        seed=35, n_steps=80, n_labels=16, opportunity_mix=0.2, freeze=True
    )
    assert pol.trained is True
    fp = pol.weight_fingerprint()
    for t, r in ((5.0, 1.0), (30.0, 2.0), (70.0, 3.0)):
        st = build_meta_rl_state(target_percent=t, max_daily_risk_percent=r)
        _ = pol.forward(st)
    pol.assert_frozen()
    assert pol.weight_fingerprint() == fp
    assert pol.inference_updates == 0


def test_mark_new_a27_a26_geometry_preserved():
    """Mark counter NEW: A27 5m + A26 hold + dual-on-agree + empty skip preserved."""
    assert PRODUCTION_CADENCE_INTERVAL_MIN == 5
    assert len(PRODUCTION_SCALPING_SLOTS) >= 8
    assert CONT_HOLD_MIN_MINUTES == 10
    assert allows_empty_slot_skip() is True
    assert production_symbols_per_slot(multi_set_consensus="agree_long") == 2
    assert production_symbols_per_slot(multi_set_consensus="incomplete") == 1
    # Default champion path training API still exists (no PROVEN overwrite in unit)
    pol = train_goal_conditioned_meta_policy(seed=3, n_steps=50, freeze=True)
    assert pol.trained is True
