"""L2L process supervision (Proposals 2–7) — train-time only.

Does **not** replace MetaBrain at inference. Builds soft process targets from
living sense packs so the brain learns *how to read* structure/load/taste/regime
without a hard if/then production path.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import numpy as np

from .senses import (
    SENSE_PACK_DIM,
    MarketSenseInput,
    SenseReport,
    encode_sense_report,
    probe_all_senses,
)
from .state import META_RL_DIM, SENSE_STATE_SLICE, build_meta_rl_state
from .types import Direction, SetConfluence, StructureFlags, VelocityStrength


@dataclass
class ProcessTarget:
    """Soft process label for meta_update (train only)."""

    teacher_act: str  # wait | long | short
    teacher_size_frac: float
    process_reward: float  # scales CE; higher = more process weight
    reason: str
    proposal_tags: Tuple[str, ...]


def process_target_from_senses(
    rep: SenseReport,
    *,
    density_mode: bool = False,
) -> ProcessTarget:
    """Derive process target from four senses — never used as live hard rule.

    P2 Sight: structure (topo + consensus force side)
    P3 Feel: load → wait; launch → may fire; collapse → wait
    P4 Taste: allow_fire / patience / conviction
    P5 Hearing: wait_subtype kill / loaded / no_trade
    P6: multi-sense agreement raises process_reward

    ``density_mode`` (L2L-P10 residual): keep the same *decisions* for fail-mode
    waits, but down-weight pure-wait CE so fire process can rebalance A13 density
    without inventing thrash at inference.
    """
    s, f, t, h = rep.sight, rep.feel, rep.taste, rep.hearing
    tags = []
    reward = 1.0
    # Soft wait scale: residual train must not drown fire with high wait CE.
    w_scale = 0.55 if density_mode else 1.0
    f_boost = 0.35 if density_mode else 0.0

    cons = str(s.get("multi_set_consensus") or "incomplete")
    topo = str(s.get("topology_class") or "chop")
    force_side = 1 if cons == "agree_long" else (-1 if cons == "agree_short" else 0)
    if force_side == 0:
        # sight incomplete — weak wait
        tags.append("P2_sight_incomplete")
        return ProcessTarget(
            "wait", 0.0, 0.85 * w_scale, "sight_incomplete_wait", tuple(tags)
        )

    tags.append("P2_sight")
    # Feel gates
    if f.get("collapse"):
        tags.append("P3_feel_collapse")
        return ProcessTarget(
            "wait", 0.0, 1.2 * w_scale, "feel_collapse_wait", tuple(tags)
        )
    if f.get("max_tension_load_building") and not f.get("launch"):
        tags.append("P3_feel_load")
        reward += 0.25
        return ProcessTarget(
            "wait", 0.0, reward * w_scale, "feel_load_wait_process", tuple(tags)
        )
    if h.get("wait_subtype") == "kill":
        tags.append("P5_hear_kill")
        return ProcessTarget(
            "wait", 0.0, 1.3 * w_scale, "hearing_kill_wait", tuple(tags)
        )
    if h.get("wait_subtype") == "no_trade":
        tags.append("P5_hear_no_trade")
        return ProcessTarget(
            "wait", 0.0, 1.0 * w_scale, "hearing_no_trade", tuple(tags)
        )

    # Taste — density residual: if force agrees and launch/topo fire-ok, prefer fire
    # process over patience when allow_fire is only soft-false.
    edge = str(t.get("edge_quality") or "noise")
    fire_topo = topo in ("launch", "release") or edge == "bread_and_butter"
    launchish = bool(f.get("launch") or fire_topo)
    if density_mode and launchish and force_side != 0 and edge != "noise":
        # Soft override: train fire process instead of pure patience wait
        tags.append("P4_density_fire_override")
        act = "long" if force_side > 0 else "short"
        conv = float(t.get("conviction") or 0.55)
        size = float(np.clip(0.4 + 0.4 * conv, 0.3, 0.9))
        rew = 1.15 + f_boost
        if f.get("launch") and edge == "bread_and_butter":
            tags.append("P6_multi_sense_agree")
            rew += 0.4
        tags.append("P2_P3_P4_fire_process")
        return ProcessTarget(act, size, rew, "process_fire_density", tuple(tags))

    if t.get("patience_preferred") or not t.get("allow_fire"):
        tags.append("P4_taste_patience")
        return ProcessTarget(
            "wait", 0.0, 1.15 * w_scale, "taste_patience_wait", tuple(tags)
        )

    if edge == "noise":
        tags.append("P4_taste_noise")
        return ProcessTarget(
            "wait", 0.0, 1.0 * w_scale, "taste_noise_wait", tuple(tags)
        )

    # Launch / release / cont with force + taste allow
    fire_ok = bool(f.get("launch") or topo in ("launch", "release") or edge == "bread_and_butter")
    if not fire_ok and topo == "slingshot_load":
        tags.append("P3_feel_still_load")
        return ProcessTarget(
            "wait", 0.0, 1.1 * w_scale, "still_load", tuple(tags)
        )

    if fire_ok and force_side != 0 and t.get("allow_fire"):
        tags.append("P2_P3_P4_fire_process")
        act = "long" if force_side > 0 else "short"
        conv = float(t.get("conviction") or 0.5)
        size = float(np.clip(0.35 + 0.45 * conv, 0.25, 0.9))
        # multi-sense agreement boost (P6)
        if f.get("launch") and edge == "bread_and_butter" and h.get("day_story_coherent"):
            tags.append("P6_multi_sense_agree")
            reward += 0.45
        elif edge == "bread_and_butter":
            reward += 0.2
        reward += f_boost
        return ProcessTarget(act, size, reward, "process_fire_with_senses", tuple(tags))

    tags.append("P5_default_wait")
    return ProcessTarget(
        "wait", 0.0, 0.9 * w_scale, "default_process_wait", tuple(tags)
    )


def _official_from_force(side: int, strength: float = 0.7) -> Dict[int, SetConfluence]:
    d = Direction.BULL if side > 0 else Direction.BEAR if side < 0 else Direction.NEUTRAL
    vel = VelocityStrength.STRONG if strength > 0.5 else VelocityStrength.MEDIUM
    out = {}
    for sid in (1, 2, 3, 4):
        out[sid] = SetConfluence(
            set_key=f"official:{sid}",
            direction=d,
            velocity=vel if sid <= 2 else VelocityStrength.WEAK,
            n_bull=2 if d == Direction.BULL else 0,
            n_bear=2 if d == Direction.BEAR else 0,
            n_neutral=1,
        )
    return out


# Density residual: fire scenarios overweight so process CE does not starve A13.
_SCENARIOS_BALANCED = (
    "load_wait",
    "launch_fire",
    "collapse_wait",
    "bb_cont",
    "conflict_wait",
    "high_target_patience",
)
# ~55% fire-ish, rest structure waits (still teach load/collapse/conflict)
_SCENARIOS_DENSITY = (
    "launch_fire",
    "launch_fire",
    "bb_cont",
    "bb_cont",
    "bb_cont",
    "load_wait",
    "collapse_wait",
    "conflict_wait",
    "high_target_patience",
)


def sample_l2l_process_episode(
    rng: np.random.Generator,
    *,
    target: Optional[float] = None,
    risk: Optional[float] = None,
    scenario: Optional[str] = None,
    holdout_mode: bool = False,
    density_mode: bool = False,
) -> Tuple[np.ndarray, ProcessTarget, SenseReport]:
    """P2–P7: synthetic episode with sense pack + process target (train only)."""
    if target is None:
        target = float(rng.choice([5.0, 15.0, 30.0, 50.0, 70.0, 90.0]))
    if risk is None:
        risk = float(rng.choice([1.0, 2.0, 3.0]))
    # holdout: novel high targets
    if holdout_mode:
        target = float(rng.uniform(55.0, 90.0))
        risk = float(rng.choice([1.0, 2.0, 3.0]))

    pool = _SCENARIOS_DENSITY if density_mode else _SCENARIOS_BALANCED
    scen = scenario or str(rng.choice(list(pool)))
    side = int(rng.choice([-1, 1]))
    if scen == "load_wait":
        inp = MarketSenseInput(
            htf_force=[0.7 * side] * 8,
            ltf_velocity=[-0.5 * side] * 4,
            inertia=[0.65 * side] * 4,
            inertia_baseline=[0.3 * side] * 4,
            velocity_baseline=[0.1 * side] * 4,
            full_body_outside_rails=True,
            ltf_inside_tight=True,
            efficiency=0.55,
            regime="bull" if side > 0 else "bear",
            g_fixed=True,
            composition_has_force=True,
            composition_has_velocity=True,
            cross_family_agree=True,
            target_percent=target,
            max_daily_risk_percent=risk,
            progress_to_target=float(rng.uniform(0.0, 0.4)),
        )
    elif scen == "launch_fire":
        inp = MarketSenseInput(
            htf_force=[0.75 * side] * 8,
            ltf_velocity=[0.55 * side] * 4,
            inertia=[0.7 * side] * 4,
            inertia_baseline=[0.35 * side] * 4,
            velocity_baseline=[0.2 * side] * 4,
            full_body_outside_rails=True,
            efficiency=0.7,
            regime="bull" if side > 0 else "bear",
            g_fixed=True,
            composition_has_force=True,
            composition_has_velocity=True,
            cross_family_agree=True,
            target_percent=target,
            max_daily_risk_percent=risk,
            progress_to_target=float(rng.uniform(0.0, 0.5)),
            realized_risk_percent=float(rng.uniform(0.0, risk * 0.3)),
        )
    elif scen == "collapse_wait":
        inp = MarketSenseInput(
            htf_force=[0.6 * side] * 8,
            ltf_velocity=[-0.6 * side] * 4,
            inertia=[-0.5 * side] * 4,
            inertia_baseline=[0.2 * side] * 4,
            velocity_baseline=[0.0] * 4,
            g_flip=True,
            g_fixed=False,
            efficiency=0.2,
            regime="vol_shock",
            composition_has_force=True,
            composition_has_velocity=True,
            target_percent=target,
            max_daily_risk_percent=risk,
        )
    elif scen == "conflict_wait":
        inp = MarketSenseInput(
            htf_force=[0.6, 0.5, -0.55, -0.5, 0.2, 0.1, -0.3, -0.2],
            ltf_velocity=[0.1, -0.1, 0.0, 0.05],
            inertia=[0.2, -0.2, 0.0, 0.0],
            inertia_baseline=[0.0] * 4,
            velocity_baseline=[0.0] * 4,
            regime="chop",
            set_conflict=True,
            cross_family_agree=False,
            composition_has_force=True,
            composition_has_velocity=False,
            target_percent=target,
            max_daily_risk_percent=risk,
        )
    elif scen == "high_target_patience":
        inp = MarketSenseInput(
            htf_force=[0.4 * side] * 8,
            ltf_velocity=[0.25 * side] * 4,
            inertia=[0.35 * side] * 4,
            inertia_baseline=[0.2 * side] * 4,
            velocity_baseline=[0.1 * side] * 4,
            efficiency=0.45,
            regime="bull" if side > 0 else "bear",
            composition_has_force=True,
            composition_has_velocity=True,
            cross_family_agree=False,
            target_percent=max(target, 50.0),
            max_daily_risk_percent=risk,
            progress_to_target=0.2,
        )
    else:  # bb_cont
        inp = MarketSenseInput(
            htf_force=[0.8 * side] * 8,
            ltf_velocity=[0.6 * side] * 4,
            inertia=[0.75 * side] * 4,
            inertia_baseline=[0.4 * side] * 4,
            velocity_baseline=[0.25 * side] * 4,
            efficiency=0.75,
            regime="bull" if side > 0 else "bear",
            g_fixed=True,
            composition_has_force=True,
            composition_has_velocity=True,
            cross_family_agree=True,
            target_percent=target,
            max_daily_risk_percent=risk,
            progress_to_target=float(rng.uniform(0.1, 0.6)),
        )

    rep = probe_all_senses(inp)
    pt = process_target_from_senses(rep, density_mode=density_mode)
    if holdout_mode:
        pt = ProcessTarget(
            pt.teacher_act,
            pt.teacher_size_frac,
            pt.process_reward * 1.1,
            pt.reason + "|P7_holdout",
            pt.proposal_tags + ("P7_l2l_holdout",),
        )

    official = _official_from_force(side if scen != "conflict_wait" else 0)
    pullback = str(rep.sight.get("topology_class")) == "slingshot_load"
    st = build_meta_rl_state(
        target_percent=float(inp.target_percent),
        max_daily_risk_percent=float(inp.max_daily_risk_percent),
        official=official,
        structure=StructureFlags(pullback=pullback, scale_conflict=scen == "conflict_wait"),
        sense_report=rep,
        progress_to_target=float(inp.progress_to_target),
        realized_risk_percent=float(inp.realized_risk_percent),
        session_phase=float(rng.uniform(0.3, 0.8)),
    )
    assert st.shape[0] == META_RL_DIM
    assert st[SENSE_STATE_SLICE].shape[0] == SENSE_PACK_DIM
    return st, pt, rep


def train_l2l_process_curriculum(
    brain: Any,
    *,
    steps: int = 4000,
    seed: int = 42,
    holdout_frac: float = 0.2,
    lr: float = 0.02,
    density_mode: bool = False,
) -> Dict[str, Any]:
    """Offline meta_update with process targets (P2–P7). Unlocks brain if frozen.

    ``density_mode``: fire-overweight scenarios + softer wait CE (L2L-P10 residual).
    """
    if getattr(brain, "frozen_for_inference", False):
        brain.unlock_for_meta_train()
    rng = np.random.default_rng(seed)
    n_hold = max(1, int(steps * holdout_frac))
    n_train = max(1, steps - n_hold)
    losses = []
    tag_counts: Dict[str, int] = {}
    n_fire = 0
    n_wait = 0
    for i in range(n_train):
        st, pt, _ = sample_l2l_process_episode(
            rng, holdout_mode=False, density_mode=density_mode
        )
        loss = brain.meta_update(
            st,
            teacher_act=pt.teacher_act,
            lr=lr * (0.97 ** (i // 200)),
            reward=float(pt.process_reward),
            teacher_size_frac=float(pt.teacher_size_frac),
        )
        losses.append(float(loss))
        if pt.teacher_act in ("long", "short"):
            n_fire += 1
        else:
            n_wait += 1
        for t in pt.proposal_tags:
            tag_counts[t] = tag_counts.get(t, 0) + 1
    # P7 holdout episodes (still offline train, novel targets)
    hold_losses = []
    for i in range(n_hold):
        st, pt, _ = sample_l2l_process_episode(
            rng, holdout_mode=True, density_mode=density_mode
        )
        loss = brain.meta_update(
            st,
            teacher_act=pt.teacher_act,
            lr=lr * 0.5,
            reward=float(pt.process_reward),
            teacher_size_frac=float(pt.teacher_size_frac),
        )
        hold_losses.append(float(loss))
        if pt.teacher_act in ("long", "short"):
            n_fire += 1
        else:
            n_wait += 1
    brain.trained = True
    total_acts = max(n_fire + n_wait, 1)
    return {
        "train_steps": n_train,
        "holdout_steps": n_hold,
        "mean_loss": float(np.mean(losses)) if losses else float("nan"),
        "hold_mean_loss": float(np.mean(hold_losses)) if hold_losses else float("nan"),
        "tag_counts": tag_counts,
        "meta_train_steps": int(brain.meta_train_steps),
        "density_mode": bool(density_mode),
        "fire_frac": float(n_fire) / total_acts,
        "n_fire": n_fire,
        "n_wait": n_wait,
        "law": "L2L_P2_P7_process_curriculum",
    }
