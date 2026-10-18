"""Teacher agents — each teaches the policy ONE lesson (Monty order).

Design (anti-thrash harness):
  - Each agent owns exactly one lesson: three pullback lessons + one
    lot-size-to-win-the-day lesson.
  - Lessons are harvested from REAL path states (thought-trace replay of the
    frozen champion) — never rebuilt synthetic states (F-025; the dynamic-size
    lab measured that synthetic-state teachers do not transfer).
  - Harvest window must PRECEDE the measurement window (no look-ahead).
  - Every agent trains its OWN candidate from a copy of the champion; agents
    never stack silently and never touch the champion npz.
  - The harness (tools/teacher_harness.py) measures every candidate on the
    same pinned 40d sensor and issues verdicts by the owner bar only
    (hits vs king, breach 0).

Agents:
  pullback_first       fire the edge side on plain HTF-agree first pullbacks
                       the brain waited on (conversion killer #1 in the map)
  pullback_confluence  fire multi-set-agree pullbacks with conviction size
  pullback_prime       fire London/NY prime-session pullbacks (A28 weighting)
  size_until_win       size head only: on real pullback fills, teach the
                       need-based fraction that wins the day
                       (remaining_goal / (expect_R x remaining_budget))
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .brain import MetaBrain
from .edge import build_tf_cache
from .goal_path import run_goal_path_day
from .policy import DEFAULT_CHAMPION_PATH, MetaPolicy

LAB_DIR = Path(__file__).resolve().parents[1] / "artifacts" / "policies_lab" / "teacher_agents"

Lesson = Dict[str, Any]  # {state, teacher_act, teacher_size_frac, weight, tag}


# ------------------------------------------------------------------ harvesting
def replay_traced_days(
    policy: MetaPolicy,
    *,
    symbol: str,
    m1: List[dict],
    dates: Sequence[str],
    pairs: Sequence[Tuple[float, float]],
    tf_cache: Optional[Dict[str, List[dict]]] = None,
) -> List[Dict[str, Any]]:
    """Observe-only traced replay of real days on the frozen policy."""
    cache = tf_cache or build_tf_cache(m1)
    days: List[Dict[str, Any]] = []
    for date, (t, r) in zip(dates, pairs):
        fills, ledger, meta = run_goal_path_day(
            policy,
            date=date,
            m1_by_symbol={symbol: m1},
            target_percent=float(t),
            max_daily_risk_percent=float(r),
            symbols=[symbol],
            tf_cache_by_symbol={symbol: cache},
            collect_thought_trace=True,
        )
        policy.assert_frozen()
        pnl = float(ledger.realized_pnl_percent)
        days.append(
            {
                "date": date,
                "target": float(t),
                "risk": float(r),
                "pnl": pnl,
                "hit": bool(pnl >= float(t) - 1e-9),
                "green": bool(pnl > 0),
                "trace": meta.get("thought_trace") or [],
            }
        )
    return days


def _decision_rows(day: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [t for t in day["trace"] if isinstance(t.get("brain"), dict) and t.get("state")]


# ------------------------------------------------------------- lesson builders
def harvest_pullback_first(days: Sequence[Dict[str, Any]]) -> List[Lesson]:
    """Brain waited on a plain HTF-agree pullback candidate → teach edge side."""
    out: List[Lesson] = []
    for d in days:
        for t in _decision_rows(d):
            if t["event"] != "brain_wait" or t["topology"] != "pullback_resume":
                continue
            side = t["edge"]["act"]
            if side not in ("long", "short"):
                continue
            w = 1.0 + 0.25 * min(int(t["edge"].get("n_htf_active") or 0), 3)
            out.append(
                {
                    "state": t["state"],
                    "teacher_act": side,
                    "teacher_size_frac": 0.55,
                    "weight": float(w),
                    "tag": f"{d['date']} {t['slot']} wait_on_pullback",
                }
            )
    return out


def harvest_pullback_confluence(days: Sequence[Dict[str, Any]]) -> List[Lesson]:
    """Multi-set-agree pullbacks (any brain outcome) → edge side, conviction size."""
    out: List[Lesson] = []
    for d in days:
        for t in _decision_rows(d):
            if t["topology"] != "pullback_resume":
                continue
            cons = str(t["edge"].get("consensus") or "")
            side = t["edge"]["act"]
            if cons not in ("agree_long", "agree_short") or side not in ("long", "short"):
                continue
            if (cons == "agree_long") != (side == "long"):
                continue
            out.append(
                {
                    "state": t["state"],
                    "teacher_act": side,
                    "teacher_size_frac": 0.72,
                    "weight": 1.5,
                    "tag": f"{d['date']} {t['slot']} confluence_{cons}",
                }
            )
    return out


def harvest_pullback_prime(days: Sequence[Dict[str, Any]]) -> List[Lesson]:
    """London/NY prime-slot pullbacks → edge side (A28: most activity, no excuse)."""
    out: List[Lesson] = []
    for d in days:
        for t in _decision_rows(d):
            if t["topology"] != "pullback_resume" or not t.get("prime"):
                continue
            side = t["edge"]["act"]
            if side not in ("long", "short"):
                continue
            out.append(
                {
                    "state": t["state"],
                    "teacher_act": side,
                    "teacher_size_frac": 0.65,
                    "weight": 1.5,
                    "tag": f"{d['date']} {t['slot']} prime",
                }
            )
    return out


def harvest_size_until_win(days: Sequence[Dict[str, Any]]) -> List[Lesson]:
    """Real pullback FILLS → size head learns the need-based winning fraction.

    teacher_size_frac = remaining_goal / (expect_R x remaining_budget), the
    fraction of remaining risk that clears the day at expect_R ~= 2 on a
    pullback leg. Green/hit days weight more (learn from what worked).
    """
    out: List[Lesson] = []
    for d in days:
        for t in _decision_rows(d):
            if t["event"] != "fired" or t["topology"] != "pullback_resume":
                continue
            ctx = t["ctx"]
            rem_goal = max(float(ctx["target"]) - float(ctx["pnl"]), 0.0)
            rem_risk = max(float(ctx["remaining"]), 1e-6)
            need_frac = float(np.clip(rem_goal / (2.0 * rem_risk), 0.10, 0.95))
            w = 1.0
            if d["hit"]:
                w = 2.0
            elif d["green"]:
                w = 1.4
            out.append(
                {
                    "state": t["state"],
                    "teacher_act": t["brain"]["act"],
                    "teacher_size_frac": need_frac,
                    "weight": float(w),
                    "tag": f"{d['date']} {t['slot']} need={need_frac:.2f}",
                }
            )
    return out


# ----------------------------------------------------------------- agent model
@dataclass
class TeacherAgent:
    name: str
    lesson: str
    harvest: Callable[[Sequence[Dict[str, Any]]], List[Lesson]]
    mode: str = "act_size"  # act_size | size_only
    size_head_drives: bool = False
    epochs: int = 6
    lr: float = 0.015


AGENT_REGISTRY: List[TeacherAgent] = [
    TeacherAgent(
        name="pullback_first",
        lesson="Fire the edge side on plain HTF-agree first pullbacks the brain waited on",
        harvest=harvest_pullback_first,
    ),
    TeacherAgent(
        name="pullback_confluence",
        lesson="Fire multi-set-agree pullbacks with conviction size",
        harvest=harvest_pullback_confluence,
    ),
    TeacherAgent(
        name="pullback_prime",
        lesson="Fire London/NY prime-session pullbacks (A28 weighting)",
        harvest=harvest_pullback_prime,
    ),
    TeacherAgent(
        name="size_until_win",
        lesson="Size head only: teach the need-based fraction that wins the day on real pullback fills",
        harvest=harvest_size_until_win,
        mode="size_only",
        size_head_drives=True,
    ),
]


def get_agent(name: str) -> TeacherAgent:
    for a in AGENT_REGISTRY:
        if a.name == name:
            return a
    raise KeyError(f"unknown teacher agent: {name} (have {[a.name for a in AGENT_REGISTRY]})")


# -------------------------------------------------------------------- training
def train_candidate(
    agent: TeacherAgent,
    lessons: Sequence[Lesson],
    *,
    champion_path: Optional[Path] = None,
    out_path: Optional[Path] = None,
    seed: int = 42,
) -> Dict[str, Any]:
    """Train ONE candidate from a champion copy with ONE agent's lessons."""
    if not lessons:
        return {"agent": agent.name, "error": "no_lessons_harvested", "n_lessons": 0}

    src = Path(champion_path) if champion_path else DEFAULT_CHAMPION_PATH
    out = Path(out_path) if out_path else (LAB_DIR / f"meta_policy_teacher_{agent.name}.npz")
    if out.resolve() == DEFAULT_CHAMPION_PATH.resolve():
        raise RuntimeError("FORBIDDEN: teacher agents may not overwrite the champion")

    pol = MetaPolicy.load(src, freeze=False)
    fp_before = pol.weight_fingerprint()

    def agreement() -> Dict[str, Any]:
        n_act = 0
        errs = []
        for l in lessons:
            st = np.asarray(l["state"], dtype=np.float64)
            act, size_logit, _ = pol.brain.predict_act(st)
            if act == l["teacher_act"]:
                n_act += 1
            if l["teacher_act"] != "wait":
                sig = 1.0 / (1.0 + np.exp(-size_logit))
                errs.append(abs(sig - float(l["teacher_size_frac"])))
        return {
            "act_agreement": round(n_act / len(lessons), 3),
            "size_mae": round(float(np.mean(errs)), 3) if errs else None,
        }

    before = agreement()
    rng = np.random.default_rng(seed)
    order = np.arange(len(lessons))
    size_only = agent.mode == "size_only"
    for ep in range(int(agent.epochs)):
        rng.shuffle(order)
        for i in order:
            l = lessons[int(i)]
            pol.brain.meta_update(
                np.asarray(l["state"], dtype=np.float64),
                teacher_act=str(l["teacher_act"]),
                lr=agent.lr * (0.9 ** ep),
                reward=float(l.get("weight") or 1.0),
                teacher_size_frac=(
                    float(l["teacher_size_frac"]) if l["teacher_act"] != "wait" else 0.0
                ),
                size_only=size_only,
            )
    after = agreement()

    pol.trained = True
    pol.size_head_drives = bool(agent.size_head_drives)
    pol.freeze_for_inference()
    out.parent.mkdir(parents=True, exist_ok=True)
    pol.save(out)
    return {
        "agent": agent.name,
        "lesson": agent.lesson,
        "mode": agent.mode,
        "size_head_drives": bool(agent.size_head_drives),
        "n_lessons": len(lessons),
        "epochs": int(agent.epochs),
        "warm_start": str(src),
        "fingerprint_before": fp_before,
        "fingerprint_after": pol.weight_fingerprint(),
        "agreement_before": before,
        "agreement_after": after,
        "saved": str(out),
    }
