"""CASE-0036 NEW tests: real-bar Watch harvest for C-003 A13 density (anti F-024)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.real_bar_harvest import (
    filter_real_bar_a13_labels,
    train_real_bar_a13_policy,
)
from evidence_court.meta_rl.goal_path import allows_empty_slot_skip, a13_trade_count_ok
from evidence_court.meta_rl.state import build_meta_rl_state


def _synthetic_realish_labels() -> list:
    """Unit fixtures with real-bar provenance fields (dated), mixed topologies."""
    return [
        {
            "teacher_act": "long",
            "topology": "pullback_resume",
            "session_band": "london_ny",
            "weight": 1.5,
            "symbol": "XAUUSD",
            "set_id": 1,
            "asof_date": "2026-02-10",
            "asof_time": "14:00:00",
            "force": 0.41,
            "what_bot_did": "wait",
            "source": "real_bar_watch",
        },
        {
            "teacher_act": "short",
            "topology": "continuation",
            "session_band": "london_ny",
            "weight": 1.5,
            "symbol": "EURUSD",
            "set_id": 2,
            "asof_date": "2026-02-11",
            "asof_time": "10:30:00",
            "force": -0.38,
            "what_bot_did": "wait",
            "source": "real_bar_watch",
        },
        {
            "teacher_act": "long",
            "topology": "chop",  # must drop
            "session_band": "other",
            "weight": 1.0,
            "symbol": "GBPUSD",
            "set_id": 3,
            "asof_date": "2026-02-12",
            "asof_time": "03:00:00",
            "force": 0.1,
            "what_bot_did": "wait",
            "source": "real_bar_watch",
        },
        {
            "teacher_act": "short",
            "topology": "pullback_resume",
            "session_band": "other",
            "weight": 1.0,
            "symbol": "XAUUSD",
            "set_id": 1,
            "asof_date": "2026-02-13",
            "asof_time": "21:00:00",
            "force": -0.33,
            "what_bot_did": "wait",
            "source": "real_bar_watch",
        },
        {
            # undated synthetic → drop (anti F-024 smuggle)
            "teacher_act": "long",
            "topology": "continuation",
            "session_band": "london_ny",
            "weight": 1.5,
            "asof_date": "",
            "asof_time": "14:00:00",
            "source": "synthetic",
        },
    ]


def test_creator_new_filter_keeps_dated_pb_cont_only():
    """Creator NEW: real-bar filter keeps dated PB/cont teachers; drops chop + undated."""
    labs = filter_real_bar_a13_labels(_synthetic_realish_labels(), max_labels=20)
    assert len(labs) == 3
    assert all(x["topology"] in ("pullback_resume", "continuation") for x in labs)
    assert all(x["asof_date"] for x in labs)
    assert all(x["source"] == "real_bar_watch" for x in labs)
    assert all(x["teacher_act"] in ("long", "short") for x in labs)


def test_mark_new_london_ny_weight_preserved_and_no_chop():
    """Mark NEW: London/NY weight > other; no chop teacher survives filter."""
    labs = filter_real_bar_a13_labels(_synthetic_realish_labels())
    ln = [x for x in labs if x["session_band"] == "london_ny"]
    other = [x for x in labs if x["session_band"] == "other"]
    assert ln and other
    assert ln[0]["weight"] > other[0]["weight"]
    assert not any(x["topology"] == "chop" for x in labs)


def test_creator_new_real_bar_train_freezes_no_retrain():
    """Creator counter: train on filtered realish labels → prove freeze across pairs."""
    labs = filter_real_bar_a13_labels(_synthetic_realish_labels())
    pol = train_real_bar_a13_policy(labs, seed=17, n_steps=80, opportunity_mix=0.2)
    assert pol.trained is True
    fp = pol.weight_fingerprint()
    for t, r in ((5.0, 1.0), (50.0, 2.0), (90.0, 3.0)):
        st = build_meta_rl_state(target_percent=t, max_daily_risk_percent=r)
        _ = pol.forward(st)
    pol.assert_frozen()
    assert pol.weight_fingerprint() == fp
    assert pol.inference_updates == 0


def test_mark_new_empty_skip_and_a13_band_geometry_preserved():
    """Mark counter: harvest path must not pad; A13 band helper + empty skip intact."""
    assert allows_empty_slot_skip() is True
    assert a13_trade_count_ok(8) is True
    assert a13_trade_count_ok(400) is True
    assert a13_trade_count_ok(7) is False
    assert a13_trade_count_ok(401) is False
    # filter never invents pad trades — only transforms labels
    labs = filter_real_bar_a13_labels(_synthetic_realish_labels())
    assert all(x.get("what_bot_did") == "wait" for x in labs)
