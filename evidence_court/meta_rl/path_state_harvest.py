"""CASE-0037 / C-003 residual: packed path-state teachers at brain-wait misses.

Anti F-025: do **not** rebuild official state from label fields. Train on the
exact ``build_meta_rl_state`` vector the brain saw when it waited on a real
Mark candidate. Offline only — never live force-pad.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np

from .edge import build_tf_cache
from .goal_path import run_goal_path_day
from .policy import (
    FrozenMetaPolicy,
    load_or_train_champion,
    train_goal_conditioned_meta_policy,
    MetaPolicy,
)
from .price_io import SYMBOL_FILES, available_symbols, bars_to_daily, load_m1_trailing_calendar_days
from .state import META_RL_DIM

DEFAULT_PACK_OUT = Path("evidence_court/artifacts/path_state_teachers_case0037.json")
DEFAULT_SHADOW_OUT = Path("evidence_court/artifacts/meta_policy_case0037_pathstate.npz")
ACTIONABLE = frozenset({"pullback_resume", "continuation"})


def filter_path_state_teachers(
    examples: Sequence[Dict[str, Any]],
    *,
    max_examples: int = 400,
) -> List[Dict[str, Any]]:
    """Keep only full-dim state + long/short teachers + PB/cont topology."""
    out: List[Dict[str, Any]] = []
    for ex in examples:
        if not isinstance(ex, dict):
            continue
        st = ex.get("state")
        if st is None:
            continue
        arr = np.asarray(st, dtype=np.float64).ravel()
        if arr.size != META_RL_DIM:
            continue
        if not np.all(np.isfinite(arr)):
            continue
        act = str(ex.get("teacher_act") or "")
        if act not in ("long", "short"):
            continue
        topo = str(ex.get("topology") or "")
        if topo not in ACTIONABLE:
            continue
        src = str(ex.get("source") or "")
        if src not in ("path_state_miss", "path_state", "path_state_watch_miss"):
            # allow explicit path sources only (anti synthetic smuggle)
            if "path_state" not in src:
                continue
        row = dict(ex)
        row["state"] = [float(x) for x in arr]
        row["teacher_act"] = act
        row["source"] = src if "path_state" in src else "path_state_miss"
        out.append(row)
        if len(out) >= int(max_examples):
            break
    return out


def apply_path_state_teachers_to_brain(
    brain: Any,
    examples: Sequence[Dict[str, Any]],
    *,
    lr: float = 0.02,
    seed: int = 11,
    max_examples: int = 500,
    n_passes: int = 1,
) -> int:
    """Offline meta_update on packed path states. Returns update count."""
    labs = filter_path_state_teachers(examples, max_examples=max_examples)
    if not labs:
        return 0
    if getattr(brain, "frozen_for_inference", False):
        brain.unlock_for_meta_train()
    rng = np.random.default_rng(seed)
    n = 0
    for _ in range(max(1, int(n_passes))):
        order = list(labs)
        rng.shuffle(order)
        for ex in order:
            st = np.asarray(ex["state"], dtype=np.float64).ravel()
            teacher = str(ex["teacher_act"])
            w = float(ex.get("weight") or 1.0)
            sf = float(ex.get("teacher_size_frac") or 0.65)
            brain.meta_update(
                st,
                teacher_act=teacher,
                lr=lr,
                reward=1.0 + 0.25 * min(w, 2.0),
                teacher_size_frac=sf,
            )
            n += 1
    brain.trained = True
    return n


def harvest_path_state_teachers(
    *,
    n_days: int = 30,
    seed: int = 42,
    max_examples: int = 400,
    max_per_day: int = 80,
    warmup_days: int = 10,
    policy: Optional[FrozenMetaPolicy] = None,
    symbols: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    """Run real path with collect_path_state_teachers; return packed examples."""
    syms = list(symbols) if symbols else [
        s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()
    ]
    if not syms:
        return {
            "examples": [],
            "n_days": 0,
            "n_examples": 0,
            "error": "no_symbols",
            "source": "path_state_miss",
        }

    pol = policy if policy is not None else load_or_train_champion(seed=seed, n_steps=2500)
    trail = max(int(n_days) + int(warmup_days) + 5, 40)
    m1_by_sym: Dict[str, List[dict]] = {}
    daily_by_sym: Dict[str, List[dict]] = {}
    tf_cache_by_symbol: Dict[str, Dict[str, List[dict]]] = {}
    for sym in syms:
        path = SYMBOL_FILES.get(sym)
        if path is None or not path.exists():
            continue
        m1 = load_m1_trailing_calendar_days(path, n_days=trail)
        if not m1:
            continue
        m1_by_sym[sym] = m1
        daily_by_sym[sym] = bars_to_daily(m1)
        tf_cache_by_symbol[sym] = build_tf_cache(m1)

    if not daily_by_sym:
        return {
            "examples": [],
            "n_days": 0,
            "n_examples": 0,
            "error": "price_data_missing",
            "source": "path_state_miss",
        }

    date_sets = [set(d["date"] for d in days) for days in daily_by_sym.values()]
    common = sorted(set.intersection(*date_sets)) if len(date_sets) > 1 else sorted(date_sets[0])
    need = int(n_days) + int(warmup_days)
    window = common[-need:] if len(common) >= need else common
    eval_dates = window[int(warmup_days) :] if len(window) > int(warmup_days) else window[1:]
    eval_dates = eval_dates[-int(n_days) :]

    raw: List[Dict[str, Any]] = []
    day_stats: List[Dict[str, Any]] = []
    rng = np.random.default_rng(seed)
    for i, date in enumerate(eval_dates):
        t = float(rng.choice([5.0, 15.0, 30.0, 50.0, 70.0])) if i % 2 else 15.0
        r = float(rng.choice([1.0, 2.0, 3.0]))
        fills, ledger, gmeta = run_goal_path_day(
            pol,
            date=date,
            m1_by_symbol=m1_by_sym,
            target_percent=t,
            max_daily_risk_percent=r,
            symbols=list(m1_by_sym.keys()),
            tf_cache_by_symbol=tf_cache_by_symbol,
            brain_drives=True,
            watch_enabled=True,
            collect_path_state_teachers=True,
            max_path_state_teachers=int(max_per_day),
        )
        exs = list(gmeta.get("path_state_teachers") or [])
        for ex in exs:
            if isinstance(ex, dict):
                row = dict(ex)
                row["harvest_day_target"] = t
                row["harvest_day_risk"] = r
                row["harvest_day_n_trades"] = len(fills)
                raw.append(row)
        day_stats.append(
            {
                "date": date,
                "n_trades": len(fills),
                "n_teachers": len(exs),
                "pnl": float(ledger.realized_pnl_percent),
                "target": t,
                "risk": r,
            }
        )

    filtered = filter_path_state_teachers(raw, max_examples=max_examples)
    n_ln = sum(1 for x in filtered if str(x.get("session_band")) == "london_ny")
    n_zero = sum(1 for d in day_stats if int(d["n_trades"]) == 0)
    # dim integrity sample
    dims_ok = all(len(x["state"]) == META_RL_DIM for x in filtered)
    return {
        "examples": filtered,
        "n_days": len(eval_dates),
        "n_raw": len(raw),
        "n_examples": len(filtered),
        "n_london_ny": n_ln,
        "n_zero_trade_days": n_zero,
        "dims_ok": dims_ok,
        "meta_rl_dim": META_RL_DIM,
        "day_stats_head": day_stats[:8],
        "source": "path_state_miss",
        "law": "A28_C003_CASE0037",
        "policy_fingerprint": pol.weight_fingerprint(),
        "symbols": list(m1_by_sym.keys()),
        "window_start": eval_dates[0] if eval_dates else None,
        "window_end": eval_dates[-1] if eval_dates else None,
    }


def save_path_state_pack(pack: Dict[str, Any], path: Path | str = DEFAULT_PACK_OUT) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    # compact: keep examples; strip day_stats tail if huge already head-only
    p.write_text(json.dumps(pack), encoding="utf-8")
    return p


def train_path_state_a13_policy(
    examples: Sequence[Dict[str, Any]],
    *,
    seed: int = 42,
    n_steps: int = 2500,
    path_mix: float = 0.35,
    freeze: bool = True,
    save_path: Optional[Path | str] = None,
) -> MetaPolicy:
    """Base meta-train + offline path-state teacher mix. Shadow only by default."""
    labs = filter_path_state_teachers(examples, max_examples=max(50, len(examples)))
    if not labs:
        raise ValueError("no path-state teachers to train on")
    # Base curriculum first (no opportunity_labels — those rebuild synthetic state)
    pol = train_goal_conditioned_meta_policy(
        seed=seed,
        n_steps=n_steps,
        freeze=False,
        opportunity_labels=None,
    )
    brain = pol.brain
    n_extra = max(1, int(n_steps * float(path_mix)))
    # first pass all labels, then mix extras
    apply_path_state_teachers_to_brain(
        brain, labs, lr=0.02, seed=seed + 7, max_examples=len(labs), n_passes=1
    )
    rng = np.random.default_rng(seed + 3)
    for i in range(n_extra):
        ex = labs[int(rng.integers(0, len(labs)))]
        st = np.asarray(ex["state"], dtype=np.float64).ravel()
        brain.meta_update(
            st,
            teacher_act=str(ex["teacher_act"]),
            lr=0.018 * (0.95 ** (i // 50)),
            reward=1.2,
            teacher_size_frac=float(ex.get("teacher_size_frac") or 0.65),
        )
    pol.trained = True
    pol.meta_train_steps = brain.meta_train_steps
    if freeze:
        pol.freeze_for_inference()
    if save_path is not None:
        pol.save(Path(save_path))
    return pol
