"""Execute arbitration 2× CLEAR ROAD: outcome harvest → train → floor dual.

Lab only. Does not replace production champion without promote_guard + Court.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import numpy as np

from .forward_eval import run_forward_eval
from .l2l_process import train_l2l_process_curriculum
from .path_learning import (
    FLOOR_100D,
    apply_outcome_tagged_path_teachers,
    path_learning_promote_guard,
    path_reanchor,
    stamp_path_teacher_day_outcome,
    train_path_learning_curriculum,
)
from .path_state_harvest import (
    filter_path_state_teachers,
    harvest_path_state_teachers,
    save_path_state_pack,
)
from .policy import DEFAULT_CHAMPION_PATH, MetaPolicy

ART = Path("evidence_court/artifacts")
SHADOW = ART / "meta_policy_2x_clear_road.npz"
SHADOW_JSON = ART / "meta_policy_2x_clear_road.json"
REPORT = ART / "execute_2x_clear_road_report.json"
OUTCOME_PACK = ART / "path_state_teachers_outcome_2x.json"
BASE_PACK = ART / "path_state_teachers_case0037.json"

# Arbitration targets
MILESTONE_A = {"hits": 15, "a13_frac": 0.64}
TARGET_2X = {"hits": 22, "low_hr": 0.50, "a13_frac": 0.85, "n_zero": 9, "breach": 0}


def _load_or_harvest_outcome_pack(
    *,
    harvest_days: int = 25,
    seed: int = 42,
    force_harvest: bool = False,
) -> Dict[str, Any]:
    """Harvest outcome-tagged path teachers, or enrich existing pack with defaults."""
    if not force_harvest and OUTCOME_PACK.exists():
        pack = json.loads(OUTCOME_PACK.read_text(encoding="utf-8"))
        if pack.get("examples") and any(
            e.get("outcome_tagged") for e in pack["examples"][:20]
        ):
            return pack

    print(f"[2x] harvest outcome-tagged path teachers days={harvest_days}…", flush=True)
    pack = harvest_path_state_teachers(
        n_days=int(harvest_days),
        seed=seed,
        max_examples=900,
        max_per_day=80,
        require_htf_active=True,
        watch_enabled=False,
    )
    # ensure stamps (harvest should already stamp)
    exs = []
    for ex in pack.get("examples") or []:
        if not ex.get("outcome_tagged"):
            ex = stamp_path_teacher_day_outcome(
                ex,
                day_pnl=float(ex.get("realized_pnl") or 0.5),
                target_percent=float(ex.get("harvest_day_target") or 15.0),
                max_daily_risk_percent=float(ex.get("harvest_day_risk") or 2.0),
                n_trades=int(ex.get("harvest_day_n_trades") or 1),
            )
        exs.append(ex)
    pack["examples"] = exs
    pack["n_outcome_tagged"] = sum(1 for e in exs if e.get("outcome_tagged"))
    pack["law"] = "PATH_OUTCOME_2X_CLEAR_ROAD"
    save_path_state_pack(pack, OUTCOME_PACK)
    return pack


def _forward_summary(rep: Any) -> Dict[str, Any]:
    days = list(rep.day_results or [])
    n = len(days)
    hits = sum(1 for d in days if d.hit_target)
    n_zero = sum(1 for d in days if int(d.n_trades) == 0)
    a13_ok = sum(1 for d in days if 8 <= int(d.n_trades) <= 400)
    green = sum(1 for d in days if float(d.pnl_percent) > 0)
    gc = (rep.metadata or {}).get("goal_consistency") or {}
    return {
        "protocol": "forward100_class",
        "n_days": n,
        "hits": hits,
        "hit_rate": hits / max(n, 1),
        "low_hr": float(gc.get("low_hit_rate") or 0.0),
        "a13_frac": a13_ok / max(n, 1),
        "a13_every_day": a13_ok == n and n > 0,
        "n_zero": n_zero,
        "breach_count": int(rep.breach_count),
        "breach": int(rep.breach_count) > 0,
        "mean_tr": float(np.mean([d.n_trades for d in days])) if days else 0.0,
        "mean_pnl": float(np.mean([d.pnl_percent for d in days])) if days else 0.0,
        "green_days": green,
        "weights_frozen": bool(rep.no_retrain),
        "no_retrain": bool(rep.no_retrain),
        "fingerprint": (rep.metadata or {}).get("policy_fingerprint"),
        "goal_consistency": gc,
    }


def run_2x_clear_road(
    *,
    harvest_days: int = 25,
    curriculum_steps: int = 2800,
    process_steps: int = 500,
    reanchor_passes: int = 2,
    dual_days: int = 100,
    seed: int = 42,
    force_harvest: bool = False,
) -> Dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    report: Dict[str, Any] = {
        "law": "ARBITRATION_2X_CLEAR_ROAD",
        "doc": "evidence_court/ARBITRATION_2X_DETHRONE.md",
        "ts": ts,
        "recipe": "warmstart0037→outcome_path_primary+conversion→light_process→path_reanchor_last→freeze→forward100",
        "milestone_A": MILESTONE_A,
        "target_2x": TARGET_2X,
        "floor_100d": FLOOR_100D,
    }

    champ_path = Path(DEFAULT_CHAMPION_PATH)
    pol = MetaPolicy.load(champ_path, freeze=False, require_serious=False)
    pol.unlock_for_meta_train()
    report["warmstart_fp"] = pol.weight_fingerprint()

    pack = _load_or_harvest_outcome_pack(
        harvest_days=harvest_days, seed=seed, force_harvest=force_harvest
    )
    labs = filter_path_state_teachers(
        pack.get("examples") or [], max_examples=900, require_htf_active=True
    )
    # also merge base pack stamped with mild positive prior if short harvest
    if BASE_PACK.exists() and len(labs) < 200:
        base = json.loads(BASE_PACK.read_text(encoding="utf-8"))
        for ex in base.get("examples") or []:
            if not ex.get("outcome_tagged"):
                ex = stamp_path_teacher_day_outcome(
                    ex,
                    day_pnl=1.0,
                    target_percent=float(ex.get("harvest_day_target") or 15.0),
                    max_daily_risk_percent=float(ex.get("harvest_day_risk") or 2.0),
                    n_trades=int(ex.get("harvest_day_n_trades") or 8),
                )
            labs.append(ex)
        labs = filter_path_state_teachers(labs, max_examples=900, require_htf_active=True)
    report["n_path_outcome"] = len(labs)
    report["n_outcome_tagged"] = sum(1 for e in labs if e.get("outcome_tagged"))

    # PRIMARY: outcome-tagged path teachers (conversion signal via day clear/dead)
    print(f"[2x] outcome-tagged path apply n={len(labs)}…", flush=True)
    o_apply = apply_outcome_tagged_path_teachers(
        pol.brain, labs, lr=0.02, seed=seed + 1, max_examples=len(labs), n_passes=3
    )
    report["outcome_path_apply"] = o_apply

    # conversion / goal-risk curriculum (PATH_LEARNING mix)
    print(f"[2x] conversion+goal curriculum steps={curriculum_steps}…", flush=True)
    cur = train_path_learning_curriculum(
        pol.brain,
        steps=int(curriculum_steps),
        seed=seed + 5,
        path_examples=labs,
        path_anchor_frac=0.15,
        holdout_frac=0.15,
        process_frac=0.08,
        lr=0.014,
        density_process=True,
    )
    report["curriculum"] = cur

    # light process then re-anchor last
    print(f"[2x] light process steps={process_steps}…", flush=True)
    proc = train_l2l_process_curriculum(
        pol.brain,
        steps=int(process_steps),
        seed=seed + 11,
        holdout_frac=0.15,
        lr=0.008,
        density_mode=True,
    )
    report["process_fire_frac"] = proc.get("fire_frac")

    print(f"[2x] path re-anchor last passes={reanchor_passes}…", flush=True)
    n_ra = path_reanchor(pol.brain, labs, n_passes=int(reanchor_passes), seed=seed + 19)
    o2 = apply_outcome_tagged_path_teachers(
        pol.brain, labs, lr=0.018, seed=seed + 21, max_examples=len(labs), n_passes=1
    )
    report["path_reanchor_updates"] = int(n_ra)
    report["path_reanchor_last"] = True
    report["outcome_reanchor"] = o2

    pol.trained = True
    pol.meta_train_steps = pol.brain.meta_train_steps
    pol.freeze_for_inference()
    pol.assert_frozen()
    fp = pol.weight_fingerprint()
    report["fingerprint"] = fp
    pol.save(SHADOW)
    SHADOW_JSON.write_text(
        json.dumps(
            {
                "fingerprint": fp,
                "meta_train_steps": int(pol.meta_train_steps),
                "law": "ARBITRATION_2X_CLEAR_ROAD",
                "promote": False,
                "warmstart": report["warmstart_fp"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    report["shadow_path"] = str(SHADOW)

    # Floor-class dual (forward100)
    print(f"[2x] forward100-class dual days={dual_days}…", flush=True)
    lab_pol = MetaPolicy.load(SHADOW, freeze=True, require_serious=False)
    rep = run_forward_eval(
        n_days=int(dual_days),
        seed=seed,
        policy=lab_pol,
        use_goal_path=True,
    )
    dual = _forward_summary(rep)
    report["dual"] = dual
    report["dual_protocol"] = "forward100_class_goal_path_multi_sym"

    # champion dual only if dual_days small; for 100d skip re-run king (use floor ref)
    # Still run champ dual only when dual_days <= 40 for speed comparison
    dual_champ = None
    if dual_days <= 40:
        print(f"[2x] forward dual champion days={dual_days}…", flush=True)
        champ_pol = MetaPolicy.load(champ_path, freeze=True, require_serious=False)
        rep_c = run_forward_eval(
            n_days=int(dual_days), seed=seed, policy=champ_pol, use_goal_path=True
        )
        dual_champ = _forward_summary(rep_c)
        report["dual_champion_same_protocol"] = dual_champ

    guard = path_learning_promote_guard(
        dual,
        dual_champ,
        floor=FLOOR_100D,
        path_only_clone=False,
        process_washout=float(dual.get("a13_frac") or 0) < 0.30,
        has_outcome_conversion_mix=True,
        court_promote=False,
    )
    hits = int(dual.get("hits") or 0)
    a13 = float(dual.get("a13_frac") or 0)
    milestone_a = hits >= int(MILESTONE_A["hits"]) and a13 >= float(MILESTONE_A["a13_frac"]) - 1e-12
    hit_2x = (
        hits >= int(TARGET_2X["hits"])
        and a13 >= float(TARGET_2X["a13_frac"]) - 1e-12
        and int(dual.get("n_zero") or 999) <= int(TARGET_2X["n_zero"])
        and int(dual.get("breach_count") or 1) == 0
    )
    report["promote_guard"] = guard
    report["milestone_A_hit"] = bool(milestone_a)
    report["target_2x_hit"] = bool(hit_2x)
    report["production_replace"] = False
    report["production_champion_unchanged"] = True
    report["king_floor_ref"] = FLOOR_100D

    REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {
                "fingerprint": fp,
                "dual": {
                    k: dual.get(k)
                    for k in (
                        "hits",
                        "hit_rate",
                        "low_hr",
                        "a13_frac",
                        "n_zero",
                        "breach_count",
                        "mean_tr",
                        "weights_frozen",
                    )
                },
                "milestone_A_hit": milestone_a,
                "target_2x_hit": hit_2x,
                "production_replace": False,
                "promote_guard": {
                    "promote_lab": guard.get("promote_lab"),
                    "floor_hold": guard.get("floor_hold"),
                    "production_replace": guard.get("production_replace"),
                },
            },
            indent=2,
        ),
        flush=True,
    )
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Execute 2× CLEAR ROAD lab train + dual")
    p.add_argument("--harvest-days", type=int, default=25)
    p.add_argument("--curriculum-steps", type=int, default=2800)
    p.add_argument("--process-steps", type=int, default=500)
    p.add_argument("--reanchor-passes", type=int, default=2)
    p.add_argument("--dual-days", type=int, default=100)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--force-harvest", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)
    run_2x_clear_road(
        harvest_days=int(args.harvest_days),
        curriculum_steps=int(args.curriculum_steps),
        process_steps=int(args.process_steps),
        reanchor_passes=int(args.reanchor_passes),
        dual_days=int(args.dual_days),
        seed=int(args.seed),
        force_harvest=bool(args.force_harvest),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
