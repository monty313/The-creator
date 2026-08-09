"""Performance test: forge_v1 (game-trained) vs production champion on real path.

Does NOT overwrite champion. Writes forge_v1_performance.json + prints summary.
"""
from __future__ import annotations

import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.brain import sample_brain_state
from evidence_court.meta_rl.forward_eval import (
    compute_goal_consistency,
    run_forward_eval,
    save_report,
)
from evidence_court.meta_rl.policy import MetaPolicy
from evidence_court.meta_rl.state import META_RL_DIM

GT = Path(__file__).resolve().parent
FORGE = GT / "meta_policy_forge_v1.npz"
CHAMP = ROOT / "evidence_court" / "artifacts" / "meta_policy_champion.npz"
OUT = GT / "forge_v1_performance.json"
# newest export by filename sort (timestamp in name)
_packs = sorted(GT.glob("policy_forge_export_*.json"))
LATEST = _packs[-1] if _packs else GT / "policy_forge_export_missing.json"

# Practical window: enough days for signal without multi-hour run
N_DAYS = 25
SEED = 42


def pad(raw) -> np.ndarray:
    s = np.asarray(raw, dtype=np.float64).reshape(-1)
    out = np.zeros(META_RL_DIM, dtype=np.float64)
    n = min(META_RL_DIM, int(s.size))
    out[:n] = s[:n]
    return out


def coach_perf(pol: MetaPolicy, pack_path: Path) -> Dict[str, Any]:
    data = json.loads(pack_path.read_text(encoding="utf-8"))
    traj = list(data.get("trajectories") or [])
    correct = 0
    fire_ok = fire_n = 0
    wait_pred = 0
    by_sess: Dict[str, Counter] = defaultdict(Counter)
    by_topo: Dict[str, Counter] = defaultdict(Counter)
    pred_dist = Counter()
    true_dist = Counter()
    ces: List[float] = []
    for t in traj:
        y = str(t.get("teacher_act") or "wait")
        st = pad(t.get("state") or [])
        pred = pol.forward(st).act
        true_dist[y] += 1
        pred_dist[pred] += 1
        if pred == "wait":
            wait_pred += 1
        if pred == y:
            correct += 1
        # CE from softmax of brain
        logits, _, _ = pol.brain.forward_raw(st)
        z = np.asarray(logits, dtype=np.float64).reshape(-1)[:3]
        e = np.exp(z - np.max(z))
        p = e / e.sum()
        yi = {"wait": 0, "long": 1, "short": 2}.get(y, 0)
        ces.append(float(-np.log(max(float(p[yi]), 1e-12))))
        if y in ("long", "short"):
            fire_n += 1
            if pred == y:
                fire_ok += 1
        sess = str(t.get("session") or "?")
        topo = str(t.get("sense_topology") or "?")
        by_sess[sess]["n"] += 1
        by_sess[sess]["ok"] += int(pred == y)
        by_topo[topo]["n"] += 1
        by_topo[topo]["ok"] += int(pred == y)
    n = max(len(traj), 1)
    return {
        "pack": pack_path.name,
        "n": len(traj),
        "coach_agreement": correct / n,
        "mean_ce": float(np.mean(ces)) if ces else None,
        "fire_side_accuracy": fire_ok / max(fire_n, 1),
        "fire_n": fire_n,
        "pred_wait_frac": wait_pred / n,
        "true_wait_frac": true_dist.get("wait", 0) / n,
        "pred_dist": dict(pred_dist),
        "true_dist": dict(true_dist),
        "by_session": {
            k: {"n": v["n"], "agree": v["ok"] / max(v["n"], 1)} for k, v in by_sess.items()
        },
        "by_topology": {
            k: {"n": v["n"], "agree": v["ok"] / max(v["n"], 1)} for k, v in by_topo.items()
        },
    }


def opportunity_curriculum_perf(pol: MetaPolicy, n: int = 400, seed: int = 7) -> Dict[str, Any]:
    """Synthetic London/NY opportunity states — does forge fire when teacher says fire?"""
    rng = np.random.default_rng(seed)
    correct = fire_ok = fire_n = wait_when_fire = 0
    pred_dist = Counter()
    for _ in range(n):
        target = float(rng.choice([5.0, 15.0, 50.0, 90.0]))
        risk = float(rng.choice([1.0, 2.0, 3.0]))
        st, teacher, _sf = sample_brain_state(
            rng, target=target, risk=risk, london_ny=True, force_opp=True
        )
        pred = pol.forward(st).act
        pred_dist[pred] += 1
        if pred == teacher:
            correct += 1
        if teacher in ("long", "short"):
            fire_n += 1
            if pred == teacher:
                fire_ok += 1
            if pred == "wait":
                wait_when_fire += 1
    return {
        "n": n,
        "london_ny_force_opp": True,
        "coach_agreement": correct / max(n, 1),
        "fire_n": fire_n,
        "fire_side_accuracy": fire_ok / max(fire_n, 1),
        "miss_rate_wait_on_fire": wait_when_fire / max(fire_n, 1),
        "pred_dist": dict(pred_dist),
    }


def summarize_forward(report) -> Dict[str, Any]:
    days = report.day_results
    n = len(days)
    trades = [d.n_trades for d in days]
    pnls = [d.pnl_percent for d in days]
    a13_days = sum(1 for t in trades if 8 <= t <= 400)
    gc_ok, gc = compute_goal_consistency(days, report.pair_results)
    return {
        "n_days": n,
        "breach_count": report.breach_count,
        "no_retrain": report.no_retrain,
        "promote_ready": report.promote_ready,
        "l2l_day_path_ok": report.l2l_day_path_ok,
        "senses_day_path_ok": report.senses_day_path_ok,
        "goal_consistency_ok": report.goal_consistency_ok,
        "total_hits": int(gc.get("total_hits", 0)),
        "low_hit_rate": float(gc.get("low_hit_rate", 0.0)),
        "mid_hit_rate": float(gc.get("mid_hit_rate", 0.0)),
        "mean_pnl": float(np.mean(pnls)) if pnls else 0.0,
        "median_pnl": float(np.median(pnls)) if pnls else 0.0,
        "total_trades": int(sum(trades)),
        "mean_trades_per_day": float(np.mean(trades)) if trades else 0.0,
        "median_trades_per_day": float(np.median(trades)) if trades else 0.0,
        "a13_day_frac": a13_days / max(n, 1),
        "a13_days": a13_days,
        "zero_trade_days": sum(1 for t in trades if t == 0),
        "hit_days": sum(1 for d in days if d.hit_target),
        "policy_fingerprint": report.metadata.get("policy_fingerprint"),
        "meta_train_steps": report.metadata.get("meta_train_steps"),
        "policy_source": report.metadata.get("policy_source"),
        "window": {
            "start": report.metadata.get("window_start"),
            "end": report.metadata.get("window_end"),
        },
        "goal_consistency": gc,
        "pair_results": report.pair_results,
    }


def main() -> int:
    t0 = time.time()
    forge = MetaPolicy.load(FORGE, freeze=True, require_serious=False)
    champ = MetaPolicy.load(CHAMP, freeze=True, require_serious=False)

    print("=== COACH (latest clean game pack) ===")
    coach_f = coach_perf(forge, LATEST)
    coach_c = coach_perf(champ, LATEST)
    print("forge ", json.dumps({k: coach_f[k] for k in ("coach_agreement", "mean_ce", "fire_side_accuracy", "pred_wait_frac")}, indent=2))
    print("champ ", json.dumps({k: coach_c[k] for k in ("coach_agreement", "mean_ce", "fire_side_accuracy", "pred_wait_frac")}, indent=2))

    print("\n=== OPPORTUNITY CURRICULUM (synthetic London/NY force_opp) ===")
    opp_f = opportunity_curriculum_perf(forge)
    opp_c = opportunity_curriculum_perf(champ)
    print("forge ", json.dumps(opp_f, indent=2))
    print("champ ", json.dumps(opp_c, indent=2))

    print(f"\n=== FORWARD PATH ({N_DAYS}d, seed={SEED}) forge_v1 ===")
    t1 = time.time()
    rep_f = run_forward_eval(
        n_days=N_DAYS,
        seed=SEED,
        champion_path=FORGE,
        pair_mode="random",
    )
    sum_f = summarize_forward(rep_f)
    print(json.dumps({k: sum_f[k] for k in sum_f if k not in ("pair_results", "goal_consistency")}, indent=2))
    print(f"  elapsed_s={time.time()-t1:.1f}")

    print(f"\n=== FORWARD PATH ({N_DAYS}d, seed={SEED}) production champion ===")
    t2 = time.time()
    rep_c = run_forward_eval(
        n_days=N_DAYS,
        seed=SEED,
        champion_path=CHAMP,
        pair_mode="random",
    )
    sum_c = summarize_forward(rep_c)
    print(json.dumps({k: sum_c[k] for k in sum_c if k not in ("pair_results", "goal_consistency")}, indent=2))
    print(f"  elapsed_s={time.time()-t2:.1f}")

    # save forge forward report artifact
    save_report(rep_f, GT / "forge_v1_forward25_report.json")

    out = {
        "track": "meta_policy_forge_v1",
        "law": "A34_performance_test",
        "n_days_forward": N_DAYS,
        "seed": SEED,
        "forge_fingerprint": forge.weight_fingerprint(),
        "champion_fingerprint": champ.weight_fingerprint(),
        "champion_untouched": True,
        "coach_latest_pack": {"forge": coach_f, "champion": coach_c},
        "opportunity_synthetic": {"forge": opp_f, "champion": opp_c},
        "forward": {"forge": sum_f, "champion": sum_c},
        "verdict": {
            "coach_fit_strong": coach_f["coach_agreement"] >= 0.9,
            "opp_fire_weak": opp_f["miss_rate_wait_on_fire"] >= 0.5,
            "forward_breach_ok": sum_f["breach_count"] == 0,
            "forward_a13_weak": sum_f["a13_day_frac"] < 0.5,
            "beats_champ_hits": sum_f["total_hits"] > sum_c["total_hits"],
            "beats_champ_a13": sum_f["a13_day_frac"] > sum_c["a13_day_frac"],
            "promote_ready": bool(sum_f["promote_ready"]),
        },
        "elapsed_s": time.time() - t0,
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT}")
    print("VERDICT", json.dumps(out["verdict"], indent=2))
    print(f"TOTAL elapsed_s={out['elapsed_s']:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
