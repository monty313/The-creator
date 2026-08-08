"""CASE-0016 — Official regime catalog for the road (Court-adjudicated).

Regimes are **filters / context labels** for the trained meta-policy — not the driver.
Each regime is bound to **Mark timeframe sets** + an **indicator group**.

Competing catalogs (Court):
  - Creator/internet: trend / range / vol expansion / compression / transition
  - Mark/physics: multi-set HTF consensus + efficiency/entropy chop mask + incomplete eyes
  - **PROMOTED hybrid:** production `RegimeId` below (measurable with existing Court sensors)

Winning day still = reach target; passing = no breach (A16 scoreboard).
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .market_ontology import (
    FORCE_CLEAR_ABS,
    FORCE_FLAT_ABS,
    IndicatorGroup,
    IndicatorSpec,
    TimeframeBinding,
    classify_momentum,
)
from .sets import OFFICIAL_SETS, assert_mark_sets_law


class RegimeId(str, Enum):
    """Production regime set (CASE-0016 hybrid catalog)."""

    TREND_BULL = "trend_bull"  # multi-set HTF agree long
    TREND_BEAR = "trend_bear"  # multi-set HTF agree short
    RANGE_CHOP = "range_chop"  # no directed multi-set force / chop
    CONFLICT = "conflict"  # sets disagree on side
    INCOMPLETE = "incomplete"  # not enough HTF eyes / weak agreement
    VOL_EXPANSION = "vol_expansion"  # high efficiency + directed force
    VOL_COMPRESSION = "vol_compression"  # low efficiency / dead tape
    TRANSITION = "transition"  # force present but consensus incomplete (shift)


# ─── Catalog rows: definition + indicators + TFs ─────────────────────────────


@dataclass(frozen=True)
class RegimeSpec:
    regime_id: RegimeId
    meaning: str
    source: str  # creator_internet | mark_physics | hybrid_court
    playbook_hint: str  # what road allows (not a hard bot)
    indicator_group: IndicatorGroup
    timeframe_bindings: Tuple[TimeframeBinding, ...]
    # Classifier keys
    consensus_values: Tuple[str, ...] = ()
    efficiency_min: Optional[float] = None
    efficiency_max: Optional[float] = None
    require_directed_force: bool = False


def _all_set_htf_bindings() -> Tuple[TimeframeBinding, ...]:
    assert_mark_sets_law()
    return tuple(
        TimeframeBinding(
            set_id=s.set_id,
            set_name=s.name,
            ltf=s.entry_tf,
            htf=s.confirmation_tfs,
            uses_ltf=False,
            uses_htf=True,
        )
        for s in OFFICIAL_SETS
    )


def _all_set_full_bindings() -> Tuple[TimeframeBinding, ...]:
    assert_mark_sets_law()
    return tuple(
        TimeframeBinding(
            set_id=s.set_id,
            set_name=s.name,
            ltf=s.entry_tf,
            htf=s.confirmation_tfs,
            uses_ltf=True,
            uses_htf=True,
        )
        for s in OFFICIAL_SETS
    )


GROUP_REGIME_HTF = IndicatorGroup(
    group_id="regime_htf_consensus",
    description="Per-set HTF trend_dir on both confirm TFs; multi-set vote",
    indicators=(
        IndicatorSpec("trend_dir", (("lookback", 5),), role="force"),
        IndicatorSpec("trend_dir", (("lookback", 10),), role="force"),
        IndicatorSpec("htf_agree_per_set", (), role="force"),
        IndicatorSpec("multi_set_consensus", (), role="regime_gate"),
    ),
)

GROUP_REGIME_VOL = IndicatorGroup(
    group_id="regime_efficiency_vol",
    description="Efficiency / movement quality proxy (0 dead → 1 great) + force",
    indicators=(
        IndicatorSpec("efficiency", (), role="regime_gate"),
        IndicatorSpec("trend_dir", (("lookback", 5),), role="force"),
        IndicatorSpec("range_expansion_proxy", (), role="expansion"),
    ),
)

GROUP_REGIME_MARK = IndicatorGroup(
    group_id="regime_mark_physics",
    description="Mark multi-set consensus + entropy/chop mask idea (efficiency low)",
    indicators=(
        IndicatorSpec("multi_set_consensus", (), role="regime_gate"),
        IndicatorSpec("efficiency", (), role="regime_gate"),
        IndicatorSpec("trend_dir", (("lookback", 5),), role="force"),
        IndicatorSpec("conflict_flag", (), role="regime_gate"),
    ),
)


def creator_internet_regime_names() -> Tuple[str, ...]:
    """Creator catalog from regime literature (design class — not authority)."""
    return (
        "trend_bull",
        "trend_bear",
        "range_chop",
        "vol_expansion",
        "vol_compression",
        "transition",
        "conflict",  # multi-TF disagreement (Court-relevant)
    )


def mark_physics_regime_names() -> Tuple[str, ...]:
    """Mark/KAG catalog: multi-set eyes + chop/entropy + incomplete."""
    return (
        "trend_bull",  # agree_long
        "trend_bear",  # agree_short
        "range_chop",  # chop / high entropy
        "conflict",  # sets fight
        "incomplete",  # not enough HTF agreement
        "vol_expansion",  # great efficiency with force
        "vol_compression",  # dead efficiency
    )


def regime_catalog() -> Dict[RegimeId, RegimeSpec]:
    """Hybrid Court catalog — every production regime we will use."""
    htf = _all_set_htf_bindings()
    full = _all_set_full_bindings()
    return {
        RegimeId.TREND_BULL: RegimeSpec(
            regime_id=RegimeId.TREND_BULL,
            meaning="Multi-set HTF force agrees long (agree_long).",
            source="hybrid_court",
            playbook_hint="Long-side pullbacks/continuations on official sets; no short thrash.",
            indicator_group=GROUP_REGIME_HTF,
            timeframe_bindings=htf,
            consensus_values=("agree_long",),
            require_directed_force=True,
        ),
        RegimeId.TREND_BEAR: RegimeSpec(
            regime_id=RegimeId.TREND_BEAR,
            meaning="Multi-set HTF force agrees short (agree_short).",
            source="hybrid_court",
            playbook_hint="Short-side pullbacks/continuations; no long thrash.",
            indicator_group=GROUP_REGIME_HTF,
            timeframe_bindings=htf,
            consensus_values=("agree_short",),
            require_directed_force=True,
        ),
        RegimeId.RANGE_CHOP: RegimeSpec(
            regime_id=RegimeId.RANGE_CHOP,
            meaning="No multi-set directed consensus; chop / flat force.",
            source="hybrid_court",
            playbook_hint="Wait or reduce fire; mean-revert only if later Court PROMOTE.",
            indicator_group=GROUP_REGIME_MARK,
            timeframe_bindings=htf,
            consensus_values=("chop",),
        ),
        RegimeId.CONFLICT: RegimeSpec(
            regime_id=RegimeId.CONFLICT,
            meaning="Official sets disagree on HTF side (conflict).",
            source="mark_physics",
            playbook_hint="KILL new risk; hearing wait_subtype=kill.",
            indicator_group=GROUP_REGIME_MARK,
            timeframe_bindings=htf,
            consensus_values=("conflict",),
        ),
        RegimeId.INCOMPLETE: RegimeSpec(
            regime_id=RegimeId.INCOMPLETE,
            meaning="Insufficient HTF agreement / incomplete multi-set eyes.",
            source="mark_physics",
            playbook_hint="Wait for confirmation; no force-side fire.",
            indicator_group=GROUP_REGIME_HTF,
            timeframe_bindings=htf,
            consensus_values=("incomplete",),
        ),
        RegimeId.VOL_EXPANSION: RegimeSpec(
            regime_id=RegimeId.VOL_EXPANSION,
            meaning="High efficiency/movement quality with directed force (trend vol).",
            source="creator_internet",
            playbook_hint="Allow continuation/pullback with force; favor R capture.",
            indicator_group=GROUP_REGIME_VOL,
            timeframe_bindings=full,
            efficiency_min=0.70,
            require_directed_force=True,
        ),
        RegimeId.VOL_COMPRESSION: RegimeSpec(
            regime_id=RegimeId.VOL_COMPRESSION,
            meaning="Low efficiency / dead tape (compression).",
            source="creator_internet",
            playbook_hint="Wait or micro size only; avoid thrash.",
            indicator_group=GROUP_REGIME_VOL,
            timeframe_bindings=full,
            efficiency_max=0.25,
        ),
        RegimeId.TRANSITION: RegimeSpec(
            regime_id=RegimeId.TRANSITION,
            meaning="Directed force on some sets but multi-set consensus still incomplete.",
            source="hybrid_court",
            playbook_hint="Cautious; prefer wait or single strong-set pullback under A12.",
            indicator_group=GROUP_REGIME_HTF,
            timeframe_bindings=htf,
            consensus_values=("incomplete",),
            require_directed_force=True,
        ),
    }


def classify_regime_court(
    *,
    multi_set_consensus: str,
    efficiency: float = 0.5,
    force: float = 0.0,
) -> RegimeId:
    """Map Court sensors → production RegimeId (priority order).

    Priority (Court): conflict > vol_compression > vol_expansion (if directed)
    > trend_bull/bear > transition > incomplete > range_chop.
    """
    c = str(multi_set_consensus or "incomplete").lower()
    eff = float(efficiency)
    f = float(force)
    directed = abs(f) >= FORCE_FLAT_ABS

    if c == "conflict":
        return RegimeId.CONFLICT
    if eff <= 0.25:
        return RegimeId.VOL_COMPRESSION
    if c == "agree_long" and (directed or abs(f) >= FORCE_CLEAR_ABS * 0.5):
        if eff >= 0.70:
            return RegimeId.VOL_EXPANSION
        return RegimeId.TREND_BULL
    if c == "agree_short" and (directed or abs(f) >= FORCE_CLEAR_ABS * 0.5):
        if eff >= 0.70:
            return RegimeId.VOL_EXPANSION
        return RegimeId.TREND_BEAR
    if c == "incomplete" and directed:
        return RegimeId.TRANSITION
    if c == "incomplete":
        return RegimeId.INCOMPLETE
    if c == "chop" or not directed:
        return RegimeId.RANGE_CHOP
    # Fallback from force alone
    m = classify_momentum(f)
    if m.value == "bull":
        return RegimeId.TREND_BULL
    if m.value == "bear":
        return RegimeId.TREND_BEAR
    return RegimeId.RANGE_CHOP


def regime_allows_fire(regime: RegimeId) -> bool:
    """Road sign: which regimes admit new risk triggers (not size)."""
    return regime in (
        RegimeId.TREND_BULL,
        RegimeId.TREND_BEAR,
        RegimeId.VOL_EXPANSION,
        RegimeId.TRANSITION,  # cautious allow — path still needs structure trigger
    )


def regime_kill_new_risk(regime: RegimeId) -> bool:
    return regime in (RegimeId.CONFLICT, RegimeId.VOL_COMPRESSION)


def catalog_self_check() -> Dict[str, Any]:
    cat = regime_catalog()
    assert len(cat) == 8
    assert set(cat.keys()) == set(RegimeId)
    # Every regime has indicators + Mark TF bindings
    for rid, spec in cat.items():
        assert spec.indicator_group.indicators, rid
        assert len(spec.timeframe_bindings) == 4, rid
        for b in spec.timeframe_bindings:
            assert b.set_id in (1, 2, 3, 4)
    # Discriminating classifications
    assert classify_regime_court(multi_set_consensus="conflict") == RegimeId.CONFLICT
    assert classify_regime_court(multi_set_consensus="agree_long", force=0.4, efficiency=0.5) == RegimeId.TREND_BULL
    assert classify_regime_court(multi_set_consensus="agree_short", force=-0.4, efficiency=0.5) == RegimeId.TREND_BEAR
    assert classify_regime_court(multi_set_consensus="agree_long", force=0.5, efficiency=0.85) == RegimeId.VOL_EXPANSION
    assert classify_regime_court(multi_set_consensus="chop", efficiency=0.1) == RegimeId.VOL_COMPRESSION
    assert classify_regime_court(multi_set_consensus="incomplete", force=0.0) == RegimeId.INCOMPLETE
    assert classify_regime_court(multi_set_consensus="incomplete", force=0.4) == RegimeId.TRANSITION
    assert classify_regime_court(multi_set_consensus="chop", force=0.0, efficiency=0.5) == RegimeId.RANGE_CHOP
    assert regime_kill_new_risk(RegimeId.CONFLICT)
    assert regime_allows_fire(RegimeId.TREND_BULL)
    assert not regime_allows_fire(RegimeId.CONFLICT)
    # Creator names ⊆ hybrid; Mark names ⊆ hybrid
    hybrid = {r.value for r in RegimeId}
    for n in creator_internet_regime_names():
        assert n in hybrid, n
    for n in mark_physics_regime_names():
        assert n in hybrid, n
    return {"ok": True, "n_regimes": len(cat)}


# ─── CASE-0017: regime-aware meta curriculum (road for the learner) ─────────
# Curriculum samples A17 regimes and labels teacher with fire/kill playbook.
# Does NOT expand META_RL_DIM; does NOT thrash goal_path fills.


def all_curriculum_regimes() -> Tuple[RegimeId, ...]:
    """Every production regime must appear in the meta curriculum."""
    return tuple(RegimeId)


def sample_curriculum_regime(rng: Any) -> RegimeId:
    """Uniform sample over the 8 Court regimes (balanced road coverage)."""
    regs = all_curriculum_regimes()
    return regs[int(rng.integers(0, len(regs)))]


def regime_sensor_template(regime: RegimeId) -> Dict[str, float | str]:
    """Synthetic multi_set_consensus / force / efficiency that classifies to `regime`."""
    rid = regime if isinstance(regime, RegimeId) else RegimeId(str(regime))
    if rid == RegimeId.CONFLICT:
        return {"multi_set_consensus": "conflict", "force": 0.0, "efficiency": 0.5}
    if rid == RegimeId.VOL_COMPRESSION:
        return {"multi_set_consensus": "chop", "force": 0.0, "efficiency": 0.1}
    if rid == RegimeId.VOL_EXPANSION:
        # side-agnostic template; caller may flip force sign for bear expansion
        return {"multi_set_consensus": "agree_long", "force": 0.6, "efficiency": 0.85}
    if rid == RegimeId.TREND_BULL:
        return {"multi_set_consensus": "agree_long", "force": 0.45, "efficiency": 0.55}
    if rid == RegimeId.TREND_BEAR:
        return {"multi_set_consensus": "agree_short", "force": -0.45, "efficiency": 0.55}
    if rid == RegimeId.TRANSITION:
        return {"multi_set_consensus": "incomplete", "force": 0.4, "efficiency": 0.5}
    if rid == RegimeId.INCOMPLETE:
        return {"multi_set_consensus": "incomplete", "force": 0.0, "efficiency": 0.5}
    if rid == RegimeId.RANGE_CHOP:
        return {"multi_set_consensus": "chop", "force": 0.0, "efficiency": 0.5}
    return {"multi_set_consensus": "incomplete", "force": 0.0, "efficiency": 0.5}


def teacher_action_under_regime(
    regime: RegimeId,
    *,
    mean_dir: float,
    allow: bool,
    risk_rem: float,
    hardness: float,
    pressure: float,
    topology: str,
) -> str:
    """A17 playbook teacher: kill/no-fire regimes → wait; fire regimes → goal-conditioned side.

    Road (not cliff): stable labels the meta-policy can fit. No pad fills.
    """
    rid = regime if isinstance(regime, RegimeId) else RegimeId(str(regime))
    # Hard kill + non-allow regimes never teach thrash fires
    if regime_kill_new_risk(rid) or not regime_allows_fire(rid):
        return "wait"
    if topology in ("chop", "collapse") and abs(float(mean_dir)) < 0.35:
        return "wait"
    if topology == "slingshot_load":
        return "wait"
    if not allow or float(risk_rem) <= 0.05:
        return "wait"
    thr = 0.22 + 0.25 * float(hardness) - 0.08 * float(pressure)
    # Transition is cautious: slightly higher direction bar
    if rid == RegimeId.TRANSITION:
        thr += 0.08
    if abs(float(mean_dir)) < thr:
        return "wait"
    return "long" if float(mean_dir) > 0 else "short"


def build_official_for_regime(
    regime: RegimeId,
    *,
    rng: Any = None,
    side: int = 1,
    strength: float = 0.7,
) -> Dict[int, Any]:
    """Build Mark-set confluence dict consistent with regime (curriculum only)."""
    from .types import Direction, SetConfluence, VelocityStrength

    rid = regime if isinstance(regime, RegimeId) else RegimeId(str(regime))
    side_i = 1 if int(side) >= 0 else -1
    # Force side from regime when directed
    if rid in (RegimeId.TREND_BULL, RegimeId.VOL_EXPANSION):
        side_i = 1
    elif rid in (RegimeId.TREND_BEAR,):
        side_i = -1
    elif rid == RegimeId.TRANSITION:
        side_i = 1 if float(strength) >= 0 else -1

    stren = float(strength)
    vel = VelocityStrength.STRONG if stren > 0.6 else VelocityStrength.MEDIUM
    official: Dict[int, Any] = {}

    for sid in (1, 2, 3, 4):
        if rid == RegimeId.CONFLICT:
            # Half bull, half bear → multi-set fight
            direction = Direction.BULL if sid % 2 == 1 else Direction.BEAR
            n_bull, n_bear, n_neutral = (3, 0, 0) if direction == Direction.BULL else (0, 3, 0)
            v = VelocityStrength.MEDIUM
        elif rid in (RegimeId.RANGE_CHOP, RegimeId.VOL_COMPRESSION, RegimeId.INCOMPLETE):
            direction = Direction.NEUTRAL
            n_bull = n_bear = n_neutral = 1
            v = VelocityStrength.WEAK
        elif rid == RegimeId.TRANSITION:
            # Incomplete eyes: only lower sets directed
            if sid <= 2:
                direction = Direction.BULL if side_i > 0 else Direction.BEAR
                n_bull, n_bear, n_neutral = (3, 0, 0) if side_i > 0 else (0, 3, 0)
                v = vel
            else:
                direction = Direction.NEUTRAL
                n_bull = n_bear = n_neutral = 1
                v = VelocityStrength.WEAK
        else:
            # trend / vol expansion: all sets agree
            if side_i > 0:
                direction = Direction.BULL
                n_bull, n_bear, n_neutral = 3, 0, 0
            else:
                direction = Direction.BEAR
                n_bull, n_bear, n_neutral = 0, 3, 0
            v = VelocityStrength.STRONG if rid == RegimeId.VOL_EXPANSION else vel
        official[sid] = SetConfluence(
            set_key=f"set{sid}",
            direction=direction,
            velocity=v,
            n_bull=n_bull,
            n_bear=n_bear,
            n_neutral=n_neutral,
        )
    return official


def curriculum_regime_self_check() -> Dict[str, Any]:
    """Pin: templates classify correctly; teacher kills conflict; fire regimes can fire."""
    for rid in all_curriculum_regimes():
        tpl = regime_sensor_template(rid)
        got = classify_regime_court(
            multi_set_consensus=str(tpl["multi_set_consensus"]),
            force=float(tpl["force"]),
            efficiency=float(tpl["efficiency"]),
        )
        # VOL_EXPANSION template uses agree_long; classify must match
        if rid == RegimeId.VOL_EXPANSION:
            assert got == RegimeId.VOL_EXPANSION, (rid, got)
        else:
            assert got == rid, (rid, got)
        off = build_official_for_regime(rid, side=1, strength=0.8)
        assert len(off) == 4
    # Teacher: kill never fires even with strong dir + allow
    assert (
        teacher_action_under_regime(
            RegimeId.CONFLICT,
            mean_dir=0.9,
            allow=True,
            risk_rem=1.0,
            hardness=0.2,
            pressure=0.5,
            topology="launch",
        )
        == "wait"
    )
    assert (
        teacher_action_under_regime(
            RegimeId.VOL_COMPRESSION,
            mean_dir=0.9,
            allow=True,
            risk_rem=1.0,
            hardness=0.2,
            pressure=0.5,
            topology="launch",
        )
        == "wait"
    )
    fire = teacher_action_under_regime(
        RegimeId.TREND_BULL,
        mean_dir=0.9,
        allow=True,
        risk_rem=1.0,
        hardness=0.2,
        pressure=0.5,
        topology="launch",
    )
    assert fire == "long"
    return {"ok": True, "n_regimes": len(all_curriculum_regimes())}


# ─── CASE-0018: day-path / inference regime channel (doctrine block) ────────
# Pack A17 regime into Mark doctrine (16-dim) so frozen policy *sees* regime
# without expanding META_RL_DIM. Curriculum and day path share the same packer.


# Fixed order for one-hot (must stay stable for trained weights)
REGIME_ONEHOT_ORDER: Tuple[RegimeId, ...] = (
    RegimeId.TREND_BULL,
    RegimeId.TREND_BEAR,
    RegimeId.RANGE_CHOP,
    RegimeId.CONFLICT,
    RegimeId.INCOMPLETE,
    RegimeId.VOL_EXPANSION,
    RegimeId.VOL_COMPRESSION,
    RegimeId.TRANSITION,
)

# Doctrine layout indices (within DOCTRINE_DIM=16 Mark block at state[32:48])
IDX_REGIME_ONEHOT0 = 0  # …7 one-hot
IDX_REGIME_ALLOW = 8
IDX_REGIME_KILL = 9
IDX_REGIME_FORCE = 10
IDX_REGIME_EFFICIENCY = 11
# 12–15 reserved


def encode_regime_doctrine(
    regime: RegimeId,
    *,
    force: float = 0.0,
    efficiency: float = 0.5,
    doctrine_dim: int = 16,
) -> "np.ndarray":
    """CASE-0018: pack A17 regime into Mark doctrine vector (no META_RL_DIM change).

    Layout: [onehot×8 | allow_fire | kill | force | efficiency | pad]
    Shared by curriculum sample_training_state and day-path build_meta_rl_state.
    """
    import numpy as np

    rid = regime if isinstance(regime, RegimeId) else RegimeId(str(regime))
    dim = int(doctrine_dim)
    out = np.zeros(dim, dtype=np.float32)
    try:
        i = REGIME_ONEHOT_ORDER.index(rid)
    except ValueError:
        i = REGIME_ONEHOT_ORDER.index(RegimeId.INCOMPLETE)
    if i < dim:
        out[i] = 1.0
    if dim > IDX_REGIME_ALLOW:
        out[IDX_REGIME_ALLOW] = 1.0 if regime_allows_fire(rid) else 0.0
    if dim > IDX_REGIME_KILL:
        out[IDX_REGIME_KILL] = 1.0 if regime_kill_new_risk(rid) else 0.0
    if dim > IDX_REGIME_FORCE:
        out[IDX_REGIME_FORCE] = float(np.clip(force, -1.0, 1.0))
    if dim > IDX_REGIME_EFFICIENCY:
        out[IDX_REGIME_EFFICIENCY] = float(np.clip(efficiency, 0.0, 1.0))
    return out


def decode_regime_from_doctrine(doctrine: "np.ndarray") -> RegimeId:
    """Inverse of one-hot prefix (argmax); fallback incomplete."""
    import numpy as np

    d = np.asarray(doctrine, dtype=np.float32).reshape(-1)
    n = min(8, int(d.size))
    if n <= 0:
        return RegimeId.INCOMPLETE
    i = int(np.argmax(d[:n]))
    if i < 0 or i >= len(REGIME_ONEHOT_ORDER) or float(d[i]) <= 0.0:
        return RegimeId.INCOMPLETE
    return REGIME_ONEHOT_ORDER[i]


def regime_from_edge_sensors(
    *,
    multi_set_consensus: str,
    consensus_force: float = 0.0,
    efficiency: float = 0.5,
) -> RegimeId:
    """Day-path helper: map Edge snapshot sensors → A17 RegimeId."""
    return classify_regime_court(
        multi_set_consensus=str(multi_set_consensus or "incomplete"),
        force=float(consensus_force),
        efficiency=float(efficiency),
    )


def day_path_regime_skip_new_risk(regime: RegimeId) -> bool:
    """Road sign for day path: skip new risk when A17 says kill (not pad)."""
    return regime_kill_new_risk(regime)


def efficiency_proxy_from_edge(
    *,
    n_pullback: int = 0,
    n_continuation: int = 0,
    consensus_force: float = 0.0,
) -> float:
    """Honest efficiency proxy from available Court sensors (no look-ahead)."""
    base = 0.30
    if int(n_pullback) + int(n_continuation) > 0:
        base = 0.55
    # Strong multi-set force → higher efficiency (vol expansion path)
    base = base + min(abs(float(consensus_force)), 0.5) * 0.5
    return float(max(0.0, min(1.0, base)))


def day_path_regime_channel_self_check() -> Dict[str, Any]:
    """Pin encode/decode round-trip and kill skip."""
    import numpy as np

    for rid in REGIME_ONEHOT_ORDER:
        vec = encode_regime_doctrine(rid, force=0.4, efficiency=0.6)
        assert vec.shape[0] == 16
        assert decode_regime_from_doctrine(vec) == rid
        assert float(vec[IDX_REGIME_ALLOW]) == (1.0 if regime_allows_fire(rid) else 0.0)
        assert float(vec[IDX_REGIME_KILL]) == (1.0 if regime_kill_new_risk(rid) else 0.0)
    assert day_path_regime_skip_new_risk(RegimeId.CONFLICT)
    assert day_path_regime_skip_new_risk(RegimeId.VOL_COMPRESSION)
    assert not day_path_regime_skip_new_risk(RegimeId.TREND_BULL)
    # Distinct encodings
    a = encode_regime_doctrine(RegimeId.TREND_BULL)
    b = encode_regime_doctrine(RegimeId.CONFLICT)
    assert not np.allclose(a, b)
    return {"ok": True, "doctrine_dim": 16, "n_regimes": len(REGIME_ONEHOT_ORDER)}
