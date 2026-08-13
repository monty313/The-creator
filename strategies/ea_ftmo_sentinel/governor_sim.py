"""FTMO Sentinel — Day Governor Monte Carlo validation.

Mirrors the EA governor trade-for-trade and measures, per scenario:
  * distribution of daily P&L (% of initial balance)
  * P(day banked >= +2.5% goal) and mean daily return
  * P(red day) and worst day (must stay far inside FTMO -5%)
  * FTMO challenge outcomes (days to +10%, breach probability)

Trade model comes from the measured corpus (strategies/reports):
  * barrier pair tp=0.00028 / sl=0.00115  ->  win = +0.2435 R, loss = -1 R
  * CCI gravity upgraded book: 44/44 wins  ->  Wilson 95% lower bound ~ 0.920
  * McFlurry accuracy-layer book: WR ~ 0.80 (212 trades)
  * cost drag ~ 0.05 R per trade (0.6 pip spread vs 11.5 pip SL)

NOT Court law. Experimental lab artifact (Summary-Court measurement only).
Usage:  python -m strategies.ea_ftmo_sentinel.governor_sim
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

# ---- governor parameters (must match EA inputs) -----------------------
BASE_RISK = 0.80          # % of initial balance per trade
MAX_RISK = 2.00           # ladder cap
LADDER_FRACTION = 0.75    # risk += frac * positive day P&L%
SOFT_STOP = 1.5           # % - no new trades
HARD_STOP = 2.0           # % - flatten (intraday floating; sim uses trade closes)
DAILY_GOAL = 2.5          # % - bank the day
RATCHET_TRIGGER = 0.8     # % day peak arms the ratchet
RATCHET_FLOOR = 0.20      # % minimum locked profit
RATCHET_TRAIL = 0.60      # floor trails this fraction of day peak
MAX_TRADES_DAY = 40
MAX_CONSEC_LOSSES = 3
LOSS_STREAK_HALVING = True

WIN_R = 0.00028 / 0.00115  # +0.2435 R per win (corpus barrier pair)
COST_R = 0.05              # R lost to spread/commission per trade

FTMO_DAILY_LIMIT = -5.0
FTMO_TOTAL_LIMIT = -10.0
FTMO_TARGET = 10.0
MIN_TRADING_DAYS = 4
TOTAL_FUSE = -6.0          # EA InpMaxTotalLossPct: permanent halt before FTMO -10%


def wilson_lower(wins: int, n: int, z: float = 1.96) -> float:
    """95% Wilson lower bound on a binomial proportion."""
    if n == 0:
        return 0.0
    p = wins / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (centre - margin) / denom


@dataclass
class DayResult:
    pl: float
    trades: int
    banked_goal: bool
    banked_ratchet: bool
    halted: bool


@dataclass
class Scenario:
    name: str
    win_rate: float
    signals_per_day: float
    note: str = ""
    days: list = field(default_factory=list)


def simulate_day(rng: random.Random, win_rate: float, signals_per_day: float) -> DayResult:
    # Poisson arrival of valid signals inside the session
    lam = signals_per_day
    n_signals = 0
    l_exp, p_acc = math.exp(-lam), 1.0
    while True:
        p_acc *= rng.random()
        if p_acc <= l_exp:
            break
        n_signals += 1

    day_pl = 0.0
    peak = 0.0
    streak = 0
    consec = 0
    trades = 0
    banked_goal = banked_ratchet = halted = False

    for _ in range(n_signals):
        if trades >= MAX_TRADES_DAY or consec >= MAX_CONSEC_LOSSES:
            halted = consec >= MAX_CONSEC_LOSSES
            break

        risk = BASE_RISK
        if LOSS_STREAK_HALVING and streak > 0:
            risk /= 2 ** min(streak, 4)
        if day_pl > 0:
            risk += LADDER_FRACTION * day_pl
        risk = min(risk, MAX_RISK, day_pl + SOFT_STOP)  # one loss cannot cross soft stop
        if risk <= 0.02:
            break

        win = rng.random() < win_rate
        day_pl += risk * (WIN_R - COST_R) if win else risk * (-1.0 - COST_R)
        trades += 1
        if win:
            streak = consec = 0
        else:
            streak += 1
            consec += 1
        peak = max(peak, day_pl)

        if day_pl <= -SOFT_STOP:
            halted = True
            break
        if day_pl >= DAILY_GOAL:
            banked_goal = True
            break
        if peak >= RATCHET_TRIGGER:
            floor = max(RATCHET_FLOOR, peak * RATCHET_TRAIL)
            if day_pl <= floor:
                banked_ratchet = True
                break

    return DayResult(day_pl, trades, banked_goal, banked_ratchet, halted)


def simulate_challenge(rng: random.Random, win_rate: float, signals_per_day: float,
                       max_days: int = 60) -> dict:
    cum = 0.0
    trading_days = 0
    for day in range(1, max_days + 1):
        r = simulate_day(rng, win_rate, signals_per_day)
        if r.trades > 0:
            trading_days += 1
        cum += r.pl
        if r.pl <= FTMO_DAILY_LIMIT:
            return {"result": "FAIL_DAILY", "days": day}
        if cum <= FTMO_TOTAL_LIMIT:
            return {"result": "FAIL_TOTAL", "days": day}
        if cum <= TOTAL_FUSE:
            # EA permanent halt: challenge not passed, account NOT breached
            return {"result": "HALT_FUSE", "days": day}
        if cum >= FTMO_TARGET and trading_days >= MIN_TRADING_DAYS:
            return {"result": "PASS", "days": day}
    return {"result": "TIMEOUT", "days": max_days, "cum": cum}


def pct(x: float) -> str:
    return f"{100.0 * x:.2f}%"


def main() -> None:
    rng = random.Random(42)
    n_days = 20000
    n_challenges = 2000

    wr_cci_lb = wilson_lower(44, 44)          # 44/44 measured -> ~0.920
    scenarios = [
        Scenario("A_cci_LB_1symbol", wr_cci_lb, 20,
                 "CCI upgraded book Wilson-LB WR, 20 signals/day (1 symbol, 2 engines)"),
        Scenario("A3_cci_LB_3symbols", wr_cci_lb, 40,
                 "same WR, ~40 signals/day (Sentinel on 3-4 symbols, shared governor)"),
        Scenario("B_cci_LB_sparse", wr_cci_lb, 8,
                 "same WR, sparse 8 signals/day (single symbol, strict gates)"),
        Scenario("C_mcflurry_base", 0.80, 20,
                 "McFlurry accuracy-layer WR (212-trade book)"),
        Scenario("D_stress", 0.70, 20,
                 "stress: WR well below every measured post-tweak family"),
    ]

    lines = []
    lines.append("# FTMO Sentinel — governor Monte Carlo (measured-parameter validation)\n")
    lines.append("**Not Court law.** Summary-Court measurement artifact. "
                 "Trade model from `strategies/reports` measured books; "
                 f"win = +{WIN_R:.3f}R, loss = -1R, cost = {COST_R}R/trade.\n")
    lines.append(f"Days per scenario: {n_days} · challenges: {n_challenges} · seed 42\n")
    lines.append("| Scenario | WR | sig/day | mean day | med day | P(day>=+2.5%) "
                 "| P(red day) | worst day | P(day<=-5%) FTMO |")
    lines.append("|---|---|---|---|---|---|---|---|---|")

    for sc in scenarios:
        results = [simulate_day(rng, sc.win_rate, sc.signals_per_day) for _ in range(n_days)]
        pls = sorted(r.pl for r in results)
        mean_pl = sum(pls) / len(pls)
        med_pl = pls[len(pls) // 2]
        p_goal = sum(1 for r in results if r.pl >= DAILY_GOAL - 1e-9) / n_days
        p_red = sum(1 for r in results if r.pl < 0) / n_days
        worst = pls[0]
        p_ftmo_breach = sum(1 for r in results if r.pl <= FTMO_DAILY_LIMIT) / n_days
        lines.append(
            f"| {sc.name} | {sc.win_rate:.3f} | {sc.signals_per_day:g} "
            f"| {mean_pl:+.3f}% | {med_pl:+.3f}% | {pct(p_goal)} "
            f"| {pct(p_red)} | {worst:+.3f}% | {pct(p_ftmo_breach)} |")
        sc.days = results

    lines.append("\n## FTMO challenge outcomes (target +10%, min 4 trading days, 60-day cap)\n")
    lines.append("`halted @-6% fuse` = EA stops itself before the FTMO -10% breach: "
                 "challenge not passed, account preserved.\n")
    lines.append("| Scenario | P(pass) | P(FTMO daily breach) | P(FTMO total breach) "
                 "| P(halted @-6% fuse) | P(timeout) | median days to pass |")
    lines.append("|---|---|---|---|---|---|---|")
    for sc in scenarios:
        runs = [simulate_challenge(rng, sc.win_rate, sc.signals_per_day)
                for _ in range(n_challenges)]
        n_pass = [r for r in runs if r["result"] == "PASS"]
        p_pass = len(n_pass) / n_challenges
        p_fd = sum(1 for r in runs if r["result"] == "FAIL_DAILY") / n_challenges
        p_ft = sum(1 for r in runs if r["result"] == "FAIL_TOTAL") / n_challenges
        p_hf = sum(1 for r in runs if r["result"] == "HALT_FUSE") / n_challenges
        p_to = sum(1 for r in runs if r["result"] == "TIMEOUT") / n_challenges
        med_days = sorted(r["days"] for r in n_pass)[len(n_pass) // 2] if n_pass else float("nan")
        lines.append(f"| {sc.name} | {pct(p_pass)} | {pct(p_fd)} | {pct(p_ft)} "
                     f"| {pct(p_hf)} | {pct(p_to)} | {med_days} |")

    lines.append("\n## Read this honestly\n")
    lines.append("- The governor **caps** every red day near the soft stop; an FTMO daily breach "
                 "(-5%) requires an intraday gap far past the hard flatten — the sim shows 0 at "
                 "trade-close granularity, live requires the hard-stop watchdog plus sane "
                 "position sizing (which the EA enforces).")
    lines.append("- '+2.5% every single day' is not physically guaranteeable: on sparse-signal "
                 "or low-WR days the governor banks smaller greens or scratches flat instead of "
                 "forcing thrash. The design maximizes P(green) first, goal-hit second.")
    lines.append("- WR inputs are from one EURUSD window (June-July 2026). Re-measure per "
                 "symbol/window before believing the absolute pass-time numbers (corpus law: "
                 "distrust specific pips until they survive new windows).")
    lines.append("- **2026-08-12 real-data measurement (VALIDATION.md) falsified scenarios "
                 "A/A3/B:** measured WR is ~70% (not 92%) at ~1-2 signals/day (not 20). "
                 "Reality matches scenario C/D: the governor protects the account "
                 "(fuse-halt, zero breaches) but the challenge is NOT passed.")

    report = "\n".join(lines) + "\n"
    out = __file__.replace("governor_sim.py", "VALIDATION.md")
    with open(out, "w") as f:
        f.write(report)
    print(report)
    print(f"[written] {out}")


if __name__ == "__main__":
    main()
