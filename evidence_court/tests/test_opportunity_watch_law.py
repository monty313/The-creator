"""Permanent pin: Opportunity Watch Agent A28 + senses docket."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

COURT = Path(__file__).resolve().parents[1]
ROOT = COURT.parent
LAW_MD = COURT / "OPPORTUNITY_WATCH_LAW.md"
LAW_JSON = COURT / "OPPORTUNITY_WATCH_LAW.json"
DOCKET = COURT / "SENSES_CASE_DOCKET.md"
AGENTS = ROOT / "AGENTS.md"
GROK = ROOT / ".grok" / "rules" / "00_opportunity_watch.md"
MASTER = COURT / "MASTER_ARCHITECTURE.md"


def test_law_files_exist():
    assert LAW_MD.is_file()
    assert LAW_JSON.is_file()
    assert DOCKET.is_file()
    assert GROK.is_file()


def test_machine_pin_a28():
    data = json.loads(LAW_JSON.read_text(encoding="utf-8"))
    assert data["law_id"] == "A28"
    assert data["status"] == "PERMANENT"
    assert data["agent"]["always_on"] is True
    assert data["agent"]["writes_production_trades"] is False
    assert "pullback_resume" in data["opportunity"]["topologies"]
    assert "continuation" in data["opportunity"]["topologies"]
    assert data["opportunity"]["prime_session"] == "london_ny"
    assert data["complaints"]["multiple_per_case"] is True
    cases = [x["case"] for x in data["senses_docket"]]
    assert cases == ["CASE-0031", "CASE-0032", "CASE-0033", "CASE-0034"]
    senses = [x["sense"] for x in data["senses_docket"]]
    assert senses == ["sight", "feel", "taste", "hearing"]


def test_docs_mention_london_ny_and_rsi_bb():
    text = LAW_MD.read_text(encoding="utf-8") + DOCKET.read_text(encoding="utf-8")
    assert "London" in text or "LONDON" in text.upper() or "london" in text.lower()
    assert "RSI" in text or "rsi" in text.lower()
    assert "pullback" in text.lower()
    assert "continuation" in text.lower()
    assert "complaint" in text.lower()
    assert "0031" in text


def test_autoload_and_master():
    assert "A28" in AGENTS.read_text(encoding="utf-8") or "Opportunity" in AGENTS.read_text(
        encoding="utf-8"
    )
    assert "opportunity" in GROK.read_text(encoding="utf-8").lower()
    assert "A28" in MASTER.read_text(encoding="utf-8") or "Opportunity Watch" in MASTER.read_text(
        encoding="utf-8"
    )


def test_london_ny_session_band():
    from evidence_court.meta_rl.opportunity_watch import (
        is_london_ny_session,
        session_band,
    )

    assert is_london_ny_session("10:00:00") is True
    assert is_london_ny_session("13:00:00") is True
    assert is_london_ny_session("16:30:00") is True
    assert is_london_ny_session("06:00:00") is False
    assert is_london_ny_session("19:00:00") is False
    assert session_band("12:00:00") == "london_ny"
    assert session_band("20:00:00") == "other"


def test_classify_and_complaint_fields():
    from evidence_court.meta_rl.edge import SetEdge
    from evidence_court.meta_rl.opportunity_watch import (
        OpportunityWatchAgent,
        edge_is_opportunity,
        classify_bot_response,
    )
    from evidence_court.meta_rl.edge import SymbolEdgeSnapshot

    e = SetEdge(
        set_id=1,
        name="1m/15m/30m",
        force=0.4,
        ltf_rsi=55.0,
        topology="pullback_resume",
        act="long",
        reason="test",
        htf_agree=True,
    )
    assert edge_is_opportunity(e) is True
    assert classify_bot_response(opportunity_side="long", bot_act="wait", bot_fired=False) == "wait"
    assert classify_bot_response(opportunity_side="long", bot_act="long", bot_fired=True) == "taken"
    assert (
        classify_bot_response(opportunity_side="long", bot_act="short", bot_fired=True)
        == "wrong_side"
    )

    snap = SymbolEdgeSnapshot(
        symbol="XAUUSD",
        set_edges=[e],
        consensus_force=0.4,
        best=e,
        multi_set_consensus="agree_long",
        n_pullback=1,
        n_continuation=0,
    )
    ag = OpportunityWatchAgent()
    # Miss: bot wait
    rep = ag.scan_snapshot(
        snap,
        asof_date="2026-03-01",
        asof_time="13:00:00",
        bot_act="wait",
        bot_fired=False,
    )
    assert rep.n_opportunities == 1
    assert rep.n_misses == 1
    assert rep.n_london_ny_misses == 1
    assert len(rep.complaints) == 1
    c = rep.complaints[0]
    assert c.topology == "pullback_resume"
    assert c.side == "long"
    assert c.session_band == "london_ny"
    assert c.how_to_sense_next
    assert c.sense_gap

    # Hit: bot took long
    rep2 = ag.scan_snapshot(
        snap,
        asof_date="2026-03-01",
        asof_time="13:00:00",
        bot_act="long",
        bot_fired=True,
        bot_symbol="XAUUSD",
    )
    assert rep2.n_misses == 0
    assert rep2.n_hits == 1


def test_multiple_complaints_one_scan():
    from evidence_court.meta_rl.edge import SetEdge, SymbolEdgeSnapshot
    from evidence_court.meta_rl.opportunity_watch import OpportunityWatchAgent

    edges = [
        SetEdge(1, "s1", 0.5, 50.0, "pullback_resume", "long", "r", True),
        SetEdge(2, "s2", 0.45, 52.0, "continuation", "long", "r", True),
        SetEdge(3, "s3", 0.1, 50.0, "chop", "wait", "r", False),
    ]
    snap = SymbolEdgeSnapshot(
        symbol="EURUSD",
        set_edges=edges,
        consensus_force=0.4,
        best=edges[0],
        multi_set_consensus="agree_long",
        n_pullback=1,
        n_continuation=1,
    )
    rep = OpportunityWatchAgent().scan_snapshot(
        snap, asof_date="2026-01-01", asof_time="10:00:00", bot_act="wait", bot_fired=False
    )
    assert rep.n_opportunities == 2
    assert rep.n_misses == 2
    assert len(rep.complaints) == 2  # multi-complaint OK
