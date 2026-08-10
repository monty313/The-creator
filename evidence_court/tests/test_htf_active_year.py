"""Unit pins for HTF-active path-state filter + champion promote floor decision."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from evidence_court.meta_rl.path_state_harvest import filter_path_state_teachers
from evidence_court.meta_rl.state import META_RL_DIM
from evidence_court.meta_rl.train_htf_active_year import FLOOR, PACK, beats_floor


def _ex(**kw):
    st = np.zeros(META_RL_DIM, dtype=np.float64)
    st[0] = 0.5
    row = {
        "state": st.tolist(),
        "teacher_act": "long",
        "topology": "pullback_resume",
        "source": "path_state_miss",
        "force": 0.4,
        "n_htf_active": 2,
        "htf_active": True,
        "session_band": "london_ny",
        "weight": 1.5,
    }
    row.update(kw)
    return row


def test_filter_requires_n_htf_active_ge_1():
    """Strict gate: missing/0 n_htf_active dropped even if htf_active stamped True."""
    dead_flag = _ex(n_htf_active=0, htf_active=True, force=0.5)
    dead_missing = _ex()
    del dead_missing["n_htf_active"]
    dead_missing["htf_active"] = True
    live = _ex(n_htf_active=1, htf_active=True, force=0.3)
    out = filter_path_state_teachers(
        [dead_flag, dead_missing, live], max_examples=10, require_htf_active=True
    )
    assert len(out) == 1
    assert int(out[0]["n_htf_active"]) >= 1
    assert out[0]["teacher_act"] == "long"


def test_filter_does_not_launder_watch_miss_without_n_htf():
    watch = _ex(
        source="path_state_watch_miss",
        n_htf_active=0,
        htf_active=True,
        weight=1.5,
    )
    out = filter_path_state_teachers([watch], max_examples=5, require_htf_active=True)
    assert out == []


def test_filter_keeps_watch_miss_with_n_htf():
    watch = _ex(
        source="path_state_watch_miss",
        n_htf_active=2,
        htf_active=True,
        teacher_act="short",
        topology="continuation",
    )
    out = filter_path_state_teachers([watch], max_examples=5, require_htf_active=True)
    assert len(out) == 1
    assert out[0]["source"] == "path_state_watch_miss"
    assert int(out[0]["n_htf_active"]) == 2


def test_filter_keeps_only_long_short_pb_cont():
    bad_act = _ex(teacher_act="wait")
    bad_topo = _ex(topology="chop")
    good = _ex(topology="continuation", teacher_act="short")
    out = filter_path_state_teachers(
        [bad_act, bad_topo, good], max_examples=10, require_htf_active=True
    )
    assert len(out) == 1
    assert out[0]["teacher_act"] == "short"
    assert out[0]["topology"] == "continuation"


def test_filter_rejects_wrong_dim():
    bad = _ex()
    bad["state"] = [0.1, 0.2]  # not META_RL_DIM
    out = filter_path_state_teachers([bad], max_examples=5, require_htf_active=True)
    assert out == []


def test_beats_floor_true_when_hold_and_improve_a13():
    score = {
        "hits": 11,
        "low_hr": 0.28,
        "a13_frac": 0.70,
        "n_zero": 18,
        "breach_count": 0,
        "breach": False,
    }
    d = beats_floor(score, FLOOR)
    assert d["beats"] is True
    assert d["hold_floor"] is True
    assert "a13" in d["improved"]


def test_beats_floor_false_on_breach():
    score = {
        "hits": 20,
        "low_hr": 0.5,
        "a13_frac": 0.9,
        "n_zero": 0,
        "breach_count": 1,
        "breach": True,
    }
    d = beats_floor(score, FLOOR)
    assert d["beats"] is False
    assert "breach" in d["fail"]


def test_beats_floor_false_when_equal_no_improve():
    score = {
        "hits": 11,
        "low_hr": 0.28,
        "a13_frac": 0.64,
        "n_zero": 18,
        "breach_count": 0,
        "breach": False,
    }
    d = beats_floor(score, FLOOR)
    assert d["beats"] is False
    assert d["hold_floor"] is True
    assert "no_improvement_over_floor" in d["fail"]


def test_beats_floor_false_when_hits_regress():
    score = {
        "hits": 10,
        "low_hr": 0.30,
        "a13_frac": 0.80,
        "n_zero": 5,
        "breach_count": 0,
        "breach": False,
    }
    d = beats_floor(score, FLOOR)
    assert d["beats"] is False
    assert any("hits" in x for x in d["fail"])


def test_year_pack_integrity_if_present():
    """When year pack exists, every row must have n_htf_active>=1 (real path)."""
    if not PACK.exists():
        pytest.skip("year pack not built yet")
    pack = json.loads(PACK.read_text(encoding="utf-8"))
    ex = pack.get("examples") or []
    assert len(ex) > 0
    assert pack.get("require_htf_active") is True or pack.get("law", "").find("htf") >= 0
    for i, row in enumerate(ex):
        assert int(row.get("n_htf_active") or 0) >= 1, f"row {i} missing n_htf_active"
        assert str(row.get("teacher_act")) in ("long", "short")
        assert str(row.get("topology")) in ("pullback_resume", "continuation")
        assert "path_state" in str(row.get("source") or "")
        assert len(row.get("state") or []) == META_RL_DIM
    # Re-filter through shipped gate must keep all
    kept = filter_path_state_teachers(ex, max_examples=len(ex) + 10, require_htf_active=True)
    assert len(kept) == len(ex)
