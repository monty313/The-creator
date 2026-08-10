"""Trade Mental Replay: 3 TF × before/during/after Policy self-observation."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.edge import SetEdge, SymbolEdgeSnapshot
from evidence_court.meta_rl.path_state_harvest import filter_path_state_teachers
from evidence_court.meta_rl.state import META_RL_DIM, build_meta_rl_state
from evidence_court.meta_rl.trade_mental_replay import (
    PHASES,
    TF_ROLES,
    annotate_chart_png,
    build_trade_mental_replay,
    classify_outcome,
    first_person_journal,
    frames_from_set_edge,
    mid_time,
    mental_replay_layout,
    save_mental_replay_pack,
    set_stack,
    teachers_from_mental_replay,
)


def _edge(set_id: int = 1, force: float = 0.4, act: str = "long", topo: str = "continuation") -> SetEdge:
    return SetEdge(
        set_id=set_id,
        name="micro" if set_id == 1 else f"s{set_id}",
        force=force,
        ltf_rsi=55.0 if act == "long" else 45.0,
        topology=topo,
        act=act,
        reason="test",
        htf_agree=True,
    )


def _snap(side: str = "long", force: float = 0.4) -> SymbolEdgeSnapshot:
    edges = [_edge(i, force=force if side == "long" else -force, act=side) for i in range(1, 5)]
    return SymbolEdgeSnapshot(
        symbol="XAUUSD",
        set_edges=edges,
        consensus_force=force if side == "long" else -force,
        best=edges[0],
        multi_set_consensus="agree_long" if side == "long" else "agree_short",
        n_pullback=0,
        n_continuation=4,
    )


def test_set_stack_mark_law():
    assert set_stack(1) == ("1m", "15m", "30m")
    assert set_stack(2) == ("5m", "30m", "1h")
    assert set_stack(3) == ("15m", "1h", "4h")
    assert set_stack(4) == ("30m", "4h", "1d")


def test_mid_time():
    assert mid_time("10:00:00", "10:10:00") == "10:05:00"
    assert mid_time("13:00:00", "13:15:00") == "13:07:30" or mid_time(
        "13:00:00", "13:15:00"
    ).startswith("13:07")


def test_frames_three_tf_roles():
    fr = frames_from_set_edge(_edge(1), 1)
    for role in TF_ROLES:
        assert role in fr
    assert fr["ltf"]["tf"] == "1m"
    assert fr["htf1"]["tf"] == "15m"
    assert fr["htf2"]["tf"] == "30m"
    assert fr["htf1"]["htf_agree"] is True


def test_build_card_has_3x3_and_first_person():
    st = build_meta_rl_state(target_percent=15.0, max_daily_risk_percent=2.0)
    st = st.copy()
    st[0] = 0.8
    before = _snap("long", 0.45)
    during = _snap("long", 0.40)
    after = _snap("long", 0.35)
    card = build_trade_mental_replay(
        trade_index=1,
        symbol="XAUUSD",
        date="2026-01-21",
        side="long",
        size_risk_percent=0.4,
        entry_slot="14:00:00",
        exit_time="14:10:00",
        topology="continuation",
        set_id=1,
        pnl_percent=0.6,
        before_snap=before,
        during_snap=during,
        after_snap=after,
        brain_act="long",
        progress_before=0.1,
        progress_after=0.3,
        packed_state_before=st,
        n_htf_active=2,
    )
    d = card.to_dict(include_state=False)
    for ph in PHASES:
        assert ph in d
        assert "frames" in d[ph]
        for role in TF_ROLES:
            assert role in d[ph]["frames"]
    assert d["grid"] == "3tf_x_3phase"
    assert "I fired long" in card.first_person
    assert "BEFORE:" in card.first_person
    assert "DURING:" in card.first_person
    assert "AFTER:" in card.first_person
    grid = card.grid_summary()
    assert set(grid.keys()) == set(PHASES)


def test_outcome_dead_wait_teacher():
    tag, hint = classify_outcome(
        side="long",
        pnl_percent=-0.3,
        size_risk_percent=0.4,
        before_force=0.4,
        after_force=-0.3,
        after_consensus="conflict",
        progress_after=0.0,
    )
    assert tag in ("dead", "thrash")
    st = build_meta_rl_state(target_percent=15.0, max_daily_risk_percent=2.0)
    card = build_trade_mental_replay(
        trade_index=2,
        symbol="XAUUSD",
        date="2026-01-22",
        side="long",
        size_risk_percent=0.4,
        entry_slot="15:00:00",
        exit_time="15:10:00",
        topology="continuation",
        set_id=1,
        pnl_percent=-0.3,
        before_snap=_snap("long", 0.4),
        during_snap=_snap("long", 0.1),
        after_snap=SymbolEdgeSnapshot(
            symbol="XAUUSD",
            set_edges=[_edge(1, force=-0.3, act="short", topo="collapse")],
            consensus_force=-0.3,
            best=_edge(1, force=-0.3, act="short", topo="collapse"),
            multi_set_consensus="conflict",
            n_pullback=0,
            n_continuation=0,
        ),
        brain_act="long",
        packed_state_before=st,
        n_htf_active=1,
    )
    teachers = teachers_from_mental_replay(card)
    assert teachers, "dead/thrash should emit conversion teacher"
    assert any(t["teacher_act"] == "wait" for t in teachers)
    assert any("mental_replay" in t["source"] for t in teachers)
    # filter accepts mental_replay sources (wait needs allow_wait)
    kept = filter_path_state_teachers(teachers, allow_wait=True, require_htf_active=True)
    assert kept, "filter must keep mental_replay teachers with allow_wait"


def test_clear_fire_teacher_filtered():
    st = build_meta_rl_state(target_percent=15.0, max_daily_risk_percent=2.0)
    st = st.copy()
    st[0] = 0.9
    card = build_trade_mental_replay(
        trade_index=3,
        symbol="XAUUSD",
        date="2026-01-23",
        side="long",
        size_risk_percent=0.5,
        entry_slot="10:00:00",
        exit_time="10:10:00",
        topology="pullback_resume",
        set_id=1,
        pnl_percent=1.2,
        before_snap=_snap("long", 0.5),
        during_snap=_snap("long", 0.5),
        after_snap=_snap("long", 0.55),
        brain_act="long",
        progress_before=0.0,
        progress_after=0.5,
        packed_state_before=st,
        n_htf_active=2,
    )
    teachers = teachers_from_mental_replay(card)
    assert teachers
    assert all(t["teacher_act"] == "long" for t in teachers)
    kept = filter_path_state_teachers(teachers, require_htf_active=True)
    assert kept
    assert all(len(t["state"]) == META_RL_DIM for t in kept)


def test_first_person_journal_shape():
    text = first_person_journal(
        {
            "side": "short",
            "symbol": "EURUSD",
            "topology": "pullback_resume",
            "set_id": 2,
            "set_name": "intraday",
            "pnl_percent": -0.1,
            "outcome_tag": "dead",
            "teacher_hint": "wait_dead",
            "before": {"frames": {"ltf": {"topology": "pullback_resume", "ltf_rsi": 42}, "htf1": {"force": -0.4, "htf_agree": True}}, "multi_set_consensus": "agree_short"},
            "during": {"frames": {"ltf": {"topology": "chop", "ltf_rsi": 50}, "htf1": {"force": -0.2, "htf_agree": True}}, "multi_set_consensus": "incomplete"},
            "after": {"frames": {"ltf": {"topology": "collapse", "ltf_rsi": 60}, "htf1": {"force": 0.3, "htf_agree": False}}, "multi_set_consensus": "conflict"},
        }
    )
    assert "I fired short" in text
    assert "5m/30m/1h" in text or "set2" in text


def test_cv2_annotate_and_save_pack(tmp_path: Path):
    import cv2

    # synthetic chart image
    img = np.zeros((200, 400, 3), dtype=np.uint8)
    img[:] = (40, 40, 40)
    src = tmp_path / "fake_chart.png"
    cv2.imwrite(str(src), img)
    st = build_meta_rl_state(target_percent=15.0, max_daily_risk_percent=2.0)
    card = build_trade_mental_replay(
        trade_index=1,
        symbol="XAUUSD",
        date="2026-01-21",
        side="long",
        size_risk_percent=0.3,
        entry_slot="11:00:00",
        exit_time="11:10:00",
        topology="continuation",
        set_id=1,
        pnl_percent=0.2,
        before_snap=_snap(),
        during_snap=_snap(),
        after_snap=_snap(),
        brain_act="long",
        packed_state_before=st,
        n_htf_active=1,
    )
    out = tmp_path / "annotated.png"
    annotate_chart_png(src, card, out)
    assert out.is_file()
    loaded = cv2.imread(str(out))
    assert loaded is not None
    pack = tmp_path / "pack.json"
    save_mental_replay_pack([card], pack, include_state=False)
    assert pack.is_file()
    text = pack.read_text(encoding="utf-8")
    assert "trade_mental_replay_v1" in text
    assert "3tf_x_3phase" in text


def test_layout_declares_gap_closed():
    lay = mental_replay_layout()
    assert lay["schema"] == "trade_mental_replay_v1"
    gaps = lay["gap_closed"]
    assert "before_during_after_tape" in gaps
    assert "three_tf_per_set" in gaps
    assert "policy_first_person_journal" in gaps
