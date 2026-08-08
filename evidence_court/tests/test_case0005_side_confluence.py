"""CASE-0005 NEW tests: multi-set side confluence gate (A10 openings + counters)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.edge import (
    SetEdge,
    SymbolEdgeSnapshot,
    count_actionable_side_agree,
    side_permission_ok,
)


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


def _snap(
    edges: list,
    *,
    consensus: str = "incomplete",
    best: SetEdge | None = None,
) -> SymbolEdgeSnapshot:
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


def test_creator_new_side_permission_requires_two_sets():
    """Creator NEW: single actionable set fails; two same-side sets pass."""
    one = _snap(
        [
            _edge(1, act="long", force=0.30, topology="pullback_resume", htf_agree=True),
            _edge(2, act="wait", force=0.05, topology="chop", htf_agree=False),
            _edge(3, act="wait", force=0.0, topology="chop", htf_agree=False),
            _edge(4, act="wait", force=0.0, topology="chop", htf_agree=False),
        ],
        consensus="incomplete",
    )
    assert side_permission_ok(one) is False

    two = _snap(
        [
            _edge(1, act="long", force=0.30, topology="pullback_resume", htf_agree=True),
            _edge(2, act="long", force=0.28, topology="continuation", htf_agree=True),
            _edge(3, act="wait", force=0.0, topology="chop", htf_agree=False),
            _edge(4, act="wait", force=0.0, topology="chop", htf_agree=False),
        ],
        consensus="incomplete",
    )
    assert side_permission_ok(two) is True


def test_mark_new_count_actionable_side_agree():
    """Mark NEW: count only htf_agree + actionable topology matching act."""
    edges = [
        _edge(1, act="long", force=0.4, topology="pullback_resume", htf_agree=True),
        _edge(2, act="long", force=0.3, topology="continuation", htf_agree=True),
        _edge(3, act="long", force=0.2, topology="chop", htf_agree=True),  # not actionable topo
        _edge(4, act="short", force=-0.3, topology="continuation", htf_agree=True),
        _edge(5, act="long", force=0.25, topology="pullback_resume", htf_agree=False),
    ]
    snap = _snap(edges, consensus="conflict")
    assert count_actionable_side_agree(snap, "long") == 2
    assert count_actionable_side_agree(snap, "short") == 1
    assert count_actionable_side_agree(snap, "wait") == 0


def test_creator_new_consensus_strong_force_carveout():
    """Creator NEW (counter): full consensus + strong force may pass with n=1."""
    strong = _snap(
        [
            _edge(1, act="long", force=0.45, topology="pullback_resume", htf_agree=True),
            _edge(2, act="wait", force=0.42, topology="chop", htf_agree=True),
            _edge(3, act="wait", force=0.41, topology="chop", htf_agree=True),
            _edge(4, act="wait", force=0.40, topology="chop", htf_agree=True),
        ],
        consensus="agree_long",
    )
    assert count_actionable_side_agree(strong, "long") == 1
    assert side_permission_ok(strong) is True

    # same n=1 but incomplete consensus → no carve-out
    incomplete = _snap(
        [
            _edge(1, act="long", force=0.45, topology="pullback_resume", htf_agree=True),
            _edge(2, act="wait", force=0.05, topology="chop", htf_agree=False),
            _edge(3, act="wait", force=0.0, topology="chop", htf_agree=False),
            _edge(4, act="wait", force=0.0, topology="chop", htf_agree=False),
        ],
        consensus="incomplete",
    )
    assert side_permission_ok(incomplete) is False


def test_mark_new_weak_single_set_blocked():
    """Mark NEW (counter): weak single-set never gets permission."""
    weak = _snap(
        [
            _edge(1, act="short", force=-0.25, topology="continuation", htf_agree=True),
            _edge(2, act="wait", force=-0.05, topology="chop", htf_agree=False),
            _edge(3, act="wait", force=0.0, topology="chop", htf_agree=False),
            _edge(4, act="wait", force=0.0, topology="chop", htf_agree=False),
        ],
        consensus="incomplete",
    )
    assert count_actionable_side_agree(weak, "short") == 1
    assert abs(weak.best.force) < 0.40
    assert side_permission_ok(weak) is False
