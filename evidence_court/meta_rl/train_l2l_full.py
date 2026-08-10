"""Run L2L Proposals 2–10 train + freeze + dual scoreboard (north star)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import numpy as np

from .edge import build_tf_cache
from .goal_path import PRODUCTION_SCALPING_SLOTS_15M, run_goal_path_day
from .l2l_process import train_l2l_process_curriculum
from .policy import DEFAULT_CHAMPION_PATH, MetaPolicy
from .price_io import SYMBOL_FILES, available_symbols, bars_to_daily, load_m1_trailing_calendar_days

ART = Path("evidence_court/artifacts")
SHADOW = ART / "meta_policy_l2l_p2_p10.npz"
SHADOW_JSON = ART / "meta_policy_l2l_p2_p10.json"
REPORT = ART / "l2l_p2_p10_report.json"


def run_north_star_dual(
    policy_path: Path,
    *,
    n_days: int = 30,
    seed: int = 42,
) -> Dict[str, Any]:
    """Random target×risk dual; reports breach, a13 every day, pb+cont, freeze."""
    pol = MetaPolicy.load(policy_path, freeze=True, require_serious=False)
    pol.assert_frozen()
    fp0 = pol.weight_fingerprint()
    syms = [s for s in ("XAUUSD",) if s in available_symbols()]
    if not syms:
        syms = [s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()]
    warmup = 12
    trail = n_days + warmup + 8
    m1_by_sym = {}
    daily_by_sym = {}
    for sym in syms:
        path = SYMBOL_FILES.get(sym)
        if path and path.exists():
            m1 = load_m1_trailing_calendar_days(path, n_days=trail)
            if m1:
                m1_by_sym[sym] = m1
                daily_by_sym[sym] = bars_to_daily(m1)
    date_sets = [set(d["date"] for d in days) for days in daily_by_sym.values()]
    common = sorted(set.intersection(*date_sets)) if len(date_sets) > 1 else sorted(date_sets[0])
    window = common[-(n_days + warmup) :] if len(common) >= n_days + warmup else common
    eval_dates = window[warmup:][-n_days:]
    tf_cache = {s: build_tf_cache(m) for s, m in m1_by_sym.items()}
    rng = np.random.default_rng(seed)
    rows = []
    n_pb = n_ct = 0
    for date in eval_dates:
        t = float(rng.choice([5.0, 15.0, 30.0, 50.0, 70.0, 90.0]))
        r = float(rng.choice([1.0, 2.0, 3.0]))
        fills, ledger, gmeta = run_goal_path_day(
            pol,
            date=date,
            m1_by_symbol=m1_by_sym,
            target_percent=t,
            max_daily_risk_percent=r,
            symbols=list(m1_by_sym.keys()),
            tf_cache_by_symbol=tf_cache,
            slots=list(PRODUCTION_SCALPING_SLOTS_15M),
            brain_drives=True,
            watch_enabled=False,
        )
        pnl = float(ledger.realized_pnl_percent)
        loss = max(-pnl, 0.0)
        worst = float(ledger.worst_case_daily_loss_percent())
        breach = loss > r + 1e-6 or worst > r + 1e-6
        n_tr = len(fills)
        n_pb += int(gmeta.get("n_pullback") or 0)
        n_ct += int(gmeta.get("n_continuation") or 0)
        rows.append(
            {
                "day": date,
                "target": t,
                "risk": r,
                "pnl": pnl,
                "n_trades": n_tr,
                "hit": pnl >= t - 1e-9,
                "breach": breach,
                "a13_ok": 8 <= n_tr <= 400,
            }
        )
    pol.assert_frozen()
    fp1 = pol.weight_fingerprint()
    n = len(rows)
    return {
        "n_days": n,
        "hits": sum(1 for d in rows if d["hit"]),
        "hit_rate": sum(1 for d in rows if d["hit"]) / max(n, 1),
        "breach_count": sum(1 for d in rows if d["breach"]),
        "breach": any(d["breach"] for d in rows),
        "a13_every_day": all(d["a13_ok"] for d in rows) if rows else False,
        "a13_frac": sum(1 for d in rows if d["a13_ok"]) / max(n, 1),
        "n_zero": sum(1 for d in rows if d["n_trades"] == 0),
        "mean_tr": float(np.mean([d["n_trades"] for d in rows])) if rows else 0.0,
        "mean_pnl": float(np.mean([d["pnl"] for d in rows])) if rows else 0.0,
        "n_pullback_signals": n_pb,
        "n_continuation_signals": n_ct,
        "both_pb_and_cont": n_pb > 0 and n_ct > 0,
        "weights_frozen": fp0 == fp1,
        "fingerprint": fp1,
        "eval_start": eval_dates[0] if eval_dates else None,
        "eval_end": eval_dates[-1] if eval_dates else None,
        "meta_train_steps": int(pol.meta_train_steps),
    }


def run_l2l_full(
    *,
    steps: int = 6000,
    dual_days: int = 30,
    seed: int = 42,
    warmstart: bool = True,
) -> Dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    report: Dict[str, Any] = {
        "law": "L2L_PROJECT_ONE_BOT_100_DAYS",
        "ts": ts,
        "proposals": {},
    }
    if warmstart and Path(DEFAULT_CHAMPION_PATH).exists():
        pol = MetaPolicy.load(DEFAULT_CHAMPION_PATH, freeze=False, require_serious=False)
        pol.unlock_for_meta_train()
        report["warmstart_fp"] = pol.weight_fingerprint()
    else:
        from .policy import train_goal_conditioned_meta_policy

        pol = train_goal_conditioned_meta_policy(seed=seed, n_steps=1500, freeze=False)
        report["warmstart_fp"] = "from_curriculum"

    # P2–P7 process curriculum
    print("[L2L] P2–P7 process curriculum…", flush=True)
    cur = train_l2l_process_curriculum(pol.brain, steps=steps, seed=seed)
    report["proposals"]["P2_P7_curriculum"] = cur
    pol.trained = True
    pol.meta_train_steps = pol.brain.meta_train_steps

    # P8 lock weights
    print("[L2L] P8 freeze…", flush=True)
    pol.freeze_for_inference()
    pol.assert_frozen()
    fp_locked = pol.weight_fingerprint()
    report["proposals"]["P8_lock"] = {
        "frozen": True,
        "fingerprint": fp_locked,
        "meta_update_forbidden": True,
    }
    pol.save(SHADOW)
    SHADOW_JSON.write_text(
        json.dumps(
            {
                "fingerprint": fp_locked,
                "meta_train_steps": int(pol.meta_train_steps),
                "trained": True,
                "law": "L2L_P2_P10",
                "l2l_steps": steps,
                "promote": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # P9–P10 dual
    print(f"[L2L] P9–P10 dual days={dual_days}…", flush=True)
    dual = run_north_star_dual(SHADOW, n_days=dual_days, seed=seed)
    report["dual"] = dual
    report["proposals"]["P9_breach0"] = {
        "accept": dual["breach_count"] == 0,
        "breach_count": dual["breach_count"],
    }
    report["proposals"]["P10_a13_clear"] = {
        "a13_every_day": dual["a13_every_day"],
        "a13_frac": dual["a13_frac"],
        "hit_rate": dual["hit_rate"],
        "both_pb_and_cont": dual["both_pb_and_cont"],
        "accept_partial": dual["breach_count"] == 0
        and dual["both_pb_and_cont"]
        and dual["a13_frac"] >= 0.3,
    }
    # Final gate (full P1–P10) — mission promote only if all true
    final_ok = (
        dual["breach_count"] == 0
        and dual["weights_frozen"]
        and dual["both_pb_and_cont"]
        and dual["a13_every_day"]
        and dual["hit_rate"] > 0.05
    )
    report["final_promote_gate"] = {
        "ready": final_ok,
        "note": "Full 100d multi-seed still required for production PROMOTE per L2L §7",
        "measured_dual_days": dual_days,
    }
    report["shadow_path"] = str(SHADOW)
    REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps({"dual": dual, "final_promote_gate": report["final_promote_gate"]}, indent=2))
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=6000)
    p.add_argument("--dual-days", type=int, default=30)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args(list(argv) if argv is not None else None)
    run_l2l_full(steps=int(args.steps), dual_days=int(args.dual_days), seed=int(args.seed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
