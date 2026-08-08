"""CASE-0018 NEW tests: day-path A17 regime channel in doctrine (ISSUE-ROAD)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence_court.meta_rl.observation import DOCTRINE_DIM, MARK_FULL_DIM
from evidence_court.meta_rl.policy import sample_training_state
from evidence_court.meta_rl.regimes import (
    REGIME_ONEHOT_ORDER,
    RegimeId,
    day_path_regime_channel_self_check,
    day_path_regime_skip_new_risk,
    decode_regime_from_doctrine,
    encode_regime_doctrine,
    efficiency_proxy_from_edge,
    regime_from_edge_sensors,
    regime_kill_new_risk,
)
from evidence_court.meta_rl.state import META_RL_DIM, build_meta_rl_state


def test_creator_new_regime_doctrine_encode_decode_distinct():
    """Creator NEW: doctrine pack is 16-dim, round-trips, and distinguishes regimes."""
    assert day_path_regime_channel_self_check()["ok"] is True
    vecs = []
    for rid in REGIME_ONEHOT_ORDER:
        v = encode_regime_doctrine(rid, force=0.3, efficiency=0.55)
        assert v.shape == (DOCTRINE_DIM,)
        assert decode_regime_from_doctrine(v) == rid
        vecs.append(v.copy())
    # All pairwise distinct
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            assert not np.allclose(vecs[i], vecs[j]), (i, j)


def test_mark_new_edge_sensors_map_to_a17_kill_playbook():
    """Mark NEW: edge sensors → A17; conflict/compression skip new risk on day path."""
    assert (
        regime_from_edge_sensors(
            multi_set_consensus="conflict", consensus_force=0.0, efficiency=0.5
        )
        == RegimeId.CONFLICT
    )
    assert day_path_regime_skip_new_risk(RegimeId.CONFLICT)
    assert regime_kill_new_risk(RegimeId.CONFLICT)

    assert (
        regime_from_edge_sensors(
            multi_set_consensus="chop", consensus_force=0.0, efficiency=0.1
        )
        == RegimeId.VOL_COMPRESSION
    )
    assert day_path_regime_skip_new_risk(RegimeId.VOL_COMPRESSION)

    rid = regime_from_edge_sensors(
        multi_set_consensus="agree_long", consensus_force=0.45, efficiency=0.55
    )
    assert rid == RegimeId.TREND_BULL
    assert not day_path_regime_skip_new_risk(rid)

    # Efficiency proxy is bounded and rises with activity/force
    e0 = efficiency_proxy_from_edge(n_pullback=0, n_continuation=0, consensus_force=0.0)
    e1 = efficiency_proxy_from_edge(n_pullback=1, n_continuation=1, consensus_force=0.5)
    assert 0.0 <= e0 <= 1.0 and 0.0 <= e1 <= 1.0
    assert e1 >= e0


def test_creator_new_state_with_doctrine_keeps_meta_rl_dim():
    """Creator counter NEW: state+doctrine stays META_RL_DIM=176; doctrine slice decodes."""
    assert META_RL_DIM == 176
    assert MARK_FULL_DIM == 168
    doctrine = encode_regime_doctrine(
        RegimeId.TREND_BEAR, force=-0.4, efficiency=0.5
    )
    st = build_meta_rl_state(
        target_percent=15.0,
        max_daily_risk_percent=2.0,
        doctrine_vec=doctrine,
    )
    assert st.shape == (META_RL_DIM,)
    # doctrine lives at mark[32:48]
    doc_slice = st[32:48]
    assert decode_regime_from_doctrine(doc_slice) == RegimeId.TREND_BEAR


def test_mark_new_curriculum_and_daypath_share_regime_doctrine_layout():
    """Mark counter NEW: curriculum samples pack same doctrine layout as day path."""
    rng = np.random.default_rng(18)
    st, teacher, _topo, rid = sample_training_state(
        rng, target=20.0, risk=2.0, regime=RegimeId.CONFLICT, return_regime=True
    )
    assert rid == RegimeId.CONFLICT
    assert teacher == "wait"
    assert st.shape == (META_RL_DIM,)
    assert decode_regime_from_doctrine(st[32:48]) == RegimeId.CONFLICT
    # Kill flag set in doctrine
    assert float(st[32 + 9]) == 1.0  # IDX_REGIME_KILL

    st2, _t2, _tp2, rid2 = sample_training_state(
        rng, target=20.0, risk=2.0, regime=RegimeId.TREND_BULL, return_regime=True
    )
    assert rid2 == RegimeId.TREND_BULL
    assert decode_regime_from_doctrine(st2[32:48]) == RegimeId.TREND_BULL
    assert float(st2[32 + 8]) == 1.0  # allow fire
    assert float(st2[32 + 9]) == 0.0  # not kill
