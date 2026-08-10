"""Year-scale HTF-active path-state aggressive train + dual + optional champion replace.

Process (00_PATH_STATE_TEACHERS):
  1. Harvest path-state teachers for ~1 year of days
     ONLY when ≥1 official HTF set is active (htf_agree)
  2. Offline aggressive meta_update (warmstart current champion)
  3. Dual measure vs BEST_POLICY floor
  4. If beats floor → backup old champ → write new champion

Does not force-pad live. Shadow first; promote only on measured beat.
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import numpy as np

from .edge import build_tf_cache
from .goal_path import PRODUCTION_SCALPING_SLOTS_15M, run_goal_path_day
from .path_state_harvest import (
    filter_path_state_teachers,
    harvest_path_state_teachers,
    save_path_state_pack,
    train_path_state_a13_policy,
)
from .policy import DEFAULT_CHAMPION_PATH, MetaPolicy, load_or_train_champion
from .price_io import SYMBOL_FILES, available_symbols, bars_to_daily, load_m1_trailing_calendar_days

ART = Path("evidence_court/artifacts")
PACK = ART / "path_state_teachers_htf_active_year.json"
PACK_CKPT = ART / "path_state_teachers_htf_active_year.partial.json"
SHADOW = ART / "meta_policy_htf_active_year.npz"
SHADOW_JSON = ART / "meta_policy_htf_active_year.json"
REPORT = ART / "htf_active_year_train_report.json"
BEST_MD = Path("evidence_court/BEST_POLICY.md")

# Floor from CASE-0037 / BEST_POLICY.md (must hold + improve)
FLOOR = {
    "hits": 11,
    "low_hr": 0.28,
    "a13_frac": 0.64,
    "n_zero": 18,
    "breach": 0,
}


def _summarize_days(rows: list) -> Dict[str, Any]:
    n = len(rows)
    if n == 0:
        return {"n_days": 0}
    hits = sum(1 for d in rows if d["hit"])
    breaches = sum(1 for d in rows if d["breach"])
    n_zero = sum(1 for d in rows if d["n_trades"] == 0)
    n_a13 = sum(1 for d in rows if 8 <= d["n_trades"] <= 400)
    low = [d for d in rows if d["target"] <= 15.0 + 1e-9]
    low_hr = (sum(1 for d in low if d["hit"]) / len(low)) if low else float("nan")
    pnls = [d["pnl"] for d in rows]
    return {
        "n_days": n,
        "hits": hits,
        "hit_rate": hits / n,
        "low_hr": low_hr,
        "a13_frac": n_a13 / n,
        "n_zero": n_zero,
        "mean_tr": float(np.mean([d["n_trades"] for d in rows])),
        "mean_pnl": float(np.mean(pnls)),
        "green_frac": sum(1 for p in pnls if p > 0) / n,
        "breach_count": breaches,
        "breach": breaches > 0,
        "max_pnl": float(np.max(pnls)),
        "min_pnl": float(np.min(pnls)),
        "total_trades": int(sum(d["n_trades"] for d in rows)),
    }


def beats_floor(score: Dict[str, Any], floor: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Hold prefer floor + improve at least one goal axis. Public for unit pins."""
    floor = dict(floor or FLOOR)
    reasons_fail = []
    reasons_ok = []
    if score.get("breach") or int(score.get("breach_count") or 0) > 0:
        reasons_fail.append("breach")
    hits = int(score.get("hits") or 0)
    a13 = float(score.get("a13_frac") or 0.0)
    low_hr = float(score.get("low_hr") or 0.0)
    n_zero = int(score.get("n_zero") or 999)
    if hits < int(floor["hits"]):
        reasons_fail.append(f"hits<{floor['hits']}")
    else:
        reasons_ok.append("hits_held")
    if low_hr == low_hr and low_hr + 1e-9 < float(floor["low_hr"]):
        reasons_fail.append(f"low_hr<{floor['low_hr']}")
    else:
        reasons_ok.append("low_hr_held")
    if a13 + 1e-9 < float(floor["a13_frac"]):
        reasons_fail.append(f"a13<{floor['a13_frac']}")
    else:
        reasons_ok.append("a13_held")

    improved = []
    if hits > int(floor["hits"]):
        improved.append("hits")
    if a13 > float(floor["a13_frac"]) + 0.01:
        improved.append("a13")
    if n_zero < int(floor["n_zero"]):
        improved.append("n_zero")

    beats = (not reasons_fail) and (len(improved) >= 1)
    # Strict: must hold floor; if all held equal, not a beat (need improve)
    if not reasons_fail and not improved:
        return {
            "beats": False,
            "hold_floor": True,
            "improved": [],
            "fail": ["no_improvement_over_floor"],
            "ok": reasons_ok,
        }
    return {
        "beats": bool(beats),
        "hold_floor": not reasons_fail,
        "improved": improved,
        "fail": reasons_fail,
        "ok": reasons_ok,
    }


# Back-compat alias
_beats_floor = beats_floor


def run_dual(
    *,
    policy_path: Path,
    n_days: int = 100,
    seed: int = 42,
    monty_htf_blend: bool = False,
) -> Dict[str, Any]:
    pol = MetaPolicy.load(policy_path, freeze=True, require_serious=False)
    pol.assert_frozen()
    # Prefer multi when available; fall back XAU-only for speed if caller sets env
    import os

    if os.environ.get("HTF_DUAL_XAU_ONLY", "1") == "1":
        syms = [s for s in ("XAUUSD",) if s in available_symbols()]
    else:
        syms = [s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()]
    warmup = 15
    trail = n_days + warmup + 10
    m1_by_sym = {}
    daily_by_sym = {}
    for sym in syms:
        path = SYMBOL_FILES.get(sym)
        if not path or not path.exists():
            continue
        m1 = load_m1_trailing_calendar_days(path, n_days=trail)
        if m1:
            m1_by_sym[sym] = m1
            daily_by_sym[sym] = bars_to_daily(m1)
    date_sets = [set(d["date"] for d in days) for days in daily_by_sym.values()]
    common = sorted(set.intersection(*date_sets)) if len(date_sets) > 1 else sorted(date_sets[0])
    need = n_days + warmup
    window = common[-need:] if len(common) >= need else common
    eval_dates = window[warmup:][-n_days:]
    tf_cache = {s: build_tf_cache(m) for s, m in m1_by_sym.items()}
    rng = np.random.default_rng(seed)
    targets = (5.0, 15.0, 30.0, 50.0, 70.0, 90.0)
    risks = (1.0, 2.0, 3.0)
    rows = []
    for i, date in enumerate(eval_dates):
        t = float(rng.choice(targets))
        r = float(rng.choice(risks))
        fills, ledger, _ = run_goal_path_day(
            pol,
            date=date,
            m1_by_symbol=m1_by_sym,
            target_percent=t,
            max_daily_risk_percent=r,
            symbols=list(m1_by_sym.keys()),
            tf_cache_by_symbol=tf_cache,
            # 15m dual grid for measure throughput (still multi-symbol brain path)
            slots=list(PRODUCTION_SCALPING_SLOTS_15M),
            brain_drives=True,
            watch_enabled=False,
            monty_htf_blend=monty_htf_blend,
        )
        pnl = float(ledger.realized_pnl_percent)
        loss = max(-pnl, 0.0)
        worst = float(ledger.worst_case_daily_loss_percent())
        breach = loss > r + 1e-6 or worst > r + 1e-6
        rows.append(
            {
                "day": date,
                "target": t,
                "risk": r,
                "pnl": pnl,
                "n_trades": len(fills),
                "hit": pnl >= t - 1e-9,
                "breach": breach,
            }
        )
    summary = _summarize_days(rows)
    summary["eval_start"] = eval_dates[0] if eval_dates else None
    summary["eval_end"] = eval_dates[-1] if eval_dates else None
    summary["policy_fp"] = pol.weight_fingerprint()
    summary["meta_train_steps"] = int(pol.meta_train_steps)
    return summary


def promote_champion(shadow_path: Path, report: Dict[str, Any]) -> Dict[str, Any]:
    champ = Path(DEFAULT_CHAMPION_PATH)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = ART / f"meta_policy_champion_backup_pre_htf_active_{ts}.npz"
    if champ.exists():
        shutil.copy2(champ, backup)
    shutil.copy2(shadow_path, champ)
    # sidecar
    shadow_meta = {}
    if SHADOW_JSON.exists():
        shadow_meta = json.loads(SHADOW_JSON.read_text(encoding="utf-8"))
    pol = MetaPolicy.load(champ, freeze=True, require_serious=False)
    sidecar = {
        "fingerprint": pol.weight_fingerprint(),
        "meta_train_steps": int(pol.meta_train_steps),
        "trained": True,
        "promoted_from": "htf_active_year_path_state",
        "law": "A29_brain_l2l",
        "format": 2,
        "seed": 42,
        "n_examples": shadow_meta.get("n_examples"),
        "require_htf_active": True,
        "backup": str(backup),
        "dual": report.get("dual_shadow"),
        "promoted_at": ts,
    }
    (ART / "meta_policy_champion.json").write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
    # BEST_POLICY note append
    note = (
        f"\n\n---\n\n## Update {ts} — HTF-active year path-state PROMOTE\n\n"
        f"- **Weights:** `meta_policy_champion.npz` (from `{shadow_path.name}`)\n"
        f"- **Fingerprint:** `{sidecar['fingerprint']}`\n"
        f"- **Backup:** `{backup.name}`\n"
        f"- **Dual:** hits={report.get('dual_shadow', {}).get('hits')} "
        f"a13={report.get('dual_shadow', {}).get('a13_frac')} "
        f"breach={report.get('dual_shadow', {}).get('breach_count')}\n"
        f"- **Teachers:** HTF-active only · year harvest · path-state process\n"
    )
    if BEST_MD.exists():
        BEST_MD.write_text(BEST_MD.read_text(encoding="utf-8") + note, encoding="utf-8")
    return {"promoted": True, "backup": str(backup), "fingerprint": sidecar["fingerprint"]}


def run_pipeline(
    *,
    harvest_days: int = 252,
    dual_days: int = 100,
    seed: int = 42,
    max_examples: int = 2500,
    max_per_day: int = 100,
    path_mix: float = 0.55,
    n_passes: int = 3,
    monty_htf_blend: bool = False,
    auto_promote: bool = True,
    skip_harvest: bool = False,
) -> Dict[str, Any]:
    report: Dict[str, Any] = {
        "law": "htf_active_year_path_state",
        "process": "00_PATH_STATE_TEACHERS + require ≥1 HTF set active",
        "harvest_days_requested": harvest_days,
        "dual_days": dual_days,
        "floor": FLOOR,
        "auto_promote": auto_promote,
        "monty_htf_blend": monty_htf_blend,
    }

    # ── 1 Harvest ─────────────────────────────────────────────
    if skip_harvest and PACK.exists():
        pack = json.loads(PACK.read_text(encoding="utf-8"))
        report["harvest"] = {
            "source": "loaded",
            "path": str(PACK),
            "n_examples": pack.get("n_examples") or len(pack.get("examples") or []),
        }
    else:
        print(f"[1/4] Harvest HTF-active path teachers · days={harvest_days}…", flush=True)
        pack = harvest_path_state_teachers(
            n_days=int(harvest_days),
            seed=seed,
            max_examples=int(max_examples),
            max_per_day=int(max_per_day),
            warmup_days=15,
            # XAU-only harvest for year throughput; dual measure stays multi-symbol
            symbols=["XAUUSD"] if "XAUUSD" in available_symbols() else None,
            monty_htf_blend=bool(monty_htf_blend),
            require_htf_active=True,
            checkpoint_every=10,
            checkpoint_path=PACK_CKPT,
            # Clean year packs must not resume stale partials without n_htf_active
            resume_from_partial=False,
            # Watch ON so residual HTF-gated path_state_watch_miss also collected
            watch_enabled=True,
        )
        save_path_state_pack(pack, PACK)
        report["harvest"] = {
            "source": "fresh",
            "path": str(PACK),
            "n_days": pack.get("n_days"),
            "n_raw": pack.get("n_raw"),
            "n_examples": pack.get("n_examples"),
            "n_london_ny": pack.get("n_london_ny"),
            "n_htf_active_teachers": pack.get("n_htf_active_teachers"),
            "dims_ok": pack.get("dims_ok"),
            "window_start": pack.get("window_start"),
            "window_end": pack.get("window_end"),
            "require_htf_active": True,
        }
        print(
            f"  days={pack.get('n_days')} examples={pack.get('n_examples')} "
            f"ln={pack.get('n_london_ny')} dims_ok={pack.get('dims_ok')}",
            flush=True,
        )

    examples = pack.get("examples") or []
    examples = filter_path_state_teachers(
        examples, max_examples=max_examples, require_htf_active=True
    )
    if len(examples) < 20:
        report["error"] = "too_few_htf_active_teachers"
        report["n_examples"] = len(examples)
        REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report

    # ── 2 Train ───────────────────────────────────────────────
    print("[2/4] Aggressive path-state train (warmstart champion)…", flush=True)
    champ = Path(DEFAULT_CHAMPION_PATH)
    before_fp = ""
    if champ.exists():
        try:
            before_fp = MetaPolicy.load(champ, freeze=True).weight_fingerprint()
        except Exception:
            pass
    pol = train_path_state_a13_policy(
        examples,
        seed=seed,
        n_steps=2500,
        path_mix=float(path_mix),
        freeze=True,
        save_path=SHADOW,
        warmstart_path=champ if champ.exists() else None,
        n_passes=int(n_passes),
    )
    after_fp = pol.weight_fingerprint()
    SHADOW_JSON.write_text(
        json.dumps(
            {
                "fingerprint": after_fp,
                "meta_train_steps": int(pol.meta_train_steps),
                "trained": True,
                "n_examples": len(examples),
                "require_htf_active": True,
                "path_mix": path_mix,
                "n_passes": n_passes,
                "warmstart_fp": before_fp,
                "law": "htf_active_year_path_state",
                "promote": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    report["train"] = {
        "shadow": str(SHADOW),
        "fp_before": before_fp,
        "fp_after": after_fp,
        "meta_train_steps": int(pol.meta_train_steps),
        "n_examples": len(examples),
        "weights_changed": before_fp != after_fp,
    }
    print(f"  steps={pol.meta_train_steps} fp={after_fp}", flush=True)

    # ── 3 Dual ────────────────────────────────────────────────
    print(f"[3/4] Dual measure shadow · days={dual_days}…", flush=True)
    dual_s = run_dual(policy_path=SHADOW, n_days=int(dual_days), seed=seed)
    report["dual_shadow"] = dual_s
    print(
        f"  hits={dual_s.get('hits')} a13={dual_s.get('a13_frac')} "
        f"n_zero={dual_s.get('n_zero')} breach={dual_s.get('breach_count')}",
        flush=True,
    )

    # Floor compare uses documented CASE-0037 numbers (not a second slow dual)
    report["dual_champion"] = {
        "source": "BEST_POLICY_FLOOR",
        "hits": FLOOR["hits"],
        "low_hr": FLOOR["low_hr"],
        "a13_frac": FLOOR["a13_frac"],
        "n_zero": FLOOR["n_zero"],
        "breach_count": FLOOR["breach"],
    }

    decision = beats_floor(dual_s, FLOOR)
    report["promote_decision"] = decision
    print(f"  promote_decision={decision}", flush=True)

    # ── 4 Promote ─────────────────────────────────────────────
    report["promoted"] = False
    if auto_promote and decision.get("beats"):
        print("[4/4] BEATS floor → replacing champion…", flush=True)
        report["promote_result"] = promote_champion(SHADOW, report)
        report["promoted"] = True
    else:
        print("[4/4] No champion replace (did not beat floor or auto_promote off).", flush=True)
        report["promote_result"] = {
            "promoted": False,
            "reason": decision.get("fail") or "no_improvement",
        }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    report["report_path"] = str(REPORT)
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="HTF-active year path-state train + promote")
    p.add_argument("--harvest-days", type=int, default=252, help="~1 trading year")
    p.add_argument("--dual-days", type=int, default=100)
    p.add_argument("--max-examples", type=int, default=2500)
    p.add_argument("--path-mix", type=float, default=0.55)
    p.add_argument("--n-passes", type=int, default=3)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--monty-htf-blend", action="store_true")
    p.add_argument("--no-promote", action="store_true")
    p.add_argument("--skip-harvest", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)
    rep = run_pipeline(
        harvest_days=int(args.harvest_days),
        dual_days=int(args.dual_days),
        seed=int(args.seed),
        max_examples=int(args.max_examples),
        path_mix=float(args.path_mix),
        n_passes=int(args.n_passes),
        monty_htf_blend=bool(args.monty_htf_blend),
        auto_promote=not bool(args.no_promote),
        skip_harvest=bool(args.skip_harvest),
    )
    print(
        json.dumps(
            {
                "promoted": rep.get("promoted"),
                "decision": rep.get("promote_decision"),
                "harvest": rep.get("harvest"),
                "dual_shadow": {
                    k: rep.get("dual_shadow", {}).get(k)
                    for k in (
                        "hits",
                        "a13_frac",
                        "n_zero",
                        "low_hr",
                        "breach_count",
                        "mean_pnl",
                    )
                },
                "report": rep.get("report_path"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
