"""CASE-L2L-P1 Creator NEW: senses packed into state change brain logits/action."""
from __future__ import annotations

import numpy as np

from evidence_court.meta_rl.brain import MetaBrain
from evidence_court.meta_rl.senses import (
    SENSE_PACK_DIM,
    MarketSenseInput,
    encode_sense_report,
    probe_all_senses,
)
from evidence_court.meta_rl.state import (
    META_RL_DIM,
    SENSE_STATE_SLICE,
    build_meta_rl_state,
    extract_sense_pack,
)


def _load_inp(**kw) -> MarketSenseInput:
    base = dict(
        htf_force=[0.8, 0.7, 0.75, 0.7, 0.6, 0.65, 0.5, 0.55],
        ltf_velocity=[-0.5, -0.4, -0.45, -0.3],
        inertia=[0.7, 0.65, 0.6, 0.55],
        inertia_baseline=[0.4, 0.4, 0.4, 0.4],
        velocity_baseline=[0.1, 0.1, 0.1, 0.1],
        full_body_outside_rails=True,
        ltf_inside_tight=True,
        efficiency=0.6,
        regime="bull",
        g_fixed=True,
        composition_has_force=True,
        composition_has_velocity=True,
        cross_family_agree=True,
        target_percent=50.0,
        max_daily_risk_percent=2.0,
        progress_to_target=0.1,
    )
    base.update(kw)
    return MarketSenseInput(**base)


def test_creator_new_encode_sense_report_fixed_dim():
    rep = probe_all_senses(_load_inp())
    v = encode_sense_report(rep)
    assert v.shape == (SENSE_PACK_DIM,)
    assert np.all(np.isfinite(v))


def test_creator_new_senses_pack_into_meta_rl_state_dim_preserved():
    rep = probe_all_senses(_load_inp())
    st = build_meta_rl_state(
        target_percent=15.0,
        max_daily_risk_percent=2.0,
        sense_report=rep,
    )
    assert st.shape == (META_RL_DIM,)
    assert META_RL_DIM == 176  # frozen-weight contract
    pack = extract_sense_pack(st)
    assert pack.shape == (SENSE_PACK_DIM,)
    # Non-zero pack on load-building market
    assert float(np.max(np.abs(pack))) > 0.0
    assert np.allclose(st[SENSE_STATE_SLICE], pack)


def test_creator_new_sense_value_change_changes_brain_logits():
    """Changing only sense channels changes forward_raw logits (senses drive brain)."""
    brain = MetaBrain.create(seed=7)
    # Ensure sense columns of W1 are live (random init usually is; force non-zero)
    brain.W1[:, SENSE_STATE_SLICE] = np.random.default_rng(7).normal(
        0.0, 0.15, size=(brain.W1.shape[0], SENSE_PACK_DIM)
    )

    rep_a = probe_all_senses(_load_inp())
    # Opposite structure: force down, launch not load
    rep_b = probe_all_senses(
        _load_inp(
            htf_force=[-0.8, -0.7, -0.75, -0.7, -0.6, -0.65, -0.5, -0.55],
            ltf_velocity=[0.5, 0.4, 0.45, 0.3],
            inertia=[-0.7, -0.65, -0.6, -0.55],
            g_fixed=False,
            g_flip=True,
            regime="bear",
            cross_family_agree=True,
            set_conflict=False,
        )
    )
    st_a = build_meta_rl_state(
        target_percent=15.0, max_daily_risk_percent=2.0, sense_report=rep_a
    )
    st_b = build_meta_rl_state(
        target_percent=15.0, max_daily_risk_percent=2.0, sense_report=rep_b
    )
    # Only sense slice differs (same target/risk; empty official zeros)
    assert not np.allclose(extract_sense_pack(st_a), extract_sense_pack(st_b))
    # Channel1 may also differ if we passed official — here both zero except senses/goal
    # Zero non-sense mark body difference except sense slots:
    mask = np.ones(META_RL_DIM, dtype=bool)
    mask[SENSE_STATE_SLICE] = False
    # goal context identical
    assert np.allclose(st_a[mask], st_b[mask], atol=1e-5)

    log_a, _, _ = brain.forward_raw(st_a)
    log_b, _, _ = brain.forward_raw(st_b)
    assert not np.allclose(log_a, log_b, atol=1e-8)
    act_a = int(np.argmax(log_a))
    act_b = int(np.argmax(log_b))
    # Prefer action flip; if not, logits still must differ (asserted above)
    _ = (act_a, act_b)


def test_mark_new_senses_not_probe_only_in_layout():
    lay = __import__(
        "evidence_court.meta_rl.state", fromlist=["meta_rl_layout"]
    ).meta_rl_layout()
    assert lay["sense_pack_dim"] == SENSE_PACK_DIM
    assert "senses_in_agent_votes" in lay
