"""Structural pin: Court trials audit exists and states honest completeness gaps."""
from __future__ import annotations

import json
import re
from pathlib import Path

from evidence_court.meta_rl.policy import DEFAULT_CHAMPION_PATH, MetaPolicy

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "COURT_TRIALS_AUDIT.md"
DOCKET = ROOT / "ISSUE_DOCKET.md"
CHECKLIST = ROOT / "schedules" / "CREATOR_GOAL_CHECKLIST.md"
CASES = ROOT / "cases"
SCAN = ROOT / "artifacts" / "_court_trials_scan.json"


def test_audit_artifact_has_required_sections():
    text = AUDIT.read_text(encoding="utf-8")
    assert "Inventory" in text or "inventory" in text.lower()
    assert "Completed Full Court" in text or "FULL_A10_A15" in text
    assert "Incomplete" in text or "not through" in text.lower()
    assert "SSOT cross-check" in text or "SSOT" in text
    assert "CASE-0037" in text
    assert "meta4275" in text
    # must not claim all C rows terminal
    assert "PENDING_COURT" in text
    assert "C-001" in text and "C-012" in text
    assert "L2L" in text
    # honest headline
    assert "No" in text or "NO" in text
    assert "goal_achieved" in text.lower() or "goal_achieved" in text


def test_audit_does_not_claim_all_checklist_closed():
    text = AUDIT.read_text(encoding="utf-8")
    cl = CHECKLIST.read_text(encoding="utf-8")
    # checklist still has PENDING
    assert "PENDING_COURT" in cl
    # audit must acknowledge incomplete
    assert "PENDING_COURT" in text
    assert "Phase 1" in text or "not terminal" in text.lower() or "false" in text.lower()


def test_scan_covers_all_case_md_files():
    md_files = sorted(p.name for p in CASES.glob("CASE*.md"))
    assert len(md_files) >= 30
    if SCAN.exists():
        rows = json.loads(SCAN.read_text(encoding="utf-8"))
        scanned = {r["file"] for r in rows}
        for name in md_files:
            assert name in scanned, f"scan missing {name}"


def test_spot_check_closed_full_and_thin_and_missing():
    """≥3 named cases: closed FULL, thin measure, missing 0032."""
    p37 = (CASES / "CASE-0037-path-state-teachers.md").read_text(encoding="utf-8")
    assert re.search(r"status:.*CLOSED", p37, re.I)
    assert "IRAC" in p37 or "Judge" in p37
    assert "Counsel" in p37 or "A15" in p37

    p22 = (CASES / "CASE-0022-a21-measure.md").read_text(encoding="utf-8")
    assert re.search(r"status:.*CLOSED", p22, re.I)
    assert "REJECT" in p22.upper()

    assert not (CASES / "CASE-0032-feel.md").exists()
    # docket still queues 0032
    docket = DOCKET.read_text(encoding="utf-8")
    assert "CASE-0032" in docket
    assert "QUEUED" in docket or "queued" in docket.lower()


def test_production_champion_still_meta4275():
    pol = MetaPolicy.load(DEFAULT_CHAMPION_PATH, freeze=True, require_serious=False)
    fp = pol.weight_fingerprint()
    assert fp.startswith("42:meta4275"), fp
    audit = AUDIT.read_text(encoding="utf-8")
    assert "meta4275" in audit


def test_docket_goal_false_and_rank1_open():
    d = DOCKET.read_text(encoding="utf-8")
    assert "goal_achieved:** **false**" in d or "goal_achieved:** false" in d
    assert "L2L-P10" in d
    assert "C-004" in d
