"""Inject batch + accuracy + Monte Carlo simulation results into every strategy file.

Targets:
  - strategies/tweaks/*.md  (MC block refresh)
  - strategies/ranked/*/README.md  (full sim block)
  - strategies/sauces/H001_*.md, DimensionJump_*.md  (MC block refresh)

Source:
  STRATEGY_TEST_REPORT.json, TWEAKED_ACCURACY_RESULTS.json, MONTE_CARLO_RESULTS.json
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRATEGIES = ROOT
TWEAKS = STRATEGIES / "tweaks"
RANKED = STRATEGIES / "ranked"
SAUCES = STRATEGIES / "sauces"

MC_JSON = STRATEGIES / "MONTE_CARLO_RESULTS.json"
ACC_JSON = STRATEGIES / "TWEAKED_ACCURACY_RESULTS.json"
BATCH_JSON = STRATEGIES / "STRATEGY_TEST_REPORT.json"

MC_BEGIN = "<!-- MONTE_CARLO_BEGIN -->"
MC_END = "<!-- MONTE_CARLO_END -->"
SIM_BEGIN = "<!-- ALL_SIM_RESULTS_BEGIN -->"
SIM_END = "<!-- ALL_SIM_RESULTS_END -->"


def _f(x, nd=4):
    if x is None:
        return "—"
    try:
        return f"{float(x):.{nd}f}"
    except (TypeError, ValueError):
        return str(x)


def _pct(x, nd=2):
    if x is None:
        return "—"
    try:
        v = float(x)
        # MC stores prob as 0-1; accuracy WR often already percent
        if abs(v) <= 1.5:
            return f"{v * 100:.{nd}f}%"
        return f"{v:.{nd}f}%"
    except (TypeError, ValueError):
        return str(x)


def load_indexes():
    mc = json.loads(MC_JSON.read_text(encoding="utf-8"))
    acc = json.loads(ACC_JSON.read_text(encoding="utf-8"))
    batch = json.loads(BATCH_JSON.read_text(encoding="utf-8"))

    mc_by = {r["family_id"]: r for r in mc["results"]}
    # rank by mc_median_terminal desc
    ranked_mc = sorted(
        mc["results"],
        key=lambda r: (r.get("mc_median_terminal") or -999, r.get("n_trades") or 0),
        reverse=True,
    )
    mc_rank = {r["family_id"]: i + 1 for i, r in enumerate(ranked_mc)}

    acc_by = {r["family_id"]: r for r in acc.get("results", [])}
    batch_by = {r["family_id"]: r for r in batch.get("ranking", [])}

    meta_mc = mc.get("meta", {})
    meta_acc = {
        "win_bar": acc.get("win_bar"),
        "min_trades": acc.get("min_trades"),
        "window": acc.get("window"),
        "data_path": acc.get("data_path"),
        "vectorbt": acc.get("vectorbt"),
        "sets": acc.get("sets"),
        "modes": acc.get("modes"),
        "family_count": acc.get("family_count"),
        "pass_count": acc.get("pass_count"),
    }
    meta_batch = {
        "window": batch.get("window"),
        "data_path": batch.get("data_path"),
        "vectorbt": batch.get("vectorbt"),
        "sets": batch.get("sets"),
        "modes": batch.get("modes"),
        "counts": batch.get("counts"),
    }
    return mc_by, mc_rank, acc_by, batch_by, meta_mc, meta_acc, meta_batch, len(ranked_mc)


def format_mc_block(fid: str, r: dict, rank: int, n_total: int, meta: dict) -> str:
    sets = meta.get("sets") or []
    modes = meta.get("modes") or []
    sets_s = ", ".join(sets) if isinstance(sets, list) else str(sets)
    modes_s = " + ".join(modes) if isinstance(modes, list) else str(modes)
    lines = [
        MC_BEGIN,
        "## Monte Carlo simulation results",
        "",
        f"**Family id:** `{fid}`  ",
        f"**MC rank (by bootstrap median terminal):** **{rank}** / {n_total}  ",
        "**Not Court law.** Bootstrap + order-shuffle on pooled trade returns.",
        "",
        "### Simulation setup",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| Window | {meta.get('window', '—')} |",
        f"| Data | `{meta.get('data_path', '—')}` |",
        f"| Sims (bootstrap) | {meta.get('n_sims', 1000)} |",
        f"| Seed | {meta.get('seed', 42)} |",
        f"| Sets | `{sets_s}` |",
        f"| Modes | {modes_s} |",
        f"| Entry shell | session 07–21 UTC, HTF strength, bar confirm, micro structure |",
        f"| Exits | tp_stop={meta.get('tp_stop', 0.00025)} · sl_stop={meta.get('sl_stop', 0.001)} (vectorbt) |",
        f"| vectorbt | {meta.get('vectorbt', '—')} |",
        "",
        "### Trade book (input to MC)",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| Pooled trades | {r.get('n_trades', '—')} |",
        f"| Mean trade return | {_f((r.get('mean_trade_return') or 0) * 100, 6)}% |",
        f"| Historical terminal (compound order of book) | {_f(r.get('hist_terminal_mult'), 6)}× |",
        f"| Historical max DD | {_f((r.get('hist_max_dd') or 0) * 100, 4)}% |",
        "",
        "### Bootstrap Monte Carlo (with replacement)",
        "",
        "Resample the trade-return vector **with replacement**, same length, "
        f"**{meta.get('n_sims', 1000)}** paths. Terminal wealth starts at 1.0 and compounds trade returns.",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| Median terminal wealth | {_f(r.get('mc_median_terminal'), 6)}× |",
        f"| Mean terminal wealth | {_f(r.get('mc_mean_terminal'), 6)}× |",
        f"| p05 terminal | {_f(r.get('mc_p05_terminal'), 6)}× |",
        f"| p25 terminal | {_f(r.get('mc_p25_terminal'), 6)}× |",
        f"| p75 terminal | {_f(r.get('mc_p75_terminal'), 6)}× |",
        f"| p95 terminal | {_f(r.get('mc_p95_terminal'), 6)}× |",
        f"| P(loss) = P(terminal < 1) | {_pct(r.get('mc_prob_loss'))} |",
        f"| P(max DD ≥ 20%) | {_pct(r.get('mc_prob_ruin_20'))} |",
        f"| Median path max DD | {_f((r.get('mc_median_max_dd') or 0) * 100, 4)}% |",
        f"| p95 path max DD | {_f((r.get('mc_p95_max_dd') or 0) * 100, 4)}% |",
        "",
        "### Order-shuffle Monte Carlo (sequence risk)",
        "",
        "Same trades, **permute order** (no replacement). Isolates path dependence from trade *sequence*.",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| Shuffle median terminal | {_f(r.get('shuffle_median_terminal'), 6)}× |",
        f"| Shuffle p05 terminal | {_f(r.get('shuffle_p05_terminal'), 6)}× |",
        f"| Shuffle P(loss) | {_pct(r.get('shuffle_prob_loss'))} |",
        "",
        "### How to read",
        "",
        "- **MC med > 1**: more than half of bootstrap paths finish above start.",
        "- **P(loss) high + hist WR high**: hit rate may look good while resampled paths still lose — fragile edge / costs.",
        "- **Low trade count**: percentiles are less stable; treat extreme WR paths carefully.",
        "- Full table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)",
        "",
        f"**Notes:** {r.get('notes') or 'bootstrap with replacement + order shuffle'}",
        "",
        MC_END,
    ]
    return "\n".join(lines) + "\n"


def format_all_sim_block(
    fid: str,
    batch_r: dict | None,
    acc_r: dict | None,
    mc_r: dict | None,
    mc_rank: int | None,
    n_mc: int,
    meta_mc: dict,
    meta_acc: dict,
    meta_batch: dict,
) -> str:
    """Compact all-sims section for ranked READMEs (includes MC full detail)."""
    lines = [
        SIM_BEGIN,
        "## All simulation results (batch + accuracy + Monte Carlo)",
        "",
        f"**Family id:** `{fid}`  ",
        "**Not Court law.** Lab claims only.",
        "",
        "### 1) Full-batch strategy test (1:1 families)",
        "",
    ]
    if batch_r:
        lines += [
            "| Metric | Value |",
            "|--------|------:|",
            f"| Batch rank | {batch_r.get('rank', '—')} |",
            f"| Score | {_f(batch_r.get('score'), 4)} |",
            f"| Win rate % | {_f(batch_r.get('win_rate'), 4)} |",
            f"| Profit factor | {_f(batch_r.get('profit_factor'), 4)} |",
            f"| Total return % | {_f(batch_r.get('total_return'), 4)} |",
            f"| Max DD % | {_f(batch_r.get('max_drawdown'), 4)} |",
            f"| Trades | {batch_r.get('trades', '—')} |",
            f"| Sharpe | {_f(batch_r.get('sharpe'), 4)} |",
            f"| Sortino | {_f(batch_r.get('sortino'), 4)} |",
            f"| Calmar | {_f(batch_r.get('calmar'), 4)} |",
            f"| Profile | `{batch_r.get('profile', '—')}` |",
            f"| n_runs (sets×modes) | {batch_r.get('n_runs', '—')} |",
            "",
            f"Window: {meta_batch.get('window', '—')}  ",
            f"Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)",
            "",
        ]
    else:
        lines += ["_No batch ranking row for this family (e.g. sauce-only)._", ""]

    lines += [
        "### 2) Accuracy-tweak batch (WR > 60.4% gate)",
        "",
    ]
    if acc_r:
        lines += [
            "| Metric | Value |",
            "|--------|------:|",
            f"| Pass gate | {'YES' if acc_r.get('passed') else 'NO'} |",
            f"| Rank by WR | {acc_r.get('rank_by_win_rate', '—')} |",
            f"| Win rate % | {_f(acc_r.get('win_rate'), 4)} |",
            f"| Baseline WR % | {_f(acc_r.get('baseline_win_rate'), 4)} |",
            f"| Trades | {acc_r.get('trades', '—')} |",
            f"| Total return % | {_f(acc_r.get('total_return'), 4)} |",
            f"| Max DD % | {_f(acc_r.get('max_drawdown'), 4)} |",
            f"| Profit factor | {_f(acc_r.get('profit_factor'), 4)} |",
            f"| Sharpe | {_f(acc_r.get('sharpe'), 4)} |",
            f"| Score | {_f(acc_r.get('score'), 4)} |",
            f"| Tier | `{acc_r.get('tier', '—')}` |",
            f"| Profile | `{acc_r.get('profile', '—')}` |",
            "",
            f"Win bar: {meta_acc.get('win_bar')} · min trades: {meta_acc.get('min_trades')}  ",
            f"Window: {meta_acc.get('window', '—')}  ",
            f"Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/{fid}.md`](../tweaks/{fid}.md)",
            "",
        ]
        tp = acc_r.get("tier_params") or {}
        if tp:
            lines += [
                "Tier params:",
                "",
                "| Param | Value |",
                "|-------|------:|",
            ]
            for k, v in tp.items():
                lines.append(f"| {k} | {v} |")
            lines.append("")
    else:
        lines += ["_No accuracy-tweak row._", ""]

    lines += [
        "### 3) Monte Carlo (bootstrap + order-shuffle)",
        "",
    ]
    if mc_r:
        lines += [
            f"**MC rank:** **{mc_rank}** / {n_mc}",
            "",
            "| Metric | Value |",
            "|--------|------:|",
            f"| Pooled trades | {mc_r.get('n_trades', '—')} |",
            f"| Mean trade return | {_f((mc_r.get('mean_trade_return') or 0) * 100, 6)}% |",
            f"| Hist terminal | {_f(mc_r.get('hist_terminal_mult'), 6)}× |",
            f"| Hist max DD | {_f((mc_r.get('hist_max_dd') or 0) * 100, 4)}% |",
            f"| MC median terminal | {_f(mc_r.get('mc_median_terminal'), 6)}× |",
            f"| MC mean terminal | {_f(mc_r.get('mc_mean_terminal'), 6)}× |",
            f"| MC p05 / p95 | {_f(mc_r.get('mc_p05_terminal'), 6)}× / {_f(mc_r.get('mc_p95_terminal'), 6)}× |",
            f"| P(loss) | {_pct(mc_r.get('mc_prob_loss'))} |",
            f"| P(DD ≥ 20%) | {_pct(mc_r.get('mc_prob_ruin_20'))} |",
            f"| Median path max DD | {_f((mc_r.get('mc_median_max_dd') or 0) * 100, 4)}% |",
            f"| Shuffle median terminal | {_f(mc_r.get('shuffle_median_terminal'), 6)}× |",
            f"| Shuffle P(loss) | {_pct(mc_r.get('shuffle_prob_loss'))} |",
            "",
            f"Sims: {meta_mc.get('n_sims', 1000)} · seed: {meta_mc.get('seed', 42)} · window: {meta_mc.get('window', '—')}  ",
            f"Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)",
            "",
        ]
    else:
        lines += ["_No Monte Carlo row for this family._", ""]

    lines += [SIM_END]
    return "\n".join(lines) + "\n"


def upsert_block(text: str, begin: str, end: str, block: str) -> str:
    replacement = block.rstrip("\n")
    if begin in text and end in text:
        pat = re.compile(
            re.escape(begin) + r".*?" + re.escape(end),
            re.DOTALL,
        )
        # lambda avoids re.sub treating backslashes in Windows paths as escapes
        return pat.sub(lambda _m: replacement, text)
    # append
    body = text.rstrip() + "\n\n" + replacement + "\n"
    return body


def family_from_ranked_dir(name: str) -> str:
    # 001_mt__cci_gravity_scalp_ftmo -> mt__cci_gravity_scalp_ftmo
    m = re.match(r"^\d+_(.+)$", name)
    return m.group(1) if m else name


def main():
    mc_by, mc_rank, acc_by, batch_by, meta_mc, meta_acc, meta_batch, n_mc = load_indexes()

    stats = {
        "tweaks_mc": 0,
        "tweaks_missing_mc": [],
        "ranked_sim": 0,
        "ranked_missing_mc": [],
        "sauces_mc": 0,
    }

    # --- tweaks: ensure MC block present ---
    for p in sorted(TWEAKS.glob("*.md")):
        fid = p.stem
        r = mc_by.get(fid)
        if not r:
            stats["tweaks_missing_mc"].append(fid)
            continue
        block = format_mc_block(fid, r, mc_rank[fid], n_mc, meta_mc)
        text = p.read_text(encoding="utf-8")
        p.write_text(upsert_block(text, MC_BEGIN, MC_END, block), encoding="utf-8")
        stats["tweaks_mc"] += 1

    # --- sauces notes ---
    sauce_map = {
        "H001_mcflurry_eddy_scalp.md": "sauce__mcflurry_eddy_scalp",
        "DimensionJump_sauce.md": "sauce__dimension_jump",
    }
    for fname, fid in sauce_map.items():
        p = SAUCES / fname
        if not p.exists():
            continue
        r = mc_by.get(fid)
        if not r:
            continue
        block = format_mc_block(fid, r, mc_rank[fid], n_mc, meta_mc)
        text = p.read_text(encoding="utf-8")
        p.write_text(upsert_block(text, MC_BEGIN, MC_END, block), encoding="utf-8")
        stats["sauces_mc"] += 1

    # --- ranked READMEs: full all-sims block ---
    for d in sorted(RANKED.iterdir()):
        if not d.is_dir():
            continue
        readme = d / "README.md"
        if not readme.exists():
            continue
        fid = family_from_ranked_dir(d.name)
        batch_r = batch_by.get(fid)
        acc_r = acc_by.get(fid)
        mc_r = mc_by.get(fid)
        if not mc_r:
            stats["ranked_missing_mc"].append(fid)
        block = format_all_sim_block(
            fid,
            batch_r,
            acc_r,
            mc_r,
            mc_rank.get(fid),
            n_mc,
            meta_mc,
            meta_acc,
            meta_batch,
        )
        text = readme.read_text(encoding="utf-8")
        readme.write_text(upsert_block(text, SIM_BEGIN, SIM_END, block), encoding="utf-8")
        stats["ranked_sim"] += 1

    # write summary
    out = STRATEGIES / "SIM_RESULTS_INJECT_REPORT.md"
    lines = [
        "# Simulation results inject report",
        "",
        f"- Monte Carlo families: **{n_mc}** (from `MONTE_CARLO_RESULTS.json`)",
        f"- Tweaks with MC block: **{stats['tweaks_mc']}**",
        f"- Tweaks missing MC row: **{len(stats['tweaks_missing_mc'])}**"
        + (f" — {stats['tweaks_missing_mc']}" if stats["tweaks_missing_mc"] else ""),
        f"- Sauces with MC block: **{stats['sauces_mc']}**",
        f"- Ranked READMEs with all-sim block: **{stats['ranked_sim']}**",
        f"- Ranked missing MC row: **{len(stats['ranked_missing_mc'])}**"
        + (f" — {stats['ranked_missing_mc']}" if stats["ranked_missing_mc"] else ""),
        "",
        "Sources: `STRATEGY_TEST_REPORT.json`, `TWEAKED_ACCURACY_RESULTS.json`, `MONTE_CARLO_RESULTS.json`",
        "",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(stats, indent=2))
    print("wrote", out)


if __name__ == "__main__":
    main()
