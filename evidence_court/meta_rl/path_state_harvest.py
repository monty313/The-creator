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
from .goal_path import (
    PRODUCTION_SCALPING_SLOTS_15M,
    build_scalping_cadence_slots,
    run_goal_path_day,
)
from .policy import (
    FrozenMetaPolicy,
    load_or_train_champion,
    train_goal_conditioned_meta_policy,
    MetaPolicy,
)
from .price_io import SYMBOL_FILES, available_symbols, bars_to_daily, load_m1_trailing_calendar_days
from .state import META_RL_DIM

DEFAULT_PACK_OUT = Path("evidence_court/artifacts/teachers/path_state_teachers_case0037.json")
DEFAULT_SHADOW_OUT = Path(
    "evidence_court/artifacts/policies_lab/meta_policy_case0037_pathstate.npz"
)
ACTIONABLE = frozenset({"pullback_resume", "continuation"})


def filter_path_state_teachers(
    examples: Sequence[Dict[str, Any]],
    *,
    max_examples: int = 400,
    require_htf_active: bool = True,
    allow_wait: bool = False,
) -> List[Dict[str, Any]]:
    """Keep full-dim path teachers + PB/cont topology.

    Default: long/short only (density/path-state clone path).
    ``allow_wait`` (conversion mode): also keep wait teachers so dead-R /
    thrash lessons are not filtered out before conversion remap.
    ``require_htf_active`` (default True): drop examples with no live HTF set.
    """
    allowed_acts = ("long", "short", "wait") if allow_wait else ("long", "short")
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
        if act not in allowed_acts:
            continue
        topo = str(ex.get("topology") or "")
        # wait teachers may carry chop/load topology for dead-R lessons
        if act in ("long", "short") and topo not in ACTIONABLE:
            continue
        if act == "wait" and topo and topo not in ACTIONABLE and topo not in (
            "chop",
            "slingshot_load",
            "load",
            "collapse",
        ):
            # still allow empty / unknown topology on wait
            if topo not in ("", "unknown", "none"):
                pass  # keep wait anyway — conversion labels it
        src = str(ex.get("source") or "")
        allowed_src = (
            "path_state_miss",
            "path_state",
            "path_state_watch_miss",
            "path_state_htf_active",
            "path_state_side_miss",
            "path_state_conversion",
            "path_state_dead",
            "path_state_clear",
            "path_state_near_breach",
            # Trade Mental Replay (3TF × before/during/after) offline teachers
            "path_state_mental_replay",
            "path_state_mental_replay_dead",
            "path_state_mental_replay_hold",
            "path_state_mental_replay_clear",
        )
        if src not in allowed_src:
            # allow explicit path sources only (anti synthetic smuggle)
            if "path_state" not in src:
                continue
        n_act = int(ex.get("n_htf_active") or 0)
        if require_htf_active:
            # Strict: must carry collector-set n_htf_active >= 1 (no stamp-launder)
            if n_act < 1:
                continue
        row = dict(ex)
        row["state"] = [float(x) for x in arr]
        row["teacher_act"] = act
        row["source"] = src if "path_state" in src else "path_state_miss"
        row["n_htf_active"] = n_act
        if require_htf_active:
            row["htf_active"] = True
        elif n_act >= 1:
            row["htf_active"] = True
        else:
            row["htf_active"] = bool(ex.get("htf_active") is True)
        out.append(row)
    # Prefer high-weight (L/NY, multi-HTF active) when capping
    out.sort(
        key=lambda r: (
            float(r.get("weight") or 1.0),
            int(r.get("n_htf_active") or 0),
            1 if str(r.get("session_band")) == "london_ny" else 0,
        ),
        reverse=True,
    )
    return out[: int(max_examples)]


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
    monty_htf_blend: bool = False,
    require_htf_active: bool = True,
    checkpoint_every: int = 25,
    checkpoint_path: Optional[Path | str] = None,
    resume_from_partial: bool = True,
    harvest_slots: Optional[Sequence[str]] = None,
    watch_enabled: bool = False,
) -> Dict[str, Any]:
    """Run real path with collect_path_state_teachers; return packed examples.

    ``monty_htf_blend=True``: harvest under Monty slope+CCI/RSI HTF force so
    teacher states include real source flags (doctrine 12–14) and blend force.

    ``require_htf_active``: keep only moments where ≥1 official HTF set is live.
    ``resume_from_partial``: if checkpoint exists with days_done, skip those days.
    ``harvest_slots``: default 15m cadence (faster year harvest; dual still uses 5m).
    ``watch_enabled``: default False on harvest (speed; teachers from path collect).
    """
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
    start_i = 0
    ckpt = Path(checkpoint_path) if checkpoint_path else None
    if resume_from_partial and ckpt is not None and ckpt.exists():
        try:
            prev = json.loads(ckpt.read_text(encoding="utf-8"))
            # Prefer full raw list if present; else examples only
            if isinstance(prev.get("raw"), list) and prev["raw"]:
                raw = list(prev["raw"])
            elif isinstance(prev.get("examples"), list):
                raw = list(prev["examples"])
            start_i = int(prev.get("days_done") or 0)
            start_i = max(0, min(start_i, len(eval_dates)))
            print(f"  resume harvest from day index {start_i}/{len(eval_dates)} raw={len(raw)}", flush=True)
        except Exception as exc:
            print(f"  resume partial failed ({exc}); starting fresh", flush=True)
            raw = []
            start_i = 0
    rng = np.random.default_rng(seed)
    # advance rng to match skipped days (even i: fixed t=15, only risk draw; odd: both)
    for j in range(start_i):
        if j % 2:
            _ = float(rng.choice([5.0, 15.0, 30.0, 50.0, 70.0]))
        _ = float(rng.choice([1.0, 2.0, 3.0]))
    for i, date in enumerate(eval_dates):
        if i < start_i:
            continue
        t = float(rng.choice([5.0, 15.0, 30.0, 50.0, 70.0])) if i % 2 else 15.0
        r = float(rng.choice([1.0, 2.0, 3.0]))
        if harvest_slots is not None:
            slots = list(harvest_slots)
        else:
            # Year harvest default: 30m grid (~27 slots) for throughput; dual uses 5m.
            slots = list(build_scalping_cadence_slots(interval_minutes=30))  # kw-only
        # Multi-symbol path still; cache lookup per sym
        fills, ledger, gmeta = run_goal_path_day(
            pol,
            date=date,
            m1_by_symbol=m1_by_sym,
            target_percent=t,
            max_daily_risk_percent=r,
            symbols=list(m1_by_sym.keys()),
            tf_cache_by_symbol=tf_cache_by_symbol,
            slots=slots,
            brain_drives=True,
            watch_enabled=bool(watch_enabled),
            collect_path_state_teachers=True,
            max_path_state_teachers=int(max_per_day),
            monty_htf_blend=bool(monty_htf_blend),
        )
        exs = list(gmeta.get("path_state_teachers") or [])
        day_pnl = float(ledger.realized_pnl_percent)
        from .path_learning import stamp_path_teacher_day_outcome

        for ex in exs:
            if isinstance(ex, dict):
                row = stamp_path_teacher_day_outcome(
                    ex,
                    day_pnl=day_pnl,
                    target_percent=t,
                    max_daily_risk_percent=r,
                    n_trades=len(fills),
                )
                row["asof_date"] = str(date)
                raw.append(row)
        day_stats.append(
            {
                "date": date,
                "n_trades": len(fills),
                "n_teachers": len(exs),
                "pnl": day_pnl,
                "target": t,
                "risk": r,
                "hit": day_pnl >= t - 1e-9,
                "breach": day_pnl < -r - 1e-9,
            }
        )
        if ckpt and checkpoint_every > 0 and (i + 1) % int(checkpoint_every) == 0:
            partial = filter_path_state_teachers(
                raw, max_examples=max_examples, require_htf_active=require_htf_active
            )
            ckpt.parent.mkdir(parents=True, exist_ok=True)
            ckpt.write_text(
                json.dumps(
                    {
                        "partial": True,
                        "days_done": i + 1,
                        "n_raw": len(raw),
                        "n_examples": len(partial),
                        "examples": partial,
                        "raw": raw,  # full list for resume
                    }
                ),
                encoding="utf-8",
            )
            print(
                f"  harvest ckpt day {i+1}/{len(eval_dates)} raw={len(raw)} kept={len(partial)}",
                flush=True,
            )

    filtered = filter_path_state_teachers(
        raw, max_examples=max_examples, require_htf_active=require_htf_active
    )
    n_ln = sum(1 for x in filtered if str(x.get("session_band")) == "london_ny")
    n_zero = sum(1 for d in day_stats if int(d["n_trades"]) == 0)
    n_htf = sum(1 for x in filtered if int(x.get("n_htf_active") or 0) >= 1)
    # dim integrity sample
    dims_ok = all(len(x["state"]) == META_RL_DIM for x in filtered)
    if require_htf_active and filtered:
        bad = [i for i, x in enumerate(filtered) if int(x.get("n_htf_active") or 0) < 1]
        if bad:
            raise ValueError(
                f"HTF-active pack integrity fail: {len(bad)} rows missing n_htf_active>=1"
            )
    return {
        "examples": filtered,
        "n_days": len(eval_dates),
        "n_raw": len(raw),
        "n_examples": len(filtered),
        "n_london_ny": n_ln,
        "n_htf_active_teachers": n_htf,
        "n_zero_trade_days": n_zero,
        "dims_ok": dims_ok,
        "meta_rl_dim": META_RL_DIM,
        "day_stats_head": day_stats[:8],
        "source": "path_state_miss",
        "law": "A28_C003_CASE0037_htf_active",
        "monty_htf_blend": bool(monty_htf_blend),
        "require_htf_active": bool(require_htf_active),
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
    warmstart_path: Optional[Path | str] = None,
    n_passes: int = 2,
) -> MetaPolicy:
    """Base meta-train (or warmstart) + offline path-state teacher mix. Shadow only."""
    labs = filter_path_state_teachers(
        examples, max_examples=max(50, len(examples)), require_htf_active=True
    )
    if not labs:
        raise ValueError("no path-state teachers to train on")
    if warmstart_path is not None and Path(warmstart_path).exists():
        # Continue from existing champion/shadow — load unlocked for offline meta_update
        pol = MetaPolicy.load(Path(warmstart_path), freeze=False, require_serious=False)
        pol.unlock_for_meta_train()
        brain = pol.brain
        base_steps = 0
    else:
        # Base curriculum first (no opportunity_labels — those rebuild synthetic state)
        pol = train_goal_conditioned_meta_policy(
            seed=seed,
            n_steps=n_steps,
            freeze=False,
            opportunity_labels=None,
        )
        brain = pol.brain
        base_steps = int(n_steps)
    n_extra = max(1, int(max(base_steps, 500) * float(path_mix)))
    # first pass(es) all labels, then mix extras
    apply_path_state_teachers_to_brain(
        brain,
        labs,
        lr=0.02,
        seed=seed + 7,
        max_examples=len(labs),
        n_passes=int(n_passes),
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
