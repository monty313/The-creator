"""
Monte Carlo simulator for all strategy families in strategies/.

For each family:
  1) Build trade return series under the lab contract (2HTF+1LTF, 4 sets, PB+cont)
     with the accuracy filter shell + first-breath TP/SL (same as tweak batch default).
  2) Run bootstrap Monte Carlo (resample trades with replacement) + order-shuffle MC.
  3) Report distribution of terminal wealth, drawdowns, P(loss), percentiles.

Usage:
  python -m strategies.python_batch.run_monte_carlo
  python -m strategies.python_batch.run_monte_carlo --sims 2000 --seed 42
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from strategies.python_batch.accuracy_tweaks import apply_entry_tweaks  # noqa: E402
from strategies.python_batch.families import fam_dimension_jump, fam_mcflurry  # noqa: E402
from strategies.python_batch.inventory_1to1 import build_inventory  # noqa: E402
from strategies.python_batch.mtf import (  # noqa: E402
    OFFICIAL_SETS,
    apply_htf_gate,
    build_all_sets,
    load_mt5_csv,
)
from strategies.python_batch.profiles import entries_for_profile  # noqa: E402

try:
    import vectorbt as vbt
except ImportError as e:
    raise SystemExit(f"vectorbt required: {e}") from e

STRATEGIES = _ROOT / "strategies"
OUT_JSON = STRATEGIES / "MONTE_CARLO_RESULTS.json"
OUT_MD = STRATEGIES / "MONTE_CARLO_REPORT.md"
DEFAULT_DATA = Path(
    r"C:\Users\user\Downloads\_OTHER_PROJECTS\ATI_FTMO_project\gravity_engine\data\EURUSD_M1_export.csv"
)
ALT_DATA = Path(
    r"C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\02_PRICE_DATA\GBPUSD_M1_202101131952_202605270000.csv"
)

# Match accuracy-layer first-breath defaults (lab shell)
TP_STOP = 0.00025
SL_STOP = 0.00100
INIT_CASH = 10_000.0
FEES = 0.00002
SLIP = 0.00001
TAIL = 40_000
DEFAULT_SIMS = 1000


@dataclass
class MCResult:
    family_id: str
    title: str
    kind: str
    profile: str
    n_trades: int
    mean_trade_return: float
    # historical path (one chronological concat of set×mode books is approximate)
    hist_terminal_mult: float
    hist_max_dd: float
    # bootstrap MC
    mc_median_terminal: float
    mc_p05_terminal: float
    mc_p25_terminal: float
    mc_p75_terminal: float
    mc_p95_terminal: float
    mc_mean_terminal: float
    mc_prob_loss: float  # P(terminal < 1.0)
    mc_prob_ruin_20: float  # P(maxDD >= 20%) along path
    mc_median_max_dd: float
    mc_p95_max_dd: float
    # shuffle MC (order risk, no replacement)
    shuffle_median_terminal: float
    shuffle_p05_terminal: float
    shuffle_prob_loss: float
    notes: str = ""
    error: str = ""


def _collect_trade_returns(
    fn_or_profile,
    sets,
    *,
    is_callable: bool,
    profile: str = "",
) -> np.ndarray:
    """Pool trade *percentage* returns across all set×mode portfolios."""
    rets: List[float] = []
    for _sn, sb in sets.items():
        for mode in ("pullback", "continuation"):
            if is_callable:
                bull, bear, modes = fn_or_profile(sb)
                le, se = apply_htf_gate(bull, bear, *modes, mode)
            else:
                le, se = entries_for_profile(sb, profile, mode)
            le, se = apply_entry_tweaks(
                sb,
                le,
                se,
                use_session=True,
                use_strength=True,
                use_bar_confirm=True,
                use_structure=True,
            )
            le = le.reindex(sb.close.index).fillna(False).astype(bool)
            se = se.reindex(sb.close.index).fillna(False).astype(bool)
            if not (le.any() or se.any()):
                continue
            z = pd.Series(False, index=sb.close.index)
            freq = {"1m": "1min", "5m": "5min", "15m": "15min", "30m": "30min"}.get(
                sb.ltf, "15min"
            )
            pf = vbt.Portfolio.from_signals(
                close=sb.close,
                entries=le,
                exits=z,
                short_entries=se,
                short_exits=z,
                tp_stop=TP_STOP,
                sl_stop=SL_STOP,
                init_cash=INIT_CASH,
                fees=FEES,
                slippage=SLIP,
                freq=freq,
            )
            # trade returns as fractions (e.g. 0.001 = +0.1%)
            try:
                tr = pf.trades.returns
                if tr is None or len(tr) == 0:
                    continue
                arr = np.asarray(tr.values, dtype=float)
                arr = arr[np.isfinite(arr)]
                rets.extend(arr.tolist())
            except Exception:
                # fallback: reconstruct from pnl / entry value if available
                try:
                    pnl = np.asarray(pf.trades.pnl.values, dtype=float)
                    # approximate return vs fixed notional
                    approx = pnl / INIT_CASH
                    approx = approx[np.isfinite(approx)]
                    rets.extend(approx.tolist())
                except Exception:
                    continue
    return np.asarray(rets, dtype=float)


def _path_stats(trade_returns: np.ndarray) -> Tuple[float, float]:
    """Terminal wealth multiple and max drawdown of equity curve from trade returns."""
    if trade_returns.size == 0:
        return 1.0, 0.0
    equity = np.cumprod(1.0 + trade_returns)
    terminal = float(equity[-1])
    peak = np.maximum.accumulate(equity)
    dd = (peak - equity) / np.where(peak > 0, peak, 1.0)
    max_dd = float(np.max(dd)) if dd.size else 0.0
    return terminal, max_dd


def monte_carlo_bootstrap(
    trade_returns: np.ndarray,
    n_sims: int,
    rng: np.random.Generator,
) -> Dict[str, float]:
    n = trade_returns.size
    if n == 0:
        return {
            "median_terminal": 1.0,
            "p05": 1.0,
            "p25": 1.0,
            "p75": 1.0,
            "p95": 1.0,
            "mean_terminal": 1.0,
            "prob_loss": 0.0,
            "prob_ruin_20": 0.0,
            "median_max_dd": 0.0,
            "p95_max_dd": 0.0,
        }
    terminals = np.empty(n_sims, dtype=float)
    max_dds = np.empty(n_sims, dtype=float)
    for i in range(n_sims):
        sample = rng.choice(trade_returns, size=n, replace=True)
        term, mdd = _path_stats(sample)
        terminals[i] = term
        max_dds[i] = mdd
    return {
        "median_terminal": float(np.median(terminals)),
        "p05": float(np.percentile(terminals, 5)),
        "p25": float(np.percentile(terminals, 25)),
        "p75": float(np.percentile(terminals, 75)),
        "p95": float(np.percentile(terminals, 95)),
        "mean_terminal": float(np.mean(terminals)),
        "prob_loss": float(np.mean(terminals < 1.0)),
        "prob_ruin_20": float(np.mean(max_dds >= 0.20)),
        "median_max_dd": float(np.median(max_dds)),
        "p95_max_dd": float(np.percentile(max_dds, 95)),
    }


def monte_carlo_shuffle(
    trade_returns: np.ndarray,
    n_sims: int,
    rng: np.random.Generator,
) -> Dict[str, float]:
    """Order-risk MC: permute trade order without replacement."""
    n = trade_returns.size
    if n == 0:
        return {
            "median_terminal": 1.0,
            "p05": 1.0,
            "prob_loss": 0.0,
        }
    terminals = np.empty(n_sims, dtype=float)
    for i in range(n_sims):
        sample = trade_returns.copy()
        rng.shuffle(sample)
        term, _ = _path_stats(sample)
        terminals[i] = term
    return {
        "median_terminal": float(np.median(terminals)),
        "p05": float(np.percentile(terminals, 5)),
        "prob_loss": float(np.mean(terminals < 1.0)),
    }


def build_family_list() -> List[dict]:
    families = []
    for f in build_inventory():
        families.append(
            {
                "family_id": f.family_id,
                "title": f.title,
                "kind": f.kind,
                "profile": f.adapter_profile,
                "fn": None,
            }
        )
    families.append(
        {
            "family_id": "sauce__mcflurry_eddy_scalp",
            "title": "McFlurry Eddy H001",
            "kind": "sauce",
            "profile": "mcflurry",
            "fn": fam_mcflurry,
        }
    )
    families.append(
        {
            "family_id": "sauce__dimension_jump",
            "title": "Dimension Jump sauce",
            "kind": "sauce",
            "profile": "dimension_jump",
            "fn": fam_dimension_jump,
        }
    )
    return families


def run_one_family(spec: dict, sets, n_sims: int, rng: np.random.Generator) -> MCResult:
    fid = spec["family_id"]
    try:
        if spec["fn"] is not None:
            rets = _collect_trade_returns(spec["fn"], sets, is_callable=True)
        else:
            rets = _collect_trade_returns(
                None, sets, is_callable=False, profile=spec["profile"]
            )
        n = int(rets.size)
        if n == 0:
            return MCResult(
                family_id=fid,
                title=spec["title"],
                kind=spec["kind"],
                profile=spec["profile"],
                n_trades=0,
                mean_trade_return=0.0,
                hist_terminal_mult=1.0,
                hist_max_dd=0.0,
                mc_median_terminal=1.0,
                mc_p05_terminal=1.0,
                mc_p25_terminal=1.0,
                mc_p75_terminal=1.0,
                mc_p95_terminal=1.0,
                mc_mean_terminal=1.0,
                mc_prob_loss=0.0,
                mc_prob_ruin_20=0.0,
                mc_median_max_dd=0.0,
                mc_p95_max_dd=0.0,
                shuffle_median_terminal=1.0,
                shuffle_p05_terminal=1.0,
                shuffle_prob_loss=0.0,
                notes="no trades under MC entry shell",
            )
        hist_term, hist_dd = _path_stats(rets)
        boot = monte_carlo_bootstrap(rets, n_sims, rng)
        shuf = monte_carlo_shuffle(rets, min(n_sims, 500), rng)
        return MCResult(
            family_id=fid,
            title=spec["title"],
            kind=spec["kind"],
            profile=spec["profile"],
            n_trades=n,
            mean_trade_return=float(np.mean(rets)),
            hist_terminal_mult=hist_term,
            hist_max_dd=hist_dd,
            mc_median_terminal=boot["median_terminal"],
            mc_p05_terminal=boot["p05"],
            mc_p25_terminal=boot["p25"],
            mc_p75_terminal=boot["p75"],
            mc_p95_terminal=boot["p95"],
            mc_mean_terminal=boot["mean_terminal"],
            mc_prob_loss=boot["prob_loss"],
            mc_prob_ruin_20=boot["prob_ruin_20"],
            mc_median_max_dd=boot["median_max_dd"],
            mc_p95_max_dd=boot["p95_max_dd"],
            shuffle_median_terminal=shuf["median_terminal"],
            shuffle_p05_terminal=shuf["p05"],
            shuffle_prob_loss=shuf["prob_loss"],
            notes="bootstrap with replacement + order shuffle",
        )
    except Exception as e:
        return MCResult(
            family_id=fid,
            title=spec["title"],
            kind=spec["kind"],
            profile=spec["profile"],
            n_trades=0,
            mean_trade_return=0.0,
            hist_terminal_mult=1.0,
            hist_max_dd=0.0,
            mc_median_terminal=1.0,
            mc_p05_terminal=1.0,
            mc_p25_terminal=1.0,
            mc_p75_terminal=1.0,
            mc_p95_terminal=1.0,
            mc_mean_terminal=1.0,
            mc_prob_loss=0.0,
            mc_prob_ruin_20=0.0,
            mc_median_max_dd=0.0,
            mc_p95_max_dd=0.0,
            shuffle_median_terminal=1.0,
            shuffle_p05_terminal=1.0,
            shuffle_prob_loss=0.0,
            error=f"{type(e).__name__}: {e}",
        )


def write_report(results: List[MCResult], meta: dict) -> None:
    # rank by mc median terminal (descending), then lower prob_loss
    ranked = sorted(
        [r for r in results if not r.error],
        key=lambda r: (r.mc_median_terminal, -r.mc_prob_loss, r.n_trades),
        reverse=True,
    )
    lines = [
        "# Monte Carlo report — all strategies",
        "",
        "**Not Court law.** Bootstrap + shuffle MC on pooled trade returns.",
        "",
        "## Method",
        "",
        "1. For each family: generate trades on **4 MARK sets × pullback + continuation**",
        "   with accuracy shell (session, HTF strength, bar confirm, structure)",
        f"   and exits `tp_stop={TP_STOP}`, `sl_stop={SL_STOP}` (vectorbt).",
        "2. Pool trade returns (fractions) across set×mode books.",
        f"3. **Bootstrap MC:** {meta['n_sims']} paths, sample n trades **with replacement**.",
        "4. **Shuffle MC:** permute trade order (sequence risk), no replacement.",
        "5. Terminal = compounded wealth multiple from 1.0; max DD on each path.",
        "",
        f"- Window: {meta['window']}",
        f"- Data: `{meta['data_path']}`",
        f"- Families: {meta['n_families']}",
        f"- Sims: {meta['n_sims']} · seed: {meta['seed']}",
        f"- vectorbt: {meta['vectorbt']}",
        "",
        "## Ranking by bootstrap median terminal wealth",
        "",
        "| Rank | Family | Trades | Mean trade r | Hist term | MC med | MC p05 | MC p95 | P(loss) | P(DD≥20%) | Med DD |",
        "|-----:|--------|-------:|-------------:|----------:|-------:|-------:|-------:|--------:|----------:|-------:|",
    ]
    for i, r in enumerate(ranked, 1):
        lines.append(
            f"| {i} | `{r.family_id}` | {r.n_trades} | {r.mean_trade_return*100:.4f}% | "
            f"{r.hist_terminal_mult:.4f} | {r.mc_median_terminal:.4f} | {r.mc_p05_terminal:.4f} | "
            f"{r.mc_p95_terminal:.4f} | {r.mc_prob_loss*100:.1f}% | {r.mc_prob_ruin_20*100:.1f}% | "
            f"{r.mc_median_max_dd*100:.1f}% |"
        )

    lines += [
        "",
        "## Worst by P(loss) (bootstrap)",
        "",
        "| Family | Trades | P(loss) | MC med | MC p05 |",
        "|--------|-------:|--------:|-------:|-------:|",
    ]
    worst = sorted(ranked, key=lambda r: (-r.mc_prob_loss, r.mc_median_terminal))
    for r in worst[:20]:
        lines.append(
            f"| `{r.family_id}` | {r.n_trades} | {r.mc_prob_loss*100:.1f}% | "
            f"{r.mc_median_terminal:.4f} | {r.mc_p05_terminal:.4f} |"
        )

    lines += [
        "",
        "## Errors / empty",
        "",
    ]
    empty = [r for r in results if r.n_trades == 0 or r.error]
    if not empty:
        lines.append("- None")
    else:
        for r in empty:
            lines.append(f"- `{r.family_id}`: trades={r.n_trades} err={r.error or r.notes}")

    lines += [
        "",
        "## How to read",
        "",
        "- **MC med > 1**: more than half of bootstrap paths end above start.",
        "- **P(loss)**: fraction of paths with terminal wealth < 1.",
        "- **P(DD≥20%)**: fraction of paths whose max drawdown hits 20%+.",
        "- **Shuffle** (in JSON): sensitivity to trade *order* with same trades.",
        "- High historical WR with high P(loss) under bootstrap ⇒ edge is fragile / small-sample.",
        "",
        "Not production promote evidence alone — one symbol/window + fixed barriers.",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sims", type=int, default=DEFAULT_SIMS)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--tail", type=int, default=TAIL)
    args = ap.parse_args(argv)

    data = DEFAULT_DATA if DEFAULT_DATA.exists() else ALT_DATA
    if not data.exists():
        print("No data", file=sys.stderr)
        return 2

    print(f"Loading {data} tail={args.tail}")
    m1 = load_mt5_csv(data, tail_bars=args.tail)
    window = f"{m1.index[0]} → {m1.index[-1]} ({len(m1)} M1)"
    print("window", window)
    sets = build_all_sets(m1)
    for k, sb in sets.items():
        print(f"  {k}: {sb.ltf} n={len(sb.close)}")

    families = build_family_list()
    rng = np.random.default_rng(args.seed)
    results: List[MCResult] = []

    for i, spec in enumerate(families, 1):
        print(f"[{i}/{len(families)}] {spec['family_id']}")
        r = run_one_family(spec, sets, args.sims, rng)
        results.append(r)
        if r.error:
            print(f"  ERR {r.error}")
        else:
            print(
                f"  tr={r.n_trades} mc_med={r.mc_median_terminal:.4f} "
                f"p_loss={r.mc_prob_loss*100:.1f}% p05={r.mc_p05_terminal:.4f}"
            )

    meta = {
        "window": window,
        "data_path": str(data),
        "n_families": len(families),
        "n_sims": args.sims,
        "seed": args.seed,
        "tp_stop": TP_STOP,
        "sl_stop": SL_STOP,
        "sets": list(OFFICIAL_SETS.keys()),
        "modes": ["pullback", "continuation"],
        "vectorbt": getattr(vbt, "__version__", "?"),
    }
    payload = {
        "meta": meta,
        "results": [asdict(r) for r in results],
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    write_report(results, meta)
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_MD)

    ok = [r for r in results if r.n_trades > 0 and not r.error]
    if ok:
        best = max(ok, key=lambda r: r.mc_median_terminal)
        print(
            f"BEST mc_med: {best.family_id} med={best.mc_median_terminal:.4f} "
            f"p_loss={best.mc_prob_loss*100:.1f}% tr={best.n_trades}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
