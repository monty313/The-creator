"""CASE-0016 NEW tests: regime catalog — who defines what, and does classify work."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.regimes import (
    RegimeId,
    catalog_self_check,
    classify_regime_court,
    creator_internet_regime_names,
    mark_physics_regime_names,
    regime_allows_fire,
    regime_catalog,
    regime_kill_new_risk,
)
from evidence_court.meta_rl.sets import assert_mark_sets_law


def test_creator_new_internet_regime_catalog_coverage():
    """Creator NEW: internet-class regimes are named and covered by hybrid catalog."""
    names = set(creator_internet_regime_names())
    # Classic literature set
    for need in (
        "trend_bull",
        "trend_bear",
        "range_chop",
        "vol_expansion",
        "vol_compression",
        "transition",
    ):
        assert need in names
    hybrid = {r.value for r in RegimeId}
    assert names <= hybrid


def test_mark_new_physics_regime_catalog_and_tfs():
    """Mark NEW: physics catalog includes conflict/incomplete; every regime on 4 Mark sets."""
    names = set(mark_physics_regime_names())
    for need in ("trend_bull", "trend_bear", "conflict", "incomplete", "range_chop"):
        assert need in names
    assert_mark_sets_law()
    cat = regime_catalog()
    for rid, spec in cat.items():
        assert len(spec.timeframe_bindings) == 4
        assert {b.set_id for b in spec.timeframe_bindings} == {1, 2, 3, 4}
        # HTF always used for regime force
        assert all(b.uses_htf for b in spec.timeframe_bindings)
        assert len(spec.indicator_group.indicators) >= 2
        # stacks match Mark law
        for b in spec.timeframe_bindings:
            if b.set_id == 1:
                assert b.htf == ("15m", "30m")
            if b.set_id == 4:
                assert b.htf == ("4h", "1d")


def test_creator_new_classifier_discriminates_regimes():
    """Creator counter NEW: classifier separates conflict / trend / vol / transition."""
    assert classify_regime_court(multi_set_consensus="conflict") == RegimeId.CONFLICT
    assert (
        classify_regime_court(multi_set_consensus="agree_long", force=0.5, efficiency=0.55)
        == RegimeId.TREND_BULL
    )
    assert (
        classify_regime_court(multi_set_consensus="agree_short", force=-0.5, efficiency=0.55)
        == RegimeId.TREND_BEAR
    )
    assert (
        classify_regime_court(multi_set_consensus="agree_long", force=0.6, efficiency=0.9)
        == RegimeId.VOL_EXPANSION
    )
    assert (
        classify_regime_court(multi_set_consensus="incomplete", force=0.35, efficiency=0.5)
        == RegimeId.TRANSITION
    )
    assert (
        classify_regime_court(multi_set_consensus="incomplete", force=0.0, efficiency=0.5)
        == RegimeId.INCOMPLETE
    )
    assert (
        classify_regime_court(multi_set_consensus="chop", force=0.0, efficiency=0.1)
        == RegimeId.VOL_COMPRESSION
    )


def test_mark_new_fire_kill_playbook_by_regime():
    """Mark counter NEW: conflict/compression kill; trend allows fire road-sign."""
    assert regime_kill_new_risk(RegimeId.CONFLICT)
    assert regime_kill_new_risk(RegimeId.VOL_COMPRESSION)
    assert not regime_kill_new_risk(RegimeId.TREND_BULL)
    assert regime_allows_fire(RegimeId.TREND_BULL)
    assert regime_allows_fire(RegimeId.TREND_BEAR)
    assert not regime_allows_fire(RegimeId.CONFLICT)
    assert not regime_allows_fire(RegimeId.RANGE_CHOP)
    assert catalog_self_check()["ok"] is True
