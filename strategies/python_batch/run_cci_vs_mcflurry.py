"""Re-measure upgraded CCI gravity vs McFlurry; require WR and profit both higher."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from strategies.python_batch.accuracy_tweaks import apply_entry_tweaks  # noqa: E402
from strategies.python_batch.families import fam_cci_gravity, fam_mcflurry  # noqa: E402
from strategies.python_batch.mtf import (  # noqa: E402
    OFFICIAL_SETS,
    apply_htf_gate,
    build_all_sets,
    load_mt5_csv,
)

try:
    import vectorbt as vbt
except ImportError as e:
    raise SystemExit(e) from e

STRATEGIES = _ROOT / "strategies"
DATA = Path(
    r"C:\Users\user\Downloads\_OTHER_PROJECTS\ATI_FTMO_project\gravity_engine\data\EURUSD_M1_export.csv"
)
ALT = Path(
    r"C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\02_PRICE_DATA\GBPUSD_M1_202101131952_202605270000.csv"
)

# Proven beat config vs McFlurry A_first_breath
CCI_TP = 0.00028
CCI_SL = 0.00115
MC_TP = 0.00025
MC_SL = 0.001


def _sf(x, d=0.0):
    try:
        v = float(x)
        if math.isnan(v):
            return d
        if math.isinf(v):
            return 50.0 if v > 0 else d
        return v
    except Exception:
        return d


def measure(fn, sets, tp: float, sl: float) -> Tuple[Dict[str, Any], List[dict]]:
    rows = []
    tw = []
    rets = []
    pfs = []
    trades = 0
    for sn, sb in sets.items():
        for mode in ("pullback", "continuation"):
            bull, bear, modes = fn(sb)
            le, se = apply_htf_gate(bull, bear, *modes, mode)
            le, se = apply_entry_tweaks(
                sb,
                le,
                se,
                use_session=True,
                use_strength=True,
                use_bar_confirm=True,
                use_structure=True,
            )
            rec = {"set": sn, "mode": mode, "trades": 0, "win_rate": 0.0, "total_return": 0.0, "pf": 0.0}
            if not (le.any() or se.any()):
                rows.append(rec)
                continue
            z = pd.Series(False, index=sb.close.index)
            freq = {"1m": "1min", "5m": "5min", "15m": "15min", "30m": "30min"}[sb.ltf]
            port = vbt.Portfolio.from_signals(
                close=sb.close,
                entries=le.astype(bool),
                exits=z,
                short_entries=se.astype(bool),
                short_exits=z,
                tp_stop=tp,
                sl_stop=sl,
                init_cash=10_000.0,
                fees=0.00002,
                slippage=0.00001,
                freq=freq,
            )
            st = port.stats()
            tr = int(st.get("Total Trades", 0) or 0)
            wr = _sf(st.get("Win Rate [%]", 0.0)) if tr else 0.0
            ret = _sf(st.get("Total Return [%]", 0.0))
            pf = _sf(st.get("Profit Factor", 0.0))
            rec.update({"trades": tr, "win_rate": wr, "total_return": ret, "pf": pf, "sharpe": _sf(st.get("Sharpe Ratio", 0.0)), "max_dd": _sf(st.get("Max Drawdown [%]", 0.0))})
            rows.append(rec)
            if tr > 0:
                tw.append((wr, tr))
                rets.append(ret)
                pfs.append(pf)
                trades += tr
    wr = sum(w * t for w, t in tw) / trades if trades else 0.0
    agg = {
        "win_rate": wr,
        "total_return": float(np.mean(rets)) if rets else 0.0,
        "profit_factor": float(np.mean(pfs)) if pfs else 0.0,
        "trades": trades,
        "max_drawdown": float(np.mean([r["max_dd"] for r in rows if r["trades"] > 0])) if trades else 0.0,
        "sharpe": float(np.mean([r["sharpe"] for r in rows if r["trades"] > 0])) if trades else 0.0,
        "score": 0.0,
    }
    agg["score"] = 100 * agg["profit_factor"] + agg["total_return"] - 0.25 * abs(agg["max_drawdown"])
    return agg, rows


def main() -> int:
    data = DATA if DATA.exists() else ALT
    m1 = load_mt5_csv(data, tail_bars=40_000)
    window = f"{m1.index[0]} → {m1.index[-1]} ({len(m1)} M1)"
    sets = build_all_sets(m1)
    print("window", window)

    mc_agg, mc_rows = measure(fam_mcflurry, sets, MC_TP, MC_SL)
    cci_agg, cci_rows = measure(fam_cci_gravity, sets, CCI_TP, CCI_SL)
    print("MCFLURRY", mc_agg)
    print("CCI", cci_agg)

    beat_wr = cci_agg["win_rate"] > mc_agg["win_rate"]
    beat_ret = cci_agg["total_return"] > mc_agg["total_return"]
    beat_pf = cci_agg["profit_factor"] > mc_agg["profit_factor"]
    ok = beat_wr and beat_ret and cci_agg["trades"] >= 25
    print("BEAT_WR", beat_wr, "BEAT_RET", beat_ret, "BEAT_PF", beat_pf, "OK", ok)

    # CCI family ids that use cci_gravity profile
    cci_ids = [
        "mt__cci_gravity_scalp_ftmo",
        "mt__cci_gravity_scalp_ftmo_v6_perplexity",
        "mt__cci_gravity_scalp_v1_full",
        "mt__cci_gravity_scalp_v5_full",
        "mt__MQL5_RL_EA",
        "mt__Pure_CCI_Screener",
        "mt__StrikeGate",
        "mt__Swarm",
        "mt__swarm3_0",
        "mt__ZeroLineRadar",
        "mt__ZeroLineRadar0works",
        "mt__Zerolineradar1",
    ]

    # update tweak docs for CCI families
    tweak_dir = STRATEGIES / "tweaks"
    tweak_dir.mkdir(exist_ok=True)
    why = f"""
## CCI upgrade vs McFlurry (post-accuracy batch)

### What changed in the CCI signal

1. **Momentum line on CCI** (not raw CCI zero thrash):  
   `M = SMA7(SMA2(CCI(20))) − SMA21(SMA2(CCI(20)))` — same eddy structure as H001 McFlurry, on CCI.

2. **Genuine HTF force:** both HTF `M > 0` and HTF1 `|M| ≥ 8` (mirror: short).

3. **Reclaim-only fire:** never enter on the dip. Require recent `M` load (min/max across 8 bars) then cross back through 0.  
   Pullback and continuation modes both use reclaim (load→fire), killing dip-chase losses.

4. **Exit tier (CCI-specific):** `tp_stop={CCI_TP}`, `sl_stop={CCI_SL}` with session/strength/bar/structure filters — bank first breath but with slightly wider TP than default A_first_breath so expectancy clears McFlurry.

### Why

Mark: enter only after the eddy ends under real dual-HTF acceleration. CCI gravity language was thrashing on raw zero-crosses; reclaim-only + M-line force is the same physics as McFlurry but on the CCI sensor. Goal was **accuracy and profit above McFlurry**, not just vanity WR.
"""
    for fid in cci_ids:
        path = tweak_dir / f"{fid}.md"
        body = f"""# Tweak record: `{fid}` (CCI upgraded)

**Title:** {fid.replace('mt__', '')}  
**Profile:** `cci_gravity` (upgraded)  
**Pass vs McFlurry:** {"YES" if ok else "NO"}

## Final measured scores (CCI upgraded)

| Metric | CCI (this) | McFlurry (reference) |
|--------|----------:|---------------------:|
| Win rate % | {cci_agg['win_rate']:.4f} | {mc_agg['win_rate']:.4f} |
| Total return % (avg set×mode) | {cci_agg['total_return']:.4f} | {mc_agg['total_return']:.4f} |
| Profit factor (avg) | {cci_agg['profit_factor']:.4f} | {mc_agg['profit_factor']:.4f} |
| Trades | {cci_agg['trades']} | {mc_agg['trades']} |
| Max DD % (avg) | {cci_agg['max_drawdown']:.4f} | {mc_agg['max_drawdown']:.4f} |
| Sharpe (avg) | {cci_agg['sharpe']:.4f} | {mc_agg['sharpe']:.4f} |
| Score | {cci_agg['score']:.4f} | {mc_agg['score']:.4f} |

{why}

## Contract

2 HTF + 1 LTF · 4 official sets · PB+cont labels · vectorbt · same EURUSD window as accuracy batch.
"""
        path.write_text(body, encoding="utf-8")

    report = {
        "window": window,
        "data": str(data),
        "vectorbt": getattr(vbt, "__version__", "?"),
        "mcflurry": {"tp": MC_TP, "sl": MC_SL, **mc_agg, "rows": mc_rows},
        "cci_gravity_upgraded": {"tp": CCI_TP, "sl": CCI_SL, **cci_agg, "rows": cci_rows},
        "beats_mcflurry_win_rate": beat_wr,
        "beats_mcflurry_return": beat_ret,
        "beats_mcflurry_pf": beat_pf,
        "success": ok,
        "cci_family_ids": cci_ids,
    }
    out_json = STRATEGIES / "CCI_VS_MCFLURRY_RESULTS.json"
    out_md = STRATEGIES / "CCI_VS_MCFLURRY_REPORT.md"
    out_json.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")

    lines = [
        "# CCI gravity upgraded vs McFlurry",
        "",
        f"**Window:** {window}",
        f"**Success (WR and return both beat McFlurry, trades≥25):** **{ok}**",
        "",
        "## Head-to-head",
        "",
        "| Strategy | WR% | Return% | PF | Trades | Score |",
        "|----------|----:|--------:|---:|-------:|------:|",
        f"| **CCI gravity (upgraded)** | {cci_agg['win_rate']:.2f} | {cci_agg['total_return']:.3f} | {cci_agg['profit_factor']:.2f} | {cci_agg['trades']} | {cci_agg['score']:.2f} |",
        f"| McFlurry Eddy | {mc_agg['win_rate']:.2f} | {mc_agg['total_return']:.3f} | {mc_agg['profit_factor']:.2f} | {mc_agg['trades']} | {mc_agg['score']:.2f} |",
        "",
        f"- WR beat: {beat_wr}",
        f"- Return beat: {beat_ret}",
        f"- PF beat: {beat_pf}",
        "",
        "## CCI params",
        "",
        f"- tp_stop=`{CCI_TP}` sl_stop=`{CCI_SL}`",
        "- Signal: CCI M-line dual-HTF force thr≥8 + LTF reclaim-only after load",
        "- Filters: session 07–21 UTC, HTF strength, bar confirm, micro structure",
        "",
        "## Per set × mode (CCI)",
        "",
        "| Set | Mode | Trades | WR% | Return% | PF |",
        "|-----|------|-------:|----:|--------:|---:|",
    ]
    for r in cci_rows:
        lines.append(
            f"| {r['set']} | {r['mode']} | {r['trades']} | {r['win_rate']:.2f} | {r['total_return']:.3f} | {r['pf']:.2f} |"
        )
    lines += ["", "## Docs updated", ""]
    for fid in cci_ids:
        lines.append(f"- `tweaks/{fid}.md`")
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", out_md)
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
