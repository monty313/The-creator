"""
Meta-RL observation + reward for top-5 strategy composites.

Method first, goal second:
  Force → Load → Reclaim → rails → (stress at eval)
  goal_target / risk_budget / PnL are SECONDARY in reward.

Each of the 5 ALM geometries is a named component in state:
  cci_gravity | mcflurry | sma_scalp | bb_mtf | guide_s01_ma_cross

Each component exposes:
  force_sign, force_strength, load_flag, load_depth, reclaim_flag
  + preferred path stage (0=mud wait, 1=force, 2=load wait, 3=reclaim fire)

Consensus (meta) force/load/reclaim is also provided for the method path.

Usage:
  from Aaron_here.tools.top5_shape_observe import (
      observe_shapes, observe_shapes_frame,
      shape_reward, preferred_action, METHOD_FIRST_REWARD,
  )
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

try:
    from strategies.python_batch import indicators as ind
    from strategies.python_batch.mtf import SetBars
except ImportError:  # pragma: no cover
    ind = None  # type: ignore
    SetBars = Any  # type: ignore

# Stable component ids (meta-policy must see these)
COMPONENTS: Tuple[str, ...] = (
    "cci_gravity",
    "mcflurry",
    "sma_scalp",
    "bb_mtf",
    "guide_s01_ma_cross",
)

WAIT, FIRE_LONG, FIRE_SHORT, EXIT = 0, 1, 2, 3

# --- Method-first reward weights (goal second) ---
METHOD_FIRST_REWARD = {
    # method path (dominant)
    "wait_force0": 0.20,
    "wait_during_load": 0.25,
    "fire_valid_reclaim": 1.20,
    "fire_force0": -1.80,
    "fire_dip_chase": -1.40,
    "fire_anti_force": -1.80,
    "fire_wrong_side_reclaim": -1.00,
    "fire_rails_off": -0.60,
    "component_align_bonus": 0.15,  # action matches a component's preferred fire
    "component_conflict_penalty": -0.10,  # fire when most components say wait/mud
    # goal second (small)
    "pnl_weight": 0.15,
    "goal_progress_weight": 0.10,  # optional: closer to goal_target without method break
    "risk_blow_penalty": -0.80,
}


def _cci_M(high, low, close) -> pd.Series:
    x = ind.cci(high, low, close, 20)
    x = ind.sma(x, 2)
    return ind.sma(x, 7) - ind.sma(x, 21)


def _rsi_M(close) -> pd.Series:
    r = ind.rsi(close, 13)
    r = ind.sma(r, 2)
    return ind.sma(r, 7) - ind.sma(r, 21)


def _cross_up(a: pd.Series, b: pd.Series) -> pd.Series:
    return (a > b) & (a.shift(1) <= b.shift(1))


def _cross_dn(a: pd.Series, b: pd.Series) -> pd.Series:
    return (a < b) & (a.shift(1) >= b.shift(1))


def _sign_force(bull: pd.Series, bear: pd.Series) -> pd.Series:
    s = pd.Series(0, index=bull.index, dtype=int)
    s = s.mask(bull.fillna(False) & ~bear.fillna(False), 1)
    s = s.mask(bear.fillna(False) & ~bull.fillna(False), -1)
    return s


def _bars_in_flag(flag: pd.Series) -> pd.Series:
    out = np.zeros(len(flag), dtype=float)
    age = 0.0
    arr = flag.fillna(0).astype(float).values
    for i in range(len(arr)):
        if arr[i] > 0.5:
            age += 1.0
        else:
            age = 0.0
        out[i] = age
    return pd.Series(out, index=flag.index)


def _bars_since_pulse(pulse: pd.Series) -> pd.Series:
    out = np.zeros(len(pulse), dtype=float)
    c = 999.0
    arr = pulse.fillna(False).astype(bool).values
    for i in range(len(arr)):
        if arr[i]:
            c = 0.0
        else:
            c = min(c + 1.0, 999.0)
        out[i] = c
    return pd.Series(out, index=pulse.index)


def _path_stage(force: pd.Series, load: pd.Series, reclaim: pd.Series) -> pd.Series:
    """0=mud, 1=force only, 2=load wait, 3=reclaim fire window."""
    st = pd.Series(0, index=force.index, dtype=int)
    st = st.mask(force != 0, 1)
    st = st.mask((force != 0) & (load > 0) & (reclaim < 1), 2)
    st = st.mask((force != 0) & (reclaim > 0), 3)
    return st


def _component_block(
    prefix: str,
    force: pd.Series,
    strength: pd.Series,
    load: pd.Series,
    depth: pd.Series,
    reclaim: pd.Series,
) -> Dict[str, pd.Series]:
    stage = _path_stage(force, load, reclaim)
    return {
        f"{prefix}__force_sign": force.astype(float),
        f"{prefix}__force_strength": strength.clip(0, 1).fillna(0),
        f"{prefix}__load_flag": load.astype(float),
        f"{prefix}__load_depth": depth.clip(0, 1).fillna(0),
        f"{prefix}__reclaim_flag": reclaim.astype(float),
        f"{prefix}__path_stage": stage.astype(float),
        f"{prefix}__bars_in_load": _bars_in_flag(load),
        f"{prefix}__bars_since_reclaim": _bars_since_pulse(reclaim.astype(bool)),
    }


def observe_shapes_frame(sb: "SetBars") -> pd.DataFrame:
    """
    Per-component F/L/R for all 5 strategies + consensus method path.
    """
    if ind is None:
        raise ImportError("strategies.python_batch required")

    idx = sb.close.index
    z = pd.Series(0.0, index=idx)

    # ========== 1) cci_gravity eyes ==========
    m_cci_1 = _cci_M(sb.h1_high, sb.h1_low, sb.h1_close)
    m_cci_2 = _cci_M(sb.h2_high, sb.h2_low, sb.h2_close)
    m_cci_l = _cci_M(sb.high, sb.low, sb.close)
    thr_cci = 8.0
    cci_force_b = (m_cci_1 > 0) & (m_cci_2 > 0) & (m_cci_1 >= thr_cci)
    cci_force_s = (m_cci_1 < 0) & (m_cci_2 < 0) & (m_cci_1 <= -thr_cci)
    cci_force = _sign_force(cci_force_b, cci_force_s)
    cci_str = (m_cci_1.abs().clip(upper=thr_cci) / thr_cci).where(cci_force != 0, 0.0)
    was_neg = m_cci_l.rolling(8, min_periods=1).min() < 0
    was_pos = m_cci_l.rolling(8, min_periods=1).max() > 0
    cci_load = (
        ((cci_force > 0) & (m_cci_l < 0)).astype(int)
        | ((cci_force < 0) & (m_cci_l > 0)).astype(int)
    )
    cci_rec = (
        ((cci_force > 0) & was_neg & _cross_up(m_cci_l, z)).astype(int)
        | ((cci_force < 0) & was_pos & _cross_dn(m_cci_l, z)).astype(int)
    )
    cci_depth = pd.Series(0.0, index=idx)
    cci_depth = cci_depth.mask(cci_force > 0, (-m_cci_l).clip(lower=0) / thr_cci)
    cci_depth = cci_depth.mask(cci_force < 0, m_cci_l.clip(lower=0) / thr_cci)

    # ========== 2) mcflurry eyes ==========
    m_rsi_1 = _rsi_M(sb.h1_close)
    m_rsi_2 = _rsi_M(sb.h2_close)
    m_rsi_l = _rsi_M(sb.close)
    thr_rsi = 1.5
    mcf_force_b = (m_rsi_1 > 0) & (m_rsi_2 > 0) & (m_rsi_1 >= thr_rsi)
    mcf_force_s = (m_rsi_1 < 0) & (m_rsi_2 < 0) & (m_rsi_1 <= -thr_rsi)
    mcf_force = _sign_force(mcf_force_b, mcf_force_s)
    mcf_str = (m_rsi_1.abs().clip(upper=thr_rsi * 3) / (thr_rsi * 3)).where(mcf_force != 0, 0.0)
    # load = eddy start (cross into wrong side) OR sitting wrong side under force
    mcf_load = (
        ((mcf_force > 0) & (m_rsi_l < 0)).astype(int)
        | ((mcf_force < 0) & (m_rsi_l > 0)).astype(int)
    )
    mcf_rec = (
        ((mcf_force > 0) & _cross_up(m_rsi_l, z)).astype(int)
        | ((mcf_force < 0) & _cross_dn(m_rsi_l, z)).astype(int)
    )
    mcf_depth = pd.Series(0.0, index=idx)
    mcf_depth = mcf_depth.mask(mcf_force > 0, (-m_rsi_l).clip(lower=0) / (thr_rsi * 3))
    mcf_depth = mcf_depth.mask(mcf_force < 0, m_rsi_l.clip(lower=0) / (thr_rsi * 3))

    # ========== 3) sma_scalp eyes ==========
    sma100_1 = ind.sma(sb.h1_close, 100)
    sma100_2 = ind.sma(sb.h2_close, 100)
    f8, s21, s50 = ind.sma(sb.close, 8), ind.sma(sb.close, 21), ind.sma(sb.close, 50)
    rsi14 = ind.rsi(sb.close, 14)
    ribbon_up = (f8 > s21) & (s21 > s50)
    ribbon_dn = (f8 < s21) & (s21 < s50)
    sma_force_b = (sb.h1_close > sma100_1) & (sb.h2_close > sma100_2)
    sma_force_s = (sb.h1_close < sma100_1) & (sb.h2_close < sma100_2)
    sma_force = _sign_force(sma_force_b, sma_force_s)
    # strength: distance from SMA100 on htf1
    sma_str = (
        (sb.h1_close - sma100_1).abs() / sb.h1_close.replace(0, np.nan)
    ).clip(0, 0.01) / 0.01
    sma_str = sma_str.where(sma_force != 0, 0.0).fillna(0)
    sma_load = (
        ((sma_force > 0) & ribbon_up & (sb.low <= s21) & (sb.close > s21) & (rsi14 < 55)).astype(int)
        | ((sma_force < 0) & ribbon_dn & (sb.high >= s21) & (sb.close < s21) & (rsi14 > 45)).astype(int)
    )
    sma_rec = (
        ((sma_force > 0) & _cross_up(f8, s21) & ribbon_up).astype(int)
        | ((sma_force < 0) & _cross_dn(f8, s21) & ribbon_dn).astype(int)
    )
    sma_depth = pd.Series(0.0, index=idx)
    sma_depth = sma_depth.mask(sma_load > 0, (s21 - sb.close).abs() / sb.close.replace(0, np.nan) * 100)
    sma_depth = sma_depth.clip(0, 1).fillna(0)

    # ========== 4) bb_mtf eyes ==========
    bb_lo, bb_mid, bb_hi = ind.bollinger(sb.close, 20, 2.0, 0)
    bb_mid_1 = ind.bollinger(sb.h1_close, 20, 2.0, 0)[1]
    bb_mid_2 = ind.bollinger(sb.h2_close, 20, 2.0, 0)[1]
    bb_force_b = (sb.h1_close > bb_mid_1) & (sb.h2_close > bb_mid_2)
    bb_force_s = (sb.h1_close < bb_mid_1) & (sb.h2_close < bb_mid_2)
    bb_force = _sign_force(bb_force_b, bb_force_s)
    bb_str = (
        (sb.h1_close - bb_mid_1).abs() / sb.h1_close.replace(0, np.nan)
    ).clip(0, 0.01) / 0.01
    bb_str = bb_str.where(bb_force != 0, 0.0).fillna(0)
    bb_load = (
        ((bb_force > 0) & (sb.close < bb_lo) & (rsi14 < 40)).astype(int)
        | ((bb_force < 0) & (sb.close > bb_hi) & (rsi14 > 60)).astype(int)
    )
    # also mild load: stretch toward outer band with force
    bb_load = bb_load | (
        ((bb_force > 0) & (sb.close < bb_mid) & (rsi14 < 45)).astype(int)
        | ((bb_force < 0) & (sb.close > bb_mid) & (rsi14 > 55)).astype(int)
    )
    bb_rec = (
        ((bb_force > 0) & _cross_up(sb.close, bb_mid) & (rsi14 > 45)).astype(int)
        | ((bb_force < 0) & _cross_dn(sb.close, bb_mid) & (rsi14 < 55)).astype(int)
    )
    band_w = (bb_hi - bb_lo).replace(0, np.nan)
    bb_depth = ((bb_mid - sb.close).abs() / band_w).clip(0, 1).fillna(0)
    bb_depth = bb_depth.where(bb_load > 0, 0.0)

    # ========== 5) guide_s01_ma_cross eyes ==========
    sma50_l, sma200_l = ind.sma(sb.close, 50), ind.sma(sb.close, 200)
    sma50_1, sma200_1 = ind.sma(sb.h1_close, 50), ind.sma(sb.h1_close, 200)
    sma50_2, sma200_2 = ind.sma(sb.h2_close, 50), ind.sma(sb.h2_close, 200)
    ma_force_b = (
        (sma50_1 > sma200_1)
        & (sma50_2 > sma200_2)
        & (sma50_1 > sma50_1.shift(3))
    )
    ma_force_s = (
        (sma50_1 < sma200_1)
        & (sma50_2 < sma200_2)
        & (sma50_1 < sma50_1.shift(3))
    )
    ma_force = _sign_force(ma_force_b, ma_force_s)
    ma_str = (
        (sma50_1 - sma200_1).abs() / sb.h1_close.replace(0, np.nan)
    ).clip(0, 0.01) / 0.01
    ma_str = ma_str.where(ma_force != 0, 0.0).fillna(0)
    ma_load = (
        ((ma_force > 0) & (sb.low <= sma50_l) & (sb.close > sma50_l)).astype(int)
        | ((ma_force < 0) & (sb.high >= sma50_l) & (sb.close < sma50_l)).astype(int)
    )
    ma_rec = (
        ((ma_force > 0) & _cross_up(sma50_l, sma200_l) & (sma50_l > sma50_l.shift(3))).astype(int)
        | ((ma_force < 0) & _cross_dn(sma50_l, sma200_l) & (sma50_l < sma50_l.shift(3))).astype(int)
    )
    # bounce reclaim alternative: tag 50 then close back with force
    ma_rec = ma_rec | (
        ((ma_force > 0) & (sb.low <= sma50_l) & (sb.close > sma50_l) & (sb.close > sb.open)).astype(int)
        | ((ma_force < 0) & (sb.high >= sma50_l) & (sb.close < sma50_l) & (sb.close < sb.open)).astype(int)
    )
    ma_depth = pd.Series(0.0, index=idx)
    ma_depth = ma_depth.mask(ma_load > 0, (sma50_l - sb.close).abs() / sb.close.replace(0, np.nan) * 50)
    ma_depth = ma_depth.clip(0, 1).fillna(0)

    # --- pack per-component blocks ---
    blocks = {}
    blocks.update(
        _component_block("cci_gravity", cci_force, cci_str, cci_load, cci_depth.clip(0, 1), cci_rec)
    )
    blocks.update(
        _component_block("mcflurry", mcf_force, mcf_str, mcf_load, mcf_depth.clip(0, 1), mcf_rec)
    )
    blocks.update(
        _component_block("sma_scalp", sma_force, sma_str, sma_load, sma_depth, sma_rec)
    )
    blocks.update(
        _component_block("bb_mtf", bb_force, bb_str, bb_load, bb_depth, bb_rec)
    )
    blocks.update(
        _component_block("guide_s01_ma_cross", ma_force, ma_str, ma_load, ma_depth, ma_rec)
    )

    # --- sensor coordinates (eyes, not actions) ---
    eyes = {
        "eye_m_cci_htf1": m_cci_1,
        "eye_m_cci_ltf": m_cci_l,
        "eye_m_rsi_htf1": m_rsi_1,
        "eye_m_rsi_ltf": m_rsi_l,
        "eye_rsi14": rsi14,
        "eye_ribbon_up": ribbon_up.astype(float),
        "eye_ribbon_dn": ribbon_dn.astype(float),
        "eye_bb_stretch": ((sb.close - bb_mid) / band_w).fillna(0),
        "eye_sma50_vs_200": (sma50_l - sma200_l),
    }

    # --- consensus method path (meta) ---
    force_stack = pd.concat(
        [cci_force, mcf_force, sma_force, bb_force, ma_force], axis=1
    )
    votes_long = (force_stack > 0).sum(axis=1)
    votes_short = (force_stack < 0).sum(axis=1)
    force_sign = pd.Series(0, index=idx, dtype=int)
    force_sign = force_sign.mask((votes_long >= 2) & (votes_long > votes_short), 1)
    force_sign = force_sign.mask((votes_short >= 2) & (votes_short > votes_long), -1)

    strength_stack = pd.concat(
        [cci_str, mcf_str, sma_str, bb_str, ma_str], axis=1
    )
    force_strength = strength_stack.mean(axis=1).where(force_sign != 0, 0.0).clip(0, 1)

    load_stack = pd.concat([cci_load, mcf_load, sma_load, bb_load, ma_load], axis=1)
    # consensus load: any component load that agrees with consensus force
    load_flag = (
        ((force_sign > 0) & (load_stack.gt(0).any(axis=1))).astype(int)
        | ((force_sign < 0) & (load_stack.gt(0).any(axis=1))).astype(int)
    )
    # only count load under force
    load_flag = load_flag.where(force_sign != 0, 0)

    depth_stack = pd.concat([cci_depth, mcf_depth, sma_depth, bb_depth, ma_depth], axis=1)
    load_depth = depth_stack.max(axis=1).where(load_flag > 0, 0.0).clip(0, 1)

    rec_stack = pd.concat([cci_rec, mcf_rec, sma_rec, bb_rec, ma_rec], axis=1)
    reclaim_flag = (
        ((force_sign > 0) & (rec_stack.gt(0).any(axis=1))).astype(int)
        | ((force_sign < 0) & (rec_stack.gt(0).any(axis=1))).astype(int)
    )
    reclaim_flag = reclaim_flag.where(force_sign != 0, 0)

    n_force_agree = votes_long.where(force_sign > 0, votes_short).where(force_sign != 0, 0)
    n_load_agree = load_stack.gt(0).sum(axis=1).where(load_flag > 0, 0)
    n_reclaim_agree = rec_stack.gt(0).sum(axis=1).where(reclaim_flag > 0, 0)

    method = {
        "force_sign": force_sign.astype(float),
        "force_strength": force_strength,
        "load_flag": load_flag.astype(float),
        "load_depth": load_depth,
        "reclaim_flag": reclaim_flag.astype(float),
        "path_stage": _path_stage(force_sign, load_flag, reclaim_flag).astype(float),
        "bars_in_load": _bars_in_flag(load_flag),
        "bars_since_reclaim": _bars_since_pulse(reclaim_flag.astype(bool)),
        "n_components_force_agree": n_force_agree.astype(float),
        "n_components_load": n_load_agree.astype(float),
        "n_components_reclaim": n_reclaim_agree.astype(float),
        "votes_long": votes_long.astype(float),
        "votes_short": votes_short.astype(float),
    }

    df = pd.DataFrame({**eyes, **blocks, **method}, index=idx)
    return df


def observe_shapes(
    sb: "SetBars",
    *,
    position: int = 0,
    bars_in_trade: int = 0,
    goal_target: float = 0.0,
    risk_budget: float = 1.0,
    session_ok: float = 1.0,
    structure_ok: float = 1.0,
    i: int = -1,
) -> Dict[str, float]:
    """Single-bar meta state: all 5 components + consensus + context."""
    df = observe_shapes_frame(sb)
    row = df.iloc[i]
    out = {k: float(row[k]) if pd.notna(row[k]) else 0.0 for k in df.columns}
    # goal/risk context — SECOND to method in reward, but always visible in state
    out["position"] = float(position)
    out["bars_in_trade"] = float(bars_in_trade)
    out["goal_target"] = float(goal_target)
    out["risk_budget"] = float(risk_budget)
    out["session_ok"] = float(session_ok)
    out["structure_ok"] = float(structure_ok)
    return out


def state_vector_keys() -> List[str]:
    """Documented key order for meta-policy input packing."""
    keys: List[str] = []
    for c in COMPONENTS:
        keys += [
            f"{c}__force_sign",
            f"{c}__force_strength",
            f"{c}__load_flag",
            f"{c}__load_depth",
            f"{c}__reclaim_flag",
            f"{c}__path_stage",
            f"{c}__bars_in_load",
            f"{c}__bars_since_reclaim",
        ]
    keys += [
        "force_sign",
        "force_strength",
        "load_flag",
        "load_depth",
        "reclaim_flag",
        "path_stage",
        "bars_in_load",
        "bars_since_reclaim",
        "n_components_force_agree",
        "n_components_load",
        "n_components_reclaim",
        "position",
        "bars_in_trade",
        "goal_target",
        "risk_budget",
        "session_ok",
        "structure_ok",
    ]
    return keys


def pack_state_vector(state: Dict[str, float]) -> np.ndarray:
    keys = state_vector_keys()
    return np.asarray([float(state.get(k, 0.0)) for k in keys], dtype=np.float64)


def _rails_ok(state: Dict[str, float]) -> bool:
    return (
        state.get("session_ok", 1.0) > 0.5
        and state.get("structure_ok", 1.0) > 0.5
        and state.get("risk_budget", 1.0) > 0.05
    )


def preferred_action(state: Dict[str, float]) -> int:
    """Method path teacher action (consensus)."""
    f = int(state.get("force_sign", 0))
    load = state.get("load_flag", 0) > 0.5
    rec = state.get("reclaim_flag", 0) > 0.5
    if f == 0:
        return WAIT
    if rec and _rails_ok(state):
        return FIRE_LONG if f > 0 else FIRE_SHORT
    if load:
        return WAIT
    return WAIT


def preferred_action_component(state: Dict[str, float], component: str) -> int:
    """What ONE strategy composite would prefer under F→L→R."""
    f = int(state.get(f"{component}__force_sign", 0))
    load = state.get(f"{component}__load_flag", 0) > 0.5
    rec = state.get(f"{component}__reclaim_flag", 0) > 0.5
    if f == 0:
        return WAIT
    if rec and _rails_ok(state):
        return FIRE_LONG if f > 0 else FIRE_SHORT
    if load:
        return WAIT
    return WAIT


def shape_reward(
    state: Dict[str, float],
    action: int,
    *,
    pnl_scaled: float = 0.0,
    goal_progress: float = 0.0,
    risk_blown: bool = False,
    w: Dict[str, float] | None = None,
) -> Dict[str, float]:
    """
    Method first, goal second.

    Returns dict with total and breakdown:
      method_reward  (dominant)
      goal_reward    (secondary — PnL / goal progress / risk)
      total

    Never optimizes win-rate.
    """
    W = dict(METHOD_FIRST_REWARD)
    if w:
        W.update(w)

    f = int(state.get("force_sign", 0))
    load = state.get("load_flag", 0) > 0.5
    rec = state.get("reclaim_flag", 0) > 0.5
    rails = _rails_ok(state)
    method = 0.0
    parts: Dict[str, float] = {}

    # ----- METHOD PATH (first) -----
    if f == 0:
        if action in (WAIT, EXIT):
            method += W["wait_force0"]
            parts["wait_force0"] = W["wait_force0"]
        if action in (FIRE_LONG, FIRE_SHORT):
            method += W["fire_force0"]
            parts["fire_force0"] = W["fire_force0"]
    else:
        if load and not rec:
            if action == WAIT:
                method += W["wait_during_load"]
                parts["wait_during_load"] = W["wait_during_load"]
            if (action == FIRE_LONG and f > 0) or (action == FIRE_SHORT and f < 0):
                method += W["fire_dip_chase"]
                parts["fire_dip_chase"] = W["fire_dip_chase"]

        if rec:
            if not rails and action in (FIRE_LONG, FIRE_SHORT):
                method += W["fire_rails_off"]
                parts["fire_rails_off"] = W["fire_rails_off"]
            elif rails:
                if action == FIRE_LONG and f > 0:
                    method += W["fire_valid_reclaim"]
                    parts["fire_valid_reclaim"] = W["fire_valid_reclaim"]
                elif action == FIRE_SHORT and f < 0:
                    method += W["fire_valid_reclaim"]
                    parts["fire_valid_reclaim"] = W["fire_valid_reclaim"]
                elif action in (FIRE_LONG, FIRE_SHORT):
                    method += W["fire_wrong_side_reclaim"]
                    parts["fire_wrong_side_reclaim"] = W["fire_wrong_side_reclaim"]

        if action == FIRE_LONG and f < 0:
            method += W["fire_anti_force"]
            parts["fire_anti_force"] = W["fire_anti_force"]
        if action == FIRE_SHORT and f > 0:
            method += W["fire_anti_force"]
            parts["fire_anti_force"] = W["fire_anti_force"]

    # component-level method alignment (meta-learning signal)
    fire_comp = 0
    wait_comp = 0
    for c in COMPONENTS:
        pa = preferred_action_component(state, c)
        if pa == action and action in (FIRE_LONG, FIRE_SHORT):
            fire_comp += 1
        if pa == WAIT and action == WAIT:
            wait_comp += 1
    if action in (FIRE_LONG, FIRE_SHORT) and fire_comp > 0:
        b = W["component_align_bonus"] * fire_comp
        method += b
        parts["component_align_bonus"] = b
    if action in (FIRE_LONG, FIRE_SHORT) and fire_comp == 0 and float(state.get("n_components_force_agree", 0)) < 2:
        method += W["component_conflict_penalty"]
        parts["component_conflict_penalty"] = W["component_conflict_penalty"]
    if action == WAIT and wait_comp >= 3:
        b = W["component_align_bonus"] * 0.5
        method += b
        parts["component_wait_align"] = b

    # ----- GOAL SECOND -----
    goal = 0.0
    goal += W["pnl_weight"] * float(pnl_scaled)
    parts["pnl_secondary"] = W["pnl_weight"] * float(pnl_scaled)
    # only count goal progress if method not badly broken this step
    method_broken = parts.get("fire_force0", 0) < 0 or parts.get("fire_dip_chase", 0) < 0 or parts.get("fire_anti_force", 0) < 0
    if not method_broken:
        goal += W["goal_progress_weight"] * float(goal_progress)
        parts["goal_progress"] = W["goal_progress_weight"] * float(goal_progress)
    else:
        parts["goal_progress"] = 0.0  # method first: no goal candy for bad shape
    if risk_blown or state.get("risk_budget", 1.0) <= 0:
        goal += W["risk_blow_penalty"]
        parts["risk_blow"] = W["risk_blow_penalty"]

    total = method + goal
    return {
        "total": total,
        "method_reward": method,
        "goal_reward": goal,
        "method_first": True,
        "parts": parts,
    }


def shape_reward_scalar(
    state: Dict[str, float],
    action: int,
    **kwargs,
) -> float:
    return float(shape_reward(state, action, **kwargs)["total"])
