"""C-002 NEW tests: opportunity-labeled meta-train from Watch curriculum_labels."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.opportunity_watch import (
    OpportunityWatchAgent,
    curriculum_labels_from_report,
)
from evidence_court.meta_rl.edge import SetEdge, SymbolEdgeSnapshot
from evidence_court.meta_rl.policy import (
    apply_opportunity_labels_to_brain,
    opportunity_label_to_training_example,
    train_goal_conditioned_meta_policy,
)
from evidence_court.meta_rl.brain import MetaBrain
from evidence_court.meta_rl.state import META_RL_DIM


def _miss_labels(n: int = 4) -> list:
    agent = OpportunityWatchAgent()
    labels = []
    for i, (topo, side, t) in enumerate(
        [
            ("pullback_resume", "long", "14:00:00"),
            ("continuation", "short", "10:30:00"),
            ("pullback_resume", "long", "03:00:00"),
            ("continuation", "long", "15:00:00"),
        ]
    ):
        force = 0.45 if side == "long" else -0.45
        e = SetEdge(1, "s", abs(force), 50.0, topo, side, "r", True)
        snap = SymbolEdgeSnapshot("XAUUSD", [e], force, e, "agree_long" if side == "long" else "agree_short", 1, 0)
        rep = agent.scan_snapshot(
            snap, asof_date="2026-02-01", asof_time=t, bot_act="wait", bot_fired=False
        )
        labels.extend(curriculum_labels_from_report(rep))
        if len(labels) >= n:
            break
    return labels[:n]


def test_creator_new_opportunity_label_to_example():
    """Creator NEW: miss label → state + teacher fire (London/NY weight)."""
    labs = _miss_labels(2)
    assert labs
    st, teacher, sf = opportunity_label_to_training_example(labs[0], target=15.0, risk=2.0)
    assert st.shape == (META_RL_DIM,)
    assert teacher in ("long", "short")
    assert sf > 0


def test_mark_new_apply_labels_updates_brain():
    """Mark NEW: offline apply_opportunity_labels_to_brain increases meta_train_steps."""
    brain = MetaBrain.create(seed=9)
    assert brain.meta_train_steps == 0
    labs = _miss_labels(4)
    n = apply_opportunity_labels_to_brain(brain, labs, target=20.0, risk=2.0, seed=3)
    assert n == len(labs)
    assert brain.meta_train_steps >= n
    assert brain.trained is True


def test_creator_new_train_with_opportunity_labels_no_retrain_at_prove():
    """Creator counter: train with labels → frozen prove fingerprint stable across pairs."""
    labs = _miss_labels(4)
    pol = train_goal_conditioned_meta_policy(
        seed=21,
        n_steps=120,
        freeze=True,
        opportunity_labels=labs,
        opportunity_mix=0.2,
    )
    assert pol.trained is True
    assert pol.meta_train_steps >= 120
    fp = pol.weight_fingerprint()
    from evidence_court.meta_rl.state import build_meta_rl_state

    for t, r in ((5.0, 1.0), (30.0, 2.0), (70.0, 3.0)):
        st = build_meta_rl_state(target_percent=t, max_daily_risk_percent=r)
        _ = pol.forward(st)
    pol.assert_frozen()
    assert pol.weight_fingerprint() == fp
    assert pol.inference_updates == 0


def test_mark_new_london_ny_label_weight_higher():
    """Mark counter: London/NY miss weight > other session in curriculum labels."""
    labs = _miss_labels(4)
    london = [x for x in labs if x.get("session_band") == "london_ny"]
    other = [x for x in labs if x.get("session_band") == "other"]
    assert london
    assert other
    assert london[0]["weight"] > other[0]["weight"]
