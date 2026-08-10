"""L2L-P10 residual: density-preserving retrain (path-state + density process).

Does NOT replace production champion unless promote_decision says so after dual.
Road (not cliff): warmstart CASE-0037 → path-state fire teachers → light density
process curriculum → freeze → dual vs champion floor → promote only on beat.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import numpy as np

from .l2l_process import train_l2l_process_curriculum
from .path_state_harvest import apply_path_state_teachers_to_brain, filter_path_state_teachers
from .policy import DEFAULT_CHAMPION_PATH, MetaPolicy
from .train_l2l_full import run_north_star_dual

ART = Path("evidence_court/artifacts")
SHADOW = ART / "meta_policy_l2l_p10_residual.npz"
SHADOW_JSON = ART / "meta_policy_l2l_p10_residual.json"
REPORT = ART / "l2l_p10_residual_report.json"
DEFAULT_PATH_STATE = ART / "path_state_teachers_case0037.json"
HTF_YEAR_PACK = ART / "path_state_teachers_htf_active_year.json"

# CASE-0037 100d floor (BEST_POLICY.md) — residual must not claim beat without measure
FLOOR_100D = {
    "hits": 11,
    "low_hr": 0.28,
    "a13_frac": 0.64,
    "n_zero": 18,
    "breach": 0,
}


def _load_path_examples(
    paths: Sequence[Path],
    *,
    max_examples: int = 900,
) -> list:
    raw: list = []
    for p in paths:
        if not p.exists():
            continue
        pack = json.loads(p.read_text(encoding="utf-8"))
        raw.extend(list(pack.get("examples") or []))
    return filter_path_state_teachers(raw, max_examples=max_examples, require_htf_active=True)


def promote_decision(
    residual_dual: Dict[str, Any],
    champion_dual: Dict[str, Any],
    *,
    floor: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Promote residual only if it beats champion dual without breach and holds density."""
    floor = floor or FLOOR_100D
    r_a13 = float(residual_dual.get("a13_frac") or 0.0)
    c_a13 = float(champion_dual.get("a13_frac") or 0.0)
    r_hits = int(residual_dual.get("hits") or 0)
    c_hits = int(champion_dual.get("hits") or 0)
    r_zero = int(residual_dual.get("n_zero") or 0)
    c_zero = int(champion_dual.get("n_zero") or 0)
    r_breach = int(residual_dual.get("breach_count") or 0)
    c_breach = int(champion_dual.get("breach_count") or 0)
    r_hr = float(residual_dual.get("hit_rate") or 0.0)
    c_hr = float(champion_dual.get("hit_rate") or 0.0)
    frozen = bool(residual_dual.get("weights_frozen"))
    pb_cont = bool(residual_dual.get("both_pb_and_cont"))

    beats_champ_a13 = r_a13 >= c_a13 - 1e-9
    beats_champ_hits = r_hits >= c_hits
    fewer_or_eq_zero = r_zero <= c_zero
    no_breach = r_breach == 0 and c_breach == 0
    # Scaled floor for short dual: a13 at least half of 100d floor is not enough —
    # residual must beat *this window's* champion and not collapse hits.
    beats = (
        frozen
        and pb_cont
        and no_breach
        and beats_champ_a13
        and beats_champ_hits
        and fewer_or_eq_zero
        and r_a13 >= 0.30  # hard floor: process wash-out guard
    )
    note_parts = []
    if not frozen:
        note_parts.append("not_frozen")
    if not pb_cont:
        note_parts.append("missing_pb_or_cont")
    if r_breach:
        note_parts.append(f"breach={r_breach}")
    if not beats_champ_a13:
        note_parts.append(f"a13 {r_a13:.3f}<champ {c_a13:.3f}")
    if not beats_champ_hits:
        note_parts.append(f"hits {r_hits}<champ {c_hits}")
    if not fewer_or_eq_zero:
        note_parts.append(f"n_zero {r_zero}>champ {c_zero}")
    if r_a13 < 0.30:
        note_parts.append(f"a13_below_hard_floor {r_a13:.3f}<0.30")

    return {
        "promote": bool(beats),
        "reason": "beats_champion_dual" if beats else ("reject: " + "; ".join(note_parts) or "reject"),
        "residual": {
            "a13_frac": r_a13,
            "hits": r_hits,
            "hit_rate": r_hr,
            "n_zero": r_zero,
            "breach_count": r_breach,
        },
        "champion": {
            "a13_frac": c_a13,
            "hits": c_hits,
            "hit_rate": c_hr,
            "n_zero": c_zero,
            "breach_count": c_breach,
        },
        "floor_100d_reference": floor,
        "note": "100d multi-seed still required for L2L §7 final gate even if promote true",
    }


def _apply_path_block(
    brain: Any,
    labs: Sequence[Dict[str, Any]],
    *,
    seed: int,
    n_passes: int,
    n_extra_frac: float = 0.5,
    lr: float = 0.02,
) -> int:
    """Path-state fire re-anchor (density lever)."""
    n_path = apply_path_state_teachers_to_brain(
        brain,
        labs,
        lr=lr,
        seed=seed,
        max_examples=len(labs),
        n_passes=int(n_passes),
    )
    rng = np.random.default_rng(seed + 3)
    n_extra = max(100, int(len(labs) * float(n_extra_frac)))
    for i in range(n_extra):
        ex = labs[int(rng.integers(0, len(labs)))]
        st = np.asarray(ex["state"], dtype=np.float64).ravel()
        brain.meta_update(
            st,
            teacher_act=str(ex["teacher_act"]),
            lr=0.018 * (0.95 ** (i // 50)),
            reward=1.25,
            teacher_size_frac=float(ex.get("teacher_size_frac") or 0.65),
        )
    return int(n_path + n_extra)


def run_l2l_p10_residual(
    *,
    path_passes: int = 3,
    process_steps: int = 800,
    dual_days: int = 30,
    seed: int = 42,
    path_max: int = 900,
    include_htf_year: bool = True,
    process_lr: float = 0.008,
    reanchor_path_passes: int = 2,
) -> Dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    report: Dict[str, Any] = {
        "law": "L2L_P10_RESIDUAL_DENSITY",
        "case": "CASE-L2L-P10-residual",
        "ts": ts,
        "goal_axes": ["G-A13", "G-CLEAR", "G-TRAIN", "G-NO_RETRAIN", "G-L2L", "G-BREACH0"],
        "recipe": "warmstart→light_density_process→path_reanchor_last",
    }

    # 1) Warmstart production champion (CASE-0037)
    champ_path = Path(DEFAULT_CHAMPION_PATH)
    if not champ_path.exists():
        report["error"] = f"missing champion {champ_path}"
        REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report
    pol = MetaPolicy.load(champ_path, freeze=False, require_serious=False)
    pol.unlock_for_meta_train()
    report["warmstart_fp"] = pol.weight_fingerprint()
    report["warmstart_meta_steps"] = int(pol.meta_train_steps)

    # 2) Load path-state fire teachers
    paths = [DEFAULT_PATH_STATE]
    if include_htf_year and HTF_YEAR_PACK.exists():
        paths.append(HTF_YEAR_PACK)
    labs = _load_path_examples(paths, max_examples=path_max)
    report["n_path_teachers"] = len(labs)
    if not labs:
        report["error"] = "no_path_state_teachers"
        REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report

    # 3) Light density process FIRST (senses road) — keep short so wait CE cannot dominate
    print(f"[P10-res] density process curriculum steps={process_steps}…", flush=True)
    cur = train_l2l_process_curriculum(
        pol.brain,
        steps=int(process_steps),
        seed=seed + 11,
        holdout_frac=0.15,
        lr=float(process_lr),
        density_mode=True,
    )
    report["process_curriculum"] = cur

    # 4) Path-state LAST (re-anchor A13 density after process — anti-washout)
    print(
        f"[P10-res] path re-anchor n={len(labs)} passes={path_passes}+{reanchor_path_passes}…",
        flush=True,
    )
    n1 = _apply_path_block(
        pol.brain, labs, seed=seed + 7, n_passes=int(path_passes), n_extra_frac=0.6
    )
    n2 = _apply_path_block(
        pol.brain,
        labs,
        seed=seed + 19,
        n_passes=int(reanchor_path_passes),
        n_extra_frac=0.8,
        lr=0.022,
    )
    report["path_updates"] = int(n1 + n2)
    report["path_reanchor_last"] = True
    pol.trained = True
    pol.meta_train_steps = pol.brain.meta_train_steps

    # 4) Freeze (P8)
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
                "law": "L2L_P10_RESIDUAL_DENSITY",
                "promote": False,
                "warmstart": report["warmstart_fp"],
                "n_path_teachers": len(labs),
                "process_fire_frac": cur.get("fire_frac"),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    report["shadow_path"] = str(SHADOW)

    # 5) Dual residual + champion same window
    print(f"[P10-res] dual residual days={dual_days}…", flush=True)
    dual_res = run_north_star_dual(SHADOW, n_days=dual_days, seed=seed)
    report["dual_residual"] = dual_res
    print(f"[P10-res] dual champion days={dual_days}…", flush=True)
    dual_champ = run_north_star_dual(champ_path, n_days=dual_days, seed=seed)
    report["dual_champion"] = dual_champ

    dec = promote_decision(dual_res, dual_champ)
    report["promote_decision"] = dec

    # Final §7 gate still false unless residual fully clears a13 every day + hits
    final_ok = (
        dual_res.get("breach_count") == 0
        and dual_res.get("weights_frozen")
        and dual_res.get("both_pb_and_cont")
        and dual_res.get("a13_every_day")
        and float(dual_res.get("hit_rate") or 0) > 0.05
    )
    report["final_promote_gate"] = {
        "ready": bool(final_ok),
        "note": "L2L §7 multi-seed 100d still required for mission PROMOTE",
        "measured_dual_days": dual_days,
    }

    # Optional: write champion only if promote_decision and still not claim final boss
    if dec["promote"]:
        # Lab promote to residual-champion shadow only — production replace needs Court order
        lab_prom = ART / "meta_policy_l2l_p10_residual_LAB_PROMOTE.npz"
        pol.save(lab_prom)
        report["lab_promote_path"] = str(lab_prom)
        report["production_champion_replaced"] = False
        report["production_note"] = (
            "beats same-window champion dual; production still CASE-0037 until "
            "Full Court PROMOTE + 100d floor hold"
        )

    REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {
                "dual_residual": {
                    k: dual_res[k]
                    for k in (
                        "hits",
                        "hit_rate",
                        "a13_frac",
                        "n_zero",
                        "breach_count",
                        "mean_tr",
                        "fingerprint",
                    )
                    if k in dual_res
                },
                "dual_champion": {
                    k: dual_champ[k]
                    for k in (
                        "hits",
                        "hit_rate",
                        "a13_frac",
                        "n_zero",
                        "breach_count",
                        "mean_tr",
                        "fingerprint",
                    )
                    if k in dual_champ
                },
                "promote_decision": dec,
                "final_promote_gate": report["final_promote_gate"],
            },
            indent=2,
        ),
        flush=True,
    )
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="L2L-P10 density residual train + dual")
    p.add_argument("--process-steps", type=int, default=800)
    p.add_argument("--path-passes", type=int, default=3)
    p.add_argument("--reanchor-passes", type=int, default=2)
    p.add_argument("--dual-days", type=int, default=30)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--path-max", type=int, default=900)
    p.add_argument("--no-htf-year", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)
    run_l2l_p10_residual(
        process_steps=int(args.process_steps),
        path_passes=int(args.path_passes),
        reanchor_path_passes=int(args.reanchor_passes),
        dual_days=int(args.dual_days),
        seed=int(args.seed),
        path_max=int(args.path_max),
        include_htf_year=not bool(args.no_htf_year),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
