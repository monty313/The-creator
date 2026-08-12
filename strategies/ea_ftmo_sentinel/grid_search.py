"""Structured grid over the Sentinel entry/exit objective space.

Not parameter thrash: the axes are the corpus P2.8 repair classes —
trigger scale (cost fraction), barrier objective (payoff ratio), engine mix,
mass gate. Selection requires month-split stability, not one aggregate number.

Usage: python3 grid_search.py EURUSD_Y
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from backtest_sentinel import Config, run_backtest   # noqa: E402


def evaluate(m1, cfg):
    trades, daily, diag = run_backtest(m1, cfg)
    days = sorted(daily)
    if not trades or not days:
        return None
    pls = [daily[d]["pl"] for d in days]
    n = len(trades)
    wins = sum(1 for t in trades if t["win"])
    bym = {}
    for d in days:
        bym.setdefault(str(d)[:7], []).append(daily[d]["pl"])
    months = {m: sum(v) for m, v in bym.items()}
    return {
        "trades": n,
        "wr": wins / n,
        "total": sum(pls),
        "mean_day": float(np.mean(pls)),
        "worst_day": min(pls),
        "tpd": n / max(sum(1 for d in days if daily[d]["trades"] > 0), 1),
        "pos_months": sum(1 for v in months.values() if v > 0),
        "n_months": len(months),
        "months": months,
    }


def main():
    sym = sys.argv[1] if len(sys.argv) > 1 else "EURUSD_Y"
    path = Path(__file__).parent / "data" / f"{sym}_M1.parquet"
    m1 = pd.read_parquet(path)
    if m1.index.tz is not None:
        m1.index = m1.index.tz_convert("UTC").tz_localize(None)
    spread = {"EURUSD": 0.00007, "GBPUSD": 0.00010, "EURUSD_Y": 0.00007,
              "GBPUSD_Y": 0.00010}.get(sym, 0.00010)

    rows = []
    for trig in ["5min", "15min", "30min"]:
        for tp, sl in [(0.7, 2.8), (1.0, 2.0), (1.2, 1.6), (1.5, 1.5), (2.0, 1.2)]:
            for eng in ["A", "B", "AB"]:
                for mass in [True, False]:
                    cfg = replace(
                        Config(), name=f"{trig}_tp{tp}_sl{sl}_{eng}_m{int(mass)}",
                        trigger=trig, tp_atr=tp, sl_atr=sl,
                        use_engine_cci=eng in ("A", "AB"),
                        use_engine_mcf=eng in ("B", "AB"),
                        require_mark_mass=mass, spread=spread)
                    r = evaluate(m1, cfg)
                    if r is None:
                        continue
                    rows.append({"name": cfg.name, **{k: v for k, v in r.items()
                                                      if k != "months"}})
    df = pd.DataFrame(rows).sort_values("total", ascending=False)
    pd.set_option("display.width", 200)
    print(df.head(25).to_string(index=False))
    print("\n-- bottom 5 --")
    print(df.tail(5).to_string(index=False))
    df.to_csv(Path(__file__).parent / f"GRID_{sym}.csv", index=False)


if __name__ == "__main__":
    main()
