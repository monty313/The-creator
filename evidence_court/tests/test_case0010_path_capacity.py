"""CASE-0010 NEW tests: path capacity — pullback carve-out + next-slot multi-leg."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.edge import (
    SetEdge,
    SymbolEdgeSnapshot,
    path_side_permission_ok,
    side_permission_ok,
)
from evidence_court.meta_rl.goal_path import DEFAULT_SLOTS, next_slot_end_time


def _edge(
    set_id: int,
    *,
    act: str = "wait",
    force: float = 0.0,
    topology: str = "chop",
    htf_agree: bool = False,
) -> SetEdge:
    return SetEdge(
        set_id=set_id,
        name=f"set{set_id}",
        force=force,
        ltf_rsi=50.0,
        topology=topology,
        act=act,
        reason="fixture",
        htf_agree=htf_agree,
    )


def _snap(edges: list, *, consensus: str = "incomplete", best: SetEdge | None = None):
    b = best
    if b is None:
        actionable = [e for e in edges if e.act in ("long", "short")]
        b = max(actionable, key=lambda e: abs(e.force)) if actionable else None
    return SymbolEdgeSnapshot(
        symbol="TEST",
        set_edges=list(edges),
        consensus_force=float(sum(e.force for e in edges) / max(len(edges), 1)),
        best=b,
        multi_set_consensus=consensus,
        n_pullback=sum(1 for e in edges if e.topology == "pullback_resume"),
        n_continuation=sum(1 for e in edges if e.topology == "continuation"),
    )


def test_creator_new_next_slot_end_time():
    """Creator NEW: each slot ends at next decision slot (multi-leg capacity)."""
    slots = DEFAULT_SLOTS
    assert next_slot_end_time("07:00:00", slots) == "10:00:00"
    assert next_slot_end_time("10:00:00", slots) == "13:00:00"
    assert next_slot_end_time("13:00:00", slots) == "16:00:00"
    assert next_slot_end_time("16:00:00", slots) == "19:00:00"


def test_mark_new_pullback_single_set_carveout():
    """Mark NEW: single-set pullback_resume passes path permission; base gate still fails."""
    one_pb = _snap(
        [
            _edge(1, act="long", force=0.30, topology="pullback_resume", htf_agree=True),
            _edge(2, act="wait", force=0.05, topology="chop", htf_agree=False),
            _edge(3, act="wait", force=0.0, topology="chop", htf_agree=False),
            _edge(4, act="wait", force=0.0, topology="chop", htf_agree=False),
        ],
        consensus="incomplete",
    )
    assert side_permission_ok(one_pb) is False  # CASE-0005 base unchanged
    assert path_side_permission_ok(one_pb) is True  # CASE-0010 carve-out


def test_creator_new_last_slot_ends_eod():
    """Creator counter NEW: last scheduled slot paths to EOD."""
    assert next_slot_end_time("19:00:00", DEFAULT_SLOTS) == "23:59:59"
    assert next_slot_end_time("unknown", DEFAULT_SLOTS) == "23:59:59"


def test_mark_new_continuation_single_set_still_blocked():
    """Mark counter NEW: single-set continuation does not get pullback carve-out."""
    one_ct = _snap(
        [
            _edge(1, act="long", force=0.30, topology="continuation", htf_agree=True),
            _edge(2, act="wait", force=0.05, topology="chop", htf_agree=False),
            _edge(3, act="wait", force=0.0, topology="chop", htf_agree=False),
            _edge(4, act="wait", force=0.0, topology="chop", htf_agree=False),
        ],
        consensus="incomplete",
    )
    assert side_permission_ok(one_ct) is False
    assert path_side_permission_ok(one_ct) is False
