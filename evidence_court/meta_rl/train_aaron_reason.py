"""Aaron method-first FLR train + dual; dethrone only if floor bar holds.

Recipe (double-loop): light path → staged FLR → density seal → short FLR seal.
Monty EO intelligent size-up remains in goal_path at dual (path law).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from .aaron_reason_curriculum import train_aaron_reason_curriculum
from .forward_eval import run_forward_eval
from .path_learning import (
    FLOOR_100D,
    apply_outcome_tagged_path_teachers,
    path_reanchor,
    stamp_path_teacher_day_outcome,
)
from .path_state_harvest import filter_path_state_teachers
from .policy import DEFAULT_CHAMPION_PATH, MetaPolicy
from .train_l2l_full import run_north_star_dual

ART = Path("evidence_court/artifacts")
SHADOW = ART / "meta_policy_aaron_reason.npz"
SHADOW_JSON = ART / "meta_policy_aaron_reason.json"
REPORT = ART / "aaron_reason_train_report.json"
BASE_PACK = ART / "path_state_teachers_case0037.json"
OUTCOME_PACK = ART / "path_state_teachers_outcome_2x.json"


def _labs(max_n: int = 700):
    raw = []
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
    return filter_path_state_teachers(raw, max_examples=max_n, require_htf_active=True)


def _floor_summary(rep: Any) -> Dict[str, Any]:
    days = list(rep.day_results or [])
    n = len(days)
    hits = sum(1 for d in days if d.hit_target)
    n_zero = sum(1 for d in days if int(d.n_trades) == 0)
    a13 = sum(1 for d in days if 8 <= int(d.n_trades) <= 400) / max(n, 1)
    gc = (rep.metadata or {}).get("goal_consistency") or {}
    return {
        "protocol": "forward100_class",
        "n_days": n,
        "hits": hits,
        "hit_rate": hits / max(n, 1),
        "low_hr": float(gc.get("low_hit_rate") or 0.0),
        "a13_frac": a13,
        "n_zero": n_zero,
        "breach_count": int(rep.breach_count),
        "mean_tr": float(sum(d.n_trades for d in days) / max(n, 1)) if days else 0.0,
        "mean_pnl": float(sum(d.pnl_percent for d in days) / max(n, 1)) if days else 0.0,
        "weights_frozen": bool(rep.no_retrain),
        "fingerprint": (rep.metadata or {}).get("policy_fingerprint"),
    }


def dethrone_decision(lab: Dict[str, Any], floor: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Dethrone = hits > floor hits AND a13>=floor AND n_zero<=floor AND breach0 AND frozen."""
    floor = floor or FLOOR_100D
    hits = int(lab.get("hits") or 0)
    a13 = float(lab.get("a13_frac") or 0.0)
    n_zero = int(lab.get("n_zero") or 999)
    breach = int(lab.get("breach_count") or 0)
    frozen = bool(lab.get("weights_frozen", True))
    fh = int(floor.get("hits") or 11)
    fa = float(floor.get("a13_frac") or 0.64)
    fz = int(floor.get("n_zero") or 18)
    beats_hits = hits > fh
    holds_a13 = a13 + 1e-12 >= fa
    holds_zero = n_zero <= fz
    ok = beats_hits and holds_a13 and holds_zero and breach == 0 and frozen
    blockers = []
    if not beats_hits:
        blockers.append(f"hits {hits}<={fh}")
    if not holds_a13:
        blockers.append(f"a13 {a13:.3f}<{fa}")
    if not holds_zero:
        blockers.append(f"n_zero {n_zero}>{fz}")
    if breach:
        blockers.append(f"breach={breach}")
    if not frozen:
        blockers.append("not_frozen")
    return {
        "dethrone": bool(ok),
        "beats_hits": beats_hits,
        "holds_a13": holds_a13,
        "holds_n_zero": holds_zero,
        "breach0": breach == 0,
        "frozen": frozen,
        "blockers": blockers,
        "floor": floor,
        "lab": {"hits": hits, "a13_frac": a13, "n_zero": n_zero, "breach_count": breach},
    }


def run_aaron_reason_train(
    *,
    flr_steps: int = 4000,
    dual_days: int = 20,
    seed: int = 42,
    floor_dual: bool = False,
    floor_days: int = 100,
    warmstart_shadow: bool = False,
    density_boost: bool = False,
) -> Dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    report: Dict[str, Any] = {
        "law": "AARON_FORCE_STATE_DETHRONE",
        "package": "Aaron_here/packages/PKG-005_meta_rl_method_first_policy.md",
        "lesson": "Learning-How_to/0002_Method_First_Force_Load_Reclaim_For_Future.md",
        "ts": ts,
        "method": "Force→Load→Reclaim staged; path density; method-first seal; EO size-up at dual",
        "teacher": "@Aaron_here",
        "production_replace": False,
        "floor_100d": FLOOR_100D,
    }
    champ = Path(DEFAULT_CHAMPION_PATH)

    print(f"[Aaron] baseline dual days={dual_days}…", flush=True)
    base = run_north_star_dual(champ, n_days=dual_days, seed=seed)
    report["baseline_window"] = {
        k: base.get(k)
        for k in (
            "hits",
            "a13_frac",
            "n_zero",
            "breach_count",
            "mean_tr",
            "mean_pnl",
            "fingerprint",
            "weights_frozen",
        )
    }

    warm_path = champ
    if warmstart_shadow and SHADOW.exists():
        warm_path = SHADOW
        report["warmstart_source"] = "shadow"
    else:
        report["warmstart_source"] = "champion"
    pol = MetaPolicy.load(warm_path, freeze=False, require_serious=False)
    pol.unlock_for_meta_train()
    report["warmstart_fp"] = pol.weight_fingerprint()

    labs = _labs()
    report["n_path_anchors"] = len(labs)

    if density_boost and labs:
        # Iteration focused on A13 / n_zero blockers (method-preserving density)
        print("[Aaron] DENSITY BOOST iteration (A13 / n_zero)…", flush=True)
        # Pure path fire capacity first (teachers are long/short only)
        path_reanchor(pol.brain, labs, n_passes=6, seed=seed + 21)
        apply_outcome_tagged_path_teachers(
            pol.brain, labs, lr=0.022, seed=seed + 22, n_passes=6, max_examples=len(labs)
        )
        path_reanchor(pol.brain, labs, n_passes=5, seed=seed + 23)
        apply_outcome_tagged_path_teachers(
            pol.brain, labs, lr=0.020, seed=seed + 24, n_passes=5, max_examples=len(labs)
        )
        path_reanchor(pol.brain, labs, n_passes=4, seed=seed + 25)
        # Reclaim-heavy method seal (not full wait flood)
        flr_b = train_aaron_reason_curriculum(
            pol.brain,
            steps=max(600, flr_steps // 5),
            seed=seed + 26,
            lr=0.012,
            staged=True,
            continuation_heavy=True,
        )
        report["flr_density_boost"] = flr_b
        # Path last so A13 density is not washed by wait CE
        path_reanchor(pol.brain, labs, n_passes=5, seed=seed + 27)
        apply_outcome_tagged_path_teachers(
            pol.brain, labs, lr=0.018, seed=seed + 28, n_passes=4, max_examples=len(labs)
        )
        report["recipe"] = (
            "warmstart→path_density_heavy→continuation_heavy_FLR→path_last→freeze→dual"
        )
        report["method_first"] = True
    else:
        # 1) Density foundation (path fire anchors — real visited states)
        if labs:
            print("[Aaron] path density foundation…", flush=True)
            apply_outcome_tagged_path_teachers(
                pol.brain,
                labs,
                lr=0.018,
                seed=seed + 3,
                n_passes=3,
                max_examples=len(labs),
            )
            path_reanchor(pol.brain, labs, n_passes=2, seed=seed + 5)

        # 2) Staged FLR method (reason — reclaim-weighted)
        print(f"[Aaron] staged FLR steps={flr_steps}…", flush=True)
        flr = train_aaron_reason_curriculum(
            pol.brain, steps=flr_steps, seed=seed, lr=0.016, staged=True
        )
        report["flr_curriculum"] = flr

        # 3) Density seal FIRST then short reclaim FLR seal (keep A13 + method)
        if labs:
            print("[Aaron] density seal then FLR seal…", flush=True)
            path_reanchor(pol.brain, labs, n_passes=3, seed=seed + 7)
            apply_outcome_tagged_path_teachers(
                pol.brain, labs, lr=0.017, seed=seed + 8, n_passes=2, max_examples=len(labs)
            )
            flr2 = train_aaron_reason_curriculum(
                pol.brain,
                steps=max(1000, flr_steps // 3),
                seed=seed + 11,
                lr=0.014,
                staged=True,
            )
            report["flr_seal"] = flr2
            apply_outcome_tagged_path_teachers(
                pol.brain, labs, lr=0.012, seed=seed + 13, n_passes=1, max_examples=len(labs)
            )
            flr3 = train_aaron_reason_curriculum(
                pol.brain,
                steps=max(800, flr_steps // 5),
                seed=seed + 17,
                lr=0.013,
                staged=True,
            )
            report["flr_final_seal"] = flr3

        report["method_first"] = True
        report["package"] = "Aaron_here/packages/PKG-005_meta_rl_method_first_policy.md"
        report["recipe"] = (
            "warmstart0037→path_density→staged_FLR→path_seal→FLR_seal"
            "→density_micro→FLR_final_seal→freeze→dual"
        )

    pol.trained = True
    pol.meta_train_steps = pol.brain.meta_train_steps
    pol.freeze_for_inference()
    pol.assert_frozen()
    fp = pol.weight_fingerprint()
    # Keep prior shadow as backup before overwrite
    if SHADOW.exists():
        import shutil

        bak = ART / "meta_policy_aaron_reason_prev.npz"
        shutil.copy2(SHADOW, bak)
        report["shadow_backup_prev"] = str(bak)
    pol.save(SHADOW)
    SHADOW_JSON.write_text(
        json.dumps(
            {
                "fingerprint": fp,
                "meta_train_steps": int(pol.meta_train_steps),
                "law": "AARON_FORCE_STATE_DETHRONE",
                "promote": False,
                "warmstart": report["warmstart_fp"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    report["fingerprint"] = fp
    report["shadow_path"] = str(SHADOW)

    print(f"[Aaron] window dual days={dual_days}…", flush=True)
    lab_w = run_north_star_dual(SHADOW, n_days=dual_days, seed=seed)
    report["lab_window"] = {
        k: lab_w.get(k)
        for k in (
            "hits",
            "a13_frac",
            "n_zero",
            "breach_count",
            "mean_tr",
            "mean_pnl",
            "weights_frozen",
        )
    }

    dual_floor = None
    dec = None
    if floor_dual:
        print(f"[Aaron] floor dual forward100 days={floor_days}…", flush=True)
        lab_pol = MetaPolicy.load(SHADOW, freeze=True, require_serious=False)
        # Pin CASE-0037 calendar end so dual matches BEST_POLICY floor window
        rep_f = run_forward_eval(
            n_days=int(floor_days),
            seed=seed,
            policy=lab_pol,
            use_goal_path=True,
            window_end_date="2026-05-26",
            trail_calendar_days=280,
        )
        dual_floor = _floor_summary(rep_f)
        report["dual_floor"] = dual_floor
        report["dual_protocol"] = "forward100_class"
        dec = dethrone_decision(dual_floor, FLOOR_100D)
        report["dethrone_decision"] = dec
        report["production_replace"] = bool(dec.get("dethrone"))
        if dec.get("dethrone"):
            # Atomic promote only when bar holds
            print("[Aaron] DETHRONE true — writing champion…", flush=True)
            backup = ART / "meta_policy_champion_pre_aaron.npz"
            if champ.exists() and not backup.exists():
                import shutil

                shutil.copy2(champ, backup)
            pol.save(champ)
            (ART / "meta_policy_champion.json").write_text(
                json.dumps(
                    {
                        "fingerprint": fp,
                        "meta_train_steps": int(pol.meta_train_steps),
                        "trained": True,
                        "promoted_from": "AARON_FORCE_STATE_DETHRONE",
                        "law": "AARON_FLR + MONTY_EO_SIZE",
                        "seed": seed,
                        "format": 2,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            report["production_champion_path"] = str(champ)
            report["backup"] = str(backup)
        else:
            report["production_champion_unchanged"] = True
            report["blockers"] = dec.get("blockers")
    else:
        report["production_champion_unchanged"] = True
        report["note"] = "floor_dual=false; window dual only — no production claim"

    REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {
                "fingerprint": fp,
                "lab_window": report.get("lab_window"),
                "dual_floor": dual_floor,
                "dethrone_decision": dec,
                "production_replace": report.get("production_replace"),
            },
            indent=2,
            default=str,
        ),
        flush=True,
    )
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Aaron FLR reason train + dual")
    p.add_argument("--flr-steps", type=int, default=4000)
    p.add_argument("--dual-days", type=int, default=20)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--floor-dual", action="store_true")
    p.add_argument("--floor-days", type=int, default=100)
    p.add_argument(
        "--warmstart-shadow",
        action="store_true",
        help="Continue from meta_policy_aaron_reason.npz if present",
    )
    p.add_argument(
        "--density-boost",
        action="store_true",
        help="A13/n_zero focused iteration (use with --warmstart-shadow)",
    )
    args = p.parse_args(list(argv) if argv is not None else None)
    run_aaron_reason_train(
        flr_steps=int(args.flr_steps),
        dual_days=int(args.dual_days),
        seed=int(args.seed),
        floor_dual=bool(args.floor_dual),
        floor_days=int(args.floor_days),
        warmstart_shadow=bool(args.warmstart_shadow),
        density_boost=bool(args.density_boost),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
