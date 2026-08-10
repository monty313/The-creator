"""
Entry point: test all strategy families under 2 HTF + 1 LTF, 4 official sets,
pullback + continuation, via vectorbt Portfolio.from_signals.

Usage (from repo root):
  python -m strategies.python_batch.run_strategy_batch
  python strategies/python_batch/run_strategy_batch.py
"""
from __future__ import annotations

import json
import math
import sys
import traceback
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

# allow both package and script execution
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[1]  # The Creator
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from strategies.python_batch import indicators as ind  # noqa: E402
from strategies.python_batch.families import (  # noqa: E402
    ALL_FAMILIES,
    FAMILY_META,
    entries_for_mode,
)
from strategies.python_batch.mtf import (  # noqa: E402
    OFFICIAL_SETS,
    build_all_sets,
    default_exits,
    load_mt5_csv,
)

try:
    import vectorbt as vbt
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"vectorbt required: {e}") from e

STRATEGIES = _ROOT / "strategies"
DEFAULT_DATA = Path(
    r"C:\Users\user\Downloads\_OTHER_PROJECTS\ATI_FTMO_project\gravity_engine\data\EURUSD_M1_export.csv"
)
ALT_DATA = Path(
    r"C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\02_PRICE_DATA\GBPUSD_M1_202101131952_202605270000.csv"
)
REPORT_MD = STRATEGIES / "STRATEGY_TEST_REPORT.md"
REPORT_JSON = STRATEGIES / "STRATEGY_TEST_REPORT.json"
RANKED_DIR = STRATEGIES / "ranked"
FAMILIES_JSON = STRATEGIES / "FAMILY_INVENTORY.json"

# Primary sort: profit factor desc, then total return desc, then max DD asc (less negative better)
HOLD_BARS = 12
INIT_CASH = 10_000.0
FEES = 0.00002  # ~0.2 pip relative on FX fraction
SLIPPAGE = 0.00001
TAIL_BARS = 45_000  # ~30 trading days of M1 — shared window for all ideas


@dataclass
class RunRow:
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
    expectancy: float = 0.0
    stats: Dict[str, Any] = field(default_factory=dict)
    error: str = ""


def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
            return default
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return default
        return v
    except Exception:
        return default


def portfolio_stats(
    close: pd.Series,
    long_e: pd.Series,
    short_e: pd.Series,
) -> Dict[str, Any]:
    long_x, short_x = default_exits(close, long_e, short_e, HOLD_BARS)
    # Combine: vectorbt supports long/short entries
    entries = long_e.astype(bool)
    exits = long_x.astype(bool)
    short_entries = short_e.astype(bool)
    short_exits = short_x.astype(bool)
    if not (entries.any() or short_entries.any()):
        return {
            "Total Return [%]": 0.0,
            "Max Drawdown [%]": 0.0,
            "Win Rate [%]": 0.0,
            "Profit Factor": 0.0,
            "Sharpe Ratio": 0.0,
            "Sortino Ratio": 0.0,
            "Calmar Ratio": 0.0,
            "Expectancy": 0.0,
            "Total Trades": 0,
            "_empty": True,
        }
    pf = vbt.Portfolio.from_signals(
        close=close,
        entries=entries,
        exits=exits,
        short_entries=short_entries,
        short_exits=short_exits,
        init_cash=INIT_CASH,
        fees=FEES,
        slippage=SLIPPAGE,
        freq="1min",  # overridden per set below if needed
    )
    st = pf.stats()
    # full stats as plain dict
    out: Dict[str, Any] = {}
    if isinstance(st, pd.Series):
        for k, v in st.items():
            if isinstance(v, (np.floating, float)):
                out[str(k)] = _safe_float(v)
            elif isinstance(v, (np.integer, int)):
                out[str(k)] = int(v)
            else:
                try:
                    out[str(k)] = _safe_float(v, default=None) if v is not None else None
                except Exception:
                    out[str(k)] = str(v)
    return out


def run_one(
    family_id: str, fam_fn, sb, mode: str, freq_label: str
) -> RunRow:
    row = RunRow(family_id=family_id, set_name=sb.name, mode=mode)
    try:
        long_e, short_e = entries_for_mode(sb, fam_fn, mode)
        # align
        long_e = long_e.reindex(sb.close.index).fillna(False).astype(bool)
        short_e = short_e.reindex(sb.close.index).fillna(False).astype(bool)
        # temporarily set freq on portfolio via close index
        close = sb.close.copy()
        long_x, short_x = default_exits(close, long_e, short_e, HOLD_BARS)
        if not (long_e.any() or short_e.any()):
            row.stats = {"Total Trades": 0, "_empty": True}
            return row
        # map LTF to pandas freq for vectorbt
        freq_map = {
            "1m": "1min",
            "5m": "5min",
            "15m": "15min",
            "30m": "30min",
        }
        freq = freq_map.get(sb.ltf, "15min")
        pf = vbt.Portfolio.from_signals(
            close=close,
            entries=long_e,
            exits=long_x,
            short_entries=short_e,
            short_exits=short_x,
            init_cash=INIT_CASH,
            fees=FEES,
            slippage=SLIPPAGE,
            freq=freq,
        )
        st = pf.stats()
        stats: Dict[str, Any] = {}
        if isinstance(st, pd.Series):
            for k, v in st.items():
                if isinstance(v, (np.floating, float, np.integer, int)):
                    stats[str(k)] = _safe_float(v) if not isinstance(v, (int, np.integer)) else int(v)
                else:
                    try:
                        stats[str(k)] = float(v)
                    except Exception:
                        stats[str(k)] = str(v) if v is not None else None
        row.stats = stats
        row.trades = int(stats.get("Total Trades", 0) or 0)
        row.total_return = _safe_float(stats.get("Total Return [%]", 0.0))
        row.max_drawdown = _safe_float(stats.get("Max Drawdown [%]", 0.0))
        row.win_rate = _safe_float(stats.get("Win Rate [%]", 0.0))
        pf_raw = stats.get("Profit Factor", 0.0)
        row.profit_factor = _safe_float(pf_raw, 0.0)
        if isinstance(pf_raw, str) and pf_raw.lower() == "inf":
            row.profit_factor = 99.0
        row.sharpe = _safe_float(stats.get("Sharpe Ratio", 0.0))
        row.sortino = _safe_float(stats.get("Sortino Ratio", 0.0))
        row.calmar = _safe_float(stats.get("Calmar Ratio", 0.0))
        row.expectancy = _safe_float(stats.get("Expectancy", stats.get("Avg Winning Trade [%]", 0.0)))
    except Exception as e:
        row.error = f"{type(e).__name__}: {e}"
        row.stats = {"error": row.error}
    return row


def aggregate_family(rows: List[RunRow]) -> Dict[str, Any]:
    ok = [r for r in rows if not r.error]
    if not ok:
        return {
            "trades": 0,
            "total_return": 0.0,
            "max_drawdown": 0.0,
            "win_rate": 0.0,
            "profit_factor": 0.0,
            "sharpe": 0.0,
            "sortino": 0.0,
            "calmar": 0.0,
            "score": -1e9,
            "n_runs": 0,
        }
    trades = sum(r.trades for r in ok)
    # equal-weight average across set×mode runs
    def avg(attr):
        return float(np.mean([getattr(r, attr) for r in ok]))

    pf = avg("profit_factor")
    ret = avg("total_return")
    dd = avg("max_drawdown")  # vectorbt: usually negative or positive % depending version
    # score: profit factor primary, then return, then less drawdown magnitude
    dd_pen = abs(dd)
    score = pf * 100.0 + ret - 0.25 * dd_pen
    # require some trades
    if trades < 5:
        score -= 50.0
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


def rl_teaching_blurb(fid: str, agg: Dict[str, Any], meta: dict) -> str:
    fid_l = fid.lower()
    fidelity = meta.get("fidelity", "")
    base = (
        f"Measured score={agg['score']:.2f}, PF={agg['profit_factor']:.3f}, "
        f"avg return%={agg['total_return']:.3f}, trades={agg['trades']} across "
        f"{agg['n_runs']} set×mode runs. Fidelity: {fidelity}. "
    )
    if "mark_rsi" in fid_l or "challenge" in fid_l:
        teach = (
            "High teaching value for the RL brain: labels map cleanly to wait_loaded vs fire_skill "
            "under HTF mass — use as **skill-id curriculum / concurrence filter**, not hard-coded entries. "
            "Reward shaping: bonus when policy action matches RSI-BB release under mass; penalty thrash without mass."
        )
    elif "truth_s1" in fid_l or "cci_gravity" in fid_l or "zero_line" in fid_l:
        teach = (
            "Useful **feel/tension** teacher: CCI vs shifted SMA encodes slingshot load. "
            "Feed as state features (cci_gap_fast/slow) + optional auxiliary policy head; "
            "do not freeze CCI thresholds as production if-rules."
        )
    elif "truth_s2" in fid_l or "gv015" in fid_l or "cool_bollinger" in fid_l:
        teach = (
            "Teaches **volatility tunnel / extreme trend** geometry. Good as sight/feel features "
            "(dist to BB10/BB100). Prefer soft labels for re-entry loops over fixed breakout bots."
        )
    elif "truth_s3" in fid_l or "ati_shifted" in fid_l or "donchian" in fid_l or "dual_thrust" in fid_l or "orb" in fid_l or "london" in fid_l:
        teach = (
            "Breakout/envelope language is a **regime sensor** (expansion vs mean-revert). "
            "Teach the brain when range is expanding; poor as sole act teacher on chop. "
            "Use for taste/hearing of structure change, not hard ORB entries."
        )
    elif "snap8" in fid_l or "sma_scalp" in fid_l or "ma_ribbon" in fid_l:
        teach = (
            "Micro-ribbon pullback is dense A13-friendly **timing texture**. "
            "Good L2L path-state features (ema_spread, rsi_reclaim). "
            "Implement as teachers of pullback geometry, not fixed EMA cross robots."
        )
    elif "rl_blackbox" in fid_l:
        teach = (
            "Original EAs are black-box learners; this run is a **proxy only**. "
            "Teaching value is the reminder that weights must come from meta-train (A14), "
            "not frozen MQL. Prefer Court meta-policy over re-importing these EAs as hard rules."
        )
    elif "public_" in fid_l or "macd" in fid_l or "moving_average" in fid_l or "bband_rsi" in fid_l:
        teach = (
            "Retail public baselines — useful as **negative curriculum / flea-jar contrast** "
            "(what not to hard-code) and as simple feature ablations. "
            "Low value as positive doctrine; OK for diversity in offline replay."
        )
    else:
        teach = (
            "Moderate teaching value as alternate geometry on the same PB/cont scaffold. "
            "Best use: extra state channels and sparse labels when concurrent with Mark timing."
        )
    return base + teach


def ten_x_blurb(fid: str, agg: Dict[str, Any]) -> str:
    tips = {
        "mark_rsi_bb_l2l": "10×: concurrence with Mark plans + multi-day skill pooling (load/release), never sole fire teacher; add London/NY session weights.",
        "truth_s1_cci_slingshot": "10×: score by CCI−SMA distance strength; only fire when slingshot tension releases with HTF both above; exit is brain job.",
        "truth_s2_bb_trend_reversion": "10×: separate entry vs re-entry tags; stop reloading when SMA50 loses BB100 upper; size by tunnel width.",
        "truth_s3_envelope_breakout": "10×: require multi-set agreement on clear; fade false breaks with LTF failure back inside envelope.",
        "truth_s4_rsi_tension_snap": "10×: dual RSI (2 & 20) BB geometry as state; snap only with HTF extreme velocity confirmed.",
        "cci_gravity_scalp": "10×: true gravity mass (dual HTF) + London session filter; kill zero-line thrash with min CCI travel.",
        "ftmo_bb_mtf_strategy4": "10×: replace RSI14/BB20 with Mark RSI5/BB-on-RSI; keep MTF only as force, not as five conflicting EAs.",
        "snap8_nested_pullback": "10×: map bias TF to set HTF not fixed M5; ATR exits as risk rails for RL, not fixed TP bots.",
        "rl_blackbox_proxy": "10×: discard MQL stubs; meta-train one policy with goal/risk context (A14) on honest path state.",
        "public_bband_rsi": "10×: only as mean-revert regime detector; invert or silence when HTF mass is strong trend.",
        "public_donchian": "10×: Donchian for regime expansion flag; entries still Mark PB/cont under mass.",
        "challenge_ea_stack": "10×: stack is too many fixed rules — distill to mass+feel features and let brain choose size/hold.",
    }
    return tips.get(
        fid,
        "10×: keep idea as feature/label teacher under official sets; add session prior, kill low-travel thrash, "
        "pair with risk envelope (breach0), never ship as sole hard-coded entry soup.",
    )


def write_report(
    symbol: str,
    data_path: str,
    window: str,
    rows: List[RunRow],
    ranking: List[Dict[str, Any]],
    vbt_version: str,
) -> str:
    lines: List[str] = []
    a = lines.append
    a("# Strategy batch test report (Mark format: 2 HTF + 1 LTF × 4 sets × PB+cont)")
    a("")
    a("**Not Court law. Not production hard-code.** Language re-expressed in Python and scored with vectorbt.")
    a("")
    a("## Run configuration")
    a("")
    a(f"| Field | Value |")
    a(f"|-------|-------|")
    a(f"| Symbol / store | `{symbol}` |")
    a(f"| Data source | `{data_path}` |")
    a(f"| Window | {window} |")
    a(f"| Official sets | `{', '.join(OFFICIAL_SETS.keys())}` |")
    a(f"| Modes | `pullback`, `continuation` |")
    a(f"| Hold (bars) | {HOLD_BARS} LTF bars time-exit + opposite signal |")
    a(f"| Init cash | {INIT_CASH} |")
    a(f"| Fees / slippage | {FEES} / {SLIPPAGE} |")
    a(f"| vectorbt | {vbt_version} |")
    a(f"| Primary sort key | `score = 100*PF + avg_return% - 0.25*|maxDD%|` (then trades sanity) |")
    a("")
    a("## Family collapses")
    a("")
    for fid, meta in FAMILY_META.items():
        cols = meta.get("collapses") or []
        if cols:
            a(f"- **{fid}** ← {', '.join(cols)}")
    a("")
    a("## Ranking (most accurate/profitable → least)")
    a("")
    a("| Rank | Family | Score | PF | Return% | MaxDD% | Win% | Trades | Sharpe |")
    a("|-----:|--------|------:|---:|--------:|-------:|-----:|-------:|-------:|")
    for i, r in enumerate(ranking, 1):
        a(
            f"| {i} | `{r['family_id']}` | {r['score']:.2f} | {r['profit_factor']:.3f} | "
            f"{r['total_return']:.3f} | {r['max_drawdown']:.3f} | {r['win_rate']:.2f} | "
            f"{r['trades']} | {r['sharpe']:.3f} |"
        )
    a("")
    a("## Per-family detail (vectorbt metrics + RL teaching + 10×)")
    a("")
    by_fam: Dict[str, List[RunRow]] = {}
    for row in rows:
        by_fam.setdefault(row.family_id, []).append(row)

    for r in ranking:
        fid = r["family_id"]
        meta = FAMILY_META.get(fid, {})
        a(f"### {r['rank']}. `{fid}` — {meta.get('title', fid)}")
        a("")
        a(f"- **Sources:** {', '.join(meta.get('sources') or [])}")
        a(f"- **Fidelity:** {meta.get('fidelity', 'n/a')}")
        a(f"- **Aggregate score:** {r['score']:.4f}")
        a("")
        a("#### Vectorbt aggregate (mean across 4 sets × 2 modes)")
        a("")
        a("| Metric | Value |")
        a("|--------|------:|")
        a(f"| Total Return [%] (avg) | {r['total_return']:.6f} |")
        a(f"| Max Drawdown [%] (avg) | {r['max_drawdown']:.6f} |")
        a(f"| Win Rate [%] (avg) | {r['win_rate']:.6f} |")
        a(f"| Profit Factor (avg) | {r['profit_factor']:.6f} |")
        a(f"| Sharpe (avg) | {r['sharpe']:.6f} |")
        a(f"| Sortino (avg) | {r['sortino']:.6f} |")
        a(f"| Calmar (avg) | {r['calmar']:.6f} |")
        a(f"| Total Trades (sum) | {r['trades']} |")
        a(f"| Runs | {r['n_runs']} |")
        a("")
        a("#### Per set × mode (vectorbt key fields)")
        a("")
        a("| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |")
        a("|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|")
        for row in sorted(by_fam.get(fid, []), key=lambda x: (x.set_name, x.mode)):
            a(
                f"| {row.set_name} | {row.mode} | {row.trades} | {row.total_return:.4f} | "
                f"{row.max_drawdown:.4f} | {row.win_rate:.2f} | {row.profit_factor:.3f} | "
                f"{row.sharpe:.3f} | {row.error[:40] if row.error else ''} |"
            )
        a("")
        # dump one full stats object sample (first non-empty)
        sample = next((x for x in by_fam.get(fid, []) if x.stats and not x.stats.get("_empty") and not x.error), None)
        if sample:
            a(f"#### Sample full vectorbt stats (`{sample.set_name}` / `{sample.mode}`)")
            a("")
            a("```")
            for k, v in sample.stats.items():
                a(f"{k}: {v}")
            a("```")
            a("")
        a("#### RL teaching value (not hard-coded instructions)")
        a("")
        a(rl_teaching_blurb(fid, r, meta))
        a("")
        a("#### 10× better")
        a("")
        a(ten_x_blurb(fid, r))
        a("")
    a("## Method notes")
    a("")
    a("- HTF bars are **shift(1)+ffill** onto LTF so LTF only sees last completed HTF bar.")
    a("- All families forced into **pullback** and **continuation** modes under dual-HTF force.")
    a("- Exits: fixed hold in LTF bars + opposite entry (satisficing; not each EA's native exit).")
    a("- Accuracy vs profitability: single **score** key used for reorder (see config table).")
    a("")
    text = "\n".join(lines)
    REPORT_MD.write_text(text, encoding="utf-8")
    return text


def reorganize_ranked(ranking: List[Dict[str, Any]]) -> None:
    RANKED_DIR.mkdir(parents=True, exist_ok=True)
    # clear old rank_* folders
    for p in RANKED_DIR.iterdir():
        if p.is_dir() and p.name[0:2].isdigit():
            # leave content as stubs
            pass
    index_lines = [
        "# Ranked strategy families (best → worst)",
        "",
        "Generated by `strategies.python_batch.run_strategy_batch`.",
        "Sort key: score = 100*PF + avg_return% − 0.25*|maxDD%|.",
        "",
        "| Rank | Family | Score | Report anchor |",
        "|-----:|--------|------:|---------------|",
    ]
    for i, r in enumerate(ranking, 1):
        fid = r["family_id"]
        folder = RANKED_DIR / f"{i:02d}_{fid}"
        folder.mkdir(parents=True, exist_ok=True)
        meta = FAMILY_META.get(fid, {})
        readme = (
            f"# Rank {i}: `{fid}`\n\n"
            f"**Title:** {meta.get('title', fid)}\n\n"
            f"**Score:** {r['score']:.4f}\n\n"
            f"**PF / Return% / MaxDD% / Trades:** "
            f"{r['profit_factor']:.3f} / {r['total_return']:.3f} / {r['max_drawdown']:.3f} / {r['trades']}\n\n"
            f"**Sources:**\n"
            + "\n".join(f"- {s}" for s in (meta.get("sources") or []))
            + f"\n\n**Collapses:** {', '.join(meta.get('collapses') or ['—'])}\n\n"
            f"**Fidelity:** {meta.get('fidelity', 'n/a')}\n\n"
            f"See full metrics: [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)\n"
        )
        (folder / "README.md").write_text(readme, encoding="utf-8")
        index_lines.append(
            f"| {i} | `{fid}` | {r['score']:.2f} | [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md) |"
        )
    (RANKED_DIR / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    # root pointer
    (STRATEGIES / "RANKED.md").write_text(
        "# Strategies reorganized by measured score\n\n"
        "See **[ranked/INDEX.md](ranked/INDEX.md)** (best → worst).\n\n"
        "Full metrics: **[STRATEGY_TEST_REPORT.md](STRATEGY_TEST_REPORT.md)**.\n",
        encoding="utf-8",
    )


def write_inventory() -> None:
    inv = []
    for fid, fn in ALL_FAMILIES:
        meta = FAMILY_META[fid]
        inv.append({"family_id": fid, **meta})
    FAMILIES_JSON.write_text(json.dumps(inv, indent=2), encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    data_path = DEFAULT_DATA if DEFAULT_DATA.exists() else ALT_DATA
    if not data_path.exists():
        print("No OHLCV data found", file=sys.stderr)
        return 2
    print(f"Loading {data_path} tail={TAIL_BARS} ...")
    m1 = load_mt5_csv(data_path, tail_bars=TAIL_BARS)
    symbol = data_path.stem.split("_")[0]
    window = f"{m1.index[0]} → {m1.index[-1]} ({len(m1)} M1 bars)"
    print(f"Window {window}")
    print("Building 4 official sets ...")
    sets = build_all_sets(m1)
    for name, sb in sets.items():
        print(f"  {name}: LTF={sb.ltf} bars={len(sb.close)}")

    write_inventory()
    all_rows: List[RunRow] = []
    for fid, fn in ALL_FAMILIES:
        print(f"=== {fid} ===")
        for set_name, sb in sets.items():
            for mode in ("pullback", "continuation"):
                row = run_one(fid, fn, sb, mode, sb.ltf)
                all_rows.append(row)
                status = row.error or f"tr={row.trades} ret={row.total_return:.3f} pf={row.profit_factor:.3f}"
                print(f"  {set_name} {mode}: {status}")

    # aggregate + rank
    ranking = []
    for fid, _ in ALL_FAMILIES:
        fam_rows = [r for r in all_rows if r.family_id == fid]
        agg = aggregate_family(fam_rows)
        ranking.append({"family_id": fid, **agg})
    ranking.sort(key=lambda r: (r["score"], r["profit_factor"], r["total_return"]), reverse=True)
    for i, r in enumerate(ranking, 1):
        r["rank"] = i

    vbt_version = getattr(vbt, "__version__", "unknown")
    write_report(symbol, str(data_path), window, all_rows, ranking, vbt_version)
    reorganize_ranked(ranking)

    payload = {
        "symbol": symbol,
        "data_path": str(data_path),
        "window": window,
        "vectorbt": vbt_version,
        "sets": list(OFFICIAL_SETS.keys()),
        "modes": ["pullback", "continuation"],
        "ranking": ranking,
        "rows": [asdict(r) for r in all_rows],
    }
    REPORT_JSON.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {REPORT_MD}")
    print(f"Wrote {REPORT_JSON}")
    print(f"Wrote {RANKED_DIR / 'INDEX.md'}")
    print("TOP 5:")
    for r in ranking[:5]:
        print(f"  #{r['rank']} {r['family_id']} score={r['score']:.2f} pf={r['profit_factor']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
