"""Permanent pin: Adversarial Rounds Law A10 cannot silently disappear or weaken."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

COURT = Path(__file__).resolve().parents[1]
ROOT = COURT.parent
LAW_MD = COURT / "ADVERSARIAL_ROUNDS_LAW.md"
LAW_JSON = COURT / "ADVERSARIAL_ROUNDS_LAW.json"
MASTER = COURT / "MASTER_ARCHITECTURE.md"
PROTOCOL = ROOT / "grok_cli_evidence_court_v2.md"
AGENTS = ROOT / "AGENTS.md"
GROK_RULE = ROOT / ".grok" / "rules" / "00_adversarial_rounds.md"

LEGACY_EXEMPT = {"CASE-0001", "CASE-0002", "CASE-FORWARD-100"}

REQUIRED_OPENING_KEYS_CREATOR = {
    "strongest_internet_argument",
    "claim",
    "new_test",
}
REQUIRED_OPENING_KEYS_MARK = {
    "strongest_knowledge_argument",
    "claim",
    "new_test",
}
REQUIRED_COUNTER_KEYS = {"used"}  # used | waived handled in value checks


def test_permanent_law_files_exist():
    assert LAW_MD.is_file(), "ADVERSARIAL_ROUNDS_LAW.md missing — permanent law"
    assert LAW_JSON.is_file(), "ADVERSARIAL_ROUNDS_LAW.json missing — machine pin"
    assert (COURT / "ADVERSARIAL_ROUNDS.md").is_file()


def test_machine_pin_immutable_a10():
    data = json.loads(LAW_JSON.read_text(encoding="utf-8"))
    assert data["law_id"] == "A10"
    assert data["status"] == "PERMANENT"
    assert data["immutable"] is True
    assert data["counter"]["max_per_side"] == 1
    assert data["counter"]["second_counter"] == "STRIKE"
    assert data["opening"]["creator"]["source"] == "internet"
    assert data["opening"]["creator"]["proof"] == "new_test"
    assert data["opening"]["mark"]["source"] == "knowledge"
    assert data["opening"]["mark"]["proof"] == "new_test"
    for field in data["required_case_fields"]:
        assert field in {
            "creator_opening",
            "mark_opening",
            "creator_counter",
            "mark_counter",
            "counsel_opinion",  # A15 permanent
        }
    assert "counsel_opinion" in data["required_case_fields"]
    assert data.get("three_opinions") == ["Creator", "Mark", "Counsel"]


def test_law_md_states_permanent_and_one_counter():
    text = LAW_MD.read_text(encoding="utf-8").upper()
    assert "PERMANENT" in text
    assert "INTERNET" in text
    assert "KNOWLEDGE" in text
    assert "NEW TEST" in text or "NEW TESTS" in text
    assert "ONE COUNTER" in text or "EXACTLY ONE" in text or "MAX 1" in text or "MAX_PER_SIDE" in text or "ONE**" in LAW_MD.read_text(encoding="utf-8")
    assert "STRIKE" in text or "NO SECOND" in text


def test_master_architecture_promotes_a10():
    text = MASTER.read_text(encoding="utf-8")
    assert "Law A10" in text or "**Law A10" in text
    assert "ADVERSARIAL" in text.upper() or "Adversarial" in text
    assert "PERMANENT" in text.upper() or "permanent" in text


def test_protocol_and_autoload_mention_adversarial_rounds():
    assert PROTOCOL.is_file()
    p = PROTOCOL.read_text(encoding="utf-8")
    assert "strongest argument from the internet" in p.lower() or "strongest argument from the **internet**" in p
    assert "strongest argument from his knowledge" in p.lower() or "strongest argument from **his knowledge**" in p
    assert "one counter" in p.lower() or "exactly one" in p.lower()
    assert AGENTS.is_file(), "root AGENTS.md must auto-load permanent Court law"
    a = AGENTS.read_text(encoding="utf-8")
    assert "A10" in a or "ADVERSARIAL" in a.upper()
    assert GROK_RULE.is_file(), ".grok/rules/00_adversarial_rounds.md must exist for auto-load"
    g = GROK_RULE.read_text(encoding="utf-8")
    assert "PERMANENT" in g.upper()
    assert "internet" in g.lower()
    assert "knowledge" in g.lower()


def test_new_case_json_must_use_adversarial_fields():
    """Cases opened after A10 must carry permanent schema; legacy PROMOTED exempt."""
    cases_dir = COURT / "cases"
    if not cases_dir.is_dir():
        pytest.skip("no cases dir")
    law = json.loads(LAW_JSON.read_text(encoding="utf-8"))
    required = set(law["required_case_fields"])
    for path in sorted(cases_dir.glob("CASE-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        cid = str(data.get("case_id", path.stem.split("-")[0] + "-" + path.stem.split("-")[1] if "-" in path.stem else path.stem))
        # Normalize: CASE-0001-meta-rl-state.json → CASE-0001
        stem = path.stem
        if stem.startswith("CASE-FORWARD"):
            short = "CASE-FORWARD-100"
        else:
            parts = stem.split("-")
            short = "-".join(parts[:2]) if len(parts) >= 2 else stem
        if short in LEGACY_EXEMPT or data.get("status") == "PROMOTED" and short in LEGACY_EXEMPT:
            continue
        # Any non-legacy case (PROPOSED or later additions) must have permanent fields
        if short in LEGACY_EXEMPT:
            continue
        # Only enforce on files that claim post-A10 procedure or are newly numbered > 0002
        if short in ("CASE-0001", "CASE-0002", "CASE-FORWARD-100"):
            continue
        missing = required - set(data.keys())
        assert not missing, f"{path.name} missing permanent adversarial fields: {missing}"
        co = data["creator_opening"]
        mo = data["mark_opening"]
        for k in REQUIRED_OPENING_KEYS_CREATOR:
            assert k in co, f"{path.name} creator_opening missing {k}"
        for k in REQUIRED_OPENING_KEYS_MARK:
            assert k in mo, f"{path.name} mark_opening missing {k}"
        for side in ("creator_counter", "mark_counter"):
            assert "used" in data[side] or data[side].get("used") is not None or "waived" in str(data[side]).lower()


def test_second_counter_is_forbidden_in_law_json():
    data = json.loads(LAW_JSON.read_text(encoding="utf-8"))
    assert data["counter"]["max_per_side"] == 1
