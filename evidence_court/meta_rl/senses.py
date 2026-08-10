"""Emergent sense probes: sight, feel, taste, hearing as relational predicates."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .types import TopologyClass


@dataclass
class MarketSenseInput:
    """Structured multi-TF relational inputs (not absolute indicator folklore)."""
    # Per official set: HTF force side (-1/0/1) for each of 2 HTFs, LTF velocity
    htf_force: Sequence[float]  # e.g. 8 values = 4 sets × 2 HTFs
    ltf_velocity: Sequence[float]  # 4 values
    inertia: Sequence[float]  # 4 values (slow period)
    inertia_baseline: Sequence[float]
    velocity_baseline: Sequence[float]
    # Tunnel: body outside both rails?
    full_body_outside_rails: bool = False
    ltf_inside_tight: bool = False
    # Efficiency / regime
    efficiency: float = 0.5  # 0 nothing, 0.5 tradable, 1 great
    regime: str = "undefined"  # bull | bear | chop | vol_shock | undefined
    g_fixed: bool = True
    g_flip: bool = False
    # Goal/risk taste
    target_percent: float = 15.0
    max_daily_risk_percent: float = 2.0
    progress_to_target: float = 0.0
    realized_risk_percent: float = 0.0
    composition_has_force: bool = True
    composition_has_velocity: bool = True
    cross_family_agree: bool = False
    set_conflict: bool = False


@dataclass
class SenseReport:
    sight: Dict[str, object]
    feel: Dict[str, object]
    taste: Dict[str, object]
    hearing: Dict[str, object]


def _sign(x: float) -> int:
    if x > 1e-9:
        return 1
    if x < -1e-9:
        return -1
    return 0


def probe_sight(inp: MarketSenseInput) -> Dict[str, object]:
    htf = list(inp.htf_force)
    ltf = list(inp.ltf_velocity)
    inertia = list(inp.inertia)

    # HTF force side per set (pairs)
    set_forces: List[float] = []
    for i in range(0, min(len(htf), 8), 2):
        pair = htf[i : i + 2]
        set_forces.append(float(np.mean(pair)) if pair else 0.0)

    multi_set_consensus = "incomplete"
    if set_forces:
        signs = [_sign(f) for f in set_forces if abs(f) >= 0.2]
        if len(signs) >= 2 and all(s == signs[0] for s in signs) and signs[0] != 0:
            multi_set_consensus = "agree_long" if signs[0] > 0 else "agree_short"
        elif len(signs) >= 2 and any(s != signs[0] for s in signs):
            multi_set_consensus = "conflict"
        elif not signs:
            multi_set_consensus = "incomplete"

    # LTF velocity phase relative to force
    phases = []
    for i, f in enumerate(set_forces):
        v = ltf[i] if i < len(ltf) else 0.0
        if abs(f) < 0.15 or abs(v) < 0.15:
            phases.append("flat")
        elif _sign(f) == _sign(v):
            phases.append("with")
        else:
            phases.append("against")

    # Inertia intact: slow still with tide during micro dip
    inertia_intact = []
    for i, f in enumerate(set_forces):
        inn = inertia[i] if i < len(inertia) else 0.0
        v = ltf[i] if i < len(ltf) else 0.0
        intact = abs(f) >= 0.2 and _sign(f) == _sign(inn) and _sign(v) != _sign(f)
        inertia_intact.append(bool(intact))

    # Topology class
    mean_f = float(np.mean(set_forces)) if set_forces else 0.0
    mean_v = float(np.mean(ltf)) if ltf else 0.0
    mean_i = float(np.mean(inertia)) if inertia else 0.0
    if abs(mean_f) < 0.15 and abs(mean_v) < 0.15:
        topo = TopologyClass.CHOP
    elif _sign(mean_f) == _sign(mean_i) and _sign(mean_f) != _sign(mean_v) and abs(mean_f) >= 0.2:
        topo = TopologyClass.SLINGSHOT_LOAD
    elif _sign(mean_f) == _sign(mean_v) and abs(mean_f) >= 0.25:
        topo = TopologyClass.LAUNCH if abs(mean_i) >= 0.2 else TopologyClass.RELEASE
    elif _sign(mean_f) != _sign(mean_i) and abs(mean_f) >= 0.2:
        topo = TopologyClass.COLLAPSE
    else:
        topo = TopologyClass.CHOP

    tunnel = "full_body_outside" if inp.full_body_outside_rails else "inside"

    return {
        "htf_force_per_set": set_forces,
        "ltf_velocity_phase": phases,
        "inertia_intact": inertia_intact,
        "tunnel_membership": tunnel,
        "multi_set_consensus": multi_set_consensus,
        "topology_class": topo.value,
        "continuation_vs_reversal": (
            "continuation" if topo in (TopologyClass.LAUNCH, TopologyClass.RELEASE) else
            "reversal_risk" if topo == TopologyClass.COLLAPSE else "neutral"
        ),
    }


def probe_feel(inp: MarketSenseInput) -> Dict[str, object]:
    inertia = list(inp.inertia)
    ib = list(inp.inertia_baseline)
    vel = list(inp.ltf_velocity)
    vb = list(inp.velocity_baseline)

    i_delta_signs = [_sign(inertia[k] - (ib[k] if k < len(ib) else 0.0)) for k in range(len(inertia))]
    v_delta_signs = [_sign(vel[k] - (vb[k] if k < len(vb) else 0.0)) for k in range(len(vel))]

    force = float(np.mean(inp.htf_force)) if len(inp.htf_force) else 0.0
    mean_i = float(np.mean(inertia)) if inertia else 0.0
    mean_v = float(np.mean(vel)) if vel else 0.0

    inertia_with = _sign(mean_i) == _sign(force) and abs(force) >= 0.15
    velocity_against = _sign(mean_v) != _sign(force) and abs(mean_v) >= 0.15
    velocity_with = _sign(mean_v) == _sign(force) and abs(mean_v) >= 0.15
    inertia_against = _sign(mean_i) != _sign(force) and abs(mean_i) >= 0.15

    max_tension = bool(inertia_with and velocity_against and inp.g_fixed)
    launch = bool(inertia_with and velocity_with and abs(force) >= 0.25)
    collapse = bool(inertia_against or inp.g_flip)
    breath_inside_momentum = bool(inp.full_body_outside_rails and inp.ltf_inside_tight)

    if inp.efficiency < 0.15:
        eff_regime = "nothing"
    elif inp.efficiency < 0.55:
        eff_regime = "tradable"
    else:
        eff_regime = "great_movement"

    return {
        "inertia_delta_signs": i_delta_signs,
        "velocity_delta_signs": v_delta_signs,
        "max_tension_load_building": max_tension,
        "launch": launch,
        "collapse": collapse,
        "breath_inside_momentum": breath_inside_momentum,
        "efficiency_regime": eff_regime,
        "clocks": {
            "inertia_with": inertia_with,
            "velocity_with": velocity_with,
            "velocity_against": velocity_against,
        },
    }


def probe_taste(inp: MarketSenseInput) -> Dict[str, object]:
    composition_valid = bool(inp.composition_has_force and inp.composition_has_velocity)
    conviction = 0.5
    if composition_valid:
        conviction += 0.2
    if inp.cross_family_agree:
        conviction += 0.2
    if inp.set_conflict:
        conviction -= 0.25
    if inp.efficiency < 0.15:
        conviction -= 0.3
    conviction = float(np.clip(conviction, 0.0, 1.0))

    goal_distance = max(1.0 - float(inp.progress_to_target), 0.0)
    risk_remaining = max(
        float(inp.max_daily_risk_percent) - float(inp.realized_risk_percent), 0.0
    ) / max(float(inp.max_daily_risk_percent), 1e-6)

    # Marginal vs bread-and-butter
    if composition_valid and conviction >= 0.65 and not inp.set_conflict:
        edge_quality = "bread_and_butter"
    elif composition_valid and conviction >= 0.4:
        edge_quality = "marginal"
    else:
        edge_quality = "noise"

    # High target + marginal → patience (taste skill)
    patience_preferred = bool(
        inp.target_percent >= 40.0 and edge_quality == "marginal" and goal_distance > 0.5
    )
    allow_fire = risk_remaining > 0 and composition_valid and edge_quality != "noise"

    return {
        "composition_valid": composition_valid,
        "edge_quality": edge_quality,
        "conviction": conviction,
        "goal_distance": goal_distance,
        "risk_remaining_frac": risk_remaining,
        "patience_preferred": patience_preferred,
        "allow_fire": allow_fire and not patience_preferred,
        "velocity_trust": inp.efficiency >= 0.15,
    }


def probe_hearing(inp: MarketSenseInput) -> Dict[str, object]:
    regime = inp.regime
    force = float(np.mean(inp.htf_force)) if len(inp.htf_force) else 0.0
    mean_i = float(np.mean(inp.inertia)) if len(inp.inertia) else 0.0
    mean_v = float(np.mean(inp.ltf_velocity)) if len(inp.ltf_velocity) else 0.0

    dual_clock = "co_alignment" if _sign(mean_i) == _sign(mean_v) and abs(mean_i) >= 0.15 else "divergence"
    if abs(mean_i) < 0.1 and abs(mean_v) < 0.1:
        dual_clock = "quiet"

    # Multi-set force consensus from sight
    sight = probe_sight(inp)
    consensus = sight["multi_set_consensus"]

    # Wait subtype with reason
    feel = probe_feel(inp)
    if feel["collapse"] or regime in ("vol_shock",):
        wait_subtype = "kill"
        wait_reason = "regime_or_collapse"
    elif feel["max_tension_load_building"]:
        wait_subtype = "loaded_not_yet"
        wait_reason = "tension_building_await_resume"
    elif regime in ("chop", "undefined") or consensus in ("conflict", "incomplete"):
        wait_subtype = "no_trade"
        wait_reason = f"regime={regime} consensus={consensus}"
    else:
        wait_subtype = ""
        wait_reason = "actionable"

    regime_shift_detected = regime in ("chop", "vol_shock", "undefined") and abs(force) < 0.2

    return {
        "regime": regime,
        "regime_shift_detected": regime_shift_detected,
        "dual_clock": dual_clock,
        "forward_shift_tunnel": (
            "mass_ahead" if inp.full_body_outside_rails else "no_clear"
        ),
        "multi_set_force_consensus": consensus,
        "wait_subtype": wait_subtype,
        "wait_reason": wait_reason,
        "day_story_coherent": not (feel["collapse"] and feel["launch"]),
    }


def probe_all_senses(inp: MarketSenseInput) -> SenseReport:
    return SenseReport(
        sight=probe_sight(inp),
        feel=probe_feel(inp),
        taste=probe_taste(inp),
        hearing=probe_hearing(inp),
    )


# Fixed sense pack for MetaBrain state (L2L Proposal 1).
# Packed into Mark agent_votes slots [0:SENSE_PACK_DIM] so META_RL_DIM stays 176
# (frozen-weight contract / champion load path unchanged).
SENSE_PACK_DIM = 16
# Mark-full layout: channel1 32 + doctrine 16 + majority 12 + agent 92 + self 16
SENSE_AGENT_SLOT_START = 0  # offset within agent_votes (state index 60+start)


def _b01(x: object) -> float:
    return 1.0 if bool(x) else 0.0


def _topo_code(topo: object) -> float:
    m = {
        "chop": 0.0,
        "slingshot_load": 0.25,
        "release": 0.5,
        "launch": 0.75,
        "collapse": 1.0,
    }
    return float(m.get(str(topo or "chop"), 0.0))


def _wait_code(subtype: object) -> float:
    m = {
        "": 0.0,
        "loaded_not_yet": 0.33,
        "no_trade": 0.66,
        "kill": 1.0,
    }
    return float(m.get(str(subtype or ""), 0.0))


def encode_sense_report(report: SenseReport) -> "np.ndarray":
    """Encode four sense reports into a fixed SENSE_PACK_DIM float vector.

    Layout (16):
      0  mean HTF force sign-magnitude (sight)
      1  multi-set consensus: -1 short / 0 incomplete-conflict / +1 long
      2  topology code
      3  fraction LTF phases against force
      4  feel load (max_tension)
      5  feel launch
      6  feel collapse
      7  efficiency regime 0/0.5/1
      8  taste conviction
      9  taste allow_fire
      10 taste patience_preferred
      11 taste risk_remaining_frac
      12 hearing wait_subtype code
      13 hearing day_story_coherent
      14 hearing regime_shift_detected
      15 dual_clock: quiet=0 divergence=0.5 co_alignment=1
    """
    import numpy as np

    s, f, t, h = report.sight, report.feel, report.taste, report.hearing
    forces = list(s.get("htf_force_per_set") or [])
    mean_f = float(np.mean(forces)) if forces else 0.0
    cons = str(s.get("multi_set_consensus") or "incomplete")
    cons_v = 1.0 if cons == "agree_long" else (-1.0 if cons == "agree_short" else 0.0)
    phases = list(s.get("ltf_velocity_phase") or [])
    against_frac = (
        float(sum(1 for p in phases if p == "against") / max(len(phases), 1))
        if phases
        else 0.0
    )
    eff = str(f.get("efficiency_regime") or "tradable")
    eff_v = 0.0 if eff == "nothing" else (1.0 if eff == "great_movement" else 0.5)
    dual = str(h.get("dual_clock") or "quiet")
    dual_v = (
        1.0
        if dual == "co_alignment"
        else (0.5 if dual == "divergence" else 0.0)
    )
    out = np.zeros(SENSE_PACK_DIM, dtype=np.float32)
    out[0] = float(np.clip(mean_f, -1.0, 1.0))
    out[1] = cons_v
    out[2] = _topo_code(s.get("topology_class"))
    out[3] = against_frac
    out[4] = _b01(f.get("max_tension_load_building"))
    out[5] = _b01(f.get("launch"))
    out[6] = _b01(f.get("collapse"))
    out[7] = eff_v
    out[8] = float(np.clip(float(t.get("conviction") or 0.0), 0.0, 1.0))
    out[9] = _b01(t.get("allow_fire"))
    out[10] = _b01(t.get("patience_preferred"))
    out[11] = float(np.clip(float(t.get("risk_remaining_frac") or 0.0), 0.0, 1.0))
    out[12] = _wait_code(h.get("wait_subtype"))
    out[13] = _b01(h.get("day_story_coherent"))
    out[14] = _b01(h.get("regime_shift_detected"))
    out[15] = dual_v
    return out


def encode_senses_from_input(inp: MarketSenseInput) -> "np.ndarray":
    return encode_sense_report(probe_all_senses(inp))
