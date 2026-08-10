"""Trade Mental Replay — Policy self-observation across 3 TFs × 3 phases.

Personified Policy journal (lab / offline):
  BEFORE  entry setup on set stack (LTF + HTF1 + HTF2)
  DURING  mid-hold geometry (same stack, no look-ahead past asof)
  AFTER   exit + outcome tag (conversion teacher source)

Closes the path-state gap: not only fire-side misses, but full trade life.
Does **not** retrain at inference (A14). Teachers are offline-only.
Optional cv2 chart annotate for evidence screenshots (not the edge engine).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np

from .opportunity_watch import session_band
from .sets import MARK_SETS_LAW, OFFICIAL_SETS
from .state import META_RL_DIM

PHASES: Tuple[str, ...] = ("before", "during", "after")
TF_ROLES: Tuple[str, ...] = ("ltf", "htf1", "htf2")

# Outcome tags (AFTER chapter)
OUTCOME_CLEAR = "clear"  # meaningful progress toward target
OUTCOME_PROGRESS = "progress"  # green but thin
OUTCOME_DEAD = "dead"  # loss / force died against side
OUTCOME_THRASH = "thrash"  # noise flip / conflict after fire
OUTCOME_SCRATCH = "scratch"  # near-flat

# Teacher hints for offline conversion (Counsel / Teacher channel)
HINT_HOLD_MORE = "hold_more"
HINT_WAIT_DEAD = "wait_dead"
HINT_SIZE_OK = "size_ok"
HINT_THRASH_EXIT = "thrash_exit"
HINT_GOOD_EXIT = "good_exit"
HINT_GOOD_FIRE = "good_fire"


def set_stack(set_id: int) -> Tuple[str, str, str]:
    """Return (ltf, htf1, htf2) for an official Mark set."""
    for s in OFFICIAL_SETS:
        if int(s.set_id) == int(set_id):
            return s.tfs
    # Fallback set1
    return ("1m", "15m", "30m")


def set_name(set_id: int) -> str:
    for s in OFFICIAL_SETS:
        if int(s.set_id) == int(set_id):
            return str(s.name)
    return "unknown"


def mid_time(start: str, end: str) -> str:
    """Midpoint clock between two HH:MM:SS strings (same day)."""

    def _sec(t: str) -> int:
        parts = str(t).split(":")
        try:
            h = int(parts[0])
            m = int(parts[1]) if len(parts) > 1 else 0
            s = int(float(parts[2])) if len(parts) > 2 else 0
        except (TypeError, ValueError, IndexError):
            return 0
        return h * 3600 + m * 60 + s

    a, b = _sec(start), _sec(end)
    if b <= a:
        b = a + 60
    mid = (a + b) // 2
    hh, rem = divmod(mid, 3600)
    mm, ss = divmod(rem, 60)
    return f"{hh:02d}:{mm:02d}:{ss:02d}"


def _sign(x: float) -> int:
    if x > 1e-9:
        return 1
    if x < -1e-9:
        return -1
    return 0


def _state_fingerprint(state: Optional[Sequence[float] | np.ndarray]) -> str:
    if state is None:
        return ""
    arr = np.asarray(state, dtype=np.float32).ravel()
    if arr.size == 0:
        return ""
    return hashlib.sha256(arr.tobytes()).hexdigest()[:16]


@dataclass
class TfFrame:
    """One timeframe cell in the 3×3 mental grid."""

    role: str  # ltf | htf1 | htf2
    tf: str
    force: float = 0.0
    ltf_rsi: float = 50.0
    topology: str = "chop"
    act: str = "wait"
    htf_agree: bool = False
    reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PhaseTape:
    """One phase (before | during | after) across the set's three TFs."""

    phase: str
    asof_date: str
    asof_time: str
    set_id: int
    set_name: str
    multi_set_consensus: str
    consensus_force: float
    frames: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    brain_act: str = "wait"
    sense_summary: Dict[str, Any] = field(default_factory=dict)
    progress_to_target: float = 0.0
    realized_risk_percent: float = 0.0
    state_fp: str = ""
    # Optional full packed state (BEFORE preferred for offline teachers)
    packed_state: Optional[List[float]] = None

    def to_dict(self, *, include_state: bool = True) -> Dict[str, Any]:
        d = {
            "phase": self.phase,
            "asof_date": self.asof_date,
            "asof_time": self.asof_time,
            "set_id": int(self.set_id),
            "set_name": self.set_name,
            "multi_set_consensus": self.multi_set_consensus,
            "consensus_force": float(self.consensus_force),
            "frames": dict(self.frames),
            "brain_act": self.brain_act,
            "sense_summary": dict(self.sense_summary),
            "progress_to_target": float(self.progress_to_target),
            "realized_risk_percent": float(self.realized_risk_percent),
            "state_fp": self.state_fp,
        }
        if include_state and self.packed_state is not None:
            d["packed_state"] = list(self.packed_state)
        return d


@dataclass
class TradeMentalReplay:
    """Full trade life: 3 phases × 3 TFs + outcome + Policy first-person."""

    trade_id: str
    symbol: str
    date: str
    session_band: str
    side: str
    size_risk_percent: float
    entry_slot: str
    exit_time: str
    topology: str
    set_id: int
    set_name: str
    pnl_percent: float
    before: PhaseTape
    during: PhaseTape
    after: PhaseTape
    outcome_tag: str
    teacher_hint: str
    first_person: str
    multi_set_consensus_entry: str = ""
    n_htf_active_entry: int = 0
    lot: float = 0.0
    source: str = "trade_mental_replay"

    def to_dict(self, *, include_state: bool = True) -> Dict[str, Any]:
        return {
            "trade_id": self.trade_id,
            "symbol": self.symbol,
            "date": self.date,
            "session_band": self.session_band,
            "side": self.side,
            "size_risk_percent": float(self.size_risk_percent),
            "entry_slot": self.entry_slot,
            "exit_time": self.exit_time,
            "topology": self.topology,
            "set_id": int(self.set_id),
            "set_name": self.set_name,
            "pnl_percent": float(self.pnl_percent),
            "before": self.before.to_dict(include_state=include_state),
            "during": self.during.to_dict(include_state=include_state),
            "after": self.after.to_dict(include_state=include_state),
            "outcome_tag": self.outcome_tag,
            "teacher_hint": self.teacher_hint,
            "first_person": self.first_person,
            "multi_set_consensus_entry": self.multi_set_consensus_entry,
            "n_htf_active_entry": int(self.n_htf_active_entry),
            "lot": float(self.lot),
            "source": self.source,
            "grid": "3tf_x_3phase",
        }

    def grid_summary(self) -> Dict[str, Dict[str, str]]:
        """Compact 3×3 mental grid: phase → role → short label."""
        out: Dict[str, Dict[str, str]] = {}
        for phase_name, tape in (
            ("before", self.before),
            ("during", self.during),
            ("after", self.after),
        ):
            row: Dict[str, str] = {}
            for role in TF_ROLES:
                fr = tape.frames.get(role) or {}
                topo = str(fr.get("topology") or "?")
                force = float(fr.get("force") or 0.0)
                if role == "ltf":
                    row[role] = f"{topo}|rsi={float(fr.get('ltf_rsi') or 50):.0f}"
                else:
                    agree = "Y" if fr.get("htf_agree") else "n"
                    row[role] = f"f={force:+.2f}|{agree}|{topo}"
            out[phase_name] = row
        return out


def frames_from_set_edge(
    edge: Any,
    set_id: int,
) -> Dict[str, Dict[str, Any]]:
    """Build LTF/HTF1/HTF2 frames from one SetEdge (+ stack names).

    SetEdge carries aggregated force + LTF timing. HTF1/HTF2 share force/agree
    (Mark permission is joint HTF); LTF carries RSI + topology timing.
    """
    ltf, h1, h2 = set_stack(int(set_id))
    force = float(getattr(edge, "force", 0.0) or 0.0)
    rsi_v = float(getattr(edge, "ltf_rsi", 50.0) or 50.0)
    topo = str(getattr(edge, "topology", "chop") or "chop")
    act = str(getattr(edge, "act", "wait") or "wait")
    agree = bool(getattr(edge, "htf_agree", False))
    reason = str(getattr(edge, "reason", "") or "")
    return {
        "ltf": TfFrame(
            role="ltf",
            tf=ltf,
            force=0.0,
            ltf_rsi=rsi_v,
            topology=topo,
            act=act,
            htf_agree=agree,
            reason=reason,
        ).to_dict(),
        "htf1": TfFrame(
            role="htf1",
            tf=h1,
            force=force,
            ltf_rsi=rsi_v,
            topology=topo if agree else "no_permission",
            act=act if agree else "wait",
            htf_agree=agree,
            reason="htf1_confirm",
        ).to_dict(),
        "htf2": TfFrame(
            role="htf2",
            tf=h2,
            force=force,
            ltf_rsi=rsi_v,
            topology=topo if agree else "no_permission",
            act=act if agree else "wait",
            htf_agree=agree,
            reason="htf2_confirm",
        ).to_dict(),
    }


def sense_summary_from_report(sense_rep: Any) -> Dict[str, Any]:
    if sense_rep is None:
        return {}
    sight = getattr(sense_rep, "sight", None) or {}
    feel = getattr(sense_rep, "feel", None) or {}
    taste = getattr(sense_rep, "taste", None) or {}
    hearing = getattr(sense_rep, "hearing", None) or {}
    return {
        "sight_topology": sight.get("topology_class") if isinstance(sight, dict) else None,
        # Sense probe key may still say load_building in code; journal language = pullback tension
        "feel_tension": feel.get("max_tension_load_building") if isinstance(feel, dict) else None,
        "taste_edge": taste.get("edge_quality") if isinstance(taste, dict) else None,
        "hearing_wait": hearing.get("wait_subtype") if isinstance(hearing, dict) else None,
        "multi_set": sight.get("multi_set_consensus") if isinstance(sight, dict) else None,
    }


def phase_tape_from_snap(
    snap: Any,
    *,
    phase: str,
    set_id: int,
    asof_date: str,
    asof_time: str,
    brain_act: str = "wait",
    sense_rep: Any = None,
    progress_to_target: float = 0.0,
    realized_risk_percent: float = 0.0,
    packed_state: Optional[Sequence[float] | np.ndarray] = None,
) -> PhaseTape:
    """Build one phase tape from a SymbolEdgeSnapshot."""
    sid = int(set_id) if set_id else 0
    edge = None
    if snap is not None:
        for e in getattr(snap, "set_edges", None) or []:
            if int(getattr(e, "set_id", 0) or 0) == sid:
                edge = e
                break
        if edge is None:
            edge = getattr(snap, "best", None)
            if edge is not None:
                sid = int(getattr(edge, "set_id", sid) or sid)
    if edge is None:
        frames = {
            r: TfFrame(role=r, tf=set_stack(sid or 1)[i]).to_dict()
            for i, r in enumerate(TF_ROLES)
        }
        force = 0.0
        consensus = "incomplete"
    else:
        frames = frames_from_set_edge(edge, sid or int(getattr(edge, "set_id", 1) or 1))
        force = float(getattr(snap, "consensus_force", 0.0) or 0.0)
        consensus = str(getattr(snap, "multi_set_consensus", "incomplete") or "incomplete")

    st_list: Optional[List[float]] = None
    if packed_state is not None:
        arr = np.asarray(packed_state, dtype=np.float64).ravel()
        if arr.size == META_RL_DIM and np.all(np.isfinite(arr)):
            st_list = [float(x) for x in arr]

    return PhaseTape(
        phase=str(phase),
        asof_date=str(asof_date),
        asof_time=str(asof_time),
        set_id=int(sid or 1),
        set_name=set_name(sid or 1),
        multi_set_consensus=consensus,
        consensus_force=float(force),
        frames=frames,
        brain_act=str(brain_act or "wait"),
        sense_summary=sense_summary_from_report(sense_rep),
        progress_to_target=float(progress_to_target),
        realized_risk_percent=float(realized_risk_percent),
        state_fp=_state_fingerprint(st_list),
        packed_state=st_list,
    )


def classify_outcome(
    *,
    side: str,
    pnl_percent: float,
    size_risk_percent: float,
    before_force: float,
    after_force: float,
    after_consensus: str,
    progress_after: float,
) -> Tuple[str, str]:
    """Return (outcome_tag, teacher_hint) from trade result + force continuity."""
    pnl = float(pnl_percent)
    size = max(float(size_risk_percent), 1e-6)
    r_mult = pnl / size  # rough R multiple of risk ticket
    side_s = 1 if str(side) == "long" else (-1 if str(side) == "short" else 0)
    force_with = side_s != 0 and _sign(after_force) == side_s and abs(after_force) >= 0.12
    force_against = side_s != 0 and _sign(after_force) == -side_s and abs(after_force) >= 0.15
    conflict = str(after_consensus) == "conflict"

    if conflict and abs(pnl) < 0.05 * size:
        return OUTCOME_THRASH, HINT_THRASH_EXIT
    if abs(pnl) < 0.03 * size:
        return OUTCOME_SCRATCH, HINT_GOOD_EXIT if force_with else HINT_WAIT_DEAD
    if pnl < 0:
        if force_against or conflict:
            return OUTCOME_DEAD, HINT_WAIT_DEAD
        return OUTCOME_DEAD, HINT_THRASH_EXIT
    # green
    if progress_after >= 0.35 or r_mult >= 1.5:
        return OUTCOME_CLEAR, HINT_GOOD_FIRE if r_mult >= 1.0 else HINT_SIZE_OK
    if force_with and r_mult < 0.6:
        return OUTCOME_PROGRESS, HINT_HOLD_MORE
    if force_with:
        return OUTCOME_PROGRESS, HINT_SIZE_OK
    return OUTCOME_PROGRESS, HINT_GOOD_EXIT


def first_person_journal(card_bits: Mapping[str, Any]) -> str:
    """Policy speaks in first person about the 3×3 tape."""
    side = str(card_bits.get("side") or "?")
    sym = str(card_bits.get("symbol") or "?")
    topo = str(card_bits.get("topology") or "?")
    set_id = int(card_bits.get("set_id") or 0)
    sn = str(card_bits.get("set_name") or set_name(set_id))
    ltf, h1, h2 = set_stack(set_id or 1)
    pnl = float(card_bits.get("pnl_percent") or 0.0)
    outcome = str(card_bits.get("outcome_tag") or "?")
    hint = str(card_bits.get("teacher_hint") or "?")
    before = card_bits.get("before") or {}
    during = card_bits.get("during") or {}
    after = card_bits.get("after") or {}

    def _ltf_line(tape: Mapping[str, Any]) -> str:
        fr = (tape.get("frames") or {}).get("ltf") or {}
        return f"{fr.get('topology', '?')} rsi={float(fr.get('ltf_rsi') or 50):.0f}"

    def _htf_line(tape: Mapping[str, Any]) -> str:
        f1 = (tape.get("frames") or {}).get("htf1") or {}
        return (
            f"force={float(f1.get('force') or 0):+.2f} "
            f"agree={'Y' if f1.get('htf_agree') else 'n'} "
            f"multi={tape.get('multi_set_consensus', '?')}"
        )

    return (
        f"I fired {side} on {sym} set{set_id}({sn}: {ltf}/{h1}/{h2}) "
        f"as {topo}.\n"
        f"BEFORE: LTF {_ltf_line(before)}; HTF {_htf_line(before)}.\n"
        f"DURING: LTF {_ltf_line(during)}; HTF {_htf_line(during)}.\n"
        f"AFTER:  LTF {_ltf_line(after)}; HTF {_htf_line(after)}.\n"
        f"Result pnl={pnl:+.3f}% → outcome={outcome}; I should learn: {hint}."
    )


def build_trade_mental_replay(
    *,
    trade_index: int,
    symbol: str,
    date: str,
    side: str,
    size_risk_percent: float,
    entry_slot: str,
    exit_time: str,
    topology: str,
    set_id: int,
    pnl_percent: float,
    before_snap: Any,
    during_snap: Any,
    after_snap: Any,
    brain_act: str,
    sense_rep_before: Any = None,
    sense_rep_during: Any = None,
    sense_rep_after: Any = None,
    progress_before: float = 0.0,
    progress_after: float = 0.0,
    risk_before: float = 0.0,
    risk_after: float = 0.0,
    packed_state_before: Optional[Sequence[float] | np.ndarray] = None,
    lot: float = 0.0,
    n_htf_active: int = 0,
) -> TradeMentalReplay:
    """Assemble full mental replay card for one closed leg."""
    sid = int(set_id) if set_id else 1
    if not set_id and before_snap is not None and getattr(before_snap, "best", None):
        sid = int(getattr(before_snap.best, "set_id", 1) or 1)

    before = phase_tape_from_snap(
        before_snap,
        phase="before",
        set_id=sid,
        asof_date=date,
        asof_time=entry_slot,
        brain_act=brain_act,
        sense_rep=sense_rep_before,
        progress_to_target=progress_before,
        realized_risk_percent=risk_before,
        packed_state=packed_state_before,
    )
    mid_t = mid_time(entry_slot, exit_time)
    during = phase_tape_from_snap(
        during_snap,
        phase="during",
        set_id=sid,
        asof_date=date,
        asof_time=mid_t,
        brain_act=brain_act,
        sense_rep=sense_rep_during,
        progress_to_target=progress_before,  # mid approx
        realized_risk_percent=risk_before,
        packed_state=None,
    )
    after = phase_tape_from_snap(
        after_snap,
        phase="after",
        set_id=sid,
        asof_date=date,
        asof_time=exit_time,
        brain_act="flat",
        sense_rep=sense_rep_after,
        progress_to_target=progress_after,
        realized_risk_percent=risk_after,
        packed_state=None,
    )

    b_force = float(
        ((before.frames.get("htf1") or {}).get("force"))
        or before.consensus_force
        or 0.0
    )
    a_force = float(
        ((after.frames.get("htf1") or {}).get("force"))
        or after.consensus_force
        or 0.0
    )
    outcome, hint = classify_outcome(
        side=side,
        pnl_percent=pnl_percent,
        size_risk_percent=size_risk_percent,
        before_force=b_force,
        after_force=a_force,
        after_consensus=after.multi_set_consensus,
        progress_after=progress_after,
    )
    band = session_band(entry_slot)
    trade_id = f"{date}|{symbol}|{entry_slot}|{trade_index}"
    bits = {
        "side": side,
        "symbol": symbol,
        "topology": topology,
        "set_id": sid,
        "set_name": set_name(sid),
        "pnl_percent": pnl_percent,
        "outcome_tag": outcome,
        "teacher_hint": hint,
        "before": before.to_dict(include_state=False),
        "during": during.to_dict(include_state=False),
        "after": after.to_dict(include_state=False),
    }
    journal = first_person_journal(bits)
    return TradeMentalReplay(
        trade_id=trade_id,
        symbol=str(symbol),
        date=str(date),
        session_band=str(band),
        side=str(side),
        size_risk_percent=float(size_risk_percent),
        entry_slot=str(entry_slot),
        exit_time=str(exit_time),
        topology=str(topology),
        set_id=sid,
        set_name=set_name(sid),
        pnl_percent=float(pnl_percent),
        before=before,
        during=during,
        after=after,
        outcome_tag=outcome,
        teacher_hint=hint,
        first_person=journal,
        multi_set_consensus_entry=before.multi_set_consensus,
        n_htf_active_entry=int(n_htf_active),
        lot=float(lot),
    )


def teachers_from_mental_replay(
    card: TradeMentalReplay,
    *,
    include_fire_anchor: bool = True,
) -> List[Dict[str, Any]]:
    """Offline teacher rows from a mental replay (anti F-025: real packed state).

    - Fire anchor: BEFORE packed state → side (sparse density anchor)
    - Conversion: BEFORE packed state → wait when dead/thrash; keep side on hold/good
    """
    out: List[Dict[str, Any]] = []
    st = card.before.packed_state
    if st is None:
        return out
    arr = np.asarray(st, dtype=np.float64).ravel()
    if arr.size != META_RL_DIM or not np.all(np.isfinite(arr)):
        return out

    band = card.session_band
    w = 1.0 + 0.25 * float(card.n_htf_active_entry)
    if band == "london_ny":
        w += 0.5
    # Outcome weight: conversion lessons matter more than pure fire copy
    if card.outcome_tag in (OUTCOME_DEAD, OUTCOME_THRASH):
        w += 0.35
    elif card.outcome_tag == OUTCOME_CLEAR:
        w += 0.25

    base = {
        "state": [float(x) for x in arr],
        "topology": card.topology,
        "session_band": band,
        "weight": float(w),
        "symbol": card.symbol,
        "asof_date": card.date,
        "asof_time": card.entry_slot,
        "force": float((card.before.frames.get("htf1") or {}).get("force") or 0.0),
        "what_bot_did": card.side,
        "multi_set_consensus": card.multi_set_consensus_entry,
        "n_htf_active": int(card.n_htf_active_entry),
        "htf_active": int(card.n_htf_active_entry) >= 1,
        "set_id": int(card.set_id),
        "trade_id": card.trade_id,
        "outcome_tag": card.outcome_tag,
        "teacher_hint": card.teacher_hint,
        "pnl_percent": float(card.pnl_percent),
        "phase": "before",
        "grid": "3tf_x_3phase",
    }

    hint = card.teacher_hint
    if hint in (HINT_WAIT_DEAD, HINT_THRASH_EXIT) and card.pnl_percent < 0:
        row = dict(base)
        row["teacher_act"] = "wait"
        row["source"] = "path_state_mental_replay_dead"
        row["teacher_size_frac"] = 0.0
        out.append(row)
    elif hint == HINT_HOLD_MORE and card.pnl_percent > 0:
        # Keep side — conversion is hold narrative; fire side still correct
        if include_fire_anchor:
            row = dict(base)
            row["teacher_act"] = card.side
            row["source"] = "path_state_mental_replay_hold"
            row["teacher_size_frac"] = 0.75
            out.append(row)
    elif include_fire_anchor and card.side in ("long", "short"):
        if card.topology in ("pullback_resume", "continuation"):
            row = dict(base)
            row["teacher_act"] = card.side
            if card.outcome_tag == OUTCOME_CLEAR:
                row["source"] = "path_state_mental_replay_clear"
            else:
                row["source"] = "path_state_mental_replay"
            t_norm = 0.5  # size frac mid; path harvest may re-weight
            row["teacher_size_frac"] = float(
                np.clip(0.55 + 0.2 * t_norm + (0.1 if band == "london_ny" else 0.0), 0.25, 0.95)
            )
            out.append(row)
    return out


def save_mental_replay_pack(
    cards: Sequence[TradeMentalReplay | Mapping[str, Any]],
    path: str | Path,
    *,
    include_state: bool = False,
) -> Path:
    """Write journal pack JSON (compact by default — no full states)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for c in cards:
        if isinstance(c, TradeMentalReplay):
            rows.append(c.to_dict(include_state=include_state))
        else:
            rows.append(dict(c))
    payload = {
        "schema": "trade_mental_replay_v1",
        "n": len(rows),
        "grid": "3tf_x_3phase",
        "phases": list(PHASES),
        "tf_roles": list(TF_ROLES),
        "mark_sets": [list(x) for x in MARK_SETS_LAW],
        "cards": rows,
    }
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return p


def annotate_chart_png(
    image_path: str | Path,
    card: TradeMentalReplay | Mapping[str, Any],
    out_path: str | Path,
    *,
    title: Optional[str] = None,
) -> Path:
    """Draw mental-replay HUD on a chart screenshot (cv2). Evidence only."""
    import cv2  # opencv-python-headless

    src = Path(image_path)
    dst = Path(out_path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    img = cv2.imread(str(src))
    if img is None:
        raise FileNotFoundError(f"cannot read image: {src}")

    if isinstance(card, TradeMentalReplay):
        d = card.to_dict(include_state=False)
        grid = card.grid_summary()
        fp = card.first_person
    else:
        d = dict(card)
        # rebuild grid lightly
        grid = {}
        for ph in PHASES:
            tape = d.get(ph) or {}
            row = {}
            for role in TF_ROLES:
                fr = (tape.get("frames") or {}).get(role) or {}
                if role == "ltf":
                    row[role] = f"{fr.get('topology', '?')}"
                else:
                    row[role] = f"f={float(fr.get('force') or 0):+.2f}"
            grid[ph] = row
        fp = str(d.get("first_person") or "")

    h, w = img.shape[:2]
    overlay = img.copy()
    # top banner
    cv2.rectangle(overlay, (0, 0), (w, min(140, h // 3)), (20, 20, 20), -1)
    img = cv2.addWeighted(overlay, 0.55, img, 0.45, 0)

    hdr = title or (
        f"TMR {d.get('trade_id', '')} | {d.get('side')} {d.get('symbol')} "
        f"set{d.get('set_id')} | pnl={float(d.get('pnl_percent') or 0):+.3f}% "
        f"| {d.get('outcome_tag')} → {d.get('teacher_hint')}"
    )
    y = 22
    cv2.putText(
        img, hdr[:120], (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 240, 240), 1, cv2.LINE_AA
    )
    y += 22
    for ph in PHASES:
        row = grid.get(ph) or {}
        line = f"{ph.upper():6s} LTF={row.get('ltf', '?')} | HTF1={row.get('htf1', '?')} | HTF2={row.get('htf2', '?')}"
        cv2.putText(
            img, line[:140], (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 220, 255), 1, cv2.LINE_AA
        )
        y += 18
    # footer first-person (wrap one line)
    foot = fp.replace("\n", " | ")[:160]
    cv2.putText(
        img,
        foot,
        (10, min(h - 12, y + 8)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (200, 200, 160),
        1,
        cv2.LINE_AA,
    )
    cv2.imwrite(str(dst), img)
    return dst


def mental_replay_layout() -> Dict[str, Any]:
    return {
        "schema": "trade_mental_replay_v1",
        "phases": list(PHASES),
        "tf_roles": list(TF_ROLES),
        "sets": mark_sets_brief(),
        "gap_closed": [
            "trade_lifecycle_package",
            "before_during_after_tape",
            "three_tf_per_set",
            "outcome_teacher_hints",
            "policy_first_person_journal",
            "optional_cv2_chart_annotate",
        ],
        "not_production_promote": True,
        "offline_teachers_only": True,
    }


def mark_sets_brief() -> List[Dict[str, Any]]:
    return [
        {
            "set_id": s.set_id,
            "name": s.name,
            "stack": list(s.tfs),
            "roles": {"ltf": s.entry_tf, "htf1": s.confirmation_tfs[0], "htf2": s.confirmation_tfs[1]},
        }
        for s in OFFICIAL_SETS
    ]
