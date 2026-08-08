"""Meta-RL state = Mark full observation + non-saturating goal/risk context."""
from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Sequence

import numpy as np

from .goal_risk import GOAL_RISK_DIM, encode_goal_risk_context
from .observation import (
    MARK_FULL_DIM,
    build_channel1_obs,
    build_mark_full_obs,
    pack_self_state_mark_legacy,
)
from .types import SetConfluence, StructureFlags

META_RL_DIM = MARK_FULL_DIM + GOAL_RISK_DIM  # 168 + 8 = 176
GOAL_RISK_SLICE = slice(MARK_FULL_DIM, META_RL_DIM)
MARK_SLICE = slice(0, MARK_FULL_DIM)


def build_meta_rl_state(
    *,
    target_percent: float,
    max_daily_risk_percent: float,
    channel1: Optional[np.ndarray] = None,
    official: Optional[Mapping[int, SetConfluence]] = None,
    subs: Optional[Mapping[str, SetConfluence]] = None,
    structure: Optional[StructureFlags] = None,
    doctrine_vec: Optional[np.ndarray] = None,
    majority_vec: Optional[np.ndarray] = None,
    agent_votes: Optional[Sequence[float] | np.ndarray] = None,
    # day self-state for legacy Mark block (kept for compatibility)
    progress_to_target: float = 0.0,
    realized_risk_percent: float = 0.0,
    equity_day_pct: float = 0.0,
    side: float = 0.0,
    session_phase: float = 0.0,
    danger: float = 0.0,
    in_trade: float = 0.0,
    mark_full: Optional[np.ndarray] = None,
    validate: bool = True,
) -> np.ndarray:
    """Build fixed-length Meta-RL state for one inference step.

    Mark full 168-dim is preserved (legacy self_state still uses /5 encoding for
    continuity). Additive GOAL_RISK_DIM channels carry non-saturating [5,90]x[1,3]
    context so the policy can distinguish pairs without retrain.
    """
    if mark_full is not None:
        mf = np.asarray(mark_full, dtype=np.float32).reshape(-1)
        if mf.size != MARK_FULL_DIM:
            tmp = np.zeros(MARK_FULL_DIM, dtype=np.float32)
            n = min(MARK_FULL_DIM, int(mf.size))
            tmp[:n] = mf[:n]
            mf = tmp
    else:
        c1 = channel1
        if c1 is None:
            c1 = build_channel1_obs(
                official,
                subs,
                structure,
                progress_to_goal=progress_to_target,
                danger=danger,
                session_phase=session_phase,
            )
        remaining = max(float(target_percent) * (1.0 - progress_to_target), 0.0)
        room = max(float(max_daily_risk_percent) - float(realized_risk_percent), 0.0)
        self_vec = pack_self_state_mark_legacy(
            side=side,
            progress=progress_to_target,
            danger=danger,
            target_pct=float(target_percent),
            risk_pct=float(max_daily_risk_percent),
            equity_pct=equity_day_pct,
            room_to_floor=room,
            remaining_to_target=remaining,
            session_phase=session_phase,
            in_trade=in_trade,
        )
        mf = build_mark_full_obs(
            c1,
            doctrine_vec=doctrine_vec,
            majority_vec=majority_vec,
            agent_votes=agent_votes,
            self_vec=self_vec,
        )

    ctx = encode_goal_risk_context(
        target_percent,
        max_daily_risk_percent,
        progress_to_target=progress_to_target,
        realized_risk_percent=realized_risk_percent,
        equity_day_pct=equity_day_pct,
        validate=validate,
    )
    return np.concatenate([mf, ctx], axis=0).astype(np.float32)


def extract_goal_risk_context(state: np.ndarray) -> np.ndarray:
    s = np.asarray(state, dtype=np.float32).reshape(-1)
    if s.size < META_RL_DIM:
        raise ValueError(f"state dim {s.size} < META_RL_DIM {META_RL_DIM}")
    return s[GOAL_RISK_SLICE].copy()


def extract_mark_full(state: np.ndarray) -> np.ndarray:
    s = np.asarray(state, dtype=np.float32).reshape(-1)
    return s[MARK_SLICE].copy()


def meta_rl_layout() -> Dict[str, Any]:
    return {
        "dim": META_RL_DIM,
        "mark_full": "0:168",
        "goal_risk_context": f"{MARK_FULL_DIM}:{META_RL_DIM}",
        "note": "Additive; does not replace Mark-168 or PROVEN stacks.",
    }
