"""Opportunity Watch Agent (Law A28) — always-on miss detector.

Watches official Mark sets: HTF trending + LTF RSI5/BB10 pullback or continuation.
If opportunity exists and bot did not fire matching side → complaint
(how should the bot sense this next time?).

London/NY session band is highest-activity priority.
Multiple complaints per scan/case are normal.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .edge import SetEdge, SymbolEdgeSnapshot, scan_all_sets
from .sets import OFFICIAL_SETS

# London–NY active band (UTC-style clock strings as used in goal_path slots)
# Covers London open through NY afternoon activity (hint: most activity here).
LONDON_NY_START = "07:00:00"
LONDON_NY_END = "17:00:00"

ACTIONABLE = frozenset({"pullback_resume", "continuation"})


@dataclass
class OpportunityComplaint:
    """One miss: opportunity existed; bot did not take it."""

    complaint_id: str
    asof_date: str
    asof_time: str
    symbol: str
    set_id: int
    set_name: str
    topology: str  # pullback_resume | continuation
    side: str  # long | short
    force: float
    session_band: str  # london_ny | other
    sense_gap: str  # sight | feel | taste | hearing | sight+feel | ...
    what_bot_did: str  # wait | skipped | wrong_side | none
    how_to_sense_next: str
    htf_agree: bool = True
    reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OpportunityWatchReport:
    """Full scan result for one decision time."""

    n_opportunities: int = 0
    n_misses: int = 0
    n_hits: int = 0
    n_london_ny_misses: int = 0
    complaints: List[OpportunityComplaint] = field(default_factory=list)
    opportunities: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_opportunities": self.n_opportunities,
            "n_misses": self.n_misses,
            "n_hits": self.n_hits,
            "n_london_ny_misses": self.n_london_ny_misses,
            "complaints": [c.to_dict() for c in self.complaints],
            "opportunities": list(self.opportunities),
        }


def is_london_ny_session(asof_time: str) -> bool:
    """True if decision time is in the high-activity London/NY band."""
    t = str(asof_time or "00:00:00")
    if len(t) == 5:
        t = t + ":00"
    return LONDON_NY_START <= t < LONDON_NY_END


def session_band(asof_time: str) -> str:
    return "london_ny" if is_london_ny_session(asof_time) else "other"


def _sense_gap_for_topology(topology: str, what_bot_did: str) -> str:
    if topology == "pullback_resume" and what_bot_did == "wait":
        return "sight+feel"  # missed resume after load
    if topology == "continuation" and what_bot_did in ("wait", "skipped"):
        return "sight+hearing"  # missed active-session continuation
    if what_bot_did == "wrong_side":
        return "sight"
    if what_bot_did == "skipped":
        return "taste"  # saw something but filters/size killed it
    return "sight"


def _how_to_sense_next(
    topology: str,
    sense_gap: str,
    session: str,
) -> str:
    parts = [
        f"Sense {sense_gap}: HTF force clear + LTF RSI5/BB10 {topology} on set entry TF.",
    ]
    if session == "london_ny":
        parts.append(
            "Priority: London/NY high-activity band — do not sleep through PB/cont here."
        )
    if "feel" in sense_gap:
        parts.append("Feel load→resume: dipped-against-force then resume with force.")
    if "hearing" in sense_gap:
        parts.append("Hear session/regime: active session + trend day favors continuation density.")
    if "taste" in sense_gap:
        parts.append("Taste: if edge real, do not over-filter; size under remaining risk toward goal.")
    parts.append("Long-term: convert repeated misses into sense weights, not one-off pads.")
    return " ".join(parts)


def edge_is_opportunity(edge: SetEdge) -> bool:
    """Canonical A28 opportunity: HTF agree + PB or cont + long/short."""
    if not edge.htf_agree:
        return False
    if edge.topology not in ACTIONABLE:
        return False
    if edge.act not in ("long", "short"):
        return False
    if abs(float(edge.force)) < 0.15:
        return False
    return True


def classify_bot_response(
    *,
    opportunity_side: str,
    bot_act: Optional[str],
    bot_fired: bool,
) -> str:
    """what_bot_did for complaint."""
    if not bot_fired or not bot_act or bot_act == "wait":
        return "wait" if bot_act == "wait" or not bot_act else "none"
    if bot_act in ("long", "short") and bot_act != opportunity_side:
        return "wrong_side"
    if bot_act == opportunity_side:
        return "taken"
    return "skipped"


class OpportunityWatchAgent:
    """Always-on agent (A28). Does not place trades; emits complaints on misses."""

    def __init__(self, *, agent_id: str = "opportunity_watch_v1") -> None:
        self.agent_id = agent_id
        self._complaint_seq = 0

    def _next_id(self, date: str, time: str) -> str:
        self._complaint_seq += 1
        return f"OW-{date}-{time}-{self._complaint_seq:04d}"

    def scan_snapshot(
        self,
        snap: SymbolEdgeSnapshot,
        *,
        asof_date: str,
        asof_time: str,
        bot_act: Optional[str] = None,
        bot_fired: bool = False,
        bot_symbol: Optional[str] = None,
    ) -> OpportunityWatchReport:
        """Compare Mark opportunities on this symbol vs what the bot did."""
        report = OpportunityWatchReport()
        band = session_band(asof_time)
        sym = snap.symbol

        for edge in snap.set_edges:
            if not edge_is_opportunity(edge):
                continue
            report.n_opportunities += 1
            opp = {
                "symbol": sym,
                "set_id": edge.set_id,
                "set_name": edge.name,
                "topology": edge.topology,
                "side": edge.act,
                "force": float(edge.force),
                "session_band": band,
            }
            report.opportunities.append(opp)

            # Hit: bot fired matching side on this symbol (path takes one best often)
            taken = (
                bot_fired
                and bot_act == edge.act
                and (bot_symbol is None or bot_symbol == sym)
            )
            if taken:
                report.n_hits += 1
                continue

            what = classify_bot_response(
                opportunity_side=edge.act,
                bot_act=bot_act,
                bot_fired=bot_fired and (bot_symbol is None or bot_symbol == sym),
            )
            if what == "taken":
                report.n_hits += 1
                continue

            # Miss → complaint
            gap = _sense_gap_for_topology(edge.topology, what)
            how = _how_to_sense_next(edge.topology, gap, band)
            c = OpportunityComplaint(
                complaint_id=self._next_id(asof_date, asof_time),
                asof_date=asof_date,
                asof_time=asof_time,
                symbol=sym,
                set_id=int(edge.set_id),
                set_name=str(edge.name),
                topology=str(edge.topology),
                side=str(edge.act),
                force=float(edge.force),
                session_band=band,
                sense_gap=gap,
                what_bot_did=what,
                how_to_sense_next=how,
                htf_agree=bool(edge.htf_agree),
                reason=str(edge.reason),
            )
            report.complaints.append(c)
            report.n_misses += 1
            if band == "london_ny":
                report.n_london_ny_misses += 1

        return report

    def scan_at_decision(
        self,
        *,
        symbol: str,
        m1_bars: Sequence[dict],
        asof_date: str,
        asof_time: str,
        tf_cache: Optional[Dict[str, List[dict]]] = None,
        bot_act: Optional[str] = None,
        bot_fired: bool = False,
    ) -> OpportunityWatchReport:
        """Scan all official sets for one symbol at a decision clock."""
        snap = scan_all_sets(
            list(m1_bars),
            symbol=symbol,
            tf_cache=tf_cache,
            asof_date=asof_date,
            asof_time=asof_time,
        )
        return self.scan_snapshot(
            snap,
            asof_date=asof_date,
            asof_time=asof_time,
            bot_act=bot_act,
            bot_fired=bot_fired,
            bot_symbol=symbol if bot_fired else None,
        )

    def merge_reports(
        self, reports: Sequence[OpportunityWatchReport]
    ) -> OpportunityWatchReport:
        """Combine multi-symbol / multi-slot scans (multi-complaint cases)."""
        out = OpportunityWatchReport()
        for r in reports:
            out.n_opportunities += r.n_opportunities
            out.n_misses += r.n_misses
            out.n_hits += r.n_hits
            out.n_london_ny_misses += r.n_london_ny_misses
            out.complaints.extend(r.complaints)
            out.opportunities.extend(r.opportunities)
        return out


# Module-level always-on singleton (permanent agent)
ALWAYS_ON_WATCH = OpportunityWatchAgent()


def watch_misses(
    *,
    symbol: str,
    m1_bars: Sequence[dict],
    asof_date: str,
    asof_time: str,
    bot_act: Optional[str] = None,
    bot_fired: bool = False,
    tf_cache: Optional[Dict[str, List[dict]]] = None,
    agent: Optional[OpportunityWatchAgent] = None,
) -> OpportunityWatchReport:
    """Convenience: always-on scan."""
    ag = agent or ALWAYS_ON_WATCH
    return ag.scan_at_decision(
        symbol=symbol,
        m1_bars=m1_bars,
        asof_date=asof_date,
        asof_time=asof_time,
        tf_cache=tf_cache,
        bot_act=bot_act,
        bot_fired=bot_fired,
    )
