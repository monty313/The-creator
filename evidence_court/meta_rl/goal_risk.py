"""Inference-time target/risk context encoding for Meta-RL (no retrain band [5,90]x[1,3])."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np

# Declared action space (objective non-negotiable)
TARGET_MIN = 5.0
TARGET_MAX = 90.0
RISK_MIN = 1.0
RISK_MAX = 3.0

GOAL_RISK_DIM = 8

# Indices into goal/risk context vector
IDX_TARGET_NORM = 0
IDX_RISK_NORM = 1
IDX_HARDNESS = 2
IDX_GOAL_PRESSURE = 3
IDX_RISK_REMAINING = 4
IDX_TARGET_BUCKET = 5
IDX_RISK_BUCKET = 6
IDX_ALLOW_FIRE = 7


@dataclass(frozen=True)
class GoalRiskInputs:
    target_percent: float
    max_daily_risk_percent: float
    progress_to_target: float = 0.0  # 0..1 fraction of target achieved
    realized_risk_percent: float = 0.0  # daily loss used so far (positive = loss)
    equity_day_pct: float = 0.0


def validate_goal_risk(target_percent: float, max_daily_risk_percent: float) -> None:
    if not (TARGET_MIN <= float(target_percent) <= TARGET_MAX):
        raise ValueError(
            f"target_percent={target_percent} outside [{TARGET_MIN}, {TARGET_MAX}]"
        )
    if not (RISK_MIN <= float(max_daily_risk_percent) <= RISK_MAX):
        raise ValueError(
            f"max_daily_risk_percent={max_daily_risk_percent} outside [{RISK_MIN}, {RISK_MAX}]"
        )


def encode_goal_risk_context(
    target_percent: float,
    max_daily_risk_percent: float,
    *,
    progress_to_target: float = 0.0,
    realized_risk_percent: float = 0.0,
    equity_day_pct: float = 0.0,
    validate: bool = True,
) -> np.ndarray:
    """Non-saturating encoding over full declared bands.

    Unlike Mark legacy self_state (target/5 saturates at 5%), this maps:
      target ∈ [5,90] → [0,1]
      risk   ∈ [1,3]  → [0,1]
    """
    if validate:
        validate_goal_risk(target_percent, max_daily_risk_percent)

    t = float(target_percent)
    r = float(max_daily_risk_percent)
    out = np.zeros(GOAL_RISK_DIM, dtype=np.float32)

    out[IDX_TARGET_NORM] = float(np.clip((t - TARGET_MIN) / (TARGET_MAX - TARGET_MIN), 0.0, 1.0))
    out[IDX_RISK_NORM] = float(np.clip((r - RISK_MIN) / (RISK_MAX - RISK_MIN), 0.0, 1.0))

    hardness = t / max(r, 1e-6)
    # log-scale hardness so 5/3 vs 90/1 remain distinguishable without saturating early
    out[IDX_HARDNESS] = float(np.clip(np.log1p(hardness) / np.log1p(TARGET_MAX / RISK_MIN), 0.0, 1.0))

    progress = float(np.clip(progress_to_target, 0.0, 2.0))
    out[IDX_GOAL_PRESSURE] = float(np.clip(1.0 - progress, -1.0, 1.0))

    remaining_risk = max(r - float(realized_risk_percent), 0.0)
    out[IDX_RISK_REMAINING] = float(np.clip(remaining_risk / max(r, 1e-6), 0.0, 1.0))

    # Coarse buckets for attention (not one-hot train pairs)
    out[IDX_TARGET_BUCKET] = float(np.clip((t - TARGET_MIN) / 15.0, 0.0, 1.0))  # ~6 bands
    out[IDX_RISK_BUCKET] = float(np.clip((r - RISK_MIN) / 1.0, 0.0, 1.0))  # 1,2,3

    out[IDX_ALLOW_FIRE] = 1.0 if remaining_risk > 1e-9 else 0.0
    return out


def decode_goal_risk_norms(ctx: np.ndarray) -> Tuple[float, float]:
    """Approximate inverse of target/risk norms (for audits)."""
    c = np.asarray(ctx, dtype=np.float32).reshape(-1)
    t = TARGET_MIN + float(c[IDX_TARGET_NORM]) * (TARGET_MAX - TARGET_MIN)
    r = RISK_MIN + float(c[IDX_RISK_NORM]) * (RISK_MAX - RISK_MIN)
    return t, r


def goal_risk_layout() -> Dict[str, object]:
    return {
        "dim": GOAL_RISK_DIM,
        "target_band": [TARGET_MIN, TARGET_MAX],
        "risk_band": [RISK_MIN, RISK_MAX],
        "fields": [
            "target_norm_5_90",
            "risk_norm_1_3",
            "hardness_log",
            "goal_pressure",
            "risk_remaining_frac",
            "target_bucket",
            "risk_bucket",
            "allow_fire",
        ],
        "note": "Inference-time only; never a train hyperparameter.",
    }
