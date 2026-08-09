"""CASE-0037 NEW tests: packed path-state teachers at brain-wait (anti F-025)."""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import run_goal_path_day, allows_empty_slot_skip
from evidence_court.meta_rl.path_state_harvest import (
    apply_path_state_teachers_to_brain,
    filter_path_state_teachers,
    train_path_state_a13_policy,
)
from evidence_court.meta_rl.brain import MetaBrain
from evidence_court.meta_rl.state import META_RL_DIM, build_meta_rl_state


def _fake_path_examples(n: int = 4) -> list:
    out = []
    for i in range(n):
        st = build_meta_rl_state(
            target_percent=15.0 + i,
            max_daily_risk_percent=2.0,
            progress_to_target=0.1 * i,
            session_phase=0.4 + 0.05 * i,
        )
        # mark force dirs so state is non-zero on eyes
        st = st.copy()
        st[0] = 0.7 if i % 2 == 0 else -0.7
        out.append(
            {
                "state": [float(x) for x in st],
                "teacher_act": "long" if i % 2 == 0 else "short",
                "teacher_size_frac": 0.7,
                "topology": "pullback_resume" if i % 2 == 0 else "continuation",
                "session_band": "london_ny" if i < 3 else "other",
                "weight": 1.5 if i < 3 else 1.0,
                "symbol": "XAUUSD",
                "asof_date": f"2026-03-0{i+1}",
                "asof_time": "14:00:00",
                "force": 0.4 if i % 2 == 0 else -0.4,
                "what_bot_did": "wait",
                "source": "path_state_miss",
            }
        )
    # smuggle synthetic-state-class junk
    out.append(
        {
            "state": [0.1] * META_RL_DIM,
            "teacher_act": "long",
            "topology": "chop",
            "source": "path_state_miss",
            "asof_date": "2026-03-09",
        }
    )
    out.append(
        {
            "state": [0.1] * 10,  # wrong dim
            "teacher_act": "short",
            "topology": "continuation",
            "source": "path_state_miss",
            "asof_date": "2026-03-10",
        }
    )
    out.append(
        {
            "state": [0.1] * META_RL_DIM,
            "teacher_act": "long",
            "topology": "continuation",
            "source": "synthetic_rebuild",  # F-025 class
            "asof_date": "2026-03-11",
        }
    )
    return out


def test_creator_new_filter_requires_full_dim_path_state():
    """Creator NEW: only META_RL_DIM path_state_miss PB/cont teachers survive."""
    labs = filter_path_state_teachers(_fake_path_examples(4), max_examples=20)
    assert len(labs) == 4
    assert all(len(x["state"]) == META_RL_DIM for x in labs)
    assert all(x["source"] == "path_state_miss" for x in labs)
    assert all(x["topology"] in ("pullback_resume", "continuation") for x in labs)
    assert all(x["teacher_act"] in ("long", "short") for x in labs)


def test_mark_new_apply_path_state_updates_on_packed_state():
    """Mark NEW: meta_update uses packed state vector (not rebuild from fields)."""
    brain = MetaBrain.create(seed=5)
    labs = filter_path_state_teachers(_fake_path_examples(4))
    n0 = brain.meta_train_steps
    n = apply_path_state_teachers_to_brain(brain, labs, seed=2)
    assert n == len(labs)
    assert brain.meta_train_steps >= n0 + n
    assert brain.trained is True
    # London/NY weight present in set
    assert any(x["session_band"] == "london_ny" for x in labs)


def test_creator_new_path_state_train_freezes_no_retrain():
    """Creator counter: path-state mix train freezes across target/risk pairs."""
    labs = filter_path_state_teachers(_fake_path_examples(4))
    pol = train_path_state_a13_policy(labs, seed=19, n_steps=60, path_mix=0.25)
    assert pol.trained is True
    fp = pol.weight_fingerprint()
    for t, r in ((5.0, 1.0), (50.0, 2.0), (90.0, 3.0)):
        st = build_meta_rl_state(target_percent=t, max_daily_risk_percent=r)
        _ = pol.forward(st)
    pol.assert_frozen()
    assert pol.weight_fingerprint() == fp
    assert pol.inference_updates == 0


def test_mark_new_goal_path_exposes_collect_flag_no_pad():
    """Mark counter: collect flag exists; empty skip still True (no pad)."""
    sig = inspect.signature(run_goal_path_day)
    assert "collect_path_state_teachers" in sig.parameters
    assert sig.parameters["collect_path_state_teachers"].default is False
    assert allows_empty_slot_skip() is True
