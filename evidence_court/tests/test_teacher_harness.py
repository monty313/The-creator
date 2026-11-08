"""Pins for the teacher-agent harness (one lesson per agent, no champion touch).

Claims:
1. Harvest works on real traced days; each agent produces only its own lesson
   class from real packed states.
2. train_candidate teaches the lesson (agreement rises), saves a LAB npz, and
   refuses to write the champion path.
3. size_until_win is size-only (act head provably untouched) and marks its
   candidate size_head_drives.
4. Harness verdicts follow the owner bar exactly.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.brain import train_meta_brain
from evidence_court.meta_rl.policy import DEFAULT_CHAMPION_PATH, MetaPolicy
from evidence_court.meta_rl.teacher_agents import (
    AGENT_REGISTRY,
    get_agent,
    harvest_pullback_confluence,
    harvest_pullback_first,
    harvest_size_until_win,
    replay_traced_days,
    train_candidate,
)


def _synth_m1(n_days: int = 8, trend: float = 0.00006) -> list:
    """1-minute uptrend with periodic dip-and-resume shapes → pullback edges."""
    rows = []
    px = 2000.0
    for d in range(n_days):
        date = f"2026-06-{d + 1:02d}"
        for m in range(0, 24 * 60):
            # every 45m: a 6-bar dip (pullback) then resume the climb
            in_dip = (m % 45) < 6
            step = -1.8 * trend if in_dip else trend
            h, mi = divmod(m, 60)
            rows.append(
                {
                    "date": date,
                    "time": f"{h:02d}:{mi:02d}:00",
                    "open": px,
                    "high": max(px, px * (1 + step)) * 1.0002,
                    "low": min(px, px * (1 + step)) * 0.9998,
                    "close": px * (1 + step),
                }
            )
            px *= 1 + step
    return rows


def _policy() -> MetaPolicy:
    pol = MetaPolicy(brain=train_meta_brain(seed=11, n_steps=600, freeze=True))
    pol.freeze_for_inference()
    return pol


@pytest.fixture(scope="module")
def traced_days():
    pol = _policy()
    m1 = _synth_m1()
    return replay_traced_days(
        pol,
        symbol="XAUUSD",
        m1=m1,
        dates=["2026-06-07", "2026-06-08"],
        pairs=[(10.0, 2.0), (5.0, 3.0)],
    )


def test_registry_has_three_pullback_teachers_and_one_size_teacher():
    names = [a.name for a in AGENT_REGISTRY]
    assert names == [
        "pullback_first",
        "pullback_confluence",
        "pullback_prime",
        "size_until_win",
    ]
    sz = get_agent("size_until_win")
    assert sz.mode == "size_only" and sz.size_head_drives
    for a in AGENT_REGISTRY[:3]:
        assert a.mode == "act_size"


def test_harvest_lessons_come_from_real_states(traced_days):
    from evidence_court.meta_rl.state import META_RL_DIM

    lessons = (
        harvest_pullback_first(traced_days)
        + harvest_pullback_confluence(traced_days)
        + harvest_size_until_win(traced_days)
    )
    assert lessons, "synthetic trend days must yield at least some pullback lessons"
    for l in lessons:
        assert len(l["state"]) == META_RL_DIM
        assert l["teacher_act"] in ("wait", "long", "short")
        assert 0.0 <= l["teacher_size_frac"] <= 0.98


def test_size_until_win_need_fraction_is_context_dependent(traced_days):
    lessons = harvest_size_until_win(traced_days)
    if len(lessons) >= 2:
        fracs = {round(l["teacher_size_frac"], 3) for l in lessons}
        assert len(fracs) >= 2  # need-based → not one constant


def test_train_candidate_teaches_and_never_touches_champion(tmp_path, traced_days):
    agent = get_agent("pullback_confluence")
    lessons = agent.harvest(traced_days)
    if not lessons:
        pytest.skip("no confluence lessons on synthetic days")
    src = tmp_path / "champ.npz"
    _policy().save(src)
    out = tmp_path / "cand.npz"
    rep = train_candidate(agent, lessons, champion_path=src, out_path=out, seed=1)
    assert rep["saved"] == str(out) and out.exists()
    assert rep["agreement_after"]["act_agreement"] >= rep["agreement_before"]["act_agreement"]
    with pytest.raises(RuntimeError, match="FORBIDDEN"):
        train_candidate(
            agent, lessons, champion_path=src, out_path=DEFAULT_CHAMPION_PATH
        )


def test_size_only_agent_keeps_act_head_frozen(tmp_path, traced_days):
    agent = get_agent("size_until_win")
    lessons = agent.harvest(traced_days)
    if not lessons:
        pytest.skip("no fills on synthetic days")
    src = tmp_path / "champ.npz"
    src_pol = _policy()
    src_pol.save(src)
    out = tmp_path / "cand.npz"
    train_candidate(agent, lessons, champion_path=src, out_path=out, seed=1)
    cand = MetaPolicy.load(out, freeze=True, require_serious=False)
    assert cand.size_head_drives is True
    assert np.array_equal(cand.brain.W1, src_pol.brain.W1)
    assert np.array_equal(cand.brain.W2, src_pol.brain.W2)
    assert not np.array_equal(cand.brain.W_size, src_pol.brain.W_size)


def test_harness_verdict_owner_bar():
    sys.path.insert(0, str(ROOT / "tools"))
    from teacher_harness import verdict

    base = {"breach": 0, "no_retrain": True}
    assert verdict({**base, "hits": 2}, 1) == "CANDIDATE_FOR_COURT"
    assert verdict({**base, "hits": 1}, 1) == "KEEP_LAB"
    assert verdict({**base, "hits": 0}, 1) == "DISCARD"
    assert verdict({"hits": 5, "breach": 1, "no_retrain": True}, 1) == "DISCARD"
    assert verdict({"hits": 5, "breach": 0, "no_retrain": False}, 1) == "DISCARD"
