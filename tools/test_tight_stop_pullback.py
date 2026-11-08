"""Test the Martin Luk idea: pullback entries + tight stops (measured, lab only).

Source: TraderLion interview "+969% Return in 1 Year" (youtu.be/VKNEJA5r8zw).
Luk's actual claim (transcript): pullback entries at support confluence with
TIGHT price stops (~1-1.5%), fixed account risk per trade -> bigger size,
10-30R winners. His win rate is LOW (<25-30%) — tight stops compensate for
inaccuracy; the edge is asymmetric R, not "90% accurate pullbacks".

Our translation: stop_distance_pct is the price-stop width in the fill model
(r_mult = move/stop). Same typed risk%% per leg, tighter stop => more R per
favorable move, more wick-out stops. Sweep it on the SAME pinned 40d protocol
(champion frozen, no behavior change to production defaults) across:
  stops x {all entries, pullback-only entries}

Owner bar: hits > king hits (1) at breach 0 on this sensor.

Usage:
  python tools/test_tight_stop_pullback.py --days 40 --seed 42
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np

from evidence_court.meta_rl.edge import build_tf_cache
from evidence_court.meta_rl.forward_eval import DEFAULT_RISK_GRID, DEFAULT_TARGET_GRID
from evidence_court.meta_rl.goal_path import run_goal_path_day
from evidence_court.meta_rl.policy import load_or_train_champion
from evidence_court.meta_rl.price_io import (
    SYMBOL_FILES,
    bars_to_daily,
    load_m1_trailing_calendar_days,
)

OUT_DEFAULT = (
    _ROOT / "evidence_court" / "artifacts" / "reports" / "tight_stop_pullback_sweep.json"
)


def protocol_days(symbol: str, n_days: int, seed: int):
    p = SYMBOL_FILES.get(symbol)
    if p is None or not p.exists():
        raise SystemExit(f"no data for {symbol}")
    m1 = load_m1_trailing_calendar_days(p, n_days=400)
    all_dates = [d["date"] for d in bars_to_daily(m1)]
    warmup = 15
    window = all_dates[-(n_days + warmup):]
    dates = window[warmup:] if len(window) > warmup else window[1:]
    rng = np.random.default_rng(seed)
    pairs = [
        (float(rng.choice(DEFAULT_TARGET_GRID)), float(rng.choice(DEFAULT_RISK_GRID)))
        for _ in dates
    ]
    return m1, dates, pairs


def run_config(
    pol, m1, cache, dates, pairs, *, stop: float, pullback_only: bool, symbol: str
):
    hits = breach = 0
    pnls, n_tr, wins, losses, full_stops, r_mults = [], [], 0, 0, 0, []
    for date, (t, r) in zip(dates, pairs):
        fills, ledger, _meta = run_goal_path_day(
            pol,
            date=date,
            m1_by_symbol={symbol: m1},
            target_percent=t,
            max_daily_risk_percent=r,
            symbols=[symbol],
            stop_distance_pct=float(stop),
            pullback_only=bool(pullback_only),
            tf_cache_by_symbol={symbol: cache},
        )
        pnl = float(ledger.realized_pnl_percent)
        pnls.append(pnl)
        n_tr.append(len(fills))
        hits += int(pnl >= t - 1e-9)
        breach += int(max(-pnl, 0.0) > r + 1e-6)
        for f in fills:
            if f.pnl_percent > 0:
                wins += 1
            else:
                losses += 1
            if f.pnl_percent <= -0.95 * f.size_risk_percent:
                full_stops += 1
            if f.size_risk_percent > 0:
                r_mults.append(f.pnl_percent / f.size_risk_percent)
    total = wins + losses
    return {
        "stop_distance_pct": stop,
        "pullback_only": pullback_only,
        "hits": hits,
        "breach": breach,
        "mean_pnl": round(float(np.mean(pnls)), 4),
        "mean_trades": round(float(np.mean(n_tr)), 2),
        "n_fills": total,
        "fill_win_rate": round(wins / max(total, 1), 4),
        "full_stop_rate": round(full_stops / max(total, 1), 4),
        "mean_R_per_fill": round(float(np.mean(r_mults)), 3) if r_mults else 0.0,
        "best_day": round(float(np.max(pnls)), 3),
        "worst_day": round(float(np.min(pnls)), 3),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=40)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--symbol", type=str, default="XAUUSD")
    ap.add_argument("--stops", type=str, default="0.45,0.30,0.20,0.12")
    ap.add_argument("--out", type=str, default=str(OUT_DEFAULT))
    args = ap.parse_args(argv)

    stops = [float(s) for s in args.stops.split(",")]
    m1, dates, pairs = protocol_days(args.symbol, args.days, args.seed)
    cache = build_tf_cache(m1)
    pol = load_or_train_champion()
    pol.assert_frozen()

    rows = []
    for pb_only in (False, True):
        for stop in stops:
            row = run_config(
                pol, m1, cache, dates, pairs,
                stop=stop, pullback_only=pb_only, symbol=args.symbol,
            )
            rows.append(row)
            print(
                f"stop={stop:.2f} pb_only={str(pb_only):5s} | hits={row['hits']} "
                f"breach={row['breach']} mean_pnl={row['mean_pnl']:+.3f} "
                f"tr/day={row['mean_trades']:5.1f} win%={row['fill_win_rate']:.2%} "
                f"fullstop%={row['full_stop_rate']:.2%} meanR={row['mean_R_per_fill']:+.3f}",
                flush=True,
            )
    pol.assert_frozen()

    report = {
        "idea": "Martin Luk pullback + tight stop (youtu.be/VKNEJA5r8zw)",
        "protocol": f"forward{args.days}_random_seed{args.seed}_{args.symbol}",
        "window": f"{dates[0]}..{dates[-1]}",
        "fingerprint": pol.weight_fingerprint(),
        "baseline_stop": 0.45,
        "king_hits_baseline": 1,
        "rows": rows,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"WROTE {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
