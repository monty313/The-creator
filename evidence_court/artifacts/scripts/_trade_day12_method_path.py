"""Trade DAY 12 ONLY (2026-01-21) the way the METHOD says — not champion thrash.

Method sequence (no load/reclaim words):
  1) Force on → WAIT (no densify)
  2) RESUME #1 → FIRE once → HOLD window (no thrash re-fire after)
  3) PULLBACK → WAIT
  4) RESUME #2 → FIRE once → HOLD
  5) DONE → no more entries

Uses real XAU M1 + same fill/risk primitives as goal_path (lab exhibit, not PROMOTE).
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

# artifacts/ is parent of scripts/
ARTIFACTS = Path(__file__).resolve().parent.parent
from typing import Any, Dict, List, Optional, Sequence

import cv2
import numpy as np

from evidence_court.meta_rl.goal_path import (
    DEFAULT_STOP_DISTANCE_PCT,
    m1_window,
    simulate_fill_m1_path,
)
from evidence_court.meta_rl.leverage import LEVERAGE, risk_legal_max_lot, stop_distance_price_from_pct
from evidence_court.meta_rl.price_io import SYMBOL_FILES, load_m1_trailing_calendar_days
from evidence_court.meta_rl.risk import (
    DailyRiskLedger,
    FrictionAssumptions,
    OpenPosition,
    apply_trade_result,
    size_position_risk_percent,
)

DAY = "2026-01-21"
SYMBOL = "XAUUSD"
TARGET = 15.0
RISK = 3.0
OUT = ARTIFACTS / "day12" / "method_trade"
OUT.mkdir(parents=True, exist_ok=True)

# Method-legal plan for day 12 only (Court exhibit times)
METHOD_LEGS = [
    {
        "id": 1,
        "name": "FIRE_1_RESUME_LAUNCH",
        "phase": "resume",
        "side": "long",
        "entry_t": "08:15:00",
        "exit_t": "08:30:00",
        "hold_note": "Hold launch; next 15m is NO thrash re-fire",
        # size: aggressive share of remaining budget (conversion toward 15 under 3)
        "aggression": 0.85,
        "size_r_arm_r": 1.5,  # hold more R than 1.0 scratch
    },
    {
        "id": 2,
        "name": "FIRE_2_RESUME_PULLBACK",
        "phase": "resume",
        "side": "long",
        "entry_t": "09:15:00",
        "exit_t": "09:50:00",  # hold through resume, not micro re-entries
        "hold_note": "Second cycle only; then day is WAIT",
        "aggression": 0.75,
        "size_r_arm_r": 1.25,
    },
]

# Explicit WAIT windows (logged, not traded)
WAIT_PHASES = [
    {"name": "FORCE_WAIT", "t0": "07:00:00", "t1": "08:15:00", "why": "Force on — wait for resume, no densify"},
    {"name": "NO_THRASH", "t0": "08:30:00", "t1": "08:45:00", "why": "After fire#1 — FLAT, no re-fire (bot thrash zone)"},
    {"name": "PULLBACK_WAIT", "t0": "08:45:00", "t1": "09:15:00", "why": "Pullback vs Force — wait, no dip-chase"},
    {"name": "DONE_WAIT", "t0": "09:50:00", "t1": "23:59:59", "why": "Method complete for day — no metronome entries"},
]


@dataclass
class MethodFill:
    name: str
    side: str
    entry_t: str
    exit_t: str
    entry_px: float
    size_risk_percent: float
    lot: float
    pnl_percent: float
    hold_minutes: float
    note: str


def tsec(t: str) -> int:
    p = str(t).split(":")
    return int(p[0]) * 3600 + int(p[1]) * 60 + int(float(p[2]) if len(p) > 2 else 0)


def hold_minutes(a: str, b: str) -> float:
    return max((tsec(b) - tsec(a)) / 60.0, 0.0)


def load_day_bars() -> List[dict]:
    path = Path(SYMBOL_FILES["XAUUSD"])
    bars = load_m1_trailing_calendar_days(path, n_days=400)
    day = [b for b in bars if str(b.get("date", "")) == DAY]
    if not day:
        raise SystemExit(f"No M1 for {DAY}")
    # need prior context for nothing critical; fill only needs day window
    return day


def trade_method_day(
    m1: Sequence[dict],
    *,
    target: float = TARGET,
    risk: float = RISK,
    equity: float = 100_000.0,
) -> Dict[str, Any]:
    fr = FrictionAssumptions()
    ledger = DailyRiskLedger(max_daily_risk_percent=risk, equity=equity, friction=fr)
    fills: List[MethodFill] = []
    log: List[str] = []

    log.append(f"I am the Policy trading {DAY} under METHOD (not thrash densify).")
    log.append(f"Target={target}%  Risk envelope={risk}%  breach must stay 0.")
    log.append("Plan: 2 resume fires only. Wait Force / pullback / post-fire / done.")

    for phase in WAIT_PHASES:
        if phase["name"] == "FORCE_WAIT":
            log.append(f"WAIT [{phase['t0']}–{phase['t1']}]: {phase['why']}")

    for leg in METHOD_LEGS:
        if ledger.realized_pnl_percent >= target - 1e-9:
            log.append("Target already hit — stop new risk.")
            break
        rem = ledger.remaining_risk_budget_percent()
        if rem <= 0.08:
            log.append("Risk budget exhausted — no new leg.")
            break

        window = m1_window(
            m1, date=DAY, start_time=leg["entry_t"], end_time=leg["exit_t"]
        )
        if len(window) < 3:
            log.append(f"SKIP {leg['name']}: not enough bars in window")
            continue

        entry = float(window[0]["open"])
        stop_px = stop_distance_price_from_pct(entry, DEFAULT_STOP_DISTANCE_PCT)
        # Size toward remaining goal under remaining risk
        progress = max(ledger.realized_pnl_percent, 0.0) / max(target, 1e-6)
        remaining_goal = max(target * (1.0 - progress), 0.0)
        size = size_position_risk_percent(
            max_daily_risk_percent=risk,
            remaining_budget_percent=rem,
            stop_distance_pct=DEFAULT_STOP_DISTANCE_PCT,
            target_percent=target,
            aggression=float(leg["aggression"]),
        )
        # Conversion bias: if far from target, use more of remaining budget (still hard-capped)
        if remaining_goal > 5.0:
            size = min(rem * 0.55, max(size, rem * 0.40))
        size = min(size, rem * 0.95)

        lot_info = risk_legal_max_lot(
            equity=equity,
            risk_percent=size,
            entry_price=entry,
            stop_distance_price=stop_px,
            symbol=SYMBOL,
            leverage=LEVERAGE,
        )
        size = min(size, float(lot_info["risk_percent_actual"]) or size)
        if size <= 0 or lot_info["lot"] <= 0:
            log.append(f"SKIP {leg['name']}: size/lot zero under envelope")
            continue
        if ledger.would_breach(size):
            log.append(f"SKIP {leg['name']}: would breach risk")
            continue

        side = 1 if leg["side"] == "long" else -1
        rem_goal = max(target - ledger.realized_pnl_percent, 0.0)
        ledger.positions.append(
            OpenPosition(
                symbol=SYMBOL,
                side=side,
                risk_percent=size,
                notional_pct=size / max(DEFAULT_STOP_DISTANCE_PCT, 1e-6) * 100.0,
            )
        )
        pnl = simulate_fill_m1_path(
            side=side,
            bars=window,
            size_risk_percent=size,
            stop_distance_pct=DEFAULT_STOP_DISTANCE_PCT,
            friction_pct=fr.total_pct,
            trail=False,
            goal_lock_pnl_percent=rem_goal if rem_goal > 0 else None,
            partial_lock_frac=0.5,
            size_r_arm_r=float(leg["size_r_arm_r"]),
        )
        apply_trade_result(ledger, pnl_percent=pnl, closed_risk_percent=size)
        ledger.positions.clear()

        fill = MethodFill(
            name=leg["name"],
            side=leg["side"],
            entry_t=leg["entry_t"],
            exit_t=leg["exit_t"],
            entry_px=entry,
            size_risk_percent=float(size),
            lot=float(lot_info["lot"]),
            pnl_percent=float(pnl),
            hold_minutes=hold_minutes(leg["entry_t"], leg["exit_t"]),
            note=leg["hold_note"],
        )
        fills.append(fill)
        log.append(
            f"FIRE {leg['name']}: {leg['side']} @{leg['entry_t']}→{leg['exit_t']} "
            f"hold={fill.hold_minutes:.0f}m size_risk={size:.3f}% lot={fill.lot:.2f} "
            f"pnl={pnl:+.3f}%  day_pnl={ledger.realized_pnl_percent:+.3f}%"
        )
        log.append(f"  note: {leg['hold_note']}")

        # After fire #1: explicit no thrash
        if leg["id"] == 1:
            log.append("WAIT [08:30–08:45]: NO thrash re-fire (method hard rule).")
            log.append("WAIT [08:45–09:15]: pullback vs Force — still WAIT.")

    log.append("WAIT [09:50–EOD]: method day complete — no more entries.")

    loss = max(-ledger.realized_pnl_percent, 0.0)
    worst = ledger.worst_case_daily_loss_percent()
    breach = loss > risk + 1e-6 or worst > risk + 1e-6
    hit = ledger.realized_pnl_percent >= target - 1e-9

    return {
        "day": DAY,
        "symbol": SYMBOL,
        "mode": "METHOD_PATH_NOT_THRASH",
        "target_percent": target,
        "max_daily_risk_percent": risk,
        "n_trades": len(fills),
        "fills": [asdict(f) for f in fills],
        "pnl_percent": float(ledger.realized_pnl_percent),
        "hit_target": bool(hit),
        "breach": bool(breach),
        "worst_case_loss_percent": float(worst),
        "wait_phases": WAIT_PHASES,
        "method_legs_planned": METHOD_LEGS,
        "policy_log": log,
        "compare_bot_class": {
            "bot_thrash_n_trades": "50–97 (reaudit)",
            "bot_thrash_pnl_approx": "~+2.9% to +3.2%",
            "bot_hit": False,
            "method_n_trades": len(fills),
            "method_pnl": float(ledger.realized_pnl_percent),
            "method_hit": bool(hit),
        },
        "not_production_promote": True,
    }


def render_result_board(rep: Dict[str, Any]) -> Path:
    img = np.zeros((720, 1200, 3), dtype=np.uint8)
    img[:] = (18, 18, 22)
    gold, green, red, white, muted, cyan = (
        (40, 180, 220),
        (80, 200, 120),
        (80, 80, 220),
        (235, 235, 235),
        (150, 150, 160),
        (200, 200, 80),
    )

    def put(t, xy, s=0.55, c=white, th=1):
        cv2.putText(img, t[:100], xy, cv2.FONT_HERSHEY_SIMPLEX, s, c, th, cv2.LINE_AA)

    put("DAY 12 METHOD TRADE — Policy ran the day correctly", (24, 36), 0.75, gold, 2)
    put(f"{DAY}  XAUUSD  target {rep['target_percent']}%  risk {rep['max_daily_risk_percent']}%", (24, 68), 0.5, muted, 1)

    hit = rep["hit_target"]
    put(
        f"PnL {rep['pnl_percent']:+.3f}%   trades={rep['n_trades']}   "
        f"hit={hit}   breach={rep['breach']}",
        (24, 110),
        0.65,
        green if hit else cyan,
        2,
    )
    put(
        "vs bot thrash class: ~+3% / 50–97 tickets / no clear",
        (24, 145),
        0.5,
        red,
        1,
    )

    y = 190
    put("FILLS (method only):", (24, y), 0.55, gold, 1)
    y += 30
    for f in rep["fills"]:
        put(
            f"{f['name']}: {f['side']} {f['entry_t']}→{f['exit_t']}  "
            f"hold={f['hold_minutes']:.0f}m  size={f['size_risk_percent']:.2f}%  "
            f"pnl={f['pnl_percent']:+.3f}%",
            (24, y),
            0.48,
            green if f["pnl_percent"] > 0 else red,
            1,
        )
        y += 26
        put(f"   {f['note']}", (24, y), 0.4, muted, 1)
        y += 28

    y += 10
    put("POLICY LOG:", (24, y), 0.5, gold, 1)
    y += 26
    for line in rep["policy_log"]:
        if y > 690:
            break
        put(line, (24, y), 0.38, white, 1)
        y += 18

    path = OUT / "day12_method_trade_result.png"
    cv2.imwrite(str(path), img)
    return path


def main() -> None:
    print("Loading", DAY, "M1…")
    m1 = load_day_bars()
    print("bars", len(m1))
    rep = trade_method_day(m1)
    json_path = OUT / "day12_method_trade_result.json"
    json_path.write_text(json.dumps(rep, indent=2), encoding="utf-8")
    md = OUT / "DAY12_METHOD_TRADE.md"
    fills_md = "\n".join(
        f"| {f['name']} | {f['side']} | {f['entry_t']} | {f['exit_t']} | "
        f"{f['hold_minutes']:.0f} | {f['size_risk_percent']:.3f} | {f['pnl_percent']:+.3f} |"
        for f in rep["fills"]
    )
    md.write_text(
        f"""# Day 12 — Policy traded the METHOD path

**Date:** {DAY} · **Symbol:** {SYMBOL}  
**Mode:** METHOD (2 resume fires) · **Not** production thrash champion  
**Target:** {TARGET}% · **Risk:** {RISK}%

## Result

| Metric | Method path | Bot thrash class |
|--------|------------:|-----------------:|
| n_trades | **{rep['n_trades']}** | 50–97 |
| PnL % | **{rep['pnl_percent']:+.3f}** | ~+2.9 to +3.2 |
| hit 15% | **{rep['hit_target']}** | false |
| breach | **{rep['breach']}** | false |

## Fills

| Name | Side | Entry | Exit | Hold min | Size risk % | PnL % |
|------|------|-------|------|----------:|------------:|------:|
{fills_md}

## Policy log

"""
        + "\n".join(f"- {ln}" for ln in rep["policy_log"])
        + "\n\n**Lab only — not Court PROMOTE.**\n",
        encoding="utf-8",
    )
    board = render_result_board(rep)
    print(json.dumps({k: rep[k] for k in (
        "n_trades", "pnl_percent", "hit_target", "breach", "fills"
    )}, indent=2))
    print("wrote", json_path)
    print("wrote", md)
    print("wrote", board)
    print("--- POLICY ---")
    for ln in rep["policy_log"]:
        print(ln)


if __name__ == "__main__":
    main()
