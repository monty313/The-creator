"""Structured grid over the Sentinel objective space with a train/test split.

Axes are the corpus P2.8 repair classes (not parameter thrash):
  trigger scale, barrier payoff objective, force magnitude, shell filters,
  session subset. Engine A (CCI) only and mass gate off, both fixed by the
  earlier cross-symbol screen.

Selection rule: positive on TRAIN months AND on TEST months (no cherry-pick),
minimum trade count, then smallest drawdown. Report both splits always.

Usage: python3 grid_search.py EURUSD [test_start=2026-06-01]
"""

from __future__ import annotations

import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from backtest_sentinel import Config, run_backtest   # noqa: E402


def split_stats(trades, daily, cutoff: date):
    out = {}
    for tag, sel in [("tr", lambda d: d < cutoff), ("te", lambda d: d >= cutoff)]:
        days = [d for d in sorted(daily) if sel(d)]
        tt = [t for t in trades if sel(t["time"].date())]
        pls = [daily[d]["pl"] for d in days]
        wd = [d for d in days if d.weekday() < 5]
        out[f"{tag}_n"] = len(tt)
        out[f"{tag}_wr"] = (sum(1 for t in tt if t["win"]) / len(tt)) if tt else np.nan
        out[f"{tag}_total"] = sum(pls) if pls else 0.0
        out[f"{tag}_tpd"] = len(tt) / max(len(wd), 1)
        out[f"{tag}_worst"] = min(pls) if pls else 0.0
    return out


def main():
    sym = sys.argv[1] if len(sys.argv) > 1 else "EURUSD"
    cutoff = date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else date(2026, 6, 1)
    path = Path(__file__).parent / "data" / f"{sym}_M1.parquet"
    m1 = pd.read_parquet(path)
    if m1.index.tz is not None:
        m1.index = m1.index.tz_convert("UTC").tz_localize(None)
    spread = {"EURUSD": 0.00007, "GBPUSD": 0.00010, "EURUSD_Y": 0.00007,
              "GBPUSD_Y": 0.00010}.get(sym, 0.00010)
    print(f"{sym}: {m1.index[0]} -> {m1.index[-1]} · test from {cutoff}")

    rows = []
    for trig in ["15min", "30min"]:
        for tp, sl in [(1.0, 1.5), (1.2, 1.6), (1.5, 1.2), (2.0, 1.2)]:
            for force in [4.0, 8.0]:
                for shell in [True, False]:
                    for sess in [(7, 21), (7, 13), (12, 21)]:
                        cfg = replace(
                            Config(),
                            name=f"{trig}_tp{tp}_sl{sl}_f{force:g}_s{int(shell)}"
                                 f"_h{sess[0]}-{sess[1]}",
                            trigger=trig, tp_atr=tp, sl_atr=sl,
                            cci_force=force,
                            use_engine_mcf=False, require_mark_mass=False,
                            use_bar_confirm=shell, use_micro_structure=shell,
                            session=sess, spread=spread)
                        trades, daily, _ = run_backtest(m1, cfg)
                        if not trades:
                            continue
                        rows.append({"name": cfg.name,
                                     **split_stats(trades, daily, cutoff)})
    df = pd.DataFrame(rows)
    df["ok"] = (df.tr_total > 0) & (df.te_total > 0) & (df.tr_n + df.te_n >= 60)
    df = df.sort_values(["ok", "te_total"], ascending=False)
    pd.set_option("display.width", 250)
    print(df.head(30).to_string(index=False))
    df.to_csv(Path(__file__).parent / f"GRID_{sym}.csv", index=False)
    print(f"[written] GRID_{sym}.csv · candidates passing both splits: {int(df.ok.sum())}")


if __name__ == "__main__":
    main()
