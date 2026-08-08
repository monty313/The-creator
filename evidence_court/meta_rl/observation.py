"""Mark Channel1 + full 168-dim packing (portable, layout-compatible with mark_here)."""
from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Sequence

import numpy as np

from .sets import OFFICIAL_SETS, SUB_SETS
from .types import Direction, SetConfluence, StructureFlags, VelocityStrength

N_OFFICIAL = 4
N_SUB = 5
FEATURES_PER_SET = 3
CHANNEL1_DIM = 32
N_SIGNAL_SLOTS = 92
DOCTRINE_DIM = 16
MAJORITY_DIM = 12
SELF_DIM = 16
MARK_FULL_DIM = CHANNEL1_DIM + DOCTRINE_DIM + MAJORITY_DIM + N_SIGNAL_SLOTS + SELF_DIM
assert MARK_FULL_DIM == 168

_VEL_SCORE = {
    VelocityStrength.NONE: 0.0,
    VelocityStrength.WEAK: 1.0 / 3.0,
    VelocityStrength.MEDIUM: 2.0 / 3.0,
    VelocityStrength.STRONG: 1.0,
}


def velocity_to_float(v: VelocityStrength) -> float:
    return float(_VEL_SCORE.get(VelocityStrength(v), 0.0))


def direction_to_float(d: Direction) -> float:
    return float(int(Direction(d)))


def confluence_score(c: SetConfluence) -> float:
    n = max(int(c.n_bull + c.n_bear + c.n_neutral), 1)
    return float(c.n_bull - c.n_bear) / float(n)


def _pack_set(c: Optional[SetConfluence]) -> tuple[float, float, float]:
    if c is None:
        return 0.0, 0.0, 0.0
    return (
        direction_to_float(c.direction),
        velocity_to_float(c.velocity),
        confluence_score(c),
    )


def empty_confluence(set_key: str) -> SetConfluence:
    return SetConfluence(
        set_key=set_key,
        direction=Direction.NEUTRAL,
        velocity=VelocityStrength.NONE,
        votes=(),
        n_bull=0,
        n_bear=0,
        n_neutral=3,
    )


def build_channel1_obs(
    official: Mapping[int, SetConfluence] | None = None,
    subs: Mapping[str, SetConfluence] | None = None,
    structure: StructureFlags | None = None,
    *,
    progress_to_goal: float = 0.0,
    danger: float = 0.0,
    session_phase: float = 0.0,
) -> np.ndarray:
    off = dict(official or {})
    sub = {str(k).upper(): v for k, v in (subs or {}).items()}
    struct = structure or StructureFlags()
    out = np.zeros(CHANNEL1_DIM, dtype=np.float32)
    for i, s in enumerate(OFFICIAL_SETS):
        d, v, sc = _pack_set(off.get(s.set_id))
        base = i * FEATURES_PER_SET
        out[base] = d
        out[base + 1] = v
        out[base + 2] = sc
    sub_base = N_OFFICIAL * FEATURES_PER_SET
    for j, s in enumerate(SUB_SETS):
        d, v, sc = _pack_set(sub.get(s.sub_id))
        base = sub_base + j * FEATURES_PER_SET
        out[base] = d
        out[base + 1] = v
        out[base + 2] = sc
    out[27] = 1.0 if struct.pullback else 0.0
    out[28] = 1.0 if struct.scale_conflict else 0.0
    out[29] = float(progress_to_goal)
    out[30] = float(danger)
    out[31] = float(session_phase)
    return out


def pack_self_state_mark_legacy(
    *,
    side: float = 0.0,
    n_open_units: float = 0.0,
    n_entries: float = 0.0,
    n_adds: float = 0.0,
    progress: float = 0.0,
    danger: float = 0.0,
    target_pct: float = 2.0,
    risk_pct: float = 3.0,
    equity_pct: float = 0.0,
    room_to_floor: float = 0.0,
    remaining_to_target: float = 0.0,
    mark_soul: float = 1.0,
    soul_flips: float = 0.0,
    session_phase: float = 0.0,
    in_trade: float = 0.0,
) -> np.ndarray:
    """Original Mark self_state encoding (saturates target at ~5%). Preserved for compatibility."""
    out = np.zeros(SELF_DIM, dtype=np.float32)
    out[0] = float(np.clip(side, -1.0, 1.0))
    out[1] = float(np.clip(n_open_units / 8.0, 0.0, 1.0))
    out[2] = float(np.clip(n_entries / 12.0, 0.0, 1.0))
    out[3] = float(np.clip(n_adds / 4.0, 0.0, 1.0))
    out[4] = float(np.clip(progress, -1.0, 1.0))
    out[5] = float(np.clip(danger, 0.0, 1.0))
    out[6] = float(np.clip(target_pct / 5.0, 0.0, 1.0))
    out[7] = float(np.clip(risk_pct / 5.0, 0.0, 1.0))
    hardness = target_pct / max(risk_pct, 1e-6)
    out[8] = float(np.clip(hardness, 0.0, 2.0) / 2.0)
    out[9] = float(np.clip(equity_pct / 5.0, -1.0, 1.0))
    out[10] = float(np.clip(room_to_floor / max(risk_pct, 1e-6), 0.0, 2.0) / 2.0)
    out[11] = float(np.clip(remaining_to_target / max(target_pct, 1e-6), -1.0, 2.0) / 2.0)
    out[12] = float(mark_soul)
    out[13] = float(np.clip(soul_flips / 4.0, 0.0, 1.0))
    out[14] = float(np.clip(session_phase, 0.0, 1.0))
    out[15] = float(in_trade)
    return out


def pack_agent_votes(votes: Optional[Sequence[float] | np.ndarray]) -> np.ndarray:
    out = np.zeros(N_SIGNAL_SLOTS, dtype=np.float32)
    if votes is None:
        return out
    v = np.asarray(votes, dtype=np.float32).reshape(-1)
    n = min(int(v.size), N_SIGNAL_SLOTS)
    if n > 0:
        out[:n] = np.clip(v[:n], -1.0, 1.0)
    return out


def build_mark_full_obs(
    channel1: np.ndarray,
    *,
    doctrine_vec: Optional[np.ndarray] = None,
    majority_vec: Optional[np.ndarray] = None,
    agent_votes: Optional[Sequence[float] | np.ndarray] = None,
    self_vec: Optional[np.ndarray] = None,
) -> np.ndarray:
    c1 = np.asarray(channel1, dtype=np.float32).reshape(-1)
    if c1.size != CHANNEL1_DIM:
        tmp = np.zeros(CHANNEL1_DIM, dtype=np.float32)
        n = min(CHANNEL1_DIM, int(c1.size))
        tmp[:n] = c1[:n]
        c1 = tmp
    d = doctrine_vec if doctrine_vec is not None else np.zeros(DOCTRINE_DIM, np.float32)
    m = majority_vec if majority_vec is not None else np.zeros(MAJORITY_DIM, np.float32)
    a = pack_agent_votes(agent_votes)
    s = self_vec if self_vec is not None else np.zeros(SELF_DIM, np.float32)
    d = np.asarray(d, dtype=np.float32).reshape(-1)[:DOCTRINE_DIM]
    m = np.asarray(m, dtype=np.float32).reshape(-1)[:MAJORITY_DIM]
    s = np.asarray(s, dtype=np.float32).reshape(-1)[:SELF_DIM]
    if d.size < DOCTRINE_DIM:
        d = np.pad(d, (0, DOCTRINE_DIM - d.size))
    if m.size < MAJORITY_DIM:
        m = np.pad(m, (0, MAJORITY_DIM - m.size))
    if s.size < SELF_DIM:
        s = np.pad(s, (0, SELF_DIM - s.size))
    return np.concatenate([c1, d, m, a, s], axis=0).astype(np.float32)


def mark_full_layout() -> Dict[str, Any]:
    return {
        "dim": MARK_FULL_DIM,
        "blocks": {
            "channel1": "0:32",
            "doctrine": "32:48",
            "majority": "48:60",
            "signal_agents_92": "60:152",
            "self_state": "152:168",
        },
    }
