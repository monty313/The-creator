"""Mark multi-set pullback / continuation edge (Court CASE-0002).

Mechanism
---------
For each official Mark set (LTF first, HTF last two):
  1. HTF force = slope pair (trend_dir) on confirmation TFs; optional lab blend
     with Monty CCI+BB / RSI+BB on both HTFs (``monty_htf_blend``).
  2. LTF timing = RSI(5) + BB(10, dev=0.5, shift=+2) on the entry TF.
  3. Pullback: HTF force clear AND LTF dipped toward opposite BB rail / RSI
     against force, then resumed with force (timing).
  4. Continuation: HTF force clear AND LTF RSI+price aligned with force
     (no deep dip required).

No look-ahead: indicators use completed bars only; BB shift delays the rails.
Source flags slope_on / cci_on / rsi_on pack into doctrine when blend is used.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .htf_force import compute_htf_force_from_bars
from .indicators import bollinger, resample_m1_to_tf, rsi, trend_dir
from .sets import OFFICIAL_SETS


@dataclass(frozen=True)
class SetEdge:
    set_id: int
    name: str
    force: float  # HTF signed
    ltf_rsi: float
    topology: str  # pullback_resume | continuation | slingshot_load | chop | collapse
    act: str  # long | short | wait
    reason: str
    htf_agree: bool
    # HTF wind source flags (0/1) — doctrine indices 12–14 when packed
    slope_on: float = 0.0
    cci_on: float = 0.0
    rsi_on: float = 0.0
    force_mode: str = "slope"
    force_reason: str = ""


@dataclass
class SymbolEdgeSnapshot:
    symbol: str
    set_edges: List[SetEdge]
    consensus_force: float
    best: Optional[SetEdge]
    multi_set_consensus: str  # agree_long | agree_short | conflict | incomplete
    n_pullback: int
    n_continuation: int
    # Aggregated source flags (OR across sets) for doctrine pack
    slope_on: float = 0.0
    cci_on: float = 0.0
    rsi_on: float = 0.0


def _closes(bars: Sequence[dict]) -> np.ndarray:
    return np.array([float(b["close"]) for b in bars], dtype=np.float64)


def _ltf_timing_signal(
    closes: np.ndarray,
    force: float,
) -> Tuple[str, str, float, str]:
    """Return topology, act, rsi_last, reason from RSI5+BB10 on LTF closes."""
    if closes.size < 20 or abs(force) < 0.15:
        return "chop", "wait", 50.0, "no_force_or_short_history"

    r = rsi(closes, period=5)
    mid, up, lo = bollinger(closes, period=10, dev=0.5, shift=2)
    i = closes.size - 1
    # need prior bar for resume detection
    if i < 1 or np.isnan(r[i]) or np.isnan(mid[i]):
        return "chop", "wait", 50.0, "indicator_nan"

    price = float(closes[i])
    price_prev = float(closes[i - 1])
    rsi_now = float(r[i])
    rsi_prev = float(r[i - 1]) if not np.isnan(r[i - 1]) else rsi_now
    m, u, l = float(mid[i]), float(up[i]), float(lo[i])
    band = max(u - l, 1e-9)

    side = 1 if force > 0 else -1
    # Location in band: 0 = lower, 1 = upper
    loc = (price - l) / band
    loc_prev = (price_prev - l) / band if not np.isnan(lo[i]) else loc

    # Against-force dip (pullback material)
    if side > 0:
        dipped = loc_prev < 0.35 or rsi_prev < 40.0
        resumed = (price > m and rsi_now > rsi_prev) or (loc > loc_prev and rsi_now >= 45.0)
        aligned = price >= m and rsi_now >= 50.0
        collapse = price < l and rsi_now < 30.0 and force > 0.25
    else:
        dipped = loc_prev > 0.65 or rsi_prev > 60.0
        resumed = (price < m and rsi_now < rsi_prev) or (loc < loc_prev and rsi_now <= 55.0)
        aligned = price <= m and rsi_now <= 50.0
        collapse = price > u and rsi_now > 70.0 and force < -0.25

    if collapse:
        return "collapse", "wait", rsi_now, "ltf_collapse_against_stale_force"

    if dipped and not resumed:
        return "slingshot_load", "wait", rsi_now, "pullback_loading_not_yet"

    if dipped and resumed:
        act = "long" if side > 0 else "short"
        return "pullback_resume", act, rsi_now, "htf_force_ltf_rsi_bb_resume"

    if aligned and abs(force) >= 0.2:
        act = "long" if side > 0 else "short"
        return "continuation", act, rsi_now, "htf_force_ltf_continuation"

    return "chop", "wait", rsi_now, "no_timing_edge"


def evaluate_set_edge(
    m1_bars: Sequence[dict],
    set_id: int,
    name: str,
    ltf: str,
    htf1: str,
    htf2: str,
    *,
    monty_htf_blend: bool = False,
) -> SetEdge:
    """Evaluate one official set from M1 history (completed bars only)."""
    ltf_bars = resample_m1_to_tf(m1_bars, ltf)
    h1_bars = resample_m1_to_tf(m1_bars, htf1)
    h2_bars = resample_m1_to_tf(m1_bars, htf2)

    htf = compute_htf_force_from_bars(
        h1_bars,
        h2_bars,
        monty_htf_blend=bool(monty_htf_blend),
        agree_min=0.12,
        incomplete_scale=0.35,
        dual_lookback=False,
    )
    force = float(htf.force)
    htf_agree = bool(htf.htf_agree)

    if len(ltf_bars) < 25:
        return SetEdge(
            set_id=set_id,
            name=name,
            force=force,
            ltf_rsi=50.0,
            topology="chop",
            act="wait",
            reason="insufficient_ltf_bars",
            htf_agree=htf_agree,
            slope_on=htf.slope_on,
            cci_on=htf.cci_on,
            rsi_on=htf.rsi_on,
            force_mode=htf.mode,
            force_reason=htf.reason,
        )

    topo, act, rsi_v, reason = _ltf_timing_signal(_closes(ltf_bars), force)
    if not htf_agree and act != "wait":
        # No permission without HTF agreement — Mark law
        act = "wait"
        topo = "chop"
        reason = "htf_incomplete_no_permission"
    return SetEdge(
        set_id=set_id,
        name=name,
        force=force,
        ltf_rsi=rsi_v,
        topology=topo,
        act=act,
        reason=reason,
        htf_agree=htf_agree,
        slope_on=htf.slope_on,
        cci_on=htf.cci_on,
        rsi_on=htf.rsi_on,
        force_mode=htf.mode,
        force_reason=htf.reason,
    )


def build_tf_cache(m1_bars: Sequence[dict]) -> Dict[str, List[dict]]:
    """Resample M1 once for all TFs used by MARK_SETS_LAW."""
    tfs = {"1m", "5m", "15m", "30m", "1h", "4h", "1d"}
    return {tf: resample_m1_to_tf(m1_bars, tf) for tf in tfs}


def _bars_upto(
    bars: Sequence[dict],
    *,
    asof_date: Optional[str] = None,
    asof_time: Optional[str] = None,
) -> List[dict]:
    """Filter completed bars only (fast reverse scan; bars assumed chronological).

    - no asof_date: all bars
    - asof_date only: date <= asof_date (legacy full-day include)
    - asof_date + asof_time: date < asof_date OR (date == asof_date AND time < asof_time)
    """
    if not asof_date:
        return list(bars)
    if not bars:
        return []
    # Walk from end: most decisions need only recent lookback after this.
    out_rev: List[dict] = []
    for i in range(len(bars) - 1, -1, -1):
        b = bars[i]
        d = str(b.get("date", ""))
        t = str(b.get("time", "00:00:00"))
        if asof_time is None:
            keep = d <= asof_date
        else:
            keep = d < asof_date or (d == asof_date and t < asof_time)
        if not keep:
            # Still past asof if d > asof_date; skip. If we already passed into
            # valid region and then hit too-new? Chronological: from end, first
            # bars may be after asof — skip until we enter valid region, then
            # collect until we have enough or exhaust.
            if d > asof_date or (asof_time is not None and d == asof_date and t >= asof_time):
                continue
        if keep:
            out_rev.append(b)
            # Early stop once we have a large buffer (caller re-caps)
            if len(out_rev) >= 800:
                break
        elif out_rev and d < asof_date:
            break
    out_rev.reverse()
    return out_rev


def _htf_completed_only(
    bars: Sequence[dict],
    *,
    asof_date: Optional[str],
    asof_time: Optional[str],
    tf: str = "",
) -> List[dict]:
    """HTF force must not use incomplete same-day buckets (CASE-0004).

    When ``asof_time`` is set (intraday decision), confirmation TFs use only
    bars with date < asof_date. LTF timing may still use same-day completed bars.
    """
    if asof_date and asof_time is not None:
        closed = [b for b in bars if str(b.get("date", "")) < asof_date]
        return closed[-120:]
    return _bars_upto(bars, asof_date=asof_date, asof_time=asof_time)[-120:]


def multi_day_momentum(
    daily_bars: Sequence[dict],
    *,
    asof_date: str,
    n: int = 3,
) -> float:
    """Signed majority of last n *completed* daily returns before asof_date. [-1,1]."""
    closed = [b for b in daily_bars if str(b.get("date", "")) < asof_date]
    if len(closed) < n + 1:
        return 0.0
    rets = []
    for i in range(-n, 0):
        a = float(closed[i - 1]["close"])
        b = float(closed[i]["close"])
        if a > 0:
            rets.append((b - a) / a)
    if not rets:
        return 0.0
    pos = sum(1 for r in rets if r > 0)
    neg = sum(1 for r in rets if r < 0)
    if pos > neg:
        return float(np.clip(np.mean([r for r in rets if r > 0]) * 40.0, 0.05, 1.0))
    if neg > pos:
        return float(np.clip(np.mean([r for r in rets if r < 0]) * 40.0, -1.0, -0.05))
    return 0.0


def evaluate_set_edge_from_cache(
    tf_cache: Dict[str, List[dict]],
    set_id: int,
    name: str,
    ltf: str,
    htf1: str,
    htf2: str,
    *,
    asof_date: Optional[str] = None,
    asof_time: Optional[str] = None,
    monty_htf_blend: bool = False,
) -> SetEdge:
    """Like evaluate_set_edge but reuses pre-resampled frames; optional asof filter."""

    # Cap lookback: RSI/BB on full multi-week 1m history is O(n) death.
    _LTF_MAX = 400
    ltf_bars = _bars_upto(tf_cache.get(ltf, []), asof_date=asof_date, asof_time=asof_time)[-_LTF_MAX:]
    # CASE-0004: HTF confirmation from completed periods only (no partial same-day 1d/4h)
    h1_bars = _htf_completed_only(
        tf_cache.get(htf1, []), asof_date=asof_date, asof_time=asof_time, tf=htf1
    )
    h2_bars = _htf_completed_only(
        tf_cache.get(htf2, []), asof_date=asof_date, asof_time=asof_time, tf=htf2
    )

    # Dual-scale slope + optional Monty blend (incomplete_scale 0.25 matches legacy cache path)
    htf = compute_htf_force_from_bars(
        h1_bars,
        h2_bars,
        monty_htf_blend=bool(monty_htf_blend),
        agree_min=0.10,
        incomplete_scale=0.25,
        dual_lookback=True,
    )
    force = float(htf.force)
    htf_agree = bool(htf.htf_agree)
    slope_on, cci_on, rsi_on = htf.slope_on, htf.cci_on, htf.rsi_on
    force_mode, force_reason = htf.mode, htf.reason

    # Multi-day momentum from daily stack when present (legacy CASE-0004 tide)
    if asof_date and "1d" in tf_cache:
        mom = multi_day_momentum(tf_cache["1d"], asof_date=asof_date, n=3)
        if abs(mom) >= 0.05:
            if force * mom > 0:
                force = float(np.clip(force * 1.15 + 0.1 * mom, -1.0, 1.0))
            elif force * mom < 0:
                # fight multi-day tide → kill permission
                htf_agree = False
                force *= 0.15
                force_reason = (force_reason + "+multiday_fight").strip("+")

    if len(ltf_bars) < 25:
        return SetEdge(
            set_id=set_id,
            name=name,
            force=force,
            ltf_rsi=50.0,
            topology="chop",
            act="wait",
            reason="insufficient_ltf_bars",
            htf_agree=htf_agree,
            slope_on=slope_on,
            cci_on=cci_on,
            rsi_on=rsi_on,
            force_mode=force_mode,
            force_reason=force_reason,
        )

    topo, act, rsi_v, reason = _ltf_timing_signal(_closes(ltf_bars), force)
    if not htf_agree and act != "wait":
        act = "wait"
        topo = "chop"
        reason = "htf_incomplete_no_permission"
    return SetEdge(
        set_id=set_id,
        name=name,
        force=force,
        ltf_rsi=rsi_v,
        topology=topo,
        act=act,
        reason=reason,
        htf_agree=htf_agree,
        slope_on=slope_on,
        cci_on=cci_on,
        rsi_on=rsi_on,
        force_mode=force_mode,
        force_reason=force_reason,
    )


def scan_all_sets(
    m1_bars: Sequence[dict],
    symbol: str = "SYM",
    *,
    tf_cache: Optional[Dict[str, List[dict]]] = None,
    asof_date: Optional[str] = None,
    asof_time: Optional[str] = None,
    monty_htf_blend: bool = False,
) -> SymbolEdgeSnapshot:
    """Scan all 4 official Mark sets — never collapse to set2 only."""
    cache = tf_cache if tf_cache is not None else build_tf_cache(m1_bars)
    # When asof set, filter to completed bars only (caller owns decision time)
    edges: List[SetEdge] = []
    for s in OFFICIAL_SETS:
        e = evaluate_set_edge_from_cache(
            cache,
            s.set_id,
            s.name,
            s.entry_tf,
            s.confirmation_tfs[0],
            s.confirmation_tfs[1],
            asof_date=asof_date,
            asof_time=asof_time,
            monty_htf_blend=bool(monty_htf_blend),
        )
        edges.append(e)

    forces = [e.force for e in edges if e.htf_agree]
    if len(forces) >= 2 and all(f > 0.12 for f in forces):
        consensus = "agree_long"
    elif len(forces) >= 2 and all(f < -0.12 for f in forces):
        consensus = "agree_short"
    elif len(forces) >= 2 and any(f > 0 for f in forces) and any(f < 0 for f in forces):
        consensus = "conflict"
    else:
        consensus = "incomplete"

    n_pb = sum(1 for e in edges if e.topology == "pullback_resume")
    n_ct = sum(1 for e in edges if e.topology == "continuation")

    # Prefer pullback_resume over continuation; then strongest |force| actionable
    actionable = [e for e in edges if e.act in ("long", "short")]
    best: Optional[SetEdge] = None
    if actionable:
        pb = [e for e in actionable if e.topology == "pullback_resume"]
        pool = pb if pb else actionable
        best = max(pool, key=lambda e: abs(e.force))

    mean_force = float(np.mean([e.force for e in edges])) if edges else 0.0
    # Prefer best-edge source flags; fall back to OR across sets
    if best is not None:
        slope_on, cci_on, rsi_on = float(best.slope_on), float(best.cci_on), float(best.rsi_on)
    else:
        slope_on = max((float(e.slope_on) for e in edges), default=0.0)
        cci_on = max((float(e.cci_on) for e in edges), default=0.0)
        rsi_on = max((float(e.rsi_on) for e in edges), default=0.0)
    return SymbolEdgeSnapshot(
        symbol=symbol,
        set_edges=edges,
        consensus_force=mean_force,
        best=best,
        multi_set_consensus=consensus,
        n_pullback=n_pb,
        n_continuation=n_ct,
        slope_on=slope_on,
        cci_on=cci_on,
        rsi_on=rsi_on,
    )


def count_actionable_side_agree(snap: SymbolEdgeSnapshot, act: str) -> int:
    """Count official sets that share actionable side (CASE-0005).

    Actionable = long|short act matching ``act``, htf_agree, topology in
    pullback_resume | continuation.
    """
    if act not in ("long", "short"):
        return 0
    return sum(
        1
        for e in snap.set_edges
        if e.act == act
        and e.htf_agree
        and e.topology in ("pullback_resume", "continuation")
    )


def side_permission_ok(
    snap: SymbolEdgeSnapshot,
    *,
    min_sets: int = 2,
    strong_force: float = 0.40,
) -> bool:
    """Multi-set side confluence gate (CASE-0005).

    Permission when:
      - ≥ min_sets official sets agree on best.act actionable side, OR
      - multi_set_consensus fully agrees with best.act AND |best.force| ≥ strong_force
        (flea-jar carve-out for high-force full consensus with single LTF timing).

    Single weak set never passes.
    """
    best = snap.best
    if best is None or best.act not in ("long", "short") or not best.htf_agree:
        return False
    n = count_actionable_side_agree(snap, best.act)
    if n >= min_sets:
        return True
    if abs(best.force) < strong_force:
        return False
    if best.act == "long" and snap.multi_set_consensus == "agree_long":
        return True
    if best.act == "short" and snap.multi_set_consensus == "agree_short":
        return True
    return False


def path_side_permission_ok(
    snap: SymbolEdgeSnapshot,
    *,
    min_sets: int = 2,
    strong_force: float = 0.40,
    pullback_force_min: float = 0.15,
) -> bool:
    """CASE-0010 path capacity: CASE-0005 gate OR pullback single-set carve-out.

    Pullback_resume with ≥1 actionable set, htf_agree, and |force|≥pullback_force_min
    is Mark LTF timing under A12 completed HTF — not multi-set thrash.
    Continuation does **not** get this carve-out (still multi-set / consensus).
    """
    if side_permission_ok(snap, min_sets=min_sets, strong_force=strong_force):
        return True
    best = snap.best
    if best is None or best.act not in ("long", "short") or not best.htf_agree:
        return False
    if best.topology != "pullback_resume":
        return False
    if abs(best.force) < float(pullback_force_min):
        return False
    return count_actionable_side_agree(snap, best.act) >= 1


def edge_to_set_confluence(snap: SymbolEdgeSnapshot):
    """Pack set edges into official SetConfluence map for Mark Channel1."""
    from .types import Direction, SetConfluence, VelocityStrength

    out = {}
    for e in snap.set_edges:
        if e.force > 0.15:
            d = Direction.BULL
        elif e.force < -0.15:
            d = Direction.BEAR
        else:
            d = Direction.NEUTRAL
        if e.topology in ("pullback_resume", "continuation"):
            vel = VelocityStrength.STRONG if abs(e.force) > 0.35 else VelocityStrength.MEDIUM
        elif e.topology == "slingshot_load":
            vel = VelocityStrength.WEAK
        else:
            vel = VelocityStrength.NONE
        out[e.set_id] = SetConfluence(
            set_key=f"official:{e.set_id}",
            direction=d,
            velocity=vel,
            n_bull=2 if d == Direction.BULL else 0,
            n_bear=2 if d == Direction.BEAR else 0,
            n_neutral=1,
        )
    return out


def edge_sensors(snap: SymbolEdgeSnapshot):
    """Role-port sensors for L2L day path from multi-set edge."""
    from .roles import SensorSpec

    f = snap.consensus_force
    best = snap.best
    v = 0.0
    if best is not None:
        # RSI normalized to [-1,1] around 50
        v = float(np.clip((best.ltf_rsi - 50.0) / 50.0, -1.0, 1.0))
        if best.act == "short":
            v = -abs(v) if best.topology != "chop" else v
        elif best.act == "long":
            v = abs(v)
    inn = f * 0.85
    return [
        SensorSpec("set_force_slow", "cci", "slow", f),
        SensorSpec("ltf_rsi_bb_fast", "rsi", "fast", v),
        SensorSpec("set_inertia_mid", "cci", "mid", inn),
    ]
