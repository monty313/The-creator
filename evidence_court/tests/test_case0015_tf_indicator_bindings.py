"""CASE-0015 Court amendment: every term bound to indicator groups + Mark TFs."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.market_ontology import (
    GROUP_HTF_FORCE,
    GROUP_LTF_TIMING,
    assert_term_bound_to_sets_and_indicators,
    official_set_stacks,
    term_definitions,
)
from evidence_court.meta_rl.sets import assert_mark_sets_law


def test_creator_new_mark_sets_law_stacks_pinned():
    """Creator NEW: ontology uses exact MARK_SETS_LAW stacks (4 sets)."""
    assert_mark_sets_law()
    stacks = official_set_stacks()
    assert stacks == (
        ("1m", "15m", "30m"),
        ("5m", "30m", "1h"),
        ("15m", "1h", "4h"),
        ("30m", "4h", "1d"),
    )
    # Each structure term lists all 4 sets
    for term in ("momentum", "pullback", "continuation", "trigger", "regime"):
        d = assert_term_bound_to_sets_and_indicators(term)
        set_ids = {b.set_id for b in d.timeframe_bindings if b.set_id > 0}
        assert set_ids == {1, 2, 3, 4}, f"{term} missing sets: {set_ids}"


def test_mark_new_momentum_htf_indicators_and_tfs():
    """Mark NEW: momentum = HTF confirmation TFs only + trend_dir group."""
    d = assert_term_bound_to_sets_and_indicators("momentum")
    assert d.indicator_group.group_id == "htf_force"
    names = {i.name for i in d.indicator_group.indicators}
    assert "trend_dir" in names
    for b in d.timeframe_bindings:
        assert b.uses_htf is True
        assert b.uses_ltf is False
        # LTF field still records set entry TF for set identity; HTF are confirm
        assert b.htf[0] in ("15m", "30m", "1h", "4h")
        assert b.htf[1] in ("30m", "1h", "4h", "1d")


def test_mark_new_pullback_ltf_rsi_bb_on_each_set():
    """Mark NEW: pullback timing = RSI5 + BB10 dev0.5 shift+2 on each set's LTF."""
    d = assert_term_bound_to_sets_and_indicators("pullback")
    assert d.indicator_group.group_id == GROUP_LTF_TIMING.group_id
    by_name = {i.name: dict(i.params) for i in d.indicator_group.indicators}
    assert by_name["rsi"]["period"] == 5
    assert by_name["bollinger"]["period"] == 10
    assert by_name["bollinger"]["dev"] == 0.5
    assert by_name["bollinger"]["shift"] == 2
    ltfs = {b.ltf for b in d.timeframe_bindings}
    assert ltfs == {"1m", "5m", "15m", "30m"}
    for b in d.timeframe_bindings:
        assert b.uses_ltf is True
        assert b.uses_htf is True  # force from HTF + timing LTF


def test_creator_new_trigger_and_win_pass_indicator_groups():
    """Creator counter NEW: trigger uses force+structure group; win/pass scoreboard-only."""
    tr = assert_term_bound_to_sets_and_indicators("trigger")
    assert tr.indicator_group.group_id == "trigger_permission"
    assert {i.name for i in tr.indicator_group.indicators} >= {
        "htf_agree",
        "structure_event",
        "multi_set_consensus",
    }
    win = assert_term_bound_to_sets_and_indicators("winning")
    pas = assert_term_bound_to_sets_and_indicators("passing")
    assert win.scoreboard_only and pas.scoreboard_only
    assert win.indicator_group.group_id == "day_scoreboard"
    assert "target_percent" in {i.name for i in win.indicator_group.indicators}
    assert "breach_flag" in {i.name for i in pas.indicator_group.indicators}


def test_mark_new_senses_intuition_bound_to_all_sets():
    """Mark counter NEW: senses + intuition bound to all Mark sets + state indicators."""
    for term in ("senses", "intuition", "regime", "continuation", "slingshot_load"):
        d = assert_term_bound_to_sets_and_indicators(term)
        assert len(d.indicator_group.indicators) >= 2
        if not d.scoreboard_only:
            assert {b.set_id for b in d.timeframe_bindings if b.set_id > 0} == {1, 2, 3, 4}


def test_creator_new_htf_force_group_matches_edge_recipe():
    """Creator: HTF force group documents dual lookback + multi-day (Court edge)."""
    names = {i.name: dict(i.params) for i in GROUP_HTF_FORCE.indicators}
    assert names["trend_dir"]["lookback"] == 5
    assert names["trend_dir_medium"]["lookback"] == 10
    assert names["multi_day_momentum"]["n_days"] == 3
