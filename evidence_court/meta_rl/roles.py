"""Learn-to-learn: role assignment and topology by function, not indicator names."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np

from .types import SensorRole, TopologyClass


# Canonical decision chain (independent of named sensors)
DECISION_CHAIN = ("tide", "regime", "breath_launch", "act", "finish")

# Functional port templates for common families (topology, not memorized recipes)
FAMILY_ROLE_TEMPLATES: Dict[str, Dict[str, SensorRole]] = {
    "cci": {
        "slow": SensorRole.FORCE,
        "fast": SensorRole.VELOCITY,
        "mid": SensorRole.INERTIA,
    },
    "rsi": {
        "slow": SensorRole.FORCE,
        "fast": SensorRole.VELOCITY,
        "mid": SensorRole.INERTIA,
    },
    "stochastic": {
        "slow": SensorRole.FORCE,
        "fast": SensorRole.VELOCITY,
        "mid": SensorRole.INERTIA,
    },
    "macd": {
        "slow": SensorRole.FORCE,
        "fast": SensorRole.VELOCITY,
        "signal": SensorRole.INERTIA,
    },
    "bb": {
        "mid": SensorRole.EQUILIBRIUM,
        "width": SensorRole.EXPANSION,
        "price": SensorRole.VELOCITY,
    },
    "adx": {
        "adx": SensorRole.REGIME_GATE,
        "plus_di": SensorRole.FORCE,
        "minus_di": SensorRole.FORCE,
    },
    "volume": {
        "vol": SensorRole.VOLUME_CONFIRM,
    },
}


@dataclass(frozen=True)
class SensorSpec:
    name: str
    family: str
    port: str  # slow | fast | mid | ...
    value: float = 0.0  # signed reading in [-1,1] or raw normalized


@dataclass
class RoleMapResult:
    roles: Dict[str, SensorRole]
    topology: TopologyClass
    chain_ok: bool
    act: str  # long | short | wait
    understanding_score: float  # role+topology quality
    act_match_possible: bool


def assign_roles(sensors: Sequence[SensorSpec]) -> Dict[str, SensorRole]:
    """Map each sensor to a functional role by family+port, not absolute name."""
    out: Dict[str, SensorRole] = {}
    for s in sensors:
        fam = s.family.lower().strip()
        port = s.port.lower().strip()
        template = FAMILY_ROLE_TEMPLATES.get(fam, {})
        role = template.get(port, SensorRole.MASKED)
        out[s.name] = role
    return out


def infer_topology(
    roles: Mapping[str, SensorRole],
    sensors: Sequence[SensorSpec],
) -> TopologyClass:
    """Relational topology from role-signed values."""
    by_role: Dict[SensorRole, List[float]] = {}
    for s in sensors:
        r = roles.get(s.name, SensorRole.MASKED)
        by_role.setdefault(r, []).append(float(s.value))

    def mean_role(role: SensorRole) -> float:
        xs = by_role.get(role, [])
        return float(np.mean(xs)) if xs else 0.0

    force = mean_role(SensorRole.FORCE)
    vel = mean_role(SensorRole.VELOCITY)
    inertia = mean_role(SensorRole.INERTIA)
    regime = mean_role(SensorRole.REGIME_GATE)

    if abs(force) < 0.15 and abs(vel) < 0.15:
        return TopologyClass.CHOP
    if force * vel < 0 and abs(force) >= 0.2 and abs(inertia) >= 0.15 and force * inertia > 0:
        return TopologyClass.SLINGSHOT_LOAD
    if force * vel > 0 and abs(force) >= 0.25 and abs(vel) >= 0.25:
        if abs(inertia) >= 0.2 and force * inertia > 0:
            return TopologyClass.LAUNCH
        return TopologyClass.RELEASE
    if force * inertia < 0 and abs(force) >= 0.2:
        return TopologyClass.COLLAPSE
    if abs(regime) < 0.1 and abs(force) < 0.2:
        return TopologyClass.CHOP
    return TopologyClass.RELEASE


def decide_act(topology: TopologyClass, roles: Mapping[str, SensorRole], sensors: Sequence[SensorSpec]) -> str:
    force_vals = [s.value for s in sensors if roles.get(s.name) == SensorRole.FORCE]
    force = float(np.mean(force_vals)) if force_vals else 0.0
    if topology in (TopologyClass.CHOP, TopologyClass.COLLAPSE):
        return "wait"
    if topology == TopologyClass.SLINGSHOT_LOAD:
        return "wait"  # loaded-not-yet
    if topology in (TopologyClass.LAUNCH, TopologyClass.RELEASE):
        if force > 0.15:
            return "long"
        if force < -0.15:
            return "short"
    return "wait"


def evaluate_understanding(
    sensors: Sequence[SensorSpec],
    *,
    expected_topology: Optional[TopologyClass] = None,
    expected_roles: Optional[Mapping[str, SensorRole]] = None,
) -> RoleMapResult:
    roles = assign_roles(sensors)
    topology = infer_topology(roles, sensors)
    act = decide_act(topology, roles, sensors)

    role_score = 1.0
    if expected_roles is not None:
        hits = 0
        total = 0
        for k, v in expected_roles.items():
            total += 1
            if roles.get(k) == v:
                hits += 1
        role_score = hits / max(total, 1)

    topo_score = 1.0
    if expected_topology is not None:
        topo_score = 1.0 if topology == expected_topology else 0.0

    understanding = 0.5 * role_score + 0.5 * topo_score
    chain_ok = all(
        any(r == need for r in roles.values())
        for need in (SensorRole.FORCE, SensorRole.VELOCITY)
    ) or any(r == SensorRole.FORCE for r in roles.values())

    return RoleMapResult(
        roles=roles,
        topology=topology,
        chain_ok=chain_ok,
        act=act,
        understanding_score=float(understanding),
        act_match_possible=True,
    )


def rename_sensors(sensors: Sequence[SensorSpec], prefix: str = "heldout_") -> List[SensorSpec]:
    """Held-out rename: same topology/ports, novel names."""
    return [
        SensorSpec(name=f"{prefix}{s.name}", family=s.family, port=s.port, value=s.value)
        for s in sensors
    ]


def swap_family(sensors: Sequence[SensorSpec], new_family: str) -> List[SensorSpec]:
    """Swap oscillator family keeping ports and values (role transfer test)."""
    return [
        SensorSpec(name=f"{new_family}_{s.port}", family=new_family, port=s.port, value=s.value)
        for s in sensors
    ]


def detect_copying_fail(
    *,
    act_match_rate: float,
    topology_match_rate: float,
    role_match_rate: float,
    act_threshold: float = 0.8,
    chance_threshold: float = 0.35,
) -> bool:
    """High act match with chance-level topology/role → COPYING_FAIL, not learning."""
    return (
        act_match_rate >= act_threshold
        and topology_match_rate <= chance_threshold
        and role_match_rate <= chance_threshold
    )


def novel_composition(
    force_family: str,
    velocity_family: str,
    *,
    force_val: float,
    velocity_val: float,
    inertia_val: float = 0.0,
) -> List[SensorSpec]:
    """Never-seen composition: force from one family, velocity from another."""
    return [
        SensorSpec(name=f"{force_family}_slow", family=force_family, port="slow", value=force_val),
        SensorSpec(
            name=f"{velocity_family}_fast",
            family=velocity_family,
            port="fast",
            value=velocity_val,
        ),
        SensorSpec(
            name=f"{force_family}_mid",
            family=force_family,
            port="mid",
            value=inertia_val,
        ),
    ]
