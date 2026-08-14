"""Tests: CCI active-flat base + one pullback teach-agent per strategy (lab)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.strategy_teach_agents import (
    PRESSURE_IDLE_ACTIVE,
    PRESSURE_IN_TRADE,
    PRESSURE_LOADED,
    PRESSURE_MUST_JUSTIFY,
    PRESSURE_NO_TRADE,
    TEACHER_LONG,
    TEACHER_SHORT,
    TEACHER_WAIT,
    active_flat_pressure,
    build_pullback_teach_roster,
    cci_active_envelope,
    harvest_agent_pullback_teachers,
    harvest_all_pullback_teachers,
    validate_roster,
)
from strategies.python_batch.families import FAMILY_META, entries_for_mode
from strategies.python_batch.mtf import build_set


def _toy_m1(n: int = 12_000, seed: int = 42, drift: float = 0.0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2024-06-01", periods=n, freq="1min")
    rets = rng.normal(drift, 0.00012, size=n)
    close = 1.10 + np.cumsum(rets)
    high = close + rng.uniform(0, 0.00025, size=n)
    low = close - rng.uniform(0, 0.00025, size=n)
    open_ = np.roll(close, 1)
    open_[0] = close[0]
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close}, index=idx
    )


def _strong_trend_m1(n: int = 20_000, seed: int = 7) -> pd.DataFrame:
    """Sustained uptrend so dual-HTF CCI M-line can print force."""
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2024-03-01", periods=n, freq="1min")
    # strong positive drift + mild noise
    rets = rng.normal(0.00008, 0.00005, size=n)
    close = 1.05 + np.cumsum(rets)
    high = close + 0.00015
    low = close - 0.00008
    open_ = np.roll(close, 1)
    open_[0] = close[0]
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close}, index=idx
    )


def test_roster_one_agent_one_pullback_strategy_cci_base():
    roster = build_pullback_teach_roster()
    validate_roster(roster)
    assert len(roster) == 8
    assert roster[0].role == "active_flat_base"
    assert roster[0].family_id == "cci_gravity_scalp"
    assert roster[0].agent_id == "base_cci"
    assert all(a.mode == "pullback" for a in roster)
    assert len({a.agent_id for a in roster}) == len(roster)
    assert len({a.family_id for a in roster}) == len(roster)
    for a in roster:
        assert a.family_id in FAMILY_META
        assert getattr(a.family_fn, "family_id") == a.family_id


def test_validate_roster_rejects_duplicate_family():
    roster = build_pullback_teach_roster()
    bad = list(roster)
    # clone specialist family onto another agent
    twin = bad[1]
    bad[2] = type(twin)(
        agent_id="dup",
        family_id=twin.family_id,
        role="specialist",
        mode="pullback",
        title="dup",
        family_fn=twin.family_fn,
    )
    with pytest.raises(ValueError, match="duplicate family"):
        validate_roster(bad)


def test_active_flat_pressure_unit_table():
    """Direct pressure table: force off / loaded / reclaim / idle / in-trade."""
    idx = pd.date_range("2024-01-01", periods=5, freq="15min")
    false = pd.Series(False, index=idx)
    env = {
        "bull_force": pd.Series([False, True, True, True, True], index=idx),
        "bear_force": false.copy(),
        "force_on": pd.Series([False, True, True, True, True], index=idx),
        "load_long": pd.Series([False, True, False, False, False], index=idx),
        "load_short": false.copy(),
        "reclaim_long": pd.Series([False, False, True, False, False], index=idx),
        "reclaim_short": false.copy(),
    }
    in_trade = pd.Series([False, False, False, False, True], index=idx)
    # bar0 force off; bar1 loaded; bar2 reclaim; bar3 active idle; bar4 in trade
    # clear load/reclaim on bar3
    df = active_flat_pressure(env, bot_in_trade=in_trade)
    assert df.loc[idx[0], "pressure"] == PRESSURE_NO_TRADE
    assert df.loc[idx[0], "teacher_act"] == TEACHER_WAIT
    assert bool(df.loc[idx[0], "justified_wait"]) is True

    assert df.loc[idx[1], "pressure"] == PRESSURE_LOADED
    assert df.loc[idx[1], "teacher_act"] == TEACHER_WAIT
    assert bool(df.loc[idx[1], "justified_wait"]) is True

    assert df.loc[idx[2], "pressure"] == PRESSURE_MUST_JUSTIFY
    assert df.loc[idx[2], "teacher_act"] == TEACHER_LONG
    assert bool(df.loc[idx[2], "justified_wait"]) is False

    assert df.loc[idx[3], "pressure"] == PRESSURE_IDLE_ACTIVE
    assert df.loc[idx[3], "teacher_act"] == TEACHER_WAIT
    assert bool(df.loc[idx[3], "justified_wait"]) is False
    assert df.loc[idx[3], "side_hint"] == "long"

    assert df.loc[idx[4], "pressure"] == PRESSURE_IN_TRADE


def test_cci_envelope_and_families_run_on_toy_bars():
    m1 = _toy_m1(10_000)
    sb = build_set(m1, "set2_5m_30m_1h")
    env = cci_active_envelope(sb)
    assert set(env) >= {
        "bull_force",
        "bear_force",
        "force_on",
        "load_long",
        "load_short",
        "reclaim_long",
        "reclaim_short",
    }
    assert len(env["force_on"]) == len(sb.close)
    pressure = active_flat_pressure(env)
    assert set(pressure["pressure"].unique()) <= {
        PRESSURE_NO_TRADE,
        PRESSURE_LOADED,
        PRESSURE_MUST_JUSTIFY,
        PRESSURE_IDLE_ACTIVE,
        PRESSURE_IN_TRADE,
    }
    roster = build_pullback_teach_roster()
    for agent in roster:
        long_e, short_e = entries_for_mode(sb, agent.family_fn, "pullback")
        assert len(long_e) == len(sb.close)
        assert long_e.dtype == bool or str(long_e.dtype) == "bool"


def test_harvest_all_agents_under_strong_trend():
    """End-to-end: CCI force prints; roster harvests under activity envelope."""
    m1 = _strong_trend_m1(24_000)
    sb = build_set(m1, "set2_5m_30m_1h")
    # Lab pin: thr=1.0 guarantees force on crafted uptrend; production family still thr=8
    report = harvest_all_pullback_teachers(
        sb, require_cci_force=True, max_events_per_agent=50, force_thr=1.0
    )
    assert report["n_force_bars"] > 0
    assert report["promoted"] is False
    assert report["lab"] is True
    assert "base_cci" in report["teachers_by_agent"]
    assert isinstance(report["teachers_by_agent"]["base_cci"], list)
    for aid, rows in report["teachers_by_agent"].items():
        assert isinstance(rows, list), aid
        for row in rows:
            assert row["agent_id"] == aid
            assert row["mode"] == "pullback"
            assert row["source"] == "strategy_teach_agent_lab"
            assert row["teacher_act"] in (TEACHER_LONG, TEACHER_SHORT, TEACHER_WAIT)
            assert row["force_on"] is True


def test_base_agent_must_justify_emits_fire_teacher():
    """When reclaim prints under force + flat, base harvest emits long/short teacher."""
    m1 = _strong_trend_m1(24_000)
    sb = build_set(m1, "set3_15m_1h_4h")
    env = cci_active_envelope(sb, force_thr=1.0)
    pressure = active_flat_pressure(env)
    must = pressure[pressure["pressure"] == PRESSURE_MUST_JUSTIFY]
    if must.empty:
        pytest.skip("no reclaim under this toy window — envelope API still covered above")
    base = build_pullback_teach_roster()[0]
    rows = harvest_agent_pullback_teachers(
        base, sb, env=env, require_cci_force=True, max_events=80
    )
    fire = [r for r in rows if r["teacher_act"] in (TEACHER_LONG, TEACHER_SHORT)]
    assert fire, "base CCI must emit fire teachers on must_justify / PB reclaim"
    assert any(
        r["reason"]
        in (
            "cci_reclaim_must_justify_wait",
            "agent_pullback_long",
            "agent_pullback_short",
        )
        for r in fire
    )
