"""Auditable daily risk aggregation and position sizing under declared envelope."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class FrictionAssumptions:
    """Declared friction — never claim frictionless production-ready."""
    spread_cost_pct: float = 0.02  # % of notional per round-turn proxy
    commission_pct: float = 0.01
    slippage_pct: float = 0.01

    @property
    def total_pct(self) -> float:
        return float(self.spread_cost_pct + self.commission_pct + self.slippage_pct)


@dataclass
class OpenPosition:
    symbol: str
    side: int  # +1 long, -1 short
    risk_percent: float  # planned max loss for this position as % equity
    notional_pct: float = 0.0


@dataclass
class DailyRiskLedger:
    """Tracks aggregated daily risk across symbols/positions."""
    max_daily_risk_percent: float
    equity: float = 100_000.0
    realized_pnl_percent: float = 0.0  # positive = profit
    positions: List[OpenPosition] = field(default_factory=list)
    friction: FrictionAssumptions = field(default_factory=FrictionAssumptions)
    closed_losses_percent: float = 0.0  # sum of closed adverse outcomes

    def open_risk_percent(self) -> float:
        return float(sum(max(p.risk_percent, 0.0) for p in self.positions))

    def friction_open_percent(self) -> float:
        # Friction assumed paid on open notional as % equity proxy
        return float(sum(max(p.notional_pct, 0.0) * self.friction.total_pct / 100.0
                         for p in self.positions))

    def worst_case_daily_loss_percent(self) -> float:
        """Max loss if all open stops hit + friction + already realized losses.

        Uses max(closed_losses, adverse realized) so apply_trade_result does not
        double-count the same closed loss via both realized_pnl and closed_losses.
        """
        adverse_realized = max(-self.realized_pnl_percent, 0.0)
        closed = max(self.closed_losses_percent, 0.0)
        realized_loss = max(adverse_realized, closed)
        return float(realized_loss + self.open_risk_percent() + self.friction_open_percent())

    def remaining_risk_budget_percent(self) -> float:
        return float(self.max_daily_risk_percent - self.worst_case_daily_loss_percent())

    def would_breach(self, additional_risk_percent: float) -> bool:
        projected = self.worst_case_daily_loss_percent() + max(float(additional_risk_percent), 0.0)
        return projected > self.max_daily_risk_percent + 1e-9

    def can_open(self, risk_percent: float) -> bool:
        return not self.would_breach(risk_percent) and risk_percent > 0


def size_position_risk_percent(
    *,
    max_daily_risk_percent: float,
    remaining_budget_percent: float,
    stop_distance_pct: float,
    target_percent: float,
    aggression: float = 0.5,
    min_risk: float = 0.05,
    max_single_fraction: float = 0.5,
    friction_reserve_percent: float = 0.05,
) -> float:
    """Return position risk % of equity, never exceeding remaining budget.

    aggression in [0,1]: higher target_percent → modestly higher risk share
    within the daily envelope (not above it). Friction reserve ensures
    stop-out + costs cannot exceed the declared max daily risk envelope.
    """
    budget = float(remaining_budget_percent) - float(friction_reserve_percent)
    if budget <= 0 or stop_distance_pct <= 0:
        return 0.0
    # Cap single ticket to a fraction of the daily envelope
    cap = min(budget, max_daily_risk_percent * max_single_fraction)
    # Goal-conditioned aggression: high target uses more of remaining budget
    t_norm = min(max((target_percent - 5.0) / 85.0, 0.0), 1.0)
    # Base fraction of cap is high so multi-R fills can reach lower targets;
    # aggression/target still scales within the envelope (never above it).
    use_frac = 0.45 + 0.50 * float(np_clip(aggression, 0.0, 1.0)) * (0.35 + 0.65 * t_norm)
    use_frac = min(use_frac, 1.0)
    raw = cap * use_frac
    if raw < min_risk and budget >= min_risk:
        raw = min_risk
    return float(min(raw, budget, cap))


def np_clip(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, float(x)))


def apply_trade_result(
    ledger: DailyRiskLedger,
    *,
    pnl_percent: float,
    closed_risk_percent: float = 0.0,
) -> DailyRiskLedger:
    """Update realized PnL; if loss, track closed loss for breach audit."""
    ledger.realized_pnl_percent += float(pnl_percent)
    if pnl_percent < 0:
        ledger.closed_losses_percent += abs(float(pnl_percent))
    # Remove one matching open risk if provided
    if closed_risk_percent > 0 and ledger.positions:
        # pop first with similar risk
        for i, p in enumerate(ledger.positions):
            if abs(p.risk_percent - closed_risk_percent) < 1e-6:
                ledger.positions.pop(i)
                break
        else:
            ledger.positions.pop(0)
    return ledger


def risk_report(ledger: DailyRiskLedger) -> Dict[str, float]:
    return {
        "max_daily_risk_percent": float(ledger.max_daily_risk_percent),
        "open_risk_percent": ledger.open_risk_percent(),
        "worst_case_daily_loss_percent": ledger.worst_case_daily_loss_percent(),
        "remaining_budget_percent": ledger.remaining_risk_budget_percent(),
        "realized_pnl_percent": float(ledger.realized_pnl_percent),
        "friction_total_pct": float(ledger.friction.total_pct),
        "breach": 1.0 if ledger.worst_case_daily_loss_percent()
        > ledger.max_daily_risk_percent + 1e-9 else 0.0,
    }
