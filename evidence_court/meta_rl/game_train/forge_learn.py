"""forge_learn — train *harder* for generalization, not answer-memorization.

Problem (intense track):
  Multi-hit ×16 on ~400 fixed path vectors + high LR + fire blitz
  → policy memorizes those states, not force→load→launch principles.

This track (learn):
  1) Unique teachers only (no multi-hit clones)
  2) Held-out dates never seen in CE (measure real agreement)
  3) On-the-fly augmentation that keeps teacher side:
       - re-encode goal×risk context (A31 no-retrain band)
       - L2L set-slot permutation (roles, not name slots)
       - light mark noise (not structure destroy)
  4) Class-balance long/short sampling
  5) Contrast mix: fire vs load-wait (skill boundary)
  6) Principle synth (force_opp + L2L) as volume, not oracle copies
  7) Lower LR, more steps, no exact-vector blitz

Champion untouched. Offline only. Never pad at inference.
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
    TrainExample,
    _bucket,
    _collect_pack_examples,
)
from evidence_court.meta_rl.goal_risk import encode_goal_risk_context
from evidence_court.meta_rl.policy import MetaPolicy
from evidence_court.meta_rl.state import GOAL_RISK_SLICE, MARK_SLICE, META_RL_DIM

_REPO = Path(__file__).resolve().parents[2]
GT = _REPO / "artifacts" / "game_train"
ART = _REPO / "artifacts"
OUT_NPZ = GT / "meta_policy_forge_learn.npz"
OUT_JSON = GT / "meta_policy_forge_learn.json"
REPORT = GT / "meta_policy_forge_learn_report.json"
DEFAULT_PATH_STATE = ART / "path_state_teachers_case0037.json"

DEFAULT_STEPS = 24000
DEFAULT_LR = 0.018
DEFAULT_FIRE_FRAC = 0.55
DEFAULT_PATH_FRAC = 0.35
DEFAULT_SYNTH_FRAC = 0.30
DEFAULT_WAIT_FRAC = 0.15
DEFAULT_NOISE = 0.04
TARGETS = (5.0, 10.0, 15.0, 30.0, 50.0, 70.0, 90.0)
RISKS = (1.0, 2.0, 3.0)


@dataclass
class UniqueTeacher:
    state: np.ndarray
    teacher_act: str
    size_frac: float
    topology: str
    session_band: str
    asof_date: str
    symbol: str
    weight: float
    source: str


def _load_unique_path_teachers(path: Path) -> List[UniqueTeacher]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    examples = raw.get("examples") if isinstance(raw, dict) else raw
    if not isinstance(examples, list):
        return []
    out: List[UniqueTeacher] = []
    seen: set[str] = set()
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
        if topo in ("chop", "collapse"):
            continue
        date = str(ex.get("asof_date") or "")
        sym = str(ex.get("symbol") or "")
        tslot = str(ex.get("asof_time") or "")
        key = f"{date}|{tslot}|{sym}|{act}|{topo}"
        if key in seen:
            continue
        seen.add(key)
        out.append(
            UniqueTeacher(
                state=arr.copy(),
                teacher_act=act,
                size_frac=float(ex.get("teacher_size_frac") or 0.65),
                topology=topo or "pullback_resume",
                session_band=str(ex.get("session_band") or "other"),
                asof_date=date,
                symbol=sym,
                weight=float(ex.get("weight") or 1.0),
                source="path_unique",
            )
        )
    return out


def _split_by_date(
    teachers: Sequence[UniqueTeacher],
    *,
    holdout_frac: float = 0.25,
) -> Tuple[List[UniqueTeacher], List[UniqueTeacher], List[str], List[str]]:
    """Hold out last dates by calendar order — never train on them."""
    dates = sorted({t.asof_date for t in teachers if t.asof_date})
    if not dates:
        return list(teachers), [], [], []
    n_hold = max(1, int(round(len(dates) * holdout_frac)))
    hold_dates = set(dates[-n_hold:])
    train_dates = [d for d in dates if d not in hold_dates]
    train = [t for t in teachers if t.asof_date not in hold_dates]
    hold = [t for t in teachers if t.asof_date in hold_dates]
    # if train empty (tiny set), keep all train
    if not train:
        return list(teachers), [], dates, []
    return train, hold, train_dates, sorted(hold_dates)


def _augment_teacher(
    rng: np.random.Generator,
    t: UniqueTeacher,
    *,
    noise: float = DEFAULT_NOISE,
    do_l2l: bool = True,
    reencode_goal: bool = True,
) -> TrainExample:
    """New view of same decision — teacher side preserved."""
    st = t.state.copy()

    if reencode_goal:
        target = float(rng.choice(TARGETS))
        risk = float(rng.choice(RISKS))
        progress = float(rng.uniform(0.0, 0.55))
        realized = float(rng.uniform(0.0, risk * 0.45))
        ctx = encode_goal_risk_context(
            target,
            risk,
            progress_to_target=progress,
            realized_risk_percent=realized,
            validate=True,
        )
        st[GOAL_RISK_SLICE] = np.asarray(ctx, dtype=np.float64).ravel()[:8]
        t_norm = (target - 5.0) / 85.0
        london = t.session_band == "london_ny"
        size = float(np.clip(0.45 + 0.4 * t_norm + (0.1 if london else 0.0), 0.25, 0.95))
    else:
        size = t.size_frac
        target = 15.0

    if do_l2l and rng.random() < 0.55:
        # Set slots: each set is 3 channels starting at 0,3,6,9 in channel1 head
        order = rng.permutation(4)
        mark = st[MARK_SLICE].copy()
        # only permute first 12 dims (4 sets × dir/vel-ish) — conservative L2L
        block = mark[:12].copy().reshape(4, 3)
        mark[:12] = block[order].reshape(-1)
        st[MARK_SLICE] = mark

    if noise > 0:
        # noise on mark body only — keep goal context clean
        m = st[MARK_SLICE]
        st[MARK_SLICE] = m + rng.normal(0.0, noise, size=m.shape)
        # mild clip so features stay in sane band
        st[MARK_SLICE] = np.clip(st[MARK_SLICE], -3.0, 3.0)

    rew = 1.35 + 0.2 * min(t.weight, 2.0)
    if t.session_band == "london_ny":
        rew += 0.15
    return TrainExample(
        state=st,
        teacher_act=t.teacher_act,
        reward=rew,
        size_frac=size,
        source=t.source,
        tag=f"aug:{t.topology}:{t.session_band}",
    )


def _synth_principle(rng: np.random.Generator, mode: str) -> TrainExample:
    target = float(rng.choice(TARGETS))
    risk = float(rng.choice(RISKS))
    if mode == "fire":
        st, teacher, sf = sample_brain_state(
            rng,
            target=target,
            risk=risk,
            london_ny=True,
            force_opp=True,
            l2l_permute=bool(rng.random() < 0.4),
        )
        # if soft wait, keep as weak wait (do NOT force side — anti-memorize oracle)
        if teacher not in ("long", "short"):
            return TrainExample(
                state=np.asarray(st, dtype=np.float64).ravel()[:META_RL_DIM],
                teacher_act="wait",
                reward=1.0,
                size_frac=0.0,
                source="synth_principle",
                tag="synth:soft_wait",
            )
        return TrainExample(
            state=np.asarray(st, dtype=np.float64).ravel()[:META_RL_DIM],
            teacher_act=teacher,
            reward=1.45,
            size_frac=float(sf),
            source="synth_principle",
            tag="synth:force_opp",
        )
    if mode == "load":
        st, _t, _sf = sample_brain_state(
            rng, target=target, risk=risk, london_ny=True, force_opp=False, l2l_permute=False
        )
        st = np.asarray(st, dtype=np.float64).ravel().copy()
        for i in (0, 3, 6, 9):
            if i < st.size:
                st[i] *= 0.28
        return TrainExample(
            state=st[:META_RL_DIM],
            teacher_act="wait",
            reward=1.25,
            size_frac=0.0,
            source="synth_principle",
            tag="synth:load_wait",
        )
    # chop / general
    st, teacher, sf = sample_brain_state(
        rng, target=target, risk=risk, london_ny=False, force_opp=False, l2l_permute=True
    )
    if teacher != "wait" and rng.random() < 0.55:
        teacher, sf = "wait", 0.0
    return TrainExample(
        state=np.asarray(st, dtype=np.float64).ravel()[:META_RL_DIM],
        teacher_act=teacher,
        reward=1.0,
        size_frac=float(sf) if teacher != "wait" else 0.0,
        source="synth_principle",
        tag="synth:general",
    )


def _balanced_pick(
    rng: np.random.Generator,
    by_side: Dict[str, List[UniqueTeacher]],
    k: int,
) -> List[UniqueTeacher]:
    if k <= 0:
        return []
    longs = by_side.get("long") or []
    shorts = by_side.get("short") or []
    out: List[UniqueTeacher] = []
    for i in range(k):
        prefer = "long" if i % 2 == 0 else "short"
        pool = by_side.get(prefer) or longs or shorts
        if not pool:
            break
        out.append(pool[int(rng.integers(0, len(pool)))])
    return out


def sample_learn_batch(
    rng: np.random.Generator,
    *,
    n: int,
    train_teachers: Sequence[UniqueTeacher],
    pack_buckets: Dict[str, List[TrainExample]],
    fire_frac: float,
    path_frac: float,
    synth_frac: float,
    wait_frac: float,
    noise: float,
) -> List[TrainExample]:
    n = max(1, int(n))
    by_side: Dict[str, List[UniqueTeacher]] = defaultdict(list)
    for t in train_teachers:
        by_side[t.teacher_act].append(t)

    n_path = int(n * path_frac) if train_teachers else 0
    n_synth = int(n * synth_frac)
    n_wait = int(n * wait_frac)
    n_pack = max(0, n - n_path - n_synth - n_wait)
    # rebalance: ensure fire-ish budget via path+synth fire
    _ = fire_frac  # used for reporting; path/synth already fire-heavy

    batch: List[TrainExample] = []

    # Augmented unique path (generalization views)
    for t in _balanced_pick(rng, by_side, n_path):
        batch.append(
            _augment_teacher(
                rng,
                t,
                noise=noise,
                do_l2l=True,
                reencode_goal=True,
            )
        )

    # Principle synth
    for _ in range(n_synth):
        mode = str(rng.choice(["fire", "fire", "fire", "load", "general"], p=[0.28, 0.28, 0.2, 0.14, 0.1]))
        batch.append(_synth_principle(rng, mode))

    # Pack launch fires (diverse browser states) — no multi-hit
    fire_pool = (
        pack_buckets.get("fire_launch")
        or pack_buckets.get("fire_lnny")
        or pack_buckets.get("fire")
        or []
    )
    if fire_pool and n_pack > 0:
        idx = rng.integers(0, len(fire_pool), size=n_pack)
        for i in idx:
            ex = fire_pool[int(i)]
            # light noise so pack rows also don't memorize
            st = ex.state.copy()
            st = st + rng.normal(0.0, noise * 0.5, size=st.shape)
            batch.append(
                TrainExample(
                    state=st,
                    teacher_act=ex.teacher_act,
                    reward=ex.reward,
                    size_frac=ex.size_frac,
                    source=ex.source,
                    tag="pack_aug:" + ex.tag,
                )
            )
    else:
        for _ in range(n_pack):
            batch.append(_synth_principle(rng, "fire"))

    # Load-wait contrast
    wait_pool = pack_buckets.get("wait_load") or []
    for _ in range(n_wait):
        if wait_pool and rng.random() < 0.45:
            ex = wait_pool[int(rng.integers(0, len(wait_pool)))]
            st = ex.state.copy() + rng.normal(0.0, noise * 0.4, size=ex.state.shape)
            batch.append(
                TrainExample(
                    state=st,
                    teacher_act="wait",
                    reward=1.2,
                    size_frac=0.0,
                    source=ex.source,
                    tag="wait_aug:load",
                )
            )
        else:
            batch.append(_synth_principle(rng, "load"))

    rng.shuffle(batch)
    while len(batch) < n:
        batch.append(_synth_principle(rng, "fire"))
    return batch[:n]


def _teacher_agreement(
    pol: MetaPolicy,
    teachers: Sequence[UniqueTeacher],
    *,
    max_n: int = 200,
    seed: int = 0,
    augment: bool = False,
) -> Dict[str, float]:
    if not teachers:
        return {"n": 0, "agree": 0.0, "fire_agree": 0.0}
    rng = np.random.default_rng(seed)
    idxs = rng.choice(len(teachers), size=min(max_n, len(teachers)), replace=False)
    ok = 0
    fire_ok = 0
    fire_n = 0
    for i in idxs:
        t = teachers[int(i)]
        if augment:
            ex = _augment_teacher(rng, t, noise=DEFAULT_NOISE, do_l2l=True, reencode_goal=True)
            st, teacher = ex.state, ex.teacher_act
        else:
            st, teacher = t.state, t.teacher_act
        act_name = "wait"
        try:
            from evidence_court.meta_rl.brain import ACT_NAMES

            logits, _sz, _h = pol.brain.forward_raw(st)
            act_name = ACT_NAMES[int(np.argmax(logits))]
        except Exception:
            act_name = "wait"
        if act_name == teacher:
            ok += 1
        if teacher in ("long", "short"):
            fire_n += 1
            if act_name == teacher:
                fire_ok += 1
    n = len(idxs)
    return {
        "n": float(n),
        "agree": float(ok / max(n, 1)),
        "fire_agree": float(fire_ok / max(fire_n, 1)),
        "fire_n": float(fire_n),
    }


def train_forge_learn(
    *,
    steps: int = DEFAULT_STEPS,
    lr: float = DEFAULT_LR,
    seed: int = 42,
    fire_frac: float = DEFAULT_FIRE_FRAC,
    path_frac: float = DEFAULT_PATH_FRAC,
    synth_frac: float = DEFAULT_SYNTH_FRAC,
    wait_frac: float = DEFAULT_WAIT_FRAC,
    noise: float = DEFAULT_NOISE,
    holdout_frac: float = 0.25,
    path_state_path: Optional[Path] = None,
    from_prior: bool = True,
    warmstart_intense: bool = False,
    warmstart_learn: bool = False,
) -> Dict[str, Any]:
    GT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    ps_path = Path(path_state_path) if path_state_path else DEFAULT_PATH_STATE

    unique = _load_unique_path_teachers(ps_path)
    train_t, hold_t, train_dates, hold_dates = _split_by_date(unique, holdout_frac=holdout_frac)
    pack_ex = _collect_pack_examples(GT)
    pack_buckets = _bucket(pack_ex)

    if warmstart_learn and OUT_NPZ.exists():
        pol = MetaPolicy.load(OUT_NPZ, freeze=True, require_serious=False)
        pol.unlock_for_meta_train()
        start_src = "learn_continue"
    elif warmstart_intense and (GT / "meta_policy_forge_intense.npz").exists():
        # fine-tune intense weights with generalize regime (optional)
        pol = MetaPolicy.load(GT / "meta_policy_forge_intense.npz", freeze=True, require_serious=False)
        pol.unlock_for_meta_train()
        start_src = "intense_warmstart"
    elif from_prior or not OUT_NPZ.exists():
        pol = MetaPolicy.untrained_prior(seed=seed)
        pol.unlock_for_meta_train()
        start_src = "prior"
    else:
        pol = MetaPolicy.load(OUT_NPZ, freeze=True, require_serious=False)
        pol.unlock_for_meta_train()
        start_src = "learn_continue"

    steps_before = int(pol.meta_train_steps)
    fp_before = pol.weight_fingerprint()

    # pre-train holdout baseline
    hold_before = _teacher_agreement(pol, hold_t, seed=seed + 1, augment=False)
    train_before = _teacher_agreement(pol, train_t, seed=seed + 2, augment=False)

    losses: List[float] = []
    applied_acts: Counter = Counter()
    applied_tags: Counter = Counter()
    bs = 32
    n_batches = max(1, int(np.ceil(steps / bs)))
    applied = 0

    for bi in range(n_batches):
        if applied >= steps:
            break
        need = min(bs, steps - applied)
        batch = sample_learn_batch(
            rng,
            n=need,
            train_teachers=train_t,
            pack_buckets=pack_buckets,
            fire_frac=fire_frac,
            path_frac=path_frac,
            synth_frac=synth_frac,
            wait_frac=wait_frac,
            noise=noise,
        )
        # mild LR decay
        step_lr = lr * (0.985 ** (applied // 500))
        for ex in batch:
            st = np.zeros(META_RL_DIM, dtype=np.float64)
            n = min(META_RL_DIM, int(ex.state.size))
            st[:n] = ex.state[:n]
            loss = pol.meta_update(
                st,
                teacher_act=ex.teacher_act,
                lr=step_lr,
                reward=ex.reward,
                teacher_size_frac=ex.size_frac,
            )
            losses.append(float(loss))
            applied_acts[ex.teacher_act] += 1
            applied_tags[ex.tag.split(":")[0]] += 1
            applied += 1
            if applied >= steps:
                break

    if applied > 0:
        pol.brain.trained = True
    pol.freeze_for_inference()
    saved = str(pol.save(OUT_NPZ))

    hold_after = _teacher_agreement(pol, hold_t, seed=seed + 3, augment=False)
    hold_aug = _teacher_agreement(pol, hold_t, seed=seed + 4, augment=True)
    train_after = _teacher_agreement(pol, train_t, seed=seed + 5, augment=False)
    train_aug = _teacher_agreement(pol, train_t, seed=seed + 6, augment=True)

    n_fire = applied_acts.get("long", 0) + applied_acts.get("short", 0)
    fire_share = float(n_fire / applied) if applied else 0.0

    # Memorization smell: train exact >> hold exact, and train exact >> train aug
    mem_gap = float(train_after.get("agree", 0) - hold_after.get("agree", 0))
    aug_gap = float(train_after.get("agree", 0) - train_aug.get("agree", 0))

    report = {
        "track": "meta_policy_forge_learn",
        "law": "A34_learn_not_memorize",
        "doctrine": "unique_teachers_heldout_augment_l2l_goal_context_no_multihit",
        "start_src": start_src,
        "n_unique_path": len(unique),
        "n_train_path": len(train_t),
        "n_hold_path": len(hold_t),
        "train_dates": train_dates,
        "hold_dates": hold_dates,
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
        "mix": {
            "fire_frac": fire_frac,
            "path_frac": path_frac,
            "synth_frac": synth_frac,
            "wait_frac": wait_frac,
            "noise": noise,
            "holdout_frac": holdout_frac,
            "multi_hit": 0,
        },
        "agreement": {
            "train_exact_before": train_before,
            "hold_exact_before": hold_before,
            "train_exact_after": train_after,
            "hold_exact_after": hold_after,
            "train_aug_after": train_aug,
            "hold_aug_after": hold_aug,
            "memorization_gap_train_minus_hold": mem_gap,
            "aug_sensitivity_train_exact_minus_aug": aug_gap,
        },
        "generalization_ok": bool(
            hold_after.get("agree", 0) >= 0.45
            and mem_gap < 0.35
            and hold_after.get("fire_agree", 0) >= 0.40
        ),
        "lr": lr,
        "seed": seed,
        "saved": saved,
        "champion_untouched": True,
        "inference_force_pad": False,
        "elapsed_note": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "measure": "holdout_agree + forward mean_trades/n_zero/a13 — not coach CE",
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "track": "forge_learn",
                "meta_train_steps": int(pol.meta_train_steps),
                "fingerprint": pol.weight_fingerprint(),
                "hold_agree": hold_after.get("agree"),
                "mem_gap": mem_gap,
                "champion_untouched": True,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Learn-not-memorize forge curriculum")
    p.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    p.add_argument("--lr", type=float, default=DEFAULT_LR)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--path-frac", type=float, default=DEFAULT_PATH_FRAC)
    p.add_argument("--synth-frac", type=float, default=DEFAULT_SYNTH_FRAC)
    p.add_argument("--wait-frac", type=float, default=DEFAULT_WAIT_FRAC)
    p.add_argument("--noise", type=float, default=DEFAULT_NOISE)
    p.add_argument("--holdout-frac", type=float, default=0.25)
    p.add_argument("--path-state", type=str, default=str(DEFAULT_PATH_STATE))
    p.add_argument("--warmstart-intense", action="store_true")
    p.add_argument("--continue", dest="cont", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)
    rep = train_forge_learn(
        steps=int(args.steps),
        lr=float(args.lr),
        seed=int(args.seed),
        path_frac=float(args.path_frac),
        synth_frac=float(args.synth_frac),
        wait_frac=float(args.wait_frac),
        noise=float(args.noise),
        holdout_frac=float(args.holdout_frac),
        path_state_path=Path(args.path_state),
        from_prior=not args.cont and not args.warmstart_intense,
        warmstart_intense=bool(args.warmstart_intense),
        warmstart_learn=bool(args.cont),
    )
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
