"""Pins: learn-phase arbitration + any_better helper + Teacher channel."""
from __future__ import annotations

from pathlib import Path

from evidence_court.meta_rl.policy import DEFAULT_CHAMPION_PATH, MetaPolicy
from evidence_court.meta_rl.train_learn_phase_20d import is_any_better, is_past_full_window

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "ARBITRATION_LEARN_PHASE.md"


def test_arbitration_personae_teacher_counsel_only():
    text = DOC.read_text(encoding="utf-8")
    assert "The Policy" in text or "### The Policy" in text
    for seat in ("Creator", "Mark", "Counsel", "Critic", "Optimist", "Judge"):
        assert seat in text
    assert "Teacher" in text
    assert "Counsel only" in text or "Counsel_only" in text or "only address Counsel" in text.lower() or "Counsel only" in text
    assert "learn" in text.lower() and "copy" in text.lower()
    assert "20" in text  # 20d phase
    assert "F-024" in text and "F-025" in text
    assert "meta4275" in text or "CASE-0037" in text


def test_is_any_better_requires_clean_and_metric():
    base = {"hits": 2, "a13_frac": 0.3, "n_zero": 8, "breach_count": 0, "weights_frozen": True}
    # worse
    assert is_any_better(
        {"hits": 1, "a13_frac": 0.2, "n_zero": 9, "breach_count": 0, "weights_frozen": True},
        base,
    )[0] is False
    # hits better
    ok, reasons = is_any_better(
        {"hits": 3, "a13_frac": 0.3, "n_zero": 8, "breach_count": 0, "weights_frozen": True},
        base,
    )
    assert ok is True
    assert any("hits" in r for r in reasons)
    # breach blocks
    assert is_any_better(
        {"hits": 9, "a13_frac": 0.9, "n_zero": 0, "breach_count": 1, "weights_frozen": True},
        base,
    )[0] is False
    # n_zero better
    ok2, r2 = is_any_better(
        {"hits": 2, "a13_frac": 0.3, "n_zero": 5, "breach_count": 0, "weights_frozen": True},
        base,
    )
    assert ok2 and any("n_zero" in x for x in r2)


def test_past_full_window_requires_hits_and_density():
    base = {"hits": 2, "a13_frac": 0.25, "n_zero": 5, "breach_count": 0, "weights_frozen": True}
    # a13 only — NOT past full window
    ok, reasons = is_past_full_window(
        {"hits": 2, "a13_frac": 0.35, "n_zero": 5, "breach_count": 0, "weights_frozen": True},
        base,
    )
    assert ok is False
    assert any("hits" in r for r in reasons)
    # hits up but a13 washout — fail
    ok2, _ = is_past_full_window(
        {"hits": 3, "a13_frac": 0.10, "n_zero": 5, "breach_count": 0, "weights_frozen": True},
        base,
    )
    assert ok2 is False
    # full past
    ok3, r3 = is_past_full_window(
        {"hits": 3, "a13_frac": 0.30, "n_zero": 4, "breach_count": 0, "weights_frozen": True},
        base,
    )
    assert ok3 is True
    assert any("hits" in x for x in r3)


def test_king_still_meta4275():
    fp = MetaPolicy.load(
        DEFAULT_CHAMPION_PATH, freeze=True, require_serious=False
    ).weight_fingerprint()
    assert fp.startswith("42:meta4275"), fp
