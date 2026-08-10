"""
Full prove pipeline for the 14 strategies from:
  strategies/Strategies to replicate in Algo Trading.docx.html
  → language notes in strategies/algo_guide_14/

Follows strategies/LLM_INSTRUCTIONS.md gates for these families only,
then merges into the shared report JSONs and injects per-file results.

Usage (from repo root):
  python -m strategies.python_batch.run_prove_guide14
  python -m strategies.python_batch.run_prove_guide14 --sims 1000 --seed 42
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from strategies.python_batch.inventory_1to1 import (  # noqa: E402
    build_inventory,
    inventory_counts,
    to_jsonable,
)
from strategies.python_batch.mtf import OFFICIAL_SETS, build_all_sets, load_mt5_csv  # noqa: E402
from strategies.python_batch.run_monte_carlo import (  # noqa: E402
    build_family_list,
    run_one_family,
    write_report as write_mc_report,
)
from strategies.python_batch.run_strategy_batch_1to1 import (  # noqa: E402
    aggregate,
    reorganize,
    run_one,
    write_report as write_batch_report,
)
from strategies.python_batch.run_tweak_batch import (  # noqa: E402
    MIN_TRADES,
    TIERS,
    WIN_BAR,
    load_baselines,
    pick_tier,
    write_family_doc,
)
from strategies.python_batch.inject_all_sim_results import main as inject_main  # noqa: E402

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
GUIDE_PREFIX = "note__algo_guide_14"
TAIL = 40_000
PROVE_MD = STRATEGIES / "ALGO_GUIDE_14_PROVE_REPORT.md"


def is_guide(fid: str) -> bool:
    return GUIDE_PREFIX in fid or fid.startswith("note__algo_guide_14")


def filter_guide_specs(specs):
    return [s for s in specs if is_guide(s.family_id)]


def merge_ranking(existing: List[dict], new_rows: List[dict]) -> List[dict]:
    by = {r["family_id"]: r for r in existing}
    for r in new_rows:
        by[r["family_id"]] = r
    ranking = list(by.values())
    ranking.sort(key=lambda r: (r.get("score", -1e9), r.get("profit_factor", 0), r.get("total_return", 0)), reverse=True)
    for i, r in enumerate(ranking, 1):
        r["rank"] = i
    return ranking


def merge_results_list(existing: List[dict], new_rows: List[dict], key: str = "family_id") -> List[dict]:
    by = {r[key]: r for r in existing}
    for r in new_rows:
        by[r[key]] = r
    return list(by.values())


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sims", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--tail", type=int, default=TAIL)
    ap.add_argument("--skip-baseline", action="store_true")
    ap.add_argument("--skip-tweak", action="store_true")
    ap.add_argument("--skip-mc", action="store_true")
    ap.add_argument("--skip-inject", action="store_true")
    args = ap.parse_args(argv)

    # --- inventory ---
    specs_all = build_inventory()
    counts = inventory_counts(specs_all)
    inv_path = STRATEGIES / "FAMILY_INVENTORY_1TO1.json"
    inv_path.write_text(
        json.dumps({"counts": counts, "families": to_jsonable(specs_all)}, indent=2),
        encoding="utf-8",
    )
    guide_specs = filter_guide_specs(specs_all)
    print("Inventory total:", counts["total_families"], "guide14:", len(guide_specs))
    if len(guide_specs) != 14:
        print("WARN expected 14 guide families, got", len(guide_specs))
        for s in guide_specs:
            print(" ", s.family_id, s.adapter_profile)

    data_path = DEFAULT_DATA if DEFAULT_DATA.exists() else ALT_DATA
    if not data_path.exists():
        print("No OHLCV data", file=sys.stderr)
        return 2
    print(f"Loading {data_path} tail={args.tail}")
    m1 = load_mt5_csv(data_path, tail_bars=args.tail)
    window = f"{m1.index[0]} → {m1.index[-1]} ({len(m1)} M1)"
    print("Window", window)
    sets = build_all_sets(m1)
    vbt_version = getattr(vbt, "__version__", "?")
    symbol = data_path.stem.split("_")[0]

    prove_lines = [
        "# Algo Guide 14 — prove report",
        "",
        f"**Source HTML:** `strategies/Strategies to replicate in Algo Trading.docx.html`",
        f"**Notes:** `strategies/algo_guide_14/`",
        f"**Window:** {window}",
        f"**Data:** `{data_path}`",
        f"**vectorbt:** {vbt_version}",
        f"**Families proven this run:** {len(guide_specs)}",
        f"**Not Court law.**",
        "",
    ]

    # --- baseline ---
    ranking_new: List[dict] = []
    if not args.skip_baseline:
        print("=== BASELINE BATCH (guide14) ===")
        all_rows = []
        for i, spec in enumerate(guide_specs, 1):
            print(f"[base {i}/{len(guide_specs)}] {spec.family_id} profile={spec.adapter_profile}")
            fam_rows = []
            for set_name, sb in sets.items():
                for mode in ("pullback", "continuation"):
                    row = run_one(spec, sb, mode)
                    fam_rows.append(row)
                    all_rows.append(row)
                    if row.error:
                        print(f"  ERR {set_name} {mode}: {row.error[:100]}")
            agg = aggregate(fam_rows)
            ranking_new.append(
                {
                    "family_id": spec.family_id,
                    "title": spec.title,
                    "kind": spec.kind,
                    "profile": spec.adapter_profile,
                    "source": spec.source,
                    **agg,
                }
            )

        report_json = STRATEGIES / "STRATEGY_TEST_REPORT.json"
        report_md = STRATEGIES / "STRATEGY_TEST_REPORT.md"
        if report_json.exists():
            payload = json.loads(report_json.read_text(encoding="utf-8"))
            existing_rank = payload.get("ranking", [])
            existing_rows = payload.get("rows", [])
        else:
            payload = {
                "mode": "1to1_no_collapse",
                "counts": counts,
                "symbol": symbol,
                "data_path": str(data_path),
                "window": window,
                "vectorbt": vbt_version,
                "sets": list(OFFICIAL_SETS.keys()),
                "modes": ["pullback", "continuation"],
                "missing_all_error": [],
                "ranking": [],
                "rows": [],
            }
            existing_rank, existing_rows = [], []

        # drop old guide rows then merge
        existing_rank = [r for r in existing_rank if not is_guide(r["family_id"])]
        existing_rows = [r for r in existing_rows if not is_guide(r.get("family_id", ""))]
        ranking = merge_ranking(existing_rank, ranking_new)
        # Full ranked/ folders need a FamilySpec for every ranking row.
        # Specs for non-guide rows come from inventory; guide from guide_specs.
        reorganize(ranking, specs_all)

        new_row_dicts = [asdict(r) for r in all_rows]
        payload["ranking"] = ranking
        payload["rows"] = existing_rows + new_row_dicts
        payload["counts"] = counts
        payload["window"] = window
        payload["data_path"] = str(data_path)
        payload["vectorbt"] = vbt_version
        report_json.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        # Keep MD report from prior full batch if present; ranking JSON is SSOT.
        # Still refresh ranked/INDEX via reorganize above.
        print("Wrote", report_json, "ranking n=", len(ranking))
        prove_lines += ["## Baseline", "", "| Family | Score | WR% | PF | Trades |", "|--------|------:|----:|---:|-------:|"]
        for r in sorted(ranking_new, key=lambda x: -x["score"]):
            prove_lines.append(
                f"| `{r['family_id']}` | {r['score']:.2f} | {r['win_rate']:.2f} | "
                f"{r['profit_factor']:.3f} | {r['trades']} |"
            )
        prove_lines.append("")

    # --- accuracy tweaks ---
    tweak_results: List[dict] = []
    if not args.skip_tweak:
        print("=== ACCURACY TWEAKS (guide14) ===")
        baselines = load_baselines()
        failures = []
        for i, spec in enumerate(guide_specs, 1):
            fid = spec.family_id
            print(f"[tweak {i}/{len(guide_specs)}] {fid}")
            tier, rows, agg = pick_tier(fid, spec.adapter_profile, sets, adapter_fn=None)
            base_wr = baselines.get(fid, 0.0)
            extra = (
                f"Guide strategy from Strategies-to-replicate HTML. "
                f"Profile `{spec.adapter_profile}` under lab shell."
            )
            doc = write_family_doc(
                fid,
                spec.title,
                spec.kind,
                spec.source,
                spec.adapter_profile,
                tier,
                base_wr,
                agg,
                extra,
            )
            rec = {
                "family_id": fid,
                "title": spec.title,
                "kind": spec.kind,
                "profile": spec.adapter_profile,
                "source": spec.source,
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
            tweak_results.append(rec)
            status = "PASS" if rec["passed"] else "FAIL"
            print(f"  {status} wr={agg['win_rate']:.2f} tr={agg['trades']} tier={tier['name']}")
            if not rec["passed"]:
                failures.append(fid)

        out_json = STRATEGIES / "TWEAKED_ACCURACY_RESULTS.json"
        if out_json.exists():
            old = json.loads(out_json.read_text(encoding="utf-8"))
            old_results = [r for r in old.get("results", []) if not is_guide(r["family_id"])]
        else:
            old = {}
            old_results = []
        merged = old_results + tweak_results
        merged.sort(key=lambda r: r["win_rate"], reverse=True)
        for i, r in enumerate(merged, 1):
            r["rank_by_win_rate"] = i
        fails_all = [r["family_id"] for r in merged if not r["passed"]]
        payload = {
            "win_bar": WIN_BAR,
            "min_trades": MIN_TRADES,
            "window": window,
            "data_path": str(data_path),
            "vectorbt": vbt_version,
            "sets": list(OFFICIAL_SETS.keys()),
            "modes": ["pullback", "continuation"],
            "family_count": len(merged),
            "pass_count": sum(1 for r in merged if r["passed"]),
            "fail_count": len(fails_all),
            "failures": fails_all,
            "min_win_rate": min((r["win_rate"] for r in merged), default=0.0),
            "max_win_rate": max((r["win_rate"] for r in merged), default=0.0),
            "results": merged,
            "guide14_failures": failures,
        }
        out_json.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        # rewrite summary MD
        lines = [
            "# Tweaked accuracy report — beat 60.4% win rate",
            "",
            f"**Win-rate gate:** `>` **{WIN_BAR}%** with **≥ {MIN_TRADES}** trades.",
            f"**Window:** {window}",
            f"**Families:** {payload['family_count']} · **Pass:** {payload['pass_count']} · **Fail:** {payload['fail_count']}",
            f"**Min / max win rate:** {payload['min_win_rate']:.2f}% / {payload['max_win_rate']:.2f}%",
            "",
            "| Rank | Family | Baseline WR% | Post WR% | Trades | Tier | Pass |",
            "|-----:|--------|-------------:|---------:|-------:|------|:----:|",
        ]
        for r in merged:
            lines.append(
                f"| {r['rank_by_win_rate']} | `{r['family_id']}` | {r['baseline_win_rate']:.2f} | "
                f"{r['win_rate']:.2f} | {r['trades']} | {r['tier']} | {'Y' if r['passed'] else 'N'} |"
            )
        lines += ["", "## Failures", ""]
        if fails_all:
            for f in fails_all:
                lines.append(f"- `{f}`")
        else:
            lines.append("- None")
        (STRATEGIES / "TWEAKED_ACCURACY_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
        print("pass guide14", sum(1 for r in tweak_results if r["passed"]), "/", len(tweak_results))
        prove_lines += [
            "## Accuracy tweaks (WR > 60.4%)",
            "",
            "| Family | WR% | Trades | Tier | Pass |",
            "|--------|----:|-------:|------|:----:|",
        ]
        for r in tweak_results:
            prove_lines.append(
                f"| `{r['family_id']}` | {r['win_rate']:.2f} | {r['trades']} | {r['tier']} | "
                f"{'Y' if r['passed'] else 'N'} |"
            )
        prove_lines.append("")

    # --- Monte Carlo ---
    if not args.skip_mc:
        print("=== MONTE CARLO (guide14) ===")
        all_fams = build_family_list()
        guide_fams = [f for f in all_fams if is_guide(f["family_id"])]
        rng = np.random.default_rng(args.seed)
        mc_new = []
        for i, spec in enumerate(guide_fams, 1):
            print(f"[mc {i}/{len(guide_fams)}] {spec['family_id']}")
            r = run_one_family(spec, sets, args.sims, rng)
            mc_new.append(asdict(r))
            print(
                f"  tr={r.n_trades} mc_med={r.mc_median_terminal:.4f} "
                f"p_loss={r.mc_prob_loss*100:.1f}%"
            )

        mc_json = STRATEGIES / "MONTE_CARLO_RESULTS.json"
        if mc_json.exists():
            old_mc = json.loads(mc_json.read_text(encoding="utf-8"))
            old_res = [r for r in old_mc.get("results", []) if not is_guide(r["family_id"])]
            meta = old_mc.get("meta", {})
        else:
            old_res = []
            meta = {}
        meta.update(
            {
                "window": window,
                "data_path": str(data_path),
                "n_sims": args.sims,
                "seed": args.seed,
                "tp_stop": 0.00025,
                "sl_stop": 0.001,
                "sets": list(OFFICIAL_SETS.keys()),
                "modes": ["pullback", "continuation"],
                "vectorbt": vbt_version,
            }
        )
        merged_mc = old_res + mc_new
        meta["n_families"] = len(merged_mc)
        mc_json.write_text(
            json.dumps({"meta": meta, "results": merged_mc}, indent=2, default=str),
            encoding="utf-8",
        )
        # rebuild MC report from merged
        from strategies.python_batch.run_monte_carlo import MCResult

        fields = set(MCResult.__dataclass_fields__)
        mc_objs = []
        for r in merged_mc:
            kwargs = {k: r.get(k) for k in fields}
            # defaults for optional
            kwargs.setdefault("notes", "")
            kwargs.setdefault("error", "")
            mc_objs.append(MCResult(**kwargs))
        write_mc_report(mc_objs, meta)
        print("Wrote MC", len(merged_mc), "families")
        prove_lines += [
            "## Monte Carlo",
            "",
            f"Sims={args.sims} seed={args.seed}",
            "",
            "| Family | Trades | MC med | P(loss) |",
            "|--------|-------:|-------:|--------:|",
        ]
        for r in mc_new:
            prove_lines.append(
                f"| `{r['family_id']}` | {r['n_trades']} | {r['mc_median_terminal']:.4f} | "
                f"{r['mc_prob_loss']*100:.1f}% |"
            )
        prove_lines.append("")

    # --- inject ---
    if not args.skip_inject:
        print("=== INJECT SIM RESULTS ===")
        inject_main()

    # checklist per family
    prove_lines += ["## Gate checklist (guide14)", ""]
    inv_ids = {s.family_id for s in guide_specs}
    tweak_by = {r["family_id"]: r for r in tweak_results} if tweak_results else {}
    mc_path = STRATEGIES / "MONTE_CARLO_RESULTS.json"
    mc_by = {}
    if mc_path.exists():
        for r in json.loads(mc_path.read_text(encoding="utf-8")).get("results", []):
            if is_guide(r["family_id"]):
                mc_by[r["family_id"]] = r
    for fid in sorted(inv_ids):
        tw = STRATEGIES / "tweaks" / f"{fid}.md"
        has_mc_block = tw.exists() and "MONTE_CARLO_BEGIN" in tw.read_text(encoding="utf-8")
        t = tweak_by.get(fid)
        m = mc_by.get(fid)
        g_wr = bool(t and t.get("passed"))
        g_mc = bool(m and m.get("n_trades", 0) > 0)
        prove_lines.append(
            f"- `{fid}`: INV=Y · TWEAK_FILE={'Y' if tw.exists() else 'N'} · "
            f"WR_GATE={'Y' if g_wr else 'N'} · MC={'Y' if g_mc else 'N'} · "
            f"MC_INJECT={'Y' if has_mc_block else 'N'}"
        )

    PROVE_MD.write_text("\n".join(prove_lines) + "\n", encoding="utf-8")
    print("Wrote", PROVE_MD)
    fails = [r["family_id"] for r in tweak_results if not r.get("passed")] if tweak_results else []
    if fails:
        print("GUIDE14 WR FAILS:", fails)
        return 2
    print("GUIDE14 prove complete — all WR gates passed (or tweak skipped).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
