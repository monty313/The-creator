"""PATH LEARNING — steps 1–6 offline helpers (learn map, not only copy answers).

Train-time only. Never replaces MetaBrain hard rules at inference.
See ``00_PATH_LEARNING/`` for definitions, implement rules, predicted outcomes.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .l2l_process import sample_l2l_process_episode, train_l2l_process_curriculum
from .path_state_harvest import apply_path_state_teachers_to_brain, filter_path_state_teachers
from .policy import teacher_action_for_state
from .state import META_RL_DIM, build_meta_rl_state, extract_goal_risk_context
from .types import Direction, SetConfluence, StructureFlags, VelocityStrength

# BEST_POLICY forward100 floor (CASE-0037)
FLOOR_100D = {
    "hits": 11,
    "low_hr": 0.28,
    "a13_frac": 0.64,
    "n_zero": 18,
    "breach": 0,
}

# Lab hard floor: below this a13 → process washout suspicion
A13_WASHOUT_HARD = 0.30


# ---------------------------------------------------------------------------
# Step 1 — Outcome-shaped offline updates
# ---------------------------------------------------------------------------


def outcome_score_from_fields(
    *,
    progress_to_target: float = 0.0,
    hit_target: bool = False,
    breach: bool = False,
    realized_pnl: float = 0.0,
    r_capture: float = 0.0,
    dead_fire: bool = False,
) -> float:
    """Map day/slot outcome fields → score in [-1, 1].

    Positive = clear/progress; negative = breach/dead fire.
    """
    if breach:
        return -1.0
    if dead_fire:
        return -0.55
    score = 0.0
    score += 0.55 if hit_target else 0.0
    score += 0.35 * float(np.clip(progress_to_target, 0.0, 1.0))
    score += 0.25 * float(np.clip(r_capture, 0.0, 1.0))
    score += 0.15 * float(np.clip(realized_pnl / 20.0, -0.5, 0.5))
    return float(np.clip(score, -1.0, 1.0))


def outcome_scale(outcome_score: float, *, base: float = 1.0) -> float:
    """Step 1: scale meta_update reward by outcome (shipped entry point).

    Goal-secondary helper only. Prefer ``compose_method_goal_reward`` when a
    method term and method_ok flag are available (method first, goal second).
    """
    s = float(np.clip(outcome_score, -1.0, 1.0))
    # map [-1,1] → [0.35, 1.65] so bad outcomes still train lightly (not zero)
    return float(base) * float(0.35 + 0.65 * (s + 1.0))


# Goal may only nudge; method term dominates. Matches Aaron PKG-005 / AARON §3.10.
GOAL_SECOND_WEIGHT = 0.25


def compose_method_goal_reward(
    method_reward: float,
    *,
    outcome_score: float = 0.0,
    method_ok: bool = True,
    goal_weight: float = GOAL_SECOND_WEIGHT,
    risk_blown: bool = False,
    risk_penalty: float = -0.80,
) -> Dict[str, float]:
    """Method first, goal second — rewards and penalties.

    ``total = method_reward + goal_reward + risk``

    | Layer | Role |
    |-------|------|
    | **Method** | Dominant (+ process shapes / − broken shapes) |
    | **Goal** | Secondary small nudge from outcome_score ∈ [-1,1] |
    | **Risk** | Always-on breach/resource penalty when risk_blown |

    **Law of candy:** if ``method_ok`` is False (mud fire, dip-chase, anti-force,
    thrash), **positive goal progress / PnL candy is zero**. Negative outcome may
    still lightly reinforce the anti-pattern; it never overrides method magnitude.

    Never puts win-rate into the total.
    """
    m = float(method_reward)
    s = float(np.clip(outcome_score, -1.0, 1.0))
    gw = float(max(0.0, goal_weight))
    # Additive goal second: |goal| <= gw * max(|method|, 1) so method always leads
    cap = gw * max(abs(m), 1.0)
    raw_goal = float(np.clip(s * cap, -cap, cap))

    if not method_ok:
        # Method first: no goal candy for broken method. Mild negative only.
        goal = min(0.0, raw_goal)
    else:
        goal = raw_goal

    risk = float(risk_penalty) if risk_blown else 0.0
    total = m + goal + risk
    return {
        "total": float(total),
        "method_reward": m,
        "goal_reward": float(goal),
        "risk_penalty": risk,
        "method_ok": bool(method_ok),
        "method_first": True,
        "goal_weight": gw,
    }


def apply_outcome_shaped_update(
    brain: Any,
    state: np.ndarray,
    *,
    teacher_act: str,
    outcome_score: float,
    lr: float = 0.02,
    teacher_size_frac: Optional[float] = None,
    base_reward: float = 1.0,
    method_ok: bool = True,
    risk_blown: bool = False,
) -> float:
    """Step 1 shipped: offline meta_update with method-first, goal-second reward.

    ``base_reward`` = method / process term (dominant).
    ``outcome_score`` = goal second (blocked when method_ok is False).
    """
    if method_ok and not risk_blown:
        # Legacy path when method is clean: multiplicative outcome scale (compat)
        rew = outcome_scale(outcome_score, base=base_reward)
    else:
        # Broken method or risk event: compose so goal candy cannot override method
        rew = float(
            compose_method_goal_reward(
                base_reward,
                outcome_score=outcome_score,
                method_ok=method_ok,
                risk_blown=risk_blown,
            )["total"]
        )
    return float(
        brain.meta_update(
            state,
            teacher_act=str(teacher_act),
            lr=float(lr),
            reward=rew,
            teacher_size_frac=teacher_size_frac,
        )
    )


def stamp_path_teacher_day_outcome(
    ex: Dict[str, Any],
    *,
    day_pnl: float,
    target_percent: float,
    max_daily_risk_percent: float,
    n_trades: int = 0,
) -> Dict[str, Any]:
    """Attach day-level outcome tags to a path teacher (shipped 2× CLEAR ROAD).

    Tags: hit_target, breach, progress_to_target, realized_pnl, r_capture,
    dead_fire, outcome_score — used by outcome-shaped path apply.
    """
    row = dict(ex)
    t = float(target_percent)
    r = float(max_daily_risk_percent)
    pnl = float(day_pnl)
    hit = pnl >= t - 1e-9
    breach = pnl < -r - 1e-9  # realized loss beyond risk (conservative day tag)
    progress = float(np.clip(pnl / max(t, 1e-6), -1.0, 1.5))
    # crude R-capture proxy: positive pnl vs risk budget
    r_cap = float(np.clip(max(pnl, 0.0) / max(r, 1e-6), 0.0, 2.0) / 2.0)
    dead = bool(n_trades > 0 and abs(pnl) < 0.05 * max(t, 1.0) and not hit)
    oc = outcome_score_from_fields(
        progress_to_target=max(progress, 0.0),
        hit_target=hit,
        breach=breach,
        realized_pnl=pnl,
        r_capture=r_cap,
        dead_fire=dead,
    )
    row["harvest_day_target"] = t
    row["harvest_day_risk"] = r
    row["harvest_day_n_trades"] = int(n_trades)
    row["realized_pnl"] = pnl
    row["hit_target"] = bool(hit)
    row["breach"] = bool(breach)
    row["progress_to_target"] = float(progress)
    row["r_capture"] = float(r_cap)
    row["dead_fire"] = bool(dead)
    row["outcome_score"] = float(oc)
    row["outcome_tagged"] = True
    return row


def outcome_score_from_teacher(ex: Dict[str, Any]) -> float:
    """Read outcome_score from a tagged teacher, or derive from fields."""
    if ex.get("outcome_score") is not None:
        return float(ex["outcome_score"])
    return outcome_score_from_fields(
        progress_to_target=float(ex.get("progress_to_target") or 0.0),
        hit_target=bool(ex.get("hit_target")),
        breach=bool(ex.get("breach")),
        realized_pnl=float(ex.get("realized_pnl") or 0.0),
        r_capture=float(ex.get("r_capture") or 0.0),
        dead_fire=bool(ex.get("dead_fire")),
    )


def apply_outcome_tagged_path_teachers(
    brain: Any,
    examples: Sequence[Dict[str, Any]],
    *,
    lr: float = 0.02,
    seed: int = 11,
    max_examples: int = 900,
    n_passes: int = 2,
) -> Dict[str, Any]:
    """Offline path-state apply with outcome-shaped rewards (2× CLEAR ROAD)."""
    labs = filter_path_state_teachers(
        list(examples), max_examples=max_examples, require_htf_active=True
    )
    if not labs:
        return {"n_updates": 0, "n_tagged": 0, "mean_outcome_score": float("nan")}
    if getattr(brain, "frozen_for_inference", False):
        brain.unlock_for_meta_train()
    rng = np.random.default_rng(seed)
    n = 0
    scores: List[float] = []
    n_tagged = 0
    for _ in range(max(1, int(n_passes))):
        order = list(labs)
        rng.shuffle(order)
        for ex in order:
            st = np.asarray(ex["state"], dtype=np.float64).ravel()
            oc = outcome_score_from_teacher(ex)
            if ex.get("outcome_tagged") or ex.get("outcome_score") is not None:
                n_tagged += 1
            scores.append(oc)
            w = float(ex.get("weight") or 1.0)
            apply_outcome_shaped_update(
                brain,
                st,
                teacher_act=str(ex["teacher_act"]),
                outcome_score=oc,
                lr=lr,
                teacher_size_frac=float(ex.get("teacher_size_frac") or 0.65),
                base_reward=1.0 + 0.2 * min(w, 2.0),
            )
            n += 1
    brain.trained = True
    return {
        "n_updates": n,
        "n_examples": len(labs),
        "n_tagged": n_tagged,
        "mean_outcome_score": float(np.mean(scores)) if scores else float("nan"),
        "law": "PATH_OUTCOME_TAGGED_APPLY",
    }


# ---------------------------------------------------------------------------
# Step 4 — Conversion teachers (not fire-only)
# ---------------------------------------------------------------------------


@dataclass
class ConversionTeacher:
    teacher_act: str
    teacher_size_frac: float
    reason: str
    class_name: str  # fire_edge | hold_convert | wait_pullback | wait_risk | size_down


def conversion_teacher_from_context(
    *,
    progress_to_target: float,
    risk_remaining_frac: float,
    topology: str = "chop",
    force_side: int = 0,
    load_building: bool = False,
    collapse: bool = False,
    conflict: bool = False,
    outcome_score: float = 0.0,
    high_target: bool = False,
) -> ConversionTeacher:
    """Step 4 shipped: conversion-aware teacher from context (not fire-only)."""
    prog = float(np.clip(progress_to_target, 0.0, 1.0))
    risk_rem = float(np.clip(risk_remaining_frac, 0.0, 1.0))
    topo = str(topology or "chop")
    side = int(force_side)

    if collapse or conflict:
        return ConversionTeacher("wait", 0.0, "conflict_or_collapse_wait", "wait_pullback")
    if load_building and topo in ("slingshot_load", "chop", "load"):
        return ConversionTeacher("wait", 0.0, "pullback_building_wait", "wait_pullback")
    if risk_rem < 0.18:
        return ConversionTeacher("wait", 0.0, "risk_floor_wait", "wait_risk")

    actionable = topo in ("pullback_resume", "continuation", "launch", "release", "bb_cont")
    if side == 0 or not actionable:
        return ConversionTeacher("wait", 0.0, "no_force_or_edge", "wait_pullback")

    act = "long" if side > 0 else "short"

    # Near risk with open edge → size down, not thrash full size
    if risk_rem < 0.35 or (high_target and prog < 0.25):
        size = float(np.clip(0.25 + 0.2 * max(outcome_score, 0.0), 0.2, 0.45))
        return ConversionTeacher(act, size, "size_down_under_risk_or_high_t", "size_down")

    # Mid progress + edge → hold/convert (sustain size)
    if 0.25 <= prog < 0.85 and actionable:
        size = float(np.clip(0.45 + 0.25 * max(outcome_score, 0.0), 0.4, 0.75))
        return ConversionTeacher(act, size, "hold_convert_mid_progress", "hold_convert")

    # Fresh edge, low progress → fire_edge
    size = float(np.clip(0.5 + 0.2 * max(outcome_score, 0.0), 0.4, 0.85))
    return ConversionTeacher(act, size, "fire_edge_low_progress", "fire_edge")


def _official_side(side: int) -> Dict[int, SetConfluence]:
    d = Direction.BULL if side > 0 else Direction.BEAR if side < 0 else Direction.NEUTRAL
    out = {}
    for sid in (1, 2, 3, 4):
        out[sid] = SetConfluence(
            set_key=f"official:{sid}",
            direction=d,
            velocity=VelocityStrength.STRONG if sid <= 2 else VelocityStrength.MEDIUM,
            n_bull=2 if d == Direction.BULL else 0,
            n_bear=2 if d == Direction.BEAR else 0,
            n_neutral=1,
        )
    return out


def sample_conversion_episode(
    rng: np.random.Generator,
    *,
    holdout_mode: bool = False,
) -> Tuple[np.ndarray, ConversionTeacher, float]:
    """Synthetic conversion episode → (state, teacher, outcome_score)."""
    if holdout_mode:
        target = float(rng.uniform(55.0, 90.0))
    else:
        target = float(rng.choice([5.0, 15.0, 30.0, 50.0, 70.0, 90.0]))
    risk = float(rng.choice([1.0, 2.0, 3.0]))
    side = int(rng.choice([-1, 1]))
    mode = str(
        rng.choice(
            [
                "load",
                "fire_edge",
                "hold",
                "risk_low",
                "conflict",
            ]
        )
    )
    if mode == "load":
        ct = conversion_teacher_from_context(
            progress_to_target=0.1,
            risk_remaining_frac=0.8,
            topology="slingshot_load",
            force_side=side,
            load_building=True,
        )
        prog, risk_rem = 0.1, 0.8
        outcome = outcome_score_from_fields(progress_to_target=0.1)
    elif mode == "hold":
        ct = conversion_teacher_from_context(
            progress_to_target=0.5,
            risk_remaining_frac=0.55,
            topology="continuation",
            force_side=side,
            outcome_score=0.4,
        )
        prog, risk_rem = 0.5, 0.55
        outcome = outcome_score_from_fields(progress_to_target=0.5, r_capture=0.4)
    elif mode == "risk_low":
        ct = conversion_teacher_from_context(
            progress_to_target=0.3,
            risk_remaining_frac=0.12,
            topology="pullback_resume",
            force_side=side,
        )
        prog, risk_rem = 0.3, 0.12
        outcome = outcome_score_from_fields(progress_to_target=0.3, breach=False)
    elif mode == "conflict":
        ct = conversion_teacher_from_context(
            progress_to_target=0.2,
            risk_remaining_frac=0.7,
            topology="chop",
            force_side=0,
            conflict=True,
        )
        prog, risk_rem = 0.2, 0.7
        side = 0
        outcome = 0.0
    else:
        ct = conversion_teacher_from_context(
            progress_to_target=0.1,
            risk_remaining_frac=0.75,
            topology="pullback_resume",
            force_side=side,
            outcome_score=0.2,
            high_target=target >= 50.0,
        )
        prog, risk_rem = 0.1, 0.75
        outcome = outcome_score_from_fields(progress_to_target=0.1, realized_pnl=1.0)

    realized_risk = float(risk) * (1.0 - risk_rem)
    st = build_meta_rl_state(
        target_percent=target,
        max_daily_risk_percent=risk,
        official=_official_side(side if side != 0 else 1),
        structure=StructureFlags(
            pullback="pullback" in ct.reason or mode == "fire_edge",
            scale_conflict=mode == "conflict",
        ),
        progress_to_target=prog,
        realized_risk_percent=realized_risk,
        session_phase=float(rng.uniform(0.35, 0.8)),
    )
    assert st.shape[0] == META_RL_DIM
    return st, ct, outcome


# ---------------------------------------------------------------------------
# Steps 2–3 — Goal/risk primary curriculum + holdout + path anchors mix
# ---------------------------------------------------------------------------


def train_path_learning_curriculum(
    brain: Any,
    *,
    steps: int = 2500,
    seed: int = 42,
    path_examples: Optional[Sequence[Dict[str, Any]]] = None,
    path_anchor_frac: float = 0.20,
    holdout_frac: float = 0.15,
    process_frac: float = 0.12,
    lr: float = 0.015,
    density_process: bool = True,
) -> Dict[str, Any]:
    """Steps 1–4 mix: goal/risk+conversion+outcome primary; sparse path anchors; holdout.

    Does **not** freeze. Caller may run process re-anchor separately (step 5).
    """
    if getattr(brain, "frozen_for_inference", False):
        brain.unlock_for_meta_train()
    rng = np.random.default_rng(seed)
    labs = []
    if path_examples:
        labs = filter_path_state_teachers(
            list(path_examples), max_examples=max(50, len(path_examples)), require_htf_active=True
        )

    n_hold = max(1, int(steps * holdout_frac))
    n_main = max(1, steps - n_hold)
    counts = {
        "conversion": 0,
        "path_anchor": 0,
        "process": 0,
        "holdout": 0,
        "outcome_shaped": 0,
    }
    class_counts: Dict[str, int] = {}
    losses: List[float] = []

    def _one(holdout: bool) -> None:
        u = float(rng.random())
        # path anchors only on main track (holdout stays goal/conversion)
        if labs and not holdout and u < float(path_anchor_frac):
            ex = labs[int(rng.integers(0, len(labs)))]
            st = np.asarray(ex["state"], dtype=np.float64).ravel()
            act = str(ex["teacher_act"])
            # mild positive outcome prior for real path edge teachers
            oc = float(ex.get("outcome_score") or 0.25)
            loss = apply_outcome_shaped_update(
                brain,
                st,
                teacher_act=act,
                outcome_score=oc,
                lr=lr * (0.5 if holdout else 1.0),
                teacher_size_frac=float(ex.get("teacher_size_frac") or 0.65),
            )
            counts["path_anchor"] += 1
            counts["outcome_shaped"] += 1
            losses.append(loss)
            return
        if not holdout and u < float(path_anchor_frac) + float(process_frac):
            st, pt, _ = sample_l2l_process_episode(
                rng, holdout_mode=False, density_mode=bool(density_process)
            )
            oc = 0.15 if pt.teacher_act == "wait" else 0.35
            loss = apply_outcome_shaped_update(
                brain,
                st,
                teacher_act=pt.teacher_act,
                outcome_score=oc,
                lr=lr,
                teacher_size_frac=float(pt.teacher_size_frac),
                base_reward=float(pt.process_reward),
            )
            counts["process"] += 1
            counts["outcome_shaped"] += 1
            losses.append(loss)
            return
        # primary: conversion + goal/risk
        st, ct, oc = sample_conversion_episode(rng, holdout_mode=holdout)
        loss = apply_outcome_shaped_update(
            brain,
            st,
            teacher_act=ct.teacher_act,
            outcome_score=oc,
            lr=lr * (0.55 if holdout else 1.0),
            teacher_size_frac=ct.teacher_size_frac,
        )
        counts["conversion"] += 1
        counts["outcome_shaped"] += 1
        if holdout:
            counts["holdout"] += 1
        class_counts[ct.class_name] = class_counts.get(ct.class_name, 0) + 1
        losses.append(loss)

    for i in range(n_main):
        _one(False)
        if i and i % 200 == 0:
            lr = lr * 0.97
    hold_losses: List[float] = []
    for _ in range(n_hold):
        before = len(losses)
        _one(True)
        if len(losses) > before:
            hold_losses.append(losses[-1])

    brain.trained = True
    total = max(sum(counts[k] for k in ("conversion", "path_anchor", "process")), 1)
    return {
        "law": "PATH_LEARNING_CURRICULUM",
        "steps": steps,
        "train_main": n_main,
        "holdout_steps": n_hold,
        "counts": counts,
        "class_counts": class_counts,
        "path_anchor_frac_realized": counts["path_anchor"] / total,
        "mean_loss": float(np.mean(losses)) if losses else float("nan"),
        "hold_mean_loss": float(np.mean(hold_losses)) if hold_losses else float("nan"),
        "meta_train_steps": int(getattr(brain, "meta_train_steps", 0)),
        "path_only_clone": counts["path_anchor"] > 0
        and counts["conversion"] == 0
        and counts["process"] == 0,
        "has_outcome_shaping": counts["outcome_shaped"] > 0,
        "has_conversion": counts["conversion"] > 0,
        "has_holdout": counts["holdout"] > 0,
    }


def path_reanchor(
    brain: Any,
    path_examples: Sequence[Dict[str, Any]],
    *,
    n_passes: int = 2,
    seed: int = 7,
    max_examples: int = 900,
) -> int:
    """Step 5 support: path-state re-anchor last (anti-washout)."""
    labs = filter_path_state_teachers(
        list(path_examples), max_examples=max_examples, require_htf_active=True
    )
    if not labs:
        return 0
    return apply_path_state_teachers_to_brain(
        brain,
        labs,
        lr=0.02,
        seed=seed,
        max_examples=len(labs),
        n_passes=int(n_passes),
    )


# ---------------------------------------------------------------------------
# Day conversion — remap real path states (not fire-only same-day clone)
# ---------------------------------------------------------------------------


def day_outcome_bucket(
    *,
    day_pnl: float,
    target_percent: float,
    max_daily_risk_percent: float,
    n_trades: int = 0,
    hit_target: Optional[bool] = None,
    breach: Optional[bool] = None,
    dead_fire: Optional[bool] = None,
) -> str:
    """Bucket a day for multi-day harvest: clear | dead | near_breach | progress."""
    t = float(target_percent)
    r = float(max_daily_risk_percent)
    pnl = float(day_pnl)
    hit = bool(hit_target) if hit_target is not None else (pnl >= t - 1e-9)
    br = bool(breach) if breach is not None else (pnl < -r - 1e-9)
    dead = (
        bool(dead_fire)
        if dead_fire is not None
        else bool(n_trades > 0 and abs(pnl) < 0.05 * max(t, 1.0) and not hit)
    )
    if br:
        return "near_breach"
    if hit:
        return "clear"
    if dead:
        return "dead"
    # near risk floor of loss without hard breach stamp
    if pnl < -0.55 * r:
        return "near_breach"
    return "progress"


def conversion_remap_path_teacher(ex: Dict[str, Any]) -> Dict[str, Any]:
    """Map one real path teacher → conversion label (wait / hold_convert / size_down / fire).

    Uses day outcome tags + topology/force — not edge-act clone.
    Arbitration day12: conversion not lot cosplay / not fire-only classification.
    """
    row = dict(ex)
    topo = str(row.get("topology") or "chop")
    force = float(row.get("force") or 0.0)
    edge_act = str(row.get("teacher_act") or "wait")
    if edge_act == "long":
        side = 1
    elif edge_act == "short":
        side = -1
    else:
        side = 1 if force > 0 else (-1 if force < 0 else 0)

    prog = float(row.get("progress_to_target") or 0.0)
    # risk remaining proxy from day risk spend
    day_risk = float(row.get("harvest_day_risk") or 3.0)
    realized = float(row.get("realized_pnl") or 0.0)
    # if mid-day progress known from state harvest, prefer it
    risk_spent_frac = float(np.clip(max(-realized, 0.0) / max(day_risk, 1e-6), 0.0, 1.0))
    risk_rem = float(np.clip(1.0 - risk_spent_frac, 0.0, 1.0))
    # fill-level override when present (day12 measure path)
    fill_pnl = row.get("fill_pnl")
    fill_label = str(row.get("fill_label") or "")

    bucket = str(
        row.get("day_bucket")
        or day_outcome_bucket(
            day_pnl=realized,
            target_percent=float(row.get("harvest_day_target") or 15.0),
            max_daily_risk_percent=day_risk,
            n_trades=int(row.get("harvest_day_n_trades") or 0),
            hit_target=row.get("hit_target"),
            breach=row.get("breach"),
            dead_fire=row.get("dead_fire"),
        )
    )
    row["day_bucket"] = bucket
    oc = outcome_score_from_teacher(row)
    cons = str(row.get("multi_set_consensus") or "")
    conflict = cons == "conflict" or abs(force) < 0.12
    dead = bool(row.get("dead_fire")) or bucket == "dead"
    high_t = float(row.get("harvest_day_target") or 15.0) >= 15.0 - 1e-9

    # Fill-selective conversion (when per-leg known)
    if fill_label == "loss" or (fill_pnl is not None and float(fill_pnl) < -0.02):
        ct = ConversionTeacher("wait", 0.0, "dead_or_loss_leg_wait", "wait_pullback")
    elif fill_label == "win" and topo == "continuation":
        ct = conversion_teacher_from_context(
            progress_to_target=max(prog, 0.35),
            risk_remaining_frac=max(risk_rem, 0.4),
            topology="continuation",
            force_side=side if side != 0 else 1,
            outcome_score=max(oc, 0.4),
            high_target=high_t,
        )
        if ct.class_name == "fire_edge":
            ct = ConversionTeacher(
                ct.teacher_act,
                float(np.clip(ct.teacher_size_frac, 0.45, 0.75)),
                "hold_convert_win_cont",
                "hold_convert",
            )
    elif bucket == "clear":
        # Clear days: hold quality cont / fire clean PB — not thrash densify
        ct = conversion_teacher_from_context(
            progress_to_target=max(prog, 0.4),
            risk_remaining_frac=max(risk_rem, 0.45),
            topology=topo if topo in ("pullback_resume", "continuation") else "continuation",
            force_side=side if side != 0 else 1,
            outcome_score=max(oc, 0.45),
            high_target=high_t,
        )
    elif bucket == "near_breach" or risk_rem < 0.22:
        ct = conversion_teacher_from_context(
            progress_to_target=prog,
            risk_remaining_frac=min(risk_rem, 0.15),
            topology=topo if topo else "continuation",
            force_side=side,
            high_target=high_t,
        )
        if ct.class_name not in ("wait_risk", "size_down"):
            ct = ConversionTeacher("wait", 0.0, "near_breach_wait", "wait_risk")
    elif dead or conflict:
        ct = ConversionTeacher("wait", 0.0, "dead_r_or_conflict_wait", "wait_pullback")
    else:
        # progress / miss-target under rail: size_down + hold_convert bias, not fire-only
        ct = conversion_teacher_from_context(
            progress_to_target=float(np.clip(prog if prog > 0 else 0.15, 0.0, 0.9)),
            risk_remaining_frac=float(np.clip(risk_rem if risk_rem > 0 else 0.55, 0.1, 0.95)),
            topology=topo if topo in ("pullback_resume", "continuation", "launch", "release") else "continuation",
            force_side=side if side != 0 else 1,
            outcome_score=oc,
            high_target=high_t,
            conflict=conflict,
        )
        # Missed high target with thrash density → prefer size_down / hold over fire_edge
        n_tr = int(row.get("harvest_day_n_trades") or 0)
        if n_tr >= 20 and not bool(row.get("hit_target")) and ct.class_name == "fire_edge":
            if risk_rem < 0.45:
                ct = ConversionTeacher(
                    ct.teacher_act,
                    float(np.clip(0.28 + 0.1 * max(oc, 0.0), 0.2, 0.42)),
                    "size_down_thrash_day",
                    "size_down",
                )
            else:
                ct = ConversionTeacher(
                    ct.teacher_act,
                    float(np.clip(0.5 + 0.15 * max(oc, 0.0), 0.4, 0.7)),
                    "hold_convert_busy_miss",
                    "hold_convert",
                )

    row["teacher_act"] = ct.teacher_act
    row["teacher_size_frac"] = float(ct.teacher_size_frac)
    row["conversion_class"] = ct.class_name
    row["conversion_reason"] = ct.reason
    row["source"] = str(row.get("source") or "path_state") + "|conversion_remap"
    if "path_state" not in row["source"]:
        row["source"] = "path_state_conversion"
    return row


def apply_conversion_path_teachers(
    brain: Any,
    examples: Sequence[Dict[str, Any]],
    *,
    lr: float = 0.02,
    seed: int = 11,
    max_examples: int = 1200,
    n_passes: int = 2,
    bucket_weights: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Offline apply with conversion remap (wait / hold_convert / size_down / fire).

    Keeps wait. Does **not** fire-only clone. Weights clear/dead/near_breach buckets.
    """
    bw = dict(bucket_weights or {"clear": 1.4, "dead": 1.25, "near_breach": 1.3, "progress": 1.0})
    raw = filter_path_state_teachers(
        list(examples),
        max_examples=max(max_examples * 2, 100),
        require_htf_active=True,
        allow_wait=True,
    )
    # If filter dropped wait-less packs, still accept long/short and remap
    if not raw:
        raw = filter_path_state_teachers(
            list(examples), max_examples=max_examples * 2, require_htf_active=True, allow_wait=False
        )
    remapped = [conversion_remap_path_teacher(ex) for ex in raw]
    # Oversample conversion classes that fire-only training skips
    boosted: List[Dict[str, Any]] = []
    for ex in remapped:
        bucket = str(ex.get("day_bucket") or "progress")
        w = float(bw.get(bucket, 1.0))
        cls = str(ex.get("conversion_class") or "")
        copies = max(1, int(round(w)))
        if cls in ("wait_pullback", "wait_risk", "hold_convert", "size_down"):
            copies += 1
        for _ in range(copies):
            boosted.append(ex)
    if len(boosted) > max_examples:
        rng = np.random.default_rng(seed)
        idx = rng.choice(len(boosted), size=int(max_examples), replace=False)
        labs = [boosted[int(i)] for i in idx]
    else:
        labs = boosted

    if not labs:
        return {
            "n_updates": 0,
            "n_examples": 0,
            "class_counts": {},
            "bucket_counts": {},
            "law": "PATH_CONVERSION_APPLY",
        }
    if getattr(brain, "frozen_for_inference", False):
        brain.unlock_for_meta_train()
    rng = np.random.default_rng(seed)
    n = 0
    class_counts: Dict[str, int] = {}
    bucket_counts: Dict[str, int] = {}
    for _ in range(max(1, int(n_passes))):
        order = list(labs)
        rng.shuffle(order)
        for ex in order:
            st = np.asarray(ex["state"], dtype=np.float64).ravel()
            if st.size != META_RL_DIM:
                continue
            oc = outcome_score_from_teacher(ex)
            cls = str(ex.get("conversion_class") or "fire_edge")
            # Dead / wait get negative-leaning oc so wait sticks
            if cls.startswith("wait") and oc > -0.1:
                oc = min(oc, -0.25)
            apply_outcome_shaped_update(
                brain,
                st,
                teacher_act=str(ex["teacher_act"]),
                outcome_score=oc,
                lr=lr,
                teacher_size_frac=float(ex.get("teacher_size_frac") or 0.0),
                base_reward=1.25 if cls in ("hold_convert", "wait_pullback", "size_down") else 1.05,
            )
            n += 1
            class_counts[cls] = class_counts.get(cls, 0) + 1
            b = str(ex.get("day_bucket") or "progress")
            bucket_counts[b] = bucket_counts.get(b, 0) + 1
    brain.trained = True
    return {
        "n_updates": n,
        "n_examples": len(labs),
        "class_counts": class_counts,
        "bucket_counts": bucket_counts,
        "has_wait": any(k.startswith("wait") for k in class_counts),
        "has_hold_convert": "hold_convert" in class_counts,
        "has_size_down": "size_down" in class_counts,
        "law": "PATH_CONVERSION_APPLY",
    }


def load_outcome_tagged_examples(
    paths: Sequence[Any],
    *,
    max_examples: int = 2000,
) -> List[Dict[str, Any]]:
    """Load multi-day outcome-tagged path teachers from JSON packs."""
    from pathlib import Path as _P

    raw: List[Dict[str, Any]] = []
    for p in paths:
        path = _P(p)
        if not path.exists():
            continue
        try:
            pack = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for ex in pack.get("examples") or []:
            if not isinstance(ex, dict):
                continue
            if not ex.get("outcome_tagged"):
                ex = stamp_path_teacher_day_outcome(
                    ex,
                    day_pnl=float(ex.get("realized_pnl") or 0.0),
                    target_percent=float(ex.get("harvest_day_target") or 15.0),
                    max_daily_risk_percent=float(ex.get("harvest_day_risk") or 2.0),
                    n_trades=int(ex.get("harvest_day_n_trades") or 0),
                )
            ex = dict(ex)
            ex["day_bucket"] = day_outcome_bucket(
                day_pnl=float(ex.get("realized_pnl") or 0.0),
                target_percent=float(ex.get("harvest_day_target") or 15.0),
                max_daily_risk_percent=float(ex.get("harvest_day_risk") or 2.0),
                n_trades=int(ex.get("harvest_day_n_trades") or 0),
                hit_target=ex.get("hit_target"),
                breach=ex.get("breach"),
                dead_fire=ex.get("dead_fire"),
            )
            raw.append(ex)
    if len(raw) > max_examples:
        # Prefer diversity of buckets
        by_b: Dict[str, List[Dict[str, Any]]] = {}
        for ex in raw:
            by_b.setdefault(str(ex.get("day_bucket") or "progress"), []).append(ex)
        out: List[Dict[str, Any]] = []
        keys = list(by_b.keys())
        i = 0
        while len(out) < max_examples and any(by_b.values()):
            k = keys[i % len(keys)]
            if by_b.get(k):
                out.append(by_b[k].pop())
            i += 1
            if i > max_examples * 4:
                break
        return out
    return raw


# ---------------------------------------------------------------------------
# Step 6 — Promote guard
# ---------------------------------------------------------------------------


def path_learning_promote_guard(
    dual_lab: Dict[str, Any],
    dual_champ: Optional[Dict[str, Any]] = None,
    *,
    floor: Optional[Dict[str, Any]] = None,
    path_only_clone: bool = False,
    process_washout: bool = False,
    has_outcome_conversion_mix: bool = True,
    court_promote: bool = False,
) -> Dict[str, Any]:
    """Step 6 shipped: reject washout / pure clone without floor; no silent production.

    ``promote_lab``: may keep as lab shadow winner vs champ window.
    ``production_replace``: only if floor held **and** court_promote True.
    """
    floor = dict(floor or FLOOR_100D)
    dual_champ = dual_champ or {}
    a13 = float(dual_lab.get("a13_frac") or 0.0)
    hits = int(dual_lab.get("hits") or 0)
    n_zero = int(dual_lab.get("n_zero") or 0)
    breach = int(dual_lab.get("breach_count") or 0)
    frozen = bool(dual_lab.get("weights_frozen", True))
    c_a13 = float(dual_champ.get("a13_frac") or 0.0) if dual_champ else a13
    c_hits = int(dual_champ.get("hits") or 0) if dual_champ else hits
    c_zero = int(dual_champ.get("n_zero") or 999) if dual_champ else n_zero

    reasons: List[str] = []
    if breach > 0:
        reasons.append(f"breach={breach}")
    if not frozen:
        reasons.append("not_frozen")
    if process_washout or a13 < A13_WASHOUT_HARD:
        reasons.append(f"process_washout_or_a13<{A13_WASHOUT_HARD}")
        process_washout = True
    if path_only_clone and not has_outcome_conversion_mix:
        reasons.append("path_only_clone_without_learning_mix")
    if not has_outcome_conversion_mix:
        reasons.append("missing_outcome_conversion_mix")

    floor_hold = (
        hits >= int(floor["hits"])
        and a13 >= float(floor["a13_frac"]) - 1e-12
        and n_zero <= int(floor["n_zero"])
        and breach == 0
    )
    # low_hr optional if present
    if "low_hr" in dual_lab and dual_lab["low_hr"] is not None:
        floor_hold = floor_hold and float(dual_lab["low_hr"]) >= float(floor["low_hr"]) - 1e-12

    beats_champ = (
        (not dual_champ)
        or (
            a13 >= c_a13 - 1e-9
            and hits >= c_hits
            and n_zero <= c_zero
            and breach == 0
        )
    )

    promote_lab = (
        frozen
        and breach == 0
        and not process_washout
        and has_outcome_conversion_mix
        and not (path_only_clone and not has_outcome_conversion_mix)
        and a13 >= A13_WASHOUT_HARD
        and beats_champ
    )
    if reasons and not (promote_lab and not reasons):
        # hard reject reasons block lab promote
        hard = any(
            x.startswith("breach")
            or "washout" in x
            or "path_only" in x
            or "missing_outcome" in x
            or x == "not_frozen"
            for x in reasons
        )
        if hard:
            promote_lab = False

    production_replace = bool(promote_lab and floor_hold and court_promote)

    return {
        "promote_lab": bool(promote_lab),
        "production_replace": bool(production_replace),
        "floor_hold": bool(floor_hold),
        "beats_champ_window": bool(beats_champ),
        "process_washout": bool(process_washout),
        "path_only_clone": bool(path_only_clone),
        "reasons": reasons,
        "floor": floor,
        "lab": {"a13_frac": a13, "hits": hits, "n_zero": n_zero, "breach_count": breach},
        "note": "production_replace requires floor_hold AND court_promote; lab shadow only otherwise",
    }
