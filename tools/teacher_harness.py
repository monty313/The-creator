"""TEACHER HARNESS — one lane per teacher agent, so we don't get lost.

Pipeline per agent (isolated, never stacked, champion never touched):
  1. HARVEST  lessons from real path states (traced replay of the frozen
              champion) on a window that PRECEDES the measurement window
  2. TRAIN    one candidate from a champion copy with that ONE lesson
  3. MEASURE  the same pinned 40d sensor every time (seed 42, XAU)
  4. VERDICT  owner bar only: hits vs king at breach 0
  5. RECORD   per-agent RESULT.json + one SCOREBOARD (json+md) + ledger event

Verdicts:
  CANDIDATE_FOR_COURT  hits > king and breach == 0  (promotion needs Full Court)
  KEEP_LAB             hits == king and breach == 0
  DISCARD              hits < king or breach > 0

Usage:
  python tools/teacher_harness.py                 # all agents
  python tools/teacher_harness.py --agent size_until_win
  python tools/teacher_harness.py --harvest-days 60 --measure-days 40
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np

from evidence_court.meta_rl.edge import build_tf_cache
from evidence_court.meta_rl.forward_eval import (
    DEFAULT_RISK_GRID,
    DEFAULT_TARGET_GRID,
    run_forward_eval,
)
from evidence_court.meta_rl.policy import load_or_train_champion
from evidence_court.meta_rl.price_io import (
    SYMBOL_FILES,
    bars_to_daily,
    load_m1_trailing_calendar_days,
)
from evidence_court.meta_rl.teacher_agents import (
    AGENT_REGISTRY,
    get_agent,
    replay_traced_days,
    train_candidate,
)

OUT_DIR = _ROOT / "evidence_court" / "artifacts" / "teacher_harness"
LEDGER = _ROOT / "evidence_court" / "ledger" / "EVIDENCE_LEDGER.jsonl"
WARMUP = 15


def windows(symbol: str, harvest_days: int, measure_days: int, seed: int):
    """Harvest window strictly precedes the measurement window (no leakage)."""
    p = SYMBOL_FILES.get(symbol)
    if p is None or not p.exists():
        raise SystemExit(f"no data for {symbol} — run tools/download_dukascopy_m1.py")
    m1 = load_m1_trailing_calendar_days(p, n_days=400)
    all_dates = [d["date"] for d in bars_to_daily(m1)]
    n_meas = measure_days + WARMUP
    measure_dates = all_dates[-n_meas:][WARMUP:]
    harvest_dates = all_dates[-(n_meas + harvest_days):-n_meas]
    assert not (set(harvest_dates) & set(measure_dates)), "window leakage"
    rng = np.random.default_rng(seed + 1000)  # independent pair draw for harvest
    harvest_pairs = [
        (float(rng.choice(DEFAULT_TARGET_GRID)), float(rng.choice(DEFAULT_RISK_GRID)))
        for _ in harvest_dates
    ]
    return m1, harvest_dates, harvest_pairs, measure_dates


def measure_candidate(npz_path: Path, *, days: int, seed: int, symbol: str) -> dict:
    report = run_forward_eval(
        n_days=days, seed=seed, symbols=[symbol], champion_path=npz_path
    )
    gc = report.metadata.get("goal_consistency") or {}
    tr = [d.n_trades for d in report.day_results]
    return {
        "hits": int(gc.get("total_hits", 0)),
        "breach": int(report.breach_count),
        "no_retrain": bool(report.no_retrain),
        "mean_pnl": round(
            float(np.mean([d.pnl_percent for d in report.day_results])), 4
        ),
        "mean_trades": round(float(np.mean(tr)), 2),
        "a13_frac": round(sum(1 for n in tr if 8 <= n <= 400) / max(len(tr), 1), 3),
        "n_zero": sum(1 for n in tr if n == 0),
        "window": f"{report.metadata.get('window_start')}..{report.metadata.get('window_end')}",
        "fingerprint": report.metadata.get("policy_fingerprint"),
    }


def verdict(m: dict, king_hits: int) -> str:
    if m["breach"] > 0 or not m["no_retrain"]:
        return "DISCARD"
    if m["hits"] > king_hits:
        return "CANDIDATE_FOR_COURT"
    if m["hits"] == king_hits:
        return "KEEP_LAB"
    return "DISCARD"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--agent", type=str, default="all")
    ap.add_argument("--symbol", type=str, default="XAUUSD")
    ap.add_argument("--harvest-days", type=int, default=60)
    ap.add_argument("--measure-days", type=int, default=40)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--king-hits", type=int, default=1, help="live king hits on this sensor")
    ap.add_argument("--no-ledger", action="store_true")
    args = ap.parse_args(argv)

    agents = AGENT_REGISTRY if args.agent == "all" else [get_agent(args.agent)]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[harness] harvest window: {args.harvest_days}d before the {args.measure_days}d sensor")
    m1, h_dates, h_pairs, m_dates = windows(
        args.symbol, args.harvest_days, args.measure_days, args.seed
    )
    print(f"[harness] harvest {h_dates[0]}..{h_dates[-1]}  |  measure {m_dates[0]}..{m_dates[-1]}")

    champion = load_or_train_champion()
    champion.assert_frozen()
    cache = build_tf_cache(m1)
    print(f"[harness] tracing {len(h_dates)} harvest days on frozen champion...")
    days = replay_traced_days(
        champion,
        symbol=args.symbol,
        m1=m1,
        dates=h_dates,
        pairs=h_pairs,
        tf_cache=cache,
    )
    n_dec = sum(len([t for t in d["trace"] if "brain" in t]) for d in days)
    print(f"[harness] {n_dec} decision states harvested")

    rows = []
    for agent in agents:
        print(f"\n[{agent.name}] {agent.lesson}")
        lessons = agent.harvest(days)
        print(f"[{agent.name}] lessons: {len(lessons)}")
        result_dir = OUT_DIR / agent.name
        result_dir.mkdir(parents=True, exist_ok=True)
        if not lessons:
            row = {"agent": agent.name, "lesson": agent.lesson, "n_lessons": 0,
                   "verdict": "NO_LESSONS"}
            (result_dir / "RESULT.json").write_text(json.dumps(row, indent=2))
            rows.append(row)
            continue
        train_rep = train_candidate(agent, lessons, seed=args.seed)
        print(
            f"[{agent.name}] trained: agreement act "
            f"{train_rep['agreement_before']['act_agreement']}→"
            f"{train_rep['agreement_after']['act_agreement']} · size_mae "
            f"{train_rep['agreement_before']['size_mae']}→{train_rep['agreement_after']['size_mae']}"
        )
        meas = measure_candidate(
            Path(train_rep["saved"]), days=args.measure_days, seed=args.seed,
            symbol=args.symbol,
        )
        v = verdict(meas, args.king_hits)
        print(
            f"[{agent.name}] MEASURED hits={meas['hits']} (king {args.king_hits}) "
            f"breach={meas['breach']} mean_pnl={meas['mean_pnl']:+.3f} "
            f"tr/day={meas['mean_trades']} → {v}"
        )
        row = {
            "agent": agent.name,
            "lesson": agent.lesson,
            "mode": agent.mode,
            "n_lessons": len(lessons),
            "train": {k: train_rep[k] for k in (
                "agreement_before", "agreement_after", "fingerprint_after", "saved")},
            "measure": meas,
            "verdict": v,
        }
        (result_dir / "RESULT.json").write_text(json.dumps(row, indent=2))
        rows.append(row)

    # ------------------------------------------------------------- scoreboard
    board = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "protocol": f"forward{args.measure_days}_random_seed{args.seed}_{args.symbol}",
        "harvest_window": f"{h_dates[0]}..{h_dates[-1]}",
        "measure_window": f"{m_dates[0]}..{m_dates[-1]}",
        "king": {"hits": args.king_hits, "fingerprint": champion.weight_fingerprint()},
        "rows": rows,
        "install_rule": "hits > king at breach 0 → Full Court case; harness never installs",
    }
    (OUT_DIR / "SCOREBOARD.json").write_text(json.dumps(board, indent=2))
    md = ["# Teacher harness scoreboard", "",
          f"Protocol `{board['protocol']}` · harvest `{board['harvest_window']}` · king hits **{args.king_hits}**", "",
          "| agent | lesson | lessons | hits | breach | mean pnl | tr/day | verdict |",
          "|---|---|---:|---:|---:|---:|---:|---|"]
    for r in rows:
        m = r.get("measure") or {}
        md.append(
            f"| {r['agent']} | {r['lesson'][:60]} | {r['n_lessons']} | "
            f"{m.get('hits','—')} | {m.get('breach','—')} | {m.get('mean_pnl','—')} | "
            f"{m.get('mean_trades','—')} | **{r['verdict']}** |"
        )
    (OUT_DIR / "SCOREBOARD.md").write_text("\n".join(md) + "\n")
    print(f"\n[harness] scoreboard → {OUT_DIR/'SCOREBOARD.md'}")

    if not args.no_ledger:
        event = {
            "ts": board["ts"],
            "event": "TEACHER_HARNESS_CYCLE",
            "goal_axes": ["G-CLEAR", "G-BREACH0", "G-A13", "G-TRAIN"],
            "protocol": board["protocol"],
            "harvest_window": board["harvest_window"],
            "king_hits": args.king_hits,
            "agents": [
                {"agent": r["agent"], "n_lessons": r["n_lessons"],
                 "hits": (r.get("measure") or {}).get("hits"),
                 "breach": (r.get("measure") or {}).get("breach"),
                 "mean_pnl": (r.get("measure") or {}).get("mean_pnl"),
                 "verdict": r["verdict"]}
                for r in rows
            ],
            "law": "one lesson per agent; one measure per candidate; no install without Court",
        }
        with LEDGER.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
        print("[harness] ledger event appended")
    return 0


if __name__ == "__main__":
    sys.exit(main())
