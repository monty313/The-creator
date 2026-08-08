"""CASE-0031 NEW tests: Sight + Opportunity Watch (A10 openings + counters)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.edge import SetEdge, SymbolEdgeSnapshot
from evidence_court.meta_rl.opportunity_watch import (
    OpportunityWatchAgent,
    edge_is_opportunity,
)


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
