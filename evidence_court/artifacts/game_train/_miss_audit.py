"""Audit pullback/continuation misses for a shadow policy (Watch + path-state)."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from evidence_court.meta_rl.edge import build_tf_cache
from evidence_court.meta_rl.goal_path import run_goal_path_day
from evidence_court.meta_rl.policy import MetaPolicy
from evidence_court.meta_rl.price_io import (
    SYMBOL_FILES,
    available_symbols,
    bars_to_daily,
    load_m1_trailing_calendar_days,
)

N_DAYS = 16
SEED = 42
DEFAULT_POL = Path("evidence_court/artifacts/game_train/meta_policy_forge_learn.npz")
DEFAULT_OUT = Path("evidence_court/artifacts/game_train/learn_miss_audit16.json")


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--policy",
        type=str,
        default=str(DEFAULT_POL),
        help="path to policy npz",
    )
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--days", type=int, default=N_DAYS)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument(
        "--aggressive",
        action="store_true",
        help="goal_path aggressive_capture (multi-sym / FX lift)",
    )
    args = ap.parse_args(argv)
    aggressive = bool(args.aggressive)
    pol_path = Path(args.policy)
    out_path = Path(args.out) if args.out else (
        Path("evidence_court/artifacts/game_train/residual_miss_audit16.json")
        if "residual" in pol_path.name
        else DEFAULT_OUT
    )
    n_days = int(args.days)
    seed = int(args.seed)

    pol = MetaPolicy.load(pol_path, freeze=True, require_serious=False)
    print("fp", pol.weight_fingerprint(), "steps", pol.meta_train_steps)

    syms = [s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()]
    trail = n_days + 20
    m1_by: dict = {}
    tf_cache: dict = {}
    daily_by: dict = {}
    for sym in syms:
        p = SYMBOL_FILES.get(sym)
        if not p or not p.exists():
            continue
        m1 = load_m1_trailing_calendar_days(p, n_days=trail)
        if not m1:
            continue
        m1_by[sym] = m1
        daily_by[sym] = bars_to_daily(m1)
        tf_cache[sym] = build_tf_cache(m1)

    date_sets = [set(d["date"] for d in days) for days in daily_by.values()]
    common = sorted(set.intersection(*date_sets)) if len(date_sets) > 1 else sorted(date_sets[0])
    eval_dates = common[-n_days:]

    rng = np.random.default_rng(seed)
    day_rows = []
    miss_topo: Counter = Counter()
    miss_band: Counter = Counter()
    miss_sym: Counter = Counter()
    hit_topo: Counter = Counter()
    path_miss_topo: Counter = Counter()
    totals = {
        "n_days": 0,
        "n_trades": 0,
        "n_zero": 0,
        "n_pullback_sensor": 0,
        "n_continuation_sensor": 0,
        "watch_opportunities": 0,
        "watch_hits": 0,
        "watch_misses": 0,
        "watch_miss_pb": 0,
        "watch_miss_cont": 0,
        "watch_lnny_misses": 0,
        "curriculum_labels": 0,
        "path_state_misses": 0,
        "path_miss_pb": 0,
        "path_miss_cont": 0,
        "fills_pb": 0,
        "fills_cont": 0,
    }

    for i, date in enumerate(eval_dates):
        t = float(rng.choice([5.0, 15.0, 30.0, 50.0, 70.0]))
        r = float(rng.choice([1.0, 2.0, 3.0]))
        fills, ledger, gmeta = run_goal_path_day(
            pol,
            date=date,
            m1_by_symbol=m1_by,
            target_percent=t,
            max_daily_risk_percent=r,
            symbols=list(m1_by.keys()),
            tf_cache_by_symbol=tf_cache,
            brain_drives=True,
            watch_enabled=True,
            collect_path_state_teachers=True,
            max_path_state_teachers=200,
            aggressive_capture=aggressive,
        )
        n_tr = len(fills)
        n_pb = int(gmeta.get("n_pullback") or 0)
        n_ct = int(gmeta.get("n_continuation") or 0)
        w_miss = int(gmeta.get("watch_n_misses") or 0)
        w_hit = int(gmeta.get("watch_n_hits") or 0)
        w_opp = int(gmeta.get("watch_n_opportunities") or 0)
        w_ln = int(gmeta.get("watch_n_london_ny_misses") or 0)
        labs = list(gmeta.get("curriculum_labels") or [])
        lab_total = int(gmeta.get("curriculum_labels_total") or len(labs))
        path_teachers = list(gmeta.get("path_state_teachers") or [])

        miss_pb = sum(1 for L in labs if L.get("topology") == "pullback_resume")
        miss_ct = sum(1 for L in labs if L.get("topology") == "continuation")
        # scale sampled topo to full label total if capped
        sampled = miss_pb + miss_ct
        if sampled > 0 and lab_total > sampled:
            scale = lab_total / sampled
            est_pb = int(round(miss_pb * scale))
            est_ct = int(round(miss_ct * scale))
        else:
            est_pb, est_ct = miss_pb, miss_ct

        p_pb = sum(1 for x in path_teachers if x.get("topology") == "pullback_resume")
        p_ct = sum(1 for x in path_teachers if x.get("topology") == "continuation")
        f_pb = sum(
            1
            for f in fills
            if getattr(f, "topology", None) == "pullback_resume"
            or getattr(f, "edge_kind", None) == "pullback_resume"
        )
        f_ct = sum(
            1
            for f in fills
            if getattr(f, "topology", None) == "continuation"
            or getattr(f, "edge_kind", None) == "continuation"
        )

        for L in labs:
            miss_topo[str(L.get("topology"))] += 1
            miss_band[str(L.get("session_band"))] += 1
            miss_sym[str(L.get("symbol"))] += 1
        for x in path_teachers:
            path_miss_topo[str(x.get("topology"))] += 1
        for f in fills:
            hit_topo[str(getattr(f, "topology", getattr(f, "edge_kind", "")))] += 1

        totals["n_days"] += 1
        totals["n_trades"] += n_tr
        totals["n_zero"] += 1 if n_tr == 0 else 0
        totals["n_pullback_sensor"] += n_pb
        totals["n_continuation_sensor"] += n_ct
        totals["watch_opportunities"] += w_opp
        totals["watch_hits"] += w_hit
        totals["watch_misses"] += w_miss
        totals["watch_miss_pb"] += est_pb
        totals["watch_miss_cont"] += est_ct
        totals["watch_lnny_misses"] += w_ln
        totals["curriculum_labels"] += lab_total
        totals["path_state_misses"] += len(path_teachers)
        totals["path_miss_pb"] += p_pb
        totals["path_miss_cont"] += p_ct
        totals["fills_pb"] += f_pb
        totals["fills_cont"] += f_ct

        day_rows.append(
            {
                "date": date,
                "target": t,
                "risk": r,
                "n_trades": n_tr,
                "pnl": float(ledger.realized_pnl_percent),
                "sensor_pb": n_pb,
                "sensor_cont": n_ct,
                "watch_opp": w_opp,
                "watch_hits": w_hit,
                "watch_misses": w_miss,
                "watch_miss_pb_est": est_pb,
                "watch_miss_cont_est": est_ct,
                "curriculum_labels_total": lab_total,
                "path_miss_pb": p_pb,
                "path_miss_cont": p_ct,
                "path_miss_total": len(path_teachers),
                "fills_pb": f_pb,
                "fills_cont": f_ct,
                "hit_target": bool(ledger.realized_pnl_percent >= t - 1e-9),
            }
        )
        print(
            f"{date} tr={n_tr:3d} path_miss_pb={p_pb:3d} path_miss_ct={p_ct:3d} "
            f"watch_miss={w_miss:4d} (pb~{est_pb} ct~{est_ct}) "
            f"fill_pb={f_pb} fill_ct={f_ct} opp={w_opp} hits={w_hit}"
        )

    opp = totals["watch_opportunities"]
    hits = totals["watch_hits"]
    misses = totals["watch_misses"]
    summary = {
        "policy": str(pol_path),
        "fingerprint": pol.weight_fingerprint(),
        "meta_train_steps": int(pol.meta_train_steps),
        "aggressive_capture": aggressive,
        "n_days": totals["n_days"],
        "window": [eval_dates[0], eval_dates[-1]] if eval_dates else [],
        "symbols": list(m1_by.keys()),
        "totals": totals,
        "mean_trades": totals["n_trades"] / max(totals["n_days"], 1),
        "watch_capture_rate": hits / max(opp, 1),
        "watch_miss_rate": misses / max(opp, 1),
        "missed_pullbacks_watch_est": totals["watch_miss_pb"],
        "missed_continuations_watch_est": totals["watch_miss_cont"],
        "missed_pullbacks_path_state": totals["path_miss_pb"],
        "missed_continuations_path_state": totals["path_miss_cont"],
        "taken_pullbacks": totals["fills_pb"],
        "taken_continuations": totals["fills_cont"],
        "pb_capture_path_view": totals["fills_pb"]
        / max(totals["fills_pb"] + totals["path_miss_pb"], 1),
        "cont_capture_path_view": totals["fills_cont"]
        / max(totals["fills_cont"] + totals["path_miss_cont"], 1),
        "miss_topo_sampled_labels": dict(miss_topo),
        "path_miss_topo": dict(path_miss_topo),
        "fill_topo": dict(hit_topo),
        "miss_band_sampled": dict(miss_band),
        "miss_sym_sampled": dict(miss_sym),
        "days": day_rows,
        "notes": [
            "sensor_pb/cont count edge scans across slots (multi-count sets/slots).",
            "watch_misses = A28 Opportunity Watch complaints (opportunity + bot wrong/wait).",
            "curriculum_labels_total = full miss count; topo split estimated if day labels capped at 200.",
            "path_state_misses = brain waited on real Mark candidate (collect_path_state_teachers).",
        ],
    }
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("--- SUMMARY ---")
    print(json.dumps({k: summary[k] for k in summary if k != "days"}, indent=2))
    print("wrote", out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
