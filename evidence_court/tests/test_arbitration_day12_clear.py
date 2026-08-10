"""Structural pin: personified day-12 arbitration exists and locks legal path."""
from __future__ import annotations

from pathlib import Path

from evidence_court.meta_rl.policy import DEFAULT_CHAMPION_PATH, MetaPolicy

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "ARBITRATION_DAY12_CLEAR.md"


def test_day12_arbitration_personae_and_facts():
    text = DOC.read_text(encoding="utf-8")
    # Policy voice + Court seats
    assert "The Policy" in text or "### The Policy" in text
    for seat in ("Creator", "Mark", "Counsel", "Critic", "Optimist", "Judge"):
        assert seat in text
    # Day 12 facts
    assert "2026-01-21" in text
    assert "15" in text and "3" in text
    assert "2.9" in text or "2.94" in text or "~2.9" in text
    assert "hit" in text.lower()
    # Illegal + legal path
    assert "lot" in text.lower()
    assert "breach" in text.lower()
    assert "DAY-12 CLEAR ROAD" in text or "get past day 12" in text.lower() or "legal" in text.lower()
    assert "conversion" in text.lower()
    assert "F-024" in text and "F-025" in text
    # No false production replace claim as done
    assert "meta4275" in text or "CASE-0037" in text
    assert "does not replace" in text.lower() or "still CASE-0037" in text or "unchanged" in text.lower()


def test_king_still_meta4275_after_day12_arbitration():
    fp = MetaPolicy.load(
        DEFAULT_CHAMPION_PATH, freeze=True, require_serious=False
    ).weight_fingerprint()
    assert fp.startswith("42:meta4275"), fp
