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
    from evidence_court.meta_rl.state import META_RL_DIM

    for f in fired:
        assert "brain" in f and "size" in f and "fill" in f
        # exact packed state travels with every decision (trainable corrections)
        assert len(f["state"]) == META_RL_DIM
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


def test_corrections_teach_moves_brain_toward_human(tmp_path):
    """Closed loop: exported correction row -> trainer -> brain agrees with human."""
    import json

    sys.path.insert(0, str(ROOT / "tools"))
    import teach_from_corrections as tfc

    # champion-like source policy
    src_pol = _policy()
    src = tmp_path / "src.npz"
    src_pol.save(src)

    # a state where the brain currently says one thing; human corrects it
    m1 = _synth_m1()
    fills, _, meta = run_goal_path_day(
        src_pol,
        date="2026-06-08",
        m1_by_symbol={"XAUUSD": m1},
        target_percent=10.0,
        max_daily_risk_percent=2.0,
        symbols=["XAUUSD"],
        collect_thought_trace=True,
    )
    decs = [t for t in meta["thought_trace"] if "brain" in t]
    assert decs, "need at least one decision with a packed state"
    t0 = decs[0]
    human_act = "short" if t0["brain"]["act"] != "short" else "long"
    row = {
        "date": "2026-06-08",
        "slot": t0["slot"],
        "symbol": t0["symbol"],
        "event": t0["event"],
        "teacher_act": human_act,
        "teacher_size_frac": 0.4,
        "weight": 1.5,
        "source": "human_thought_map_edit",
        "state": t0["state"],
    }
    corr = tmp_path / "corr.jsonl"
    corr.write_text(json.dumps(row) + "\n", encoding="utf-8")

    out = tmp_path / "lab.npz"
    rc = tfc.main(
        [str(corr), "--champion", str(src), "--out", str(out), "--epochs", "60"]
    )
    assert rc == 0 and out.exists()

    from evidence_court.meta_rl.policy import MetaPolicy
    import numpy as np

    lab = MetaPolicy.load(out, freeze=True, require_serious=False)
    act, _, _ = lab.brain.predict_act(np.asarray(t0["state"], dtype=float))
    assert act == human_act  # the brain learned the human correction
    # champion source untouched on disk
    untouched = MetaPolicy.load(src, freeze=True, require_serious=False)
    assert untouched.weight_fingerprint() == src_pol.weight_fingerprint()
