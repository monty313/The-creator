"""CASE-0015 — Market ontology: shared vocabulary for the road (not the driver).

These definitions are the **road signs** the trained meta-policy and Court share.
They do not replace Mark eyes or A14 training — they name what already exists
so curriculum, senses, edge, and scoreboard speak one language.

**Every market structure term is bound to:**
  - official Mark **timeframe sets** (LTF first, HTF last two — MARK_SETS_LAW)
  - a **group of indicators** (recipe names + params used in Court edge/senses)

Winning / passing are **day scoreboard** terms (goal + risk inputs, not TFs).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .sets import MARK_SETS_LAW, OFFICIAL_SETS, assert_mark_sets_law


# ─── Day scoreboard (what "good" means for the bot) ───────────────────────────


class DayOutcome(str, Enum):
    """End-of-day result relative to Monty's typed target and risk."""

    WIN = "win"  # reached target
    PASS = "pass"  # no breach (may or may not win)
    FAIL_BREACH = "fail_breach"  # hit risk floor
    MISS = "miss"  # no breach, did not reach target


def day_is_win(*, pnl_percent: float, target_percent: float) -> bool:
    """WINNING = reaching the daily profit target (equity %)."""
    return float(pnl_percent) >= float(target_percent) - 1e-9


def day_is_pass(*, breach: bool) -> bool:
    """PASSING = no daily risk breach (risk floor not hit)."""
    return not bool(breach)


def classify_day_outcome(
    *,
    pnl_percent: float,
    target_percent: float,
    breach: bool,
) -> DayOutcome:
    """Joint day label for curriculum / scoreboard."""
    if breach:
        return DayOutcome.FAIL_BREACH
    if day_is_win(pnl_percent=pnl_percent, target_percent=target_percent):
        return DayOutcome.WIN
    return DayOutcome.MISS


# ─── Indicator groups + timeframe bindings (CASE-0015 Court requirement) ─────


@dataclass(frozen=True)
class IndicatorSpec:
    """One named indicator recipe (params must match Court edge/senses usage)."""

    name: str
    params: Tuple[Tuple[str, object], ...] = ()
    role: str = ""  # force | velocity | equilibrium | regime_gate | scoreboard | self


@dataclass(frozen=True)
class IndicatorGroup:
    """A named bag of indicators used together for one ontology term."""

    group_id: str
    indicators: Tuple[IndicatorSpec, ...]
    description: str = ""


@dataclass(frozen=True)
class TimeframeBinding:
    """Which TFs on which official Mark set a term uses."""

    set_id: int
    set_name: str
    ltf: str
    htf: Tuple[str, str]
    uses_ltf: bool = True
    uses_htf: bool = True


@dataclass(frozen=True)
class TermDefinition:
    """Full Court definition: meaning + indicator group + TF binding(s)."""

    term: str
    meaning: str
    indicator_group: IndicatorGroup
    timeframe_bindings: Tuple[TimeframeBinding, ...]
    scoreboard_only: bool = False  # win/pass: no market TFs


def _official_tf_bindings(*, uses_ltf: bool = True, uses_htf: bool = True) -> Tuple[TimeframeBinding, ...]:
    """Bind to all four MARK_SETS_LAW stacks."""
    assert_mark_sets_law()
    out: List[TimeframeBinding] = []
    for s in OFFICIAL_SETS:
        out.append(
            TimeframeBinding(
                set_id=s.set_id,
                set_name=s.name,
                ltf=s.entry_tf,
                htf=s.confirmation_tfs,
                uses_ltf=uses_ltf,
                uses_htf=uses_htf,
            )
        )
    return tuple(out)


# Indicator recipes pinned to Court implementation (edge.py / indicators.py / goal_risk)
GROUP_HTF_FORCE = IndicatorGroup(
    group_id="htf_force",
    description="HTF confirmation force — trend_dir on each confirmation TF, agree = momentum",
    indicators=(
        IndicatorSpec("trend_dir", (("lookback", 5),), role="force"),
        IndicatorSpec("trend_dir_medium", (("lookback", 10),), role="force"),
        IndicatorSpec("multi_day_momentum", (("n_days", 3),), role="force"),
    ),
)

GROUP_LTF_TIMING = IndicatorGroup(
    group_id="ltf_timing",
    description="LTF entry timing — RSI(5) + BB(10, dev=0.5, shift=+2) on set LTF closes",
    indicators=(
        IndicatorSpec("rsi", (("period", 5),), role="velocity"),
        IndicatorSpec(
            "bollinger",
            (("period", 10), ("dev", 0.5), ("shift", 2)),
            role="equilibrium",
        ),
        IndicatorSpec("price_vs_bb_rails", (), role="velocity"),
    ),
)

GROUP_REGIME = IndicatorGroup(
    group_id="regime_multi_set",
    description="Regime from all 4 sets' HTF force signs + efficiency proxy",
    indicators=(
        IndicatorSpec("trend_dir", (("lookback", 5),), role="force"),
        IndicatorSpec("multi_set_consensus", (), role="regime_gate"),
        IndicatorSpec("efficiency", (), role="regime_gate"),
    ),
)

GROUP_TRIGGER = IndicatorGroup(
    group_id="trigger_permission",
    description="Fire vs wait: HTF agree + LTF topology + conflict kill",
    indicators=(
        IndicatorSpec("htf_agree", (), role="force"),
        IndicatorSpec("structure_event", (), role="velocity"),
        IndicatorSpec("multi_set_consensus", (), role="regime_gate"),
    ),
)

GROUP_SCOREBOARD = IndicatorGroup(
    group_id="day_scoreboard",
    description="Win/pass from equity day PnL vs typed target/risk — not chart TFs",
    indicators=(
        IndicatorSpec("realized_pnl_percent", (), role="scoreboard"),
        IndicatorSpec("target_percent", (), role="scoreboard"),
        IndicatorSpec("max_daily_risk_percent", (), role="scoreboard"),
        IndicatorSpec("breach_flag", (), role="scoreboard"),
    ),
)

GROUP_SENSES = IndicatorGroup(
    group_id="senses_relational",
    description="Sight/feel/taste/hearing probes on multi-TF force/velocity/inertia",
    indicators=(
        IndicatorSpec("htf_force_channels", (), role="force"),
        IndicatorSpec("ltf_velocity_channels", (), role="velocity"),
        IndicatorSpec("inertia_channels", (), role="inertia"),
        IndicatorSpec("goal_risk_context", (), role="scoreboard"),
    ),
)

GROUP_INTUITION = IndicatorGroup(
    group_id="intuition_learned",
    description="Trained meta-policy attention over full Meta-RL state (168+goal) — A14 weights",
    indicators=(
        IndicatorSpec("meta_rl_state_176", (), role="self"),
        IndicatorSpec("channel1_set_dirs", (), role="force"),
        IndicatorSpec("goal_risk_context_8", (), role="scoreboard"),
        IndicatorSpec("sense_probes", (), role="self"),
    ),
)


def term_definitions() -> Dict[str, TermDefinition]:
    """Canonical term → indicator group + timeframe bindings (all official sets)."""
    all_sets = _official_tf_bindings(uses_ltf=True, uses_htf=True)
    htf_only = _official_tf_bindings(uses_ltf=False, uses_htf=True)
    ltf_only = _official_tf_bindings(uses_ltf=True, uses_htf=False)
    # Win/pass: no chart TFs — empty binding with set 0 sentinel
    scoreboard_tf = (
        TimeframeBinding(
            set_id=0,
            set_name="scoreboard",
            ltf="day",
            htf=("day", "day"),
            uses_ltf=False,
            uses_htf=False,
        ),
    )
    return {
        "momentum": TermDefinition(
            term="momentum",
            meaning="HTF directed force: trend_dir on both confirmation TFs of each Mark set; agree + same sign = bull/bear force.",
            indicator_group=GROUP_HTF_FORCE,
            timeframe_bindings=htf_only,
        ),
        "regime": TermDefinition(
            term="regime",
            meaning="Across all 4 Mark sets: multi-set HTF force consensus + efficiency (tradable/chop/shock).",
            indicator_group=GROUP_REGIME,
            timeframe_bindings=htf_only,
        ),
        "pullback": TermDefinition(
            term="pullback",
            meaning="On set LTF: RSI5+BB10(dev0.5,shift+2) shows dip against HTF force then resume with force (pullback_resume).",
            indicator_group=GROUP_LTF_TIMING,
            timeframe_bindings=all_sets,
        ),
        "continuation": TermDefinition(
            term="continuation",
            meaning="On set LTF: RSI5+BB aligned with HTF force without deep opposite-rail dip.",
            indicator_group=GROUP_LTF_TIMING,
            timeframe_bindings=all_sets,
        ),
        "slingshot_load": TermDefinition(
            term="slingshot_load",
            meaning="LTF velocity against HTF force while inertia still with force — WAIT (not reverse thrash).",
            indicator_group=GROUP_LTF_TIMING,
            timeframe_bindings=all_sets,
        ),
        "trigger": TermDefinition(
            term="trigger",
            meaning="Fire only if HTF agree on set + LTF structure is pullback_resume or continuation + multi-set not conflict.",
            indicator_group=GROUP_TRIGGER,
            timeframe_bindings=all_sets,
        ),
        "winning": TermDefinition(
            term="winning",
            meaning="Day equity PnL % >= typed target_percent.",
            indicator_group=GROUP_SCOREBOARD,
            timeframe_bindings=scoreboard_tf,
            scoreboard_only=True,
        ),
        "passing": TermDefinition(
            term="passing",
            meaning="No daily risk breach under typed max_daily_risk_percent.",
            indicator_group=GROUP_SCOREBOARD,
            timeframe_bindings=scoreboard_tf,
            scoreboard_only=True,
        ),
        "senses": TermDefinition(
            term="senses",
            meaning="Sight/feel/taste/hearing relational probes on multi-set HTF force, LTF velocity, inertia, goal/risk.",
            indicator_group=GROUP_SENSES,
            timeframe_bindings=all_sets,
        ),
        "intuition": TermDefinition(
            term="intuition",
            meaning="Learned attention of trained meta-policy (A14) over Meta-RL state + senses — not a fixed indicator recipe.",
            indicator_group=GROUP_INTUITION,
            timeframe_bindings=all_sets,
        ),
    }


def official_set_stacks() -> Tuple[Tuple[str, str, str], ...]:
    """LTF, HTF1, HTF2 for each official set — must match MARK_SETS_LAW."""
    return tuple(s.tfs for s in OFFICIAL_SETS)


def assert_term_bound_to_sets_and_indicators(term: str) -> TermDefinition:
    """Fail if a market term lacks TF binding and indicator group (Court pin)."""
    defs = term_definitions()
    if term not in defs:
        raise AssertionError(f"unknown ontology term: {term}")
    d = defs[term]
    if not d.indicator_group.indicators:
        raise AssertionError(f"{term}: empty indicator group")
    if not d.timeframe_bindings:
        raise AssertionError(f"{term}: empty timeframe bindings")
    if not d.scoreboard_only:
        # Must reference real Mark stacks
        stacks = {s.tfs for s in OFFICIAL_SETS}
        for b in d.timeframe_bindings:
            if b.set_id == 0:
                continue
            trip = (b.ltf, b.htf[0], b.htf[1])
            if trip not in stacks:
                raise AssertionError(f"{term}: binding {trip} not in MARK_SETS_LAW")
    return d


# ─── Market structure (Mark multi-TF language) ────────────────────────────────


class MomentumKind(str, Enum):
    """Momentum = directed force from HTF confirmation TFs (trend_dir group)."""

    BULL = "bull"  # HTF force net long
    BEAR = "bear"  # HTF force net short
    FLAT = "flat"  # no clear HTF force


class RegimeKind(str, Enum):
    """Regime = multi-set consensus + tradability (efficiency), not a single TF."""

    BULL = "bull"
    BEAR = "bear"
    CHOP = "chop"
    CONFLICT = "conflict"
    INCOMPLETE = "incomplete"
    VOL_SHOCK = "vol_shock"
    UNDEFINED = "undefined"


class TriggerKind(str, Enum):
    """Trigger = permission to consider an act (not the size decision)."""

    FIRE_LONG = "fire_long"
    FIRE_SHORT = "fire_short"
    WAIT = "wait"
    KILL = "kill"  # risk/conflict stand-down


class StructureEvent(str, Enum):
    """Named structure events on official Mark sets (edge topology)."""

    PULLBACK_RESUME = "pullback_resume"  # dipped against force, resumed with force
    CONTINUATION = "continuation"  # aligned with force, no deep dip required
    SLINGSHOT_LOAD = "slingshot_load"  # loading — wait (inertia with, velocity against)
    COLLAPSE = "collapse"  # structure fails — wait/kill
    CHOP = "chop"  # no clean timing edge


# Force thresholds (road signs — shared with edge/senses conventions)
FORCE_FLAT_ABS = 0.15
FORCE_CLEAR_ABS = 0.20
EFFICIENCY_TRADABLE = 0.45
EFFICIENCY_GREAT = 0.75


def classify_momentum(force: float) -> MomentumKind:
    """Momentum from signed HTF force proxy in [-1, 1]."""
    f = float(force)
    if f >= FORCE_FLAT_ABS:
        return MomentumKind.BULL
    if f <= -FORCE_FLAT_ABS:
        return MomentumKind.BEAR
    return MomentumKind.FLAT


def classify_regime(
    *,
    multi_set_consensus: str,
    efficiency: float = 0.5,
    force: float = 0.0,
) -> RegimeKind:
    """Regime from multi-set consensus + efficiency shock flag."""
    c = str(multi_set_consensus or "undefined").lower()
    eff = float(efficiency)
    if eff < 0.15 and abs(float(force)) >= FORCE_CLEAR_ABS:
        return RegimeKind.VOL_SHOCK
    if c == "agree_long":
        return RegimeKind.BULL
    if c == "agree_short":
        return RegimeKind.BEAR
    if c == "conflict":
        return RegimeKind.CONFLICT
    if c == "incomplete":
        return RegimeKind.INCOMPLETE
    if c == "chop":
        return RegimeKind.CHOP
    # Fall back to force-only when consensus undefined
    m = classify_momentum(force)
    if m == MomentumKind.BULL:
        return RegimeKind.BULL
    if m == MomentumKind.BEAR:
        return RegimeKind.BEAR
    return RegimeKind.UNDEFINED


def classify_structure_event(topology: str) -> StructureEvent:
    """Map edge topology string → StructureEvent."""
    t = str(topology or "chop").lower()
    for e in StructureEvent:
        if e.value == t:
            return e
    # policy vocabulary aliases
    if t == "launch":
        return StructureEvent.PULLBACK_RESUME
    if t == "release":
        return StructureEvent.CONTINUATION
    return StructureEvent.CHOP


def is_pullback(topology: str) -> bool:
    """Pullback = pullback_resume (or policy launch alias)."""
    return classify_structure_event(topology) == StructureEvent.PULLBACK_RESUME


def is_continuation(topology: str) -> bool:
    return classify_structure_event(topology) == StructureEvent.CONTINUATION


def is_wait_structure(topology: str) -> bool:
    """Structures that must not open new risk as timing fire."""
    e = classify_structure_event(topology)
    return e in (
        StructureEvent.SLINGSHOT_LOAD,
        StructureEvent.COLLAPSE,
        StructureEvent.CHOP,
    )


def classify_trigger(
    *,
    act: str,
    topology: str,
    htf_agree: bool,
    multi_set_consensus: str = "incomplete",
) -> TriggerKind:
    """Trigger = when an act is admissible as a fire vs wait/kill.

    Fire requires: act long|short, htf_agree, structure not wait-class, not conflict.
    """
    a = str(act or "wait").lower()
    if multi_set_consensus == "conflict":
        return TriggerKind.KILL
    if not htf_agree or is_wait_structure(topology) or a not in ("long", "short"):
        return TriggerKind.WAIT
    if a == "long":
        return TriggerKind.FIRE_LONG
    return TriggerKind.FIRE_SHORT


# ─── Perception (senses + intuition) ──────────────────────────────────────────


class SenseModality(str, Enum):
    """Four Court senses (CASE-0001 / protocol) — relational, not absolute levels."""

    SIGHT = "sight"  # structure: HTF force, LTF phase, topology, multi-set
    FEEL = "feel"  # tension: dual clocks, load vs launch
    TASTE = "taste"  # edge quality + goal/risk remaining
    HEARING = "hearing"  # day story / wait subtype (wait, fire, kill)


@dataclass(frozen=True)
class SenseVocabulary:
    """Names the policy and Court use for each modality (road signs)."""

    sight_keys: Tuple[str, ...] = (
        "htf_force_sides",
        "ltf_velocity_phase",
        "topology_class",
        "multi_set_consensus",
        "inertia_intact",
    )
    feel_keys: Tuple[str, ...] = (
        "max_tension_load_building",
        "launch_alignment",
        "dual_clock_signs",
    )
    taste_keys: Tuple[str, ...] = (
        "edge_quality",
        "composition_valid",
        "goal_distance",
        "risk_remaining",
    )
    hearing_keys: Tuple[str, ...] = (
        "wait_subtype",  # loaded_not_yet | no_trade | kill | ""
        "day_story",
    )


def intuition_definition() -> str:
    """Intuition is NOT a separate hardcoded indicator.

    It is the **learned attention** of the meta-policy over senses + state
    (what to trust, when to wait, when to fire) under goal/risk context.
    Court proves senses with probes; A14 trains intuition into weights.
    """
    return (
        "intuition = trained meta-policy attention over sight/feel/taste/hearing "
        "+ Mark structure + goal/risk context; not a hand-authored rule tree"
    )


# ─── Glossary dump (docs / curriculum) ───────────────────────────────────────


def ontology_glossary() -> Dict[str, str]:
    """Human-readable definitions including indicator groups + TF stacks."""
    base = {
        "winning": "Day PnL % >= typed target_percent (day_is_win). Scoreboard only.",
        "passing": "No daily risk breach (day_is_pass). Scoreboard only.",
        "intuition": intuition_definition(),
        "road": "Names + TF/indicator bindings are signs for trained weights (A14); not the driver.",
        "mark_sets": "1m|15m,30m · 5m|30m,1h · 15m|1h,4h · 30m|4h,1d (LTF first).",
    }
    for term, d in term_definitions().items():
        inds = ", ".join(
            f"{i.name}{dict(i.params) if i.params else ''}" for i in d.indicator_group.indicators
        )
        tfs = "; ".join(
            f"set{b.set_id}:{b.ltf}+{b.htf[0]}/{b.htf[1]}"
            for b in d.timeframe_bindings
            if b.set_id > 0
        ) or "scoreboard/day"
        base[term] = f"{d.meaning} | indicators=[{inds}] | TFs=[{tfs}]"
    return base


def ontology_self_check() -> Dict[str, Any]:
    """Tiny internal consistency check for unit tests."""
    g = ontology_glossary()
    assert "winning" in g and "passing" in g
    assert day_is_win(pnl_percent=5.0, target_percent=5.0)
    assert not day_is_win(pnl_percent=4.99, target_percent=5.0)
    assert day_is_pass(breach=False)
    assert not day_is_pass(breach=True)
    assert classify_day_outcome(pnl_percent=10.0, target_percent=5.0, breach=False) == DayOutcome.WIN
    assert classify_day_outcome(pnl_percent=1.0, target_percent=5.0, breach=False) == DayOutcome.MISS
    assert classify_day_outcome(pnl_percent=-3.0, target_percent=5.0, breach=True) == DayOutcome.FAIL_BREACH
    assert classify_momentum(0.3) == MomentumKind.BULL
    assert classify_momentum(-0.3) == MomentumKind.BEAR
    assert classify_momentum(0.0) == MomentumKind.FLAT
    assert is_pullback("pullback_resume") and is_pullback("launch")
    assert is_continuation("continuation") and is_continuation("release")
    assert is_wait_structure("slingshot_load")
    assert classify_trigger(act="long", topology="pullback_resume", htf_agree=True) == TriggerKind.FIRE_LONG
    assert classify_trigger(act="long", topology="slingshot_load", htf_agree=True) == TriggerKind.WAIT
    assert classify_trigger(act="long", topology="continuation", htf_agree=True, multi_set_consensus="conflict") == TriggerKind.KILL
    assert classify_regime(multi_set_consensus="agree_long") == RegimeKind.BULL
    assert "intuition" in g
    # Every structure term must bind to Mark sets + indicators
    for term in (
        "momentum",
        "regime",
        "pullback",
        "continuation",
        "trigger",
        "senses",
        "slingshot_load",
    ):
        assert_term_bound_to_sets_and_indicators(term)
    assert official_set_stacks() == (
        ("1m", "15m", "30m"),
        ("5m", "30m", "1h"),
        ("15m", "1h", "4h"),
        ("30m", "4h", "1d"),
    )
    return {"ok": True, "n_terms": len(g), "n_bound": len(term_definitions())}
