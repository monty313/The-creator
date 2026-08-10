"""Fair-ish head-to-head: PROVEN (the-truth) vs Court CASE-0037 champion.

Same SCORE DEFINITION (Mark GOAL language):
  clear  = day PnL >= target  AND  not breach
  breach = day loss exceeds risk floor (worst-case / risk hit)
  green  = day PnL > 0

Same RUNTIME PAIR(s) (default yardstick 3.0 / 3.5 + Court-ish 15 / 2).

Engines stay native (cannot load PROVEN weights into MetaBrain):
  PROVEN → the-truth FastSim + prove path (XAUUSD curriculum)
  Court  → goal_path MultiBrain on same calendar dates when possible

Outputs JSON report under evidence_court/artifacts/.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

CREATOR_ROOT = Path(__file__).resolve().parents[2]
TRUTH_ROOT = Path(r"C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\the-truth")
DEFAULT_OUT = CREATOR_ROOT / "evidence_court" / "artifacts" / "fair_policy_showdown.json"
PROVEN_NAME = "PROVEN_SPRINT_row04_clear24_2026-07-20"
COURT_CHAMP = CREATOR_ROOT / "evidence_court" / "artifacts" / "meta_policy_champion.npz"


def _run_proven_prove_it(target: float, risk: float) -> Dict[str, Any]:
    """Run the-truth prove_it; parse scoreboard printout."""
    script = TRUTH_ROOT / "scripts" / "prove_it.py"
    if not script.exists():
        return {"error": f"missing {script}"}
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [
            str(TRUTH_ROOT),
            str(TRUTH_ROOT / "code"),
            str(TRUTH_ROOT / "src"),
            env.get("PYTHONPATH", ""),
        ]
    )
    cmd = [
        sys.executable,
        str(script),
        PROVEN_NAME,
        str(target),
        str(risk),
    ]
    proc = subprocess.run(
        cmd,
        cwd=str(TRUTH_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=3600,
    )
    text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    out: Dict[str, Any] = {
        "engine": "the-truth FastSim prove_it",
        "brain": PROVEN_NAME,
        "target": float(target),
        "risk": float(risk),
        "returncode": proc.returncode,
        "raw_tail": text[-2500:],
    }
    if proc.returncode != 0:
        out["error"] = "prove_it_failed"
        return out

    def _pct(label: str) -> Optional[float]:
        m = re.search(label + r".*?([0-9]+)\s*%%", text)
        if m:
            return float(m.group(1)) / 100.0
        return None

    m_days = re.search(r"\|\s*(\d+)\s*real trading days", text)
    m_clear = re.search(r"cleared.*?([0-9]+)\s*%\s*of days", text, re.I)
    m_breach = re.search(r"breached.*?([0-9]+)\s*%\s*of days", text, re.I)
    m_avg = re.search(r"average day result:\s*([+\-0-9.]+)\s*%", text, re.I)
    m_med = re.search(r"median day result:\s*([+\-0-9.]+)\s*%", text, re.I)
    m_green = re.search(r"green days.*?([0-9]+)\s*%\s*of days", text, re.I)
    m_best = re.search(r"best / worst day:\s*([+\-0-9.]+)\s*%\s*/\s*([+\-0-9.]+)\s*%", text, re.I)
    m_streak = re.search(r"longest cleared streak.*?(\d+)\s*days", text, re.I)

    n_days = int(m_days.group(1)) if m_days else None
    clear = float(m_clear.group(1)) / 100.0 if m_clear else None
    breach = float(m_breach.group(1)) / 100.0 if m_breach else None
    out.update(
        {
            "n_days": n_days,
            "clear_rate": clear,
            "breach_rate": breach,
            "mean_pnl_pct": float(m_avg.group(1)) if m_avg else None,
            "median_pnl_pct": float(m_med.group(1)) if m_med else None,
            "green_frac": float(m_green.group(1)) / 100.0 if m_green else None,
            "max_pnl_pct": float(m_best.group(1)) if m_best else None,
            "min_pnl_pct": float(m_best.group(2)) if m_best else None,
            "longest_clear_streak": int(m_streak.group(1)) if m_streak else None,
            "symbol": "XAUUSD",
            "multi_symbol": False,
        }
    )
    return out


def _run_court_fixed_pair(
    *,
    target: float,
    risk: float,
    n_days: int,
    seed: int = 42,
    symbols: Optional[Sequence[str]] = None,
    champion_path: Path = COURT_CHAMP,
    monty_htf_blend: bool = False,
) -> Dict[str, Any]:
    """Court goal_path dual at ONE fixed target/risk (Mark score definition)."""
    # Import Court stack from Creator root
    if str(CREATOR_ROOT) not in sys.path:
        sys.path.insert(0, str(CREATOR_ROOT))

    from evidence_court.meta_rl.edge import build_tf_cache
    from evidence_court.meta_rl.goal_path import run_goal_path_day
    from evidence_court.meta_rl.policy import load_or_train_champion
    from evidence_court.meta_rl.price_io import (
        SYMBOL_FILES,
        available_symbols,
        bars_to_daily,
        load_m1_trailing_calendar_days,
    )

    syms = list(symbols) if symbols else [
        s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()
    ]
    # Prefer XAU-only arm for closer match to PROVEN curriculum
    if "XAUUSD" in available_symbols() and symbols is None:
        # dual arms: multi will be separate call
        pass

    pol = load_or_train_champion(
        path=champion_path if champion_path.exists() else None,
        seed=seed,
        n_steps=2500,
    )
    pol.assert_frozen()

    warmup = 12
    trail = int(n_days) + warmup + 8
    m1_by_sym: Dict[str, list] = {}
    daily_by_sym: Dict[str, list] = {}
    for sym in syms:
        path = SYMBOL_FILES.get(sym)
        if path is None or not path.exists():
            continue
        m1 = load_m1_trailing_calendar_days(path, n_days=trail)
        if m1:
            m1_by_sym[sym] = m1
            daily_by_sym[sym] = bars_to_daily(m1)

    if not m1_by_sym:
        return {"error": "no_price", "engine": "court goal_path"}

    date_sets = [set(d["date"] for d in days) for days in daily_by_sym.values()]
    common = sorted(set.intersection(*date_sets)) if len(date_sets) > 1 else sorted(next(iter(date_sets)))
    need = int(n_days) + warmup
    window = common[-need:] if len(common) >= need else common
    eval_dates = window[warmup:] if len(window) > warmup else window[1:]
    eval_dates = eval_dates[-int(n_days) :]

    tf_cache = {s: build_tf_cache(m) for s, m in m1_by_sym.items()}
    rows: List[Dict[str, Any]] = []
    for date in eval_dates:
        fills, ledger, gmeta = run_goal_path_day(
            pol,
            date=date,
            m1_by_symbol=m1_by_sym,
            target_percent=float(target),
            max_daily_risk_percent=float(risk),
            symbols=list(m1_by_sym.keys()),
            tf_cache_by_symbol=tf_cache,
            brain_drives=True,
            watch_enabled=True,
            monty_htf_blend=bool(monty_htf_blend),
        )
        pnl = float(ledger.realized_pnl_percent)
        loss = max(-pnl, 0.0)
        worst = float(ledger.worst_case_daily_loss_percent())
        breach = bool(loss > float(risk) + 1e-6 or worst > float(risk) + 1e-6)
        hit = bool(pnl >= float(target) - 1e-9)
        clear = bool(hit and not breach)
        rows.append(
            {
                "day": date,
                "pnl": pnl,
                "n_trades": len(fills),
                "hit": hit,
                "breach": breach,
                "clear": clear,
                "green": pnl > 0,
            }
        )

    n = len(rows)
    if n == 0:
        return {"error": "no_eval_days", "engine": "court goal_path"}

    pnls = [r["pnl"] for r in rows]
    clears = sum(1 for r in rows if r["clear"])
    breaches = sum(1 for r in rows if r["breach"])
    greens = sum(1 for r in rows if r["green"])
    # clear streak
    streak = best_streak = 0
    for r in rows:
        if r["clear"]:
            streak += 1
            best_streak = max(best_streak, streak)
        else:
            streak = 0

    a13 = sum(1 for r in rows if 8 <= r["n_trades"] <= 400) / n
    n_zero = sum(1 for r in rows if r["n_trades"] == 0)

    return {
        "engine": "court goal_path MetaBrain",
        "brain": str(champion_path.name),
        "fingerprint": pol.weight_fingerprint(),
        "target": float(target),
        "risk": float(risk),
        "n_days": n,
        "eval_start": eval_dates[0],
        "eval_end": eval_dates[-1],
        "symbols": list(m1_by_sym.keys()),
        "multi_symbol": len(m1_by_sym) > 1,
        "monty_htf_blend": bool(monty_htf_blend),
        "clear_rate": clears / n,
        "breach_rate": breaches / n,
        "hit_rate": sum(1 for r in rows if r["hit"]) / n,
        "green_frac": greens / n,
        "mean_pnl_pct": float(np.mean(pnls)),
        "median_pnl_pct": float(np.median(pnls)),
        "max_pnl_pct": float(np.max(pnls)),
        "min_pnl_pct": float(np.min(pnls)),
        "longest_clear_streak": best_streak,
        "a13_frac": a13,
        "n_zero": n_zero,
        "mean_trades": float(np.mean([r["n_trades"] for r in rows])),
        "total_trades": int(sum(r["n_trades"] for r in rows)),
    }


def _winner(proven: Dict[str, Any], court: Dict[str, Any]) -> Dict[str, Any]:
    """Rank on Mark mission: (1) breach must be 0-ish (2) clear_rate (3) mean_pnl."""
    issues = []
    if proven.get("error"):
        issues.append("proven_error")
    if court.get("error"):
        issues.append("court_error")
    if issues:
        return {"winner": None, "reason": ",".join(issues)}

    pc, cc = proven.get("clear_rate"), court.get("clear_rate")
    pb, cb = proven.get("breach_rate"), court.get("breach_rate")
    # breach: lower better; treat >0 as serious
    proven_safe = (pb is not None) and (pb <= 1e-9)
    court_safe = (cb is not None) and (cb <= 1e-9)

    if proven_safe and not court_safe:
        return {"winner": "PROVEN", "reason": "court_has_breach_proven_clean"}
    if court_safe and not proven_safe:
        return {"winner": "COURT_0037", "reason": "proven_has_breach_court_clean"}
    if not proven_safe and not court_safe:
        # both breach — higher clear still noted but safety fail
        if pc is not None and cc is not None and abs(pc - cc) > 0.01:
            w = "PROVEN" if pc > cc else "COURT_0037"
            return {"winner": w, "reason": "both_breach_higher_clear", "tie_break": "clear"}
        return {"winner": "TIE_UNSAFE", "reason": "both_breach"}

    # both safe: higher clear wins
    if pc is None or cc is None:
        return {"winner": None, "reason": "missing_clear"}
    if abs(pc - cc) < 0.005:
        # tie on clear → mean pnl
        pm, cm = proven.get("mean_pnl_pct"), court.get("mean_pnl_pct")
        if pm is not None and cm is not None and abs(pm - cm) >= 0.05:
            w = "PROVEN" if pm > cm else "COURT_0037"
            return {"winner": w, "reason": "clear_tie_mean_pnl"}
        return {"winner": "TIE", "reason": "clear_and_pnl_close"}
    w = "PROVEN" if pc > cc else "COURT_0037"
    return {
        "winner": w,
        "reason": "higher_clear_rate_breach_0",
        "clear_proven": pc,
        "clear_court": cc,
        "delta_clear_court_minus_proven": float(cc) - float(pc),
    }


def run_showdown(
    *,
    pairs: Optional[Sequence[Tuple[float, float]]] = None,
    court_days: int = 90,
    out_path: Path = DEFAULT_OUT,
) -> Dict[str, Any]:
    # Court legal band: target [5,90], risk [1,3]. Mark yardstick 3.0/3.5 is
    # PROVEN-native only — still scored for reference.
    pairs = list(pairs) if pairs else [(5.0, 3.0), (15.0, 2.0), (3.0, 3.5)]
    report: Dict[str, Any] = {
        "law": "fair_policy_showdown_proven_vs_court0037",
        "score_definition": {
            "clear": "day_pnl >= target AND not breach",
            "breach": "loss or worst-case exceeds risk floor",
            "green": "day_pnl > 0",
        },
        "engines": {
            "PROVEN": "the-truth FastSim + XAUUSD curriculum (native prove_it)",
            "COURT_0037": "Evidence Court goal_path MetaBrain (native dual path)",
        },
        "bands": {
            "court_legal": "target [5,90] x risk [1,3]",
            "mark_yardstick": "3.0 / 3.5 (PROVEN-native; Court rejects 3.0 target and 3.5 risk)",
            "primary_shared_pair": "5.0 / 3.0 (closest legal shared yardstick)",
        },
        "caveats": [
            "Different fill models and feature stacks — cannot share weights.",
            "PROVEN is XAU-only curriculum window; Court uses trailing multi-symbol common calendar.",
            "Same metric DEFINITION and same typed target/risk when both legal; not identical bar path.",
            "Court cannot natively run target=3 or risk=3.5 (GOAL_LAW band).",
        ],
        "pairs": [],
    }

    def _court_legal(t: float, r: float) -> bool:
        return 5.0 <= float(t) <= 90.0 and 1.0 <= float(r) <= 3.0

    for tgt, risk in pairs:
        print(f"=== Pair target={tgt} risk={risk} ===", flush=True)
        print("[PROVEN] prove_it…", flush=True)
        proven = _run_proven_prove_it(tgt, risk)
        print(
            f"  clear={proven.get('clear_rate')} breach={proven.get('breach_rate')} "
            f"n={proven.get('n_days')}",
            flush=True,
        )

        court_xau: Dict[str, Any]
        court_multi: Dict[str, Any] = {"skipped": True}
        if not _court_legal(tgt, risk):
            court_xau = {
                "error": "court_band_illegal",
                "note": "Court target must be [5,90], risk [1,3]",
                "target": tgt,
                "risk": risk,
            }
            print("  [COURT] skipped — pair outside Court GOAL band", flush=True)
        else:
            print("[COURT XAU-only] goal_path (closest to PROVEN)…", flush=True)
            court_xau = _run_court_fixed_pair(
                target=tgt,
                risk=risk,
                n_days=court_days,
                symbols=["XAUUSD"],
            )
            print(
                f"  clear={court_xau.get('clear_rate')} breach={court_xau.get('breach_rate')} "
                f"n={court_xau.get('n_days')}",
                flush=True,
            )
            # Multi only on primary shared pair 5/3
            if abs(float(tgt) - 5.0) < 1e-9 and abs(float(risk) - 3.0) < 1e-9:
                print("[COURT multi-symbol] goal_path…", flush=True)
                court_multi = _run_court_fixed_pair(
                    target=tgt,
                    risk=risk,
                    n_days=min(int(court_days), 60),
                    symbols=["XAUUSD", "EURUSD", "GBPUSD"],
                )
                print(
                    f"  clear={court_multi.get('clear_rate')} breach={court_multi.get('breach_rate')} "
                    f"n={court_multi.get('n_days')}",
                    flush=True,
                )

        row = {
            "target": tgt,
            "risk": risk,
            "court_legal": _court_legal(tgt, risk),
            "proven": proven,
            "court_multi": court_multi,
            "court_xau_only": court_xau,
            "winner_vs_multi": _winner(proven, court_multi)
            if not court_multi.get("skipped") and not court_multi.get("error")
            else {"winner": None, "reason": "multi_skipped_or_error"},
            "winner_vs_xau": _winner(proven, court_xau)
            if not court_xau.get("error")
            else {"winner": "PROVEN", "reason": "court_cannot_run_pair"},
        }
        report["pairs"].append(row)

    # Primary shared: 5.0/3.0 XAU; reference Mark yardstick PROVEN-only 3.0/3.5
    shared = next(
        (p for p in report["pairs"] if abs(p["target"] - 5.0) < 1e-9 and abs(p["risk"] - 3.0) < 1e-9),
        None,
    )
    mark_y = next(
        (p for p in report["pairs"] if abs(p["target"] - 3.0) < 1e-9 and abs(p["risk"] - 3.5) < 1e-9),
        None,
    )
    primary = shared or next((p for p in report["pairs"] if p.get("court_legal")), report["pairs"][0])
    w = primary.get("winner_vs_xau") or {}
    report["headline"] = {
        "primary_shared_pair": {"target": primary["target"], "risk": primary["risk"]},
        "winner_primary_proven_vs_court_xau": w,
        "winner_primary_proven_vs_court_multi": primary.get("winner_vs_multi"),
        "proven_clear": (primary.get("proven") or {}).get("clear_rate"),
        "court_xau_clear": (primary.get("court_xau_only") or {}).get("clear_rate"),
        "court_multi_clear": (primary.get("court_multi") or {}).get("clear_rate"),
        "proven_breach": (primary.get("proven") or {}).get("breach_rate"),
        "court_xau_breach": (primary.get("court_xau_only") or {}).get("breach_rate"),
        "mark_yardstick_3_3p5_proven_only": {
            "clear": ((mark_y or {}).get("proven") or {}).get("clear_rate"),
            "breach": ((mark_y or {}).get("proven") or {}).get("breach_rate"),
            "n_days": ((mark_y or {}).get("proven") or {}).get("n_days"),
            "note": "Court cannot run 3.0/3.5 natively",
        },
    }
    report["overall_best"] = w.get("winner") or "UNKNOWN"
    report["overall_reason"] = w.get("reason")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    report["out_path"] = str(out_path)
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="PROVEN vs Court 0037 fair showdown")
    p.add_argument("--court-days", type=int, default=90)
    p.add_argument("--out", type=str, default=str(DEFAULT_OUT))
    p.add_argument(
        "--pairs",
        type=str,
        default="5.0,3.0;15.0,2.0;3.0,3.5",
        help="target,risk;target,risk — include 5/3 shared + Mark 3/3.5 PROVEN-only",
    )
    args = p.parse_args(list(argv) if argv is not None else None)
    pairs = []
    for part in str(args.pairs).split(";"):
        part = part.strip()
        if not part:
            continue
        a, b = part.split(",")
        pairs.append((float(a), float(b)))
    rep = run_showdown(pairs=pairs, court_days=int(args.court_days), out_path=Path(args.out))
    print(json.dumps(rep.get("headline"), indent=2))
    print("overall_best:", rep.get("overall_best"), rep.get("overall_reason"))
    print("out:", rep.get("out_path"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
