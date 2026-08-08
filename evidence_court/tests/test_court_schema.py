"""Court artifact schema + sets law pins."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
COURT = ROOT / "evidence_court"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.sets import assert_mark_sets_law, mark_sets_law_table


REQUIRED_CASE_KEYS = [
    "case_id",
    "status",
    "question",
    "scope",
    "protected_invariants",
    "creator_submission",
    "mark_submission",
    "critic_cross_examination",
    "optimist_challenge",
    "judge_pretrial_order",
    "execution_record",
    "judge_IRAC_verdict",
]


def test_mark_sets_law_pin():
    assert_mark_sets_law()
    table = mark_sets_law_table()
    assert len(table) == 4
    assert table[0]["stack"] == ["1m", "15m", "30m"]
    assert table[1]["stack"] == ["5m", "30m", "1h"]
    assert table[2]["stack"] == ["15m", "1h", "4h"]
    assert table[3]["stack"] == ["30m", "4h", "1d"]


def test_case_0001_schema_present():
    path = COURT / "cases" / "CASE-0001-meta-rl-state.json"
    assert path.exists(), "CASE-0001 json missing"
    data = json.loads(path.read_text(encoding="utf-8"))
    for k in REQUIRED_CASE_KEYS:
        assert k in data, f"missing schema key {k}"
    assert data["case_id"] == "CASE-0001"
    q = data["question"].lower()
    assert "target" in q and "risk" in q
    assert "learn" in q or "l2l" in q or "transfer" in q
    assert "sense" in q
    assert data["status"] in (
        "PROPOSED",
        "INCONCLUSIVE",
        "ADMITTED",
        "REJECTED",
        "PROMOTED",
    )


def test_inventory_exists():
    assert (COURT / "INVENTORY.md").exists()
