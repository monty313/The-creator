"""Permanent pin: A30 full-project checklist schedule (Creator then Mark)."""
from __future__ import annotations

import json
from pathlib import Path

COURT = Path(__file__).resolve().parents[1]
ROOT = COURT.parent
LAW_MD = COURT / "FULL_PROJECT_CHECKLIST_LAW.md"
LAW_JSON = COURT / "FULL_PROJECT_CHECKLIST_LAW.json"
SCHED = COURT / "schedules"
CREATOR = SCHED / "CREATOR_GOAL_CHECKLIST.md"
MARK = SCHED / "MARK_GOAL_CHECKLIST.md"
MASTER_SCHED = SCHED / "SCHEDULE.md"
AGENTS = ROOT / "AGENTS.md"


def test_files_exist():
    assert LAW_MD.is_file()
    assert LAW_JSON.is_file()
    assert CREATOR.is_file()
    assert MARK.is_file()
    assert MASTER_SCHED.is_file()
    assert (SCHED / "CHECKLIST_ITEM_TEMPLATE.md").is_file()


def test_machine_pin_a30():
    data = json.loads(LAW_JSON.read_text(encoding="utf-8"))
    assert data["law_id"] == "A30"
    assert data["status"] == "PERMANENT"
    assert len(data["phases"]) == 2
    assert data["phases"][0]["owner"] == "Creator"
    assert data["phases"][1]["owner"] == "Mark"
    assert data["phases"][1]["starts_when"] == "phase_1_complete"
    assert "skip_court_on_checklist_item" in data["forbidden"]
    assert "start_mark_phase_before_creator_complete" in data["forbidden"]


def test_creator_checklist_has_items_and_court_rule():
    text = CREATOR.read_text(encoding="utf-8")
    assert "C-001" in text
    assert "C-012" in text
    assert "PENDING_COURT" in text
    assert "Court" in text or "A10" in text
    assert "GOAL" in text or "goal" in text.lower()


def test_mark_phase_blocked_until_creator_done():
    text = MARK.read_text(encoding="utf-8")
    assert "BLOCKED" in text
    assert "KAG" in text or "kag" in text.lower()
    assert "Phase 1" in text or "phase 1" in text.lower() or "Phase 1" in text


def test_schedule_phase_order():
    text = MASTER_SCHED.read_text(encoding="utf-8")
    assert "Creator" in text
    assert "Mark" in text
    assert "IN PROGRESS" in text or "IN_PROGRESS" in text
    assert "BLOCKED" in text


def test_agents_mentions_a30_or_checklist_schedule():
    a = AGENTS.read_text(encoding="utf-8")
    assert "A30" in a or "checklist" in a.lower() or "CREATOR_GOAL_CHECKLIST" in a
