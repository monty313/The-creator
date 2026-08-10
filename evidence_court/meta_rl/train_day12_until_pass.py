"""Day-12 conversion trainer — NOT fire-only same-day classification.

Arbitration (ARBITRATION_DAY12_CLEAR): clear days like 2026-01-21 by
**conversion learning**, not lot cosplay / fire-clone.

Rule
----
If a day misses target under a hard risk rail, do **not** keep training
fire-only behavior on that same day. Harvest outcome-tagged real path states
from **clear / dead / near-breach** days, include **wait / hold_convert /
size_down** teachers, and only mark promote-ready after a **fresh dual** shows
more target hits with **zero** breach.

Lab shadow only. Production champion never silently replaced.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .edge import build_tf_cache
from .goal_path import PRODUCTION_SCALPING_SLOTS_15M, run_goal_path_day
from .path_learning import (
    apply_conversion_path_teachers,
    conversion_remap_path_teacher,
    day_outcome_bucket,
    load_outcome_tagged_examples,
    path_learning_promote_guard,
    path_reanchor,
    sample_conversion_episode,
    apply_outcome_shaped_update,
    stamp_path_teacher_day_outcome,
    train_path_learning_curriculum,
    apply_outcome_tagged_path_teachers,
)
from .policy import DEFAULT_CHAMPION_PATH, MetaPolicy
from .price_io import SYMBOL_FILES, available_symbols, load_m1_trailing_calendar_days
from .train_learn_phase_20d import train_day12_drill, train_hold_r_flood
from .train_l2l_full import run_north_star_dual

ART = Path("evidence_court/artifacts")
SHADOW = ART / "meta_policy_day12_teacher.npz"
SHADOW_JSON = ART / "meta_policy_day12_teacher.json"
REPORT = ART / "day12_teacher_train_report.json"
OUTCOME_PACK = ART / "path_state_teachers_outcome_2x.json"
BASE_PACK = ART / "path_state_teachers_case0037.json"

DAY12 = "2026-01-21"
TARGET = 15.0
RISK = 3.0
MAX_ROUNDS = 12
DUAL_DAYS = 20
WIN_EPS = 0.02


def _load_m1_covering(date: str, n_trail: int = 120) -> Tuple[Dict[str, List], Dict[str, Any]]:
    m1_by: Dict[str, List] = {}
    for sym in ("XAUUSD", "EURUSD", "GBPUSD"):
        if sym not in available_symbols():
            continue
        path = SYMBOL_FILES.get(sym)
        if path is None or not path.exists():
            continue
        m1 = load_m1_trailing_calendar_days(path, n_days=n_trail)
        if not m1:
            continue
        dates = {b.get("date") for b in m1}
        if date not in dates:
            m1 = load_m1_trailing_calendar_days(path, n_days=max(n_trail, 400))
            dates = {b.get("date") for b in m1}
        if date in dates:
            m1_by[sym] = m1
    if not m1_by:
        return {}, {"error": f"no_m1_for_{date}"}
    return m1_by, {"symbols": list(m1_by.keys())}


def measure_day12(pol: MetaPolicy, m1_by: Dict[str, List], tf_cache: Dict) -> Dict[str, Any]:
    """Diagnostic re-sim of day 12 — not a fire-clone training source alone."""
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
        collect_path_state_teachers=True,
        max_path_state_teachers=200,
    )
    pnl = float(ledger.realized_pnl_percent)
    worst = float(ledger.worst_case_daily_loss_percent())
    loss = max(-pnl, 0.0)
    breach = loss > RISK + 1e-6 or worst > RISK + 1e-6
    hit = pnl >= TARGET - 1e-9
    bucket = day_outcome_bucket(
        day_pnl=pnl,
        target_percent=TARGET,
        max_daily_risk_percent=RISK,
        n_trades=len(fills),
        hit_target=hit,
        breach=breach,
    )

    fill_by_key: Dict[Tuple[str, str], Dict[str, Any]] = {}
    fill_rows: List[Dict[str, Any]] = []
    for f in fills:
        row = {
            "slot": str(f.slot),
            "symbol": str(f.symbol),
            "act": str(f.act),
            "pnl": float(f.pnl_percent),
            "size": float(f.size_risk_percent),
            "topology": str(f.topology),
        }
        fill_rows.append(row)
        fill_by_key[(row["symbol"], row["slot"])] = row

    stamped: List[Dict[str, Any]] = []
    for ex in gmeta.get("path_state_teachers") or []:
        if not isinstance(ex, dict):
            continue
        row = stamp_path_teacher_day_outcome(
            ex,
            day_pnl=pnl,
            target_percent=TARGET,
            max_daily_risk_percent=RISK,
            n_trades=len(fills),
        )
        row["day_bucket"] = bucket
        key = (str(row.get("symbol") or ""), str(row.get("asof_time") or ""))
        fr = fill_by_key.get(key)
        if fr is not None:
            row["fill_pnl"] = float(fr["pnl"])
            row["fill_act"] = str(fr["act"])
            row["has_fill"] = True
            if fr["pnl"] > WIN_EPS:
                row["fill_label"] = "win"
            elif fr["pnl"] < -WIN_EPS:
                row["fill_label"] = "loss"
            else:
                row["fill_label"] = "scratch"
        else:
            row["has_fill"] = False
            row["fill_label"] = "no_fill"
        # Conversion remap for harvest (wait/hold/size_down) — not fire clone
        stamped.append(conversion_remap_path_teacher(row))

    n_pos = sum(1 for r in fill_rows if r["pnl"] > WIN_EPS)
    n_neg = sum(1 for r in fill_rows if r["pnl"] <= WIN_EPS)
    return {
        "date": DAY12,
        "target": TARGET,
        "risk": RISK,
        "pnl": pnl,
        "n_trades": len(fills),
        "n_pos": n_pos,
        "n_neg": n_neg,
        "hit": hit,
        "breach": breach,
        "day_bucket": bucket,
        "progress": float(np.clip(pnl / TARGET, -1.0, 2.0)),
        "n_teachers": len(stamped),
        "teachers": stamped,
        "fills": fill_rows,
        "fingerprint": pol.weight_fingerprint(),
    }


def _load_multi_day_conversion_labs() -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """Harvest clear / dead / near-breach / progress from outcome packs."""
    labs = load_outcome_tagged_examples(
        [OUTCOME_PACK, BASE_PACK],
        max_examples=2200,
    )
    # Remap all to conversion labels
    remapped = [conversion_remap_path_teacher(ex) for ex in labs]
    counts: Dict[str, int] = {}
    for ex in remapped:
        b = str(ex.get("day_bucket") or "progress")
        counts[b] = counts.get(b, 0) + 1
    return remapped, counts


def _teach_conversion_round(
    brain: Any,
    *,
    multi_day_labs: Sequence[Dict[str, Any]],
    day12_labs: Sequence[Dict[str, Any]],
    round_i: int,
    seed: int,
) -> Dict[str, Any]:
    """Conversion primary. Day12 states used only as outcome-tagged conversion labs,
    never as fire-only clone of the same miss path.
    """
    if getattr(brain, "frozen_for_inference", False):
        brain.unlock_for_meta_train()

    # Mix: multi-day clear/dead/near-breach + light day12 conversion remap
    pool: List[Dict[str, Any]] = list(multi_day_labs)
    # Cap day12 contribution so we do not re-clone the miss day
    d12 = list(day12_labs)[: min(80, len(day12_labs))]
    for ex in d12:
        # force conversion remap again (wait/hold/size_down)
        pool.append(conversion_remap_path_teacher(ex))

    lr = 0.018 + 0.004 * min(round_i, 6)
    conv_apply = apply_conversion_path_teachers(
        brain,
        pool,
        lr=lr,
        seed=seed + round_i * 13,
        max_examples=1400,
        n_passes=2 + min(round_i // 2, 3),
        bucket_weights={"clear": 1.5, "dead": 1.35, "near_breach": 1.4, "progress": 1.0},
    )

    # Synthetic conversion flood (hold_convert / size_down / wait) — 15/3 pressure
    d12_drill = train_day12_drill(brain, steps=900 + round_i * 60, seed=seed + round_i)
    hold_n = train_hold_r_flood(brain, steps=500 + round_i * 40, seed=seed + 50 + round_i)

    # Full path-learning mix with sparse path anchors (not path-only)
    cur = train_path_learning_curriculum(
        brain,
        steps=1800 + round_i * 100,
        seed=seed + 70 + round_i,
        path_examples=list(multi_day_labs)[:600],
        path_anchor_frac=0.12,  # sparse — conversion primary
        holdout_frac=0.15,
        process_frac=0.10,
        lr=0.014,
        density_process=True,
    )

    # Light path re-anchor last (anti washout) — multi-day only, not day12 fire clone
    n_re = path_reanchor(
        brain,
        list(multi_day_labs)[:500],
        n_passes=1,
        seed=seed + 99 + round_i,
        max_examples=400,
    )

    # Extra explicit conversion episodes biased to wait/hold/size_down
    rng = np.random.default_rng(seed + round_i * 3)
    n_extra = 0
    class_extra: Dict[str, int] = {}
    for _ in range(400 + round_i * 30):
        st, ct, oc = sample_conversion_episode(rng, holdout_mode=False)
        # Bias away from pure fire_edge
        if ct.class_name == "fire_edge" and rng.random() < 0.55:
            side = 1 if ct.teacher_act == "long" else -1
            from .path_learning import conversion_teacher_from_context

            mode = str(rng.choice(["hold", "size_down", "wait_dead"]))
            if mode == "hold":
                ct2 = conversion_teacher_from_context(
                    progress_to_target=0.5,
                    risk_remaining_frac=0.55,
                    topology="continuation",
                    force_side=side,
                    outcome_score=0.5,
                )
            elif mode == "size_down":
                ct2 = conversion_teacher_from_context(
                    progress_to_target=0.18,
                    risk_remaining_frac=0.28,
                    topology="continuation",
                    force_side=side,
                    high_target=True,
                )
            else:
                ct2 = conversion_teacher_from_context(
                    progress_to_target=0.12,
                    risk_remaining_frac=0.7,
                    topology="chop",
                    force_side=0,
                    conflict=True,
                )
                oc = -0.4
            ct = ct2
        apply_outcome_shaped_update(
            brain,
            st,
            teacher_act=ct.teacher_act,
            outcome_score=oc,
            lr=0.016,
            teacher_size_frac=ct.teacher_size_frac,
            base_reward=1.2,
        )
        n_extra += 1
        class_extra[ct.class_name] = class_extra.get(ct.class_name, 0) + 1

    brain.trained = True
    return {
        "mode": "conversion_not_fire_clone",
        "conversion_apply": conv_apply,
        "day12_drill": d12_drill,
        "hold_r_flood": hold_n,
        "curriculum": {
            "has_conversion": cur.get("has_conversion"),
            "has_outcome_shaping": cur.get("has_outcome_shaping"),
            "path_only_clone": cur.get("path_only_clone"),
            "class_counts": cur.get("class_counts"),
            "path_anchor_frac_realized": cur.get("path_anchor_frac_realized"),
        },
        "n_reanchor": n_re,
        "n_extra_conversion": n_extra,
        "extra_class_counts": class_extra,
        "day12_labs_used": len(d12),
        "multi_day_labs": len(multi_day_labs),
        "fire_only_same_day": False,
    }


def run_day12_until_pass(
    *,
    max_rounds: int = MAX_ROUNDS,
    seed: int = 42,
    dual_days: int = DUAL_DAYS,
    run_dual_every: int = 2,
) -> Dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    report: Dict[str, Any] = {
        "law": "TEACHER_DAY12_CONVERSION",
        "arbitration": "ARBITRATION_DAY12_CLEAR",
        "rule": (
            "miss under risk rail → multi-day clear/dead/near-breach harvest; "
            "wait/hold_convert/size_down; dual gate; no fire-only same-day clone"
        ),
        "ts": ts,
        "day": DAY12,
        "target": TARGET,
        "risk": RISK,
        "max_rounds": max_rounds,
        "rounds": [],
        "production_replace": False,
        "production_champion_unchanged": True,
    }

    multi_day, bucket_counts = _load_multi_day_conversion_labs()
    report["multi_day_bucket_counts"] = bucket_counts
    report["n_multi_day_labs"] = len(multi_day)
    print(
        f"[day12-conv] multi-day labs={len(multi_day)} buckets={bucket_counts}",
        flush=True,
    )
    if len(multi_day) < 20:
        report["warning"] = "thin_multi_day_pack — conversion still runs on synthetics"

    m1_by, meta = _load_m1_covering(DAY12)
    if not m1_by:
        report["error"] = meta.get("error", "no_data")
        REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return report
    report["symbols"] = meta.get("symbols")
    tf_cache = {s: build_tf_cache(m) for s, m in m1_by.items()}

    pol = MetaPolicy.load(DEFAULT_CHAMPION_PATH, freeze=False, require_serious=False)
    pol.unlock_for_meta_train()
    report["warmstart_fp"] = pol.weight_fingerprint()

    print(f"[day12-conv] baseline diagnostic {DAY12} 15/3…", flush=True)
    base = measure_day12(pol, m1_by, tf_cache)
    report["baseline"] = {k: base[k] for k in base if k not in ("teachers", "fills")}
    print(
        json.dumps(
            {
                "pnl": base["pnl"],
                "n_trades": base["n_trades"],
                "n_pos": base["n_pos"],
                "n_neg": base["n_neg"],
                "day_bucket": base["day_bucket"],
                "hit": base["hit"],
            },
            indent=2,
        ),
        flush=True,
    )

    # Champion dual baseline (for promote guard comparison)
    print(f"[day12-conv] champ dual baseline {dual_days}d…", flush=True)
    dual_champ = run_north_star_dual(DEFAULT_CHAMPION_PATH, n_days=int(dual_days), seed=seed)
    report["dual_champ"] = {
        k: dual_champ.get(k)
        for k in (
            "hits",
            "a13_frac",
            "n_zero",
            "breach_count",
            "low_hr",
            "weights_frozen",
            "mean_pnl",
        )
        if k in dual_champ or True
    }
    # fill keys safely
    report["dual_champ"] = {
        "hits": int(dual_champ.get("hits") or 0),
        "a13_frac": float(dual_champ.get("a13_frac") or 0.0),
        "n_zero": int(dual_champ.get("n_zero") or 0),
        "breach_count": int(dual_champ.get("breach_count") or 0),
        "low_hr": dual_champ.get("low_hr"),
        "weights_frozen": bool(dual_champ.get("weights_frozen", True)),
        "mean_pnl": dual_champ.get("mean_pnl"),
    }
    print(json.dumps(report["dual_champ"], indent=2), flush=True)

    if base["hit"] and not base["breach"]:
        # Still need dual gate for promote-ready
        pol.freeze_for_inference()
        pol.save(SHADOW)
        dual_lab = run_north_star_dual(SHADOW, n_days=int(dual_days), seed=seed + 1)
        guard = path_learning_promote_guard(
            dual_lab,
            report["dual_champ"],
            has_outcome_conversion_mix=True,
            path_only_clone=False,
            court_promote=False,
        )
        report["passed_day12"] = True
        report["promote_ready"] = bool(
            guard.get("promote_lab")
            and int(dual_lab.get("hits") or 0) > int(report["dual_champ"]["hits"])
            and int(dual_lab.get("breach_count") or 0) == 0
        )
        report["dual_lab"] = {
            "hits": int(dual_lab.get("hits") or 0),
            "a13_frac": float(dual_lab.get("a13_frac") or 0.0),
            "breach_count": int(dual_lab.get("breach_count") or 0),
            "n_zero": int(dual_lab.get("n_zero") or 0),
        }
        report["guard"] = guard
        report["stop_reason"] = "day12_already_clear"
        report["production_replace"] = False
        REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
        return report

    best_pnl = float(base["pnl"])
    best_dual_hits = int(report["dual_champ"]["hits"])
    day12_memory: List[Dict[str, Any]] = list(base.get("teachers") or [])
    best_shadow_fp = None

    for r in range(1, int(max_rounds) + 1):
        print(f"[day12-conv] round {r}/{max_rounds} conversion teach…", flush=True)
        pol.unlock_for_meta_train()
        teach = _teach_conversion_round(
            pol.brain,
            multi_day_labs=multi_day,
            day12_labs=day12_memory,
            round_i=r,
            seed=seed,
        )
        pol.trained = True
        pol.meta_train_steps = pol.brain.meta_train_steps
        pol.freeze_for_inference()
        pol.assert_frozen()
        pol.save(SHADOW)

        print(f"[day12-conv] round {r} day12 diagnostic…", flush=True)
        m = measure_day12(pol, m1_by, tf_cache)
        # Merge conversion-labeled day12 states (capped) — never fire-only flood
        for ex in (m.get("teachers") or [])[:60]:
            day12_memory.append(ex)
        if len(day12_memory) > 400:
            day12_memory = day12_memory[-400:]

        row: Dict[str, Any] = {
            "round": r,
            "pnl": m["pnl"],
            "n_trades": m["n_trades"],
            "n_pos": m.get("n_pos"),
            "n_neg": m.get("n_neg"),
            "hit": m["hit"],
            "breach": m["breach"],
            "day_bucket": m.get("day_bucket"),
            "progress": m["progress"],
            "teach_summary": {
                "mode": teach.get("mode"),
                "fire_only_same_day": teach.get("fire_only_same_day"),
                "conversion_classes": (teach.get("conversion_apply") or {}).get("class_counts"),
                "buckets": (teach.get("conversion_apply") or {}).get("bucket_counts"),
                "has_wait": (teach.get("conversion_apply") or {}).get("has_wait"),
                "has_hold_convert": (teach.get("conversion_apply") or {}).get("has_hold_convert"),
                "has_size_down": (teach.get("conversion_apply") or {}).get("has_size_down"),
                "curriculum_path_only_clone": (teach.get("curriculum") or {}).get(
                    "path_only_clone"
                ),
            },
            "fingerprint": m["fingerprint"],
        }

        # Dual on schedule or when day12 improved
        do_dual = (r % max(1, int(run_dual_every)) == 0) or m["hit"] or (
            m["pnl"] > best_pnl + 0.15
        )
        if do_dual:
            print(f"[day12-conv] round {r} fresh dual {dual_days}d…", flush=True)
            dual_lab = run_north_star_dual(SHADOW, n_days=int(dual_days), seed=seed + r)
            guard = path_learning_promote_guard(
                dual_lab,
                report["dual_champ"],
                has_outcome_conversion_mix=True,
                path_only_clone=bool(
                    (teach.get("curriculum") or {}).get("path_only_clone")
                ),
                court_promote=False,
            )
            d_hits = int(dual_lab.get("hits") or 0)
            d_breach = int(dual_lab.get("breach_count") or 0)
            row["dual"] = {
                "hits": d_hits,
                "a13_frac": float(dual_lab.get("a13_frac") or 0.0),
                "n_zero": int(dual_lab.get("n_zero") or 0),
                "breach_count": d_breach,
                "mean_pnl": dual_lab.get("mean_pnl"),
            }
            row["guard"] = {
                "promote_lab": guard.get("promote_lab"),
                "production_replace": guard.get("production_replace"),
                "floor_hold": guard.get("floor_hold"),
                "reasons": guard.get("reasons"),
            }
            # Promote-ready: more hits than champ dual, zero breach, conversion mix
            promote_ready = bool(
                d_breach == 0
                and d_hits > int(report["dual_champ"]["hits"])
                and guard.get("promote_lab")
            )
            row["promote_ready"] = promote_ready
            if d_hits > best_dual_hits and d_breach == 0:
                best_dual_hits = d_hits
                best_shadow_fp = m["fingerprint"]
                SHADOW_JSON.write_text(
                    json.dumps(
                        {
                            "fingerprint": m["fingerprint"],
                            "day12_pnl": m["pnl"],
                            "day12_hit": m["hit"],
                            "dual_hits": d_hits,
                            "dual_breach": d_breach,
                            "promote": False,
                            "promote_ready": promote_ready,
                            "strategy": "conversion_not_fire_clone",
                        },
                        indent=2,
                    ),
                    encoding="utf-8",
                )
            if promote_ready and m["hit"] and not m["breach"]:
                report["passed_day12"] = True
                report["promote_ready"] = True
                report["stop_reason"] = "day12_clear_and_dual_promote_ready"
                report["winning_round"] = r
                report["final"] = {k: m[k] for k in m if k not in ("teachers", "fills")}
                report["dual_lab"] = row["dual"]
                report["guard"] = row["guard"]
                report["rounds"].append(row)
                print(json.dumps(row, indent=2, default=str), flush=True)
                break
            if promote_ready and not m["hit"]:
                # Dual improved but day12 not clear — keep training conversion
                print(
                    f"[day12-conv] dual promote_ready hits={d_hits} but day12 still miss",
                    flush=True,
                )

        if m["pnl"] > best_pnl and not m["breach"]:
            best_pnl = float(m["pnl"])
            SHADOW_JSON.write_text(
                json.dumps(
                    {
                        "fingerprint": m["fingerprint"],
                        "day12_pnl": m["pnl"],
                        "day12_hit": m["hit"],
                        "best_day12_pnl": best_pnl,
                        "promote": False,
                        "strategy": "conversion_not_fire_clone",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

        report["rounds"].append(row)
        print(json.dumps(row, indent=2, default=str), flush=True)
    else:
        report["passed_day12"] = bool(
            report["rounds"]
            and report["rounds"][-1].get("hit")
            and not report["rounds"][-1].get("breach")
        )
        # Final dual if last round skipped
        if report["rounds"] and "dual" not in report["rounds"][-1]:
            print("[day12-conv] final dual…", flush=True)
            dual_lab = run_north_star_dual(SHADOW, n_days=int(dual_days), seed=seed + 99)
            guard = path_learning_promote_guard(
                dual_lab,
                report["dual_champ"],
                has_outcome_conversion_mix=True,
                path_only_clone=False,
                court_promote=False,
            )
            report["dual_lab"] = {
                "hits": int(dual_lab.get("hits") or 0),
                "a13_frac": float(dual_lab.get("a13_frac") or 0.0),
                "n_zero": int(dual_lab.get("n_zero") or 0),
                "breach_count": int(dual_lab.get("breach_count") or 0),
            }
            report["guard"] = guard
            report["promote_ready"] = bool(
                int(dual_lab.get("breach_count") or 0) == 0
                and int(dual_lab.get("hits") or 0) > int(report["dual_champ"]["hits"])
                and guard.get("promote_lab")
            )
        else:
            last = report["rounds"][-1] if report["rounds"] else {}
            report["promote_ready"] = bool(last.get("promote_ready"))
            if "dual" in last:
                report["dual_lab"] = last["dual"]
            if "guard" in last:
                report["guard"] = last["guard"]
        report["stop_reason"] = (
            "day12_clear_dual_not_ready"
            if report.get("passed_day12") and not report.get("promote_ready")
            else "max_rounds_conversion_incomplete"
        )
        report["best_day12_pnl"] = best_pnl
        report["best_dual_hits"] = best_dual_hits

    report["shadow_path"] = str(SHADOW)
    report["production_replace"] = False
    report["production_champion_unchanged"] = True
    report["best_day12_pnl"] = best_pnl
    REPORT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(
        json.dumps(
            {
                "passed_day12": report.get("passed_day12"),
                "promote_ready": report.get("promote_ready"),
                "stop_reason": report.get("stop_reason"),
                "baseline_pnl": report["baseline"].get("pnl"),
                "best_day12_pnl": best_pnl,
                "dual_champ_hits": report["dual_champ"].get("hits"),
                "dual_lab": report.get("dual_lab"),
                "rounds": len(report["rounds"]),
                "production_replace": False,
            },
            indent=2,
            default=str,
        ),
        flush=True,
    )
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Day12 conversion trainer (not fire-clone)")
    p.add_argument("--max-rounds", type=int, default=MAX_ROUNDS)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--dual-days", type=int, default=DUAL_DAYS)
    p.add_argument("--dual-every", type=int, default=2)
    args = p.parse_args(list(argv) if argv is not None else None)
    run_day12_until_pass(
        max_rounds=int(args.max_rounds),
        seed=int(args.seed),
        dual_days=int(args.dual_days),
        run_dual_every=int(args.dual_every),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
