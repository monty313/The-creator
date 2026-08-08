"""Permanent pin: Law A13 MUST 8–400 trades/day; Monty overrules Judge."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

COURT = Path(__file__).resolve().parents[1]
ROOT = COURT.parent
LAW_MD = COURT / "SCALPING_CADENCE_LAW.md"
LAW_JSON = COURT / "SCALPING_CADENCE_LAW.json"
MASTER = COURT / "MASTER_ARCHITECTURE.md"
GOAL = ROOT / "mark_here" / "knowledge" / "lab" / "GOAL.md"
AGENTS = ROOT / "AGENTS.md"
GROK_RULE = ROOT / ".grok" / "rules" / "00_scalping_cadence.md"


def test_permanent_law_files_exist():
    assert LAW_MD.is_file(), "SCALPING_CADENCE_LAW.md missing"
    assert LAW_JSON.is_file(), "SCALPING_CADENCE_LAW.json missing"
    assert GROK_RULE.is_file(), "00_scalping_cadence.md auto-load rule missing"


def test_machine_pin_a13_must_band():
    data = json.loads(LAW_JSON.read_text(encoding="utf-8"))
    assert data["law_id"] == "A13"
    assert data["status"] == "PERMANENT"
    assert data["immutable"] is True
    assert data["owner_overrules_judge"] is True
    assert data["bot_class"] == "scalper"
    band = data["daily_trade_count"]
    assert band["min_inclusive"] == 8
    assert band["max_inclusive"] == 400
    assert band["modality"] == "MUST"
    assert "must" in band["meaning"].lower()
    assert data["experimental_partial_path"]["production_legal"] is False
    assert "must_8_to_400_trades_per_day" in data["protected_invariants"]
    assert "soften_must_to_may" in data["judge_forbidden"]


def test_law_md_states_must_and_owner_overrule():
    text = LAW_MD.read_text(encoding="utf-8")
    upper = text.upper()
    assert "PERMANENT" in upper
    assert "MUST" in upper
    assert "OVERRULE" in upper or "OVERRULES" in upper
    assert "SCALP" in upper
    assert "8" in text and "400" in text
    assert "A13" in text
    # Soft "may fire" identity language is forbidden for the mandate
    assert "may fire anywhere" not in text.lower()


def test_master_architecture_promotes_a13_must():
    text = MASTER.read_text(encoding="utf-8")
    assert "A13" in text or "Law A13" in text
    assert "400" in text
    assert "scalp" in text.lower()
    assert "MUST" in text.upper() or "must" in text


def test_goal_and_autoload_mention_must_scalping():
    goal = GOAL.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    rule = GROK_RULE.read_text(encoding="utf-8")
    for blob in (goal, agents, rule):
        assert "8" in blob and "400" in blob
        assert "scalp" in blob.lower()
        assert "MUST" in blob.upper() or "must" in blob


def test_goal_path_a13_compliance_helpers():
    from evidence_court.meta_rl.goal_path import (
        SCALPING_TRADES_PER_DAY_MAX,
        SCALPING_TRADES_PER_DAY_MIN,
        a13_trade_count_ok,
        assert_a13_trade_count,
    )

    assert SCALPING_TRADES_PER_DAY_MIN == 8
    assert SCALPING_TRADES_PER_DAY_MAX == 400
    assert a13_trade_count_ok(8) is True
    assert a13_trade_count_ok(400) is True
    assert a13_trade_count_ok(100) is True
    assert a13_trade_count_ok(7) is False
    assert a13_trade_count_ok(0) is False
    assert a13_trade_count_ok(5) is False  # old DEFAULT_SLOTS max
    assert a13_trade_count_ok(401) is False
    assert_a13_trade_count(42)
    with pytest.raises(AssertionError, match="A13"):
        assert_a13_trade_count(3)
    with pytest.raises(AssertionError, match="A13"):
        assert_a13_trade_count(500)
