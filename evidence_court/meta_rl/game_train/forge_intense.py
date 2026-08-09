"""forge_intense — unhinged *train-time* aggression (shadow track only).

Doctrine:
  The policy only learns what the gradient hits. Wait-skewed CE taught a waiter.
  This track **starves WAIT** and **floods fire** offline — London/NY, real-bar
  Watch misses, **packed path-state teachers (CASE-0037)**, launch packs, synth
  force_opp — so the map *must* learn to pull on states it actually sees.

Hard rails (not unhinged):
  - Offline meta_update only
  - Never force trades at inference / prove
  - Production champion UNTOUCHED
  - Load-wait kept as a small skill slice (not zero — still need slingshot skill)

Unhinged levers:
  - fire_frac default 0.75
  - path-state teachers (real 176-d) preferred over rebuilt label states
  - real_bar Watch fires multi-hit into the stream
  - synth almost pure London/NY force_opp
  - pack Asia-wait spam deprioritized
  - higher reward + LR on fire updates
  - periodic pure-fire blitz blocks
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
from evidence_court.meta_rl.game_train.forge_v2 import (
    FIRE_TOPO,
    LOAD_TOPO,
    TrainExample,
    _bucket,
    _collect_pack_examples,
)
from evidence_court.meta_rl.game_train.ingest import _pad_state
from evidence_court.meta_rl.policy import (
    MetaPolicy,
    opportunity_label_to_training_example,
)
from evidence_court.meta_rl.state import META_RL_DIM

_REPO = Path(__file__).resolve().parents[2]
GT = _REPO / "artifacts" / "game_train"
ART = _REPO / "artifacts"
OUT_NPZ = GT / "meta_policy_forge_intense.npz"
OUT_JSON = GT / "meta_policy_forge_intense.json"
REPORT = GT / "meta_policy_forge_intense_report.json"
DEFAULT_REAL_BAR = ART / "real_bar_opp_labels_case0036.json"
DEFAULT_PATH_STATE = ART / "path_state_teachers_case0037.json"

# Unhinged defaults — train budget composition (feral continue)
DEFAULT_STEPS = 20000
DEFAULT_FIRE_FRAC = 0.75
DEFAULT_PATH_FRAC = 0.40  # of total — real packed path states (best)
DEFAULT_REAL_BAR_FRAC = 0.15  # rebuilt label states (secondary)
DEFAULT_SYNTH_FRAC = 0.20  # of total; almost pure L/NY force_opp
DEFAULT_LR = 0.035
DEFAULT_FIRE_REWARD = 1.85
DEFAULT_MULTI_HIT = 16  # each path/real teacher cloned into pool


def _load_real_bar_examples(
    path: Path = DEFAULT_REAL_BAR,
    *,
    multi_hit: int = DEFAULT_MULTI_HIT,
    seed: int = 7,
) -> List[TrainExample]:
    """Real-bar PB/cont fires → training examples; multi-hit for intensity."""
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    labels = raw.get("labels") if isinstance(raw, dict) else raw
    if not isinstance(labels, list):
        return []
    rng = np.random.default_rng(seed)
    base: List[TrainExample] = []
    for lab in labels:
        if not isinstance(lab, dict):
            continue
        side = str(lab.get("teacher_act") or lab.get("side") or "")
        if side not in ("long", "short"):
            continue
        topo = str(lab.get("topology") or "")
        if topo and topo not in ("pullback_resume", "continuation", "launch", "release"):
            # allow empty topo; skip chop-like
            if topo in ("chop", "collapse"):
                continue
        band = str(lab.get("session_band") or "other")
        w = float(lab.get("weight") or (1.5 if band == "london_ny" else 1.0))
        target = float(lab.get("harvest_day_target") or rng.choice([5.0, 15.0, 30.0, 50.0]))
        risk = float(lab.get("harvest_day_risk") or rng.choice([1.0, 2.0, 3.0]))
        st, teacher, sf = opportunity_label_to_training_example(
            lab, target=target, risk=risk, rng=rng
        )
        if teacher not in ("long", "short"):
            teacher = side
        rew = max(DEFAULT_FIRE_REWARD, 1.2 + 0.35 * min(w, 2.0))
        if band == "london_ny":
            rew = max(rew, 1.9)
        base.append(
            TrainExample(
                state=np.asarray(st, dtype=np.float64).reshape(-1)[:META_RL_DIM],
                teacher_act=teacher,
                reward=rew,
                size_frac=float(sf) if teacher != "wait" else 0.55,
                source=str(path.name),
                tag=f"realbar:{topo or 'pb'}:{band}",
            )
        )
    if not base:
        return []
    # Multi-hit: unhinged volume on rare good teachers
    out: List[TrainExample] = []
    hits = max(1, int(multi_hit))
    for ex in base:
        for _ in range(hits):
            out.append(ex)
    return out


def _load_path_state_examples(
    path: Path = DEFAULT_PATH_STATE,
    *,
    multi_hit: int = DEFAULT_MULTI_HIT,
) -> List[TrainExample]:
    """CASE-0037: exact 176-d path states the brain waited on (anti F-025 rebuild)."""
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    examples = raw.get("examples") if isinstance(raw, dict) else raw
    if not isinstance(examples, list):
        return []
    base: List[TrainExample] = []
    for ex in examples:
        if not isinstance(ex, dict):
            continue
        st = ex.get("state")
        if st is None:
            continue
        arr = np.asarray(st, dtype=np.float64).ravel()
        if arr.size != META_RL_DIM or not np.all(np.isfinite(arr)):
            continue
        act = str(ex.get("teacher_act") or "")
        if act not in ("long", "short"):
            continue
        topo = str(ex.get("topology") or "")
        if topo and topo not in ("pullback_resume", "continuation", "launch", "release"):
            if topo in ("chop", "collapse"):
                continue
        band = str(ex.get("session_band") or "other")
        w = float(ex.get("weight") or (1.5 if band == "london_ny" else 1.0))
        sf = float(ex.get("teacher_size_frac") or 0.65)
        rew = max(DEFAULT_FIRE_REWARD + 0.2, 1.5 + 0.4 * min(w, 2.0))
        if band == "london_ny":
            rew = max(rew, 2.1)
        base.append(
            TrainExample(
                state=arr[:META_RL_DIM].copy(),
                teacher_act=act,
                reward=rew,
                size_frac=sf,
                source=str(path.name),
                tag=f"path:{topo or 'pb'}:{band}",
            )
        )
    if not base:
        return []
    hits = max(1, int(multi_hit))
    out: List[TrainExample] = []
    for ex in base:
        for _ in range(hits):
            out.append(ex)
    return out


def _synth_fire(rng: np.random.Generator) -> TrainExample:
    """Guaranteed fire teacher under London/NY force_opp (override soft wait)."""
    target = float(rng.choice([5.0, 15.0, 30.0, 50.0, 70.0, 90.0]))
    risk = float(rng.choice([1.0, 2.0, 3.0]))
    st, teacher, sf = sample_brain_state(
        rng, target=target, risk=risk, london_ny=True, force_opp=True
    )
    st = np.asarray(st, dtype=np.float64).reshape(-1).copy()
    # Unhinged: if soft sampler still waits, force side from set dirs
    if teacher not in ("long", "short"):
        dirs = [float(st[i * 3]) for i in range(4) if i * 3 < st.size]
        mean_d = float(np.mean(dirs)) if dirs else float(rng.choice([-0.6, 0.6]))
        if abs(mean_d) < 0.15:
            mean_d = float(rng.choice([-0.7, 0.7]))
            for i in range(4):
                if i * 3 < st.size:
                    st[i * 3] = mean_d
        teacher = "long" if mean_d > 0 else "short"
        t_norm = (target - 5.0) / 85.0
        sf = float(np.clip(0.55 + 0.35 * t_norm, 0.4, 0.95))
    return TrainExample(
        state=st[:META_RL_DIM],
        teacher_act=teacher,
        reward=DEFAULT_FIRE_REWARD + 0.15,
        size_frac=float(sf) if sf else 0.6,
        source="synthetic",
        tag="synth:force_opp_guaranteed",
    )


def _synth_load_wait(rng: np.random.Generator) -> TrainExample:
    target = float(rng.choice([15.0, 30.0, 50.0]))
    risk = float(rng.choice([1.0, 2.0, 3.0]))
    st, _t, _sf = sample_brain_state(
        rng, target=target, risk=risk, london_ny=True, force_opp=False
    )
    st = np.asarray(st, dtype=np.float64).reshape(-1).copy()
    for i in (0, 3, 6, 9):
        if i < st.size:
            st[i] *= 0.3
    return TrainExample(
        state=st[:META_RL_DIM],
        teacher_act="wait",
        reward=1.2,
        size_frac=0.0,
        source="synthetic",
        tag="synth:load_wait",
    )


def sample_unhinged_curriculum(
    rng: np.random.Generator,
    *,
    n: int,
    pack_buckets: Dict[str, List[TrainExample]],
    path_pool: List[TrainExample],
    real_pool: List[TrainExample],
    fire_frac: float = DEFAULT_FIRE_FRAC,
    path_frac: float = DEFAULT_PATH_FRAC,
    real_bar_frac: float = DEFAULT_REAL_BAR_FRAC,
    synth_frac: float = DEFAULT_SYNTH_FRAC,
) -> List[TrainExample]:
    """Aggressive mix: path-state (best) + real-bar + pack launch + synth; tiny wait."""
    n = max(1, int(n))
    n_path = int(n * path_frac) if path_pool else 0
    n_real = int(n * real_bar_frac) if real_pool else 0
    # if path missing, give real-bar the path budget
    if not path_pool and real_pool:
        n_real = int(n * (path_frac + real_bar_frac))
    n_fire = int(n * fire_frac)
    n_synth = int(n * synth_frac)
    n_premium = n_path + n_real
    n_wait = max(0, n - max(n_fire, n_premium) - n_synth)
    n_pack_fire = max(0, n_fire - n_premium)

    batch: List[TrainExample] = []

    def take(pool: List[TrainExample], k: int) -> List[TrainExample]:
        if not pool or k <= 0:
            return []
        idx = rng.integers(0, len(pool), size=k)
        return [pool[int(i)] for i in idx]

    # 1) Packed path-state fires (highest priority — real 176-d)
    if path_pool and n_path > 0:
        batch.extend(take(path_pool, n_path))

    # 2) Real-bar rebuilt fires (secondary)
    if real_pool and n_real > 0:
        batch.extend(take(real_pool, n_real))

    # 3) Pack launch / LN-NY fires
    fire_pool = (
        pack_buckets.get("fire_launch")
        or pack_buckets.get("fire_lnny")
        or pack_buckets.get("fire")
        or []
    )
    long_p = pack_buckets.get("long") or fire_pool
    short_p = pack_buckets.get("short") or fire_pool
    n_long = n_pack_fire // 2
    n_short = n_pack_fire - n_long
    got_pack = take(long_p, n_long) + take(short_p, n_short)
    batch.extend(got_pack)
    shortfall = n_pack_fire - len(got_pack)
    for _ in range(max(0, shortfall)):
        batch.append(_synth_fire(rng))

    # 4) Synth London/NY force_opp (guaranteed fire)
    for _ in range(n_synth):
        batch.append(_synth_fire(rng))

    # 5) Small load-wait skill slice
    wait_pool = pack_buckets.get("wait_load") or pack_buckets.get("wait") or []
    if n_wait > 0:
        if wait_pool:
            batch.extend(take(wait_pool, n_wait))
        else:
            for _ in range(n_wait):
                batch.append(_synth_load_wait(rng))

    rng.shuffle(batch)
    while len(batch) < n:
        # prefer path when padding
        if path_pool and rng.random() < 0.6:
            batch.append(path_pool[int(rng.integers(0, len(path_pool)))])
        else:
            batch.append(_synth_fire(rng))
    return batch[:n]


def train_forge_intense(
    *,
    steps: int = DEFAULT_STEPS,
    lr: float = DEFAULT_LR,
    seed: int = 42,
    fire_frac: float = DEFAULT_FIRE_FRAC,
    path_frac: float = DEFAULT_PATH_FRAC,
    real_bar_frac: float = DEFAULT_REAL_BAR_FRAC,
    synth_frac: float = DEFAULT_SYNTH_FRAC,
    multi_hit: int = DEFAULT_MULTI_HIT,
    real_bar_path: Optional[Path] = None,
    path_state_path: Optional[Path] = None,
    from_prior: bool = True,
    warmstart_forge_v2: bool = False,
    warmstart_intense: bool = False,
    blitz_every: int = 48,
    blitz_size: int = 24,
) -> Dict[str, Any]:
    """Unhinged offline train → meta_policy_forge_intense.npz (champion safe)."""
    GT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rb_path = Path(real_bar_path) if real_bar_path else DEFAULT_REAL_BAR
    ps_path = Path(path_state_path) if path_state_path else DEFAULT_PATH_STATE

    pack_ex = _collect_pack_examples(GT)
    pack_buckets = _bucket(pack_ex)
    path_pool = _load_path_state_examples(ps_path, multi_hit=multi_hit)
    real_pool = _load_real_bar_examples(rb_path, multi_hit=max(4, multi_hit // 2), seed=seed + 99)

    if warmstart_intense and OUT_NPZ.exists():
        pol = MetaPolicy.load(OUT_NPZ, freeze=True, require_serious=False)
        pol.unlock_for_meta_train()
        start_src = "intense_continue"
    elif warmstart_forge_v2 and (GT / "meta_policy_forge_v2.npz").exists():
        pol = MetaPolicy.load(GT / "meta_policy_forge_v2.npz", freeze=True, require_serious=False)
        pol.unlock_for_meta_train()
        start_src = "forge_v2"
    elif from_prior or not OUT_NPZ.exists():
        pol = MetaPolicy.untrained_prior(seed=seed)
        pol.unlock_for_meta_train()
        start_src = "prior"
    else:
        pol = MetaPolicy.load(OUT_NPZ, freeze=True, require_serious=False)
        pol.unlock_for_meta_train()
        start_src = "intense_continue"

    steps_before = int(pol.meta_train_steps)
    fp_before = pol.weight_fingerprint()

    losses: List[float] = []
    applied_tags: Counter = Counter()
    applied_acts: Counter = Counter()
    applied_sources: Counter = Counter()

    bs = 32
    n_batches = max(1, int(np.ceil(steps / bs)))
    applied = 0
    fire_lr_boost = 1.45

    for bi in range(n_batches):
        if applied >= steps:
            break
        need = min(bs, steps - applied)
        batch = sample_unhinged_curriculum(
            rng,
            n=need,
            pack_buckets=pack_buckets,
            path_pool=path_pool,
            real_pool=real_pool,
            fire_frac=fire_frac,
            path_frac=path_frac,
            real_bar_frac=real_bar_frac,
            synth_frac=synth_frac,
        )
        for ex in batch:
            st = np.zeros(META_RL_DIM, dtype=np.float64)
            n = min(META_RL_DIM, int(ex.state.size))
            st[:n] = ex.state[:n]
            is_fire = ex.teacher_act in ("long", "short")
            step_lr = lr * (0.98 ** (applied // 400))
            if is_fire:
                step_lr *= fire_lr_boost
            # path states get extra LR — they match prove distribution
            if ex.tag.startswith("path:"):
                step_lr *= 1.15
            loss = pol.meta_update(
                st,
                teacher_act=ex.teacher_act,
                lr=step_lr,
                reward=ex.reward,
                teacher_size_frac=ex.size_frac,
            )
            losses.append(float(loss))
            applied_acts[ex.teacher_act] += 1
            src = ex.tag.split(":")[0] if ex.tag else ex.source
            applied_tags[src] += 1
            applied_sources[ex.source[:40]] += 1
            applied += 1
            if applied >= steps:
                break

        # Periodic pure-fire blitz — prefer path states
        if applied < steps and blitz_every > 0 and (bi + 1) % max(1, blitz_every // bs) == 0:
            for _ in range(min(blitz_size, steps - applied)):
                u = rng.random()
                if path_pool and u < 0.65:
                    ex = path_pool[int(rng.integers(0, len(path_pool)))]
                elif real_pool and u < 0.85:
                    ex = real_pool[int(rng.integers(0, len(real_pool)))]
                else:
                    ex = _synth_fire(rng)
                st = np.zeros(META_RL_DIM, dtype=np.float64)
                n = min(META_RL_DIM, int(ex.state.size))
                st[:n] = ex.state[:n]
                loss = pol.meta_update(
                    st,
                    teacher_act=ex.teacher_act,
                    lr=lr * fire_lr_boost * 1.15,
                    reward=max(ex.reward, DEFAULT_FIRE_REWARD),
                    teacher_size_frac=ex.size_frac or 0.6,
                )
                losses.append(float(loss))
                applied_acts[ex.teacher_act] += 1
                applied_tags["blitz"] += 1
                applied += 1
                if applied >= steps:
                    break

    if applied > 0:
        pol.brain.trained = True
    pol.freeze_for_inference()
    saved = str(pol.save(OUT_NPZ))

    n_fire = applied_acts.get("long", 0) + applied_acts.get("short", 0)
    fire_share = float(n_fire / applied) if applied else 0.0

    report = {
        "track": "meta_policy_forge_intense",
        "law": "A34_unhinged_train_time_aggression",
        "doctrine": "starve_wait_flood_fire_path_state_first_offline_only",
        "unhinged": True,
        "start_src": start_src,
        "n_unique_pack_examples": len(pack_ex),
        "n_path_state_base": len(path_pool) // max(1, multi_hit) if path_pool else 0,
        "n_path_state_pool": len(path_pool),
        "n_real_bar_base": len(real_pool) // max(1, multi_hit // 2 or 1) if real_pool else 0,
        "n_real_bar_pool": len(real_pool),
        "multi_hit": multi_hit,
        "path_state_path": str(ps_path),
        "real_bar_path": str(rb_path),
        "pack_bucket_sizes": {k: len(v) for k, v in pack_buckets.items()},
        "steps_requested": steps,
        "steps_applied": applied,
        "steps_before": steps_before,
        "steps_after": int(pol.meta_train_steps),
        "fingerprint_before": fp_before,
        "fingerprint_after": pol.weight_fingerprint(),
        "mean_loss": float(np.mean(losses)) if losses else None,
        "applied_acts": dict(applied_acts),
        "fire_share_applied": fire_share,
        "applied_tags": dict(applied_tags),
        "fire_frac": fire_frac,
        "path_frac": path_frac,
        "real_bar_frac": real_bar_frac,
        "synth_frac": synth_frac,
        "lr": lr,
        "fire_reward": DEFAULT_FIRE_REWARD,
        "seed": seed,
        "saved": saved,
        "champion_untouched": True,
        "inference_force_pad": False,
        "elapsed_note": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "measure_not_coach_ce": "use_forward_mean_trades_n_zero_a13_frac",
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "track": "forge_intense",
                "meta_train_steps": int(pol.meta_train_steps),
                "fingerprint": pol.weight_fingerprint(),
                "fire_share_applied": fire_share,
                "unhinged": True,
                "champion_untouched": True,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Unhinged train-time fire curriculum (shadow)")
    p.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    p.add_argument("--lr", type=float, default=DEFAULT_LR)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--fire-frac", type=float, default=DEFAULT_FIRE_FRAC)
    p.add_argument("--path-frac", type=float, default=DEFAULT_PATH_FRAC)
    p.add_argument("--real-bar-frac", type=float, default=DEFAULT_REAL_BAR_FRAC)
    p.add_argument("--synth-frac", type=float, default=DEFAULT_SYNTH_FRAC)
    p.add_argument("--multi-hit", type=int, default=DEFAULT_MULTI_HIT)
    p.add_argument("--real-bar", type=str, default=str(DEFAULT_REAL_BAR))
    p.add_argument("--path-state", type=str, default=str(DEFAULT_PATH_STATE))
    p.add_argument("--warmstart-v2", action="store_true")
    p.add_argument("--continue", dest="cont", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)
    rep = train_forge_intense(
        steps=int(args.steps),
        lr=float(args.lr),
        seed=int(args.seed),
        fire_frac=float(args.fire_frac),
        path_frac=float(args.path_frac),
        real_bar_frac=float(args.real_bar_frac),
        synth_frac=float(args.synth_frac),
        multi_hit=int(args.multi_hit),
        real_bar_path=Path(args.real_bar),
        path_state_path=Path(args.path_state),
        from_prior=not args.cont and not args.warmstart_v2,
        warmstart_forge_v2=bool(args.warmstart_v2),
        warmstart_intense=bool(args.cont),
    )
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
