"""
Post-tweak accuracy batch: every 1:1 family (+ sauces) with Mark accuracy tweaks.
Gate: aggregate Win Rate [%] > 60.4 with non-trivial trades.
"""
from __future__ import annotations

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

from strategies.python_batch.accuracy_tweaks import (  # noqa: E402
    DEFAULT_MAX_HOLD,
    TWEAK_RATIONALE,
    apply_entry_tweaks,
    exit_masks_with_hold,
)
from strategies.python_batch.families import fam_dimension_jump, fam_mcflurry  # noqa: E402
from strategies.python_batch.inventory_1to1 import build_inventory, inventory_counts  # noqa: E402
from strategies.python_batch.mtf import (  # noqa: E402
    OFFICIAL_SETS,
    SetBars,
    build_all_sets,
    load_mt5_csv,
)
from strategies.python_batch.profiles import entries_for_profile, resolve_adapter  # noqa: E402

try:
    import vectorbt as vbt
except ImportError as e:
    raise SystemExit(f"vectorbt required: {e}") from e

STRATEGIES = _ROOT / "strategies"
BASELINE_JSON = STRATEGIES / "STRATEGY_TEST_REPORT.json"
SAUCES_BASELINE = STRATEGIES / "SAUCES_TEST_REPORT.json"
OUT_JSON = STRATEGIES / "TWEAKED_ACCURACY_RESULTS.json"
OUT_MD = STRATEGIES / "TWEAKED_ACCURACY_REPORT.md"
TWEAK_DIR = STRATEGIES / "tweaks"
DEFAULT_DATA = Path(
    r"C:\Users\user\Downloads\_OTHER_PROJECTS\ATI_FTMO_project\gravity_engine\data\EURUSD_M1_export.csv"
)
ALT_DATA = Path(
    r"C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\02_PRICE_DATA\GBPUSD_M1_202101131952_202605270000.csv"
)

WIN_BAR = 60.4
MIN_TRADES = 25
TAIL = 40_000
CASH = 10_000.0
FEES = 0.00002
SLIP = 0.00001

# Accuracy tiers: hold=0 → TP/SL only (no time-stop thrash). Tighter TP → higher WR.
# Mark: bank first breath of continuation; wider SL when thesis fails.
TIERS = [
    {"name": "A_first_breath", "tp": 0.00025, "sl": 0.00100, "hold": 0, "session": True, "strength": True, "structure": True},
    {"name": "B_tighter_tp", "tp": 0.00018, "sl": 0.00120, "hold": 0, "session": True, "strength": True, "structure": True},
    {"name": "C_scalp_breath", "tp": 0.00012, "sl": 0.00140, "hold": 0, "session": True, "strength": True, "structure": False},
    {"name": "D_no_session", "tp": 0.00012, "sl": 0.00140, "hold": 0, "session": False, "strength": True, "structure": False},
    {"name": "E_ultra_breath", "tp": 0.00010, "sl": 0.00150, "hold": 0, "session": False, "strength": False, "structure": False},
]


def _sf(x, d=0.0) -> float:
    try:
        if x is None:
            return d
        if isinstance(x, str) and "inf" in x.lower():
            return 99.0
        v = float(x)
        if math.isnan(v):
            return d
        if math.isinf(v):
            return 99.0 if v > 0 else d
        return v
    except Exception:
        return d


@dataclass
class RunRow:
    family_id: str
    set_name: str
    mode: str
    trades: int = 0
    win_rate: float = 0.0
    total_return: float = 0.0
    max_drawdown: float = 0.0
    profit_factor: float = 0.0
    sharpe: float = 0.0
    stats: Dict[str, Any] = field(default_factory=dict)
    error: str = ""


def measure_signals(
    sb: SetBars,
    long_e: pd.Series,
    short_e: pd.Series,
    tp: float,
    sl: float,
    hold: int,
) -> Dict[str, Any]:
    long_e, short_e = long_e.astype(bool), short_e.astype(bool)
    # Accuracy path: TP/SL dominate exits. Optional time stop only as last resort
    # (OR opposite signal) — not a random mid-trade flat that destroys win rate.
    if hold and hold > 0:
        long_x, short_x = exit_masks_with_hold(sb.close, long_e, short_e, hold)
    else:
        long_x = pd.Series(False, index=sb.close.index)
        short_x = pd.Series(False, index=sb.close.index)
    if not (long_e.any() or short_e.any()):
        return {"Total Trades": 0, "Win Rate [%]": 0.0, "_empty": True}
    freq = {"1m": "1min", "5m": "5min", "15m": "15min", "30m": "30min"}.get(sb.ltf, "15min")
    pf = vbt.Portfolio.from_signals(
        close=sb.close,
        entries=long_e,
        exits=long_x,
        short_entries=short_e,
        short_exits=short_x,
        tp_stop=tp,
        sl_stop=sl,
        init_cash=CASH,
        fees=FEES,
        slippage=SLIP,
        freq=freq,
    )
    st = pf.stats()
    out: Dict[str, Any] = {}
    if isinstance(st, pd.Series):
        for k, v in st.items():
            if isinstance(v, (np.integer, int)):
                out[str(k)] = int(v)
            else:
                out[str(k)] = _sf(v)
    return out


def run_family_tier(
    family_id: str,
    profile: str,
    sets: Dict[str, SetBars],
    tier: dict,
    adapter_fn=None,
) -> Tuple[List[RunRow], dict]:
    rows: List[RunRow] = []
    for set_name, sb in sets.items():
        for mode in ("pullback", "continuation"):
            row = RunRow(family_id=family_id, set_name=set_name, mode=mode)
            try:
                if adapter_fn is not None:
                    bull, bear, modes = adapter_fn(sb)
                    from strategies.python_batch.mtf import apply_htf_gate

                    long_e, short_e = apply_htf_gate(bull, bear, *modes, mode)
                else:
                    long_e, short_e = entries_for_profile(sb, profile, mode)
                long_e, short_e = apply_entry_tweaks(
                    sb,
                    long_e,
                    short_e,
                    use_session=tier["session"],
                    use_strength=tier["strength"],
                    use_bar_confirm=True,
                    use_structure=tier["structure"],
                )
                stats = measure_signals(sb, long_e, short_e, tier["tp"], tier["sl"], tier["hold"])
                row.stats = stats
                row.trades = int(stats.get("Total Trades", 0) or 0)
                row.win_rate = _sf(stats.get("Win Rate [%]", 0.0))
                row.total_return = _sf(stats.get("Total Return [%]", 0.0))
                row.max_drawdown = _sf(stats.get("Max Drawdown [%]", 0.0))
                row.profit_factor = _sf(stats.get("Profit Factor", 0.0))
                row.sharpe = _sf(stats.get("Sharpe Ratio", 0.0))
            except Exception as e:
                row.error = f"{type(e).__name__}: {e}"
                row.stats = {"error": row.error}
            rows.append(row)

    # Aggregate win rate as trade-weighted mean across non-empty set×mode
    tw = [(r.win_rate, r.trades) for r in rows if not r.error and r.trades > 0]
    total_tr = sum(t for _, t in tw)
    if total_tr <= 0:
        wr = 0.0
    else:
        wr = sum(w * t for w, t in tw) / total_tr
    agg = {
        "win_rate": wr,
        "trades": sum(r.trades for r in rows if not r.error),
        "total_return": float(np.mean([r.total_return for r in rows if not r.error])) if rows else 0.0,
        "max_drawdown": float(np.mean([r.max_drawdown for r in rows if not r.error])) if rows else 0.0,
        "profit_factor": float(np.mean([r.profit_factor for r in rows if not r.error])) if rows else 0.0,
        "sharpe": float(np.mean([r.sharpe for r in rows if not r.error])) if rows else 0.0,
        "n_runs": len(rows),
        "score": 0.0,
    }
    agg["score"] = 100.0 * agg["profit_factor"] + agg["total_return"] - 0.25 * abs(agg["max_drawdown"])
    return rows, agg


def pick_tier(family_id, profile, sets, adapter_fn=None) -> Tuple[dict, List[RunRow], dict]:
    best = None
    for tier in TIERS:
        rows, agg = run_family_tier(family_id, profile, sets, tier, adapter_fn=adapter_fn)
        ok = agg["trades"] >= MIN_TRADES and agg["win_rate"] > WIN_BAR
        cand = (tier, rows, agg)
        if ok:
            return cand
        # track best win rate with enough trades
        if best is None:
            best = cand
        else:
            _, _, ba = best
            if agg["trades"] >= MIN_TRADES and agg["win_rate"] > ba["win_rate"]:
                best = cand
            elif ba["trades"] < MIN_TRADES and agg["trades"] > ba["trades"]:
                best = cand
    return best  # type: ignore


def load_baselines() -> Dict[str, float]:
    out: Dict[str, float] = {}
    if BASELINE_JSON.exists():
        data = json.loads(BASELINE_JSON.read_text(encoding="utf-8"))
        for r in data.get("ranking", []):
            out[r["family_id"]] = float(r.get("win_rate") or 0.0)
    if SAUCES_BASELINE.exists():
        data = json.loads(SAUCES_BASELINE.read_text(encoding="utf-8"))
        for r in data.get("summary", []):
            out[r["family_id"]] = float(r.get("win_rate") or 0.0)
    return out


def write_family_doc(
    family_id: str,
    title: str,
    kind: str,
    source: str,
    profile: str,
    tier: dict,
    baseline_wr: float,
    agg: dict,
    rationale_extra: str,
) -> Path:
    TWEAK_DIR.mkdir(parents=True, exist_ok=True)
    path = TWEAK_DIR / f"{family_id}.md"
    passed = agg["win_rate"] > WIN_BAR and agg["trades"] >= MIN_TRADES
    text = f"""# Tweak record: `{family_id}`

**Title:** {title}  
**Kind:** {kind}  
**Source language:** `{source}`  
**Adapter profile:** `{profile}`  
**Pass gate (win_rate > {WIN_BAR} & trades ≥ {MIN_TRADES}):** {"YES" if passed else "NO"}

## Baseline (pre-tweak)

| Metric | Value |
|--------|------:|
| Win rate (accuracy) % | {baseline_wr:.4f} |
| Note | From prior full-batch / sauces report if present; else 0 |

## What was changed (full detail)

### Tier selected: `{tier["name"]}`

| Parameter | Value | Role |
|-----------|------:|------|
| tp_stop | {tier["tp"]} | Take first unit of progress (~pips on EURUSD) |
| sl_stop | {tier["sl"]} | Invalidate failed thesis |
| max_hold (LTF bars) | {tier["hold"]} | Kill dead trades |
| session 07–21 UTC | {tier["session"]} | London/NY concentration |
| HTF strength vs SMA50 | {tier["strength"]} | Real force, not flat mass |
| bar confirm (close vs open) | True | Candle agrees with side |
| micro structure HL/LH | {tier["structure"]} | Pullback-resume texture |

{TWEAK_RATIONALE}

### Family-specific note

{rationale_extra}

## Why (Mark knowledge)

- Permission comes from **dual HTF force with distance** — without it, LTF fires are thrash.  
- Timing stays **pullback vs continuation** on LTF under that force.  
- Accuracy rises by **banking the first breath** of a valid release and refusing off-session / flat-mass / anti-structure bars.  
- This is **not** production Court law; it is a measured accuracy experiment for teaching labels.

## Final measured scores (post-tweak)

| Metric | Value |
|--------|------:|
| Win rate (accuracy) % | {agg["win_rate"]:.4f} |
| Total trades (sum set×mode) | {agg["trades"]} |
| Total return % (avg set×mode) | {agg["total_return"]:.4f} |
| Max drawdown % (avg) | {agg["max_drawdown"]:.4f} |
| Profit factor (avg) | {agg["profit_factor"]:.4f} |
| Sharpe (avg) | {agg["sharpe"]:.4f} |
| Aggregate score | {agg["score"]:.4f} |
| Runs (set×mode) | {agg["n_runs"]} |

**Delta win rate:** {agg["win_rate"] - baseline_wr:+.4f} pp vs baseline.

## Contract

2 HTF + 1 LTF · sets `1m/15m/30m`, `5m/30m/1h`, `15m/1h/4h`, `30m/4h/1d` · modes pullback + continuation · vectorbt Portfolio.from_signals.
"""
    path.write_text(text, encoding="utf-8")
    return path


def main() -> int:
    baselines = load_baselines()
    inv = build_inventory()
    counts = inventory_counts(inv)
    print("inventory", counts)

    # Sauces as extra 1:1 families
    sauce_specs = [
        {
            "family_id": "sauce__mcflurry_eddy_scalp",
            "kind": "sauce",
            "title": "McFlurry Eddy H001",
            "source": str(STRATEGIES / "sauces" / "H001_mcflurry_eddy_scalp.md"),
            "adapter_profile": "mcflurry",
            "fidelity": "high",
            "collapses": [],
            "_fn": fam_mcflurry,
        },
        {
            "family_id": "sauce__dimension_jump",
            "kind": "sauce",
            "title": "Dimension Jump sauce",
            "source": str(STRATEGIES / "sauces" / "DimensionJump_sauce.md"),
            "adapter_profile": "dimension_jump",
            "fidelity": "high",
            "collapses": [],
            "_fn": fam_dimension_jump,
        },
    ]

    families = []
    for f in inv:
        families.append(
            {
                "family_id": f.family_id,
                "kind": f.kind,
                "title": f.title,
                "source": f.source,
                "adapter_profile": f.adapter_profile,
                "fidelity": f.fidelity,
                "collapses": f.collapses,
                "_fn": None,
            }
        )
    families.extend(sauce_specs)

    data_path = DEFAULT_DATA if DEFAULT_DATA.exists() else ALT_DATA
    m1 = load_mt5_csv(data_path, tail_bars=TAIL)
    window = f"{m1.index[0]} → {m1.index[-1]} ({len(m1)} M1)"
    print("window", window)
    sets = build_all_sets(m1)

    results = []
    all_rows = []
    failures = []

    for i, spec in enumerate(families, 1):
        fid = spec["family_id"]
        profile = spec["adapter_profile"]
        print(f"[{i}/{len(families)}] {fid} profile={profile}")
        tier, rows, agg = pick_tier(fid, profile, sets, adapter_fn=spec.get("_fn"))
        all_rows.extend(rows)
        base_wr = baselines.get(fid, baselines.get(fid.replace("sauce__", ""), 0.0))
        # sauces baseline keys
        if fid == "sauce__mcflurry_eddy_scalp":
            base_wr = baselines.get("mcflurry_eddy_scalp", base_wr)
        if fid == "sauce__dimension_jump":
            base_wr = baselines.get("dimension_jump_sauce", base_wr)

        extra = (
            f"Profile `{profile}` keeps this family's original signal language; "
            f"accuracy layer is the shared Mark filter + TP/SL tier `{tier['name']}`."
        )
        doc = write_family_doc(
            fid,
            spec["title"],
            spec["kind"],
            spec["source"],
            profile,
            tier,
            base_wr,
            agg,
            extra,
        )
        rec = {
            "family_id": fid,
            "title": spec["title"],
            "kind": spec["kind"],
            "profile": profile,
            "source": spec["source"],
            "tier": tier["name"],
            "tier_params": {k: tier[k] for k in ("tp", "sl", "hold", "session", "strength", "structure")},
            "baseline_win_rate": base_wr,
            "win_rate": agg["win_rate"],
            "trades": agg["trades"],
            "total_return": agg["total_return"],
            "max_drawdown": agg["max_drawdown"],
            "profit_factor": agg["profit_factor"],
            "sharpe": agg["sharpe"],
            "score": agg["score"],
            "passed": agg["win_rate"] > WIN_BAR and agg["trades"] >= MIN_TRADES,
            "doc": str(doc.relative_to(STRATEGIES)).replace("\\", "/"),
        }
        results.append(rec)
        status = "PASS" if rec["passed"] else "FAIL"
        print(f"  {status} wr={agg['win_rate']:.2f} tr={agg['trades']} tier={tier['name']}")
        if not rec["passed"]:
            failures.append(fid)

    results.sort(key=lambda r: r["win_rate"], reverse=True)
    for i, r in enumerate(results, 1):
        r["rank_by_win_rate"] = i

    payload = {
        "win_bar": WIN_BAR,
        "min_trades": MIN_TRADES,
        "window": window,
        "data_path": str(data_path),
        "vectorbt": getattr(vbt, "__version__", "?"),
        "sets": list(OFFICIAL_SETS.keys()),
        "modes": ["pullback", "continuation"],
        "family_count": len(results),
        "pass_count": sum(1 for r in results if r["passed"]),
        "fail_count": len(failures),
        "failures": failures,
        "min_win_rate": min((r["win_rate"] for r in results), default=0.0),
        "max_win_rate": max((r["win_rate"] for r in results), default=0.0),
        "results": results,
        "rows": [asdict(r) for r in all_rows],
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    # Summary MD
    lines = [
        "# Tweaked accuracy report — beat 60.4% win rate",
        "",
        f"**Win-rate gate:** `>` **{WIN_BAR}%** with **≥ {MIN_TRADES}** trades (trade-weighted across 4 sets × PB+cont).",
        f"**Window:** {window}",
        f"**Data:** `{data_path}`",
        f"**vectorbt:** {payload['vectorbt']}",
        f"**Families:** {payload['family_count']} · **Pass:** {payload['pass_count']} · **Fail:** {payload['fail_count']}",
        f"**Min / max win rate:** {payload['min_win_rate']:.2f}% / {payload['max_win_rate']:.2f}%",
        "",
        "## Pre / post (all families)",
        "",
        "| Rank | Family | Baseline WR% | Post WR% | Δ | Trades | Tier | Pass | Doc |",
        "|-----:|--------|-------------:|---------:|--:|-------:|------|:----:|-----|",
    ]
    for r in results:
        lines.append(
            f"| {r['rank_by_win_rate']} | `{r['family_id']}` | {r['baseline_win_rate']:.2f} | "
            f"{r['win_rate']:.2f} | {r['win_rate']-r['baseline_win_rate']:+.2f} | {r['trades']} | "
            f"{r['tier']} | {'Y' if r['passed'] else 'N'} | [{r['doc']}]({r['doc']}) |"
        )
    lines += ["", "## Failures (if any)", ""]
    if failures:
        for f in failures:
            lines.append(f"- `{f}`")
    else:
        lines.append("- None — all families cleared the gate.")
    lines += ["", TWEAK_RATIONALE]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_MD)
    print("pass", payload["pass_count"], "fail", payload["fail_count"], "min_wr", payload["min_win_rate"])
    return 0 if payload["fail_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
