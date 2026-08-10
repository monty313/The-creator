"""
1:1 batch: every MT name + every strategy note as its own family (no collapses).

Same contract as prior batch: 2 HTF + 1 LTF, 4 official sets, pullback+continuation,
vectorbt Portfolio.from_signals.

Usage:
  python -m strategies.python_batch.run_strategy_batch_1to1
"""
from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from strategies.python_batch.inventory_1to1 import (  # noqa: E402
    FamilySpec,
    build_inventory,
    inventory_counts,
    to_jsonable,
)
from strategies.python_batch.mtf import (  # noqa: E402
    OFFICIAL_SETS,
    build_all_sets,
    default_exits,
    load_mt5_csv,
)
from strategies.python_batch.profiles import entries_for_profile  # noqa: E402

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

INVENTORY_JSON = STRATEGIES / "FAMILY_INVENTORY_1TO1.json"
REPORT_MD = STRATEGIES / "STRATEGY_TEST_REPORT.md"
REPORT_JSON = STRATEGIES / "STRATEGY_TEST_REPORT.json"
RANKED_DIR = STRATEGIES / "ranked"

HOLD_BARS = 12
INIT_CASH = 10_000.0
FEES = 0.00002
SLIPPAGE = 0.00001
TAIL_BARS = 40_000  # slightly leaner for ~120 families


@dataclass
class RunRow:
    family_id: str
    title: str
    kind: str
    profile: str
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


def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        if x is None:
            return default
        if isinstance(x, str) and x.lower() in {"inf", "+inf", "infinity"}:
            return 99.0
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return default if not math.isinf(v) else (99.0 if v > 0 else default)
        return v
    except Exception:
        return default


def run_one(spec: FamilySpec, sb, mode: str) -> RunRow:
    row = RunRow(
        family_id=spec.family_id,
        title=spec.title,
        kind=spec.kind,
        profile=spec.adapter_profile,
        set_name=sb.name,
        mode=mode,
    )
    try:
        long_e, short_e = entries_for_profile(sb, spec.adapter_profile, mode)
        long_e = long_e.reindex(sb.close.index).fillna(False).astype(bool)
        short_e = short_e.reindex(sb.close.index).fillna(False).astype(bool)
        long_x, short_x = default_exits(sb.close, long_e, short_e, HOLD_BARS)
        if not (long_e.any() or short_e.any()):
            row.stats = {"Total Trades": 0, "_empty": True}
            return row
        freq_map = {"1m": "1min", "5m": "5min", "15m": "15min", "30m": "30min"}
        freq = freq_map.get(sb.ltf, "15min")
        pf = vbt.Portfolio.from_signals(
            close=sb.close,
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
                if isinstance(v, (np.floating, float)):
                    stats[str(k)] = _safe_float(v)
                elif isinstance(v, (np.integer, int)):
                    stats[str(k)] = int(v)
                else:
                    try:
                        stats[str(k)] = _safe_float(v)
                    except Exception:
                        stats[str(k)] = str(v) if v is not None else None
        row.stats = stats
        row.trades = int(stats.get("Total Trades", 0) or 0)
        row.total_return = _safe_float(stats.get("Total Return [%]", 0.0))
        row.max_drawdown = _safe_float(stats.get("Max Drawdown [%]", 0.0))
        row.win_rate = _safe_float(stats.get("Win Rate [%]", 0.0))
        row.profit_factor = _safe_float(stats.get("Profit Factor", 0.0))
        row.sharpe = _safe_float(stats.get("Sharpe Ratio", 0.0))
        row.sortino = _safe_float(stats.get("Sortino Ratio", 0.0))
        row.calmar = _safe_float(stats.get("Calmar Ratio", 0.0))
    except Exception as e:
        row.error = f"{type(e).__name__}: {e}"
        row.stats = {"error": row.error}
    return row


def aggregate(rows: List[RunRow]) -> Dict[str, Any]:
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

    def avg(attr: str) -> float:
        return float(np.mean([getattr(r, attr) for r in ok]))

    trades = sum(r.trades for r in ok)
    pf, ret, dd = avg("profit_factor"), avg("total_return"), avg("max_drawdown")
    score = pf * 100.0 + ret - 0.25 * abs(dd)
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


def rl_blurb(spec: FamilySpec, agg: Dict[str, Any]) -> str:
    base = (
        f"Measured score={agg['score']:.2f}, PF={agg['profit_factor']:.3f}, "
        f"avg return%={agg['total_return']:.3f}, trades={agg['trades']} over "
        f"{agg['n_runs']} set×mode runs. Fidelity={spec.fidelity}; profile={spec.adapter_profile}. "
    )
    p = spec.adapter_profile
    if p == "mark_rsi_bb":
        t = (
            "Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, "
            "not hard-coded entries."
        )
    elif p.startswith("truth_"):
        t = (
            "Truth-line geometry (CCI/BB/envelope/RSI snap) is good state/label material for L2L; "
            "do not freeze thresholds as production law."
        )
    elif p in {"cci_gravity", "jordan", "kinetic"}:
        t = "CCI/momentum feel features for the brain; optional aux labels, not sole decider."
    elif p == "rl_proxy":
        t = (
            "Black-box EA name only — teaching value is A14 meta-train reminder; "
            "do not re-import MQL as hard rules."
        )
    elif p in {"orb", "dual_thrust", "donchian", "supertrend"}:
        t = "Regime/expansion sensor value; weak as sole act teacher on chop."
    else:
        t = (
            "Use as alternate geometry features on the shared PB/cont scaffold; "
            "prefer soft teaching labels over shipping if-rules."
        )
    return base + t


def tenx_blurb(spec: FamilySpec) -> str:
    return (
        f"10× for `{spec.title}`: keep as **separate** teaching channel named by this source; "
        f"add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), "
        f"and train the meta-policy on path state rather than freezing profile=`{spec.adapter_profile}` rules."
    )


def write_report(
    symbol: str,
    data_path: str,
    window: str,
    specs: List[FamilySpec],
    rows: List[RunRow],
    ranking: List[Dict[str, Any]],
    vbt_version: str,
    counts: dict,
) -> None:
    lines: List[str] = []
    a = lines.append
    a("# Strategy batch test report — **1:1 no-collapse** (every MT name + every note)")
    a("")
    a("**Not Court law.** Each MT index name and each strategy note is its **own family** (no merges).")
    a("")
    a("## Run configuration")
    a("")
    a("| Field | Value |")
    a("|-------|-------|")
    a(f"| Symbol | `{symbol}` |")
    a(f"| Data | `{data_path}` |")
    a(f"| Window | {window} |")
    a(f"| MT names | {counts['mt_names']} |")
    a(f"| Note files | {counts['note_files']} |")
    a(f"| Total families (1:1) | {counts['total_families']} |")
    a(f"| Collapse entries | {counts['total_collapse_entries']} (must be 0) |")
    a(f"| Sets | `{', '.join(OFFICIAL_SETS.keys())}` |")
    a("| Modes | `pullback`, `continuation` |")
    a(f"| Hold bars | {HOLD_BARS} |")
    a(f"| vectorbt | {vbt_version} |")
    a("| Primary sort | `score = 100*PF + avg_return% - 0.25*|maxDD%|` |")
    a("")
    a("## Ranking (most accurate/profitable → least)")
    a("")
    a("| Rank | Family id | Title | Kind | Score | PF | Return% | MaxDD% | Win% | Trades |")
    a("|-----:|-----------|-------|------|------:|---:|--------:|-------:|-----:|-------:|")
    for r in ranking:
        a(
            f"| {r['rank']} | `{r['family_id']}` | {r['title'][:40]} | {r['kind']} | "
            f"{r['score']:.2f} | {r['profit_factor']:.3f} | {r['total_return']:.3f} | "
            f"{r['max_drawdown']:.3f} | {r['win_rate']:.2f} | {r['trades']} |"
        )
    a("")
    a("## Per-family detail")
    a("")
    by_fam: Dict[str, List[RunRow]] = {}
    for row in rows:
        by_fam.setdefault(row.family_id, []).append(row)
    spec_by = {s.family_id: s for s in specs}

    for r in ranking:
        fid = r["family_id"]
        spec = spec_by[fid]
        a(f"### {r['rank']}. `{fid}`")
        a("")
        a(f"- **Title:** {spec.title}")
        a(f"- **Kind:** {spec.kind}")
        a(f"- **Source:** `{spec.source}`")
        a(f"- **Adapter profile (logic only; family not collapsed):** `{spec.adapter_profile}`")
        a(f"- **Fidelity:** {spec.fidelity}")
        a(f"- **Collapses:** `{spec.collapses}` (empty)")
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
        a("#### Per set × mode")
        a("")
        a("| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |")
        a("|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|")
        for row in sorted(by_fam.get(fid, []), key=lambda x: (x.set_name, x.mode)):
            a(
                f"| {row.set_name} | {row.mode} | {row.trades} | {row.total_return:.4f} | "
                f"{row.max_drawdown:.4f} | {row.win_rate:.2f} | {row.profit_factor:.3f} | "
                f"{row.sharpe:.3f} | {(row.error or '')[:50]} |"
            )
        a("")
        sample = next(
            (x for x in by_fam.get(fid, []) if x.stats and not x.stats.get("_empty") and not x.error),
            None,
        )
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
        a(rl_blurb(spec, r))
        a("")
        a("#### 10× better")
        a("")
        a(tenx_blurb(spec))
        a("")

    a("## Method notes")
    a("")
    a("- **No collapses:** inventory forbids merging multiple MT names or notes into one family.")
    a("- Adapter *profiles* may be shared for thin language; each **family_id** still runs and ranks alone.")
    a("- HTF: completed bar only (shift+1 ffill). Exits: hold + opposite signal.")
    a("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def reorganize(ranking: List[Dict[str, Any]], specs: List[FamilySpec]) -> None:
    # wipe old ranked children
    if RANKED_DIR.exists():
        for p in RANKED_DIR.iterdir():
            if p.is_dir():
                for f in p.rglob("*"):
                    if f.is_file():
                        f.unlink()
                # remove nested empties
                for sub in sorted(p.rglob("*"), reverse=True):
                    if sub.is_dir():
                        try:
                            sub.rmdir()
                        except OSError:
                            pass
                try:
                    p.rmdir()
                except OSError:
                    pass
            elif p.name != "INDEX.md":
                p.unlink()
    RANKED_DIR.mkdir(parents=True, exist_ok=True)
    spec_by = {s.family_id: s for s in specs}
    idx = [
        "# Ranked strategy families — **1:1 no-collapse** (best → worst)",
        "",
        "Generated by `strategies.python_batch.run_strategy_batch_1to1`.",
        "",
        "| Rank | Family id | Title | Score |",
        "|-----:|-----------|-------|------:|",
    ]
    for r in ranking:
        fid = r["family_id"]
        # folder names limited length
        folder = RANKED_DIR / f"{r['rank']:03d}_{fid[:80]}"
        folder.mkdir(parents=True, exist_ok=True)
        spec = spec_by[fid]
        (folder / "README.md").write_text(
            f"# Rank {r['rank']}: `{fid}`\n\n"
            f"**Title:** {spec.title}\n\n"
            f"**Kind:** {spec.kind}\n\n"
            f"**Source:** `{spec.source}`\n\n"
            f"**Score:** {r['score']:.4f}\n\n"
            f"**PF / Return% / MaxDD% / Trades:** "
            f"{r['profit_factor']:.3f} / {r['total_return']:.3f} / "
            f"{r['max_drawdown']:.3f} / {r['trades']}\n\n"
            f"**Collapses:** []\n\n"
            f"See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)\n",
            encoding="utf-8",
        )
        idx.append(
            f"| {r['rank']} | `{fid}` | {spec.title[:50]} | {r['score']:.2f} |"
        )
    (RANKED_DIR / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    (STRATEGIES / "RANKED.md").write_text(
        "# Strategies ranked 1:1 (no collapse)\n\n"
        "See **[ranked/INDEX.md](ranked/INDEX.md)** and "
        "**[STRATEGY_TEST_REPORT.md](STRATEGY_TEST_REPORT.md)**.\n",
        encoding="utf-8",
    )


def main(argv: Optional[List[str]] = None) -> int:
    specs = build_inventory()
    counts = inventory_counts(specs)
    assert counts["total_collapse_entries"] == 0, counts
    assert counts["total_families"] == counts["mt_names"] + counts["note_files"], counts
    assert counts["mt_names"] == counts["mt_index_parsed"], counts
    assert counts["note_files"] == counts["note_files_listed"], counts

    INVENTORY_JSON.write_text(
        json.dumps({"counts": counts, "families": to_jsonable(specs)}, indent=2),
        encoding="utf-8",
    )
    print("Inventory:", counts)

    data_path = DEFAULT_DATA if DEFAULT_DATA.exists() else ALT_DATA
    if not data_path.exists():
        print("No OHLCV", file=sys.stderr)
        return 2
    print(f"Loading {data_path} tail={TAIL_BARS}")
    m1 = load_mt5_csv(data_path, tail_bars=TAIL_BARS)
    symbol = data_path.stem.split("_")[0]
    window = f"{m1.index[0]} → {m1.index[-1]} ({len(m1)} M1 bars)"
    print("Window", window)
    sets = build_all_sets(m1)
    for name, sb in sets.items():
        print(f"  {name}: LTF={sb.ltf} n={len(sb.close)}")

    all_rows: List[RunRow] = []
    missing: List[str] = []
    for i, spec in enumerate(specs, 1):
        print(f"[{i}/{len(specs)}] {spec.family_id}")
        fam_rows: List[RunRow] = []
        for set_name, sb in sets.items():
            for mode in ("pullback", "continuation"):
                row = run_one(spec, sb, mode)
                fam_rows.append(row)
                all_rows.append(row)
                if row.error:
                    print(f"  ERR {set_name} {mode}: {row.error[:80]}")
        # family-level hard fail only if every run errored
        if fam_rows and all(r.error for r in fam_rows):
            missing.append(spec.family_id)

    ranking: List[Dict[str, Any]] = []
    for spec in specs:
        fam_rows = [r for r in all_rows if r.family_id == spec.family_id]
        agg = aggregate(fam_rows)
        ranking.append(
            {
                "family_id": spec.family_id,
                "title": spec.title,
                "kind": spec.kind,
                "profile": spec.adapter_profile,
                "source": spec.source,
                **agg,
            }
        )
    ranking.sort(key=lambda r: (r["score"], r["profit_factor"], r["total_return"]), reverse=True)
    for i, r in enumerate(ranking, 1):
        r["rank"] = i

    vbt_version = getattr(vbt, "__version__", "unknown")
    write_report(symbol, str(data_path), window, specs, all_rows, ranking, vbt_version, counts)
    reorganize(ranking, specs)

    payload = {
        "mode": "1to1_no_collapse",
        "counts": counts,
        "symbol": symbol,
        "data_path": str(data_path),
        "window": window,
        "vectorbt": vbt_version,
        "sets": list(OFFICIAL_SETS.keys()),
        "modes": ["pullback", "continuation"],
        "missing_all_error": missing,
        "ranking": ranking,
        "rows": [asdict(r) for r in all_rows],
    }
    REPORT_JSON.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    print(f"Wrote {REPORT_MD}")
    print(f"Wrote {REPORT_JSON}")
    print(f"Families ranked: {len(ranking)} inventory={counts['total_families']}")
    if missing:
        print("ALL-ERROR families:", missing)
        return 3
    print("TOP 5:")
    for r in ranking[:5]:
        print(f"  #{r['rank']} {r['family_id']} score={r['score']:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
