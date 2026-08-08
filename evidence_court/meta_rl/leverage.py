"""1:100 leverage + risk-legal max lot sizing (flea-jar full action space)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


LEVERAGE = 100.0  # 1:100


@dataclass(frozen=True)
class InstrumentSpec:
    symbol: str
    contract_size: float  # units per lot
    tick_size: float
    tick_value_per_lot: float  # account currency per tick per lot (approx)
    min_lot: float = 0.01
    lot_step: float = 0.01
    # approx $ move per 1.0 price unit per 1.0 lot (simplified)
    value_per_price_unit_per_lot: float = 100.0


# Simplified specs for shadow sim (not broker-certified)
INSTRUMENTS: Dict[str, InstrumentSpec] = {
    "XAUUSD": InstrumentSpec("XAUUSD", 100.0, 0.01, 1.0, value_per_price_unit_per_lot=100.0),
    "EURUSD": InstrumentSpec("EURUSD", 100_000.0, 0.00001, 1.0, value_per_price_unit_per_lot=10.0),
    "GBPUSD": InstrumentSpec("GBPUSD", 100_000.0, 0.00001, 1.0, value_per_price_unit_per_lot=10.0),
    "US30": InstrumentSpec("US30", 1.0, 0.1, 1.0, value_per_price_unit_per_lot=1.0),
}


def margin_required(equity: float, notional: float, leverage: float = LEVERAGE) -> float:
    return float(notional / max(leverage, 1e-9))


def risk_legal_max_lot(
    *,
    equity: float,
    risk_percent: float,
    entry_price: float,
    stop_distance_price: float,
    symbol: str,
    leverage: float = LEVERAGE,
) -> Dict[str, float]:
    """Max lot such that stop loss ≈ risk_percent of equity, under 1:100 margin.

    Returns lot, notional, margin, risk_dollars, risk_percent_actual.
    """
    spec = INSTRUMENTS.get(symbol, INSTRUMENTS["XAUUSD"])
    risk_dollars = equity * (risk_percent / 100.0)
    stop = max(abs(stop_distance_price), 1e-9)
    # loss per lot ≈ stop * value_per_price_unit_per_lot
    loss_per_lot = stop * spec.value_per_price_unit_per_lot
    if loss_per_lot <= 0:
        return {"lot": 0.0, "notional": 0.0, "margin": 0.0, "risk_dollars": 0.0, "risk_percent_actual": 0.0}

    lot_by_risk = risk_dollars / loss_per_lot
    # margin constraint: notional/leverage <= equity (simplified full margin use cap 50%)
    notional_per_lot = entry_price * spec.contract_size
    if notional_per_lot <= 0:
        notional_per_lot = entry_price * spec.value_per_price_unit_per_lot
    max_notional = equity * leverage * 0.5
    lot_by_margin = max_notional / max(notional_per_lot, 1e-9)
    lot = min(lot_by_risk, lot_by_margin)
    # quantize
    if lot < spec.min_lot:
        lot = 0.0
    else:
        steps = int(lot / spec.lot_step)
        lot = steps * spec.lot_step

    notional = lot * notional_per_lot
    margin = margin_required(equity, notional, leverage)
    risk_actual = lot * loss_per_lot
    return {
        "lot": float(lot),
        "notional": float(notional),
        "margin": float(margin),
        "risk_dollars": float(risk_actual),
        "risk_percent_actual": float(100.0 * risk_actual / max(equity, 1e-9)),
        "leverage": float(leverage),
        "loss_per_lot": float(loss_per_lot),
    }


def stop_distance_price_from_pct(entry: float, stop_pct: float) -> float:
    return abs(entry) * (stop_pct / 100.0)
