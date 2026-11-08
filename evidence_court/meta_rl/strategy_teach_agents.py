"""LAB — one teach-agent per pullback strategy; CCI gravity as active-flat base.

Quarantine: experimental curriculum road. Not Court-PROMOTED production path.
Does not replace CASE-0037 champion. Agents emit teacher *labels* only.

Design (Monty):
- CCI gravity owns the activity envelope: while dual-HTF CCI force is on and the
  bot is flat, silence must be justified (loaded / kill / reclaim fire).
- Specialist agents each own one distinct pullback geometry and harvest PB-mode
  teachers under that same envelope — one family per agent, no soup.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Sequence

import pandas as pd

from strategies.python_batch import indicators as ind
from strategies.python_batch.families import (
    FAMILY_META,
    FamilyFn,
    entries_for_mode,
    fam_cci_gravity,
    fam_dimension_jump,
    fam_mark_rsi_bb,
    fam_mcflurry,
    fam_s1_cci,
    fam_s4_rsi_snap,
    fam_sma_scalp,
    fam_snap8,
)
from strategies.python_batch.mtf import SetBars

# Pressure labels for active-flat interrogation (CCI base).
PRESSURE_NO_TRADE = "no_trade"
PRESSURE_LOADED = "loaded_not_yet"
PRESSURE_MUST_JUSTIFY = "must_justify_wait"
PRESSURE_IN_TRADE = "in_trade_ok"
PRESSURE_IDLE_ACTIVE = "active_idle"

TEACHER_WAIT = "wait"
TEACHER_LONG = "long"
TEACHER_SHORT = "short"


@dataclass(frozen=True)
class StrategyTeachAgent:
    """One agent → one family → one teaching job."""

    agent_id: str
    family_id: str
    role: str  # active_flat_base | specialist
    mode: str  # pullback (binding for this lab)
    title: str
    family_fn: FamilyFn

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.pop("family_fn", None)
        return d


def _cci_momentum_line(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    """Same M-line as fam_cci_gravity (lab pin — do not diverge silently)."""
    x = ind.cci(high, low, close, 20)
    x = ind.sma(x, 2)
    return ind.sma(x, 7) - ind.sma(x, 21)


def cci_active_envelope(
    sb: SetBars, *, force_thr: float = 8.0, load_lookback: int = 8
) -> Dict[str, pd.Series]:
    """CCI gravity activity envelope: force / load / reclaim (not entry soup).

    Returns boolean Series aligned to LTF index:
      bull_force, bear_force, force_on,
      load_long, load_short, reclaim_long, reclaim_short
    """
    thr = float(force_thr)
    m1 = _cci_momentum_line(sb.h1_high, sb.h1_low, sb.h1_close)
    m2 = _cci_momentum_line(sb.h2_high, sb.h2_low, sb.h2_close)
    m = _cci_momentum_line(sb.high, sb.low, sb.close)
    bull = (m1 > 0) & (m2 > 0) & (m1 >= thr)
    bear = (m1 < 0) & (m2 < 0) & (m1 <= -thr)
    z = pd.Series(0.0, index=m.index)
    was_neg = m.rolling(load_lookback, min_periods=1).min() < 0
    was_pos = m.rolling(load_lookback, min_periods=1).max() > 0
    reclaim_l = was_neg & ind.cross_up(m, z)
    reclaim_s = was_pos & ind.cross_dn(m, z)
    # load = eddy against force (not yet reclaim)
    load_l = bull & was_neg & (m < 0) & ~reclaim_l
    load_s = bear & was_pos & (m > 0) & ~reclaim_s
    force_on = (bull | bear).fillna(False)
    return {
        "bull_force": bull.fillna(False),
        "bear_force": bear.fillna(False),
        "force_on": force_on,
        "load_long": load_l.fillna(False),
        "load_short": load_s.fillna(False),
        "reclaim_long": reclaim_l.fillna(False),
        "reclaim_short": reclaim_s.fillna(False),
        "m_ltf": m,
    }


def active_flat_pressure(
    env: Dict[str, pd.Series],
    *,
    bot_in_trade: Optional[pd.Series] = None,
) -> pd.DataFrame:
    """While CCI force is active and bot is flat: why aren't we in a trade?

    Columns: pressure, teacher_act, side_hint, force_on, justified_wait
    """
    idx = env["force_on"].index
    if bot_in_trade is None:
        in_trade = pd.Series(False, index=idx)
    else:
        in_trade = bot_in_trade.reindex(idx).fillna(False).astype(bool)

    force_on = env["force_on"].astype(bool)
    load = (env["load_long"] | env["load_short"]).astype(bool)
    reclaim_l = env["reclaim_long"].astype(bool)
    reclaim_s = env["reclaim_short"].astype(bool)
    bull = env["bull_force"].astype(bool)
    bear = env["bear_force"].astype(bool)

    pressure = pd.Series(PRESSURE_NO_TRADE, index=idx, dtype=object)
    teacher_act = pd.Series(TEACHER_WAIT, index=idx, dtype=object)
    side_hint = pd.Series("", index=idx, dtype=object)
    justified = pd.Series(True, index=idx)

    # In trade → no interrogation
    pressure = pressure.where(~in_trade, PRESSURE_IN_TRADE)

    active_flat = force_on & ~in_trade
    # Loaded eddy: wait is legal
    loaded = active_flat & load
    pressure = pressure.mask(loaded, PRESSURE_LOADED)
    teacher_act = teacher_act.mask(loaded, TEACHER_WAIT)
    justified = justified.mask(loaded, True)

    # Reclaim printed while flat → must justify wait; default teacher = fire
    reclaim_flat_l = active_flat & reclaim_l & bull
    reclaim_flat_s = active_flat & reclaim_s & bear
    pressure = pressure.mask(reclaim_flat_l | reclaim_flat_s, PRESSURE_MUST_JUSTIFY)
    teacher_act = teacher_act.mask(reclaim_flat_l, TEACHER_LONG)
    teacher_act = teacher_act.mask(reclaim_flat_s, TEACHER_SHORT)
    side_hint = side_hint.mask(reclaim_flat_l, "long")
    side_hint = side_hint.mask(reclaim_flat_s, "short")
    justified = justified.mask(reclaim_flat_l | reclaim_flat_s, False)

    # Active, flat, neither load nor reclaim → soft idle pressure
    idle = active_flat & ~load & ~reclaim_l & ~reclaim_s
    # don't overwrite reclaim / loaded
    still_default = pressure == PRESSURE_NO_TRADE
    idle = idle & still_default
    pressure = pressure.mask(idle, PRESSURE_IDLE_ACTIVE)
    teacher_act = teacher_act.mask(idle, TEACHER_WAIT)
    justified = justified.mask(idle, False)  # soft: unexplained idle under force
    side_hint = side_hint.mask(idle & bull, "long")
    side_hint = side_hint.mask(idle & bear, "short")

    # Force off + flat stays no_trade / wait / justified
    return pd.DataFrame(
        {
            "pressure": pressure,
            "teacher_act": teacher_act,
            "side_hint": side_hint,
            "force_on": force_on,
            "justified_wait": justified,
            "in_trade": in_trade,
        },
        index=idx,
    )


def build_pullback_teach_roster() -> List[StrategyTeachAgent]:
    """Binding lab roster: CCI base + distinct pullback specialists."""
    return [
        StrategyTeachAgent(
            agent_id="base_cci",
            family_id="cci_gravity_scalp",
            role="active_flat_base",
            mode="pullback",
            title="CCI gravity active-flat base",
            family_fn=fam_cci_gravity,
        ),
        StrategyTeachAgent(
            agent_id="a1_mark",
            family_id="mark_rsi_bb_l2l",
            role="specialist",
            mode="pullback",
            title="Mark RSI+BB pullback timing",
            family_fn=fam_mark_rsi_bb,
        ),
        StrategyTeachAgent(
            agent_id="a2_mcflurry",
            family_id="mcflurry_eddy_scalp",
            role="specialist",
            mode="pullback",
            title="McFlurry RSI M-line eddy load",
            family_fn=fam_mcflurry,
        ),
        StrategyTeachAgent(
            agent_id="a3_dimension_jump",
            family_id="dimension_jump_sauce",
            role="specialist",
            mode="pullback",
            title="Dimension Jump BB-on-CCI load",
            family_fn=fam_dimension_jump,
        ),
        StrategyTeachAgent(
            agent_id="a4_s1_cci",
            family_id="truth_s1_cci_slingshot",
            role="specialist",
            mode="pullback",
            title="S1 Dual CCI SMA slingshot tension",
            family_fn=fam_s1_cci,
        ),
        StrategyTeachAgent(
            agent_id="a5_snap8",
            family_id="snap8_nested_pullback",
            role="specialist",
            mode="pullback",
            title="SNAP-8 nested ribbon pullback",
            family_fn=fam_snap8,
        ),
        StrategyTeachAgent(
            agent_id="a6_s4_rsi_snap",
            family_id="truth_s4_rsi_tension_snap",
            role="specialist",
            mode="pullback",
            title="S4 RSI Bollinger tension snap",
            family_fn=fam_s4_rsi_snap,
        ),
        StrategyTeachAgent(
            agent_id="a7_sma_scalp",
            family_id="ftmo_sma_scalper",
            role="specialist",
            mode="pullback",
            title="SMA ribbon touch-reclaim",
            family_fn=fam_sma_scalp,
        ),
    ]


def validate_roster(roster: Sequence[StrategyTeachAgent]) -> None:
    """One agent ↔ one family; exactly one active_flat_base; pullback-only."""
    if not roster:
        raise ValueError("empty teach roster")
    bases = [a for a in roster if a.role == "active_flat_base"]
    if len(bases) != 1:
        raise ValueError(f"need exactly one active_flat_base, got {len(bases)}")
    if bases[0].family_id != "cci_gravity_scalp":
        raise ValueError("active_flat_base must be cci_gravity_scalp")
    ids = [a.agent_id for a in roster]
    fids = [a.family_id for a in roster]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate agent_id")
    if len(fids) != len(set(fids)):
        raise ValueError("duplicate family_id — one agent per strategy")
    for a in roster:
        if a.mode != "pullback":
            raise ValueError(f"{a.agent_id} mode must be pullback in this lab")
        if a.family_id not in FAMILY_META and a.family_fn is None:
            raise ValueError(f"unknown family {a.family_id}")
    # family_fn.family_id must match declared id when present
    for a in roster:
        fn_id = getattr(a.family_fn, "family_id", None)
        if fn_id is not None and fn_id != a.family_id:
            raise ValueError(f"{a.agent_id}: fn.family_id={fn_id} != {a.family_id}")


def harvest_agent_pullback_teachers(
    agent: StrategyTeachAgent,
    sb: SetBars,
    *,
    env: Optional[Dict[str, pd.Series]] = None,
    require_cci_force: bool = True,
    max_events: int = 200,
) -> List[Dict[str, Any]]:
    """Harvest PB-mode long/short teachers for one agent under CCI envelope.

    When require_cci_force=True (default), only emit when CCI force is on —
    specialists teach pullbacks *inside* the CCI activity window.
    Base agent also emits must_justify / loaded wait rows from pressure table.
    """
    if agent.mode != "pullback":
        raise ValueError("pullback-only harvest")
    fn_id = getattr(agent.family_fn, "family_id", None)
    if fn_id is not None and fn_id != agent.family_id:
        raise ValueError(f"{agent.agent_id}: fn.family_id={fn_id} != {agent.family_id}")

    if env is None:
        env = cci_active_envelope(sb)
    pressure = active_flat_pressure(env)
    long_e, short_e = entries_for_mode(sb, agent.family_fn, "pullback")
    force_on = env["force_on"]
    if require_cci_force:
        long_e = long_e & force_on
        short_e = short_e & force_on

    out: List[Dict[str, Any]] = []

    def _add(ts, act: str, reason: str, extra: Optional[Dict[str, Any]] = None) -> None:
        if len(out) >= max_events:
            return
        row = {
            "agent_id": agent.agent_id,
            "family_id": agent.family_id,
            "role": agent.role,
            "mode": "pullback",
            "asof": str(ts),
            "teacher_act": act,
            "topology": "pullback_resume" if act in (TEACHER_LONG, TEACHER_SHORT) else "slingshot_load",
            "reason": reason,
            "pressure": str(pressure.loc[ts, "pressure"]),
            "force_on": bool(pressure.loc[ts, "force_on"]),
            "source": "strategy_teach_agent_lab",
            "set_name": sb.name,
        }
        if extra:
            row.update(extra)
        out.append(row)

    # Entry fires from this agent's geometry
    for ts in long_e[long_e].index:
        _add(ts, TEACHER_LONG, "agent_pullback_long")
        if len(out) >= max_events:
            return out
    for ts in short_e[short_e].index:
        _add(ts, TEACHER_SHORT, "agent_pullback_short")
        if len(out) >= max_events:
            return out

    # Base agent also teaches active-flat interrogation rows
    if agent.role == "active_flat_base":
        must = pressure["pressure"] == PRESSURE_MUST_JUSTIFY
        for ts in pressure.index[must]:
            act = str(pressure.loc[ts, "teacher_act"])
            if act not in (TEACHER_LONG, TEACHER_SHORT):
                continue
            _add(ts, act, "cci_reclaim_must_justify_wait")
            if len(out) >= max_events:
                return out
        loaded = pressure["pressure"] == PRESSURE_LOADED
        for ts in pressure.index[loaded]:
            _add(ts, TEACHER_WAIT, "cci_loaded_wait_ok", {"topology": "slingshot_load"})
            if len(out) >= max_events:
                return out

    return out


def harvest_all_pullback_teachers(
    sb: SetBars,
    *,
    roster: Optional[Sequence[StrategyTeachAgent]] = None,
    require_cci_force: bool = True,
    max_events_per_agent: int = 100,
    force_thr: float = 8.0,
) -> Dict[str, Any]:
    """Run full lab roster; return per-agent teachers + summary."""
    roster = list(roster) if roster is not None else build_pullback_teach_roster()
    validate_roster(roster)
    env = cci_active_envelope(sb, force_thr=force_thr)
    pressure = active_flat_pressure(env)
    by_agent: Dict[str, List[Dict[str, Any]]] = {}
    for agent in roster:
        by_agent[agent.agent_id] = harvest_agent_pullback_teachers(
            agent,
            sb,
            env=env,
            require_cci_force=require_cci_force,
            max_events=max_events_per_agent,
        )
    n_force = int(env["force_on"].sum())
    n_must = int((pressure["pressure"] == PRESSURE_MUST_JUSTIFY).sum())
    n_loaded = int((pressure["pressure"] == PRESSURE_LOADED).sum())
    n_idle = int((pressure["pressure"] == PRESSURE_IDLE_ACTIVE).sum())
    return {
        "set_name": sb.name,
        "n_bars": int(len(sb.close)),
        "n_force_bars": n_force,
        "n_must_justify": n_must,
        "n_loaded_wait": n_loaded,
        "n_active_idle": n_idle,
        "roster": [a.to_dict() for a in roster],
        "teachers_by_agent": by_agent,
        "n_teachers_total": int(sum(len(v) for v in by_agent.values())),
        "lab": True,
        "promoted": False,
        "force_thr": float(force_thr),
    }
