"""Aaron Force + LTF state curriculum — teach reasoning shapes, not answer-copy.

Force (2 HTFs agree) → LTF state (pullback / continuation / calibrating)
→ **Hold while Force holds** (t4) → exit when Force dies.

**Forbidden language:** Load / Reclaim. Method-first rewards from Aaron_here/AARON.md.
Offline meta_update only. Does not replace MetaBrain at inference.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from .path_learning import compose_method_goal_reward
from .state import META_RL_DIM, SENSE_STATE_SLICE, build_meta_rl_state
from .senses import MarketSenseInput, SENSE_PACK_DIM, probe_all_senses
from .types import Direction, SetConfluence, StructureFlags, VelocityStrength

# Aaron §3.10 — METHOD FIRST (dominant), GOAL SECOND (outcome_score, blocked if method broken).
# Magnitudes are *meta_update rewards* (higher = stronger CE pull), not PnL.
# Compose with path_learning.compose_method_goal_reward at train time.
METHOD_REWARD = {
    "force_wait": 1.15,  # + WAIT when force == 0
    "pullback_wait": 1.25,  # + WAIT when LTF pullback under Force
    "continuation_fire": 1.55,  # + FIRE on continuation with Force
    "hold_while_force": 1.70,  # + t4 hold / re-commit while Force holds (anti early scratch)
    "force_exit_wait": 1.30,  # + stop new fire when Force dies
    "kill_wait": 1.35,  # + WAIT on collapse
    "dip_chase_wait": 1.45,  # + correct WAIT on load-bottom (punish premature fire via teacher)
    "anti_force_wait": 1.50,  # + WAIT rather than fight the tide
    "thrash_wait": 1.40,  # + WAIT on no-force spam / conflict thrash
}
# Negative outcome prior when method is broken — goal candy is zeroed by compose.
METHOD_PENALTY_OUTCOME = {
    "fire_no_force": -0.85,
    "fire_on_pullback": -0.75,
    "fire_against_force": -0.90,
    "early_scratch_reverse": -0.70,
    "size_past_risk": -0.80,
}


@dataclass
class AaronProcessLabel:
    """Process target: what the student should *reason*, not a hard live rule."""

    teacher_act: str  # wait | long | short
    teacher_size_frac: float
    process_reward: float
    shape: str
    # force_wait | pullback_wait | continuation_fire | hold_while_force | force_exit_wait
    # | kill_wait | dip_chase_wait | anti_force_wait | thrash_wait
    reason: str
    outcome_score: float = 0.25  # process-shaped prior; negative = method broken
    method_ok: bool = True


def _official(side: int) -> Dict[int, SetConfluence]:
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


def aaron_force_state_from_senses(
    rep: Any,
    *,
    progress_to_target: float = 0.0,
    hold_mode: bool = False,
) -> AaronProcessLabel:
    """Map living sense pack → Force+state process label (train-time only).

    Force = multi-set consensus side (proxy for dual HTF agree).
    Pullback = tension / slingshot without launch → WAIT.
    Continuation = launch/release/continuation with Force → preferred FIRE.
    Hold (scalper) = mid-progress + Force live + continuation → re-commit same side.
    """
    s, f, t, h = rep.sight, rep.feel, rep.taste, rep.hearing
    cons = str(s.get("multi_set_consensus") or "incomplete")
    topo = str(s.get("topology_class") or "chop")
    force_side = 1 if cons == "agree_long" else (-1 if cons == "agree_short" else 0)
    prog = float(np.clip(progress_to_target, 0.0, 1.5))

    # No Force → wait (permission missing). Soft CE so wait does not starve density.
    if force_side == 0:
        return AaronProcessLabel(
            "wait",
            0.0,
            METHOD_REWARD["force_wait"],
            "force_wait",
            "no_force_permission_wait",
            outcome_score=0.1,
        )
    # Kill / collapse → Force thesis dying → exit new commitments (Aaron t5)
    if f.get("collapse") or h.get("wait_subtype") == "kill":
        return AaronProcessLabel(
            "wait",
            0.0,
            METHOD_REWARD["kill_wait"],
            "force_exit_wait" if prog > 0.15 else "kill_wait",
            "collapse_or_kill_wait",
            outcome_score=0.05,
        )
    # Pullback building, no launch → wait (pullback ≠ fire) — dip-chase is wrong shape
    if f.get("max_tension_load_building") and not f.get("launch"):
        return AaronProcessLabel(
            "wait",
            0.0,
            METHOD_REWARD["dip_chase_wait"] if topo in ("slingshot_load", "chop") else METHOD_REWARD["pullback_wait"],
            "dip_chase_wait" if topo == "slingshot_load" else "pullback_wait",
            "pullback_building_not_continuation",
            outcome_score=0.15,
        )
    if topo == "slingshot_load" and not f.get("launch"):
        return AaronProcessLabel(
            "wait",
            0.0,
            METHOD_REWARD["pullback_wait"],
            "pullback_wait",
            "slingshot_pullback_wait",
            outcome_score=0.15,
        )
    # Patience / noise without continuation shape
    edge = str(t.get("edge_quality") or "noise")
    continuation_ok = bool(
        f.get("launch")
        or topo in ("launch", "release", "continuation")
        or edge == "bread_and_butter"
    )
    # Aaron balance: with Force + cont topology, prefer continuation fire over soft taste block
    if force_side != 0 and topo in ("continuation", "launch", "release") and edge != "noise":
        continuation_ok = True
    if not continuation_ok:
        return AaronProcessLabel(
            "wait",
            0.0,
            METHOD_REWARD["pullback_wait"],
            "pullback_wait",
            "not_continuation_or_taste_block",
            outcome_score=0.1,
        )

    act = "long" if force_side > 0 else "short"
    conv = float(t.get("conviction") or 0.6)

    # Aaron t4 for SCALPER: "hold while Force holds" = re-commit same side on the
    # next short scalp (progressive size), NOT multi-hour bag-holding.
    # Mid-progress under live Force + reclaim → same-side fire with solid size.
    if hold_mode or (0.20 <= prog < 0.90 and continuation_ok and force_side != 0):
        if hold_mode or topo in ("continuation", "release", "launch") or edge == "bread_and_butter":
            # Progressive size-up with progress (far from clear → larger fraction)
            size = float(np.clip(0.42 + 0.40 * conv + 0.12 * prog, 0.40, 0.92))
            return AaronProcessLabel(
                act,
                size,
                METHOD_REWARD["hold_while_force"],
                "hold_while_force",
                "scalp_recommit_while_force_t4",
                outcome_score=float(np.clip(0.35 + 0.4 * prog, 0.35, 0.85)),
            )

    # Continuation with Force → fire (strong process reward — method that clears)
    rew = METHOD_REWARD["continuation_fire"]
    if f.get("launch") and edge == "bread_and_butter":
        rew = 1.75
    elif topo == "continuation":
        rew = 1.60
    size = float(np.clip(0.48 + 0.48 * conv, 0.38, 0.98))
    return AaronProcessLabel(
        act,
        size,
        rew,
        "continuation_fire",
        "continuation_with_force_fire",
        outcome_score=0.40,
    )


def method_penalty_label(
    *,
    kind: str,
    force_side: int = 0,
) -> AaronProcessLabel:
    """Teacher for *broken method* states: WAIT + strong process reward (anti fire).

    outcome_score negative so outcome-shaped paths do not candy goal progress
    when method is broken (PKG-005 method first).
    """
    oc = float(METHOD_PENALTY_OUTCOME.get(kind, -0.6))
    if kind == "fire_against_force" and force_side != 0:
        # Correct act is Force side if continuation would be valid — but penalty path teaches WAIT
        # until continuation; never anti-force.
        return AaronProcessLabel(
            "wait",
            0.0,
            METHOD_REWARD["anti_force_wait"],
            "anti_force_wait",
            f"penalty_{kind}",
            outcome_score=oc,
            method_ok=False,
        )
    return AaronProcessLabel(
        "wait",
        0.0,
        METHOD_REWARD["thrash_wait"] if "thrash" in kind or kind == "fire_no_force" else METHOD_REWARD["dip_chase_wait"],
        "thrash_wait" if kind == "fire_no_force" else "dip_chase_wait",
        f"penalty_{kind}",
        outcome_score=oc,
        method_ok=False,
    )


def sample_aaron_episode(
    rng: np.random.Generator,
    *,
    target: Optional[float] = None,
    risk: Optional[float] = None,
    scenario: Optional[str] = None,
) -> Tuple[np.ndarray, AaronProcessLabel]:
    """Synthetic Force+state episode for offline process training (method-rich)."""
    if target is None:
        target = float(rng.choice([5.0, 15.0, 30.0, 50.0, 70.0, 90.0]))
    if risk is None:
        risk = float(rng.choice([1.0, 2.0, 3.0]))
    scen = scenario or str(
        rng.choice(
            [
                "no_force",
                "pullback_wait",
                "continuation_fire",
                "continuation_fire",
                "hold_while_force",
                "hold_while_force",
                "dip_chase",
                "force_exit",
                "collapse",
                "conflict",
            ]
        )
    )
    side = int(rng.choice([-1, 1]))
    hold_mode = False
    progress = 0.0
    if scen == "no_force":
        inp = MarketSenseInput(
            htf_force=[0.2, -0.2, 0.1, -0.1, 0.0, 0.0, 0.05, -0.05],
            ltf_velocity=[0.0] * 4,
            inertia=[0.0] * 4,
            inertia_baseline=[0.0] * 4,
            velocity_baseline=[0.0] * 4,
            regime="chop",
            set_conflict=True,
            cross_family_agree=False,
            composition_has_force=False,
            target_percent=target,
            max_daily_risk_percent=risk,
        )
        side = 0
        lab_override: Optional[AaronProcessLabel] = method_penalty_label(kind="fire_no_force")
    elif scen == "dip_chase":
        # Bad path A: Force + pullback bottom — teacher WAIT (not fire)
        progress = float(rng.uniform(0.0, 0.2))
        inp = MarketSenseInput(
            htf_force=[0.8 * side] * 8,
            ltf_velocity=[-0.65 * side] * 4,
            inertia=[0.7 * side] * 4,
            inertia_baseline=[0.35 * side] * 4,
            velocity_baseline=[0.05 * side] * 4,
            full_body_outside_rails=True,
            ltf_inside_tight=True,
            efficiency=0.45,
            regime="bull" if side > 0 else "bear",
            g_fixed=True,
            composition_has_force=True,
            composition_has_velocity=True,
            cross_family_agree=True,
            target_percent=target,
            max_daily_risk_percent=risk,
            progress_to_target=progress,
        )
        lab_override = method_penalty_label(kind="fire_on_pullback", force_side=side)
    elif scen == "pullback_wait":
        progress = float(rng.uniform(0.0, 0.35))
        inp = MarketSenseInput(
            htf_force=[0.75 * side] * 8,
            ltf_velocity=[-0.55 * side] * 4,
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
            progress_to_target=progress,
        )
        lab_override = None
    elif scen == "force_exit":
        # Force dying mid-day after some progress — stop new thrash fire
        progress = float(rng.uniform(0.25, 0.65))
        inp = MarketSenseInput(
            htf_force=[0.15 * side, -0.2 * side, 0.1, -0.1, 0.0, 0.05, -0.05, 0.0],
            ltf_velocity=[-0.3 * side] * 4,
            inertia=[-0.4 * side] * 4,
            inertia_baseline=[0.1 * side] * 4,
            velocity_baseline=[0.0] * 4,
            g_flip=True,
            g_fixed=False,
            efficiency=0.25,
            regime="vol_shock",
            set_conflict=True,
            composition_has_force=False,
            composition_has_velocity=True,
            target_percent=target,
            max_daily_risk_percent=risk,
            progress_to_target=progress,
            realized_risk_percent=float(risk * 0.35),
        )
        side = 0
        lab_override = AaronProcessLabel(
            "wait",
            0.0,
            METHOD_REWARD["force_exit_wait"],
            "force_exit_wait",
            "force_died_exit_new_commits",
            outcome_score=0.1,
        )
    elif scen == "collapse":
        progress = float(rng.uniform(0.1, 0.5))
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
            progress_to_target=progress,
        )
        lab_override = None
    elif scen == "conflict":
        inp = MarketSenseInput(
            htf_force=[0.6, 0.5, -0.55, -0.5, 0.2, 0.1, -0.3, -0.2],
            ltf_velocity=[0.1, -0.1, 0.0, 0.05],
            inertia=[0.1, -0.1, 0.0, 0.0],
            inertia_baseline=[0.0] * 4,
            velocity_baseline=[0.0] * 4,
            regime="chop",
            set_conflict=True,
            cross_family_agree=False,
            composition_has_force=True,
            target_percent=target,
            max_daily_risk_percent=risk,
        )
        side = 0
        lab_override = method_penalty_label(kind="fire_no_force")
    elif scen == "hold_while_force":
        # Aaron t4: mid-progress, Force still live, continuation — HOLD same side
        hold_mode = True
        progress = float(rng.uniform(0.28, 0.72))
        inp = MarketSenseInput(
            htf_force=[0.85 * side] * 8,
            ltf_velocity=[0.5 * side] * 4,
            inertia=[0.75 * side] * 4,
            inertia_baseline=[0.4 * side] * 4,
            velocity_baseline=[0.25 * side] * 4,
            efficiency=0.8,
            regime="bull" if side > 0 else "bear",
            g_fixed=True,
            composition_has_force=True,
            composition_has_velocity=True,
            cross_family_agree=True,
            target_percent=target,
            max_daily_risk_percent=risk,
            progress_to_target=progress,
            realized_risk_percent=float(rng.uniform(0.0, risk * 0.35)),
        )
        lab_override = None
    else:  # continuation_fire
        progress = float(rng.uniform(0.0, 0.35))
        inp = MarketSenseInput(
            htf_force=[0.8 * side] * 8,
            ltf_velocity=[0.55 * side] * 4,
            inertia=[0.7 * side] * 4,
            inertia_baseline=[0.35 * side] * 4,
            velocity_baseline=[0.2 * side] * 4,
            efficiency=0.75,
            regime="bull" if side > 0 else "bear",
            g_fixed=True,
            composition_has_force=True,
            composition_has_velocity=True,
            cross_family_agree=True,
            target_percent=target,
            max_daily_risk_percent=risk,
            progress_to_target=progress,
            realized_risk_percent=float(rng.uniform(0.0, risk * 0.25)),
        )
        lab_override = None

    rep = probe_all_senses(inp)
    if lab_override is not None:
        lab = lab_override
    else:
        lab = aaron_force_state_from_senses(
            rep,
            progress_to_target=float(inp.progress_to_target),
            hold_mode=hold_mode,
        )
    st = build_meta_rl_state(
        target_percent=float(inp.target_percent),
        max_daily_risk_percent=float(inp.max_daily_risk_percent),
        official=_official(side if side != 0 else 1),
        structure=StructureFlags(
            pullback=str(rep.sight.get("topology_class")) == "slingshot_load"
            or scen in ("pullback_wait", "dip_chase"),
            scale_conflict=scen in ("conflict", "no_force", "force_exit"),
        ),
        sense_report=rep,
        progress_to_target=float(inp.progress_to_target),
        realized_risk_percent=float(inp.realized_risk_percent),
        session_phase=float(rng.uniform(0.3, 0.85)),
    )
    assert st.shape[0] == META_RL_DIM
    assert st[SENSE_STATE_SLICE].shape[0] == SENSE_PACK_DIM
    return st, lab


def train_aaron_reason_curriculum(
    brain: Any,
    *,
    steps: int = 3000,
    seed: int = 42,
    lr: float = 0.016,
    staged: bool = True,
    continuation_heavy: bool = False,
    method_rich: bool = False,
) -> Dict[str, Any]:
    """Offline: reward correct Force+state *process*, not path-side copy alone.

    ``staged=True`` (Aaron method-first): Force-wait → pullback-wait → continuation-fire → mixed.
    ``method_rich=True``: full Aaron path — Force → pullback → continuation → hold while Force
    → exit when Force dies + dip-chase / thrash penalties (AARON.md).
    ``continuation_heavy=True``: almost all continuation_fire (density-safe method seal).
    """
    if getattr(brain, "frozen_for_inference", False):
        brain.unlock_for_meta_train()
    rng = np.random.default_rng(seed)
    shape_counts: Dict[str, int] = {}
    losses: List[float] = []
    penalty_counts: Dict[str, int] = {}

    def _step(scenario: Optional[str], i: int, stage_lr: float) -> None:
        st, lab = sample_aaron_episode(rng, scenario=scenario)
        # Method first, goal second: compose process + outcome; zero candy if method broken
        method = float(lab.process_reward)
        if not lab.method_ok:
            method = max(method, 1.25)  # keep anti-fire WAIT teaching strong
            penalty_counts[lab.reason] = penalty_counts.get(lab.reason, 0) + 1
        composed = compose_method_goal_reward(
            method,
            outcome_score=float(lab.outcome_score),
            method_ok=bool(lab.method_ok),
        )
        reward = float(composed["total"])
        loss = brain.meta_update(
            st,
            teacher_act=lab.teacher_act,
            lr=stage_lr * (0.97 ** (i // 200)),
            reward=reward,
            teacher_size_frac=float(lab.teacher_size_frac),
        )
        losses.append(float(loss))
        shape_counts[lab.shape] = shape_counts.get(lab.shape, 0) + 1

    n = max(1, int(steps))
    if method_rich and n >= 50:
        # Aaron curriculum stages 1–5 method-rich (hold is stage after continuation)
        # Force 12% · pullback+dip 15% · continuation 28% · Hold 28% · Exit/penalty 10% · mixed 7%
        n_f = max(1, int(n * 0.12))
        n_l = max(1, int(n * 0.15))
        n_r = max(1, int(n * 0.28))
        n_h = max(1, int(n * 0.28))
        n_x = max(1, int(n * 0.10))
        n_m = max(1, n - n_f - n_l - n_r - n_h - n_x)
        i = 0
        for _ in range(n_f):
            _step(str(rng.choice(["no_force", "conflict"])), i, lr * 0.95)
            i += 1
        for _ in range(n_l):
            _step(str(rng.choice(["pullback_wait", "dip_chase", "dip_chase", "pullback_wait"])), i, lr)
            i += 1
        for _ in range(n_r):
            _step("continuation_fire", i, lr * 1.12)
            i += 1
        for _ in range(n_h):
            _step("hold_while_force", i, lr * 1.18)  # strongest pull: hold winners
            i += 1
        for _ in range(n_x):
            _step(str(rng.choice(["force_exit", "collapse", "no_force"])), i, lr * 1.05)
            i += 1
        for _ in range(n_m):
            scen = str(
                rng.choice(
                    [
                        "hold_while_force",
                        "continuation_fire",
                        "pullback_wait",
                        "dip_chase",
                        "no_force",
                    ]
                )
            )
            _step(scen, i, lr)
            i += 1
        stages = {
            "force_wait_steps": n_f,
            "pullback_wait_steps": n_l,
            "continuation_fire_steps": n_r,
            "hold_while_force_steps": n_h,
            "force_exit_penalty_steps": n_x,
            "mixed_steps": n_m,
            "method_rich": True,
        }
    elif continuation_heavy and n >= 20:
        n_r = max(1, int(n * 0.80))
        n_l = max(1, int(n * 0.12))
        n_f = max(1, n - n_r - n_l)
        i = 0
        for _ in range(n_f):
            _step("no_force", i, lr * 0.9)
            i += 1
        for _ in range(n_l):
            _step("pullback_wait", i, lr * 0.95)
            i += 1
        for _ in range(n_r):
            _step("continuation_fire", i, lr * 1.15)
            i += 1
        stages = {
            "force_wait_steps": n_f,
            "pullback_wait_steps": n_l,
            "continuation_fire_steps": n_r,
            "mixed_steps": 0,
            "continuation_heavy": True,
        }
    elif staged and n >= 40:
        n_f = max(1, int(n * 0.15))
        n_l = max(1, int(n * 0.15))
        n_r = max(1, int(n * 0.55))
        n_m = max(1, n - n_f - n_l - n_r)
        i = 0
        for _ in range(n_f):
            _step(str(rng.choice(["no_force", "conflict"])), i, lr * 0.95)
            i += 1
        for _ in range(n_l):
            _step(str(rng.choice(["pullback_wait", "collapse"])), i, lr * 0.95)
            i += 1
        for _ in range(n_r):
            _step("continuation_fire", i, lr * 1.12)
            i += 1
        for _ in range(n_m):
            scen = str(rng.choice(["continuation_fire", "continuation_fire", "pullback_wait", "no_force"]))
            _step(scen, i, lr)
            i += 1
        stages = {
            "force_wait_steps": n_f,
            "pullback_wait_steps": n_l,
            "continuation_fire_steps": n_r,
            "mixed_steps": n_m,
        }
    else:
        for i in range(n):
            _step(None, i, lr)
        stages = {"mixed_only": n}

    brain.trained = True
    return {
        "law": "AARON_FORCE_STATE_CURRICULUM",
        "steps": n,
        "staged": bool(staged),
        "method_rich": bool(method_rich),
        "stages": stages,
        "mean_loss": float(np.mean(losses)) if losses else float("nan"),
        "shape_counts": shape_counts,
        "penalty_counts": penalty_counts,
        "method_rewards": dict(METHOD_REWARD),
        "meta_train_steps": int(getattr(brain, "meta_train_steps", 0)),
        "method": (
            "Force→pullback→continuation→hold method-rich (Aaron)"
            if method_rich
            else "Force→pullback→continuation staged process (method-first, not answer-copy)"
        ),
        "has_hold_shape": "hold_while_force" in shape_counts,
    }

# Deprecated alias (old name)
aaron_flr_from_senses = aaron_force_state_from_senses
