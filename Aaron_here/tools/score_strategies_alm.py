"""
Aaron Learning Method (ALM) scorer for strategies/ lab results.

Reads:
  strategies/MONTE_CARLO_RESULTS.json
  strategies/TWEAKED_ACCURACY_RESULTS.json  (optional soft WR)

Writes:
  Aaron_here/AARON_ALM_SCORES.json
  Aaron_here/AARON_ALM_TOP10.md
  Aaron_here/AARON_ALM_FULL_RANK.md

Usage (repo root):
  python -m Aaron_here.tools.score_strategies_alm
  python Aaron_here/tools/score_strategies_alm.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
STRATEGIES = ROOT / "strategies"
AARON = ROOT / "Aaron_here"
MC_JSON = STRATEGIES / "MONTE_CARLO_RESULTS.json"
ACC_JSON = STRATEGIES / "TWEAKED_ACCURACY_RESULTS.json"
OUT_JSON = AARON / "AARON_ALM_SCORES.json"
OUT_TOP10 = AARON / "AARON_ALM_TOP10.md"
OUT_FULL = AARON / "AARON_ALM_FULL_RANK.md"

# --- ALM weights (transparent) ---
W_MC_MED = 120.0       # per unit terminal above/below 1.0  (0.01 → +1.2)
W_P_LOSS = 55.0        # * (1 - p_loss)
W_MEAN_TR = 8000.0     # * mean_trade_return (fraction)
W_HIST_DD = 40.0       # * hist_max_dd (fraction) penalty
W_WR_SOFT = 0.08       # * min(wr, 85)  secondary only
# sample + geometry added separately

# Geometry class: profile → bonus (shape alignment with Force/Load/Reclaim teaching)
GEO_BONUS = {
    "mcflurry": 8.0,
    "cci_gravity": 7.5,
    "mark_rsi_bb": 6.5,
    "truth_s1_cci": 5.0,
    "truth_s4_rsi_snap": 4.5,
    "sma_scalp": 4.0,
    "dimension_jump": 3.5,
    "bb_mtf": 2.0,
    "donchian": 1.5,
    "guide_s03_donchian_turtle": 1.5,
    "guide_s01_ma_cross": 1.0,
    "guide_s06_psar": 1.0,
    "guide_s04_adx_di": 1.0,
    "guide_s05_roc": 0.5,
    # mean-rev / thrash / black-box: penalty or zero
    "rl_proxy": -6.0,
    "challenge": -4.0,
    "ma_ribbon": -5.0,
    "guide_s07_ema_ribbon": -5.0,
    "guide_s08_bb_mr": -1.0,
    "guide_s09_rsi_mr": -1.0,
    "guide_s10_vwap_mr": -2.0,
    "guide_s13_stoch_mr": -1.5,
    "guide_s14_willr_mr": -1.5,
    "momentum": -2.0,
}


def sample_quality(n: int) -> float:
    """Enough trades, but thrash spam is not virtue."""
    if n <= 0:
        return -25.0
    if n < 15:
        return -12.0
    if n < 25:
        return -4.0
    if n <= 400:
        return 6.0 + min(4.0, math.log10(max(n, 10)) * 2.0)
    if n <= 900:
        return 3.0
    if n <= 1400:
        return -2.0
    return -8.0  # thrash volume


def geo_bonus(profile: str) -> float:
    if not profile:
        return 0.0
    if profile in GEO_BONUS:
        return GEO_BONUS[profile]
    if profile.startswith("guide_s0") and int(profile[7:9] or "0") <= 7:
        return 0.5  # trend-ish guides mild
    if profile.startswith("guide_"):
        return -0.5
    return 0.0


def alm_score(row: Dict[str, Any], wr: Optional[float]) -> Dict[str, Any]:
    n = int(row.get("n_trades") or 0)
    mc_med = float(row.get("mc_median_terminal") or 1.0)
    p_loss = float(row.get("mc_prob_loss") or 0.0)
    mean_tr = float(row.get("mean_trade_return") or 0.0)
    hist_dd = float(row.get("hist_max_dd") or 0.0)
    profile = str(row.get("profile") or "")
    wr_v = float(wr) if wr is not None else 0.0

    parts = {
        "mc_med_term": W_MC_MED * (mc_med - 1.0),
        "p_loss_term": W_P_LOSS * (1.0 - p_loss),
        "mean_tr_term": W_MEAN_TR * mean_tr,
        "dd_penalty": -W_HIST_DD * hist_dd,
        "sample_q": sample_quality(n),
        "wr_soft": W_WR_SOFT * min(max(wr_v, 0.0), 85.0),
        "geo": geo_bonus(profile),
    }
    # hard disqualify empty books from top (still scored low)
    if n <= 0 or row.get("error"):
        parts["empty_penalty"] = -50.0
    else:
        parts["empty_penalty"] = 0.0

    total = sum(parts.values())
    return {
        "alm_score": total,
        "parts": parts,
        "n_trades": n,
        "mc_median_terminal": mc_med,
        "mc_prob_loss": p_loss,
        "mean_trade_return": mean_tr,
        "hist_max_dd": hist_dd,
        "win_rate_acc": wr_v,
        "profile": profile,
    }


def main() -> int:
    if not MC_JSON.exists():
        print("Missing", MC_JSON, file=sys.stderr)
        return 2
    mc = json.loads(MC_JSON.read_text(encoding="utf-8"))
    wr_by: Dict[str, float] = {}
    if ACC_JSON.exists():
        acc = json.loads(ACC_JSON.read_text(encoding="utf-8"))
        for r in acc.get("results", []):
            wr_by[r["family_id"]] = float(r.get("win_rate") or 0.0)

    scored: List[Dict[str, Any]] = []
    for row in mc.get("results", []):
        fid = row["family_id"]
        s = alm_score(row, wr_by.get(fid))
        scored.append(
            {
                "family_id": fid,
                "title": row.get("title"),
                "kind": row.get("kind"),
                "profile": s["profile"],
                "alm_score": s["alm_score"],
                "n_trades": s["n_trades"],
                "mc_median_terminal": s["mc_median_terminal"],
                "mc_prob_loss": s["mc_prob_loss"],
                "mean_trade_return": s["mean_trade_return"],
                "hist_max_dd": s["hist_max_dd"],
                "win_rate_acc": s["win_rate_acc"],
                "hist_terminal_mult": row.get("hist_terminal_mult"),
                "parts": s["parts"],
                "error": row.get("error") or "",
            }
        )

    scored.sort(key=lambda r: (r["alm_score"], r["mc_median_terminal"], -r["mc_prob_loss"]), reverse=True)
    for i, r in enumerate(scored, 1):
        r["alm_rank"] = i

    meta = {
        "method": "Aaron Learning Method (ALM)",
        "n_families": len(scored),
        "mc_meta": mc.get("meta", {}),
        "weights": {
            "W_MC_MED": W_MC_MED,
            "W_P_LOSS": W_P_LOSS,
            "W_MEAN_TR": W_MEAN_TR,
            "W_HIST_DD": W_HIST_DD,
            "W_WR_SOFT": W_WR_SOFT,
            "sample_quality": "see score_strategies_alm.sample_quality",
            "geometry_bonus": GEO_BONUS,
        },
        "not": [
            "Court promote",
            "live deploy list",
            "win-rate-only ranking",
        ],
    }
    OUT_JSON.write_text(
        json.dumps({"meta": meta, "ranking": scored}, indent=2, default=str),
        encoding="utf-8",
    )

    top = scored[:10]
    # one best family per profile (unique geometry classes)
    seen_prof = set()
    top_unique: List[Dict[str, Any]] = []
    for r in scored:
        p = r["profile"] or "_none_"
        if p in seen_prof:
            continue
        seen_prof.add(p)
        top_unique.append(r)
        if len(top_unique) >= 10:
            break

    lines = [
        "# Aaron ALM — Top 10 strategies (lab fuel)",
        "",
        "**Teacher:** Aaron (`@Aaron_here`)",
        f"**Families scored:** {len(scored)} (every row in Monte Carlo results)",
        "**Method:** [AARON_LEARNING_METHOD.md](AARON_LEARNING_METHOD.md)",
        "**Not Court law. Not a live deploy list.**",
        "",
        "Test = ALM re-score of each strategy’s lab Monte Carlo + accuracy WR (soft).",
        "Contract: same EURUSD window / 2HTF+1LTF / PB+cont as `strategies/` prove pipeline.",
        "",
        "## ALM ranking formula (plain)",
        "",
        "```text",
        "alm_score =",
        f"  {W_MC_MED} * (mc_median_terminal - 1)",
        f"+ {W_P_LOSS} * (1 - P(loss))",
        f"+ {W_MEAN_TR} * mean_trade_return",
        f"- {W_HIST_DD} * hist_max_dd",
        "+ sample_quality(n_trades)",
        f"+ {W_WR_SOFT} * min(accuracy_WR, 85)   # soft only",
        "+ geometry_bonus(profile)         # F/L/R alignment",
        "```",
        "",
        "## A) Top 10 by raw ALM score (filenames)",
        "",
        "Many may share one **profile** (same geometry).",
        "",
        "| ALM# | Family | Profile | ALM score | MC med | P(loss) | Trades | Acc WR% | Mean tr |",
        "|-----:|--------|---------|----------:|-------:|--------:|-------:|--------:|--------:|",
    ]
    for r in top:
        lines.append(
            f"| {r['alm_rank']} | `{r['family_id']}` | `{r['profile']}` | {r['alm_score']:.2f} | "
            f"{r['mc_median_terminal']:.4f} | {r['mc_prob_loss']*100:.1f}% | {r['n_trades']} | "
            f"{r['win_rate_acc']:.1f} | {r['mean_trade_return']*100:.4f}% |"
        )

    lines += [
        "",
        "## B) Top 10 **unique geometries** (one winner per profile) — use this for teaching",
        "",
        "| # | Family (best of profile) | Profile | ALM# | ALM score | MC med | P(loss) | Trades | Acc WR% |",
        "|--:|--------------------------|---------|-----:|----------:|-------:|--------:|-------:|--------:|",
    ]
    for i, r in enumerate(top_unique, 1):
        lines.append(
            f"| {i} | `{r['family_id']}` | `{r['profile']}` | {r['alm_rank']} | {r['alm_score']:.2f} | "
            f"{r['mc_median_terminal']:.4f} | {r['mc_prob_loss']*100:.1f}% | {r['n_trades']} | "
            f"{r['win_rate_acc']:.1f} |"
        )

    lines += [
        "",
        "## How to read this top 10",
        "",
        "| Do | Don't |",
        "|----|--------|",
        "| Use as **positive shape pointers** for RL curriculum | Call them production bots |",
        "| Prefer table **B** (unique profiles) for diversity | Treat 10 CCI filenames as 10 edges |",
        "| Prefer high MC med + low P(loss) + sane N | Rank by Acc WR alone |",
        "",
        "### Profile collapse note",
        "",
        "Raw top-10 is often almost all `cci_gravity` reclaim geometry — **one shape**, many MT names.",
        "Table **B** is Aaron’s teaching shortlist.",
        "",
        "## Geometry bonuses used (excerpt)",
        "",
        "```text",
        "mcflurry +8 · cci_gravity +7.5 · mark_rsi_bb +6.5 · sma_scalp +4",
        "rl_proxy -6 · ma_ribbon / guide ema ribbon -5 · challenge -4",
        "```",
        "",
        "## Full rank",
        "",
        "See [AARON_ALM_FULL_RANK.md](AARON_ALM_FULL_RANK.md) · raw [AARON_ALM_SCORES.json](AARON_ALM_SCORES.json)",
        "",
        "## Bottom 5 (counter-examples for training)",
        "",
        "| ALM# | Family | ALM score | MC med | P(loss) | Trades |",
        "|-----:|--------|----------:|-------:|--------:|-------:|",
    ]
    for r in scored[-5:]:
        lines.append(
            f"| {r['alm_rank']} | `{r['family_id']}` | {r['alm_score']:.2f} | "
            f"{r['mc_median_terminal']:.4f} | {r['mc_prob_loss']*100:.1f}% | {r['n_trades']} |"
        )
    lines += [
        "",
        "---",
        "",
        "**Aaron:** Top-10 under ALM = best **lab fuel** for Force/Load/Reclaim teaching + path honesty on this window.",
        "Next: label windows from table B profiles (PKG-001), train stages 1–3, re-score student compliance.",
        "",
    ]
    OUT_TOP10.write_text("\n".join(lines), encoding="utf-8")

    # also store unique top in json meta output already written — patch file with unique list
    payload = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    payload["top10"] = top
    payload["top10_unique_profile"] = top_unique
    OUT_JSON.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    full = [
        "# Aaron ALM — full rank (all strategies)",
        "",
        f"n={len(scored)} · method weights in AARON_ALM_SCORES.json meta",
        "",
        "| Rank | Family | Profile | ALM | MC med | P(loss) | N | WR% |",
        "|-----:|--------|---------|----:|-------:|--------:|--:|----:|",
    ]
    for r in scored:
        full.append(
            f"| {r['alm_rank']} | `{r['family_id']}` | `{r['profile']}` | {r['alm_score']:.2f} | "
            f"{r['mc_median_terminal']:.4f} | {r['mc_prob_loss']*100:.1f}% | {r['n_trades']} | {r['win_rate_acc']:.1f} |"
        )
    OUT_FULL.write_text("\n".join(full) + "\n", encoding="utf-8")

    print(f"Scored {len(scored)} families")
    print("TOP 10:")
    for r in top:
        print(
            f"  #{r['alm_rank']:2d} {r['family_id'][:48]:48s} "
            f"alm={r['alm_score']:7.2f} mc={r['mc_median_terminal']:.4f} "
            f"ploss={r['mc_prob_loss']*100:5.1f}% n={r['n_trades']}"
        )
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_TOP10)
    print("Wrote", OUT_FULL)
    return 0


if __name__ == "__main__":
    # allow both package and script path
    raise SystemExit(main())
