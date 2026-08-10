"""LEARN-PHASE COMPACT v2: creative loop until past full 20d window (hits+density).

Does not stop on a13-only. Requires hits past baseline while holding density,
or max rounds with honest no_lift. Lab only. Teacher material offline only.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .l2l_process import train_l2l_process_curriculum
from .path_learning import (
    apply_outcome_shaped_update,
    apply_outcome_tagged_path_teachers,
    conversion_teacher_from_context,
    outcome_score_from_fields,
    path_reanchor,
    sample_conversion_episode,
    stamp_path_teacher_day_outcome,
    train_path_learning_curriculum,
)
from .path_state_harvest import filter_path_state_teachers
from .policy import DEFAULT_CHAMPION_PATH, MetaPolicy
from .state import build_meta_rl_state
from .train_l2l_full import run_north_star_dual
from .types import Direction, SetConfluence, StructureFlags, VelocityStrength

ART = Path("evidence_court/artifacts")
SHADOW = ART / "meta_policy_learn_phase.npz"
SHADOW_JSON = ART / "meta_policy_learn_phase.json"
REPORT = ART / "learn_phase_20d_report.json"
OUTCOME_PACK = ART / "path_state_teachers_outcome_2x.json"
BASE_PACK = ART / "path_state_teachers_case0037.json"

MAX_ROUNDS = 12
DUAL_DAYS = 20

# Creative mode names (Teacher → Counsel → Creator implements)
MODES = (
    "clear_boost_path",  # overweight clear-outcome path teachers
    "day12_drill_15_3",  # 15%/3% hold-convert pressure
    "conversion_flood",  # conversion primary, path sparse
    "hold_r_sustain",  # mid-progress hold teachers
    "anti_thrash_wait",  # wait on dead + conflict more
    "continue_best_lab",  # warmstart last best lab shadow
    "outcome_fire_only",  # only positive-outcome fire path
    "balanced_reanchor",  # classic recipe stronger reanchor
    "high_conv_lr",  # aggressive conversion lr
    "path_then_convert",  # anchors first then convert
    "size_down_risk",  # size_down near floor lessons
    "mixed_creative",  # blend all
)


def _load_outcome_labs(max_examples: int = 900) -> List[Dict[str, Any]]:
    raw: List[Dict[str, Any]] = []
    for p in (OUTCOME_PACK, BASE_PACK):
        if not p.exists():
            continue
        pack = json.loads(p.read_text(encoding="utf-8"))
        for ex in pack.get("examples") or []:
            if not ex.get("outcome_tagged"):
                ex = stamp_path_teacher_day_outcome(
                    ex,
                    day_pnl=float(ex.get("realized_pnl") or 1.0),
                    target_percent=float(ex.get("harvest_day_target") or 15.0),
                    max_daily_risk_percent=float(ex.get("harvest_day_risk") or 2.0),
                    n_trades=int(ex.get("harvest_day_n_trades") or 8),
                )
            raw.append(ex)
    return filter_path_state_teachers(raw, max_examples=max_examples, require_htf_active=True)


def _clear_boost_labs(labs: Sequence[Dict[str, Any]], *, multi: int = 4) -> List[Dict[str, Any]]:
    """Oversample high-outcome / hit teachers (learn clear, not only fire)."""
    out: List[Dict[str, Any]] = list(labs)
    good = [
        ex
        for ex in labs
        if float(ex.get("outcome_score") or 0) >= 0.25 or bool(ex.get("hit_target"))
    ]
    if not good:
        good = list(labs)
    for _ in range(max(1, multi)):
        out.extend(good)
    return out


def is_any_better(lab: Dict[str, Any], base: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """At least one metric better (legacy)."""
    reasons: List[str] = []
    if int(lab.get("breach_count") or 0) != 0:
        return False, ["lab_breach"]
    if not lab.get("weights_frozen", True):
        return False, ["lab_not_frozen"]
    lh, bh = int(lab.get("hits") or 0), int(base.get("hits") or 0)
    la, ba = float(lab.get("a13_frac") or 0), float(base.get("a13_frac") or 0)
    lz, bz = int(lab.get("n_zero") or 0), int(base.get("n_zero") or 0)
    if lh > bh:
        reasons.append(f"hits {lh}>{bh}")
    if la > ba + 1e-12:
        reasons.append(f"a13 {la:.3f}>{ba:.3f}")
    if lz < bz:
        reasons.append(f"n_zero {lz}<{bz}")
    return (len(reasons) > 0), reasons


def is_past_full_window(
    lab: Dict[str, Any],
    base: Dict[str, Any],
    *,
    prior_best: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    """Past the 20d achievement: hits past baseline AND density held vs baseline.

    If prior_best exists (e.g. a13-only lab), also require hits > prior hits
    so we do not stop on density-only win.
    """
    if int(lab.get("breach_count") or 0) != 0:
        return False, ["lab_breach"]
    if not lab.get("weights_frozen", True):
        return False, ["lab_not_frozen"]
    lh, bh = int(lab.get("hits") or 0), int(base.get("hits") or 0)
    la, ba = float(lab.get("a13_frac") or 0), float(base.get("a13_frac") or 0)
    lz, bz = int(lab.get("n_zero") or 0), int(base.get("n_zero") or 0)
    reasons: List[str] = []
    # Must beat hits (conversion) — core of "past the 20 days achieved"
    if lh <= bh:
        return False, [f"hits_not_past {lh}<={bh}"]
    reasons.append(f"hits {lh}>{bh}")
    # Hold density vs baseline (not wash out while chasing hits)
    if la + 1e-12 < ba:
        return False, reasons + [f"a13_regressed {la:.3f}<{ba:.3f}"]
    if lz > bz:
        return False, reasons + [f"n_zero_regressed {lz}>{bz}"]
    if la > ba + 1e-12:
        reasons.append(f"a13 {la:.3f}>={ba:.3f}")
    else:
        reasons.append(f"a13_held {la:.3f}>={ba:.3f}")
    if lz < bz:
        reasons.append(f"n_zero {lz}<{bz}")
    else:
        reasons.append(f"n_zero_held {lz}<={bz}")
    if prior_best is not None:
        ph = int(prior_best.get("hits") or 0)
        if lh <= ph:
            return False, reasons + [f"hits_not_past_prior_best {lh}<={ph}"]
        reasons.append(f"hits_past_prior {lh}>{ph}")
    return True, reasons


def _official(side: int) -> Dict[int, SetConfluence]:
    d = Direction.BULL if side > 0 else Direction.BEAR
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


def train_day12_drill(brain: Any, *, steps: int = 800, seed: int = 7) -> Dict[str, Any]:
    """Creative: pressure 15% target under risk 3% — hold/fire with good outcome, wait thrash."""
    if getattr(brain, "frozen_for_inference", False):
        brain.unlock_for_meta_train()
    rng = np.random.default_rng(seed)
    n_hold = n_fire = n_wait = 0
    for i in range(max(1, steps)):
        side = int(rng.choice([-1, 1]))
        mode = str(rng.choice(["hold", "hold", "fire", "fire", "wait_dead", "size_down"]))
        target, risk = 15.0, 3.0
        if mode == "hold":
            prog, risk_rem = 0.45, 0.55
            ct = conversion_teacher_from_context(
                progress_to_target=prog,
                risk_remaining_frac=risk_rem,
                topology="continuation",
                force_side=side,
                outcome_score=0.55,
            )
            oc = outcome_score_from_fields(
                progress_to_target=prog, hit_target=False, r_capture=0.5, realized_pnl=6.0
            )
            n_hold += 1
        elif mode == "fire":
            prog, risk_rem = 0.12, 0.75
            ct = conversion_teacher_from_context(
                progress_to_target=prog,
                risk_remaining_frac=risk_rem,
                topology="pullback_resume",
                force_side=side,
                outcome_score=0.4,
            )
            oc = outcome_score_from_fields(progress_to_target=prog, r_capture=0.35, realized_pnl=4.0)
            n_fire += 1
        elif mode == "size_down":
            prog, risk_rem = 0.2, 0.28
            ct = conversion_teacher_from_context(
                progress_to_target=prog,
                risk_remaining_frac=risk_rem,
                topology="continuation",
                force_side=side,
                high_target=True,
            )
            oc = 0.15
            n_fire += 1
        else:
            prog, risk_rem = 0.15, 0.7
            ct = conversion_teacher_from_context(
                progress_to_target=prog,
                risk_remaining_frac=risk_rem,
                topology="chop",
                force_side=0,
                conflict=True,
            )
            oc = outcome_score_from_fields(dead_fire=True)
            n_wait += 1
        st = build_meta_rl_state(
            target_percent=target,
            max_daily_risk_percent=risk,
            official=_official(side if ct.teacher_act != "wait" else 1),
            structure=StructureFlags(pullback=mode == "fire", scale_conflict=mode == "wait_dead"),
            progress_to_target=prog,
            realized_risk_percent=risk * (1.0 - risk_rem),
            session_phase=float(rng.uniform(0.35, 0.85)),
        )
        apply_outcome_shaped_update(
            brain,
            st,
            teacher_act=ct.teacher_act,
            outcome_score=oc,
            lr=0.018 * (0.97 ** (i // 100)),
            teacher_size_frac=ct.teacher_size_frac,
            base_reward=1.15 if mode in ("hold", "fire") else 0.9,
        )
    brain.trained = True
    return {"day12_steps": steps, "n_hold": n_hold, "n_fire": n_fire, "n_wait": n_wait}


def train_hold_r_flood(brain: Any, *, steps: int = 600, seed: int = 9) -> int:
    if getattr(brain, "frozen_for_inference", False):
        brain.unlock_for_meta_train()
    rng = np.random.default_rng(seed)
    n = 0
    for i in range(steps):
        st, ct, oc = sample_conversion_episode(rng, holdout_mode=False)
        # Bias: force hold-like when we can
        if ct.class_name != "hold_convert" and rng.random() < 0.5:
            side = 1 if ct.teacher_act == "long" else (-1 if ct.teacher_act == "short" else int(rng.choice([-1, 1])))
            ct = conversion_teacher_from_context(
                progress_to_target=0.5,
                risk_remaining_frac=0.55,
                topology="continuation",
                force_side=side,
                outcome_score=0.5,
            )
            oc = 0.45
        apply_outcome_shaped_update(
            brain,
            st,
            teacher_act=ct.teacher_act,
            outcome_score=oc,
            lr=0.016,
            teacher_size_frac=ct.teacher_size_frac,
        )
        n += 1
    return n


def train_one_round(
    *,
    round_i: int,
    labs: Sequence[Dict[str, Any]],
    seed: int,
    warmstart_path: Optional[Path] = None,
    mode: Optional[str] = None,
) -> Tuple[MetaPolicy, str]:
    """Creative learn-not-copy recipe by mode."""
    mode = mode or MODES[int(round_i) % len(MODES)]
    ws = Path(warmstart_path) if warmstart_path and Path(warmstart_path).exists() else Path(DEFAULT_CHAMPION_PATH)
    if mode == "continue_best_lab" and SHADOW.exists():
        ws = SHADOW
    pol = MetaPolicy.load(ws, freeze=False, require_serious=False)
    pol.unlock_for_meta_train()

    use_labs = list(labs)
    if mode in ("clear_boost_path", "outcome_fire_only", "mixed_creative"):
        use_labs = _clear_boost_labs(labs, multi=5 if mode == "clear_boost_path" else 3)
    if mode == "outcome_fire_only":
        use_labs = [
            ex
            for ex in use_labs
            if float(ex.get("outcome_score") or 0) >= 0.15
            and str(ex.get("teacher_act")) in ("long", "short")
        ] or use_labs

    path_passes = 1 if mode in ("conversion_flood", "day12_drill_15_3") else 2
    if mode in ("balanced_reanchor", "path_then_convert"):
        path_passes = 3
    cur_steps = 800 if mode == "day12_drill_15_3" else 1400 + round_i * 200
    if mode == "conversion_flood":
        cur_steps = 2200 + round_i * 150
    if mode == "high_conv_lr":
        cur_steps = 1800
    path_frac = 0.08 if mode in ("conversion_flood", "day12_drill_15_3") else 0.16
    if mode == "path_then_convert":
        path_frac = 0.28
    conv_lr = 0.022 if mode == "high_conv_lr" else 0.014
    proc_steps = 200 if mode == "anti_thrash_wait" else 350

    # Order varies by mode
    if mode == "path_then_convert":
        apply_outcome_tagged_path_teachers(
            pol.brain, use_labs, lr=0.02, seed=seed + round_i, n_passes=path_passes, max_examples=len(use_labs)
        )
        train_path_learning_curriculum(
            pol.brain,
            steps=cur_steps,
            seed=seed + 11 + round_i,
            path_examples=use_labs,
            path_anchor_frac=path_frac,
            holdout_frac=0.2,
            process_frac=0.05,
            lr=conv_lr,
            density_process=True,
        )
    else:
        if mode != "day12_drill_15_3":
            apply_outcome_tagged_path_teachers(
                pol.brain,
                use_labs,
                lr=0.02,
                seed=seed + round_i * 3,
                max_examples=len(use_labs),
                n_passes=path_passes,
            )
        train_path_learning_curriculum(
            pol.brain,
            steps=int(cur_steps),
            seed=seed + 11 + round_i,
            path_examples=use_labs,
            path_anchor_frac=float(path_frac),
            holdout_frac=0.2,
            process_frac=0.06 if mode != "anti_thrash_wait" else 0.14,
            lr=float(conv_lr),
            density_process=True,
        )

    if mode in ("day12_drill_15_3", "mixed_creative", "size_down_risk"):
        train_day12_drill(pol.brain, steps=900 + round_i * 50, seed=seed + 50 + round_i)
    if mode in ("hold_r_sustain", "mixed_creative", "conversion_flood"):
        train_hold_r_flood(pol.brain, steps=500 + round_i * 40, seed=seed + 60 + round_i)

    train_l2l_process_curriculum(
        pol.brain,
        steps=int(proc_steps),
        seed=seed + 21 + round_i,
        holdout_frac=0.15,
        lr=0.007 if mode != "anti_thrash_wait" else 0.01,
        density_mode=True,
    )

    # Path re-anchor last (anti-washout) — always
    re_pass = 3 if mode in ("balanced_reanchor", "clear_boost_path") else 2
    path_reanchor(pol.brain, labs, n_passes=re_pass, seed=seed + 31 + round_i)
    apply_outcome_tagged_path_teachers(
        pol.brain,
        _clear_boost_labs(labs, multi=2) if mode == "clear_boost_path" else labs,
        lr=0.017,
        seed=seed + 41 + round_i,
        max_examples=len(labs),
        n_passes=1,
    )

    pol.trained = True
    pol.meta_train_steps = pol.brain.meta_train_steps
    pol.freeze_for_inference()
    pol.assert_frozen()
    return pol, mode


def run_learn_phase(
    *,
    dual_days: int = DUAL_DAYS,
    max_rounds: int = MAX_ROUNDS,
    seed: int = 42,
    require_full_window: bool = True,
) -> Dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    report: Dict[str, Any] = {
        "law": "ARBITRATION_LEARN_PHASE_V2",
        "doc": "evidence_court/ARBITRATION_LEARN_PHASE.md",
        "ts": ts,
        "dual_days": dual_days,
        "max_rounds": max_rounds,
        "protocol": f"north_star_random_TxR_XAU_15m_n{dual_days}",
        "require_full_window": bool(require_full_window),
        "stop_rule": "past_full_window_hits_and_density" if require_full_window else "any_better",
        "learn_not_copy": True,
        "teacher_channel": "Counsel_only",
        "creative_modes": list(MODES),
        "rounds": [],
        "production_replace": False,
    }

    champ_path = Path(DEFAULT_CHAMPION_PATH)
    labs = _load_outcome_labs()
    report["n_path_labs"] = len(labs)
    if not labs:
        report["error"] = "no_path_labs"
        REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report

    print(f"[learn-phase] baseline dual days={dual_days} seed={seed}…", flush=True)
    base = run_north_star_dual(champ_path, n_days=dual_days, seed=seed)
    report["baseline"] = {
        k: base.get(k)
        for k in (
            "hits",
            "hit_rate",
            "a13_frac",
            "n_zero",
            "breach_count",
            "mean_tr",
            "mean_pnl",
            "weights_frozen",
            "fingerprint",
            "eval_start",
            "eval_end",
        )
    }

    past_full = False
    any_better = False
    best_lab: Optional[Dict[str, Any]] = None
    best_score = -1e9
    best_reasons: List[str] = []
    prior_best_lab: Optional[Dict[str, Any]] = None

    def _score(lab: Dict[str, Any]) -> float:
        # Prefer hits, then a13, then fewer zeros
        return (
            100.0 * int(lab.get("hits") or 0)
            + 10.0 * float(lab.get("a13_frac") or 0)
            - 0.5 * int(lab.get("n_zero") or 0)
            + 0.01 * float(lab.get("mean_pnl") or 0)
        )

    for r in range(int(max_rounds)):
        mode = MODES[r % len(MODES)]
        print(f"[learn-phase] round {r+1}/{max_rounds} mode={mode} train…", flush=True)
        warm = SHADOW if (prior_best_lab is not None and mode == "continue_best_lab") else None
        pol, mode_used = train_one_round(
            round_i=r, labs=labs, seed=seed, warmstart_path=warm, mode=mode
        )
        pol.save(SHADOW)
        fp = pol.weight_fingerprint()
        SHADOW_JSON.write_text(
            json.dumps(
                {
                    "fingerprint": fp,
                    "meta_train_steps": int(pol.meta_train_steps),
                    "law": "ARBITRATION_LEARN_PHASE_V2",
                    "round": r + 1,
                    "mode": mode_used,
                    "promote": False,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"[learn-phase] round {r+1} dual days={dual_days}…", flush=True)
        lab = run_north_star_dual(SHADOW, n_days=dual_days, seed=seed)
        lab_sum = {
            k: lab.get(k)
            for k in (
                "hits",
                "hit_rate",
                "a13_frac",
                "n_zero",
                "breach_count",
                "mean_tr",
                "mean_pnl",
                "weights_frozen",
            )
        }
        better, b_reasons = is_any_better(lab, base)
        full_ok, f_reasons = is_past_full_window(lab, base, prior_best=prior_best_lab)
        sc = _score(lab_sum)
        row = {
            "round": r + 1,
            "mode": mode_used,
            "fingerprint": fp,
            "lab": lab_sum,
            "any_better": better,
            "any_better_reasons": b_reasons,
            "past_full_window": full_ok,
            "past_full_reasons": f_reasons,
            "score": sc,
        }
        report["rounds"].append(row)
        print(json.dumps(row, indent=2, default=str), flush=True)

        if better:
            any_better = True
        if sc > best_score and int(lab_sum.get("breach_count") or 0) == 0:
            best_score = sc
            best_lab = lab_sum
            best_reasons = f_reasons if full_ok else b_reasons
            prior_best_lab = dict(lab_sum)

        if require_full_window and full_ok:
            past_full = True
            report["stop_reason"] = "past_full_20d_window"
            report["winning_round"] = r + 1
            report["winning_mode"] = mode_used
            break
        if not require_full_window and better:
            report["stop_reason"] = "any_better"
            report["winning_round"] = r + 1
            break
    else:
        report["stop_reason"] = (
            "max_rounds_no_full_window" if require_full_window else "max_rounds_no_lift"
        )

    report["any_better"] = bool(any_better)
    report["past_full_window"] = bool(past_full)
    report["best_lab"] = best_lab
    report["best_reasons"] = best_reasons
    report["shadow_path"] = str(SHADOW)
    report["production_champion_unchanged"] = True
    report["production_replace"] = False
    report["phase_note"] = (
        "20d phase only — past_full_window requires hits>baseline + density held; not 100d PROMOTE"
    )

    REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {
                "any_better": any_better,
                "past_full_window": past_full,
                "stop_reason": report.get("stop_reason"),
                "baseline": report["baseline"],
                "best_lab": best_lab,
                "best_reasons": best_reasons,
                "winning_mode": report.get("winning_mode"),
                "production_replace": False,
            },
            indent=2,
        ),
        flush=True,
    )
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Creative learn-phase 20d until past full window")
    p.add_argument("--dual-days", type=int, default=DUAL_DAYS)
    p.add_argument("--max-rounds", type=int, default=MAX_ROUNDS)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--any-better-stop",
        action="store_true",
        help="Stop on any metric better (old rule); default is past full window",
    )
    args = p.parse_args(list(argv) if argv is not None else None)
    run_learn_phase(
        dual_days=int(args.dual_days),
        max_rounds=int(args.max_rounds),
        seed=int(args.seed),
        require_full_window=not bool(args.any_better_stop),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
