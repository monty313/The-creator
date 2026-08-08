"""Pin Law A31 GOAL_LAW — mission axes and permanence."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAW_MD = ROOT / "GOAL_LAW.md"
LAW_JSON = ROOT / "GOAL_LAW.json"

REQUIRED_AXES = {
    "G-NO_RETRAIN",
    "G-BREACH0",
    "G-CLEAR",
    "G-A13",
    "G-L2L",
    "G-SIGHT",
    "G-FEEL",
    "G-TASTE",
    "G-HEAR",
    "G-TRAIN",
    "G-LONG",
    "G-ONEBOT",
}


def test_goal_law_files_exist():
    assert LAW_MD.is_file(), "GOAL_LAW.md missing"
    assert LAW_JSON.is_file(), "GOAL_LAW.json missing"


def test_goal_law_json_schema():
    data = json.loads(LAW_JSON.read_text(encoding="utf-8"))
    assert data["law_id"] == "A31"
    assert data["status"] == "PERMANENT"
    axes = set(data["goal_axes"])
    assert REQUIRED_AXES <= axes
    fb = data["final_boss"]
    assert fb["breach"] == 0
    assert fb["no_retrain"] is True
    assert fb["a13_trades_per_day"] == [8, 400]
    assert fb["senses_drive_brain"] is True


def test_goal_law_md_mentions_mission_and_senses():
    text = LAW_MD.read_text(encoding="utf-8")
    assert "without having to retrain" in text.lower() or "no retrain" in text.lower()
    assert "8" in text and "400" in text
    for sense in ("sight", "feel", "taste", "hearing"):
        assert sense in text.lower()
    assert "PERMANENT" in text
    assert "G-SIGHT" in text


def test_issue_docket_has_goal_axes():
    docket = (ROOT / "ISSUE_DOCKET.md").read_text(encoding="utf-8")
    assert "goal_axes" in docket
    assert "G-CLEAR" in docket
    assert "C-001" in docket
    assert "goal_achieved" in docket.lower() or "goal_achieved" in docket
