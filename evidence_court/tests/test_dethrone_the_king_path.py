"""Pin: Court-legal dethrone path doc + live king/challenger identities.

Drives real shipped load paths (MetaPolicy.load / DEFAULT_CHAMPION_PATH) and
asserts the analysis SSOT still matches production truth: king is CASE-0037
meta4275; residual lab is distinct and not claimed as production.
"""
from __future__ import annotations

import json
from pathlib import Path

from evidence_court.meta_rl.policy import DEFAULT_CHAMPION_PATH, MetaPolicy

ROOT = Path(__file__).resolve().parents[1]
PATH_DOC = ROOT / "DETHRONE_THE_KING.md"
BEST = ROOT / "BEST_POLICY.md"
DOCKET = ROOT / "ISSUE_DOCKET.md"
L2L_STATUS = ROOT / "L2L_SERIES_STATUS.md"
RES_REPORT = ROOT / "artifacts" / "l2l_p10_residual_report.json"
RES_NPZ = ROOT / "artifacts" / "meta_policy_l2l_p10_residual.npz"

KING_FP_PREFIX = "42:meta4275"
RES_FP_PREFIX = "42:meta10835"


def test_dethrone_path_doc_has_legal_gates_and_forbiddens():
    text = PATH_DOC.read_text(encoding="utf-8")
    # PROMOTE-only replace language
    assert "PROMOTE" in text
    assert "silent overwrite" in text.lower() or "Silent overwrite" in text
    # Floor numbers (or re-floor clause — both required by plan)
    assert "11" in text and "0.28" in text and "0.64" in text
    assert "n_zero" in text.lower() or "n_zero" in text
    assert "re-floor" in text.lower() or "re-floors" in text.lower()
    # Forbidden list
    assert "F-024" in text
    assert "F-025" in text
    assert "process-washout" in text.lower() or "Process-washout" in text
    assert "inference retrain" in text.lower() or "Inference retrain" in text
    # King + residual lab not production
    assert "CASE-0037" in text
    assert "meta4275" in text
    assert "not production" in text.lower()
    # Dual SSOT resolution
    assert "forward100" in text or "Floor dual" in text
    assert "north-star" in text.lower() or "North-star" in text
    # Ranked next
    assert "L2L-P10" in text
    assert "C-004" in text
    # Honest non-claim
    assert "final boss" in text.lower() or "§7" in text or "final_gate" in text


def test_live_king_is_still_meta4275_not_residual():
    """Ship path: champion load must still be CASE-0037 fingerprint class."""
    assert Path(DEFAULT_CHAMPION_PATH).exists()
    king = MetaPolicy.load(DEFAULT_CHAMPION_PATH, freeze=True, require_serious=False)
    kfp = king.weight_fingerprint()
    assert kfp.startswith(KING_FP_PREFIX), kfp
    assert RES_NPZ.exists()
    res = MetaPolicy.load(RES_NPZ, freeze=True, require_serious=False)
    rfp = res.weight_fingerprint()
    assert rfp.startswith(RES_FP_PREFIX), rfp
    assert kfp != rfp


def test_ssot_files_do_not_claim_production_replaced_or_final_gate():
    best = BEST.read_text(encoding="utf-8")
    assert "CASE-0037" in best
    assert "meta4275" in best
    assert "meta_policy_l2l_p10_residual" in best
    assert "not production" in best.lower()

    l2l = L2L_STATUS.read_text(encoding="utf-8")
    assert "Final §7 gate:** **false**" in l2l or "final_gate" in l2l.lower()
    assert "still CASE-0037" in l2l or "Production champion:** still CASE-0037" in l2l

    docket = DOCKET.read_text(encoding="utf-8")
    assert "goal_achieved:** **false**" in docket
    assert "L2L-P10" in docket
    assert "C-004" in docket
    # rank-1 is still the residual density / every-day problem
    assert "rank-1" in docket.lower() or "| 1 |" in docket

    rep = json.loads(RES_REPORT.read_text(encoding="utf-8"))
    # residual report must not claim production replace
    assert rep.get("production_replace") is not True
    assert rep.get("production_champion_replaced") is not True
    gate = rep.get("final_promote_gate") or {}
    assert gate.get("ready") is not True


def test_dethrone_path_floor_clause_matches_best_policy_numbers():
    """Cross-check: path doc floor table numbers match BEST_POLICY floor table."""
    best = BEST.read_text(encoding="utf-8")
    # BEST_POLICY floor block
    assert "**11**" in best
    assert "**0.28**" in best
    assert "**0.64**" in best
    assert "**18**" in best
    path = PATH_DOC.read_text(encoding="utf-8")
    assert "≥ 11" in path or "hits ≥ 11" in path or "hits≥11" in path
    assert "0.64" in path
    assert "0.28" in path
