"""CASE-0015 NEW tests: market ontology (road vocabulary)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.market_ontology import (
    DayOutcome,
    MomentumKind,
    RegimeKind,
    SenseModality,
    StructureEvent,
    TriggerKind,
    classify_day_outcome,
    classify_momentum,
    classify_regime,
    classify_structure_event,
    classify_trigger,
    day_is_pass,
    day_is_win,
    intuition_definition,
    is_pullback,
    is_wait_structure,
    ontology_glossary,
    ontology_self_check,
)


def test_creator_new_win_and_pass_definitions():
    """Creator NEW: winning = target hit; passing = no breach."""
    assert day_is_win(pnl_percent=5.0, target_percent=5.0)
    assert day_is_win(pnl_percent=12.0, target_percent=5.0)
    assert not day_is_win(pnl_percent=4.9, target_percent=5.0)
    assert day_is_pass(breach=False)
    assert not day_is_pass(breach=True)
    assert classify_day_outcome(pnl_percent=6.0, target_percent=5.0, breach=False) == DayOutcome.WIN
    assert classify_day_outcome(pnl_percent=1.0, target_percent=5.0, breach=False) == DayOutcome.MISS
    assert (
        classify_day_outcome(pnl_percent=-2.0, target_percent=5.0, breach=True)
        == DayOutcome.FAIL_BREACH
    )


def test_mark_new_momentum_regime_pullback_trigger():
    """Mark NEW: force=momentum; multi-set=regime; pullback vs load; fire vs wait."""
    assert classify_momentum(0.4) == MomentumKind.BULL
    assert classify_momentum(-0.4) == MomentumKind.BEAR
    assert classify_momentum(0.05) == MomentumKind.FLAT
    assert classify_regime(multi_set_consensus="agree_short") == RegimeKind.BEAR
    assert classify_regime(multi_set_consensus="conflict") == RegimeKind.CONFLICT
    assert is_pullback("pullback_resume")
    assert is_wait_structure("slingshot_load")
    assert (
        classify_trigger(act="short", topology="continuation", htf_agree=True)
        == TriggerKind.FIRE_SHORT
    )
    assert (
        classify_trigger(act="long", topology="slingshot_load", htf_agree=True)
        == TriggerKind.WAIT
    )


def test_creator_new_senses_and_intuition_vocabulary():
    """Creator counter NEW: four senses named; intuition is trained attention not a rule tree."""
    mods = {m.value for m in SenseModality}
    assert mods == {"sight", "feel", "taste", "hearing"}
    text = intuition_definition().lower()
    assert "trained" in text or "meta-policy" in text or "attention" in text
    assert "not a hand-authored" in text or "not a hand" in text


def test_mark_new_structure_event_aliases():
    """Mark counter NEW: policy launch/release map to pullback/continuation events."""
    assert classify_structure_event("launch") == StructureEvent.PULLBACK_RESUME
    assert classify_structure_event("release") == StructureEvent.CONTINUATION
    assert classify_structure_event("pullback_resume") == StructureEvent.PULLBACK_RESUME
    g = ontology_glossary()
    for k in (
        "winning",
        "passing",
        "momentum",
        "regime",
        "trigger",
        "pullback",
        "senses",
        "intuition",
    ):
        assert k in g and len(g[k]) > 10
    assert ontology_self_check()["ok"] is True
