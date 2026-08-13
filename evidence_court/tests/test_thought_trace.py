"""Pins for the thought-map trace (visual thought map).

Claims:
1. ``collect_thought_trace=True`` is OBSERVE-ONLY — identical fills, pnl, and
   weights vs an untraced run (never changes production behavior).
2. Trace is present only when requested and carries scan/decision events.
3. The deficiency diagnoser flags brain-wait-on-edge and never crashes on
   empty days.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.goal_path import run_goal_path_day
from evidence_court.meta_rl.policy import MetaPolicy
from evidence_court.meta_rl.brain import train_meta_brain


def _synth_m1(n_days: int = 8, trend: float = 0.00015) -> list:
    rows = []
    px = 2000.0
    for d in range(n_days):
        date = f"2026-06-{d + 1:02d}"
        for m in range(0, 24 * 60, 5):
            h, mi = divmod(m, 60)
            rows.append(
                {
                    "date": date,
                    "time": f"{h:02d}:{mi:02d}:00",
                    "open": px,
                    "high": max(px, px * (1 + trend)) * 1.0003,
                    "low": min(px, px * (1 + trend)) * 0.9997,
                    "close": px * (1 + trend),
                }
            )
            px *= 1 + trend
    return rows


def _policy() -> MetaPolicy:
    pol = MetaPolicy(brain=train_meta_brain(seed=11, n_steps=600, freeze=True))
    pol.freeze_for_inference()
    return pol


def test_trace_is_observe_only_and_gated():
    m1 = _synth_m1()
    pol = _policy()
    kw = dict(
        date="2026-06-08",
        m1_by_symbol={"XAUUSD": m1},
        target_percent=10.0,
        max_daily_risk_percent=2.0,
        symbols=["XAUUSD"],
    )
    fills0, led0, meta0 = run_goal_path_day(pol, **kw)
    fills1, led1, meta1 = run_goal_path_day(pol, **kw, collect_thought_trace=True)

    assert "thought_trace" not in meta0
    assert "thought_trace" in meta1
    # identical behavior
    assert len(fills0) == len(fills1)
    assert abs(led0.realized_pnl_percent - led1.realized_pnl_percent) < 1e-12
    assert [f.slot for f in fills0] == [f.slot for f in fills1]
    assert [f.size_risk_percent for f in fills0] == [f.size_risk_percent for f in fills1]
    pol.assert_frozen()

    tr = meta1["thought_trace"]
    assert isinstance(tr, list)
    events = {t["event"] for t in tr}
    assert "scan" in events
    fired = [t for t in tr if t["event"] == "fired"]
    assert len(fired) == len(fills1)
    for f in fired:
        assert "brain" in f and "size" in f and "fill" in f
        assert f["size"]["source"] in (
            "size_head_passthrough",
            "intelligent_size_up_blend",
            "brain_direct",
            "clear_path_heuristic",
        )


def test_diagnoser_flags_and_empty_day():
    sys.path.insert(0, str(ROOT / "tools"))
    from thought_map import diagnose_day

    empty = {"date": "x", "target": 15.0, "risk": 2.0, "trace": []}
    assert diagnose_day(empty) == []

    waits = [
        {
            "event": "brain_wait",
            "prime": True,
            "slot": "10:00:00",
            "symbol": "XAUUSD",
        }
        for _ in range(4)
    ]
    day = {"date": "x", "target": 15.0, "risk": 2.0, "trace": waits}
    kinds = {f["kind"] for f in diagnose_day(day)}
    assert "BRAIN_WAIT_ON_EDGE" in kinds
