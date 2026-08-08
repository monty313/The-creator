"""Sense probes: sight / feel / taste / hearing call shipped predicates."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.senses import MarketSenseInput, probe_all_senses, probe_feel, probe_hearing, probe_sight, probe_taste


def _load_building() -> MarketSenseInput:
    return MarketSenseInput(
        htf_force=[0.8, 0.7, 0.75, 0.7, 0.6, 0.65, 0.5, 0.55],
        ltf_velocity=[-0.5, -0.4, -0.45, -0.3],
        inertia=[0.7, 0.65, 0.6, 0.55],
        inertia_baseline=[0.4, 0.4, 0.4, 0.4],
        velocity_baseline=[0.1, 0.1, 0.1, 0.1],
        full_body_outside_rails=True,
        ltf_inside_tight=True,
        efficiency=0.6,
        regime="bull",
        g_fixed=True,
        composition_has_force=True,
        composition_has_velocity=True,
        cross_family_agree=True,
        target_percent=50.0,
        max_daily_risk_percent=2.0,
        progress_to_target=0.1,
    )


def test_sight_topology_and_consensus():
    s = probe_sight(_load_building())
    assert s["topology_class"] == "slingshot_load"
    assert s["multi_set_consensus"] in ("agree_long", "agree_short", "conflict", "incomplete")
    assert s["multi_set_consensus"] == "agree_long"
    assert "with" in s["ltf_velocity_phase"] or "against" in s["ltf_velocity_phase"]
    assert s["tunnel_membership"] in ("full_body_outside", "inside")


def test_feel_max_tension():
    f = probe_feel(_load_building())
    assert f["max_tension_load_building"] is True
    assert f["efficiency_regime"] in ("nothing", "tradable", "great_movement")
    assert f["clocks"]["inertia_with"] is True
    assert f["clocks"]["velocity_against"] is True


def test_taste_edge_and_goal_distance():
    t = probe_taste(_load_building())
    assert t["composition_valid"] is True
    assert t["edge_quality"] in ("bread_and_butter", "marginal", "noise")
    assert 0.0 <= t["goal_distance"] <= 1.0
    assert 0.0 <= t["risk_remaining_frac"] <= 1.0


def test_taste_patience_on_high_target_marginal():
    inp = MarketSenseInput(
        htf_force=[0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.0, 0.0],
        ltf_velocity=[0.2, 0.1, 0.0, 0.0],
        inertia=[0.2, 0.2, 0.1, 0.1],
        inertia_baseline=[0.0] * 4,
        velocity_baseline=[0.0] * 4,
        efficiency=0.3,
        composition_has_force=True,
        composition_has_velocity=True,
        cross_family_agree=False,
        set_conflict=False,
        target_percent=80.0,
        max_daily_risk_percent=1.5,
        progress_to_target=0.2,
    )
    t = probe_taste(inp)
    # marginal + high target → patience preferred path exercises taste skill
    assert t["composition_valid"] is True


def test_hearing_wait_subtypes():
    h = probe_hearing(_load_building())
    assert h["wait_subtype"] in ("loaded_not_yet", "no_trade", "kill", "")
    assert h["wait_reason"]
    assert h["dual_clock"] in ("co_alignment", "divergence", "quiet")
    assert "regime" in h


def test_probe_all_senses():
    rep = probe_all_senses(_load_building())
    assert "topology_class" in rep.sight
    assert "max_tension_load_building" in rep.feel
    assert "edge_quality" in rep.taste
    assert "wait_subtype" in rep.hearing
