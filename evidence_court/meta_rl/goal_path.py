"""Goal-conditioned multi-leg day path (CASE-0003).

Internet class: hierarchical / goal-conditioned RL — sequential subgoals under a
hard risk budget (no retrain; target/risk are inference context only).
Refs: goal-conditioned RL / hierarchical trading policies (design class).

Mark class: HTF force permission + LTF RSI5/BB timing; wait slingshot_load;
fire pullback_resume / continuation; lock when target hit.

No look-ahead: each slot uses only bars completed before decision time.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .edge import (
    build_tf_cache,
    count_actionable_side_agree,
    edge_sensors,
    edge_to_set_confluence,
    path_side_permission_ok,
    scan_all_sets,
    side_permission_ok,
)
from .leverage import LEVERAGE, risk_legal_max_lot, stop_distance_price_from_pct
from .opportunity_watch import (
    OpportunityWatchAgent,
    curriculum_labels_from_report,
    session_band,
    watch_day_summary,
)
from .policy import FrozenMetaPolicy, PolicyAction
from .risk import (
    DailyRiskLedger,
    FrictionAssumptions,
    OpenPosition,
    apply_trade_result,
    size_position_risk_percent,
)
from .roles import evaluate_understanding, novel_composition, rename_sensors, swap_family
from .senses import MarketSenseInput, encode_sense_report, probe_all_senses
from .regimes import (
    day_path_regime_skip_new_risk,
    efficiency_proxy_from_edge,
    encode_regime_doctrine,
    regime_from_edge_sensors,
)
from .state import build_meta_rl_state
from .trade_mental_replay import (
    build_trade_mental_replay,
    mid_time as tmr_mid_time,
    teachers_from_mental_replay,
)
from .types import StructureFlags

# Law A13 (Monty overrules Judge): production day MUST land 8–400 trades.
# DEFAULT_SLOTS (5) cannot satisfy min 8 → NON-COMPLIANT as production path (lab shadow only).
DEFAULT_SLOTS: Tuple[str, ...] = ("07:00:00", "10:00:00", "13:00:00", "16:00:00", "19:00:00")
DEFAULT_STOP_DISTANCE_PCT = 0.45  # slightly wider → fewer noise stops; size scales via risk %
# CASE-0009: London–NY active windows on the legacy 5-slot grid (lab only under A13)
PRIME_SESSION_SLOTS: Tuple[str, ...] = ("10:00:00", "13:00:00", "16:00:00")
# Law A13 hard mandate (Monty) — every production day must land in this band
SCALPING_TRADES_PER_DAY_MIN = 8
SCALPING_TRADES_PER_DAY_MAX = 400
DEFAULT_SESSION_MIN_ALIGN = 1.5e-4  # mild same-day lean with force (~noise floor)


def session_min_align_for_path(*, multi_set_agree: bool = False) -> float:
    """CASE-0030: multi-set HTF agree eases same-day path confirm threshold.

    When Mark multi-set agrees, HTF confluence already is the primary bias —
    do not also require a non-trivial open→asof lean (which starves quiet days).
    Non-multi keeps DEFAULT_SESSION_MIN_ALIGN (anti thrash). min_align=0 still
    requires correct *sign* of session move (session_confirms_side).
    """
    if multi_set_agree:
        return 0.0
    return float(DEFAULT_SESSION_MIN_ALIGN)


def a13_trade_count_ok(n_trades: int) -> bool:
    """Law A13: True iff production day trade count is in [8, 400]."""
    n = int(n_trades)
    return SCALPING_TRADES_PER_DAY_MIN <= n <= SCALPING_TRADES_PER_DAY_MAX


def assert_a13_trade_count(n_trades: int) -> None:
    """Raise AssertionError if trade count is outside Law A13 hard band."""
    n = int(n_trades)
    if not a13_trade_count_ok(n):
        raise AssertionError(
            f"A13 breach: trades/day={n} not in "
            f"[{SCALPING_TRADES_PER_DAY_MIN}, {SCALPING_TRADES_PER_DAY_MAX}] "
            f"(Monty mandate: MUST take 8–400 trades every day)"
        )


def build_scalping_cadence_slots(
    *,
    start_hour: int = 7,
    end_hour: int = 20,
    interval_minutes: int = 30,
) -> Tuple[str, ...]:
    """CASE-0011: dense decision clock for A13 path capacity (no pad fills).

    Returns HH:MM:SS strings from start_hour inclusive through end_hour inclusive
    at fixed interval. Production default is 30m → capacity ≥8 and ≤400.
    """
    if interval_minutes <= 0:
        raise ValueError("interval_minutes must be positive")
    out: List[str] = []
    # minutes from midnight
    t = int(start_hour) * 60
    end = int(end_hour) * 60
    step = int(interval_minutes)
    while t <= end:
        hh, mm = divmod(t, 60)
        if hh > 23:
            break
        out.append(f"{hh:02d}:{mm:02d}:00")
        t += step
        if len(out) > SCALPING_TRADES_PER_DAY_MAX * 2:
            break  # safety
    return tuple(out)


# CASE-0011 lab / pin grid (30m) — name kept for historical tests
SCALPING_CADENCE_SLOTS: Tuple[str, ...] = build_scalping_cadence_slots(interval_minutes=30)
# CASE-0023 15m pin (regression / lab shadow)
PRODUCTION_SCALPING_SLOTS_15M: Tuple[str, ...] = build_scalping_cadence_slots(
    interval_minutes=15
)
# CASE-0027 10m pin (A25 law) — denser than 15m, coarser than production
PRODUCTION_SCALPING_SLOTS_10M: Tuple[str, ...] = build_scalping_cadence_slots(
    interval_minutes=10
)
# CASE-0029 production grid (5m): structural density continuation of A25 (empty skip, no pad)
PRODUCTION_CADENCE_INTERVAL_MIN = 5
PRODUCTION_SCALPING_SLOTS: Tuple[str, ...] = build_scalping_cadence_slots(
    interval_minutes=PRODUCTION_CADENCE_INTERVAL_MIN
)

# Continuation outside prime only when multi-set agrees + strong force (CASE-0023/0026)
# CASE-0026: multi-set densify — extended floor 0.35→0.28 (still multi-set-only, no pad)
CONT_EXTENDED_FORCE_MIN = 0.28
ACTIVE_CONT_HOUR_START = 8
ACTIVE_CONT_HOUR_END = 18
# CASE-0025: dense London–NY overlap prime band (hours inclusive) for cont session-ok
PRIME_BAND_HOUR_START = 12
PRIME_BAND_HOUR_END = 16
# CASE-0026: multi-set cont entry floor on prime (was hard-coded 0.32)
MULTI_SET_CONT_ENTRY_FORCE_MIN = 0.28


def max_fills_for_a13(target_percent: float = 0.0) -> int:
    """CASE-0011: hard fill cap at A13 max (envelope still limits risk)."""
    _ = target_percent  # reserved for future goal-conditioned cap shaping
    return int(SCALPING_TRADES_PER_DAY_MAX)


def allows_empty_slot_skip() -> bool:
    """CASE-0011 Mark counter: empty candidates must skip (no synthetic pad trades)."""
    return True


@dataclass
class LegFill:
    symbol: str
    slot: str
    act: str
    size_risk_percent: float
    pnl_percent: float
    topology: str
    edge_kind: str
    lot: float


def m1_window(
    m1: Sequence[dict],
    *,
    date: str,
    start_time: str,
    end_time: Optional[str],
) -> List[dict]:
    out: List[dict] = []
    for b in m1:
        if str(b.get("date", "")) != date:
            continue
        t = str(b.get("time", "00:00:00"))
        if t < start_time:
            continue
        if end_time is not None and t >= end_time:
            continue
        out.append(b)
    return out


def is_prime_session_slot(slot: str) -> bool:
    """CASE-0009 / CASE-0025: high-liquidity session decision times.

    Classic named primes (10/13/16) remain. CASE-0025 densifies cont session-ok
    across London–NY overlap hours [PRIME_BAND_HOUR_START, PRIME_BAND_HOUR_END]
    on the production 15m grid. Thin open / late fade stay non-prime; shoulders
    still use multi-set extended path (A22).
    """
    s = str(slot)
    if s in PRIME_SESSION_SLOTS:
        return True
    try:
        hh = int(s.split(":")[0])
    except (TypeError, ValueError, IndexError):
        return False
    return int(PRIME_BAND_HOUR_START) <= hh <= int(PRIME_BAND_HOUR_END)


def next_slot_end_time(
    slot: str,
    slots: Sequence[str],
    *,
    eod: str = "23:59:59",
) -> str:
    """CASE-0010: fill path ends at next decision slot (multi-leg capacity).

    Last / unknown slot → EOD. No look-ahead past scheduled slot times.
    """
    slot_list = [str(s) for s in slots]
    s = str(slot)
    try:
        i = slot_list.index(s)
    except ValueError:
        return eod
    if i + 1 < len(slot_list):
        return slot_list[i + 1]
    return eod


def _slot_to_minutes(slot: str) -> int:
    """HH:MM[:SS] → minutes from midnight."""
    parts = str(slot).split(":")
    try:
        hh = int(parts[0])
        mm = int(parts[1]) if len(parts) > 1 else 0
    except (TypeError, ValueError, IndexError):
        return 0
    return hh * 60 + mm


def next_slot_end_after_minutes(
    slot: str,
    slots: Sequence[str],
    minutes: int,
    *,
    eod: str = "23:59:59",
) -> str:
    """First scheduled slot at least ``minutes`` after ``slot`` (else EOD).

    CASE-0028: cont min hold path without look-ahead past the slot grid.
    """
    slot_list = [str(s) for s in slots]
    s = str(slot)
    try:
        i = slot_list.index(s)
    except ValueError:
        return eod
    target = _slot_to_minutes(s) + max(0, int(minutes))
    for j in range(i + 1, len(slot_list)):
        if _slot_to_minutes(slot_list[j]) >= target:
            return slot_list[j]
    return eod


# ---------------------------------------------------------------------------
# SCALPING HOLD LAW (Monty 2026-08-10 overrule — A13 identity)
# This is a **scalping** meta-RL bot. Trade life is short.
# Conversion = many quality scalps + progressive size-up — NOT multi-hour holds.
# Prior CASE-0028 30m cont / EOD pullback was swing-like; too long for scalp class.
# ---------------------------------------------------------------------------
CONT_HOLD_MIN_MINUTES = 10  # continuation scalp window (was 30 — too long)
PB_HOLD_MIN_MINUTES = 15  # pullback scalp runner (was EOD — not scalping)
# method_hold: NEVER extend past scalp window (was 120m — forbidden for scalp class)
METHOD_HOLD_CONT_MINUTES = CONT_HOLD_MIN_MINUTES
METHOD_HOLD_SIZE_R_ARM = 1.0  # scalp: bank at 1R; progressive size carries conversion


def fill_hold_end_time(
    topology: str,
    slot: str,
    slots: Sequence[str],
    *,
    eod: str = "23:59:59",
    cont_hold_min_minutes: int = CONT_HOLD_MIN_MINUTES,
    pb_hold_min_minutes: int = PB_HOLD_MIN_MINUTES,
) -> str:
    """Scalp hold windows — short for both topologies (Monty scalp law).

    Continuation: ``cont_hold_min_minutes`` (default **10m**).
    Pullback resume: ``pb_hold_min_minutes`` (default **15m**) — not EOD.
    Last slot → EOD for both (no look-ahead past day).
    """
    if str(topology) == "pullback_resume":
        return next_slot_end_after_minutes(
            slot, slots, int(pb_hold_min_minutes), eod=eod
        )
    return next_slot_end_after_minutes(
        slot, slots, int(cont_hold_min_minutes), eod=eod
    )


def n_symbols_per_slot() -> int:
    """CASE-0012: one best symbol per decision slot (anti multi-symbol thrash).

    Multi-symbol book still via later slots (A8 flea-jar), not concurrent same-slot.
    CASE-0013 residual phase may use symbols_per_slot_for_leg instead.
    """
    return 1


def residual_leg_allowed(
    n_fills_so_far: int,
    *,
    realized_pnl_percent: float = 0.0,
    topology: str = "continuation",
    anchor_fills: int = 1,
    require_profit: bool = True,
    continuation_only: bool = True,
) -> bool:
    """CASE-0019: residual micro/multi only after anchor when dual-safe.

    Road (anti F-019): do not thrash residual into losses or pullback EOD path.
    Residual legs require:
      - n_fills >= anchor_fills
      - realized_pnl > 0 when require_profit (default)
      - topology == continuation when continuation_only (default)
    """
    if int(n_fills_so_far) < int(anchor_fills):
        return False
    if require_profit and float(realized_pnl_percent) <= 0.0:
        return False
    if continuation_only and str(topology) != "continuation":
        return False
    return True


def residual_size_scale(
    n_fills_so_far: int,
    *,
    anchor_fills: int = 1,
    micro_scale: float = 0.25,
    realized_pnl_percent: float = 0.0,
    topology: str = "continuation",
    profit_gate: bool = False,
    continuation_only: bool = False,
) -> float:
    """CASE-0013: full size for first anchor fills; then micro residual scale.

    CASE-0019 (opt-in via profit_gate/continuation_only): residual scale only when
    ``residual_leg_allowed`` — else 0.0 (block residual thrash; no pad).

    Defaults keep CASE-0013 pin tests (ungated micro after anchor).
    """
    if int(n_fills_so_far) < int(anchor_fills):
        return 1.0
    if profit_gate or continuation_only:
        if not residual_leg_allowed(
            n_fills_so_far,
            realized_pnl_percent=realized_pnl_percent,
            topology=topology,
            anchor_fills=anchor_fills,
            require_profit=profit_gate,
            continuation_only=continuation_only,
        ):
            return 0.0
    s = float(micro_scale)
    if s <= 0.0 or s >= 1.0:
        s = 0.25
    return s


def symbols_per_slot_for_leg(
    n_fills_so_far: int,
    *,
    anchor_fills: int = 1,
    residual_n: int = 3,
    realized_pnl_percent: float = 0.0,
    profit_gate: bool = False,
) -> int:
    """CASE-0013: 1 symbol on anchor legs; multi-symbol only when residual/micro.

    CASE-0019: when profit_gate, multi only if realized_pnl > 0 after anchor
    (topology gate applied per-leg via residual_size_scale).
    """
    if int(n_fills_so_far) < int(anchor_fills):
        return 1
    if profit_gate and float(realized_pnl_percent) <= 0.0:
        return 1
    return max(1, int(residual_n))


def production_symbols_per_slot(
    *,
    multi_set_consensus: str = "incomplete",
    dual_on_agree: bool = True,
    aggressive_capture: bool = False,
) -> int:
    """CASE-0021 base: 1 best symbol. CASE-0030: 2 when multi-set agrees (real dual book).

    Not residual thrash (F-017/F-019): dual only on agree_long/agree_short consensus.
    Incomplete/chop/conflict stay 1-sym (or kill path already filters conflict).

    ``aggressive_capture`` (lab/shadow): up to 3 symbols so FX PB/cont are not
    starved by XAU rank bias — still no pad; risk envelope hard.
    """
    if aggressive_capture:
        if dual_on_agree and str(multi_set_consensus) in ("agree_long", "agree_short"):
            return 3
        return 2
    if dual_on_agree and str(multi_set_consensus) in ("agree_long", "agree_short"):
        return 2
    return 1


def production_leg_size_scale(_n_fills_so_far: int = 0) -> float:
    """CASE-0021: full size every 1-sym leg — no residual micro starve (F-020).

    Residual multi/micro API (A20) remains for experiments; production day path
    uses full-scale 1-sym geometry (CASE-0012 class) on the A16–A19 road.
    """
    return 1.0


def real_edge_force_min(
    *,
    topology: str,
    multi_set_agree: bool = False,
) -> float:
    """CASE-0021/0026: honest force floors — denser when multi-set agrees.

    Not pad: floors stay strictly positive. Multi-set agree = real confluence
    (Mark eyes), so lower bar is still a real edge, not empty thrash.
    CASE-0026 densifies multi-set only; non-multi floors unchanged (A21).
    """
    topo = str(topology)
    if topo == "pullback_resume":
        return 0.10 if multi_set_agree else 0.15
    if topo == "continuation":
        return 0.15 if multi_set_agree else 0.22
    return 99.0  # non-fire topologies


def first_entry_cont_force_min(*, multi_set_agree: bool = False) -> float:
    """CASE-0021/0026: first leg cont stronger force; multi-set densified (0.28→0.24)."""
    return 0.24 if multi_set_agree else 0.35


def continuation_session_ok(
    slot: str,
    *,
    multi_set_agree: bool = False,
    force: float = 0.0,
    extended_force_min: float = CONT_EXTENDED_FORCE_MIN,
) -> bool:
    """CASE-0023: continuation session gate.

    - Prime slots (London–NY core): always session-ok (force floor separate).
    - Non-prime: only if multi-set HTF agree **and** |force| ≥ extended_force_min
      **and** hour in [8, 18] (active band) — real confluence density, not pad thrash.
    """
    if is_prime_session_slot(slot):
        return True
    if not multi_set_agree:
        return False
    if abs(float(force)) < float(extended_force_min):
        return False
    try:
        hh = int(str(slot).split(":")[0])
    except (TypeError, ValueError, IndexError):
        return False
    return int(ACTIVE_CONT_HOUR_START) <= hh <= int(ACTIVE_CONT_HOUR_END)


def entry_quality_ok(
    *,
    slot: str,
    topology: str,
    n_fills: int,
    force: float,
    cont_force_min: float = 0.40,
    multi_set_agree: bool = False,
) -> bool:
    """CASE-0009: pullback-first; continuation session+force gated.

    CASE-0021/0026: when multi_set_agree on prime, cont floor eases to
    MULTI_SET_CONT_ENTRY_FORCE_MIN (0.28 after CASE-0026 densify).
    CASE-0023: multi-set agree + strong force can open active-band non-prime cont
    (see continuation_session_ok). Pullback any slot. No pad.
    """
    if topology == "pullback_resume":
        return True
    if topology != "continuation":
        return False
    if not continuation_session_ok(
        slot, multi_set_agree=multi_set_agree, force=force
    ):
        return False
    floor = float(cont_force_min)
    if multi_set_agree:
        floor = min(floor, float(MULTI_SET_CONT_ENTRY_FORCE_MIN))
    # Non-prime extended path already requires extended_force_min
    if not is_prime_session_slot(slot):
        floor = max(floor, float(CONT_EXTENDED_FORCE_MIN))
    return abs(float(force)) >= floor


def session_confirms_side(
    m1: Sequence[dict],
    *,
    date: str,
    asof_time: str,
    side: int,
    min_bars: int = 20,
    min_align: float = 0.0,
) -> bool:
    """Prior-only same-day path must already lean with force (no future bars).

    ``min_align`` (CASE-0009): require signed open→asof move ≥ min_align with side
    after enough bars (filters mild counter-open thrash). Early day (&lt; min_bars)
    still allows HTF-only permission (flea-jar).
    """
    pre = m1_window(m1, date=date, start_time="00:00:00", end_time=asof_time)
    if len(pre) < min_bars:
        return True  # too early — allow HTF-only permission
    o = float(pre[0]["open"])
    c = float(pre[-1]["close"])
    if o <= 0:
        return False
    move = (c - o) / o
    align = float(min_align)
    if side > 0:
        return move >= align
    return move <= -align


def progressive_partial_floor(
    floating: float,
    *,
    goal_lock: Optional[float],
    partial_frac: Optional[float],
) -> Optional[float]:
    """CASE-0007: path-only partial floor = frac×lock when floating reaches it.

    Requires 0 < partial_frac < 1. Never grants floor above threshold without
    floating evidence (caller supplies floating from bars seen so far).
    """
    if goal_lock is None or partial_frac is None:
        return None
    frac = float(partial_frac)
    lock = float(goal_lock)
    if lock <= 0 or frac <= 0.0 or frac >= 1.0:
        return None
    threshold = frac * lock
    if float(floating) + 1e-12 >= threshold:
        return float(threshold)
    return None


def size_r_partial_floor(
    floating: float,
    *,
    size_risk_percent: float,
    arm_r: Optional[float],
    friction: float = 0.0,
) -> Optional[float]:
    """CASE-0008: path-only floor = size×arm_r − friction when floating reaches it.

    Independent of rem_goal (fixes F-012: half-rem_goal rarely binds). arm_r≥1.0
    preferred so noise excursions do not bank early.
    """
    if arm_r is None or size_risk_percent <= 0:
        return None
    ar = float(arm_r)
    if ar <= 0:
        return None
    fr = max(float(friction), 0.0)
    threshold = float(size_risk_percent) * ar - fr
    if threshold <= 0:
        return None
    if float(floating) + 1e-12 >= threshold:
        return float(threshold)
    return None


def simulate_fill_m1_path(
    *,
    side: int,
    bars: Sequence[dict],
    size_risk_percent: float,
    stop_distance_pct: float = DEFAULT_STOP_DISTANCE_PCT,
    friction_pct: float = 0.04,
    trail: bool = False,
    goal_lock_pnl_percent: Optional[float] = None,
    be_arm_r: float = 1.5,
    partial_lock_frac: Optional[float] = None,
    size_r_arm_r: Optional[float] = None,
) -> float:
    """Enter first open; hard stop; optional BE trail / partial floors / goal-lock.

    ``goal_lock_pnl_percent``: exit when unrealized equity-% reaches this
    (goal-conditioned take-profit — no look-ahead beyond path bars).

    ``trail`` + ``be_arm_r`` (CASE-0006 experimental): Full-BE win-path REJECTED (F-011).

    ``partial_lock_frac`` (CASE-0007): frac×goal_lock floor (F-012: alone insufficient).

    ``size_r_arm_r`` (CASE-0008): bank size×arm_r − fr when floating reaches it
    (independent of rem_goal; production arm_r=1.0).
    """
    if not bars or size_risk_percent <= 0:
        return 0.0
    o = float(bars[0]["open"])
    if o <= 0:
        return 0.0
    stop_frac = stop_distance_pct / 100.0
    fr = float(friction_pct) * 0.01
    r_dist = o * stop_frac
    stop_px = o - r_dist if side > 0 else o + r_dist
    lock = float(goal_lock_pnl_percent) if goal_lock_pnl_percent and goal_lock_pnl_percent > 0 else None
    be_armed = False
    arm_r = float(be_arm_r) if be_arm_r and be_arm_r > 0 else 1.5
    pnl_floor: Optional[float] = None

    for b in bars:
        h, l = float(b["high"]), float(b["low"])
        # Favorable floating from path bars only (for floor + goal lock)
        if side > 0:
            fav_pct = (h - o) / o * 100.0
        else:
            fav_pct = (o - l) / o * 100.0
        r_mult_fav = fav_pct / max(stop_distance_pct, 1e-6)
        floating = size_risk_percent * r_mult_fav - fr

        # CASE-0007: rem_goal-frac floor (secondary)
        if lock is not None and size_risk_percent > 0:
            fl = progressive_partial_floor(
                floating, goal_lock=lock, partial_frac=partial_lock_frac
            )
            if fl is not None:
                # never above lock or floating
                fl = min(fl, lock, floating)
                pnl_floor = fl if pnl_floor is None else max(pnl_floor, fl)

        # CASE-0008: size-R floor (primary lever; works when rem_goal huge)
        if size_risk_percent > 0:
            fl_r = size_r_partial_floor(
                floating,
                size_risk_percent=size_risk_percent,
                arm_r=size_r_arm_r,
                friction=fr,
            )
            if fl_r is not None:
                fl_r = min(fl_r, floating)
                if lock is not None:
                    fl_r = min(fl_r, lock)
                pnl_floor = fl_r if pnl_floor is None else max(pnl_floor, fl_r)

        # CASE-0006: optional BE trail (goal_path production wire uses trail=False)
        if trail and size_risk_percent > 0:
            if r_mult_fav >= arm_r:
                be_armed = True
                stop_px = o  # breakeven at entry

        if side > 0 and l <= stop_px:
            if be_armed and abs(stop_px - o) < 1e-12 * max(abs(o), 1.0):
                if pnl_floor is not None:
                    return float(pnl_floor)
                return float(-fr)
            if pnl_floor is not None:
                return float(pnl_floor)
            return float(-size_risk_percent - fr)
        if side < 0 and h >= stop_px:
            if be_armed and abs(stop_px - o) < 1e-12 * max(abs(o), 1.0):
                if pnl_floor is not None:
                    return float(pnl_floor)
                return float(-fr)
            if pnl_floor is not None:
                return float(pnl_floor)
            return float(-size_risk_percent - fr)
        # Full goal lock
        if lock is not None and size_risk_percent > 0 and floating >= lock:
            return float(lock)

    c = float(bars[-1]["close"])
    if side > 0:
        move_pct = (c - o) / o * 100.0
    else:
        move_pct = (o - c) / o * 100.0
    r_mult = float(np.clip(move_pct / max(stop_distance_pct, 1e-6), -1.0, 20.0))
    pnl = size_risk_percent * r_mult - fr
    if lock is not None:
        pnl = min(pnl, lock)
    if pnl_floor is not None:
        pnl = max(pnl, pnl_floor)
    return float(max(pnl, -size_risk_percent - fr))


def remaining_to_target(ledger: DailyRiskLedger, target_percent: float) -> float:
    return float(max(target_percent - ledger.realized_pnl_percent, 0.0))


def clear_expect_r(topology: str, target_percent: float) -> float:
    """CASE-0006: pullback_resume sizes for ~1.0R clear; continuation more conservative."""
    if topology == "pullback_resume":
        return 1.0
    if float(target_percent) <= 15.0:
        return 1.35
    return 1.9


def goal_path_size_for_clear(
    *,
    ledger: DailyRiskLedger,
    target_percent: float,
    topology: str,
    wounded: bool = False,
) -> float:
    """Size under envelope so expect_r covers remaining goal (CASE-0006 pure helper)."""
    rem_goal = remaining_to_target(ledger, target_percent)
    rem_risk = ledger.remaining_risk_budget_percent()
    if rem_risk <= 0.05 or rem_goal <= 0:
        return 0.0
    expect_r = clear_expect_r(topology, target_percent)
    size = min(
        rem_goal / max(expect_r, 0.5),
        rem_risk * 0.95,
        ledger.max_daily_risk_percent * (
            0.95 if ledger.realized_pnl_percent > 0 else 0.80
        ),
    )
    if wounded:
        size *= 0.85
    return float(max(size, 0.0))


# Monty executive order: intelligent size-up toward clear (still breach-0 rail).
INTELLIGENT_SIZE_UP = True


def intelligent_size_toward_clear(
    *,
    ledger: DailyRiskLedger,
    target_percent: float,
    topology: str,
    brain_size: float = 0.0,
    wounded: bool = False,
    edge_quality: float = 1.0,
    conf: float = 0.55,
) -> float:
    """Progressive size-up toward target + hard size-down near breach (scalp EO).

    Monty law (2026-08-10):
    - **Progressive size UP** when far from target and edge is live (reach clear).
    - **Size DOWN** when close to breach (thin remaining risk skin).
    - Brain head **blends** into legal progressive size (method binds; not pure max).
    - Never past remaining worst-case budget (breach 0).

    Scalping identity: conversion via many short legs × growing size — not one giant lot.
    """
    rem_goal = remaining_to_target(ledger, target_percent)
    rem_risk = ledger.remaining_risk_budget_percent()
    max_r = float(ledger.max_daily_risk_percent)
    if rem_risk <= 0.05 or rem_goal <= 0:
        return 0.0

    clear_sz = goal_path_size_for_clear(
        ledger=ledger,
        target_percent=target_percent,
        topology=topology,
        wounded=wounded,
    )
    brain = max(float(brain_size), 0.0)
    expect_r = clear_expect_r(topology, target_percent)
    # Scalp windows capture less path R → slightly softer R for size math when conf high
    eq = float(np.clip(edge_quality, 0.0, 1.5))
    cf = float(np.clip(conf, 0.0, 1.0))
    soft_r = max(expect_r * (1.0 - 0.30 * cf * min(eq, 1.0)), 0.45)
    progress = 1.0 - float(np.clip(rem_goal / max(float(target_percent), 1e-6), 0.0, 1.0))
    risk_skin = float(np.clip(rem_risk / max(max_r, 1e-6), 0.0, 1.0))  # 1=full, 0=empty
    high_q = cf >= 0.58 and eq >= 0.70
    mid_q = cf >= 0.45 and eq >= 0.50

    # --- Near breach: HARD size-down (Monty) ---
    if risk_skin < 0.22 or rem_risk < 0.35:
        tiny = min(rem_risk * 0.22, max(brain * 0.35, 0.08), clear_sz * 0.35)
        if wounded:
            tiny *= 0.85
        if tiny <= 0.05 or ledger.would_breach(tiny):
            return 0.0
        return float(max(tiny, 0.0))

    # --- Progressive size-UP toward target (far → larger share of rem_risk) ---
    # Leave room for later A13 legs when not high-q; open the throttle when far+clean.
    if high_q and progress < 0.30:
        budget_frac = 0.82  # progressive open: far from target, clean edge
    elif high_q and progress < 0.55:
        budget_frac = 0.70
    elif high_q and progress < 0.80:
        budget_frac = 0.58
    elif mid_q and progress < 0.40:
        budget_frac = 0.62  # medium edge still sizes up when far
    elif progress < 0.50:
        budget_frac = 0.48
    else:
        budget_frac = 0.38  # near clear — ease off, bank risk for protect
    if risk_skin < 0.40:
        budget_frac *= 0.72  # approach breach zone — taper
    if wounded:
        budget_frac *= 0.82

    progressive = min(rem_goal / soft_r, rem_risk * budget_frac)
    progressive *= float(np.clip(0.55 + 0.50 * cf * min(eq, 1.0), 0.50, 1.15))
    # Floor progressive near clear_sz when far from target so we actually climb
    if progress < 0.45:
        progressive = max(progressive, clear_sz * (1.05 if high_q else 0.95))

    # --- Brain blend (method binds) — not pure max(brain, clear, aggressive) ---
    # size = blend so size_down/up teachers and progressive both matter
    if brain > 0.05:
        # Weight brain more when conf high (method reclaim); progressive when far
        w_brain = float(np.clip(0.25 + 0.35 * cf, 0.25, 0.60))
        w_prog = 1.0 - w_brain
        size = w_brain * brain + w_prog * progressive
        # Far from target + high quality: never let tiny brain starve progressive up
        if progress < 0.40 and high_q:
            size = max(size, progressive * 0.90)
    else:
        size = progressive

    single_cap = rem_risk * (0.80 if high_q and progress < 0.45 else 0.62)
    day_cap = max_r * (0.85 if high_q and progress < 0.5 else 0.72)
    size = min(size, single_cap, day_cap, rem_risk * 0.92)
    if wounded:
        size *= 0.88
    if size <= 0.05 or ledger.would_breach(size):
        size = min(max(clear_sz * 0.7, brain * 0.5), rem_risk * 0.85)
        if size <= 0.05 or ledger.would_breach(size):
            return 0.0
    return float(max(size, 0.0))


def goal_conditioned_size(
    *,
    ledger: DailyRiskLedger,
    target_percent: float,
    stop_distance_pct: float,
    aggression: float,
    expect_r: float = 2.0,
) -> float:
    rem_goal = remaining_to_target(ledger, target_percent)
    rem_risk = ledger.remaining_risk_budget_percent()
    if rem_risk <= 0.05 or rem_goal <= 0:
        return 0.0
    ideal = rem_goal / max(expect_r, 0.5)
    base = size_position_risk_percent(
        max_daily_risk_percent=ledger.max_daily_risk_percent,
        remaining_budget_percent=rem_risk,
        stop_distance_pct=stop_distance_pct,
        target_percent=target_percent,
        aggression=aggression,
        max_single_fraction=0.95,
        friction_reserve_percent=0.04,
    )
    size = max(base, min(ideal, rem_risk * 0.95))
    if rem_goal < target_percent * 0.35:
        size = min(size, max(rem_goal / max(expect_r, 1.0), 0.08))
    return float(min(size, rem_risk * 0.95))


def sense_input_from_snap(snap, target: float, risk: float) -> MarketSenseInput:
    """Build MarketSenseInput from a SymbolEdgeSnapshot (shared by probe + state pack)."""
    forces = [e.force for e in snap.set_edges]
    while len(forces) < 8:
        forces.append(0.0)
    vels = [(e.ltf_rsi - 50.0) / 50.0 for e in snap.set_edges] or [0.0]
    while len(vels) < 4:
        vels.append(0.0)
    return MarketSenseInput(
        htf_force=forces[:8],
        ltf_velocity=vels[:4],
        inertia=[f * 0.85 for f in forces[:4]],
        inertia_baseline=[f * 0.4 for f in forces[:4]],
        velocity_baseline=[v * 0.3 for v in vels[:4]],
        full_body_outside_rails=abs(snap.consensus_force) >= 0.35,
        ltf_inside_tight=True,
        efficiency=0.55 if snap.n_pullback + snap.n_continuation > 0 else 0.3,
        regime=(
            "bull"
            if snap.multi_set_consensus == "agree_long"
            else "bear"
            if snap.multi_set_consensus == "agree_short"
            else "chop"
        ),
        g_fixed=True,
        target_percent=target,
        max_daily_risk_percent=risk,
        composition_has_force=any(abs(e.force) >= 0.15 for e in snap.set_edges),
        composition_has_velocity=any(e.topology != "chop" for e in snap.set_edges),
        cross_family_agree=snap.multi_set_consensus in ("agree_long", "agree_short"),
        set_conflict=snap.multi_set_consensus == "conflict",
    )


def _sense_l2l_once(snap, target: float, risk: float) -> Tuple[bool, bool, Tuple[str, ...]]:
    sensors = edge_sensors(snap)
    role_base = evaluate_understanding(sensors)
    renamed = evaluate_understanding(rename_sensors(sensors, prefix="HO_"))
    swapped = evaluate_understanding(swap_family(sensors, "rsi"))
    novel = evaluate_understanding(
        novel_composition(
            "macd",
            "stochastic",
            force_val=float(snap.consensus_force),
            velocity_val=float(sensors[1].value),
            inertia_val=float(sensors[2].value),
        )
    )
    l2l_ok = (
        role_base.topology == renamed.topology
        and role_base.act == renamed.act
        and role_base.topology == swapped.topology
        and novel.chain_ok
    )
    sense_inp = sense_input_from_snap(snap, target, risk)
    sense_rep = probe_all_senses(sense_inp)
    senses_ok = (
        "topology_class" in sense_rep.sight
        and "max_tension_load_building" in sense_rep.feel
        and "edge_quality" in sense_rep.taste
        and "wait_subtype" in sense_rep.hearing
    )
    roles = tuple(sorted({r.value for r in role_base.roles.values()})) or ("force", "velocity")
    return senses_ok, l2l_ok, roles


def run_goal_path_day(
    policy: FrozenMetaPolicy,
    *,
    date: str,
    m1_by_symbol: Dict[str, List[dict]],
    target_percent: float,
    max_daily_risk_percent: float,
    symbols: Sequence[str],
    slots: Sequence[str] = PRODUCTION_SCALPING_SLOTS,
    stop_distance_pct: float = DEFAULT_STOP_DISTANCE_PCT,
    equity: float = 100_000.0,
    friction: Optional[FrictionAssumptions] = None,
    tf_cache_by_symbol: Optional[Dict[str, Dict[str, List[dict]]]] = None,
    brain_drives: bool = True,
    watch_enabled: bool = True,
    collect_path_state_teachers: bool = False,
    max_path_state_teachers: int = 80,
    collect_mental_replay: bool = False,
    max_mental_replays: int = 80,
    aggressive_capture: bool = False,
    monty_htf_blend: bool = False,
    method_hold_while_force: bool = False,
    collect_thought_trace: bool = False,
) -> Tuple[List[LegFill], DailyRiskLedger, Dict[str, Any]]:
    """Multi-slot scalping path. Law A29: brain decides; sensors feed state.

    ``brain_drives=True`` (default, permanent): Mark HTF+LTF opportunities are
    candidates; hard gate soup is off. Brain chooses wait/fire/size. Only risk
    envelope remains hard. London/NY opportunities must be capturable (≥8).

    ``watch_enabled=True`` (default, A28/C-001): Opportunity Watch scans every
    decision slot — logs misses + curriculum labels; does **not** force trades.

    ``collect_path_state_teachers`` (CASE-0037 lab): when brain waits on a real
    candidate, dump packed ``build_meta_rl_state`` + edge teacher_act for offline
    train (anti F-025 synthetic-state rebuild). Never forces live trades.

    ``collect_mental_replay`` (lab): after each closed fill, build a 3-TF ×
    before/during/after Trade Mental Replay card (Policy self-observation).
    Also auto-on when ``collect_path_state_teachers`` so conversion teachers can
    use outcome tags. Offline only — no inference retrain (A14).

    ``aggressive_capture`` (shadow/lab): multi-symbol pick up to 3, no XAU rank
    monopoly, cont/FX boosted in quality — risk envelope still hard; no pad.

    ``monty_htf_blend`` (lab/shadow, default **False**): HTF force = Court slope
    blended with Monty CCI+BB / RSI+BB on both HTFs; packs slope_on/cci_on/rsi_on
    into doctrine[12:15] so the brain can learn wind source. Production champ
    stays slope-only until Court PROMOTE + retrain.

    ``method_hold_while_force`` (lab/shadow, default **False**): Aaron t4 —
    when multi-set Force agrees and brain fires with confidence, extend cont hold
    and raise size-R arm so winners are not scratched at +1R / 30m. Production
    path stays CASE-0028 defaults until Court PROMOTE.

    Default clock is PRODUCTION_SCALPING_SLOTS (CASE-0029 5m).
    """
    fr = friction or FrictionAssumptions()
    ledger = DailyRiskLedger(
        max_daily_risk_percent=max_daily_risk_percent,
        equity=equity,
        friction=fr,
    )
    fills: List[LegFill] = []
    path_state_teachers: List[Dict[str, Any]] = []
    mental_replays: List[Dict[str, Any]] = []
    # Path teachers imply mental replay so AFTER outcomes can label conversion
    want_mental = bool(collect_mental_replay or collect_path_state_teachers)
    meta: Dict[str, Any] = {
        "slots": list(slots),
        "n_slots_fired": 0,
        "n_method_hold_legs": 0,
        "method_hold_while_force": bool(method_hold_while_force),
        "locked_target": False,
        "path": "goal_conditioned_scalping_cadence_a30_ms_session",
        "a13_slots_capacity": len(slots),
        "cadence_interval_min": (
            PRODUCTION_CADENCE_INTERVAL_MIN
            if len(slots) >= len(PRODUCTION_SCALPING_SLOTS) - 1
            else (10 if len(slots) > 60 else (15 if len(slots) > 40 else 30))
        ),
        "prime_band_hours": [PRIME_BAND_HOUR_START, PRIME_BAND_HOUR_END],
        "multiset_force_densify": True,
        "cont_hold_min_minutes": CONT_HOLD_MIN_MINUTES,
        "multiset_session_align_ease": True,
        "brain_drives": bool(brain_drives),
        "watch_enabled": bool(watch_enabled),
        "aggressive_capture": bool(aggressive_capture),
        "monty_htf_blend": bool(monty_htf_blend),
        "law": "A29_brain_l2l",
    }
    slot_list = list(slots)
    n_pb = n_ct = 0
    senses_ok = True
    l2l_ok = True
    roles_all: List[str] = []
    probed = False
    # Observe-only thought trace (visual thought map) — never changes behavior
    trace: List[Dict[str, Any]] = []

    def _tr(event: str, **kw: Any) -> Dict[str, Any]:
        rec = {"event": event, **kw}
        if collect_thought_trace:
            trace.append(rec)
        return rec
    # C-001 / A28: always-on Opportunity Watch → path meta + curriculum labels
    watch_agent = OpportunityWatchAgent() if watch_enabled else None
    watch_slot_reports: List[Any] = []

    caches: Dict[str, Dict[str, List[dict]]] = {}
    for sym in symbols:
        if tf_cache_by_symbol and sym in tf_cache_by_symbol:
            caches[sym] = tf_cache_by_symbol[sym]
        elif m1_by_symbol.get(sym):
            caches[sym] = build_tf_cache(m1_by_symbol[sym])

    # CASE-0011 / A13: hard fill cap 400; risk envelope still limits size
    max_fills = max_fills_for_a13(target_percent)
    wounded = False

    for si, slot in enumerate(slot_list):
        if ledger.realized_pnl_percent >= target_percent - 1e-9:
            meta["locked_target"] = True
            _tr("day_end", slot=slot, reason="target_locked",
                pnl=float(ledger.realized_pnl_percent))
            break
        if ledger.remaining_risk_budget_percent() <= 0.08:
            _tr("day_end", slot=slot, reason="risk_budget_exhausted",
                pnl=float(ledger.realized_pnl_percent),
                remaining=float(ledger.remaining_risk_budget_percent()))
            break
        if len(fills) >= max_fills:
            _tr("day_end", slot=slot, reason="max_fills_cap", n_fills=len(fills))
            break

        # CASE-0012: hold end depends on topology (set per pick below); placeholder
        end_time_fill = next_slot_end_time(slot, slot_list)

        candidates: List[Tuple[float, str, Any, str]] = []
        slot_snaps: Dict[str, Any] = {}
        for sym in symbols:
            m1 = m1_by_symbol.get(sym, [])
            cache = caches.get(sym)
            if not m1 or cache is None:
                continue
            snap = scan_all_sets(
                [],
                symbol=sym,
                tf_cache=cache,
                asof_date=date,
                asof_time=slot,
                monty_htf_blend=bool(monty_htf_blend),
            )
            slot_snaps[sym] = snap
            n_pb += snap.n_pullback
            n_ct += snap.n_continuation
            if not probed:
                s_ok, l_ok, roles = _sense_l2l_once(
                    snap, target_percent, max_daily_risk_percent
                )
                senses_ok = s_ok
                l2l_ok = l_ok
                roles_all.extend(roles)
                probed = True

            best = snap.best
            topology = best.topology if best else "chop"
            if best is None or best.act not in ("long", "short") or not best.htf_agree:
                continue
            if topology in ("slingshot_load", "collapse", "chop"):
                continue
            # --- A29 brain_drives: sensors only; no hard-rule veto soup ---
            if brain_drives:
                multi_agree = snap.multi_set_consensus in ("agree_long", "agree_short")
                n_side = count_actionable_side_agree(snap, best.act)
                quality = abs(best.force) + (0.55 if topology == "pullback_resume" else 0.0)
                # Aggressive: continuation is first-class in L/NY (Watch residual)
                if aggressive_capture and topology == "continuation":
                    quality += 0.45
                quality += 0.15 * n_side
                if multi_agree:
                    quality += 0.35
                if is_prime_session_slot(slot):
                    quality += 0.40  # London/NY — no excuse band
                if aggressive_capture:
                    # Kill XAU monopoly; lift FX so EURUSD cont reaches the brain
                    if sym in ("EURUSD", "GBPUSD"):
                        quality += 0.35
                    # slight diversify: do not auto-prefer gold
                elif sym == "XAUUSD":
                    quality += 0.20
                candidates.append((quality, sym, snap, topology))
                continue
            # --- legacy hard-filter path (lab only; brain_drives=False) ---
            _eff = efficiency_proxy_from_edge(
                n_pullback=snap.n_pullback,
                n_continuation=snap.n_continuation,
                consensus_force=float(snap.consensus_force),
            )
            _rid = regime_from_edge_sensors(
                multi_set_consensus=snap.multi_set_consensus,
                consensus_force=float(snap.consensus_force),
                efficiency=_eff,
            )
            if day_path_regime_skip_new_risk(_rid):
                continue
            if snap.multi_set_consensus == "conflict":
                continue
            if snap.multi_set_consensus == "agree_long" and best.act != "long":
                continue
            if snap.multi_set_consensus == "agree_short" and best.act != "short":
                continue
            if wounded and topology != "pullback_resume":
                continue
            multi_agree = snap.multi_set_consensus in ("agree_long", "agree_short")
            fmin = real_edge_force_min(topology=topology, multi_set_agree=multi_agree)
            if not fills and topology == "continuation":
                if abs(best.force) < first_entry_cont_force_min(multi_set_agree=multi_agree):
                    continue
            if abs(float(best.force)) < float(fmin):
                continue
            if not entry_quality_ok(
                slot=slot,
                topology=topology,
                n_fills=len(fills),
                force=float(best.force),
                multi_set_agree=multi_agree,
            ):
                continue
            if not path_side_permission_ok(snap):
                continue
            n_side = count_actionable_side_agree(snap, best.act)
            side_i = 1 if best.act == "long" else -1
            if not session_confirms_side(
                m1,
                date=date,
                asof_time=slot,
                side=side_i,
                min_align=session_min_align_for_path(multi_set_agree=multi_agree),
            ):
                continue
            quality = abs(best.force) + (0.55 if topology == "pullback_resume" else 0.0)
            quality += 0.15 * n_side
            if snap.multi_set_consensus in ("agree_long", "agree_short"):
                quality += 0.35
            if sym == "XAUUSD":
                quality += 0.30
            if is_prime_session_slot(slot):
                quality += 0.25
            candidates.append((quality, sym, snap, topology))

        # Symbol → act for fires completed this slot (Watch compares vs opportunities)
        fired_this_slot: Dict[str, str] = {}

        if collect_thought_trace and slot_snaps:
            qual_by_sym = {c[1]: float(c[0]) for c in candidates}
            per_sym = []
            for _sym, _snap in slot_snaps.items():
                _b = _snap.best
                _topo = _b.topology if _b else "chop"
                if _b is None or _b.act not in ("long", "short"):
                    _why = "no_edge_side"
                elif not _b.htf_agree:
                    _why = "htf_disagree"
                elif _topo in ("slingshot_load", "collapse", "chop"):
                    _why = f"topology_{_topo}"
                else:
                    _why = "candidate"
                per_sym.append(
                    {
                        "symbol": _sym,
                        "consensus": str(_snap.multi_set_consensus),
                        "force": round(float(_snap.consensus_force or 0.0), 3),
                        "edge_act": str(_b.act) if _b else "none",
                        "edge_force": round(float(getattr(_b, "force", 0.0) or 0.0), 3),
                        "topology": str(_topo),
                        "status": _why,
                        "quality": round(qual_by_sym.get(_sym, 0.0), 2),
                        "n_pullback": int(_snap.n_pullback),
                        "n_continuation": int(_snap.n_continuation),
                    }
                )
            _tr(
                "scan",
                slot=slot,
                prime=bool(is_prime_session_slot(slot)),
                symbols=per_sym,
                n_candidates=len(candidates),
                pnl=round(float(ledger.realized_pnl_percent), 3),
                remaining=round(float(ledger.remaining_risk_budget_percent()), 3),
            )

        if not candidates:
            # Mark: empty slot skip — no pad trades (allows_empty_slot_skip)
            # C-001: still Watch — bot waited while sensors may have seen PB/cont
            if watch_agent is not None and slot_snaps:
                slot_reps = []
                for sym, snap in slot_snaps.items():
                    slot_reps.append(
                        watch_agent.scan_snapshot(
                            snap,
                            asof_date=date,
                            asof_time=slot,
                            bot_act="wait",
                            bot_fired=False,
                            bot_symbol=None,
                        )
                    )
                _rep = watch_agent.merge_reports(slot_reps)
                watch_slot_reports.append(_rep)
                if collect_thought_trace:
                    for _c in getattr(_rep, "complaints", None) or []:
                        _tr(
                            "watch_miss",
                            slot=slot,
                            symbol=str(getattr(_c, "symbol", "") or ""),
                            side=str(getattr(_c, "side", "") or ""),
                            topology=str(getattr(_c, "topology", "") or ""),
                            session_band=str(getattr(_c, "session_band", "") or ""),
                        )
            continue
        candidates.sort(key=lambda x: -x[0])
        # CASE-0030: dual-sym only when multi-set agrees (best candidate sets tone)
        top_consensus = str(candidates[0][2].multi_set_consensus)
        if top_consensus == "agree_long":
            side_pool = [
                c
                for c in candidates
                if c[2].best is not None and c[2].best.act == "long"
            ]
            if side_pool:
                candidates = side_pool
        elif top_consensus == "agree_short":
            side_pool = [
                c
                for c in candidates
                if c[2].best is not None and c[2].best.act == "short"
            ]
            if side_pool:
                candidates = side_pool
        n_take = min(
            len(candidates),
            production_symbols_per_slot(
                multi_set_consensus=top_consensus,
                aggressive_capture=bool(aggressive_capture),
            ),
        )
        # Aggressive diversity: guarantee FX symbols in pick when present (Watch residual)
        if aggressive_capture and len(candidates) > n_take:
            picked_list = list(candidates[:n_take])
            have = {c[1] for c in picked_list}
            for c in candidates[n_take:]:
                if len(picked_list) >= max(n_take, 3):
                    break
                if c[1] not in have and c[1] in ("EURUSD", "GBPUSD"):
                    # swap weakest gold if needed to free a slot for FX
                    if len(picked_list) >= n_take:
                        for j in range(len(picked_list) - 1, -1, -1):
                            if picked_list[j][1] == "XAUUSD":
                                picked_list[j] = c
                                have = {x[1] for x in picked_list}
                                break
                        else:
                            picked_list.append(c)
                    else:
                        picked_list.append(c)
                        have.add(c[1])
            picked = picked_list[: max(n_take, min(3, len(candidates)))]
        else:
            picked = candidates[:n_take]

        for quality, sym, snap, topology in picked:
            if ledger.realized_pnl_percent >= target_percent - 1e-9:
                meta["locked_target"] = True
                break
            if ledger.remaining_risk_budget_percent() <= 0.08:
                break
            if len(fills) >= max_fills:
                break
            best = snap.best
            assert best is not None
            m1 = m1_by_symbol[sym]
            # CASE-0012/0028: pullback → EOD; cont → min hold path (default 30m)
            # Method hold applied after brain forward (needs conf) — placeholder first
            end_time_fill = fill_hold_end_time(topology, slot, slot_list)
            pol_topo = "launch" if topology == "pullback_resume" else "release"

            official = edge_to_set_confluence(snap)
            progress = max(ledger.realized_pnl_percent, 0.0) / max(target_percent, 1e-6)
            # CASE-0018: pack A17 regime into doctrine so frozen policy sees it
            eff_p = efficiency_proxy_from_edge(
                n_pullback=snap.n_pullback,
                n_continuation=snap.n_continuation,
                consensus_force=float(snap.consensus_force),
            )
            rid = regime_from_edge_sensors(
                multi_set_consensus=snap.multi_set_consensus,
                consensus_force=float(snap.consensus_force),
                efficiency=eff_p,
            )
            doctrine = encode_regime_doctrine(
                rid,
                force=float(snap.consensus_force),
                efficiency=eff_p,
                slope_on=float(getattr(snap, "slope_on", 0.0) or 0.0),
                cci_on=float(getattr(snap, "cci_on", 0.0) or 0.0),
                rsi_on=float(getattr(snap, "rsi_on", 0.0) or 0.0),
            )
            # L2L Proposal 1: pack living senses into state (not probe-only)
            sense_inp = sense_input_from_snap(
                snap,
                float(target_percent),
                float(max_daily_risk_percent),
            )
            sense_inp.progress_to_target = float(np.clip(progress, 0, 1.5))
            sense_inp.realized_risk_percent = max(-ledger.realized_pnl_percent, 0.0)
            sense_rep = probe_all_senses(sense_inp)
            state = build_meta_rl_state(
                target_percent=target_percent,
                max_daily_risk_percent=max_daily_risk_percent,
                official=official,
                doctrine_vec=doctrine,
                structure=StructureFlags(
                    pullback=topology == "pullback_resume",
                    scale_conflict=False,
                ),
                sense_report=sense_rep,
                progress_to_target=float(np.clip(progress, 0, 1.5)),
                realized_risk_percent=max(-ledger.realized_pnl_percent, 0.0),
                session_phase=float(si / max(len(slot_list) - 1, 1)),
            )
            meta["last_regime"] = rid.value
            meta["regime_channel"] = "a17_doctrine"
            meta["senses_packed"] = True
            meta["sense_pack"] = [float(x) for x in encode_sense_report(sense_rep)]
            meta["htf_source"] = {
                "slope_on": float(getattr(snap, "slope_on", 0.0) or 0.0),
                "cci_on": float(getattr(snap, "cci_on", 0.0) or 0.0),
                "rsi_on": float(getattr(snap, "rsi_on", 0.0) or 0.0),
                "monty_htf_blend": bool(monty_htf_blend),
            }
            roles = tuple(roles_all) or ("force", "velocity")
            action: PolicyAction = policy.forward(
                state, ledger=ledger, topology=pol_topo, roles=roles
            )
            dec: Dict[str, Any] = {}
            if collect_thought_trace:
                _act_p, _size_logit, _probs = policy.brain.predict_act(state)
                dec = {
                    # exact packed state the brain saw — makes human corrections
                    # directly trainable (anti F-025: never rebuild fake states)
                    "state": [round(float(x), 4) for x in np.asarray(state).ravel()],
                    "slot": slot,
                    "symbol": sym,
                    "prime": bool(is_prime_session_slot(slot)),
                    "quality": round(float(quality), 2),
                    "topology": str(topology),
                    "edge": {
                        "act": str(best.act),
                        "force": round(float(best.force), 3),
                        "set_id": int(getattr(best, "set_id", 0) or 0),
                        "consensus": str(snap.multi_set_consensus),
                        "n_htf_active": sum(
                            1 for e in (snap.set_edges or [])
                            if bool(getattr(e, "htf_agree", False))
                        ),
                    },
                    "senses": {
                        "sight": str(sense_rep.sight.get("topology_class", "")),
                        "feel": str(sense_rep.feel.get("max_tension_load_building", "")),
                        "taste": str(sense_rep.taste.get("edge_quality", "")),
                        "hearing": str(sense_rep.hearing.get("wait_subtype", "")),
                    },
                    "ctx": {
                        "target": float(target_percent),
                        "risk": float(max_daily_risk_percent),
                        "progress": round(float(progress), 3),
                        "pnl": round(float(ledger.realized_pnl_percent), 3),
                        "remaining": round(
                            float(ledger.remaining_risk_budget_percent()), 3
                        ),
                        "session_phase": round(float(si / max(len(slot_list) - 1, 1)), 3),
                        "wounded": bool(wounded),
                        "n_fills": len(fills),
                    },
                    "brain": {
                        "act": str(action.act),
                        "probs": {
                            "wait": round(float(_probs[0]), 3),
                            "long": round(float(_probs[1]), 3),
                            "short": round(float(_probs[2]), 3),
                        },
                        "size_sig": round(
                            float(1.0 / (1.0 + np.exp(-_size_logit))), 3
                        ),
                        "size_risk_percent": round(float(action.size_risk_percent), 3),
                        "reason": str(action.reason),
                        "wait_subtype": str(action.wait_subtype or ""),
                    },
                }
            # Brain path: one forward only — no hard nudge oracle (A29)
            if not brain_drives and action.act == "wait":
                st2 = state.copy()
                sign = 1.0 if best.act == "long" else -1.0
                for idx in (0, 3, 6, 9):
                    if idx < st2.size:
                        st2[idx] = sign * 0.95
                action = policy.forward(st2, ledger=ledger, topology="launch", roles=roles)
            # HTF-active curriculum: pack every visited state where ≥1 set has HTF agree
            # and Mark has long/short — not only waits (dense champs rarely wait).
            n_htf_active = sum(
                1 for e in (snap.set_edges or []) if bool(getattr(e, "htf_agree", False))
            )
            if (
                collect_path_state_teachers
                and brain_drives
                and best.act in ("long", "short")
                and bool(getattr(best, "htf_agree", False))
                and n_htf_active >= 1
                and len(path_state_teachers) < int(max_path_state_teachers)
            ):
                band = session_band(slot)
                t_norm = (float(target_percent) - 5.0) / 85.0
                size_frac = float(
                    np.clip(
                        0.5
                        + 0.35 * t_norm
                        + (0.12 if band == "london_ny" else 0.0),
                        0.25,
                        0.95,
                    )
                )
                w = 1.0 + 0.25 * float(n_htf_active)
                if band == "london_ny":
                    w += 0.5
                bot = str(action.act or "wait")
                if bot not in ("long", "short"):
                    src = "path_state_miss"
                elif bot == str(best.act):
                    src = "path_state_htf_active"
                else:
                    src = "path_state_side_miss"
                path_state_teachers.append(
                    {
                        "state": [float(x) for x in np.asarray(state, dtype=np.float64).ravel()],
                        "teacher_act": str(best.act),
                        "teacher_size_frac": size_frac,
                        "topology": str(topology),
                        "session_band": band,
                        "weight": float(w),
                        "symbol": str(sym),
                        "asof_date": str(date),
                        "asof_time": str(slot),
                        "force": float(best.force),
                        "what_bot_did": bot,
                        "source": src,
                        "multi_set_consensus": str(snap.multi_set_consensus),
                        "n_htf_active": int(n_htf_active),
                        "htf_active": True,
                        "slope_on": float(getattr(snap, "slope_on", 0.0) or 0.0),
                        "cci_on": float(getattr(snap, "cci_on", 0.0) or 0.0),
                        "rsi_on": float(getattr(snap, "rsi_on", 0.0) or 0.0),
                    }
                )
            if action.act not in ("long", "short"):
                if collect_thought_trace:
                    dec["event"] = "brain_wait"
                    dec["outcome"] = f"edge wanted {best.act}, brain waited"
                    trace.append(dec)
                continue
            # Align with edge side when brain fires opposite (sensor truth)
            if brain_drives and action.act != best.act:
                # Allow brain side if multi-set not conflict; else take edge side
                if snap.multi_set_consensus == "conflict":
                    if collect_thought_trace:
                        dec["event"] = "blocked_conflict"
                        dec["outcome"] = (
                            f"brain {action.act} vs edge {best.act} under conflict"
                        )
                        trace.append(dec)
                    continue
                if snap.multi_set_consensus == "agree_long":
                    action = PolicyAction(
                        act="long",
                        size_risk_percent=action.size_risk_percent,
                        reason=action.reason + "|edge_align_long",
                        topology=topology,
                        roles_cited=roles,
                    )
                elif snap.multi_set_consensus == "agree_short":
                    action = PolicyAction(
                        act="short",
                        size_risk_percent=action.size_risk_percent,
                        reason=action.reason + "|edge_align_short",
                        topology=topology,
                        roles_cited=roles,
                    )
                else:
                    action = PolicyAction(
                        act=best.act,
                        size_risk_percent=action.size_risk_percent,
                        reason=action.reason + "|edge_side",
                        topology=topology,
                        roles_cited=roles,
                    )

            rem_goal = remaining_to_target(ledger, target_percent)
            # Edge quality from snapshot consensus / force (for intelligent size-up)
            _eq = 0.5
            if snap.multi_set_consensus in ("agree_long", "agree_short"):
                _eq = 0.85 + 0.15 * min(abs(float(snap.consensus_force or 0.0)), 1.0)
            elif abs(float(getattr(best, "force", 0.0) or 0.0)) >= 0.35:
                _eq = 0.7
            if (
                brain_drives
                and getattr(policy, "size_head_drives", False)
                and action.size_risk_percent > 0.05
            ):
                # Dynamic-size lab: the policy's trained size head passes its
                # own size to the fill — no intelligent-size blend override.
                # Envelope still hard-gates below (would_breach / lot legal).
                size = float(action.size_risk_percent)
                _size_src = "size_head_passthrough"
            elif brain_drives and INTELLIGENT_SIZE_UP:
                # Monty EO: max(brain, clear-path, intelligent aggressor) under envelope
                _conf = 0.55
                if "conf=" in str(action.reason or ""):
                    try:
                        _conf = float(str(action.reason).split("conf=")[1].split()[0])
                    except (IndexError, ValueError):
                        _conf = 0.55
                size = intelligent_size_toward_clear(
                    ledger=ledger,
                    target_percent=target_percent,
                    topology=topology,
                    brain_size=float(action.size_risk_percent or 0.0),
                    wounded=wounded,
                    edge_quality=float(_eq),
                    conf=float(_conf),
                )
                size = float(size) * production_leg_size_scale(len(fills))
                _size_src = "intelligent_size_up_blend"
            elif brain_drives and action.size_risk_percent > 0.05:
                size = float(action.size_risk_percent)
                _size_src = "brain_direct"
            else:
                size = goal_path_size_for_clear(
                    ledger=ledger,
                    target_percent=target_percent,
                    topology=topology,
                    wounded=wounded,
                )
                size = float(size) * production_leg_size_scale(len(fills))
                _size_src = "clear_path_heuristic"
            if size <= 0.05 or ledger.would_breach(size):
                if collect_thought_trace:
                    dec["event"] = "blocked_envelope"
                    dec["size"] = {
                        "attempted": round(float(size), 3),
                        "source": _size_src,
                        "would_breach": bool(ledger.would_breach(size)),
                    }
                    dec["outcome"] = "size zero or would breach envelope"
                    trace.append(dec)
                continue
            meta["path_geometry"] = (
                "a29_brain_drives" if brain_drives else "a21_one_sym_full_scale"
            )

            # Aaron method for SCALPER (lab): Force agree → re-commit same side at
            # **scalp** window only (never 30–120m). "Hold" = thesis continuity across
            # short legs + progressive size, not long bag-holding.
            size_r_arm = 1.0
            method_hold_leg = False
            if method_hold_while_force and brain_drives:
                _conf_h = 0.55
                if "conf=" in str(action.reason or ""):
                    try:
                        _conf_h = float(str(action.reason).split("conf=")[1].split()[0])
                    except (IndexError, ValueError):
                        _conf_h = 0.55
                force_live = snap.multi_set_consensus in ("agree_long", "agree_short")
                same_side = (
                    (snap.multi_set_consensus == "agree_long" and action.act == "long")
                    or (snap.multi_set_consensus == "agree_short" and action.act == "short")
                    or (force_live and action.act in ("long", "short"))
                )
                if force_live and same_side and _conf_h >= 0.55:
                    method_hold_leg = True
                    # Explicit scalp window only (METHOD_HOLD_CONT == CONT_HOLD = 10m)
                    end_time_fill = fill_hold_end_time(
                        topology,
                        slot,
                        slot_list,
                        cont_hold_min_minutes=METHOD_HOLD_CONT_MINUTES,
                        pb_hold_min_minutes=PB_HOLD_MIN_MINUTES,
                    )
                    size_r_arm = float(METHOD_HOLD_SIZE_R_ARM)
                    meta["method_hold_while_force"] = True
                    meta["path_geometry"] = "a29_brain_scalp_method"

            window = m1_window(m1, date=date, start_time=slot, end_time=end_time_fill)
            if len(window) < 5:
                if collect_thought_trace:
                    dec["event"] = "blocked_window"
                    dec["outcome"] = "not enough M1 bars in fill window"
                    trace.append(dec)
                continue
            entry = float(window[0]["open"])
            stop_px = stop_distance_price_from_pct(entry, stop_distance_pct)
            lot_info = risk_legal_max_lot(
                equity=equity,
                risk_percent=size,
                entry_price=entry,
                stop_distance_price=stop_px,
                symbol=sym,
                leverage=LEVERAGE,
            )
            size = min(size, float(lot_info["risk_percent_actual"]) or size)
            if size <= 0 or lot_info["lot"] <= 0:
                if collect_thought_trace:
                    dec["event"] = "blocked_lot"
                    dec["outcome"] = "risk-legal lot rounds to zero"
                    trace.append(dec)
                continue

            side = 1 if best.act == "long" else -1
            action_act = best.act
            ledger.positions.append(
                OpenPosition(
                    symbol=sym,
                    side=side,
                    risk_percent=size,
                    notional_pct=size / max(stop_distance_pct, 1e-6) * 100.0,
                )
            )
            # CASE-0008: size-R floor @1.0R default; method hold raises arm (lab)
            # secondary 50% rem_goal; no full BE (F-011)
            pnl = simulate_fill_m1_path(
                side=side,
                bars=window,
                size_risk_percent=size,
                stop_distance_pct=stop_distance_pct,
                friction_pct=fr.total_pct,
                trail=False,
                goal_lock_pnl_percent=rem_goal if rem_goal > 0 else None,
                partial_lock_frac=0.5,
                size_r_arm_r=float(size_r_arm),
            )
            if method_hold_leg:
                meta["n_method_hold_legs"] = int(meta.get("n_method_hold_legs") or 0) + 1
            apply_trade_result(ledger, pnl_percent=pnl, closed_risk_percent=size)
            ledger.positions.clear()
            fills.append(
                LegFill(
                    symbol=sym,
                    slot=slot,
                    act=action_act,
                    size_risk_percent=size,
                    pnl_percent=pnl,
                    topology=topology,
                    edge_kind=topology,
                    lot=float(lot_info["lot"]),
                )
            )
            fired_this_slot[sym] = action_act
            meta["n_slots_fired"] += 1
            if collect_thought_trace:
                dec["event"] = "fired"
                _ov = ""
                if "|edge_align" in str(action.reason):
                    _ov = "edge_align_" + str(action.reason).rsplit("edge_align_", 1)[-1][:5]
                elif "|edge_side" in str(action.reason):
                    _ov = "edge_side"
                dec["override"] = _ov
                dec["size"] = {
                    "final": round(float(size), 3),
                    "source": _size_src,
                    "brain_asked": round(float(action.size_risk_percent), 3),
                    "frac_of_remaining_before": round(
                        float(size)
                        / max(float(size) + ledger.remaining_risk_budget_percent(), 1e-6),
                        3,
                    ),
                    "lot": round(float(lot_info["lot"]), 3),
                }
                dec["fill"] = {
                    "act": str(action_act),
                    "pnl": round(float(pnl), 3),
                    "window_end": str(end_time_fill),
                    "method_hold": bool(method_hold_leg),
                    "pnl_after": round(float(ledger.realized_pnl_percent), 3),
                    "remaining_after": round(
                        float(ledger.remaining_risk_budget_percent()), 3
                    ),
                }
                dec["outcome"] = (
                    f"{action_act} {size:.2f}% -> pnl {pnl:+.2f}% "
                    f"(day {ledger.realized_pnl_percent:+.2f}%)"
                )
                trace.append(dec)
            # --- Trade Mental Replay: 3 TF × before/during/after (Policy mind) ---
            if want_mental and len(mental_replays) < int(max_mental_replays):
                try:
                    cache = (tf_cache_by_symbol or {}).get(sym)
                    if cache is None:
                        cache = build_tf_cache(m1)
                    mid_t = tmr_mid_time(slot, end_time_fill)
                    during_snap = scan_all_sets(
                        m1,
                        sym,
                        tf_cache=cache,
                        asof_date=date,
                        asof_time=mid_t,
                        monty_htf_blend=bool(monty_htf_blend),
                    )
                    after_snap = scan_all_sets(
                        m1,
                        sym,
                        tf_cache=cache,
                        asof_date=date,
                        asof_time=end_time_fill,
                        monty_htf_blend=bool(monty_htf_blend),
                    )
                    # ledger already includes this fill's pnl
                    pre_realized = float(ledger.realized_pnl_percent) - float(pnl)
                    progress_after = max(ledger.realized_pnl_percent, 0.0) / max(
                        target_percent, 1e-6
                    )
                    risk_after = max(-ledger.realized_pnl_percent, 0.0)
                    risk_before = max(-pre_realized, 0.0)
                    sense_during = probe_all_senses(
                        sense_input_from_snap(
                            during_snap,
                            float(target_percent),
                            float(max_daily_risk_percent),
                        )
                    )
                    sense_after = probe_all_senses(
                        sense_input_from_snap(
                            after_snap,
                            float(target_percent),
                            float(max_daily_risk_percent),
                        )
                    )
                    n_htf_here = sum(
                        1
                        for e in (snap.set_edges or [])
                        if bool(getattr(e, "htf_agree", False))
                    )
                    card = build_trade_mental_replay(
                        trade_index=len(fills),
                        symbol=sym,
                        date=date,
                        side=str(action_act),
                        size_risk_percent=float(size),
                        entry_slot=str(slot),
                        exit_time=str(end_time_fill),
                        topology=str(topology),
                        set_id=int(getattr(best, "set_id", 0) or 0),
                        pnl_percent=float(pnl),
                        before_snap=snap,
                        during_snap=during_snap,
                        after_snap=after_snap,
                        brain_act=str(action_act),
                        sense_rep_before=sense_rep,
                        sense_rep_during=sense_during,
                        sense_rep_after=sense_after,
                        progress_before=float(np.clip(progress, 0, 1.5)),
                        progress_after=float(np.clip(progress_after, 0, 1.5)),
                        risk_before=float(risk_before),
                        risk_after=float(risk_after),
                        packed_state_before=state,
                        lot=float(lot_info["lot"]),
                        n_htf_active=int(n_htf_here),
                    )
                    # Compact journal in meta (full state only inside teacher export)
                    mental_replays.append(card.to_dict(include_state=False))
                    if collect_path_state_teachers:
                        for trow in teachers_from_mental_replay(card):
                            if len(path_state_teachers) >= int(max_path_state_teachers):
                                break
                            path_state_teachers.append(trow)
                except Exception as _tmr_exc:  # never break the day path
                    meta["mental_replay_last_error"] = str(_tmr_exc)[:200]
            if pnl < 0:
                wounded = True
            if ledger.realized_pnl_percent >= target_percent - 1e-9:
                meta["locked_target"] = True
                break

        # C-001: Watch every decision clock (fires + waits on remaining symbols)
        if watch_agent is not None and slot_snaps:
            slot_reps = []
            for sym, snap in slot_snaps.items():
                act = fired_this_slot.get(sym)
                slot_reps.append(
                    watch_agent.scan_snapshot(
                        snap,
                        asof_date=date,
                        asof_time=slot,
                        bot_act=act if act else "wait",
                        bot_fired=act is not None,
                        bot_symbol=sym if act is not None else None,
                    )
                )
            _rep_eos = watch_agent.merge_reports(slot_reps)
            watch_slot_reports.append(_rep_eos)
            if collect_thought_trace:
                for _c in getattr(_rep_eos, "complaints", None) or []:
                    _tr(
                        "watch_miss",
                        slot=slot,
                        symbol=str(getattr(_c, "symbol", "") or ""),
                        side=str(getattr(_c, "side", "") or ""),
                        topology=str(getattr(_c, "topology", "") or ""),
                        session_band=str(getattr(_c, "session_band", "") or ""),
                    )
            # Residual harvest: pack *real* path state at Watch miss (anti F-025 rebuild)
            # HTF-active gate: ≥1 official set htf_agree (same as brain-wait teachers)
            if collect_path_state_teachers:
                progress = max(ledger.realized_pnl_percent, 0.0) / max(target_percent, 1e-6)
                realized_risk = max(-ledger.realized_pnl_percent, 0.0)
                sess = float(si / max(len(slot_list) - 1, 1))
                for rep in slot_reps:
                    for c in getattr(rep, "complaints", None) or []:
                        if len(path_state_teachers) >= int(max_path_state_teachers):
                            break
                        side = str(getattr(c, "side", "") or "")
                        topo = str(getattr(c, "topology", "") or "")
                        if side not in ("long", "short"):
                            continue
                        if topo not in ("pullback_resume", "continuation"):
                            continue
                        csym = str(getattr(c, "symbol", "") or "")
                        snap = slot_snaps.get(csym)
                        if snap is None:
                            continue
                        n_htf_active = sum(
                            1
                            for e in (snap.set_edges or [])
                            if bool(getattr(e, "htf_agree", False))
                        )
                        if n_htf_active < 1:
                            continue
                        official = edge_to_set_confluence(snap)
                        eff_p = efficiency_proxy_from_edge(
                            n_pullback=snap.n_pullback,
                            n_continuation=snap.n_continuation,
                            consensus_force=float(snap.consensus_force),
                        )
                        rid = regime_from_edge_sensors(
                            multi_set_consensus=snap.multi_set_consensus,
                            consensus_force=float(snap.consensus_force),
                            efficiency=eff_p,
                        )
                        doctrine = encode_regime_doctrine(
                            rid,
                            force=float(snap.consensus_force),
                            efficiency=eff_p,
                            slope_on=float(getattr(snap, "slope_on", 0.0) or 0.0),
                            cci_on=float(getattr(snap, "cci_on", 0.0) or 0.0),
                            rsi_on=float(getattr(snap, "rsi_on", 0.0) or 0.0),
                        )
                        si = sense_input_from_snap(
                            snap, float(target_percent), float(max_daily_risk_percent)
                        )
                        si.progress_to_target = float(np.clip(progress, 0, 1.5))
                        si.realized_risk_percent = float(realized_risk)
                        srep = probe_all_senses(si)
                        st = build_meta_rl_state(
                            target_percent=target_percent,
                            max_daily_risk_percent=max_daily_risk_percent,
                            official=official,
                            doctrine_vec=doctrine,
                            structure=StructureFlags(
                                pullback=topo == "pullback_resume",
                                scale_conflict=False,
                            ),
                            sense_report=srep,
                            progress_to_target=float(np.clip(progress, 0, 1.5)),
                            realized_risk_percent=realized_risk,
                            session_phase=sess,
                        )
                        band = session_band(slot)
                        t_norm = (float(target_percent) - 5.0) / 85.0
                        size_frac = float(
                            np.clip(
                                0.5
                                + 0.35 * t_norm
                                + (0.12 if band == "london_ny" else 0.0),
                                0.25,
                                0.95,
                            )
                        )
                        w = 1.0 + 0.25 * float(n_htf_active)
                        if band == "london_ny":
                            w += 0.5
                        path_state_teachers.append(
                            {
                                "state": [
                                    float(x)
                                    for x in np.asarray(st, dtype=np.float64).ravel()
                                ],
                                "teacher_act": side,
                                "teacher_size_frac": size_frac,
                                "topology": topo,
                                "session_band": band,
                                "weight": float(w),
                                "symbol": csym,
                                "asof_date": str(date),
                                "asof_time": str(slot),
                                "force": float(getattr(c, "force", 0.0) or 0.0),
                                "what_bot_did": str(getattr(c, "what_bot_did", "wait") or "wait"),
                                "source": "path_state_watch_miss",
                                "multi_set_consensus": str(snap.multi_set_consensus),
                                "set_id": int(getattr(c, "set_id", 0) or 0),
                                "n_htf_active": int(n_htf_active),
                                "htf_active": True,
                                "slope_on": float(getattr(snap, "slope_on", 0.0) or 0.0),
                                "cci_on": float(getattr(snap, "cci_on", 0.0) or 0.0),
                                "rsi_on": float(getattr(snap, "rsi_on", 0.0) or 0.0),
                            }
                        )

        if meta.get("locked_target"):
            break

    meta["n_pullback"] = n_pb
    meta["n_continuation"] = n_ct
    meta["senses_ok"] = senses_ok if probed else False
    meta["l2l_ok"] = l2l_ok if probed else False
    meta["n_fills"] = len(fills)
    meta["n_trades"] = len(fills)
    meta["a13_ok"] = a13_trade_count_ok(len(fills))
    meta["max_fills"] = max_fills
    meta["roles"] = tuple(sorted(set(roles_all))) or ("force", "velocity")
    # C-001 closed loop: Watch aggregates → meta for forward/curriculum
    if watch_agent is not None:
        merged = watch_agent.merge_reports(watch_slot_reports)
        meta["watch"] = watch_day_summary(merged)
        meta["watch_n_misses"] = int(merged.n_misses)
        meta["watch_n_london_ny_misses"] = int(merged.n_london_ny_misses)
        meta["watch_n_hits"] = int(merged.n_hits)
        meta["watch_n_opportunities"] = int(merged.n_opportunities)
        # Cap label payload for path speed/memory; counts stay full in watch summary
        all_labs = curriculum_labels_from_report(merged)
        meta["curriculum_labels_total"] = len(all_labs)
        meta["curriculum_labels"] = all_labs[:200]
    else:
        meta["watch"] = {"always_on": False, "n_misses": 0, "n_curriculum_labels": 0}
        meta["curriculum_labels"] = []
        meta["curriculum_labels_total"] = 0
    meta["path_state_teachers"] = path_state_teachers
    meta["n_path_state_teachers"] = len(path_state_teachers)
    meta["collect_path_state_teachers"] = bool(collect_path_state_teachers)
    meta["mental_replays"] = mental_replays
    meta["n_mental_replays"] = len(mental_replays)
    meta["collect_mental_replay"] = bool(want_mental)
    meta["mental_replay_grid"] = "3tf_x_3phase"
    if collect_thought_trace:
        meta["thought_trace"] = trace
    return fills, ledger, meta
