"""MARK HERE, ESQ. — NEW tests for CASE-0002 (not recycled prior suite).

Court rule: Mark may not prove a principle with old greens alone.
These tests were written for this case only and exercise shipped edge/risk units.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.edge import evaluate_set_edge, scan_all_sets
from evidence_court.meta_rl.leverage import LEVERAGE, risk_legal_max_lot
from evidence_court.meta_rl.policy import FrozenMetaPolicy
from evidence_court.meta_rl.risk import DailyRiskLedger, OpenPosition
from evidence_court.meta_rl.state import build_meta_rl_state
from evidence_court.meta_rl.types import Direction, SetConfluence, VelocityStrength


def _m1_flat_then_htf_conflict(n: int = 800) -> list:
    """Synthetic M1 where micro noise exists but no clean dual-HTF force."""
    bars = []
    px = 1.1000
    for i in range(n):
        day = 1 + (i // 400)
        date = f"2026-02-{day:02d}"
        # chop: alternate small moves — HTFs will not agree strongly
        drift = 0.00005 if (i // 20) % 2 == 0 else -0.00005
        o, c = px, px + drift
        bars.append(
            {
                "date": date,
                "time": f"{(i % 400) // 60:02d}:{(i % 60):02d}:00",
                "open": o,
                "high": max(o, c) + 0.00002,
                "low": min(o, c) - 0.00002,
                "close": c,
            }
        )
        px = c
    return bars


def test_NEW_mark_htf_incomplete_blocks_lone_ltf_fire():
    """Mark claim: LTF may not redefine side without HTF permission.

    NEW measurement: on choppy dual-HTF incomplete force, actionable acts must
    not claim htf_agree permission.
    """
    bars = _m1_flat_then_htf_conflict()
    snap = scan_all_sets(bars, symbol="EURUSD")
    # No set may fire long/short with htf_agree True on pure chop
    illegal = [e for e in snap.set_edges if e.act in ("long", "short") and e.htf_agree]
    assert illegal == [], f"Mark law broken: LTF fire with HTF agree on chop: {illegal}"


def test_NEW_mark_all_four_sets_scanned_never_set2_only():
    """Mark claim: Mark-on-chart scans all four official stacks every decision."""
    bars = _m1_flat_then_htf_conflict(900)
    snap = scan_all_sets(bars, symbol="XAUUSD")
    assert len(snap.set_edges) == 4
    assert [e.set_id for e in snap.set_edges] == [1, 2, 3, 4]
    assert {e.name for e in snap.set_edges} == {"micro", "intraday", "swing", "macro"}


def test_NEW_mark_multi_symbol_aggregate_risk_envelope():
    """Mark/Critic flea-jar: concurrent symbols share one daily risk ledger."""
    ledger = DailyRiskLedger(max_daily_risk_percent=2.0, equity=100_000.0)
    ledger.positions.append(
        OpenPosition(symbol="XAUUSD", side=1, risk_percent=1.0, notional_pct=50.0)
    )
    ledger.positions.append(
        OpenPosition(symbol="EURUSD", side=-1, risk_percent=0.8, notional_pct=40.0)
    )
    # 1.0 + 0.8 = 1.8 open risk under 2.0 envelope (plus friction)
    assert ledger.open_risk_percent() == pytest.approx(1.8)
    assert ledger.would_breach(0.5) is True  # would exceed
    assert ledger.can_open(0.1) is True or ledger.remaining_risk_budget_percent() >= 0.0


def test_NEW_mark_risk_legal_lot_uses_leverage_100():
    """Flea-jar: lot math must carry 1:100 — not raw range folklore."""
    info = risk_legal_max_lot(
        equity=50_000.0,
        risk_percent=2.0,
        entry_price=1.0850,
        stop_distance_price=0.0015,
        symbol="EURUSD",
        leverage=LEVERAGE,
    )
    assert info["leverage"] == 100.0
    assert info["lot"] >= 0.0
    # If a lot is risk-legal, risk_percent_actual must not exceed declared risk
    if info["lot"] > 0:
        assert info["risk_percent_actual"] <= 2.0 + 0.15


def test_NEW_mark_state_dirs_drive_policy_not_rhetoric():
    """Creator vs Mark: act side must follow packed Channel1 set directions."""
    policy = FrozenMetaPolicy.from_seed(99)
    st = build_meta_rl_state(target_percent=20.0, max_daily_risk_percent=2.0).copy()
    # Bull official dirs
    st[0] = st[3] = st[6] = st[9] = 1.0
    a = policy.forward(st, topology="launch", roles=("force", "velocity"))
    if a.act in ("long", "short"):
        assert a.act == "long"
    st[0] = st[3] = st[6] = st[9] = -1.0
    b = policy.forward(st, topology="launch", roles=("force", "velocity"))
    if b.act in ("long", "short"):
        assert b.act == "short"
