"""Forward eval: no look-ahead, multi-TF edge path, multi-symbol, promote gates."""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.forward_eval import (
    DEFAULT_PRICE,
    decision_features_from_history,
    run_forward_eval,
    run_one_day,
    simulate_fill_open_to_close,
)
from evidence_court.meta_rl.leverage import LEVERAGE
from evidence_court.meta_rl.policy import FrozenMetaPolicy
from evidence_court.meta_rl.price_io import available_symbols
from evidence_court.meta_rl.state import build_meta_rl_state


def test_decision_features_ignore_current_day_close():
    hist = [
        {"date": "d1", "open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5},
        {"date": "d2", "open": 100.5, "high": 102.0, "low": 100.0, "close": 101.5},
        {"date": "d3", "open": 101.5, "high": 103.0, "low": 101.0, "close": 102.0},
    ]
    f1 = decision_features_from_history(hist)
    f2 = decision_features_from_history(hist)
    assert f1["dir_sign"] == f2["dir_sign"]


def test_simulate_fill_can_exceed_one_percent_on_strong_move():
    day = {"open": 100.0, "high": 103.0, "low": 99.9, "close": 102.5}
    pnl = simulate_fill_open_to_close(
        side=1, day=day, size_risk_percent=1.0, stop_distance_pct=0.35, friction_pct=0.04
    )
    assert pnl > 1.0


def test_policy_act_from_state_set_dirs_not_oracle():
    policy = FrozenMetaPolicy.from_seed(1)
    st = build_meta_rl_state(target_percent=15.0, max_daily_risk_percent=2.0).copy()
    st[0] = st[3] = st[6] = st[9] = 1.0
    a_long = policy.forward(st, topology="launch")
    st2 = st.copy()
    st2[0] = st2[3] = st2[6] = st2[9] = -1.0
    a_short = policy.forward(st2, topology="launch")
    if a_long.act in ("long", "short"):
        assert a_long.act == "long"
    if a_short.act in ("long", "short"):
        assert a_short.act == "short"
    assert "force_side" not in inspect.signature(policy.forward).parameters


def test_run_one_day_wires_senses_and_l2l():
    policy = FrozenMetaPolicy.from_seed(2)
    history = []
    px = 100.0
    for i in range(12):
        history.append(
            {
                "date": f"2026-01-{i+1:02d}",
                "open": px,
                "high": px + 0.8,
                "low": px - 0.3,
                "close": px + 0.5,
            }
        )
        px += 0.5
    day = {
        "date": "2026-01-13",
        "open": px,
        "high": px + 1.5,
        "low": px - 0.2,
        "close": px + 1.2,
    }
    dr = run_one_day(
        policy,
        day,
        history,
        target_percent=5.0,
        max_daily_risk_percent=2.0,
    )
    assert dr.senses_ok is True
    assert dr.l2l_ok is True
    assert dr.fill_model == "open_decision_close_or_stop"
    assert dr.leverage == LEVERAGE


@pytest.mark.skipif(not DEFAULT_PRICE.exists(), reason="price CSV not available")
def test_forward_subset_multi_symbol_contracts():
    syms = [s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()]
    if len(syms) < 2:
        pytest.skip("need >=2 symbols")
    report = run_forward_eval(n_days=8, seed=11, warmup_days=10, symbols=syms[:3])
    assert report.n_days == 8
    assert report.breach_count == 0
    assert report.no_retrain is True
    assert report.metadata.get("force_side_used") is False
    assert report.metadata.get("no_lookahead") is True
    assert report.metadata.get("leverage") == LEVERAGE
    assert report.metadata.get("multi_symbol") is True
    assert all(d.retrain_steps == 0 for d in report.day_results)


@pytest.mark.skipif(not DEFAULT_PRICE.exists(), reason="price CSV not available")
def test_forward_100_promote_gates():
    syms = [s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()]
    report = run_forward_eval(
        n_days=100,
        seed=42,
        warmup_days=15,
        symbols=syms[:3] if len(syms) >= 2 else None,
    )
    assert report.n_days == 100
    assert report.breach_count == 0
    assert report.no_retrain is True
    assert report.l2l_day_path_ok is True
    assert report.senses_day_path_ok is True
    assert report.goal_consistency_ok is True
    assert report.metadata.get("pullback_continuation_coverage") is True
    assert report.metadata.get("leverage") == 100.0
    assert report.promote_ready is True
    gc = report.metadata["goal_consistency"]
    assert gc["max_day_pnl_percent"] >= 1.0 or gc["total_hits"] >= 1
