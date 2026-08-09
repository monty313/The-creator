"""Side-by-side dual: champion with monty_htf_blend OFF vs ON.

Same weights, same days, same target×risk schedule.
Lab measure only — does not write champion.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .edge import build_tf_cache
from .goal_path import run_goal_path_day
from .policy import load_or_train_champion
from .price_io import SYMBOL_FILES, available_symbols, bars_to_daily, load_m1_trailing_calendar_days

DEFAULT_OUT = Path("evidence_court/artifacts/htf_blend_dual_compare.json")
DEFAULT_TARGETS = (5.0, 15.0, 30.0, 50.0, 70.0, 90.0)
DEFAULT_RISKS = (1.0, 2.0, 3.0)


def _a13_ok(n: int) -> bool:
    return 8 <= int(n) <= 400


def _summarize(days: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not days:
        return {"n_days": 0}
    n = len(days)
    hits = sum(1 for d in days if d["hit"])
    breaches = sum(1 for d in days if d["breach"])
    n_zero = sum(1 for d in days if d["n_trades"] == 0)
    n_partial = sum(1 for d in days if 1 <= d["n_trades"] <= 7)
    n_a13 = sum(1 for d in days if _a13_ok(d["n_trades"]))
    n_over = sum(1 for d in days if d["n_trades"] > 400)
    pnls = [float(d["pnl"]) for d in days]
    trades = [int(d["n_trades"]) for d in days]
    green = sum(1 for p in pnls if p > 0)
    # low-target hit rate (targets <= 15)
    low = [d for d in days if d["target"] <= 15.0 + 1e-9]
    low_hr = (sum(1 for d in low if d["hit"]) / len(low)) if low else float("nan")
    return {
        "n_days": n,
        "hits": hits,
        "hit_rate": hits / n,
        "low_hr": low_hr,
        "a13_frac": n_a13 / n,
        "n_zero": n_zero,
        "n_partial_1_7": n_partial,
        "n_a13_8_400": n_a13,
        "n_over_400": n_over,
        "mean_tr": float(np.mean(trades)),
        "median_tr": float(np.median(trades)),
        "mean_pnl": float(np.mean(pnls)),
        "green_days": green,
        "green_frac": green / n,
        "max_pnl": float(np.max(pnls)),
        "min_pnl": float(np.min(pnls)),
        "breach_count": breaches,
        "breach": breaches > 0,
        "total_trades": int(sum(trades)),
    }


def _delta(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """b - a for key metrics (blend_on minus blend_off)."""
    keys = [
        "hit_rate",
        "low_hr",
        "a13_frac",
        "n_zero",
        "mean_tr",
        "mean_pnl",
        "green_frac",
        "total_trades",
        "breach_count",
    ]
    out = {}
    for k in keys:
        va, vb = a.get(k), b.get(k)
        if va is None or vb is None:
            continue
        if va != va or vb != vb:  # nan
            out[k] = None
        else:
            out[k] = float(vb) - float(va)
    return out


def run_arm(
    *,
    pol: Any,
    eval_dates: Sequence[str],
    m1_by_sym: Dict[str, List[dict]],
    daily_maps: Dict[str, Dict[str, dict]],
    tf_cache_by_symbol: Dict[str, Dict[str, List[dict]]],
    syms: Sequence[str],
    schedule: Sequence[Tuple[float, float]],
    monty_htf_blend: bool,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for i, date in enumerate(eval_dates):
        t, r = schedule[i]
        hist = {s: m1_by_sym[s] for s in syms if s in m1_by_sym}
        if not any(date in daily_maps.get(s, {}) for s in syms):
            continue
        fills, ledger, gmeta = run_goal_path_day(
            pol,
            date=date,
            m1_by_symbol=hist,
            target_percent=float(t),
            max_daily_risk_percent=float(r),
            symbols=list(syms),
            tf_cache_by_symbol=tf_cache_by_symbol,
            brain_drives=True,
            watch_enabled=True,
            monty_htf_blend=bool(monty_htf_blend),
        )
        pnl = float(ledger.realized_pnl_percent)
        loss = max(-pnl, 0.0)
        worst = float(ledger.worst_case_daily_loss_percent())
        breach = loss > float(r) + 1e-6 or worst > float(r) + 1e-6
        rows.append(
            {
                "day": date,
                "target": float(t),
                "risk": float(r),
                "n_trades": len(fills),
                "pnl": pnl,
                "hit": bool(pnl >= float(t) - 1e-9),
                "breach": bool(breach),
                "n_pb": int(gmeta.get("n_pullback") or 0),
                "n_ct": int(gmeta.get("n_continuation") or 0),
                "htf_source": gmeta.get("htf_source"),
            }
        )
    return rows


def run_compare(
    *,
    n_days: int = 20,
    seed: int = 42,
    warmup_days: int = 12,
    symbols: Optional[Sequence[str]] = None,
    champion_path: Optional[Path] = None,
    out_path: Path | str = DEFAULT_OUT,
    fixed_target: Optional[float] = None,
    fixed_risk: Optional[float] = None,
) -> Dict[str, Any]:
    syms = list(symbols) if symbols else [
        s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()
    ]
    pol = load_or_train_champion(
        path=Path(champion_path) if champion_path else None,
        seed=seed,
        n_steps=2500,
    )
    pol.assert_frozen()

    trail = n_days + warmup_days + 5
    m1_by_sym: Dict[str, List[dict]] = {}
    daily_by_sym: Dict[str, List[dict]] = {}
    for sym in syms:
        path = SYMBOL_FILES.get(sym)
        if path is None or not path.exists():
            continue
        m1 = load_m1_trailing_calendar_days(path, n_days=trail)
        if not m1:
            continue
        m1_by_sym[sym] = m1
        daily_by_sym[sym] = bars_to_daily(m1)

    if not m1_by_sym:
        return {"error": "no_price_data", "symbols": syms}

    date_sets = [set(d["date"] for d in days) for days in daily_by_sym.values()]
    common = sorted(set.intersection(*date_sets)) if len(date_sets) > 1 else sorted(date_sets[0])
    need = n_days + warmup_days
    window = common[-need:] if len(common) >= need else common
    eval_dates = window[warmup_days:] if len(window) > warmup_days else window[1:]
    eval_dates = eval_dates[-n_days:]

    daily_maps = {sym: {d["date"]: d for d in days} for sym, days in daily_by_sym.items()}
    tf_cache_by_symbol = {sym: build_tf_cache(m1) for sym, m1 in m1_by_sym.items()}

    rng = np.random.default_rng(seed)
    schedule: List[Tuple[float, float]] = []
    for i in range(len(eval_dates)):
        if fixed_target is not None and fixed_risk is not None:
            schedule.append((float(fixed_target), float(fixed_risk)))
        else:
            schedule.append(
                (
                    float(rng.choice(DEFAULT_TARGETS)),
                    float(rng.choice(DEFAULT_RISKS)),
                )
            )

    off = run_arm(
        pol=pol,
        eval_dates=eval_dates,
        m1_by_sym=m1_by_sym,
        daily_maps=daily_maps,
        tf_cache_by_symbol=tf_cache_by_symbol,
        syms=list(m1_by_sym.keys()),
        schedule=schedule,
        monty_htf_blend=False,
    )
    on = run_arm(
        pol=pol,
        eval_dates=eval_dates,
        m1_by_sym=m1_by_sym,
        daily_maps=daily_maps,
        tf_cache_by_symbol=tf_cache_by_symbol,
        syms=list(m1_by_sym.keys()),
        schedule=schedule,
        monty_htf_blend=True,
    )

    sum_off = _summarize(off)
    sum_on = _summarize(on)
    delta = _delta(sum_off, sum_on)

    # Per-day agreement / trade delta
    by_day = []
    on_map = {d["day"]: d for d in on}
    for d0 in off:
        d1 = on_map.get(d0["day"])
        if not d1:
            continue
        by_day.append(
            {
                "day": d0["day"],
                "target": d0["target"],
                "risk": d0["risk"],
                "trades_off": d0["n_trades"],
                "trades_on": d1["n_trades"],
                "d_trades": d1["n_trades"] - d0["n_trades"],
                "pnl_off": d0["pnl"],
                "pnl_on": d1["pnl"],
                "d_pnl": d1["pnl"] - d0["pnl"],
                "hit_off": d0["hit"],
                "hit_on": d1["hit"],
            }
        )

    # Simple verdict
    better = []
    worse = []
    if delta.get("breach_count", 0) and delta["breach_count"] > 0:
        worse.append("more_breaches")
    if delta.get("hit_rate") is not None:
        if delta["hit_rate"] > 0.01:
            better.append("hit_rate")
        elif delta["hit_rate"] < -0.01:
            worse.append("hit_rate")
    if delta.get("a13_frac") is not None:
        if delta["a13_frac"] > 0.02:
            better.append("a13_frac")
        elif delta["a13_frac"] < -0.02:
            worse.append("a13_frac")
    if delta.get("mean_pnl") is not None:
        if delta["mean_pnl"] > 0.05:
            better.append("mean_pnl")
        elif delta["mean_pnl"] < -0.05:
            worse.append("mean_pnl")
    if delta.get("n_zero") is not None:
        if delta["n_zero"] < -0.5:
            better.append("fewer_silent_days")
        elif delta["n_zero"] > 0.5:
            worse.append("more_silent_days")

    if sum_on.get("breach"):
        verdict = "BLEND_WORSE_SAFETY"
    elif better and not worse:
        verdict = "BLEND_BETTER"
    elif worse and not better:
        verdict = "BLEND_WORSE"
    elif better and worse:
        verdict = "BLEND_MIXED"
    else:
        verdict = "BLEND_NEUTRAL"

    report = {
        "law": "lab_htf_blend_dual_compare",
        "note": "Same frozen champion; only monty_htf_blend flag differs. Not a PROMOTE.",
        "n_days": len(eval_dates),
        "eval_start": eval_dates[0] if eval_dates else None,
        "eval_end": eval_dates[-1] if eval_dates else None,
        "symbols": list(m1_by_sym.keys()),
        "seed": seed,
        "policy_fp": pol.weight_fingerprint(),
        "meta_train_steps": int(pol.meta_train_steps),
        "blend_off": sum_off,
        "blend_on": sum_on,
        "delta_on_minus_off": delta,
        "verdict": verdict,
        "better_axes": better,
        "worse_axes": worse,
        "day_head": by_day[:8],
        "day_all": by_day,
    }
    outp = Path(out_path)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report["out_path"] = str(outp)
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Compare monty_htf_blend off vs on")
    p.add_argument("--days", type=int, default=20)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out", type=str, default=str(DEFAULT_OUT))
    p.add_argument("--target", type=float, default=0.0, help="If >0 with --risk, fix pair")
    p.add_argument("--risk", type=float, default=0.0)
    p.add_argument("--champion", type=str, default="")
    args = p.parse_args(list(argv) if argv is not None else None)
    ft = float(args.target) if float(args.target) > 0 else None
    fr = float(args.risk) if float(args.risk) > 0 else None
    rep = run_compare(
        n_days=int(args.days),
        seed=int(args.seed),
        out_path=args.out,
        champion_path=Path(args.champion) if args.champion else None,
        fixed_target=ft,
        fixed_risk=fr,
    )
    print(
        json.dumps(
            {
                "verdict": rep.get("verdict"),
                "n_days": rep.get("n_days"),
                "blend_off": rep.get("blend_off"),
                "blend_on": rep.get("blend_on"),
                "delta_on_minus_off": rep.get("delta_on_minus_off"),
                "better_axes": rep.get("better_axes"),
                "worse_axes": rep.get("worse_axes"),
                "out": rep.get("out_path"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
