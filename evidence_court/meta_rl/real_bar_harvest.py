"""CASE-0036 / C-003: real-bar Watch miss harvest for offline A13 curriculum.

Unlike CASE-0035 synthetic densify (F-024), labels come from production path
runs on real M1: Opportunity Watch curriculum_labels when the bot waited on
Mark PB/cont. Offline train only — never live force-pad.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .edge import build_tf_cache
from .goal_path import run_goal_path_day
from .policy import (
    FrozenMetaPolicy,
    load_or_train_champion,
    train_goal_conditioned_meta_policy,
)
from .price_io import SYMBOL_FILES, available_symbols, bars_to_daily, load_m1_trailing_calendar_days

ACTIONABLE = frozenset({"pullback_resume", "continuation"})
DEFAULT_HARVEST_OUT = Path(
    "evidence_court/artifacts/teachers/real_bar_opp_labels_case0036.json"
)
DEFAULT_SHADOW_OUT = Path(
    "evidence_court/artifacts/policies_lab/meta_policy_case0036_realbar.npz"
)


def filter_real_bar_a13_labels(
    labels: Sequence[Dict[str, Any]],
    *,
    max_labels: int = 250,
    require_actionable: bool = True,
) -> List[Dict[str, Any]]:
    """Mark topology gate: PB/cont teachers only; keep real asof metadata.

    London/NY labels keep their Watch weight; no chop/collapse teachers.
    """
    out: List[Dict[str, Any]] = []
    for lab in labels:
        if not isinstance(lab, dict):
            continue
        topo = str(lab.get("topology") or "")
        side = str(lab.get("teacher_act") or lab.get("side") or "")
        if require_actionable and topo not in ACTIONABLE:
            continue
        if side not in ("long", "short"):
            continue
        # Real-bar provenance flag (anti F-024 synthetic-only claim)
        row = dict(lab)
        row["teacher_act"] = side
        row["source"] = str(row.get("source") or "real_bar_watch")
        if "asof_date" not in row or not row["asof_date"]:
            continue  # must be dated from path
        out.append(row)
        if len(out) >= int(max_labels):
            break
    return out


def _dedupe_labels(labels: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out: List[Dict[str, Any]] = []
    for lab in labels:
        key = (
            str(lab.get("asof_date")),
            str(lab.get("asof_time")),
            str(lab.get("symbol")),
            str(lab.get("topology")),
            str(lab.get("teacher_act") or lab.get("side")),
            int(lab.get("set_id") or 0),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(lab)
    return out


def harvest_real_bar_opportunity_labels(
    *,
    n_days: int = 30,
    seed: int = 42,
    max_labels: int = 250,
    warmup_days: int = 10,
    policy: Optional[FrozenMetaPolicy] = None,
    symbols: Optional[Sequence[str]] = None,
    target_percent: float = 15.0,
    max_daily_risk_percent: float = 2.0,
) -> Dict[str, Any]:
    """Run production goal_path on real M1; collect Watch miss curriculum_labels.

    Offline only. Empty-skip preserved (Watch observes; does not force).
    Returns dict with labels + harvest meta for Court evidence.
    """
    syms = list(symbols) if symbols else [s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()]
    if not syms:
        return {
            "labels": [],
            "n_days": 0,
            "n_raw_labels": 0,
            "n_labels": 0,
            "error": "no_symbols",
            "source": "real_bar_watch",
        }

    pol = policy if policy is not None else load_or_train_champion(seed=seed, n_steps=2500)
    trail = max(int(n_days) + int(warmup_days) + 5, 40)
    daily_by_sym: Dict[str, List[dict]] = {}
    m1_by_sym: Dict[str, List[dict]] = {}
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
            "labels": [],
            "n_days": 0,
            "n_raw_labels": 0,
            "n_labels": 0,
            "error": "price_data_missing",
            "source": "real_bar_watch",
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
        # mild target/risk diversity so harvest spans goal context
        t = float(target_percent) if i % 3 else float(rng.choice([5.0, 15.0, 30.0, 50.0]))
        r = float(max_daily_risk_percent) if i % 2 else float(rng.choice([1.0, 2.0, 3.0]))
        hist = {sym: m1_by_sym[sym] for sym in m1_by_sym}
        fills, ledger, gmeta = run_goal_path_day(
            pol,
            date=date,
            m1_by_symbol=hist,
            target_percent=t,
            max_daily_risk_percent=r,
            symbols=list(m1_by_sym.keys()),
            tf_cache_by_symbol=tf_cache_by_symbol,
            brain_drives=True,
            watch_enabled=True,
        )
        labs = list(gmeta.get("curriculum_labels") or [])
        for lab in labs:
            if isinstance(lab, dict):
                lab = dict(lab)
                lab["source"] = "real_bar_watch"
                lab["harvest_day_target"] = t
                lab["harvest_day_risk"] = r
                lab["harvest_day_n_trades"] = len(fills)
                raw.append(lab)
        day_stats.append(
            {
                "date": date,
                "n_trades": len(fills),
                "n_labels": len(labs),
                "pnl": float(ledger.realized_pnl_percent),
                "target": t,
                "risk": r,
            }
        )

    deduped = _dedupe_labels(raw)
    filtered = filter_real_bar_a13_labels(deduped, max_labels=max_labels)
    n_ln = sum(1 for x in filtered if str(x.get("session_band")) == "london_ny")
    n_zero_days = sum(1 for d in day_stats if int(d["n_trades"]) == 0)
    return {
        "labels": filtered,
        "n_days": len(eval_dates),
        "n_raw_labels": len(raw),
        "n_deduped": len(deduped),
        "n_labels": len(filtered),
        "n_london_ny": n_ln,
        "n_zero_trade_days": n_zero_days,
        "day_stats_head": day_stats[:8],
        "source": "real_bar_watch",
        "law": "A28_C003_CASE0036",
        "policy_fingerprint": pol.weight_fingerprint(),
        "symbols": list(m1_by_sym.keys()),
        "window_start": eval_dates[0] if eval_dates else None,
        "window_end": eval_dates[-1] if eval_dates else None,
    }


def save_harvest(pack: Dict[str, Any], path: Path | str = DEFAULT_HARVEST_OUT) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(pack, indent=2), encoding="utf-8")
    return p


def train_real_bar_a13_policy(
    labels: Sequence[Dict[str, Any]],
    *,
    seed: int = 42,
    n_steps: int = 2500,
    opportunity_mix: float = 0.30,
    freeze: bool = True,
    save_path: Optional[Path | str] = None,
) -> Any:
    """Offline train shadow from real-bar labels. Does not touch PROVEN by default."""
    labs = filter_real_bar_a13_labels(labels, max_labels=max(50, len(labels)))
    if not labs:
        raise ValueError("no real-bar actionable labels to train on")
    pol = train_goal_conditioned_meta_policy(
        seed=seed,
        n_steps=n_steps,
        freeze=freeze,
        opportunity_labels=labs,
        opportunity_mix=opportunity_mix,
    )
    if save_path is not None:
        pol.save(Path(save_path))
    return pol
