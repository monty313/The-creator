"""Pin Law A33 GOAL_RELATIVE_COURT_LAW — continuous process + retention paths."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAW_MD = ROOT / "GOAL_RELATIVE_COURT_LAW.md"
LAW_JSON = ROOT / "GOAL_RELATIVE_COURT_LAW.json"
LEDGER = ROOT / "ledger" / "EVIDENCE_LEDGER.jsonl"
SCORE = ROOT / "ledger" / "SCOREBOARD_HISTORY.jsonl"
COUNSEL = ROOT / "ledger" / "COUNSEL_CACHE.jsonl"


def test_a33_files_exist():
    assert LAW_MD.is_file()
    assert LAW_JSON.is_file()
    assert LEDGER.is_file()
    assert SCORE.is_file()
    assert COUNSEL.is_file()


def test_a33_json():
    data = json.loads(LAW_JSON.read_text(encoding="utf-8"))
    assert data["law_id"] == "A33"
    assert data["status"] == "PERMANENT"
    assert "full_court" in data["tiers"]
    assert "summary_court" in data["tiers"]
    paths = data["retention_paths"]
    assert "ledger" in paths and "scoreboard" in paths
    for f in data["required_issue_fields"]:
        assert f in ("issue_id", "goal_axes", "blocks_metric", "severity", "status")


def test_ledger_is_jsonl_with_goal_axes():
    lines = [ln for ln in LEDGER.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) >= 3
    for ln in lines:
        obj = json.loads(ln)
        assert "event_id" in obj
        assert "goal_axes" in obj
        assert "kind" in obj


def test_scoreboard_history_has_floor_row():
    rows = [json.loads(ln) for ln in SCORE.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert any(r.get("case_id") == "CASE-0029" for r in rows)
    last = rows[-1]
    assert last.get("breach") == 0


def test_process_md_requires_continuous_loop():
    text = LAW_MD.read_text(encoding="utf-8")
    assert "generate" in text.lower()
    assert "goal" in text.lower()
    assert "Full Court" in text or "full court" in text.lower()
    assert "Summary Court" in text or "summary court" in text.lower()
    assert "EVIDENCE_LEDGER" in text


def test_checkpoint_points_at_c001():
    cp = (ROOT / "CONTINUATION_CHECKPOINT.md").read_text(encoding="utf-8")
    assert "C-001" in cp
    assert "CASE-0031" in cp
    assert "A31" in cp and "A32" in cp and "A33" in cp
