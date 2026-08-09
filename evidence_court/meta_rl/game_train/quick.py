"""One-command Policy Forge loop (A34) — pull → ingest forge_v1 → fast score.

Never touches production champion.

Usage (from repo root):
  python -m evidence_court.meta_rl.cli forge go
  python -m evidence_court.meta_rl.cli forge play
  python -m evidence_court.meta_rl.cli forge pull
  python -m evidence_court.meta_rl.cli forge ingest
  python -m evidence_court.meta_rl.cli forge score
  python evidence_court/meta_rl/game_train/quick.py go
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from evidence_court.meta_rl.brain import sample_brain_state
from evidence_court.meta_rl.forward_eval import compute_goal_consistency, run_forward_eval
from evidence_court.meta_rl.game_train.ingest import ingest_game_pack, load_pack
from evidence_court.meta_rl.policy import MetaPolicy
from evidence_court.meta_rl.state import META_RL_DIM

GT = _REPO / "evidence_court" / "artifacts" / "game_train"
ART = _REPO / "evidence_court" / "artifacts"
FORGE_NPZ = GT / "meta_policy_forge_v1.npz"
FORGE_JSON = GT / "meta_policy_forge_v1.json"
INGESTED_LOG = GT / "forge_v1_ingested.jsonl"
SCORE_JSON = GT / "forge_v1_quick_score.json"
CHAMPION = ART / "meta_policy_champion.npz"

# Drop zones scanned for new exports
DROP_GLOBS = (
    Path.home() / "Downloads",
    ART,  # accidental drops next to champion
    GT,
)


def _packs_in(dir_path: Path) -> List[Path]:
    if not dir_path.is_dir():
        return []
    return sorted(dir_path.glob("policy_forge_export_*.json"))


def _read_ingested() -> set[str]:
    done: set[str] = set()
    if not INGESTED_LOG.exists():
        return done
    for line in INGESTED_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            done.add(json.loads(line).get("file", ""))
        except Exception:
            pass
    return {x for x in done if x}


def _append_ingested(row: Dict[str, Any]) -> None:
    GT.mkdir(parents=True, exist_ok=True)
    with INGESTED_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def pull() -> Dict[str, Any]:
    """Copy new policy_forge_export_*.json from Downloads / artifacts → game_train."""
    GT.mkdir(parents=True, exist_ok=True)
    existing = {p.name for p in _packs_in(GT)}
    copied: List[str] = []
    seen_src: set[str] = set()
    for root in DROP_GLOBS:
        if root.resolve() == GT.resolve():
            continue
        for src in _packs_in(root):
            key = str(src.resolve())
            if key in seen_src:
                continue
            seen_src.add(key)
            if src.name in existing:
                continue
            dest = GT / src.name
            shutil.copy2(src, dest)
            copied.append(src.name)
            existing.add(src.name)
            # clean accidental drop next to champion
            if src.parent.resolve() == ART.resolve() and src.name.startswith("policy_forge_export_"):
                try:
                    src.unlink()
                except Exception:
                    pass
    packs = _packs_in(GT)
    return {
        "copied": copied,
        "n_copied": len(copied),
        "n_packs_in_game_train": len(packs),
        "latest": packs[-1].name if packs else None,
        "game_train": str(GT),
    }


def _pack_summary(path: Path) -> Dict[str, Any]:
    d = load_pack(path)
    traj = list(d.get("trajectories") or [])
    acts = Counter(str(t.get("teacher_act") or "?") for t in traj)
    sess = Counter(str(t.get("session") or "?") for t in traj)
    fire = acts.get("long", 0) + acts.get("short", 0)
    n = max(len(traj), 1)
    sb = d.get("scoreboard") if isinstance(d.get("scoreboard"), dict) else {}
    return {
        "file": path.name,
        "n_traj": len(traj),
        "wait": acts.get("wait", 0),
        "long": acts.get("long", 0),
        "short": acts.get("short", 0),
        "fire_density": fire / n,
        "sessions": dict(sess),
        "align_rate": sb.get("align_rate"),
        "browser_steps": (d.get("brain") or {}).get("meta_train_steps")
        if isinstance(d.get("brain"), dict)
        else None,
    }


def ingest(
    *,
    newest_only: bool = True,
    all_new: bool = False,
    lr: float = 0.02,
    force_reprocess: bool = False,
) -> Dict[str, Any]:
    """Ingest into forge_v1 only. Default: newest pack not yet logged."""
    GT.mkdir(parents=True, exist_ok=True)
    packs = _packs_in(GT)
    if not packs:
        return {"error": "no_packs", "hint": "Export from Policy Forge then: forge pull"}

    done = _read_ingested()
    if force_reprocess:
        targets = packs[-1:] if newest_only and not all_new else packs
    elif all_new:
        targets = [p for p in packs if p.name not in done]
        if not targets:
            return {
                "n_applied_total": 0,
                "message": "all packs already ingested",
                "latest": packs[-1].name,
                "forge_steps": _forge_steps(),
            }
    else:
        # newest only if not yet ingested; else re-ingest newest (user just played)
        latest = packs[-1]
        if latest.name in done and not force_reprocess:
            # still allow re-ingest of newest — user often wants "I just exported"
            targets = [latest]
            reprocess = True
        else:
            targets = [latest]
            reprocess = latest.name in done
        # if only newest and already done, still run once (explicit user intent via go/ingest)
        _ = reprocess

    results = []
    for i, pack in enumerate(targets):
        from_prior = (not FORGE_NPZ.exists()) and i == 0 and not done
        # first ever pack on empty forge track
        if not FORGE_NPZ.exists():
            from_prior = True
        rep = ingest_game_pack(
            pack,
            out_path=FORGE_NPZ,
            lr=lr,
            from_prior=from_prior,
            seed=42,
        )
        row = {
            "file": pack.name,
            "n_traj": rep.n_traj,
            "n_applied": rep.n_applied,
            "mean_loss": rep.mean_loss,
            "steps_before": rep.meta_train_steps_before,
            "steps_after": rep.meta_train_steps_after,
            "fp_after": rep.fingerprint_after,
            "pack": _pack_summary(pack),
        }
        results.append(row)
        _append_ingested(
            {
                "file": pack.name,
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "n_applied": rep.n_applied,
                "steps_after": rep.meta_train_steps_after,
            }
        )

    # champion safety check
    champ_ok = True
    champ_fp = None
    if CHAMPION.exists():
        try:
            c = MetaPolicy.load(CHAMPION, freeze=True, require_serious=False)
            champ_fp = c.weight_fingerprint()
            champ_ok = "meta9600" in champ_fp or c.meta_train_steps >= 5000
        except Exception:
            champ_ok = False

    return {
        "ingested": results,
        "n_packs": len(results),
        "n_applied_total": sum(r["n_applied"] for r in results),
        "forge_steps": _forge_steps(),
        "forge_path": str(FORGE_NPZ),
        "champion_untouched_check": champ_ok,
        "champion_fp": champ_fp,
    }


def _forge_steps() -> Optional[int]:
    if not FORGE_JSON.exists():
        return None
    try:
        return int(json.loads(FORGE_JSON.read_text(encoding="utf-8")).get("meta_train_steps") or 0)
    except Exception:
        return None


def _pad(raw) -> np.ndarray:
    s = np.asarray(raw, dtype=np.float64).reshape(-1)
    out = np.zeros(META_RL_DIM, dtype=np.float64)
    n = min(META_RL_DIM, int(s.size))
    out[:n] = s[:n]
    return out


def score(
    *,
    days: int = 8,
    seed: int = 42,
    vs_champion: bool = False,
) -> Dict[str, Any]:
    """Fast score: coach on newest pack + opp synth + short forward (forge only by default)."""
    t0 = time.time()
    if not FORGE_NPZ.exists():
        return {"error": "no_forge", "hint": "forge ingest first"}

    forge = MetaPolicy.load(FORGE_NPZ, freeze=True, require_serious=False)
    packs = _packs_in(GT)
    latest = packs[-1] if packs else None
    out: Dict[str, Any] = {
        "forge_steps": forge.meta_train_steps,
        "forge_fp": forge.weight_fingerprint(),
        "latest_pack": latest.name if latest else None,
    }

    # coach on newest
    if latest:
        d = load_pack(latest)
        traj = list(d.get("trajectories") or [])
        ok = fire_ok = fire_n = wait_pred = 0
        for t in traj:
            st = _pad(t.get("state") or [])
            pred = forge.forward(st).act
            y = str(t.get("teacher_act") or "wait")
            if pred == y:
                ok += 1
            if pred == "wait":
                wait_pred += 1
            if y in ("long", "short"):
                fire_n += 1
                if pred == y:
                    fire_ok += 1
        n = max(len(traj), 1)
        acts = Counter(str(t.get("teacher_act")) for t in traj)
        sess = Counter(str(t.get("session")) for t in traj)
        out["coach"] = {
            "n": len(traj),
            "agree": ok / n,
            "fire_side": fire_ok / max(fire_n, 1),
            "fire_n": fire_n,
            "pred_wait": wait_pred / n,
            "label_fire_density": (acts.get("long", 0) + acts.get("short", 0)) / n,
            "sessions": dict(sess),
        }

    # synthetic opp (fast)
    rng = np.random.default_rng(7)
    ok = fire_ok = fire_n = wait_on_fire = 0
    n_opp = 200
    for _ in range(n_opp):
        st, teacher, _sf = sample_brain_state(
            rng,
            target=float(rng.choice([5.0, 15.0, 50.0, 90.0])),
            risk=float(rng.choice([1.0, 2.0, 3.0])),
            london_ny=True,
            force_opp=True,
        )
        pred = forge.forward(st).act
        if pred == teacher:
            ok += 1
        if teacher in ("long", "short"):
            fire_n += 1
            if pred == teacher:
                fire_ok += 1
            if pred == "wait":
                wait_on_fire += 1
    out["opportunity"] = {
        "n": n_opp,
        "agree": ok / n_opp,
        "fire_side": fire_ok / max(fire_n, 1),
        "miss_wait_on_fire": wait_on_fire / max(fire_n, 1),
    }

    # short forward forge only
    t1 = time.time()
    rep = run_forward_eval(
        n_days=int(days),
        seed=seed,
        champion_path=FORGE_NPZ,
        pair_mode="random",
    )
    trades = [d.n_trades for d in rep.day_results]
    _gc_ok, gc = compute_goal_consistency(rep.day_results, rep.pair_results)
    a13 = sum(1 for t in trades if 8 <= t <= 400)
    n = max(len(trades), 1)
    out["forward"] = {
        "n_days": rep.n_days,
        "breach_count": rep.breach_count,
        "no_retrain": rep.no_retrain,
        "total_trades": int(sum(trades)),
        "mean_trades_per_day": float(np.mean(trades)) if trades else 0.0,
        "a13_day_frac": a13 / n,
        "zero_trade_days": sum(1 for t in trades if t == 0),
        "total_hits": int(gc.get("total_hits", 0)),
        "low_hit_rate": float(gc.get("low_hit_rate", 0.0)),
        "mean_pnl": float(np.mean([d.pnl_percent for d in rep.day_results])) if rep.day_results else 0.0,
        "promote_ready": bool(rep.promote_ready),
        "elapsed_s": time.time() - t1,
        "window": {
            "start": rep.metadata.get("window_start"),
            "end": rep.metadata.get("window_end"),
        },
    }

    if vs_champion and CHAMPION.exists():
        t2 = time.time()
        rep_c = run_forward_eval(
            n_days=int(days),
            seed=seed,
            champion_path=CHAMPION,
            pair_mode="random",
        )
        trades_c = [d.n_trades for d in rep_c.day_results]
        _ok2, gc_c = compute_goal_consistency(rep_c.day_results, rep_c.pair_results)
        a13c = sum(1 for t in trades_c if 8 <= t <= 400)
        out["champion_forward"] = {
            "total_trades": int(sum(trades_c)),
            "mean_trades_per_day": float(np.mean(trades_c)) if trades_c else 0.0,
            "a13_day_frac": a13c / max(len(trades_c), 1),
            "total_hits": int(gc_c.get("total_hits", 0)),
            "elapsed_s": time.time() - t2,
        }

    # human-readable delta hints
    fw = out["forward"]
    opp = out["opportunity"]
    out["verdict"] = {
        "helped_if": "trades>0 and miss_wait_on_fire falling",
        "trades_ok_start": fw["total_trades"] > 0,
        "still_too_quiet": fw["mean_trades_per_day"] < 2.0,
        "opp_still_weak": opp["miss_wait_on_fire"] > 0.4,
        "breach_ok": fw["breach_count"] == 0,
        "promote": False,
    }
    out["elapsed_s"] = time.time() - t0
    SCORE_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    out["saved"] = str(SCORE_JSON)
    return out


def play() -> int:
    """Launch Policy Forge browser."""
    from evidence_court.meta_rl.game_train.launch_policy_forge import main as launch_main

    return int(launch_main())


def go(
    *,
    days: int = 8,
    vs_champion: bool = False,
    all_new: bool = False,
) -> Dict[str, Any]:
    """pull → ingest newest → fast score. One command."""
    t0 = time.time()
    pulled = pull()
    ing = ingest(newest_only=not all_new, all_new=all_new)
    sc = score(days=days, vs_champion=vs_champion)
    return {
        "pull": pulled,
        "ingest": ing,
        "score": sc,
        "elapsed_s": time.time() - t0,
        "next": "Play more London/NY fire → Export → forge go",
    }


def _print(obj: Any) -> None:
    print(json.dumps(obj, indent=2, default=str))


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="forge",
        description="Policy Forge fast loop (forge_v1 only; champion safe)",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("pull", help="Copy exports from Downloads/artifacts → game_train/")
    sub.add_parser("play", help="Open Policy Forge in browser")

    ing = sub.add_parser("ingest", help="Ingest newest pack into forge_v1")
    ing.add_argument("--all-new", action="store_true", help="All packs not yet logged")
    ing.add_argument("--lr", type=float, default=0.02)

    sc = sub.add_parser("score", help="Fast coach+opp+short forward (default 8d, forge only)")
    sc.add_argument("--days", type=int, default=8)
    sc.add_argument("--vs-champion", action="store_true", help="Also run champion forward (slow)")
    sc.add_argument("--seed", type=int, default=42)

    g = sub.add_parser("go", help="pull + ingest newest + fast score (default path)")
    g.add_argument("--days", type=int, default=8)
    g.add_argument("--vs-champion", action="store_true")
    g.add_argument("--all-new", action="store_true")

    sub.add_parser("status", help="Show packs + forge steps")

    v2 = sub.add_parser(
        "train-v2",
        help="Train forge_v2: balanced force/load/launch (not wait-copy); champion safe",
    )
    v2.add_argument("--steps", type=int, default=4000)
    v2.add_argument("--lr", type=float, default=0.02)
    v2.add_argument("--fire-frac", type=float, default=0.45)
    v2.add_argument("--synth-frac", type=float, default=0.30)
    v2.add_argument("--warmstart-v1", action="store_true")
    v2.add_argument("--continue", dest="cont", action="store_true")

    ix = sub.add_parser(
        "train-intense",
        help="UNHINGED fire flood: path-state + real-bar + L/NY synth (champion safe)",
    )
    ix.add_argument("--steps", type=int, default=20000)
    ix.add_argument("--lr", type=float, default=0.035)
    ix.add_argument("--fire-frac", type=float, default=0.75)
    ix.add_argument("--path-frac", type=float, default=0.40)
    ix.add_argument("--real-bar-frac", type=float, default=0.15)
    ix.add_argument("--synth-frac", type=float, default=0.20)
    ix.add_argument("--multi-hit", type=int, default=16)
    ix.add_argument("--warmstart-v2", action="store_true")
    ix.add_argument("--continue", dest="cont", action="store_true")

    ln = sub.add_parser(
        "train-learn",
        help="LEARN not memorize: unique teachers, holdout dates, L2L+goal aug (champion safe)",
    )
    ln.add_argument("--steps", type=int, default=24000)
    ln.add_argument("--lr", type=float, default=0.018)
    ln.add_argument("--path-frac", type=float, default=0.35)
    ln.add_argument("--synth-frac", type=float, default=0.30)
    ln.add_argument("--wait-frac", type=float, default=0.15)
    ln.add_argument("--noise", type=float, default=0.04)
    ln.add_argument("--holdout-frac", type=float, default=0.25)
    ln.add_argument("--warmstart-intense", action="store_true")
    ln.add_argument("--continue", dest="cont", action="store_true")

    rs = sub.add_parser(
        "train-residual",
        help="Residual: train on actual Watch PB/cont misses (EURUSD/cont boost, no multi-hit)",
    )
    rs.add_argument("--steps", type=int, default=16000)
    rs.add_argument("--lr", type=float, default=0.016)
    rs.add_argument("--miss-frac", type=float, default=0.65)
    rs.add_argument("--harvest-days", type=int, default=16)
    rs.add_argument("--no-reharvest", action="store_true")
    rs.add_argument("--no-aggressive", action="store_true")

    args = p.parse_args(list(argv) if argv is not None else None)

    if args.cmd == "pull":
        _print(pull())
        return 0
    if args.cmd == "play":
        return play()
    if args.cmd == "ingest":
        _print(ingest(all_new=bool(args.all_new), lr=float(args.lr)))
        return 0
    if args.cmd == "score":
        _print(score(days=int(args.days), vs_champion=bool(args.vs_champion), seed=int(args.seed)))
        return 0
    if args.cmd == "go":
        _print(
            go(
                days=int(args.days),
                vs_champion=bool(args.vs_champion),
                all_new=bool(args.all_new),
            )
        )
        return 0
    if args.cmd == "status":
        packs = _packs_in(GT)
        done = _read_ingested()
        v2p = GT / "meta_policy_forge_v2.npz"
        v2_steps = None
        if (GT / "meta_policy_forge_v2.json").exists():
            try:
                v2_steps = json.loads((GT / "meta_policy_forge_v2.json").read_text(encoding="utf-8")).get(
                    "meta_train_steps"
                )
            except Exception:
                pass
        _print(
            {
                "game_train": str(GT),
                "n_packs": len(packs),
                "latest": packs[-1].name if packs else None,
                "forge_v1_steps": _forge_steps(),
                "forge_v1_exists": FORGE_NPZ.exists(),
                "forge_v2_exists": v2p.exists(),
                "forge_v2_steps": v2_steps,
                "ingested_log_n": len(done),
                "not_in_log": [p.name for p in packs if p.name not in done][-5:],
            }
        )
        return 0
    if args.cmd == "train-v2":
        from evidence_court.meta_rl.game_train.forge_v2 import train_forge_v2

        rep = train_forge_v2(
            steps=int(args.steps),
            lr=float(args.lr),
            fire_frac=float(args.fire_frac),
            synth_frac=float(args.synth_frac),
            from_prior=not bool(args.cont) and not bool(args.warmstart_v1),
            warmstart_forge_v1=bool(args.warmstart_v1),
        )
        _print(rep)
        return 0
    if args.cmd == "train-intense":
        from evidence_court.meta_rl.game_train.forge_intense import train_forge_intense

        rep = train_forge_intense(
            steps=int(args.steps),
            lr=float(args.lr),
            fire_frac=float(args.fire_frac),
            path_frac=float(args.path_frac),
            real_bar_frac=float(args.real_bar_frac),
            synth_frac=float(args.synth_frac),
            multi_hit=int(args.multi_hit),
            from_prior=not bool(args.cont) and not bool(args.warmstart_v2),
            warmstart_forge_v2=bool(args.warmstart_v2),
            warmstart_intense=bool(args.cont),
        )
        _print(rep)
        return 0
    if args.cmd == "train-learn":
        from evidence_court.meta_rl.game_train.forge_learn import train_forge_learn

        rep = train_forge_learn(
            steps=int(args.steps),
            lr=float(args.lr),
            path_frac=float(args.path_frac),
            synth_frac=float(args.synth_frac),
            wait_frac=float(args.wait_frac),
            noise=float(args.noise),
            holdout_frac=float(args.holdout_frac),
            from_prior=not bool(args.cont) and not bool(args.warmstart_intense),
            warmstart_intense=bool(args.warmstart_intense),
            warmstart_learn=bool(args.cont),
        )
        _print(rep)
        return 0
    if args.cmd == "train-residual":
        from evidence_court.meta_rl.game_train.residual_miss import train_residual_miss

        rep = train_residual_miss(
            steps=int(args.steps),
            lr=float(args.lr),
            miss_frac=float(args.miss_frac),
            reharvest=not bool(args.no_reharvest),
            harvest_days=int(args.harvest_days),
            warmstart_learn=True,
            aggressive_capture=not bool(args.no_aggressive),
        )
        _print(rep)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
