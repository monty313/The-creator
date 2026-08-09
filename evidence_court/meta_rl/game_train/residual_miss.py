"""Residual miss curriculum — train on *actual* Watch PB/cont misses (no multi-hit).

After learn track still leaves ~13% Watch miss (esp. EURUSD continuation):
  harvest full curriculum_labels from frozen shadow → unique offline teachers →
  augment (goal×risk, L2L, noise) → meta_update on learn warmstart.

Never multi-hit exact vectors. Never inference pad. Champion untouched.
"""
from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from evidence_court.meta_rl.edge import build_tf_cache
from evidence_court.meta_rl.game_train.forge_learn import (
    UniqueTeacher,
    _augment_teacher,
    _synth_principle,
    _teacher_agreement,
)
from evidence_court.meta_rl.goal_path import run_goal_path_day
from evidence_court.meta_rl.policy import (
    MetaPolicy,
    opportunity_label_to_training_example,
)
from evidence_court.meta_rl.price_io import (
    SYMBOL_FILES,
    available_symbols,
    bars_to_daily,
    load_m1_trailing_calendar_days,
)
from evidence_court.meta_rl.state import META_RL_DIM

_REPO = Path(__file__).resolve().parents[2]
GT = _REPO / "artifacts" / "game_train"
ART = _REPO / "artifacts"
MISS_PACK = GT / "residual_watch_misses.json"
OUT_NPZ = GT / "meta_policy_forge_residual.npz"
OUT_JSON = GT / "meta_policy_forge_residual.json"
REPORT = GT / "meta_policy_forge_residual_report.json"
LEARN_NPZ = GT / "meta_policy_forge_learn.npz"

DEFAULT_STEPS = 12000
DEFAULT_LR = 0.014
DEFAULT_MISS_FRAC = 0.55  # residual stream
DEFAULT_SYNTH_FRAC = 0.20
DEFAULT_WAIT_FRAC = 0.10
# rest = light path-style balance via synth fire
DEFAULT_NOISE = 0.05
TARGETS = (5.0, 10.0, 15.0, 30.0, 50.0, 70.0, 90.0)
RISKS = (1.0, 2.0, 3.0)


def harvest_watch_misses(
    *,
    policy_path: Path = LEARN_NPZ,
    n_days: int = 16,
    seed: int = 42,
    max_labels: int = 2000,
    aggressive_capture: bool = True,
) -> Dict[str, Any]:
    """Run goal_path with Watch; collect unique miss labels + *path-state* at miss."""
    pol = MetaPolicy.load(policy_path, freeze=True, require_serious=False)
    syms = [s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()]
    trail = int(n_days) + 20
    m1_by: Dict[str, List[dict]] = {}
    tf_cache: Dict[str, Dict[str, List[dict]]] = {}
    daily_by: Dict[str, List[dict]] = {}
    for sym in syms:
        p = SYMBOL_FILES.get(sym)
        if p is None or not p.exists():
            continue
        m1 = load_m1_trailing_calendar_days(p, n_days=trail)
        if not m1:
            continue
        m1_by[sym] = m1
        daily_by[sym] = bars_to_daily(m1)
        tf_cache[sym] = build_tf_cache(m1)

    date_sets = [set(d["date"] for d in days) for days in daily_by.values()]
    common = (
        sorted(set.intersection(*date_sets)) if len(date_sets) > 1 else sorted(date_sets[0])
    )
    eval_dates = common[-int(n_days) :]
    rng = np.random.default_rng(seed)

    raw_labels: List[Dict[str, Any]] = []
    raw_path: List[Dict[str, Any]] = []
    day_stats: List[Dict[str, Any]] = []
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
            max_path_state_teachers=250,
            aggressive_capture=bool(aggressive_capture),
        )
        wsum = gmeta.get("watch") or {}
        labs = list(wsum.get("curriculum_labels") or gmeta.get("curriculum_labels") or [])
        for lab in labs:
            if not isinstance(lab, dict):
                continue
            row = dict(lab)
            row["source"] = "watch_residual_miss"
            row["harvest_day_target"] = t
            row["harvest_day_risk"] = r
            row["harvest_day_n_trades"] = len(fills)
            row["asof_date"] = str(row.get("asof_date") or date)
            raw_labels.append(row)
        # Prefer real path-state at Watch miss (anti F-025)
        for ex in gmeta.get("path_state_teachers") or []:
            if not isinstance(ex, dict):
                continue
            if "path_state" not in str(ex.get("source") or ""):
                continue
            row = dict(ex)
            row["harvest_day_target"] = t
            row["harvest_day_risk"] = r
            raw_path.append(row)
        day_stats.append(
            {
                "date": date,
                "n_trades": len(fills),
                "n_miss_labels": len(labs),
                "n_path_state": len(gmeta.get("path_state_teachers") or []),
                "watch_misses": int(gmeta.get("watch_n_misses") or 0),
                "watch_opp": int(gmeta.get("watch_n_opportunities") or 0),
                "watch_hits": int(gmeta.get("watch_n_hits") or 0),
                "target": t,
                "risk": r,
            }
        )

    def _dedupe_labels(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen: set[str] = set()
        unique: List[Dict[str, Any]] = []
        for lab in rows:
            act = str(lab.get("teacher_act") or lab.get("side") or "")
            if act not in ("long", "short"):
                continue
            topo = str(lab.get("topology") or "")
            if topo not in ("pullback_resume", "continuation"):
                continue
            key = "|".join(
                [
                    str(lab.get("asof_date") or ""),
                    str(lab.get("asof_time") or ""),
                    str(lab.get("symbol") or ""),
                    topo,
                    act,
                    str(lab.get("set_id") or ""),
                    str(lab.get("source") or ""),
                ]
            )
            if key in seen:
                continue
            seen.add(key)
            unique.append(lab)
            if len(unique) >= int(max_labels):
                break
        return unique

    unique_path = _dedupe_labels(raw_path)
    unique_labels = _dedupe_labels(raw_labels)
    # Prefer path-state teachers for training payload
    primary = unique_path if unique_path else unique_labels
    topo_c = Counter(str(x.get("topology")) for x in primary)
    sym_c = Counter(str(x.get("symbol")) for x in primary)
    band_c = Counter(str(x.get("session_band")) for x in primary)
    pack = {
        "labels": unique_labels,
        "path_state_teachers": unique_path,
        "n_labels": len(unique_labels),
        "n_path_state": len(unique_path),
        "n_primary": len(primary),
        "primary": "path_state" if unique_path else "rebuilt_label",
        "n_raw_labels": len(raw_labels),
        "n_raw_path": len(raw_path),
        "n_days": len(eval_dates),
        "topo": dict(topo_c),
        "symbols": dict(sym_c),
        "session_band": dict(band_c),
        "day_stats": day_stats,
        "source_policy": str(policy_path),
        "source_fingerprint": pol.weight_fingerprint(),
        "window": [eval_dates[0], eval_dates[-1]] if eval_dates else [],
        "law": "A28_residual_miss_path_state",
        "multi_hit": 0,
    }
    MISS_PACK.parent.mkdir(parents=True, exist_ok=True)
    MISS_PACK.write_text(json.dumps(pack, indent=2), encoding="utf-8")
    return pack


def _rows_to_unique_teachers(
    rows: Sequence[Dict[str, Any]],
    *,
    seed: int = 0,
    prefer_path_state: bool = True,
) -> List[UniqueTeacher]:
    """Path-state rows preferred; rebuilt labels only as fallback."""
    rng = np.random.default_rng(seed)
    out: List[UniqueTeacher] = []
    for lab in rows:
        act = str(lab.get("teacher_act") or lab.get("side") or "")
        if act not in ("long", "short"):
            continue
        topo = str(lab.get("topology") or "pullback_resume")
        band = str(lab.get("session_band") or "other")
        st_raw = lab.get("state")
        if prefer_path_state and st_raw is not None:
            arr = np.asarray(st_raw, dtype=np.float64).ravel()
            if arr.size != META_RL_DIM or not np.all(np.isfinite(arr)):
                continue
            st = arr[:META_RL_DIM].copy()
            teacher = act
            sf = float(lab.get("teacher_size_frac") or 0.65)
            src = str(lab.get("source") or "path_state_watch_miss")
        else:
            target = float(lab.get("harvest_day_target") or rng.choice(TARGETS))
            risk = float(lab.get("harvest_day_risk") or rng.choice(RISKS))
            st, teacher, sf = opportunity_label_to_training_example(
                lab, target=target, risk=risk, rng=rng
            )
            if teacher not in ("long", "short"):
                teacher = act
            st = np.asarray(st, dtype=np.float64).ravel()[:META_RL_DIM].copy()
            src = "watch_residual_miss_rebuilt"
        w = float(lab.get("weight") or 1.0)
        if topo == "continuation":
            w *= 1.35
        if str(lab.get("symbol") or "").upper() == "EURUSD":
            w *= 1.4
        if band == "london_ny":
            w = max(w, 1.5)
        out.append(
            UniqueTeacher(
                state=st,
                teacher_act=teacher,
                size_frac=float(sf) if teacher != "wait" else 0.6,
                topology=topo,
                session_band=band,
                asof_date=str(lab.get("asof_date") or ""),
                symbol=str(lab.get("symbol") or ""),
                weight=w,
                source=src,
            )
        )
    return out


def _weighted_pick(
    rng: np.random.Generator,
    teachers: Sequence[UniqueTeacher],
    k: int,
) -> List[UniqueTeacher]:
    if not teachers or k <= 0:
        return []
    weights = np.array([max(t.weight, 0.1) for t in teachers], dtype=np.float64)
    # boost cont / eurusd again at sample time
    for i, t in enumerate(teachers):
        if t.topology == "continuation":
            weights[i] *= 1.25
        if t.symbol.upper() == "EURUSD":
            weights[i] *= 1.3
    weights = weights / weights.sum()
    idx = rng.choice(len(teachers), size=k, replace=True, p=weights)
    return [teachers[int(i)] for i in idx]


def train_residual_miss(
    *,
    steps: int = DEFAULT_STEPS,
    lr: float = DEFAULT_LR,
    seed: int = 42,
    miss_frac: float = DEFAULT_MISS_FRAC,
    synth_frac: float = DEFAULT_SYNTH_FRAC,
    wait_frac: float = DEFAULT_WAIT_FRAC,
    noise: float = DEFAULT_NOISE,
    miss_pack: Optional[Path] = None,
    warmstart_learn: bool = True,
    reharvest: bool = True,
    harvest_days: int = 16,
    aggressive_capture: bool = True,
) -> Dict[str, Any]:
    GT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    pack_path = Path(miss_pack) if miss_pack else MISS_PACK

    if reharvest or not pack_path.exists():
        pack = harvest_watch_misses(
            policy_path=LEARN_NPZ if LEARN_NPZ.exists() else pack_path,
            n_days=harvest_days,
            seed=seed,
            aggressive_capture=bool(aggressive_capture),
        )
    else:
        pack = json.loads(pack_path.read_text(encoding="utf-8"))

    labels = list(pack.get("labels") or [])
    path_rows = list(pack.get("path_state_teachers") or [])
    # Prefer real path-state at miss; fallback to rebuilt labels
    primary_rows = path_rows if path_rows else labels
    teachers = _rows_to_unique_teachers(
        primary_rows, seed=seed + 3, prefer_path_state=bool(path_rows)
    )
    # hold out last 20% of dates among residual
    dates = sorted({t.asof_date for t in teachers if t.asof_date})
    n_hold = max(1, int(round(len(dates) * 0.2))) if dates else 0
    hold_dates = set(dates[-n_hold:]) if dates else set()
    train_t = [t for t in teachers if t.asof_date not in hold_dates] or list(teachers)
    hold_t = [t for t in teachers if t.asof_date in hold_dates]

    if warmstart_learn and LEARN_NPZ.exists():
        pol = MetaPolicy.load(LEARN_NPZ, freeze=True, require_serious=False)
        pol.unlock_for_meta_train()
        start_src = "learn_warmstart"
    elif OUT_NPZ.exists():
        pol = MetaPolicy.load(OUT_NPZ, freeze=True, require_serious=False)
        pol.unlock_for_meta_train()
        start_src = "residual_continue"
    else:
        pol = MetaPolicy.untrained_prior(seed=seed)
        pol.unlock_for_meta_train()
        start_src = "prior"

    steps_before = int(pol.meta_train_steps)
    fp_before = pol.weight_fingerprint()
    hold_before = _teacher_agreement(pol, hold_t, seed=seed + 1, augment=False)
    train_before = _teacher_agreement(pol, train_t, seed=seed + 2, augment=False)

    losses: List[float] = []
    applied_acts: Counter = Counter()
    applied_tags: Counter = Counter()
    applied = 0
    bs = 32
    n_batches = max(1, int(np.ceil(steps / bs)))

    for bi in range(n_batches):
        if applied >= steps:
            break
        need = min(bs, steps - applied)
        n_miss = int(need * miss_frac) if train_t else 0
        n_synth = int(need * synth_frac)
        n_wait = int(need * wait_frac)
        n_fire = max(0, need - n_miss - n_synth - n_wait)
        batch = []

        # Residual misses — always augmented (never raw multi-hit)
        for t in _weighted_pick(rng, train_t, n_miss):
            batch.append(
                _augment_teacher(
                    rng, t, noise=noise, do_l2l=True, reencode_goal=True
                )
            )
        # Extra cont emphasis: one more aug pass preference
        cont_only = [t for t in train_t if t.topology == "continuation"]
        if cont_only and n_miss > 0 and rng.random() < 0.4:
            t = cont_only[int(rng.integers(0, len(cont_only)))]
            batch.append(
                _augment_teacher(rng, t, noise=noise * 1.1, do_l2l=True, reencode_goal=True)
            )

        for _ in range(n_synth + n_fire):
            batch.append(_synth_principle(rng, "fire" if rng.random() < 0.75 else "general"))
        for _ in range(n_wait):
            batch.append(_synth_principle(rng, "load"))

        rng.shuffle(batch)
        step_lr = lr * (0.985 ** (applied // 400))
        for ex in batch:
            if applied >= steps:
                break
            st = np.zeros(META_RL_DIM, dtype=np.float64)
            n = min(META_RL_DIM, int(ex.state.size))
            st[:n] = ex.state[:n]
            # residual boost LR on cont tags
            use_lr = step_lr
            if "continuation" in ex.tag or ex.tag.startswith("aug:"):
                if "continuation" in ex.tag:
                    use_lr *= 1.2
            loss = pol.meta_update(
                st,
                teacher_act=ex.teacher_act,
                lr=use_lr,
                reward=ex.reward,
                teacher_size_frac=ex.size_frac,
            )
            losses.append(float(loss))
            applied_acts[ex.teacher_act] += 1
            applied_tags[ex.tag.split(":")[0]] += 1
            applied += 1

    if applied > 0:
        pol.brain.trained = True
    pol.freeze_for_inference()
    saved = str(pol.save(OUT_NPZ))

    hold_after = _teacher_agreement(pol, hold_t, seed=seed + 3, augment=False)
    hold_aug = _teacher_agreement(pol, hold_t, seed=seed + 4, augment=True)
    train_after = _teacher_agreement(pol, train_t, seed=seed + 5, augment=False)
    train_aug = _teacher_agreement(pol, train_t, seed=seed + 6, augment=True)
    mem_gap = float(train_after.get("agree", 0) - hold_after.get("agree", 0))

    report = {
        "track": "meta_policy_forge_residual",
        "law": "A28_residual_watch_miss_no_multihit",
        "doctrine": "train_on_actual_pb_cont_misses_augmented_eurusd_cont_boost",
        "start_src": start_src,
        "n_miss_labels": len(labels),
        "n_path_state": len(path_rows),
        "primary": pack.get("primary"),
        "n_unique_teachers": len(teachers),
        "n_train": len(train_t),
        "n_hold": len(hold_t),
        "hold_dates": sorted(hold_dates),
        "pack_topo": pack.get("topo"),
        "pack_symbols": pack.get("symbols"),
        "steps_applied": applied,
        "steps_before": steps_before,
        "steps_after": int(pol.meta_train_steps),
        "fingerprint_before": fp_before,
        "fingerprint_after": pol.weight_fingerprint(),
        "mean_loss": float(np.mean(losses)) if losses else None,
        "applied_acts": dict(applied_acts),
        "applied_tags": dict(applied_tags),
        "mix": {
            "miss_frac": miss_frac,
            "synth_frac": synth_frac,
            "wait_frac": wait_frac,
            "noise": noise,
            "multi_hit": 0,
        },
        "agreement": {
            "train_before": train_before,
            "hold_before": hold_before,
            "train_after": train_after,
            "hold_after": hold_after,
            "train_aug": train_aug,
            "hold_aug": hold_aug,
            "mem_gap": mem_gap,
        },
        "lr": lr,
        "seed": seed,
        "saved": saved,
        "miss_pack": str(pack_path),
        "aggressive_capture_harvest": bool(aggressive_capture),
        "champion_untouched": True,
        "inference_force_pad": False,
        "elapsed_note": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "track": "forge_residual",
                "meta_train_steps": int(pol.meta_train_steps),
                "fingerprint": pol.weight_fingerprint(),
                "n_miss_labels": len(labels),
                "champion_untouched": True,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Residual Watch miss curriculum")
    p.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    p.add_argument("--lr", type=float, default=DEFAULT_LR)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--miss-frac", type=float, default=DEFAULT_MISS_FRAC)
    p.add_argument("--harvest-days", type=int, default=16)
    p.add_argument("--no-reharvest", action="store_true")
    p.add_argument("--harvest-only", action="store_true")
    p.add_argument("--no-aggressive", action="store_true", help="Disable aggressive_capture harvest")
    args = p.parse_args(list(argv) if argv is not None else None)
    if args.harvest_only:
        pack = harvest_watch_misses(
            n_days=int(args.harvest_days),
            seed=int(args.seed),
            aggressive_capture=not bool(args.no_aggressive),
        )
        print(
            json.dumps(
                {k: pack[k] for k in pack if k not in ("labels", "path_state_teachers")},
                indent=2,
            )
        )
        return 0
    rep = train_residual_miss(
        steps=int(args.steps),
        lr=float(args.lr),
        seed=int(args.seed),
        miss_frac=float(args.miss_frac),
        reharvest=not bool(args.no_reharvest),
        harvest_days=int(args.harvest_days),
        aggressive_capture=not bool(args.no_aggressive),
    )
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
