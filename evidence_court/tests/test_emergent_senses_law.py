"""Pin Law A32 EMERGENT_SENSES_LAW — full sense definitions and fail modes."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAW_MD = ROOT / "EMERGENT_SENSES_LAW.md"
LAW_JSON = ROOT / "EMERGENT_SENSES_LAW.json"
DOCKET = ROOT / "SENSES_CASE_DOCKET.md"


def test_senses_law_files_exist():
    assert LAW_MD.is_file()
    assert LAW_JSON.is_file()
    assert DOCKET.is_file()


def test_senses_json():
    data = json.loads(LAW_JSON.read_text(encoding="utf-8"))
    assert data["law_id"] == "A32"
    assert data["status"] == "PERMANENT"
    assert data["senses"] == ["sight", "feel", "taste", "hearing"]
    assert len(data["official_sets"]) == 4
    assert data["production_rule"] == "senses_pack_into_state_and_train_brain_not_probe_only"
    for key in ("sight", "feel", "taste", "hearing"):
        assert key in data["fail_modes"]
        assert data["axes"][key].startswith("G-")


def test_senses_md_fail_modes():
    text = LAW_MD.read_text(encoding="utf-8")
    assert "bread-and-butter" in text.lower() or "bread and butter" in text.lower()
    assert "lone oscillator" in text.lower()
    assert "marginal" in text.lower()
    assert "thrash" in text.lower()
    assert "slingshot_load" in text
    assert "loaded-not-yet" in text
    assert "CASE-0031" in text
    assert "probe-only" in text.lower() or "probe only" in text.lower()


def test_senses_docket_maps_cases():
    text = DOCKET.read_text(encoding="utf-8")
    for cid in ("CASE-0031", "CASE-0032", "CASE-0033", "CASE-0034"):
        assert cid in text
    assert "G-SIGHT" in text
    assert "G-FEEL" in text
    assert "G-TASTE" in text
    assert "G-HEAR" in text
