"""Pipeline: path-state teachers (00_PATH_STATE_TEACHERS) + Monty HTF blend retrain.

Lab only — writes shadow weights + dual compare. Does NOT replace champion.

Steps:
  1. Harvest packed path-state teachers under monty_htf_blend=True
  2. Warmstart production champion → offline path-state meta_update
  3. Dual measure: champ slope-only vs new shadow with blend ON
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from .htf_blend_dual_compare import run_arm, _summarize, _delta
from .path_state_harvest import (
    harvest_path_state_teachers,
    save_path_state_pack,
    train_path_state_a13_policy,
)
from .policy import DEFAULT_CHAMPION_PATH, load_or_train_champion, MetaPolicy
from .edge import build_tf_cache
from .price_io import SYMBOL_FILES, available_symbols, bars_to_daily, load_m1_trailing_calendar_days
import numpy as np

DEFAULT_PACK = Path("evidence_court/artifacts/teachers/path_state_teachers_monty_blend.json")
DEFAULT_SHADOW = Path(
    "evidence_court/artifacts/policies_lab/meta_policy_pathstate_monty_blend.npz"
)
DEFAULT_SHADOW_JSON = Path(
    "evidence_court/artifacts/policies_lab/meta_policy_pathstate_monty_blend.json"
)
DEFAULT_REPORT = Path(
    "evidence_court/artifacts/reports/path_state_monty_blend_train_report.json"
)


def run_pipeline(
    *,
    harvest_days: int = 20,
    dual_days: int = 20,
    seed: int = 42,
    max_examples: int = 400,
    path_mix: float = 0.40,
    n_passes: int = 2,
    champion_path: Optional[Path] = None,
    pack_out: Path = DEFAULT_PACK,
    shadow_out: Path = DEFAULT_SHADOW,
    report_out: Path = DEFAULT_REPORT,
    skip_harvest: bool = False,
    pack_in: Optional[Path] = None,
) -> Dict[str, Any]:
    champ = Path(champion_path) if champion_path else DEFAULT_CHAMPION_PATH
    report: Dict[str, Any] = {
        "law": "lab_path_state_monty_blend_retrain",
        "process": "00_PATH_STATE_TEACHERS + monty_htf_blend",
        "champion_path": str(champ),
        "seed": seed,
        "harvest_days": harvest_days,
        "dual_days": dual_days,
        "promote": False,
    }

    # ── 1. Harvest ─────────────────────────────────────────────
    if skip_harvest and pack_in and Path(pack_in).exists():
        pack = json.loads(Path(pack_in).read_text(encoding="utf-8"))
        report["harvest"] = {
            "source": "loaded",
            "path": str(pack_in),
            "n_examples": pack.get("n_examples") or len(pack.get("examples") or []),
            "n_london_ny": pack.get("n_london_ny"),
            "dims_ok": pack.get("dims_ok"),
            "monty_htf_blend": pack.get("monty_htf_blend"),
        }
    else:
        print("[1/3] Harvest path-state teachers (monty_htf_blend=True)…", flush=True)
        pack = harvest_path_state_teachers(
            n_days=int(harvest_days),
            seed=seed,
            max_examples=int(max_examples),
            monty_htf_blend=True,
        )
        save_path_state_pack(pack, pack_out)
        report["harvest"] = {
            "source": "fresh",
            "path": str(pack_out),
            "n_days": pack.get("n_days"),
            "n_raw": pack.get("n_raw"),
            "n_examples": pack.get("n_examples"),
            "n_london_ny": pack.get("n_london_ny"),
            "dims_ok": pack.get("dims_ok"),
            "monty_htf_blend": pack.get("monty_htf_blend"),
            "window_start": pack.get("window_start"),
            "window_end": pack.get("window_end"),
            "policy_fingerprint": pack.get("policy_fingerprint"),
        }
        print(
            f"  examples={pack.get('n_examples')} ln={pack.get('n_london_ny')} "
            f"dims_ok={pack.get('dims_ok')}",
            flush=True,
        )

    examples = pack.get("examples") or []
    if len(examples) < 10:
        report["error"] = "too_few_teachers"
        report_out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report

    # ── 2. Train shadow (warmstart champion) ───────────────────
    print("[2/3] Train shadow: warmstart champion + path-state teachers…", flush=True)
    before_fp = ""
    if champ.exists():
        try:
            before_fp = MetaPolicy.load(champ, freeze=True).weight_fingerprint()
        except Exception:
            before_fp = ""
    pol = train_path_state_a13_policy(
        examples,
        seed=seed,
        n_steps=2500,
        path_mix=float(path_mix),
        freeze=True,
        save_path=shadow_out,
        warmstart_path=champ if champ.exists() else None,
        n_passes=int(n_passes),
    )
    after_fp = pol.weight_fingerprint()
    sidecar = {
        "fingerprint": after_fp,
        "meta_train_steps": int(pol.meta_train_steps),
        "trained": True,
        "n_examples": len(examples),
        "warmstart": str(champ) if champ.exists() else None,
        "warmstart_fp": before_fp,
        "monty_htf_blend_harvest": True,
        "law": "lab_path_state_monty_blend",
        "format": 2,
        "seed": seed,
        "promote": False,
    }
    DEFAULT_SHADOW_JSON.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
    report["train"] = {
        "shadow_path": str(shadow_out),
        "sidecar": str(DEFAULT_SHADOW_JSON),
        "meta_train_steps": int(pol.meta_train_steps),
        "fp_before": before_fp,
        "fp_after": after_fp,
        "weights_changed": before_fp != after_fp,
        "path_mix": path_mix,
        "n_passes": n_passes,
    }
    print(f"  steps={pol.meta_train_steps} fp={after_fp}", flush=True)

    # ── 3. Dual: champ slope-off vs shadow blend-on ────────────
    print("[3/3] Dual measure (champ slope-only vs shadow blend-on)…", flush=True)
    dual = _dual_champ_vs_shadow(
        shadow_path=shadow_out,
        champion_path=champ,
        n_days=int(dual_days),
        seed=seed,
    )
    report["dual"] = dual
    report["verdict"] = dual.get("verdict")
    report_out.parent.mkdir(parents=True, exist_ok=True)
    report_out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report["report_path"] = str(report_out)
    print(json.dumps({"verdict": report["verdict"], "dual": dual.get("summary")}, indent=2), flush=True)
    return report


def _dual_champ_vs_shadow(
    *,
    shadow_path: Path,
    champion_path: Path,
    n_days: int,
    seed: int,
) -> Dict[str, Any]:
    from .htf_blend_dual_compare import DEFAULT_TARGETS, DEFAULT_RISKS

    syms = [s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()]
    champ = load_or_train_champion(path=champion_path if champion_path.exists() else None, seed=seed)
    shadow = MetaPolicy.load(shadow_path, freeze=True, require_serious=False)
    champ.assert_frozen()
    shadow.assert_frozen()

    warmup = 12
    trail = n_days + warmup + 5
    m1_by_sym: Dict[str, list] = {}
    daily_by_sym: Dict[str, list] = {}
    for sym in syms:
        path = SYMBOL_FILES.get(sym)
        if path is None or not path.exists():
            continue
        m1 = load_m1_trailing_calendar_days(path, n_days=trail)
        if m1:
            m1_by_sym[sym] = m1
            daily_by_sym[sym] = bars_to_daily(m1)
    if not m1_by_sym:
        return {"error": "no_price"}

    date_sets = [set(d["date"] for d in days) for days in daily_by_sym.values()]
    common = sorted(set.intersection(*date_sets)) if len(date_sets) > 1 else sorted(date_sets[0])
    need = n_days + warmup
    window = common[-need:] if len(common) >= need else common
    eval_dates = window[warmup:] if len(window) > warmup else window[1:]
    eval_dates = eval_dates[-n_days:]
    daily_maps = {sym: {d["date"]: d for d in days} for sym, days in daily_by_sym.items()}
    tf_cache = {sym: build_tf_cache(m1) for sym, m1 in m1_by_sym.items()}

    rng = np.random.default_rng(seed)
    schedule = [
        (float(rng.choice(DEFAULT_TARGETS)), float(rng.choice(DEFAULT_RISKS)))
        for _ in eval_dates
    ]
    sym_list = list(m1_by_sym.keys())

    # Production-like: champ + slope only
    off = run_arm(
        pol=champ,
        eval_dates=eval_dates,
        m1_by_sym=m1_by_sym,
        daily_maps=daily_maps,
        tf_cache_by_symbol=tf_cache,
        syms=sym_list,
        schedule=schedule,
        monty_htf_blend=False,
    )
    # New stack: shadow trained on blend path-states, measure with blend on
    on = run_arm(
        pol=shadow,
        eval_dates=eval_dates,
        m1_by_sym=m1_by_sym,
        daily_maps=daily_maps,
        tf_cache_by_symbol=tf_cache,
        syms=sym_list,
        schedule=schedule,
        monty_htf_blend=True,
    )
    # Control: shadow weights but slope-only edge (did retrain help without blend at prove?)
    on_slope = run_arm(
        pol=shadow,
        eval_dates=eval_dates,
        m1_by_sym=m1_by_sym,
        daily_maps=daily_maps,
        tf_cache_by_symbol=tf_cache,
        syms=sym_list,
        schedule=schedule,
        monty_htf_blend=False,
    )

    s_off = _summarize(off)
    s_on = _summarize(on)
    s_on_slope = _summarize(on_slope)
    delta = _delta(s_off, s_on)

    better, worse = [], []
    if delta.get("breach_count", 0) and delta["breach_count"] > 0:
        worse.append("more_breaches")
    if s_on.get("breach"):
        worse.append("breach")
    if delta.get("hit_rate") is not None:
        if delta["hit_rate"] > 0.01:
            better.append("hit_rate")
        elif delta["hit_rate"] < -0.01:
            worse.append("hit_rate")
    if delta.get("a13_frac") is not None:
        if delta["a13_frac"] > 0.02:
            better.append("a13_frac")
        elif delta["a13_frac"] < -0.02:
            worse.append("a13_frac")
    if delta.get("mean_pnl") is not None:
        if delta["mean_pnl"] > 0.05:
            better.append("mean_pnl")
        elif delta["mean_pnl"] < -0.05:
            worse.append("mean_pnl")
    if delta.get("n_zero") is not None:
        if delta["n_zero"] < -0.5:
            better.append("fewer_silent_days")
        elif delta["n_zero"] > 0.5:
            worse.append("more_silent_days")

    if s_on.get("breach"):
        verdict = "SHADOW_WORSE_SAFETY"
    elif better and not worse:
        verdict = "SHADOW_BETTER"
    elif worse and not better:
        verdict = "SHADOW_WORSE"
    elif better and worse:
        verdict = "SHADOW_MIXED"
    else:
        verdict = "SHADOW_NEUTRAL"

    return {
        "verdict": verdict,
        "better_axes": better,
        "worse_axes": worse,
        "n_days": len(eval_dates),
        "eval_start": eval_dates[0] if eval_dates else None,
        "eval_end": eval_dates[-1] if eval_dates else None,
        "champ_slope_only": s_off,
        "shadow_blend_on": s_on,
        "shadow_slope_only": s_on_slope,
        "delta_shadow_blend_minus_champ": delta,
        "summary": {
            "verdict": verdict,
            "champ_a13": s_off.get("a13_frac"),
            "shadow_a13": s_on.get("a13_frac"),
            "champ_hits": s_off.get("hits"),
            "shadow_hits": s_on.get("hits"),
            "champ_mean_pnl": s_off.get("mean_pnl"),
            "shadow_mean_pnl": s_on.get("mean_pnl"),
            "champ_n_zero": s_off.get("n_zero"),
            "shadow_n_zero": s_on.get("n_zero"),
            "breach_shadow": s_on.get("breach"),
        },
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Path-state + Monty HTF blend retrain pipeline")
    p.add_argument("--harvest-days", type=int, default=20)
    p.add_argument("--dual-days", type=int, default=20)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--max-examples", type=int, default=400)
    p.add_argument("--path-mix", type=float, default=0.40)
    p.add_argument("--n-passes", type=int, default=2)
    p.add_argument("--skip-harvest", action="store_true")
    p.add_argument("--pack", type=str, default="")
    p.add_argument("--out-report", type=str, default=str(DEFAULT_REPORT))
    args = p.parse_args(list(argv) if argv is not None else None)
    run_pipeline(
        harvest_days=int(args.harvest_days),
        dual_days=int(args.dual_days),
        seed=int(args.seed),
        max_examples=int(args.max_examples),
        path_mix=float(args.path_mix),
        n_passes=int(args.n_passes),
        skip_harvest=bool(args.skip_harvest),
        pack_in=Path(args.pack) if args.pack else None,
        report_out=Path(args.out_report),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
