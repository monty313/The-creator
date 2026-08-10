"""Aaron method-rich train: Force→Load→Reclaim→Hold while Force + dual.

Rewards/penalties create the path to success relative to method (AARON.md),
not fire-clone or lot cosplay.

Lab shadow only. Production champion unchanged unless dual dethrones + Court.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from .aaron_reason_curriculum import train_aaron_reason_curriculum
from .edge import build_tf_cache
from .goal_path import PRODUCTION_SCALPING_SLOTS_15M, run_goal_path_day
from .path_learning import (
    FLOOR_100D,
    apply_conversion_path_teachers,
    load_outcome_tagged_examples,
    path_learning_promote_guard,
    path_reanchor,
)
from .policy import DEFAULT_CHAMPION_PATH, MetaPolicy
from .price_io import SYMBOL_FILES, available_symbols, load_m1_trailing_calendar_days
from .train_aaron_reason import dethrone_decision
from .train_l2l_full import run_north_star_dual

ART = Path("evidence_court/artifacts")
SHADOW = ART / "meta_policy_aaron_method_hold.npz"
SHADOW_JSON = ART / "meta_policy_aaron_method_hold.json"
REPORT = ART / "aaron_method_hold_train_report.json"
OUTCOME_PACK = ART / "path_state_teachers_outcome_2x.json"
BASE_PACK = ART / "path_state_teachers_case0037.json"

DAY12 = "2026-01-21"
TARGET = 15.0
RISK = 3.0


def _measure_day12_method(
    pol: MetaPolicy,
    m1_by: Dict[str, List],
    tf_cache: Dict,
    *,
    method_hold: bool,
) -> Dict[str, Any]:
    fills, ledger, gmeta = run_goal_path_day(
        pol,
        date=DAY12,
        m1_by_symbol=m1_by,
        target_percent=TARGET,
        max_daily_risk_percent=RISK,
        symbols=list(m1_by.keys()),
        tf_cache_by_symbol=tf_cache,
        slots=list(PRODUCTION_SCALPING_SLOTS_15M),
        brain_drives=True,
        watch_enabled=False,
        method_hold_while_force=bool(method_hold),
    )
    pnl = float(ledger.realized_pnl_percent)
    worst = float(ledger.worst_case_daily_loss_percent())
    loss = max(-pnl, 0.0)
    breach = loss > RISK + 1e-6 or worst > RISK + 1e-6
    return {
        "pnl": pnl,
        "n_trades": len(fills),
        "hit": pnl >= TARGET - 1e-9,
        "breach": breach,
        "n_method_hold_legs": int(gmeta.get("n_method_hold_legs") or 0),
        "method_hold_while_force": bool(method_hold),
        "progress": float(pnl / TARGET) if TARGET else 0.0,
        "fingerprint": pol.weight_fingerprint(),
    }


def run_aaron_method_hold_train(
    *,
    method_steps: int = 8000,
    dual_days: int = 30,
    seed: int = 42,
    measure_day12: bool = True,
) -> Dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    report: Dict[str, Any] = {
        "law": "AARON_METHOD_HOLD_TRAIN",
        "teacher": "Aaron_here/AARON.md §3.7–3.11 + PKG-002/005",
        "method": "Force→Load→Reclaim→HoldWhileForce→ExitWhenForceDies",
        "reward_priority": "method first, goal second, never WR alone",
        "ts": ts,
        "production_replace": False,
    }

    pol = MetaPolicy.load(DEFAULT_CHAMPION_PATH, freeze=False, require_serious=False)
    pol.unlock_for_meta_train()
    report["warmstart_fp"] = pol.weight_fingerprint()

    print("[aaron-method] stage 1–5 method-rich FLR+hold curriculum…", flush=True)
    cur = train_aaron_reason_curriculum(
        pol.brain,
        steps=int(method_steps),
        seed=seed,
        lr=0.017,
        staged=True,
        method_rich=True,
    )
    report["curriculum"] = {
        "shape_counts": cur.get("shape_counts"),
        "stages": cur.get("stages"),
        "has_hold_shape": cur.get("has_hold_shape"),
        "penalty_counts": cur.get("penalty_counts"),
        "mean_loss": cur.get("mean_loss"),
        "method": cur.get("method"),
    }
    print(json.dumps(report["curriculum"], indent=2, default=str), flush=True)

    # Multi-day conversion harvest (clear/dead/near-breach) — sparse path, not fire-clone
    print("[aaron-method] conversion multi-day apply (wait/hold/size_down)…", flush=True)
    multi = load_outcome_tagged_examples([OUTCOME_PACK, BASE_PACK], max_examples=1600)
    conv = apply_conversion_path_teachers(
        pol.brain,
        multi,
        lr=0.016,
        seed=seed + 3,
        max_examples=1000,
        n_passes=2,
        bucket_weights={"clear": 1.5, "dead": 1.3, "near_breach": 1.35, "progress": 1.0},
    )
    report["conversion_apply"] = {
        "n_updates": conv.get("n_updates"),
        "class_counts": conv.get("class_counts"),
        "bucket_counts": conv.get("bucket_counts"),
        "has_wait": conv.get("has_wait"),
        "has_hold_convert": conv.get("has_hold_convert"),
        "has_size_down": conv.get("has_size_down"),
    }

    # Density seal reclaim-heavy light + re-anchor last
    print("[aaron-method] reclaim density seal + path re-anchor…", flush=True)
    seal = train_aaron_reason_curriculum(
        pol.brain,
        steps=max(800, method_steps // 6),
        seed=seed + 7,
        lr=0.014,
        continuation_heavy=True,
    )
    n_re = path_reanchor(pol.brain, multi[:500], n_passes=1, seed=seed + 11, max_examples=400)
    report["seal"] = {
        "shape_counts": seal.get("shape_counts"),
        "n_reanchor": n_re,
    }

    # Hold-while-force seal (second pass — method priority)
    hold_seal = train_aaron_reason_curriculum(
        pol.brain,
        steps=max(1200, method_steps // 4),
        seed=seed + 13,
        lr=0.018,
        method_rich=True,
    )
    report["hold_seal"] = {
        "shape_counts": hold_seal.get("shape_counts"),
        "has_hold_shape": hold_seal.get("has_hold_shape"),
    }

    pol.trained = True
    pol.meta_train_steps = pol.brain.meta_train_steps
    pol.freeze_for_inference()
    pol.assert_frozen()
    pol.save(SHADOW)
    report["shadow_fp"] = pol.weight_fingerprint()
    report["shadow_path"] = str(SHADOW)

    # Dual: lab uses method_hold path for day path via separate day12 measure;
    # north-star dual uses production path geometry (honest default).
    print(f"[aaron-method] dual {dual_days}d (production path geometry)…", flush=True)
    dual_lab = run_north_star_dual(SHADOW, n_days=int(dual_days), seed=seed)
    dual_champ = run_north_star_dual(DEFAULT_CHAMPION_PATH, n_days=int(dual_days), seed=seed)
    report["dual_lab"] = {
        "hits": int(dual_lab.get("hits") or 0),
        "a13_frac": float(dual_lab.get("a13_frac") or 0.0),
        "n_zero": int(dual_lab.get("n_zero") or 0),
        "breach_count": int(dual_lab.get("breach_count") or 0),
        "mean_pnl": dual_lab.get("mean_pnl"),
        "weights_frozen": dual_lab.get("weights_frozen"),
    }
    report["dual_champ"] = {
        "hits": int(dual_champ.get("hits") or 0),
        "a13_frac": float(dual_champ.get("a13_frac") or 0.0),
        "n_zero": int(dual_champ.get("n_zero") or 0),
        "breach_count": int(dual_champ.get("breach_count") or 0),
        "mean_pnl": dual_champ.get("mean_pnl"),
    }
    guard = path_learning_promote_guard(
        dual_lab,
        dual_champ,
        has_outcome_conversion_mix=True,
        path_only_clone=False,
        court_promote=False,
    )
    deth = dethrone_decision(
        {
            "hits": report["dual_lab"]["hits"],
            "a13_frac": report["dual_lab"]["a13_frac"],
            "n_zero": report["dual_lab"]["n_zero"],
            "breach_count": report["dual_lab"]["breach_count"],
            "weights_frozen": True,
        },
        FLOOR_100D,
    )
    report["guard"] = guard
    report["dethrone"] = deth
    report["production_replace"] = False

    if measure_day12:
        print("[aaron-method] day12 diagnostic (baseline path vs method_hold path)…", flush=True)
        m1_by: Dict[str, List] = {}
        for sym in ("XAUUSD", "EURUSD", "GBPUSD"):
            if sym not in available_symbols():
                continue
            path = SYMBOL_FILES.get(sym)
            if path is None or not path.exists():
                continue
            m1 = load_m1_trailing_calendar_days(path, n_days=400)
            if m1 and any(b.get("date") == DAY12 for b in m1):
                m1_by[sym] = m1
        if m1_by:
            tf = {s: build_tf_cache(m) for s, m in m1_by.items()}
            # champ baseline no method hold
            champ = MetaPolicy.load(DEFAULT_CHAMPION_PATH, freeze=True, require_serious=False)
            base_off = _measure_day12_method(champ, m1_by, tf, method_hold=False)
            lab_off = _measure_day12_method(pol, m1_by, tf, method_hold=False)
            lab_on = _measure_day12_method(pol, m1_by, tf, method_hold=True)
            report["day12"] = {
                "champ_no_method_hold": base_off,
                "lab_no_method_hold": lab_off,
                "lab_method_hold": lab_on,
                "note": "method_hold is lab path geometry (Aaron t4); not production default",
            }
            print(json.dumps(report["day12"], indent=2, default=str), flush=True)

    SHADOW_JSON.write_text(
        json.dumps(
            {
                "fingerprint": report["shadow_fp"],
                "promote": False,
                "dethrone": deth.get("dethrone"),
                "dual_hits": report["dual_lab"]["hits"],
                "strategy": "aaron_method_hold",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {
                "shadow_fp": report["shadow_fp"],
                "dual_lab": report["dual_lab"],
                "dual_champ": report["dual_champ"],
                "dethrone": deth.get("dethrone"),
                "blockers": deth.get("blockers"),
                "has_hold_shape": report["curriculum"].get("has_hold_shape"),
                "production_replace": False,
                "day12_method_hold_pnl": (report.get("day12") or {})
                .get("lab_method_hold", {})
                .get("pnl"),
            },
            indent=2,
            default=str,
        ),
        flush=True,
    )
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Aaron method-rich hold train")
    p.add_argument("--steps", type=int, default=8000)
    p.add_argument("--dual-days", type=int, default=30)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--no-day12", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)
    run_aaron_method_hold_train(
        method_steps=int(args.steps),
        dual_days=int(args.dual_days),
        seed=int(args.seed),
        measure_day12=not args.no_day12,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
