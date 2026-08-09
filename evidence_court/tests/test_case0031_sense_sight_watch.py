"""CASE-0031 NEW tests: Sight + Opportunity Watch (A10 openings + counters).

Also C-001 path wire: Watch runs inside run_goal_path_day every decision.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.edge import SetEdge, SymbolEdgeSnapshot
from evidence_court.meta_rl.goal_path import run_goal_path_day
from evidence_court.meta_rl.opportunity_watch import (
    OpportunityWatchAgent,
    curriculum_labels_from_report,
    edge_is_opportunity,
)
from evidence_court.meta_rl.policy import FrozenMetaPolicy


def test_creator_new_watch_flags_miss_on_wait():
    """Creator NEW: wait on PB opportunity → miss complaint (sight)."""
    e = SetEdge(1, "set1", 0.4, 48.0, "pullback_resume", "long", "htf_ltf", True)
    snap = SymbolEdgeSnapshot("XAUUSD", [e], 0.4, e, "agree_long", 1, 0)
    rep = OpportunityWatchAgent().scan_snapshot(
        snap, asof_date="2026-02-01", asof_time="14:00:00", bot_act="wait", bot_fired=False
    )
    assert rep.n_misses >= 1
    assert any("sense" in c.how_to_sense_next.lower() or "Sense" in c.how_to_sense_next for c in rep.complaints)
    assert rep.n_london_ny_misses >= 1


def test_mark_new_multi_set_multi_complaint():
    """Mark NEW: two sets PB+cont same clock → two complaints when flat."""
    edges = [
        SetEdge(1, "a", 0.5, 50.0, "pullback_resume", "long", "r", True),
        SetEdge(2, "b", 0.4, 55.0, "continuation", "long", "r", True),
    ]
    snap = SymbolEdgeSnapshot("EURUSD", edges, 0.45, edges[0], "agree_long", 1, 1)
    rep = OpportunityWatchAgent().scan_snapshot(
        snap, asof_date="2026-02-01", asof_time="10:00:00", bot_act="wait", bot_fired=False
    )
    assert rep.n_opportunities == 2
    assert len(rep.complaints) == 2


def test_creator_new_no_opportunity_without_htf_agree():
    """Creator counter NEW: no HTF agree → not an opportunity (no pad)."""
    e = SetEdge(1, "set1", 0.5, 50.0, "continuation", "long", "r", False)
    assert edge_is_opportunity(e) is False
    snap = SymbolEdgeSnapshot("XAUUSD", [e], 0.2, e, "incomplete", 0, 0)
    rep = OpportunityWatchAgent().scan_snapshot(
        snap, asof_date="2026-02-01", asof_time="13:00:00", bot_act="wait", bot_fired=False
    )
    assert rep.n_opportunities == 0
    assert rep.n_misses == 0


def test_mark_new_taken_is_hit_not_complaint():
    """Mark counter NEW: matching fire → hit, zero miss complaints."""
    e = SetEdge(1, "set1", 0.4, 50.0, "continuation", "short", "r", True)
    snap = SymbolEdgeSnapshot("GBPUSD", [e], -0.4, e, "agree_short", 0, 1)
    rep = OpportunityWatchAgent().scan_snapshot(
        snap,
        asof_date="2026-02-01",
        asof_time="15:00:00",
        bot_act="short",
        bot_fired=True,
        bot_symbol="GBPUSD",
    )
    assert rep.n_hits == 1
    assert rep.n_misses == 0
    assert rep.complaints == []


def test_c001_curriculum_labels_weight_london_ny():
    """C-001: miss labels feed offline curriculum; London/NY higher weight."""
    e = SetEdge(1, "set1", 0.4, 48.0, "pullback_resume", "long", "r", True)
    snap = SymbolEdgeSnapshot("XAUUSD", [e], 0.4, e, "agree_long", 1, 0)
    london = OpportunityWatchAgent().scan_snapshot(
        snap, asof_date="2026-02-01", asof_time="14:00:00", bot_act="wait", bot_fired=False
    )
    other = OpportunityWatchAgent().scan_snapshot(
        snap, asof_date="2026-02-01", asof_time="03:00:00", bot_act="wait", bot_fired=False
    )
    lab_l = curriculum_labels_from_report(london)
    lab_o = curriculum_labels_from_report(other)
    assert lab_l and lab_l[0]["teacher_act"] == "long"
    assert lab_l[0]["weight"] > lab_o[0]["weight"]
    assert lab_l[0]["session_band"] == "london_ny"


def test_c001_goal_path_watch_meta_always_on():
    """C-001 wire: run_goal_path_day always emits watch meta + labels; no force."""
    rows = []
    px = 2000.0
    for d in range(1, 12):
        date = f"2026-06-{d:02d}"
        for m in range(0, 24 * 60, 15):
            h, mi = divmod(m, 60)
            t = f"{h:02d}:{mi:02d}:00"
            o = px
            c = px * 1.00012
            rows.append(
                {
                    "date": date,
                    "time": t,
                    "open": o,
                    "high": max(o, c) * 1.0003,
                    "low": min(o, c) * 0.9997,
                    "close": c,
                }
            )
            px = c
    date = sorted(set(b["date"] for b in rows))[-2]
    policy = FrozenMetaPolicy.from_seed(7)
    fp = policy.weight_fingerprint()
    # Sparse slots so path is fast; watch still runs every slot
    slots = ("10:00:00", "11:00:00", "13:00:00", "14:00:00", "16:00:00")
    fills, ledger, meta = run_goal_path_day(
        policy,
        date=date,
        m1_by_symbol={"XAUUSD": rows},
        target_percent=5.0,
        max_daily_risk_percent=3.0,
        symbols=["XAUUSD"],
        slots=slots,
        watch_enabled=True,
    )
    policy.assert_frozen()
    assert policy.weight_fingerprint() == fp
    assert meta.get("watch_enabled") is True
    assert "watch" in meta
    assert meta["watch"]["always_on"] is True
    assert "n_misses" in meta["watch"]
    assert "curriculum_labels" in meta
    assert isinstance(meta["curriculum_labels"], list)
    # Watch must not itself pad fills (no force)
    assert meta["n_fills"] == len(fills)
    loss = max(-ledger.realized_pnl_percent, 0.0)
    assert loss <= 3.0 + 1e-6


def test_c001_watch_disabled_opt_out_lab_only():
    """Lab opt-out: watch_enabled=False yields empty curriculum labels."""
    rows = []
    px = 100.0
    for d in range(1, 6):
        date = f"2026-07-{d:02d}"
        for m in range(0, 24 * 60, 30):
            h, mi = divmod(m, 60)
            rows.append(
                {
                    "date": date,
                    "time": f"{h:02d}:{mi:02d}:00",
                    "open": px,
                    "high": px * 1.001,
                    "low": px * 0.999,
                    "close": px * 1.0001,
                }
            )
            px *= 1.0001
    date = sorted(set(b["date"] for b in rows))[-2]
    policy = FrozenMetaPolicy.from_seed(3)
    _, _, meta = run_goal_path_day(
        policy,
        date=date,
        m1_by_symbol={"EURUSD": rows},
        target_percent=3.0,
        max_daily_risk_percent=2.0,
        symbols=["EURUSD"],
        slots=("10:00:00", "13:00:00"),
        watch_enabled=False,
    )
    assert meta.get("watch_enabled") is False
    assert meta.get("curriculum_labels") == []
    assert meta["watch"].get("always_on") is False
