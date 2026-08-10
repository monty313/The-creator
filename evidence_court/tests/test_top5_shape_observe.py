"""Top-5 method-first observe/reward — drives shipped Aaron_here tools."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from Aaron_here.tools.top5_shape_observe import (
    COMPONENTS,
    FIRE_LONG,
    FIRE_SHORT,
    METHOD_FIRST_REWARD,
    WAIT,
    observe_shapes,
    observe_shapes_frame,
    pack_state_vector,
    preferred_action,
    preferred_action_component,
    shape_reward,
    state_vector_keys,
)
from strategies.python_batch.mtf import SetBars


def _toy_setbars(n: int = 400) -> SetBars:
    """Synthetic OHLCV with mild uptrend so dual-HTF mass can form."""
    rng = np.random.default_rng(42)
    t = np.arange(n, dtype=float)
    close = 1.10 + 0.00002 * t + rng.normal(0, 0.00015, size=n)
    high = close + 0.0002
    low = close - 0.0002
    open_ = close - 0.00005
    idx = pd.date_range("2026-01-01", periods=n, freq="5min")
    s = lambda a: pd.Series(a, index=idx)
    # HTF: slower upward drift (force long-ish)
    h1 = 1.10 + 0.00003 * t
    h2 = 1.10 + 0.000025 * t
    return SetBars(
        name="toy",
        ltf="5m",
        htf1="30m",
        htf2="1h",
        open=s(open_),
        high=s(high),
        low=s(low),
        close=s(close),
        h1_open=s(h1 - 0.0001),
        h1_high=s(h1 + 0.0002),
        h1_low=s(h1 - 0.0002),
        h1_close=s(h1),
        h2_open=s(h2 - 0.0001),
        h2_high=s(h2 + 0.0002),
        h2_low=s(h2 - 0.0002),
        h2_close=s(h2),
    )


def test_components_are_top5_unique_geometries():
    assert set(COMPONENTS) == {
        "cci_gravity",
        "mcflurry",
        "sma_scalp",
        "bb_mtf",
        "guide_s01_ma_cross",
    }


def test_observe_frame_exposes_per_component_flr():
    sb = _toy_setbars()
    df = observe_shapes_frame(sb)
    for c in COMPONENTS:
        for field in (
            "force_sign",
            "force_strength",
            "load_flag",
            "load_depth",
            "reclaim_flag",
            "path_stage",
        ):
            col = f"{c}__{field}"
            assert col in df.columns, col
    assert "force_sign" in df.columns
    assert "path_stage" in df.columns
    assert len(df) == len(sb.close)


def test_method_first_reward_dominates_goal_candy():
    """Mud fire is punished even if fake PnL/goal progress is large."""
    assert METHOD_FIRST_REWARD["fire_valid_reclaim"] > METHOD_FIRST_REWARD["pnl_weight"]
    assert METHOD_FIRST_REWARD["fire_force0"] < 0

    mud = {
        "force_sign": 0.0,
        "load_flag": 0.0,
        "reclaim_flag": 0.0,
        "session_ok": 1.0,
        "structure_ok": 1.0,
        "risk_budget": 1.0,
        "n_components_force_agree": 0.0,
    }
    for c in COMPONENTS:
        mud[f"{c}__force_sign"] = 0.0
        mud[f"{c}__load_flag"] = 0.0
        mud[f"{c}__reclaim_flag"] = 0.0

    r_fire = shape_reward(mud, FIRE_LONG, pnl_scaled=5.0, goal_progress=5.0)
    r_wait = shape_reward(mud, WAIT, pnl_scaled=0.0, goal_progress=0.0)
    assert r_fire["method_reward"] < 0
    assert r_fire["total"] < r_wait["total"]
    # goal progress must not override method break
    assert r_fire["parts"].get("goal_progress", 0.0) == 0.0


def test_reclaim_fire_rewarded_method_first():
    st = {
        "force_sign": 1.0,
        "load_flag": 0.0,
        "reclaim_flag": 1.0,
        "session_ok": 1.0,
        "structure_ok": 1.0,
        "risk_budget": 1.0,
        "n_components_force_agree": 3.0,
    }
    for c in COMPONENTS:
        st[f"{c}__force_sign"] = 1.0
        st[f"{c}__load_flag"] = 0.0
        st[f"{c}__reclaim_flag"] = 1.0 if c == "cci_gravity" else 0.0
    r = shape_reward(st, FIRE_LONG, pnl_scaled=0.1, goal_progress=0.2)
    assert r["method_reward"] > 0
    assert r["method_reward"] > abs(r["goal_reward"])
    assert preferred_action(st) == FIRE_LONG


def test_dip_chase_penalized():
    st = {
        "force_sign": 1.0,
        "load_flag": 1.0,
        "reclaim_flag": 0.0,
        "session_ok": 1.0,
        "structure_ok": 1.0,
        "risk_budget": 1.0,
        "n_components_force_agree": 2.0,
    }
    for c in COMPONENTS:
        st[f"{c}__force_sign"] = 1.0
        st[f"{c}__load_flag"] = 1.0
        st[f"{c}__reclaim_flag"] = 0.0
    r = shape_reward(st, FIRE_LONG)
    assert r["parts"].get("fire_dip_chase", 0) < 0
    assert preferred_action(st) == WAIT


def test_pack_state_vector_length():
    st = observe_shapes(_toy_setbars(), goal_target=0.15, risk_budget=0.02)
    vec = pack_state_vector(st)
    assert vec.shape[0] == len(state_vector_keys())
    assert vec.dtype == np.float64


def test_preferred_action_component_independent():
    st = {f"{c}__force_sign": 0.0 for c in COMPONENTS}
    for c in COMPONENTS:
        st[f"{c}__load_flag"] = 0.0
        st[f"{c}__reclaim_flag"] = 0.0
    st["session_ok"] = 1.0
    st["structure_ok"] = 1.0
    st["risk_budget"] = 1.0
    st["mcflurry__force_sign"] = 1.0
    st["mcflurry__reclaim_flag"] = 1.0
    st["mcflurry__load_flag"] = 0.0
    assert preferred_action_component(st, "mcflurry") == FIRE_LONG
    assert preferred_action_component(st, "cci_gravity") == WAIT
