"""Learn-to-learn gates: rename/swap/novel + COPYING_FAIL detection on shipped units."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.roles import (
    SensorSpec,
    assign_roles,
    detect_copying_fail,
    evaluate_understanding,
    infer_topology,
    novel_composition,
    rename_sensors,
    swap_family,
)
from evidence_court.meta_rl.types import SensorRole, TopologyClass


def _launch_cci():
    return [
        SensorSpec("cci_slow", "cci", "slow", 0.8),
        SensorSpec("cci_fast", "cci", "fast", 0.7),
        SensorSpec("cci_mid", "cci", "mid", 0.6),
    ]


def test_rename_preserves_topology_and_roles():
    base = _launch_cci()
    r0 = evaluate_understanding(base)
    renamed = rename_sensors(base, prefix="HO_")
    r1 = evaluate_understanding(renamed)
    assert r0.topology == r1.topology
    assert r0.act == r1.act
    # roles by port/family not by name
    roles0 = list(r0.roles.values())
    roles1 = list(r1.roles.values())
    assert sorted(x.value for x in roles0) == sorted(x.value for x in roles1)


def test_swap_family_rsi_same_topology():
    base = _launch_cci()
    r0 = evaluate_understanding(base)
    swapped = swap_family(base, "rsi")
    r1 = evaluate_understanding(swapped)
    assert r0.topology == r1.topology
    assert r0.act == r1.act
    assert all(v in (SensorRole.FORCE, SensorRole.VELOCITY, SensorRole.INERTIA) for v in r1.roles.values())


def test_novel_composition_role_ports():
    sensors = novel_composition("macd", "stochastic", force_val=0.75, velocity_val=0.7, inertia_val=0.55)
    r = evaluate_understanding(sensors)
    assert SensorRole.FORCE in r.roles.values()
    assert SensorRole.VELOCITY in r.roles.values()
    assert r.act in ("long", "short", "wait")
    assert r.chain_ok


def test_slingshot_load_wait():
    sensors = [
        SensorSpec("cci_slow", "cci", "slow", 0.7),
        SensorSpec("cci_fast", "cci", "fast", -0.5),
        SensorSpec("cci_mid", "cci", "mid", 0.6),
    ]
    r = evaluate_understanding(sensors, expected_topology=TopologyClass.SLINGSHOT_LOAD)
    assert r.topology == TopologyClass.SLINGSHOT_LOAD
    assert r.act == "wait"


def test_copying_fail_detection():
    assert detect_copying_fail(
        act_match_rate=0.95,
        topology_match_rate=0.2,
        role_match_rate=0.25,
    )
    assert not detect_copying_fail(
        act_match_rate=0.95,
        topology_match_rate=0.9,
        role_match_rate=0.85,
    )


def test_chronological_forward_style_act_consistency():
    """Same topology features on 'new day' → same role understanding (no retrain)."""
    day_a = _launch_cci()
    day_b = [
        SensorSpec("cci_slow", "cci", "slow", 0.82),
        SensorSpec("cci_fast", "cci", "fast", 0.71),
        SensorSpec("cci_mid", "cci", "mid", 0.58),
    ]
    ra = evaluate_understanding(day_a)
    rb = evaluate_understanding(day_b)
    assert ra.topology == rb.topology
    assert ra.act == rb.act
