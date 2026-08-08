"""Minimal perception types (portable; mirrors lab adaptive_rl_brain types)."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Direction(int, Enum):
    BEAR = -1
    NEUTRAL = 0
    BULL = 1


class VelocityStrength(str, Enum):
    NONE = "none"
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"


class TopologyClass(str, Enum):
    SLINGSHOT_LOAD = "slingshot_load"
    RELEASE = "release"
    LAUNCH = "launch"
    COLLAPSE = "collapse"
    CHOP = "chop"


class SensorRole(str, Enum):
    FORCE = "force"
    INERTIA = "inertia"
    VELOCITY = "velocity"
    EQUILIBRIUM = "equilibrium"
    REGIME_GATE = "regime_gate"
    EXPANSION = "expansion"
    VOLUME_CONFIRM = "volume_confirm"
    MASKED = "masked"


@dataclass(frozen=True)
class OfficialSet:
    set_id: int
    name: str
    entry_tf: str
    confirmation_tfs: Tuple[str, str]

    @property
    def tfs(self) -> Tuple[str, str, str]:
        return (self.entry_tf, self.confirmation_tfs[0], self.confirmation_tfs[1])


@dataclass(frozen=True)
class SubSet:
    sub_id: str
    entry_tf: str
    confirmation_tf: str

    @property
    def tfs(self) -> Tuple[str, str]:
        return (self.entry_tf, self.confirmation_tf)


@dataclass(frozen=True)
class SetConfluence:
    set_key: str
    direction: Direction
    velocity: VelocityStrength
    votes: Tuple = ()
    n_bull: int = 0
    n_bear: int = 0
    n_neutral: int = 3


@dataclass(frozen=True)
class StructureFlags:
    pullback: bool = False
    scale_conflict: bool = False
