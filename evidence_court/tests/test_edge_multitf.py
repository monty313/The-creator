"""Multi-TF RSI5+BB pullback/continuation edge + 1:100 leverage (CASE-0002)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.edge import scan_all_sets
from evidence_court.meta_rl.indicators import bollinger, rsi
from evidence_court.meta_rl.leverage import LEVERAGE, risk_legal_max_lot
from evidence_court.meta_rl.sets import assert_mark_sets_law


def _synth_trend_m1(n_days: int = 40, up: bool = True) -> list:
    bars = []
    px = 2000.0
    for d in range(n_days):
        month = 3 if d < 28 else 4
        day = d + 1 if d < 28 else d - 27
        date = f"2026-{month:02d}-{day:02d}"
        for m in range(0, 180):
            drift = 0.12 if up else -0.12
            if d == n_days - 3 and 50 <= m < 90:
                drift = -0.3 if up else 0.3
            if d == n_days - 3 and m >= 90:
                drift = 0.4 if up else -0.4
            o = px
            c = px + drift
            bars.append(
                {
                    "date": date,
                    "time": f"{1 + m // 60:02d}:{m % 60:02d}:00",
                    "open": o,
                    "high": max(o, c) + 0.05,
                    "low": min(o, c) - 0.05,
                    "close": c,
                }
            )
            px = c
    return bars


def test_rsi_and_bb_shift_no_lookahead_length():
    rng = np.random.default_rng(0)
    closes = np.cumsum(rng.normal(0, 1, size=100)) + 100
    r = rsi(closes, 5)
    mid, up, lo = bollinger(closes, 10, 0.5, shift=2)
    assert r.shape == closes.shape
    assert mid.shape == closes.shape
    assert np.isnan(mid[0]) and np.isnan(mid[1])


def test_scan_all_four_mark_sets():
    assert_mark_sets_law()
    bars = _synth_trend_m1(20, up=True)
    snap = scan_all_sets(bars, symbol="XAUUSD")
    assert len(snap.set_edges) == 4
    assert {e.set_id for e in snap.set_edges} == {1, 2, 3, 4}


def test_uptrend_force_non_zero():
    bars = _synth_trend_m1(25, up=True)
    snap = scan_all_sets(bars, symbol="XAUUSD")
    assert abs(snap.consensus_force) > 0.0 or any(abs(e.force) > 0 for e in snap.set_edges)


def test_leverage_is_1_to_100_risk_legal_lot():
    assert LEVERAGE == 100.0
    info = risk_legal_max_lot(
        equity=100_000.0,
        risk_percent=1.0,
        entry_price=2000.0,
        stop_distance_price=7.0,
        symbol="XAUUSD",
        leverage=LEVERAGE,
    )
    assert info["leverage"] == 100.0
    assert info["lot"] > 0
    assert info["risk_percent_actual"] <= 1.05
    assert info["margin"] > 0
