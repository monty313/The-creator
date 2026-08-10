"""Meta-RL state = Mark full observation + non-saturating goal/risk context."""
from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Sequence

import numpy as np

from .goal_risk import GOAL_RISK_DIM, encode_goal_risk_context
from .observation import (
    MARK_FULL_DIM,
    N_SIGNAL_SLOTS,
    build_channel1_obs,
    build_mark_full_obs,
    pack_agent_votes,
    pack_self_state_mark_legacy,
)
from .senses import SENSE_PACK_DIM, SenseReport, encode_sense_report
from .types import SetConfluence, StructureFlags

META_RL_DIM = MARK_FULL_DIM + GOAL_RISK_DIM  # 168 + 8 = 176
GOAL_RISK_SLICE = slice(MARK_FULL_DIM, META_RL_DIM)
MARK_SLICE = slice(0, MARK_FULL_DIM)
# Senses occupy first SENSE_PACK_DIM of agent_votes inside Mark-168 (index 60..)
SENSE_STATE_SLICE = slice(60, 60 + SENSE_PACK_DIM)
assert SENSE_PACK_DIM <= N_SIGNAL_SLOTS


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
    sense_report: Optional[SenseReport] = None,
    senses_vec: Optional[Sequence[float] | np.ndarray] = None,
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

    L2L Proposal 1: optional sense pack is written into agent_votes[0:SENSE_PACK_DIM]
    so META_RL_DIM stays 176 (champion load path unchanged).
    """
    # Merge sense pack into agent_votes (does not expand META_RL_DIM)
    av = pack_agent_votes(agent_votes)
    if sense_report is not None:
        sv = encode_sense_report(sense_report)
        n = min(SENSE_PACK_DIM, int(sv.size), int(av.size))
        av[:n] = np.asarray(sv[:n], dtype=np.float32)
    elif senses_vec is not None:
        sv = np.asarray(senses_vec, dtype=np.float32).reshape(-1)
        n = min(SENSE_PACK_DIM, int(sv.size), int(av.size))
        av[:n] = sv[:n]

    if mark_full is not None:
        mf = np.asarray(mark_full, dtype=np.float32).reshape(-1)
        if mf.size != MARK_FULL_DIM:
            tmp = np.zeros(MARK_FULL_DIM, dtype=np.float32)
            n = min(MARK_FULL_DIM, int(mf.size))
            tmp[:n] = mf[:n]
            mf = tmp
        # Still overlay senses into agent-vote region of provided mark_full
        if sense_report is not None or senses_vec is not None:
            mf = mf.copy()
            mf[SENSE_STATE_SLICE] = av[:SENSE_PACK_DIM]
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
            agent_votes=av,
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
        "senses_in_agent_votes": f"60:{60 + SENSE_PACK_DIM}",
        "sense_pack_dim": SENSE_PACK_DIM,
        "note": "Additive; senses packed into Mark agent_votes slots (L2L P1).",
    }


def extract_sense_pack(state: np.ndarray) -> np.ndarray:
    s = np.asarray(state, dtype=np.float32).reshape(-1)
    if s.size < 60 + SENSE_PACK_DIM:
        raise ValueError(f"state dim {s.size} too small for sense pack")
    return s[SENSE_STATE_SLICE].copy()
