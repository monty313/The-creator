"""Permanent pin: Counsel Law A15 — three opinions; internet sift for best policy."""
from __future__ import annotations

import json
from pathlib import Path

COURT = Path(__file__).resolve().parents[1]
ROOT = COURT.parent
LAW_MD = COURT / "COUNSEL_TO_THE_COURT_LAW.md"
LAW_JSON = COURT / "COUNSEL_TO_THE_COURT_LAW.json"
MASTER = COURT / "MASTER_ARCHITECTURE.md"
AGENTS = ROOT / "AGENTS.md"
GROK_RULE = ROOT / ".grok" / "rules" / "00_counsel.md"
A10_MD = COURT / "ADVERSARIAL_ROUNDS_LAW.md"
PROTOCOL = ROOT / "grok_cli_evidence_court_v2.md"


def test_counsel_law_files_exist():
    assert LAW_MD.is_file()
    assert LAW_JSON.is_file()
    assert GROK_RULE.is_file()


def test_machine_pin_a15():
    data = json.loads(LAW_JSON.read_text(encoding="utf-8"))
    assert data["law_id"] == "A15"
    assert data["status"] == "PERMANENT"
    assert data["immutable"] is True
    assert data["role"]["name"] == "Counsel to the Court"
    assert data["role"]["writes_production_code"] is False
    assert data["role"]["filings_per_case"] == 1
    parties = [p["party"] for p in data["three_opinions_judge_must_weigh"]]
    assert parties == ["Creator", "Mark", "Counsel"]
    assert "counsel_opinion" in data["required_case_fields"]
    for k in (
        "internet_sift",
        "policy_recommendation",
        "opinion",
        "evidence",
        "sources",
    ):
        assert k in data["counsel_opinion_required_keys"]
    assert "promote_without_three_opinion_deliberation" in data["judge_forbidden"]
    assert data["sequence_after_counters"][0] == "counsel_opinion"
    assert data["sequence_after_counters"][-1] == "judge_irac_three_opinions"


def test_law_md_three_opinions_and_internet_sift():
    text = LAW_MD.read_text(encoding="utf-8")
    upper = text.upper()
    assert "PERMANENT" in upper
    assert "COUNSEL" in upper
    assert "INTERNET" in upper
    assert "THREE" in upper or "3" in text
    assert "POLICY" in upper
    assert "JUDGE" in upper
    assert "A15" in text


def test_master_and_autoload():
    master = MASTER.read_text(encoding="utf-8")
    agents = AGENTS.read_text(encoding="utf-8")
    rule = GROK_RULE.read_text(encoding="utf-8")
    a10 = A10_MD.read_text(encoding="utf-8")
    protocol = PROTOCOL.read_text(encoding="utf-8")
    for blob in (master, agents, rule):
        assert "A15" in blob or "Counsel" in blob
        assert "counsel" in blob.lower() or "Counsel" in blob
    assert "Counsel" in a10 or "COUNSEL" in a10 or "A15" in a10
    assert "Counsel" in protocol or "COUNSEL" in protocol or "A15" in protocol


def test_adversarial_rounds_sheet_mentions_counsel():
    sheet = (COURT / "ADVERSARIAL_ROUNDS.md").read_text(encoding="utf-8")
    assert "Counsel" in sheet or "counsel" in sheet
