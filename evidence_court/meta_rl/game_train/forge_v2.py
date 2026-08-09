"""forge_v2 — learn high-trend decisions (not wait-copy).

Diagnosis (forge_v1):
  Copied game coach on browser states, especially WAIT. Did not learn
  force → load → launch that transfers to the real day path.

Wrong fix:
  Force long/short at *inference* every bar → pad thrash, fake A13, cliff.

Right fix (this module) — train-time only:
  1) Rebalance: fire and load waits share the curriculum (not 90% wait CE)
  2) Prefer launch/release / london / ny rows from packs
  3) Inject synthetic London/NY force_opp states (path-like structure)
  4) Offline meta_update only; freeze for inference; champion untouched

Track:
  evidence_court/artifacts/game_train/meta_policy_forge_v2.npz
"""
from __future__ import annotations

import json
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from evidence_court.meta_rl.brain import sample_brain_state
from evidence_court.meta_rl.game_train.ingest import _pad_state, load_pack
from evidence_court.meta_rl.policy import MetaPolicy
from evidence_court.meta_rl.state import META_RL_DIM

_REPO = Path(__file__).resolve().parents[2]
GT = _REPO / "artifacts" / "game_train"
OUT_NPZ = GT / "meta_policy_forge_v2.npz"
OUT_JSON = GT / "meta_policy_forge_v2.json"
REPORT = GT / "meta_policy_forge_v2_train_report.json"

FIRE_TOPO = {"launch", "release", "pullback_resume", "continuation"}
LOAD_TOPO = {"slingshot_load", "load"}
WAIT_TOPO = {"chop", "collapse", "slingshot_load"}


@dataclass
class TrainExample:
    state: np.ndarray
    teacher_act: str
    reward: float
    size_frac: Optional[float]
    source: str
    tag: str


def _collect_pack_examples(gt: Path = GT) -> List[TrainExample]:
    """Dedupe by ts; keep teacher_act only."""
    packs = sorted(gt.glob("policy_forge_export_*.json"))
    seen: set[str] = set()
    out: List[TrainExample] = []
    for p in packs:
        data = load_pack(p)
        for row in data.get("trajectories") or []:
            act = str(row.get("teacher_act") or "")
            if act not in ("wait", "long", "short"):
                continue
            ts = str(row.get("ts") or "")
            key = f"{ts}|{act}|{row.get('sense_topology')}|{row.get('session')}"
            if ts and key in seen:
                continue
            if ts:
                seen.add(key)
            st = _pad_state(row.get("state") or [])
            if st.size != META_RL_DIM:
                continue
            topo = str(row.get("sense_topology") or "").lower()
            sess = str(row.get("session") or "").lower()
            # base reward from pack, boost good high-trend fires
            rew = float(row.get("reward", 1.0))
            if act in ("long", "short") and topo in FIRE_TOPO:
                rew = max(rew, 1.35)
            if act in ("long", "short") and sess in ("london", "ny"):
                rew = max(rew, 1.25)
            if act == "wait" and topo in LOAD_TOPO:
                rew = max(rew, 1.1)  # load-wait is the skill, not asia grind wait
            size = row.get("teacher_size_frac")
            out.append(
                TrainExample(
                    state=st,
                    teacher_act=act,
                    reward=rew,
                    size_frac=float(size) if size is not None else None,
                    source=p.name,
                    tag=f"pack:{topo or 'na'}:{sess or 'na'}",
                )
            )
    return out


def _bucket(examples: Sequence[TrainExample]) -> Dict[str, List[TrainExample]]:
    b: Dict[str, List[TrainExample]] = defaultdict(list)
    for ex in examples:
        if ex.teacher_act in ("long", "short"):
            b["fire"].append(ex)
            b[ex.teacher_act].append(ex)
            if "launch" in ex.tag or "release" in ex.tag:
                b["fire_launch"].append(ex)
            if ":london" in ex.tag or ":ny" in ex.tag:
                b["fire_lnny"].append(ex)
        else:
            b["wait"].append(ex)
            if "slingshot" in ex.tag or "load" in ex.tag:
                b["wait_load"].append(ex)
    return b


def _synth_batch(rng: np.random.Generator, n: int) -> List[TrainExample]:
    """Path-like high-trend / load / chop synthetic states."""
    out: List[TrainExample] = []
    for _ in range(n):
        target = float(rng.choice([5.0, 15.0, 30.0, 50.0, 70.0, 90.0]))
        risk = float(rng.choice([1.0, 2.0, 3.0]))
        mode = str(rng.choice(["fire", "fire", "fire", "load", "chop"], p=[0.25, 0.25, 0.2, 0.2, 0.1]))
        if mode == "fire":
            st, teacher, sf = sample_brain_state(
                rng, target=target, risk=risk, london_ny=True, force_opp=True
            )
            rew = 1.4
            tag = "synth:force_opp"
        elif mode == "load":
            # force structure but teacher wait (load not yet) — soft skill
            st, _t, _sf = sample_brain_state(
                rng, target=target, risk=risk, london_ny=True, force_opp=False
            )
            # damp set dirs slightly to look like load / incomplete
            st = st.copy()
            for i in (0, 3, 6, 9):
                st[i] *= 0.35
            teacher, sf, rew, tag = "wait", 0.0, 1.15, "synth:load_wait"
        else:
            st, teacher, sf = sample_brain_state(
                rng, target=target, risk=risk, london_ny=False, force_opp=False
            )
            if teacher != "wait" and rng.random() < 0.7:
                teacher, sf = "wait", 0.0
            rew, tag = 1.0, "synth:chopish"
        out.append(
            TrainExample(
                state=np.asarray(st, dtype=np.float64).reshape(-1)[:META_RL_DIM],
                teacher_act=teacher,
                reward=rew,
                size_frac=float(sf) if teacher != "wait" else 0.0,
                source="synthetic",
                tag=tag,
            )
        )
    return out


def sample_curriculum(
    rng: np.random.Generator,
    buckets: Dict[str, List[TrainExample]],
    *,
    n: int,
    fire_frac: float = 0.45,
    synth_frac: float = 0.30,
) -> List[TrainExample]:
    """Forced *decision mix* at train time: not all WAIT CE."""
    n_fire = int(n * fire_frac)
    n_synth = int(n * synth_frac)
    n_wait = max(0, n - n_fire - n_synth)
    batch: List[TrainExample] = []

    def take(pool: List[TrainExample], k: int) -> List[TrainExample]:
        if not pool or k <= 0:
            return []
        idx = rng.integers(0, len(pool), size=k)
        return [pool[int(i)] for i in idx]

    # fire: prefer launch/london-ny pools when available
    fire_pool = buckets.get("fire_launch") or buckets.get("fire_lnny") or buckets.get("fire") or []
    long_pool = buckets.get("long") or fire_pool
    short_pool = buckets.get("short") or fire_pool
    # balance long/short inside fire
    n_long = n_fire // 2
    n_short = n_fire - n_long
    batch.extend(take(long_pool, n_long))
    batch.extend(take(short_pool, n_short))
    # if fire pool empty, synth will carry

    wait_pool = buckets.get("wait_load") or buckets.get("wait") or []
    batch.extend(take(wait_pool, n_wait))
    batch.extend(_synth_batch(rng, n_synth + max(0, n_fire - len(fire_pool))))

    rng.shuffle(batch)
    return batch[:n] if len(batch) > n else batch


def train_forge_v2(
    *,
    steps: int = 4000,
    lr: float = 0.02,
    seed: int = 42,
    fire_frac: float = 0.45,
    synth_frac: float = 0.30,
    from_prior: bool = True,
    warmstart_forge_v1: bool = False,
) -> Dict[str, Any]:
    GT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    examples = _collect_pack_examples(GT)
    buckets = _bucket(examples)
    mix = Counter(ex.teacher_act for ex in examples)

    if warmstart_forge_v1 and (GT / "meta_policy_forge_v1.npz").exists():
        pol = MetaPolicy.load(GT / "meta_policy_forge_v1.npz", freeze=True, require_serious=False)
        pol.unlock_for_meta_train()
        start_src = "forge_v1"
    elif from_prior or not OUT_NPZ.exists():
        pol = MetaPolicy.untrained_prior(seed=seed)
        pol.unlock_for_meta_train()
        start_src = "prior"
    else:
        pol = MetaPolicy.load(OUT_NPZ, freeze=True, require_serious=False)
        pol.unlock_for_meta_train()
        start_src = "forge_v2_continue"

    steps_before = int(pol.meta_train_steps)
    fp_before = pol.weight_fingerprint()

    losses: List[float] = []
    applied_tags: Counter = Counter()
    applied_acts: Counter = Counter()

    # stream mini-batches of 32
    bs = 32
    n_batches = max(1, int(np.ceil(steps / bs)))
    applied = 0
    for bi in range(n_batches):
        if applied >= steps:
            break
        need = min(bs, steps - applied)
        batch = sample_curriculum(
            rng, buckets, n=need, fire_frac=fire_frac, synth_frac=synth_frac
        )
        for ex in batch:
            # pad state
            st = np.zeros(META_RL_DIM, dtype=np.float64)
            n = min(META_RL_DIM, int(ex.state.size))
            st[:n] = ex.state[:n]
            loss = pol.meta_update(
                st,
                teacher_act=ex.teacher_act,
                lr=lr * (0.97 ** (applied // 200)),
                reward=ex.reward,
                teacher_size_frac=ex.size_frac,
            )
            losses.append(float(loss))
            applied_tags[ex.tag.split(":")[0]] += 1
            applied_acts[ex.teacher_act] += 1
            applied += 1
            if applied >= steps:
                break

    if applied > 0:
        pol.brain.trained = True
    pol.freeze_for_inference()
    saved = str(pol.save(OUT_NPZ))

    report = {
        "track": "meta_policy_forge_v2",
        "law": "A34_learn_decision_not_wait_copy",
        "doctrine": "train_time_balanced_force_load_launch_not_inference_force_trade",
        "start_src": start_src,
        "n_unique_pack_examples": len(examples),
        "pack_label_mix": dict(mix),
        "bucket_sizes": {k: len(v) for k, v in buckets.items()},
        "steps_requested": steps,
        "steps_applied": applied,
        "steps_before": steps_before,
        "steps_after": int(pol.meta_train_steps),
        "fingerprint_before": fp_before,
        "fingerprint_after": pol.weight_fingerprint(),
        "mean_loss": float(np.mean(losses)) if losses else None,
        "applied_acts": dict(applied_acts),
        "applied_sources": dict(applied_tags),
        "fire_frac": fire_frac,
        "synth_frac": synth_frac,
        "lr": lr,
        "seed": seed,
        "saved": saved,
        "champion_untouched": True,
        "elapsed_note": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    # enrich sidecar json if present
    if OUT_JSON.exists():
        try:
            meta = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
        meta["forge_v2_train"] = {
            "steps": applied,
            "mean_loss": report["mean_loss"],
            "applied_acts": report["applied_acts"],
        }
        OUT_JSON.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Train forge_v2 decision curriculum")
    p.add_argument("--steps", type=int, default=4000)
    p.add_argument("--lr", type=float, default=0.02)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--fire-frac", type=float, default=0.45)
    p.add_argument("--synth-frac", type=float, default=0.30)
    p.add_argument("--warmstart-v1", action="store_true")
    p.add_argument("--continue", dest="cont", action="store_true", help="Continue existing v2")
    args = p.parse_args(list(argv) if argv is not None else None)
    rep = train_forge_v2(
        steps=int(args.steps),
        lr=float(args.lr),
        seed=int(args.seed),
        fire_frac=float(args.fire_frac),
        synth_frac=float(args.synth_frac),
        from_prior=not args.cont and not args.warmstart_v1,
        warmstart_forge_v1=bool(args.warmstart_v1),
    )
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
