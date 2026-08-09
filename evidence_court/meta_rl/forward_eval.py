"""100-forward-day multi-TF multi-symbol evaluation (sim/shadow).

Fill timing (no look-ahead)
---------------------------
- **Decision time:** day open. Features/indicators use only *completed* prior days
  (M1 history with date < today). Current-day high/low/close are NOT decision inputs.
- **Fill path:** enter at open after decision; exit at close or stop if adverse
  excursion from open reaches stop distance first.
- **Multi-TF edge:** official Mark sets; HTF force + LTF RSI(5)+BB(10,0.5,shift+2)
  for pullback resume / continuation (CASE-0002 / Possible edge not tested).
- **Multi-symbol:** concurrent book with aggregated daily risk; 1:100 leverage
  risk-legal sizing (flea-jar full action space).
- Label: ``forward_sim_shadow`` — not live MT5.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .edge import build_tf_cache, edge_sensors, edge_to_set_confluence, scan_all_sets
from .goal_path import run_goal_path_day
from .leverage import LEVERAGE, risk_legal_max_lot, stop_distance_price_from_pct
from .policy import FrozenMetaPolicy, load_or_train_champion
from .price_io import (
    SYMBOL_FILES,
    available_symbols,
    bars_to_daily,
    load_m1_bars,
    load_m1_trailing_calendar_days,
)
from .risk import DailyRiskLedger, FrictionAssumptions, OpenPosition, apply_trade_result
from .roles import evaluate_understanding, novel_composition, rename_sensors, swap_family
from .senses import MarketSenseInput, probe_all_senses
from .state import build_meta_rl_state
from .types import StructureFlags

DEFAULT_PRICE = SYMBOL_FILES.get("XAUUSD", Path("."))
FALLBACK_PRICE = DEFAULT_PRICE

DEFAULT_TARGET_GRID = (5.0, 15.0, 30.0, 50.0, 70.0, 90.0)
DEFAULT_RISK_GRID = (1.0, 2.0, 3.0)
DEFAULT_SYMBOLS = ("XAUUSD", "EURUSD", "GBPUSD")
DEFAULT_STOP_DISTANCE_PCT = 0.35


@dataclass
class SymbolDayTrade:
    symbol: str
    act: str
    size_risk_percent: float
    pnl_percent: float
    topology: str
    set_id: int
    edge_kind: str  # pullback_resume | continuation | wait | ...
    lot: float
    leverage: float


@dataclass
class DayResult:
    day: str
    target_percent: float
    max_daily_risk_percent: float
    pnl_percent: float
    worst_case_loss_percent: float
    breach: bool
    n_trades: int
    retrain_steps: int
    topology: str
    act_summary: str
    hit_target: bool = False
    goal_progress: float = 0.0
    wait_subtype: str = ""
    roles: Tuple[str, ...] = ()
    decision_dir: float = 0.0
    fill_model: str = "open_decision_close_or_stop"
    senses_ok: bool = False
    l2l_ok: bool = False
    n_pullback: int = 0
    n_continuation: int = 0
    symbols_traded: Tuple[str, ...] = ()
    symbol_trades: Tuple[Dict[str, Any], ...] = ()
    leverage: float = LEVERAGE


@dataclass
class ForwardEvalReport:
    n_days: int
    breach_count: int
    pair_results: Dict[str, Dict[str, Any]]
    day_results: List[DayResult] = field(default_factory=list)
    no_retrain: bool = True
    l2l_day_path_ok: bool = False
    senses_day_path_ok: bool = False
    goal_consistency_ok: bool = False
    l2l_unit_ok: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def l2l_novel_ok(self) -> bool:
        return self.l2l_day_path_ok

    @property
    def promote_ready(self) -> bool:
        """Final-boss gate: 100d, breach 0, no retrain, L2L/senses, consistent hits."""
        gc = self.metadata.get("goal_consistency") or {}
        low_hr = float(gc.get("low_hit_rate", 0.0))
        total_hits = int(gc.get("total_hits", 0))
        consistent = bool(gc.get("consistent_spectrum", False)) or (
            low_hr >= 0.20 and total_hits >= 15
        )
        return (
            self.n_days >= 100
            and self.breach_count == 0
            and self.no_retrain
            and self.l2l_day_path_ok
            and self.senses_day_path_ok
            and self.goal_consistency_ok
            and consistent
            and len(self.pair_results) >= 2
            and bool(self.metadata.get("multi_symbol"))
            and bool(self.metadata.get("pullback_continuation_coverage"))
            and float(self.metadata.get("leverage", 0)) == LEVERAGE
            and bool(self.metadata.get("goal_path_multi_leg", True))
        )


def simulate_fill_open_to_close(
    *,
    side: int,
    day: Dict[str, Any],
    size_risk_percent: float,
    stop_distance_pct: float = DEFAULT_STOP_DISTANCE_PCT,
    friction_pct: float = 0.04,
) -> float:
    o = float(day["open"])
    h = float(day["high"])
    l = float(day["low"])
    c = float(day["close"])
    if o <= 0 or size_risk_percent <= 0:
        return 0.0
    if side > 0:
        adverse_pct = (o - l) / o * 100.0
        move_pct = (c - o) / o * 100.0
    else:
        adverse_pct = (h - o) / o * 100.0
        move_pct = (o - c) / o * 100.0
    fr = float(friction_pct) * 0.01
    if adverse_pct >= stop_distance_pct:
        return float(-size_risk_percent - fr)
    r_mult = float(np.clip(move_pct / max(stop_distance_pct, 1e-6), -1.0, 12.0))
    pnl = size_risk_percent * r_mult - fr
    return float(max(pnl, -size_risk_percent - fr))


def _sense_from_edge(snap, target: float, risk: float) -> MarketSenseInput:
    forces = [e.force for e in snap.set_edges]
    # pad to 8
    while len(forces) < 8:
        forces.append(forces[-1] if forces else 0.0)
    vels = []
    inns = []
    for e in snap.set_edges:
        v = (e.ltf_rsi - 50.0) / 50.0
        vels.append(float(np.clip(v, -1, 1)))
        inns.append(e.force * 0.85)
    while len(vels) < 4:
        vels.append(0.0)
        inns.append(0.0)
    best = snap.best
    topo = best.topology if best else "chop"
    return MarketSenseInput(
        htf_force=forces[:8],
        ltf_velocity=vels[:4],
        inertia=inns[:4],
        inertia_baseline=[x * 0.5 for x in inns[:4]],
        velocity_baseline=[x * 0.3 for x in vels[:4]],
        full_body_outside_rails=abs(snap.consensus_force) >= 0.35,
        ltf_inside_tight=True,
        efficiency=0.55 if snap.n_pullback + snap.n_continuation > 0 else 0.3,
        regime=(
            "bull"
            if snap.multi_set_consensus == "agree_long"
            else "bear"
            if snap.multi_set_consensus == "agree_short"
            else "chop"
            if snap.multi_set_consensus == "conflict"
            else "undefined"
        ),
        g_fixed=True,
        target_percent=target,
        max_daily_risk_percent=risk,
        composition_has_force=any(abs(e.force) >= 0.15 for e in snap.set_edges),
        composition_has_velocity=any(e.topology != "chop" for e in snap.set_edges),
        cross_family_agree=snap.multi_set_consensus in ("agree_long", "agree_short"),
        set_conflict=snap.multi_set_consensus == "conflict",
    )


def run_one_day_multi(
    policy: FrozenMetaPolicy,
    day_by_symbol: Dict[str, Dict[str, Any]],
    m1_history_by_symbol: Dict[str, List[dict]],
    *,
    target_percent: float,
    max_daily_risk_percent: float,
    symbols: Sequence[str],
    friction: Optional[FrictionAssumptions] = None,
    stop_distance_pct: float = DEFAULT_STOP_DISTANCE_PCT,
    equity: float = 100_000.0,
    tf_cache_by_symbol: Optional[Dict[str, Dict[str, List[dict]]]] = None,
) -> DayResult:
    """One calendar day across symbols: prior-only multi-TF edge → open fills."""
    fp_before = policy.weight_fingerprint()
    fr = friction or FrictionAssumptions()
    ledger = DailyRiskLedger(
        max_daily_risk_percent=max_daily_risk_percent,
        equity=equity,
        friction=fr,
    )

    date = next(iter(day_by_symbol.values()))["date"]
    # Indicators as-of previous calendar day only (no same-day bars)
    # Caller should pass history with date < today; asof_date = last hist date
    trades: List[SymbolDayTrade] = []
    n_pb = n_ct = 0
    topologies: List[str] = []
    acts: List[str] = []
    senses_ok = True
    l2l_ok = True
    roles_all: List[str] = []
    decision_dirs: List[float] = []

    # Equal risk slice per symbol opportunity, remaining budget shared
    for sym in symbols:
        day = day_by_symbol.get(sym)
        hist = m1_history_by_symbol.get(sym, [])
        if day is None:
            continue
        cache = None
        if tf_cache_by_symbol and sym in tf_cache_by_symbol:
            cache = tf_cache_by_symbol[sym]
        asof = hist[-1]["date"] if hist else None
        if cache is None and len(hist) < 200:
            continue
        snap = scan_all_sets(hist if cache is None else [], symbol=sym, tf_cache=cache, asof_date=asof)
        n_pb += snap.n_pullback
        n_ct += snap.n_continuation
        official = edge_to_set_confluence(snap)
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
        day_l2l = (
            role_base.topology == renamed.topology
            and role_base.act == renamed.act
            and role_base.topology == swapped.topology
            and novel.chain_ok
        )
        l2l_ok = l2l_ok and day_l2l

        sense_inp = _sense_from_edge(snap, target_percent, max_daily_risk_percent)
        sense_rep = probe_all_senses(sense_inp)
        day_senses = (
            "topology_class" in sense_rep.sight
            and "max_tension_load_building" in sense_rep.feel
            and "edge_quality" in sense_rep.taste
            and "wait_subtype" in sense_rep.hearing
        )
        senses_ok = senses_ok and day_senses

        best = snap.best
        topology = best.topology if best else "chop"
        # Map edge topologies into policy vocabulary
        pol_topo = {
            "pullback_resume": "launch",
            "continuation": "release",
            "slingshot_load": "slingshot_load",
            "collapse": "collapse",
            "chop": "chop",
        }.get(topology, "chop")
        topologies.append(topology)
        roles = tuple(sorted({r.value for r in role_base.roles.values()})) or ("force", "velocity")
        roles_all.extend(roles)
        decision_dirs.append(float(snap.consensus_force))

        pullback_flag = topology == "slingshot_load" or topology == "pullback_resume"
        state = build_meta_rl_state(
            target_percent=target_percent,
            max_daily_risk_percent=max_daily_risk_percent,
            official=official,
            structure=StructureFlags(pullback=pullback_flag, scale_conflict=snap.multi_set_consensus == "conflict"),
            progress_to_target=max(ledger.realized_pnl_percent, 0.0) / max(target_percent, 1e-6),
            realized_risk_percent=max(-ledger.realized_pnl_percent, 0.0),
            session_phase=0.35,
        )

        # Prefer edge act when HTF+LTF edge fires; policy sizes / risk-gates
        action = policy.forward(state, ledger=ledger, topology=pol_topo, roles=roles)

        # Coverage: if edge says pullback_resume or continuation, do not let chop stand-down kill it
        if best is not None and best.act in ("long", "short") and best.htf_agree:
            if action.act == "wait" and pol_topo in ("launch", "release"):
                # Re-ask with launch topology for sizing only — side from state set dirs
                action = policy.forward(state, ledger=ledger, topology="launch", roles=roles)
            # If state dirs neutral but edge clear, pack stronger dirs into a fresh state
            if action.act == "wait" or (action.act in ("long", "short") and action.act != best.act):
                st2 = state.copy()
                sign = 1.0 if best.act == "long" else -1.0
                # Only boost if edge is real — still prior-only features
                for idx in (0, 3, 6, 9):
                    if idx < st2.size:
                        st2[idx] = sign * max(abs(float(st2[idx])), 0.85)
                action = policy.forward(st2, ledger=ledger, topology="launch", roles=roles)
                if action.act in ("long", "short") and action.act != best.act:
                    # force side via state only (already set dirs)
                    pass

        hearing_wait = sense_rep.hearing.get("wait_subtype") or ""
        if hearing_wait == "kill" and snap.multi_set_consensus == "conflict":
            action = type(action)(
                act="wait",
                size_risk_percent=0.0,
                reason="hearing_kill_conflict",
                wait_subtype="kill",
                topology=topology,
                roles_cited=roles,
            )

        remaining = ledger.remaining_risk_budget_percent()
        if action.act in ("long", "short") and action.size_risk_percent > 0 and remaining > 0.05:
            # Cap ticket to remaining; flea-jar: use risk-legal max under envelope
            size = min(action.size_risk_percent, remaining * 0.95)
            entry = float(day["open"])
            stop_px = stop_distance_price_from_pct(entry, stop_distance_pct)
            lot_info = risk_legal_max_lot(
                equity=equity,
                risk_percent=size,
                entry_price=entry,
                stop_distance_price=stop_px,
                symbol=sym,
                leverage=LEVERAGE,
            )
            # Align size to what lot actually risks
            size = min(size, float(lot_info["risk_percent_actual"]) or size)
            if size <= 0 or lot_info["lot"] <= 0:
                acts.append("wait")
                continue
            if ledger.would_breach(size):
                acts.append("wait")
                continue

            side = 1 if action.act == "long" else -1
            pnl = simulate_fill_open_to_close(
                side=side,
                day=day,
                size_risk_percent=size,
                stop_distance_pct=stop_distance_pct,
                friction_pct=fr.total_pct,
            )
            ledger.positions.append(
                OpenPosition(
                    symbol=sym,
                    side=side,
                    risk_percent=size,
                    notional_pct=size / max(stop_distance_pct, 1e-6) * 100.0,
                )
            )
            apply_trade_result(ledger, pnl_percent=pnl, closed_risk_percent=size)
            trades.append(
                SymbolDayTrade(
                    symbol=sym,
                    act=action.act,
                    size_risk_percent=size,
                    pnl_percent=pnl,
                    topology=topology,
                    set_id=best.set_id if best else 0,
                    edge_kind=topology,
                    lot=float(lot_info["lot"]),
                    leverage=LEVERAGE,
                )
            )
            acts.append(action.act)
        else:
            acts.append("wait")

    loss_today = max(-ledger.realized_pnl_percent, 0.0)
    worst = ledger.worst_case_daily_loss_percent()
    breach = loss_today > max_daily_risk_percent + 1e-6 or worst > max_daily_risk_percent + 1e-6

    policy.assert_frozen()
    if policy.weight_fingerprint() != fp_before:
        raise RuntimeError("NO_RETRAIN_VIOLATION mid day")

    pnl_final = float(ledger.realized_pnl_percent)
    hit = bool(pnl_final >= float(target_percent) - 1e-9)
    progress = float(np.clip(pnl_final / max(float(target_percent), 1e-6), 0.0, 1.0))
    act_summary = ",".join(acts) if acts else "wait"
    topo_summary = ",".join(topologies) if topologies else "chop"

    return DayResult(
        day=date,
        target_percent=target_percent,
        max_daily_risk_percent=max_daily_risk_percent,
        pnl_percent=pnl_final,
        worst_case_loss_percent=float(max(loss_today, 0.0)),
        breach=bool(breach),
        n_trades=len(trades),
        retrain_steps=policy.train_steps,
        topology=topo_summary,
        act_summary=act_summary,
        hit_target=hit,
        goal_progress=progress,
        wait_subtype="" if trades else "no_trade",
        roles=tuple(sorted(set(roles_all))) or ("force", "velocity"),
        decision_dir=float(np.mean(decision_dirs)) if decision_dirs else 0.0,
        fill_model="open_decision_close_or_stop",
        senses_ok=senses_ok,
        l2l_ok=l2l_ok,
        n_pullback=n_pb,
        n_continuation=n_ct,
        symbols_traded=tuple(t.symbol for t in trades),
        symbol_trades=tuple(asdict(t) for t in trades),
        leverage=LEVERAGE,
    )


def compute_goal_consistency(
    day_results: Sequence[DayResult],
    pair_results: Dict[str, Dict[str, Any]],
) -> Tuple[bool, Dict[str, Any]]:
    meta: Dict[str, Any] = {}
    if not day_results or not pair_results:
        return False, {"reason": "empty"}

    total_hits = sum(1 for d in day_results if d.hit_target)
    mean_progress = float(np.mean([d.goal_progress for d in day_results]))
    max_pnl = float(max(d.pnl_percent for d in day_results))
    meta["total_hits"] = total_hits
    meta["mean_goal_progress"] = mean_progress
    meta["max_day_pnl_percent"] = max_pnl

    by_target: Dict[float, List[DayResult]] = {}
    for d in day_results:
        by_target.setdefault(d.target_percent, []).append(d)
    target_stats = {}
    for t, rows in sorted(by_target.items()):
        hits = sum(1 for r in rows if r.hit_target)
        fires = sum(1 for r in rows if r.n_trades > 0)
        target_stats[str(t)] = {
            "days": len(rows),
            "hits": hits,
            "hit_rate": hits / len(rows),
            "fire_rate": fires / len(rows),
            "mean_pnl": float(np.mean([r.pnl_percent for r in rows])),
            "mean_goal_progress": float(np.mean([r.goal_progress for r in rows])),
        }
    meta["by_target"] = target_stats

    low = [d for d in day_results if d.target_percent <= 15.0]
    high = [d for d in day_results if d.target_percent >= 70.0]
    low_fire = (sum(1 for d in low if d.n_trades > 0) / len(low)) if low else 0.0
    high_fire = (sum(1 for d in high if d.n_trades > 0) / len(high)) if high else 0.0
    low_prog = float(np.mean([d.goal_progress for d in low])) if low else 0.0
    high_prog = float(np.mean([d.goal_progress for d in high])) if high else 0.0
    low_hits = sum(1 for d in low if d.hit_target) if low else 0
    low_hit_rate = (low_hits / len(low)) if low else 0.0
    mid = [d for d in day_results if 15.0 < d.target_percent < 70.0]
    mid_hits = sum(1 for d in mid if d.hit_target) if mid else 0
    mid_hit_rate = (mid_hits / len(mid)) if mid else 0.0
    meta["low_fire_rate"] = low_fire
    meta["high_fire_rate"] = high_fire
    meta["low_mean_goal_progress"] = low_prog
    meta["high_mean_goal_progress"] = high_prog
    meta["low_hits"] = low_hits
    meta["low_hit_rate"] = low_hit_rate
    meta["mid_hits"] = mid_hits
    meta["mid_hit_rate"] = mid_hit_rate

    # Final-boss consistency: low band must clear often; total hits non-vacuous
    non_vacuous = (total_hits >= 5 and low_hits >= 3) or (
        low_hit_rate >= 0.15 and max_pnl >= 5.0 and total_hits >= 3
    )
    behavior_conditioned = abs(low_fire - high_fire) >= 0.02 or abs(low_prog - high_prog) >= 0.01
    pairs_ok = all("hit_rate" in b for b in pair_results.values())
    spectrum_ok = pairs_ok and len(target_stats) >= 2
    progress_consistent = low_prog + 1e-9 >= high_prog * 0.35 or low_hits >= 3
    consistent_spectrum = low_hit_rate >= 0.18 and total_hits >= 12 and (
        mid_hit_rate >= 0.05 or mid_hits >= 2 or low_hit_rate >= 0.30
    )
    ok = bool(
        non_vacuous
        and behavior_conditioned
        and spectrum_ok
        and progress_consistent
        and (consistent_spectrum or (low_hit_rate >= 0.25 and total_hits >= 20))
    )
    meta["non_vacuous"] = non_vacuous
    meta["behavior_conditioned"] = behavior_conditioned
    meta["spectrum_ok"] = spectrum_ok
    meta["progress_consistent"] = progress_consistent
    meta["consistent_spectrum"] = consistent_spectrum
    meta["goal_consistency_ok"] = ok
    return ok, meta


def _l2l_unit_check() -> bool:
    sensors = novel_composition("cci", "rsi", force_val=0.7, velocity_val=0.6, inertia_val=0.5)
    r = evaluate_understanding(sensors)
    return r.act in ("long", "short") and r.chain_ok


def run_forward_eval(
    *,
    price_path: Optional[Path] = None,
    n_days: int = 100,
    targets: Sequence[float] = DEFAULT_TARGET_GRID,
    risks: Sequence[float] = DEFAULT_RISK_GRID,
    seed: int = 42,
    warmup_days: int = 15,
    symbols: Optional[Sequence[str]] = None,
    pair_mode: str = "random",  # random | rotate — document final boss uses random targets
    use_goal_path: bool = True,
    policy: Optional[FrozenMetaPolicy] = None,
    champion_path: Optional[Path] = None,
) -> ForwardEvalReport:
    syms = list(symbols) if symbols else [s for s in DEFAULT_SYMBOLS if s in available_symbols()]
    if not syms:
        syms = ["XAUUSD"]

    # Primary path for fingerprint; multi-symbol loads all
    primary = Path(price_path) if price_path else SYMBOL_FILES.get(syms[0], DEFAULT_PRICE)

    metadata: Dict[str, Any] = {
        "price_path": str(primary),
        "price_exists": primary.exists() if primary else False,
        "symbols": syms,
        "multi_symbol": len(syms) > 1,
        "n_days_requested": n_days,
        "targets": list(targets),
        "risks": list(risks),
        "seed": seed,
        "label": "forward_sim_shadow",
        "fill_timing": (
            "goal_path_multi_slot_m1"
            if use_goal_path
            else "decision_at_open_from_prior_m1; fill open_to_close_or_stop"
        ),
        "no_lookahead": True,
        "force_side_used": False,
        "leverage": LEVERAGE,
        "edge": "mark_sets_htf_force_ltf_rsi5_bb10_shift2_pullback_continuation",
        "friction": asdict(FrictionAssumptions()),
        "stop_distance_pct": DEFAULT_STOP_DISTANCE_PCT,
        "warmup_days": warmup_days,
        "pair_mode": pair_mode,
        "goal_path_multi_leg": bool(use_goal_path),
    }

    unit_l2l = _l2l_unit_check()

    # Discover calendar intersection across symbols
    daily_by_sym: Dict[str, List[dict]] = {}
    m1_by_sym: Dict[str, List[dict]] = {}

    trail = max(n_days + warmup_days + 5, 130)
    for sym in syms:
        path = SYMBOL_FILES.get(sym)
        if path is None or not path.exists():
            continue
        # Trailing calendar window only — multi-symbol full CSVs are 100MB+ each
        m1_all = load_m1_trailing_calendar_days(path, n_days=trail)
        if not m1_all:
            continue
        daily = bars_to_daily(m1_all)
        daily_by_sym[sym] = daily
        m1_by_sym[sym] = m1_all

    if not daily_by_sym:
        metadata["error"] = "price_data_missing"
        return ForwardEvalReport(
            n_days=0,
            breach_count=-1,
            pair_results={},
            no_retrain=True,
            l2l_unit_ok=unit_l2l,
            metadata=metadata,
        )

    # Intersection of dates present on all symbols (multi-symbol concurrent)
    date_sets = [set(d["date"] for d in days) for days in daily_by_sym.values()]
    common = sorted(set.intersection(*date_sets)) if len(date_sets) > 1 else sorted(date_sets[0])
    metadata["available_calendar_days"] = len(common)

    need = n_days + warmup_days
    if len(common) < need:
        metadata["warning"] = f"only {len(common)} common calendar days; need {need}"
        window_dates = common
    else:
        window_dates = common[-(n_days + warmup_days) :]

    eval_dates = window_dates[warmup_days:] if len(window_dates) > warmup_days else window_dates[1:]
    if len(eval_dates) > n_days:
        eval_dates = eval_dates[-n_days:]

    if eval_dates:
        metadata["window"] = "last_n_common_chronological_with_warmup"
        metadata["window_start"] = eval_dates[0]
        metadata["window_end"] = eval_dates[-1]
        metadata["warmup_start"] = window_dates[0]

    # Build date->daily bar per symbol
    daily_maps = {
        sym: {d["date"]: d for d in days} for sym, days in daily_by_sym.items()
    }

    # Pre-resample TF frames once per symbol (major speedup)
    tf_cache_by_symbol: Dict[str, Dict[str, List[dict]]] = {}
    for sym, m1 in m1_by_sym.items():
        tf_cache_by_symbol[sym] = build_tf_cache(m1)

    # Permanent Law A14: trained meta-policy required; no weight update during forward
    # CASE-0035: optional shadow policy / champion_path for opportunity-curriculum measure
    if policy is not None:
        pol = policy
        metadata["policy_source"] = "injected"
    elif champion_path is not None:
        pol = load_or_train_champion(path=Path(champion_path), seed=seed, n_steps=2500)
        metadata["policy_source"] = f"path:{Path(champion_path).name}"
    else:
        pol = load_or_train_champion(seed=seed, n_steps=2500)
        metadata["policy_source"] = "default_champion"
    policy = pol
    policy.assert_frozen()
    fp0 = policy.weight_fingerprint()
    metadata["policy_trained"] = bool(policy.trained)
    metadata["meta_train_steps"] = int(policy.meta_train_steps)
    metadata["policy_fingerprint"] = fp0
    pairs = [(float(t), float(r)) for t in targets for r in risks]
    rng = np.random.default_rng(seed)
    day_results: List[DayResult] = []

    for i, date in enumerate(eval_dates):
        if pair_mode == "random":
            t = float(rng.choice(list(targets)))
            r = float(rng.choice(list(risks)))
        else:
            t, r = pairs[i % len(pairs)]

        day_by_symbol = {}
        hist_by_symbol = {}
        for sym in syms:
            if sym not in daily_maps or date not in daily_maps[sym]:
                continue
            day_by_symbol[sym] = daily_maps[sym][date]
            # Full M1 history for goal-path (edge filters by asof_date/time)
            hist_by_symbol[sym] = m1_by_sym.get(sym, [])

        if not day_by_symbol:
            continue

        if use_goal_path:
            fills, ledger, gmeta = run_goal_path_day(
                policy,
                date=date,
                m1_by_symbol=hist_by_symbol,
                target_percent=float(t),
                max_daily_risk_percent=float(r),
                symbols=syms,
                tf_cache_by_symbol=tf_cache_by_symbol,
            )
            loss_today = max(-ledger.realized_pnl_percent, 0.0)
            worst = ledger.worst_case_daily_loss_percent()
            breach = loss_today > float(r) + 1e-6 or worst > float(r) + 1e-6
            pnl_final = float(ledger.realized_pnl_percent)
            hit = bool(pnl_final >= float(t) - 1e-9)
            progress = float(np.clip(pnl_final / max(float(t), 1e-6), 0.0, 1.0))
            acts = [f.act for f in fills]
            topos = [f.topology for f in fills]
            dr = DayResult(
                day=date,
                target_percent=float(t),
                max_daily_risk_percent=float(r),
                pnl_percent=pnl_final,
                worst_case_loss_percent=float(max(loss_today, 0.0)),
                breach=bool(breach),
                n_trades=len(fills),
                retrain_steps=policy.train_steps,
                topology=",".join(topos) if topos else "chop",
                act_summary=",".join(acts) if acts else "wait",
                hit_target=hit,
                goal_progress=progress,
                wait_subtype="" if fills else "no_trade",
                roles=tuple(gmeta.get("roles") or ("force", "velocity")),
                decision_dir=0.0,
                fill_model="goal_path_multi_slot_m1",
                senses_ok=bool(gmeta.get("senses_ok")),
                l2l_ok=bool(gmeta.get("l2l_ok")),
                n_pullback=int(gmeta.get("n_pullback", 0)),
                n_continuation=int(gmeta.get("n_continuation", 0)),
                symbols_traded=tuple(f.symbol for f in fills),
                symbol_trades=tuple(
                    {
                        "symbol": f.symbol,
                        "act": f.act,
                        "size_risk_percent": f.size_risk_percent,
                        "pnl_percent": f.pnl_percent,
                        "topology": f.topology,
                        "edge_kind": f.edge_kind,
                        "lot": f.lot,
                        "slot": f.slot,
                        "leverage": LEVERAGE,
                    }
                    for f in fills
                ),
                leverage=LEVERAGE,
            )
        else:
            # Legacy single open→close path (compat)
            hist_stub = {}
            for sym in day_by_symbol:
                prev_dates = [d for d in daily_maps[sym] if d < date]
                if not prev_dates:
                    continue
                asof = prev_dates[-1]
                hist_stub[sym] = [
                    {
                        "date": asof,
                        "time": "23:59:00",
                        "open": daily_maps[sym][asof]["open"],
                        "high": daily_maps[sym][asof]["high"],
                        "low": daily_maps[sym][asof]["low"],
                        "close": daily_maps[sym][asof]["close"],
                    }
                ]
            dr = run_one_day_multi(
                policy,
                day_by_symbol,
                hist_stub,
                target_percent=float(t),
                max_daily_risk_percent=float(r),
                symbols=syms,
                tf_cache_by_symbol=tf_cache_by_symbol,
            )
        day_results.append(dr)

    policy.assert_frozen()
    # no_retrain = no inference-time weight updates when target/risk changes (meta already trained)
    no_retrain = (
        policy.weight_fingerprint() == fp0
        and policy.inference_updates == 0
        and policy.frozen_for_inference
        and policy.trained
    )
    breach_count = sum(1 for d in day_results if d.breach)

    pair_results: Dict[str, Dict[str, Any]] = {}
    for d in day_results:
        key = f"{d.target_percent}_{d.max_daily_risk_percent}"
        bucket = pair_results.setdefault(
            key,
            {
                "target": d.target_percent,
                "risk": d.max_daily_risk_percent,
                "days": 0,
                "breaches": 0,
                "hits": 0,
                "hit_rate": 0.0,
                "mean_pnl": 0.0,
                "mean_goal_progress": 0.0,
                "trades": 0,
                "pullbacks": 0,
                "continuations": 0,
            },
        )
        bucket["days"] += 1
        bucket["breaches"] += int(d.breach)
        bucket["hits"] += int(d.hit_target)
        bucket["mean_pnl"] += d.pnl_percent
        bucket["mean_goal_progress"] += d.goal_progress
        bucket["trades"] += d.n_trades
        bucket["pullbacks"] += d.n_pullback
        bucket["continuations"] += d.n_continuation
    for b in pair_results.values():
        n = max(b["days"], 1)
        b["mean_pnl"] = b["mean_pnl"] / n
        b["mean_goal_progress"] = b["mean_goal_progress"] / n
        b["hit_rate"] = b["hits"] / n

    goal_ok, goal_meta = compute_goal_consistency(day_results, pair_results)
    l2l_day = all(d.l2l_ok for d in day_results) and len(day_results) > 0
    senses_day = all(d.senses_ok for d in day_results) and len(day_results) > 0
    total_pb = sum(d.n_pullback for d in day_results)
    total_ct = sum(d.n_continuation for d in day_results)

    raw = primary.read_bytes()[:4096] if primary.exists() else b""
    metadata["dataset_fingerprint"] = hashlib.sha256(raw).hexdigest()[:16]
    metadata["policy_fingerprint"] = fp0
    metadata["n_days_executed"] = len(day_results)
    metadata["goal_consistency"] = goal_meta
    metadata["l2l_day_path_ok"] = l2l_day
    metadata["senses_day_path_ok"] = senses_day
    metadata["l2l_unit_ok"] = unit_l2l
    metadata["pullback_continuation_coverage"] = total_pb + total_ct > 0
    metadata["total_pullback_signals"] = total_pb
    metadata["total_continuation_signals"] = total_ct
    metadata["symbols_with_trades"] = sorted(
        {s for d in day_results for s in d.symbols_traded}
    )

    return ForwardEvalReport(
        n_days=len(day_results),
        breach_count=breach_count,
        pair_results=pair_results,
        day_results=day_results,
        no_retrain=no_retrain,
        l2l_day_path_ok=l2l_day,
        senses_day_path_ok=senses_day,
        goal_consistency_ok=goal_ok,
        l2l_unit_ok=unit_l2l,
        metadata=metadata,
    )


# Back-compat helpers used by older tests
def decision_features_from_history(history: Sequence[Dict[str, Any]], lookback: int = 5) -> Dict[str, Any]:
    """Legacy prior-only daily features (kept for unit tests)."""
    if len(history) < 1:
        return {"dir_sign": 0.0, "force": 0.0, "velocity": 0.0, "inertia": 0.0}
    closes = [float(d["close"]) for d in history[-lookback:]]
    rets = []
    for i in range(1, len(closes)):
        if closes[i - 1]:
            rets.append((closes[i] - closes[i - 1]) / closes[i - 1])
    mean_ret = float(np.mean(rets)) if rets else 0.0
    last = history[-1]
    o, h, l, c = float(last["open"]), float(last["high"]), float(last["low"]), float(last["close"])
    rng = max(h - l, 1e-9)
    body = (c - o) / rng
    force = float(np.clip(mean_ret * 80.0, -1.0, 1.0))
    velocity = float(np.clip(body, -1.0, 1.0))
    return {
        "dir_sign": float(np.clip(0.65 * force + 0.35 * velocity, -1.0, 1.0)),
        "force": force,
        "velocity": velocity,
        "inertia": force * 0.8,
        "efficiency": 0.5,
        "regime": "bull" if force > 0.2 else "bear" if force < -0.2 else "chop",
        "pullback": force * velocity < 0,
        "range_pct_prior": float(rng / max(c, 1e-9) * 100.0),
        "prior_ret_pct": mean_ret * 100.0,
    }


def run_one_day(policy, day, history, **kwargs):
    """Single-symbol adapter for unit tests (XAU-shaped)."""
    # synthesize minimal m1 from daily history
    m1 = []
    for d in history:
        m1.append(
            {
                "date": d["date"],
                "time": "12:00:00",
                "open": d["open"],
                "high": d["high"],
                "low": d["low"],
                "close": d["close"],
            }
        )
        # pad synthetic intraday so RSI/BB have bars
        px = float(d["close"])
        for k in range(1, 30):
            m1.append(
                {
                    "date": d["date"],
                    "time": f"{12 + k // 60:02d}:{k % 60:02d}:00",
                    "open": px,
                    "high": px * 1.0002,
                    "low": px * 0.9998,
                    "close": px * (1 + 0.0001 * (1 if k % 2 == 0 else -1)),
                }
            )
            px = m1[-1]["close"]
    return run_one_day_multi(
        policy,
        {"XAUUSD": day},
        {"XAUUSD": m1},
        target_percent=kwargs.get("target_percent", 5.0),
        max_daily_risk_percent=kwargs.get("max_daily_risk_percent", 2.0),
        symbols=["XAUUSD"],
        friction=kwargs.get("friction"),
        stop_distance_pct=kwargs.get("stop_distance_pct", DEFAULT_STOP_DISTANCE_PCT),
    )


def load_daily_bars(path: Path) -> List[Dict[str, Any]]:
    m1 = load_m1_bars(Path(path))
    return bars_to_daily(m1)


def report_to_dict(report: ForwardEvalReport) -> Dict[str, Any]:
    return {
        "n_days": report.n_days,
        "breach_count": report.breach_count,
        "pair_results": report.pair_results,
        "no_retrain": report.no_retrain,
        "l2l_day_path_ok": report.l2l_day_path_ok,
        "l2l_novel_ok": report.l2l_novel_ok,
        "l2l_unit_ok": report.l2l_unit_ok,
        "senses_day_path_ok": report.senses_day_path_ok,
        "goal_consistency_ok": report.goal_consistency_ok,
        "promote_ready": report.promote_ready,
        "metadata": report.metadata,
        "day_results_head": [asdict(d) for d in report.day_results[:5]],
        "day_results_tail": [asdict(d) for d in report.day_results[-5:]],
    }


def save_report(report: ForwardEvalReport, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = report_to_dict(report)
    payload["day_results_all"] = [asdict(d) for d in report.day_results]
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
