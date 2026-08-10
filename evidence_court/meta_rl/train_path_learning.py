"""Execute PATH LEARNING steps 1–6 offline → lab shadow + dual + promote_guard.

Does NOT replace production champion unless guard.production_replace and Court PROMOTE.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import numpy as np

from .l2l_process import train_l2l_process_curriculum
from .path_learning import (
    FLOOR_100D,
    path_learning_promote_guard,
    path_reanchor,
    train_path_learning_curriculum,
)
from .path_state_harvest import filter_path_state_teachers
from .policy import DEFAULT_CHAMPION_PATH, MetaPolicy
from .train_l2l_full import run_north_star_dual

ART = Path("evidence_court/artifacts")
SHADOW = ART / "meta_policy_path_learning.npz"
SHADOW_JSON = ART / "meta_policy_path_learning.json"
REPORT = ART / "path_learning_report.json"
PATH_PACK = ART / "path_state_teachers_case0037.json"
HTF_PACK = ART / "path_state_teachers_htf_active_year.json"


def _load_path(max_examples: int = 900) -> list:
    raw: list = []
    for p in (PATH_PACK, HTF_PACK):
        if p.exists():
            pack = json.loads(p.read_text(encoding="utf-8"))
            raw.extend(list(pack.get("examples") or []))
    return filter_path_state_teachers(raw, max_examples=max_examples, require_htf_active=True)


def run_path_learning(
    *,
    curriculum_steps: int = 2500,
    process_steps: int = 600,
    reanchor_passes: int = 2,
    dual_days: int = 30,
    seed: int = 42,
    court_promote: bool = False,
) -> Dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    report: Dict[str, Any] = {
        "law": "PATH_LEARNING",
        "case": "CASE-PATH-LEARNING",
        "ts": ts,
        "goal_axes": [
            "G-TRAIN",
            "G-L2L",
            "G-A13",
            "G-CLEAR",
            "G-NO_RETRAIN",
            "G-BREACH0",
        ],
        "recipe": "warmstart→goal/conversion/outcome primary→light process→path reanchor last→freeze→dual→guard",
    }

    champ_path = Path(DEFAULT_CHAMPION_PATH)
    if not champ_path.exists():
        report["error"] = "missing_champion"
        REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report

    pol = MetaPolicy.load(champ_path, freeze=False, require_serious=False)
    pol.unlock_for_meta_train()
    report["warmstart_fp"] = pol.weight_fingerprint()

    labs = _load_path(900)
    report["n_path_anchors"] = len(labs)

    # Steps 1–4 curriculum
    print(f"[PATH_LEARN] curriculum steps={curriculum_steps}…", flush=True)
    cur = train_path_learning_curriculum(
        pol.brain,
        steps=int(curriculum_steps),
        seed=seed,
        path_examples=labs,
        path_anchor_frac=0.18,
        holdout_frac=0.15,
        process_frac=0.10,
        lr=0.014,
        density_process=True,
    )
    report["curriculum"] = cur

    # Step 5 light process then re-anchor last
    print(f"[PATH_LEARN] light density process steps={process_steps}…", flush=True)
    proc = train_l2l_process_curriculum(
        pol.brain,
        steps=int(process_steps),
        seed=seed + 11,
        holdout_frac=0.15,
        lr=0.008,
        density_mode=True,
    )
    report["process"] = {
        "fire_frac": proc.get("fire_frac"),
        "n_fire": proc.get("n_fire"),
        "n_wait": proc.get("n_wait"),
        "density_mode": True,
    }

    print(f"[PATH_LEARN] path re-anchor last passes={reanchor_passes}…", flush=True)
    n_ra = path_reanchor(pol.brain, labs, n_passes=int(reanchor_passes), seed=seed + 7)
    # extra outcome-shaped pass on path anchors
    rng = np.random.default_rng(seed + 3)
    from .path_learning import apply_outcome_shaped_update

    for i in range(max(50, len(labs) // 2)):
        ex = labs[int(rng.integers(0, len(labs)))]
        apply_outcome_shaped_update(
            pol.brain,
            np.asarray(ex["state"], dtype=np.float64).ravel(),
            teacher_act=str(ex["teacher_act"]),
            outcome_score=float(ex.get("outcome_score") or 0.3),
            lr=0.016 * (0.95 ** (i // 40)),
            teacher_size_frac=float(ex.get("teacher_size_frac") or 0.65),
        )
    report["path_reanchor_updates"] = int(n_ra)
    report["path_reanchor_last"] = True

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
                "trained": True,
                "law": "PATH_LEARNING",
                "promote": False,
                "warmstart": report["warmstart_fp"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    report["shadow_path"] = str(SHADOW)

    print(f"[PATH_LEARN] dual lab days={dual_days}…", flush=True)
    dual_lab = run_north_star_dual(SHADOW, n_days=dual_days, seed=seed)
    print(f"[PATH_LEARN] dual champ days={dual_days}…", flush=True)
    dual_champ = run_north_star_dual(champ_path, n_days=dual_days, seed=seed)
    report["dual_lab"] = dual_lab
    report["dual_champ"] = dual_champ
    report["dual_protocol"] = "north_star_random_TxR_XAU_15m"

    guard = path_learning_promote_guard(
        dual_lab,
        dual_champ,
        floor=FLOOR_100D,
        path_only_clone=bool(cur.get("path_only_clone")),
        process_washout=float(dual_lab.get("a13_frac") or 0) < 0.30,
        has_outcome_conversion_mix=bool(
            cur.get("has_outcome_shaping") and cur.get("has_conversion")
        ),
        court_promote=bool(court_promote),
    )
    report["promote_guard"] = guard
    report["production_replace"] = bool(guard.get("production_replace"))
    report["production_champion_unchanged"] = True
    report["floor_100d_reference"] = FLOOR_100D

    REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {
                "fingerprint": fp,
                "dual_lab": {
                    k: dual_lab.get(k)
                    for k in (
                        "hits",
                        "a13_frac",
                        "n_zero",
                        "breach_count",
                        "mean_tr",
                        "weights_frozen",
                    )
                },
                "dual_champ": {
                    k: dual_champ.get(k)
                    for k in ("hits", "a13_frac", "n_zero", "breach_count", "mean_tr")
                },
                "promote_guard": guard,
            },
            indent=2,
        ),
        flush=True,
    )
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="PATH LEARNING lab train + dual")
    p.add_argument("--curriculum-steps", type=int, default=2500)
    p.add_argument("--process-steps", type=int, default=600)
    p.add_argument("--reanchor-passes", type=int, default=2)
    p.add_argument("--dual-days", type=int, default=30)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--court-promote", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)
    run_path_learning(
        curriculum_steps=int(args.curriculum_steps),
        process_steps=int(args.process_steps),
        reanchor_passes=int(args.reanchor_passes),
        dual_days=int(args.dual_days),
        seed=int(args.seed),
        court_promote=bool(args.court_promote),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
