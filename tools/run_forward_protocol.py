"""Pinned forward-test protocol runner (consistency = same protocol every run).

Runs the frozen champion over N chronological real-data days with a random
target×risk pair per day (seeded), XAU-only or multi-symbol, and writes the
full report JSON + a one-line scoreboard row.

Usage:
  python tools/run_forward_protocol.py --days 40 --seed 42 --symbols XAUUSD
  python tools/run_forward_protocol.py --days 100 --seed 42 --symbols XAUUSD,EURUSD,GBPUSD
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from evidence_court.meta_rl.forward_eval import run_forward_eval, save_report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=40)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--symbols", type=str, default="XAUUSD")
    ap.add_argument("--champion", type=str, default="", help="optional shadow .npz")
    ap.add_argument("--window-end", type=str, default="", help="pin last eval date YYYY-MM-DD")
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args(argv)

    syms = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    out = Path(args.out) if args.out else (
        _ROOT
        / "evidence_court"
        / "artifacts"
        / "reports"
        / f"forward{args.days}_seed{args.seed}_{'_'.join(syms)}.json"
    )

    report = run_forward_eval(
        n_days=args.days,
        seed=args.seed,
        symbols=syms,
        champion_path=Path(args.champion) if args.champion else None,
        window_end_date=args.window_end or None,
    )
    save_report(report, out)

    gc = report.metadata.get("goal_consistency") or {}
    hits = int(gc.get("total_hits", 0))
    days = [d for d in report.day_results]
    n_tr = [d.n_trades for d in days]
    mean_tr = sum(n_tr) / max(len(n_tr), 1)
    mean_pnl = sum(d.pnl_percent for d in days) / max(len(days), 1)
    a13 = sum(1 for n in n_tr if 8 <= n <= 400) / max(len(n_tr), 1)
    row = {
        "protocol": f"forward{args.days}_random_seed{args.seed}_{'_'.join(syms)}",
        "n_days": report.n_days,
        "hits": hits,
        "hit_rate": round(hits / max(report.n_days, 1), 4),
        "breach_count": report.breach_count,
        "no_retrain": report.no_retrain,
        "mean_pnl": round(mean_pnl, 4),
        "mean_trades_per_day": round(mean_tr, 2),
        "a13_frac": round(a13, 4),
        "n_zero_trade_days": sum(1 for n in n_tr if n == 0),
        "low_hit_rate": round(float(gc.get("low_hit_rate", 0.0)), 4),
        "fingerprint": report.metadata.get("policy_fingerprint"),
        "window": f"{report.metadata.get('window_start')}..{report.metadata.get('window_end')}",
        "promote_ready": report.promote_ready,
        "report": str(out),
    }
    print(json.dumps(row, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
