"""Test McFlurry Eddy + Dimension Jump only (same 4-set PB/cont + vectorbt contract)."""
from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from strategies.python_batch.families import (  # noqa: E402
    FAMILY_META,
    fam_dimension_jump,
    fam_mcflurry,
)
from strategies.python_batch.mtf import (  # noqa: E402
    OFFICIAL_SETS,
    apply_htf_gate,
    build_all_sets,
    default_exits,
    load_mt5_csv,
)

try:
    import vectorbt as vbt
except ImportError as e:
    raise SystemExit(f"vectorbt required: {e}") from e

STRATEGIES = _ROOT / "strategies"
DEFAULT_DATA = Path(
    r"C:\Users\user\Downloads\_OTHER_PROJECTS\ATI_FTMO_project\gravity_engine\data\EURUSD_M1_export.csv"
)
ALT_DATA = Path(
    r"C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\02_PRICE_DATA\GBPUSD_M1_202101131952_202605270000.csv"
)
OUT_MD = STRATEGIES / "SAUCES_TEST_REPORT.md"
OUT_JSON = STRATEGIES / "SAUCES_TEST_REPORT.json"

HOLD = 12
CASH = 10_000.0
FEES = 0.00002
SLIP = 0.00001
TAIL = 45_000

SPECS = [
    ("mcflurry_eddy_scalp", fam_mcflurry),
    ("dimension_jump_sauce", fam_dimension_jump),
]


def _sf(x, d=0.0):
    try:
        if x is None:
            return d
        if isinstance(x, str) and "inf" in x.lower():
            return 99.0
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return 99.0 if (isinstance(v, float) and math.isinf(v) and v > 0) else d
        return v
    except Exception:
        return d


@dataclass
class Row:
    family_id: str
    set_name: str
    mode: str
    trades: int = 0
    total_return: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    sharpe: float = 0.0
    sortino: float = 0.0
    calmar: float = 0.0
    stats: Dict[str, Any] = field(default_factory=dict)
    error: str = ""


def run_one(fid, fn, sb, mode) -> Row:
    row = Row(family_id=fid, set_name=sb.name, mode=mode)
    try:
        bull, bear, modes = fn(sb)
        pb_l, pb_s, cont_l, cont_s = modes
        long_e, short_e = apply_htf_gate(bull, bear, pb_l, pb_s, cont_l, cont_s, mode)
        long_e = long_e.reindex(sb.close.index).fillna(False).astype(bool)
        short_e = short_e.reindex(sb.close.index).fillna(False).astype(bool)
        long_x, short_x = default_exits(sb.close, long_e, short_e, HOLD)
        if not (long_e.any() or short_e.any()):
            row.stats = {"Total Trades": 0, "_empty": True}
            return row
        freq = {"1m": "1min", "5m": "5min", "15m": "15min", "30m": "30min"}.get(sb.ltf, "15min")
        pf = vbt.Portfolio.from_signals(
            close=sb.close,
            entries=long_e,
            exits=long_x,
            short_entries=short_e,
            short_exits=short_x,
            init_cash=CASH,
            fees=FEES,
            slippage=SLIP,
            freq=freq,
        )
        st = pf.stats()
        stats = {}
        if hasattr(st, "items"):
            for k, v in st.items():
                try:
                    stats[str(k)] = _sf(v) if not isinstance(v, (int, np.integer)) else int(v)
                except Exception:
                    stats[str(k)] = str(v)
        row.stats = stats
        row.trades = int(stats.get("Total Trades", 0) or 0)
        row.total_return = _sf(stats.get("Total Return [%]", 0))
        row.max_drawdown = _sf(stats.get("Max Drawdown [%]", 0))
        row.win_rate = _sf(stats.get("Win Rate [%]", 0))
        row.profit_factor = _sf(stats.get("Profit Factor", 0))
        row.sharpe = _sf(stats.get("Sharpe Ratio", 0))
        row.sortino = _sf(stats.get("Sortino Ratio", 0))
        row.calmar = _sf(stats.get("Calmar Ratio", 0))
    except Exception as e:
        row.error = f"{type(e).__name__}: {e}"
        row.stats = {"error": row.error}
    return row


def agg(rows: List[Row]) -> dict:
    ok = [r for r in rows if not r.error]
    if not ok:
        return {"trades": 0, "score": -1e9, "n_runs": 0}

    def avg(a):
        return float(np.mean([getattr(r, a) for r in ok]))

    pf, ret, dd = avg("profit_factor"), avg("total_return"), avg("max_drawdown")
    trades = sum(r.trades for r in ok)
    score = 100 * pf + ret - 0.25 * abs(dd)
    if trades < 5:
        score -= 50
    return {
        "trades": trades,
        "total_return": ret,
        "max_drawdown": dd,
        "win_rate": avg("win_rate"),
        "profit_factor": pf,
        "sharpe": avg("sharpe"),
        "sortino": avg("sortino"),
        "calmar": avg("calmar"),
        "score": score,
        "n_runs": len(ok),
    }


def main() -> int:
    data = DEFAULT_DATA if DEFAULT_DATA.exists() else ALT_DATA
    print("data", data)
    m1 = load_mt5_csv(data, tail_bars=TAIL)
    window = f"{m1.index[0]} → {m1.index[-1]} ({len(m1)} M1)"
    print("window", window)
    sets = build_all_sets(m1)
    all_rows: List[Row] = []
    summary = []
    for fid, fn in SPECS:
        print("===", fid)
        rows = []
        for sn, sb in sets.items():
            for mode in ("pullback", "continuation"):
                row = run_one(fid, fn, sb, mode)
                rows.append(row)
                all_rows.append(row)
                print(f"  {sn} {mode}: tr={row.trades} ret={row.total_return:.3f} pf={row.profit_factor:.3f} err={row.error}")
        a = agg(rows)
        meta = FAMILY_META.get(fid, {})
        summary.append({"family_id": fid, "title": meta.get("title", fid), **a, "sources": meta.get("sources", [])})

    summary.sort(key=lambda x: x["score"], reverse=True)
    for i, s in enumerate(summary, 1):
        s["rank"] = i

    lines = [
        "# Sauces test report — McFlurry + Dimension Jump",
        "",
        "**Not Court law.** Same contract as folder batch: 2 HTF + 1 LTF, 4 sets, PB+cont, vectorbt.",
        "",
        f"- Data: `{data}`",
        f"- Window: {window}",
        f"- vectorbt: {getattr(vbt, '__version__', '?')}",
        f"- Sort: `score = 100*PF + avg_return% - 0.25*|maxDD%|`",
        "",
        "## Ranking",
        "",
        "| Rank | Strategy | Score | PF | Return% | MaxDD% | Win% | Trades |",
        "|-----:|----------|------:|---:|--------:|-------:|-----:|-------:|",
    ]
    for s in summary:
        lines.append(
            f"| {s['rank']} | `{s['family_id']}` | {s['score']:.2f} | {s['profit_factor']:.3f} | "
            f"{s['total_return']:.3f} | {s['max_drawdown']:.3f} | {s['win_rate']:.2f} | {s['trades']} |"
        )
    lines += ["", "## Per set × mode", ""]
    by = {}
    for r in all_rows:
        by.setdefault(r.family_id, []).append(r)
    for s in summary:
        fid = s["family_id"]
        lines += [f"### `{fid}` — {s['title']}", ""]
        lines.append(f"- Sources: {s.get('sources')}")
        lines.append(f"- Aggregate score: {s['score']:.4f}")
        lines += [
            "",
            "| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe |",
            "|-----|------|-------:|--------:|-------:|-----:|---:|-------:|",
        ]
        for r in sorted(by[fid], key=lambda x: (x.set_name, x.mode)):
            lines.append(
                f"| {r.set_name} | {r.mode} | {r.trades} | {r.total_return:.4f} | "
                f"{r.max_drawdown:.4f} | {r.win_rate:.2f} | {r.profit_factor:.3f} | {r.sharpe:.3f} |"
            )
        sample = next((x for x in by[fid] if x.stats and not x.stats.get("_empty") and not x.error), None)
        if sample:
            lines += ["", f"Sample full vectorbt stats (`{sample.set_name}` / `{sample.mode}`):", "", "```"]
            for k, v in sample.stats.items():
                lines.append(f"{k}: {v}")
            lines += ["```", ""]
        lines += [
            "#### RL teaching (not hard-code)",
            "",
            (
                "McFlurry: multi-TF RSI momentum line as **feel of acceleration**; eddy = load, zero-cross reclaim = fire under HTF M>0. "
                "Teach as skill labels, not fixed +1.5 threshold law."
                if "mcflurry" in fid
                else "Dimension Jump: CCI dimension vs BB-on-CCI as **momentum mass**; LTF CCI30 dip/reclaim under dual HTF CCI100 mass. "
                "Pair with McFlurry as dual-sauce state channels."
            ),
            "",
            "#### 10× better",
            "",
            (
                "10× McFlurry: session filter (London/NY), sweep M_htf threshold, ATR exits from H001, multi-asset, random-entry control."
                if "mcflurry" in fid
                else "10× Dimension Jump: require both CCI30 and CCI100 dimension alignment strength; concurrence with Mark RSI-BB release; no lone oscillator fires."
            ),
            "",
        ]

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "window": window,
                "data": str(data),
                "sets": list(OFFICIAL_SETS.keys()),
                "modes": ["pullback", "continuation"],
                "summary": summary,
                "rows": [asdict(r) for r in all_rows],
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    print("Wrote", OUT_MD)
    for s in summary:
        print(f"#{s['rank']} {s['family_id']} score={s['score']:.2f} pf={s['profit_factor']:.3f} ret={s['total_return']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
