"""Inventory packs, support forge_v1 eval (A34). Ingest is done via CLI."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.game_train.ingest import load_pack
from evidence_court.meta_rl.policy import MetaPolicy
from evidence_court.meta_rl.state import META_RL_DIM

GT = Path(__file__).resolve().parent
OUT_NPZ = GT / "meta_policy_forge_v1.npz"
OUT_JSON = GT / "meta_policy_forge_v1.json"
ACTS = ("wait", "long", "short")
ACT_I = {a: i for i, a in enumerate(ACTS)}


def pad_state(raw) -> np.ndarray:
    s = np.asarray(raw, dtype=np.float64).reshape(-1)
    out = np.zeros(META_RL_DIM, dtype=np.float64)
    n = min(META_RL_DIM, int(s.size))
    out[:n] = s[:n]
    return out


def inventory():
    files = sorted(GT.glob("policy_forge_export_*.json"))
    rows = []
    print(f"PACKS: {len(files)}")
    print("=" * 90)
    for p in files:
        d = load_pack(p)
        traj = list(d.get("trajectories") or [])
        acts = Counter()
        days = set()
        sessions = set()
        for t in traj:
            a = str(t.get("teacher_act") or "?")
            acts[a] += 1
            for key_src in (t, t.get("meta") if isinstance(t.get("meta"), dict) else {}):
                if not isinstance(key_src, dict):
                    continue
                if "day_index" in key_src:
                    days.add(key_src["day_index"])
                if "session" in key_src:
                    sessions.add(str(key_src["session"]))
        sb = d.get("scoreboard") if isinstance(d.get("scoreboard"), dict) else {}
        align = d.get("align_rate", sb.get("align_rate", sb.get("align", "n/a")))
        brain = d.get("brain") if isinstance(d.get("brain"), dict) else {}
        meta_steps = d.get("meta_train_steps", brain.get("meta_train_steps", "n/a"))
        day_top = d.get("day_index", d.get("day", "n/a"))
        sess_top = d.get("session", d.get("session_id", "n/a"))
        if days:
            day_range = f"{min(days)}-{max(days)}" if len(days) > 1 else str(next(iter(days)))
        else:
            day_range = str(day_top)
        sess_str = ",".join(sorted(sessions)[:6]) if sessions else str(sess_top)[:100]
        row = {
            "file": p.name,
            "traj": len(traj),
            "wait": int(acts.get("wait", 0)),
            "long": int(acts.get("long", 0)),
            "short": int(acts.get("short", 0)),
            "align_rate": align,
            "meta_train_steps": meta_steps,
            "day": day_range,
            "session": sess_str,
            "format": d.get("format"),
            "dim": d.get("meta_rl_dim"),
        }
        rows.append(row)
        print(p.name)
        print(
            f"  traj={row['traj']} wait={row['wait']} long={row['long']} "
            f"short={row['short']} align={row['align_rate']} meta_steps={row['meta_train_steps']}"
        )
        print(f"  day={row['day']} session={row['session']} format={row['format']} dim={row['dim']}")
    if files:
        d0 = load_pack(files[0])
        tr0 = (d0.get("trajectories") or [{}])[0]
        print("=" * 90)
        print("TOP KEYS:", sorted(d0.keys()))
        if isinstance(tr0, dict):
            print("TRAJ0 KEYS:", sorted(tr0.keys()))
            st = tr0.get("state")
            if st is not None:
                print(f"  state_len={len(st)}")
            for k in (
                "teacher_act",
                "reward",
                "teacher_size_frac",
                "target_percent",
                "day_index",
                "session",
            ):
                if k in tr0:
                    print(f"  {k}={tr0[k]!r}")
            if isinstance(d0.get("scoreboard"), dict):
                print("scoreboard:", json.dumps(d0["scoreboard"], default=str)[:500])
    return files, rows


def collect_all_traj(files):
    all_t = []
    for p in files:
        d = load_pack(p)
        for t in d.get("trajectories") or []:
            act = str(t.get("teacher_act") or "")
            if act not in ACT_I:
                continue
            all_t.append(
                {
                    "state": pad_state(t.get("state") or []),
                    "teacher_act": act,
                    "reward": float(t.get("reward", 1.0)),
                    "source": p.name,
                }
            )
    return all_t


def predict(pol: MetaPolicy, state: np.ndarray):
    """Use brain forward_raw (works for untrained seed prior)."""
    logits, _, _ = pol.brain.forward_raw(state)
    logits = np.asarray(logits, dtype=np.float64).reshape(-1)[:3]
    e = np.exp(logits - np.max(logits))
    probs = e / e.sum()
    idx = int(np.argmax(probs))
    return ACTS[idx], probs


def eval_policy(pol: MetaPolicy, trajs, label: str) -> dict:
    if not trajs:
        return {"label": label, "n": 0}
    correct = 0
    ces = []
    pred_counts = Counter()
    true_counts = Counter()
    fire_correct = 0
    fire_total = 0
    for t in trajs:
        y = t["teacher_act"]
        true_counts[y] += 1
        pred, probs = predict(pol, t["state"])
        pred_counts[pred] += 1
        if pred == y:
            correct += 1
        ces.append(float(-np.log(max(float(probs[ACT_I[y]]), 1e-12))))
        if y in ("long", "short"):
            fire_total += 1
            if pred == y:
                fire_correct += 1
    n = len(trajs)
    wait_frac = pred_counts.get("wait", 0) / max(n, 1)
    fire_labels = true_counts.get("long", 0) + true_counts.get("short", 0)
    return {
        "label": label,
        "n": n,
        "coach_agreement": correct / max(n, 1),
        "mean_ce": float(np.mean(ces)) if ces else None,
        "pred_dist": dict(pred_counts),
        "true_dist": dict(true_counts),
        "pred_wait_frac": wait_frac,
        "true_wait_frac": true_counts.get("wait", 0) / max(n, 1),
        "wait_bias_flag": wait_frac > 0.80,
        "fire_label_count": fire_labels,
        "fire_label_density": fire_labels / max(n, 1),
        "fire_side_accuracy": fire_correct / max(fire_total, 1) if fire_total else None,
        "meta_train_steps": int(pol.brain.meta_train_steps),
        "fingerprint": pol.weight_fingerprint(),
        "trained": bool(pol.brain.trained),
        "frozen": bool(pol.brain.frozen_for_inference),
    }


def main(mode: str = "inventory"):
    files, inv_rows = inventory()
    if mode == "inventory":
        # write partial summary for later merge
        partial = GT / "_inventory_only.json"
        partial.write_text(json.dumps({"inventory": inv_rows}, indent=2), encoding="utf-8")
        print(f"Wrote {partial}")
        return 0

    if not files:
        print("No packs")
        return 1

    all_traj = collect_all_traj(files)
    n = len(all_traj)
    split = int(n * 0.8) if n >= 5 else n
    holdout = all_traj[split:] if n >= 5 else all_traj
    train_like = all_traj[:split] if n >= 5 else all_traj
    label_mix = Counter(t["teacher_act"] for t in all_traj)
    print("\nAGGREGATE LABELS:", dict(label_mix), f"total={n}")
    print(f"holdout n={len(holdout)} train80 n={len(train_like)}")

    seed_pol = MetaPolicy.untrained_prior(seed=42)
    eval_a = eval_policy(seed_pol, holdout, "A_untrained_seed_holdout")
    print("EVAL A:", json.dumps(eval_a, indent=2))

    if not OUT_NPZ.exists():
        print(f"Missing {OUT_NPZ} — run ingest first")
        return 2

    forge = MetaPolicy.load(OUT_NPZ, freeze=True, require_serious=False)
    eval_b_hold = eval_policy(forge, holdout, "B_forge_v1_holdout")
    eval_b_all = eval_policy(forge, all_traj, "B_forge_v1_all")
    eval_b_train = eval_policy(forge, train_like, "B_forge_v1_train80")
    print("EVAL B holdout:", json.dumps(eval_b_hold, indent=2))
    print("EVAL B all:", json.dumps(eval_b_all, indent=2))
    print("EVAL B train80:", json.dumps(eval_b_train, indent=2))

    champ = ROOT / "evidence_court" / "artifacts" / "meta_policy_champion.npz"
    champ_info = {"exists": champ.exists(), "path": str(champ)}
    if champ.exists():
        import hashlib

        champ_info["sha256_16"] = hashlib.sha256(champ.read_bytes()).hexdigest()[:16]
        try:
            cp = MetaPolicy.load(champ, freeze=True, require_serious=False)
            champ_info["meta_train_steps"] = int(cp.brain.meta_train_steps)
            champ_info["fingerprint"] = cp.weight_fingerprint()
        except Exception as e:
            champ_info["load_err"] = str(e)

    fire = label_mix.get("long", 0) + label_mix.get("short", 0)
    wait_frac = label_mix.get("wait", 0) / max(n, 1)
    summary = {
        "track": "meta_policy_forge_v1",
        "law": "A34_offline_game_ingest",
        "n_packs": len(files),
        "n_traj_total": n,
        "label_mix": dict(label_mix),
        "fire_density": fire / max(n, 1),
        "inventory": inv_rows,
        "eval_A_seed_holdout": eval_a,
        "eval_B_forge_holdout": eval_b_hold,
        "eval_B_forge_all": eval_b_all,
        "eval_B_forge_train80": eval_b_train,
        "outputs": {"npz": str(OUT_NPZ), "json": str(OUT_JSON)},
        "champion_untouched_check": champ_info,
        "verdict_hints": {
            "wait_heavy_labels": wait_frac > 0.80,
            "fire_too_low": fire < max(10, n * 0.05),
            "improved_agreement": (eval_b_hold.get("coach_agreement") or 0)
            > (eval_a.get("coach_agreement") or 0),
            "improved_ce": (eval_b_hold.get("mean_ce") or 9)
            < (eval_a.get("mean_ce") or 9),
        },
    }
    # preserve policy sidecar meta from save; write full report next to it
    report_path = GT / "meta_policy_forge_v1_report.json"
    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    # also enrich OUT_JSON if present
    if OUT_JSON.exists():
        try:
            meta = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
        meta["forge_eval"] = {
            "eval_A": eval_a,
            "eval_B_holdout": eval_b_hold,
            "label_mix": dict(label_mix),
            "n_traj_total": n,
        }
        OUT_JSON.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {report_path}")
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "inventory"
    raise SystemExit(main(mode))
