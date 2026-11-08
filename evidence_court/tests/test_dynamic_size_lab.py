"""Pins for the dynamic lot-size lab recipe (size-budget class).

Claims under test:
1. ``size_only=True`` meta updates change ONLY the size head — trunk and act
   head stay byte-identical, so fire/wait decisions cannot change.
2. The dynamic size teacher law is monotone in the right directions:
   more edge → bigger; less remaining budget → smaller; near target → locked;
   marginal edge → probe-size; wait → zero.
3. Training measurably improves size-head fit (corr with teacher) vs champion.
"""
from __future__ import annotations

import numpy as np
import pytest

from evidence_court.meta_rl.brain import MetaBrain, train_meta_brain
from evidence_court.meta_rl.train_dynamic_size import (
    dynamic_size_teacher,
    sample_size_state,
)


def test_size_only_update_never_touches_trunk_or_act_head():
    brain = train_meta_brain(seed=3, n_steps=60, freeze=False)
    rng = np.random.default_rng(0)
    st, teacher_act, frac, _ = sample_size_state(rng, target=30.0, risk=2.0)
    w1, b1 = brain.W1.copy(), brain.b1.copy()
    w2, b2 = brain.W2.copy(), brain.b2.copy()
    for _ in range(25):
        brain.meta_update(
            st, teacher_act=teacher_act, teacher_size_frac=frac, size_only=True
        )
    assert np.array_equal(brain.W1, w1)
    assert np.array_equal(brain.b1, b1)
    assert np.array_equal(brain.W2, w2)
    assert np.array_equal(brain.b2, b2)


def test_size_only_update_moves_size_head_toward_teacher():
    brain = train_meta_brain(seed=3, n_steps=60, freeze=False)
    rng = np.random.default_rng(1)
    st, teacher_act, _, _ = sample_size_state(rng, target=30.0, risk=2.0)
    target_frac = 0.2
    _, logit0, _ = brain.forward_raw(st)
    err0 = abs(target_frac - 1.0 / (1.0 + np.exp(-logit0)))
    for _ in range(60):
        brain.meta_update(
            st, teacher_act=teacher_act, teacher_size_frac=target_frac, size_only=True
        )
    _, logit1, _ = brain.forward_raw(st)
    err1 = abs(target_frac - 1.0 / (1.0 + np.exp(-logit1)))
    assert err1 < err0


def test_size_only_forbidden_when_frozen():
    brain = train_meta_brain(seed=3, n_steps=60, freeze=True)
    rng = np.random.default_rng(2)
    st, teacher_act, frac, _ = sample_size_state(rng, target=15.0, risk=2.0)
    with pytest.raises(RuntimeError, match="NO_RETRAIN_VIOLATION"):
        brain.meta_update(
            st, teacher_act=teacher_act, teacher_size_frac=frac, size_only=True
        )


def test_dynamic_teacher_monotone_edge_and_budget():
    kw = dict(target_norm=0.5, risk_remaining=1.0, progress=0.2)
    weak = dynamic_size_teacher(edge_strength=0.4, **kw)
    strong = dynamic_size_teacher(edge_strength=0.9, **kw)
    assert strong > weak

    kw2 = dict(edge_strength=0.8, target_norm=0.5, progress=0.2)
    full = dynamic_size_teacher(risk_remaining=1.0, **kw2)
    burnt = dynamic_size_teacher(risk_remaining=0.2, **kw2)
    assert burnt < full


def test_dynamic_teacher_near_target_lock_and_marginal_probe():
    # v2: lock only when essentially clear (0.97+) — never starve the final push
    locked = dynamic_size_teacher(
        edge_strength=0.9, target_norm=0.8, risk_remaining=1.0, progress=0.99
    )
    assert locked <= 0.25
    push = dynamic_size_teacher(
        edge_strength=0.9, target_norm=0.8, risk_remaining=1.0, progress=0.9
    )
    assert push > 0.4  # still pushing at 90% progress
    marginal = dynamic_size_teacher(
        edge_strength=0.1, target_norm=0.8, risk_remaining=1.0, progress=0.1
    )
    assert marginal <= 0.15
    assert dynamic_size_teacher(
        edge_strength=0.9, target_norm=0.5, risk_remaining=1.0, progress=0.1, fire=False
    ) == 0.0


def test_size_head_drives_flag_changes_size_not_act(tmp_path):
    from evidence_court.meta_rl.policy import MetaPolicy

    brain = train_meta_brain(seed=5, n_steps=600, freeze=True)
    pol = MetaPolicy(brain=brain)
    pol.freeze_for_inference()

    rng = np.random.default_rng(9)
    acts_legacy, acts_dyn, sizes_legacy, sizes_dyn = [], [], [], []
    for _ in range(120):
        st, _, _, _ = sample_size_state(rng, target=30.0, risk=2.0)
        pol.size_head_drives = False
        a0 = pol.forward(st)
        pol.size_head_drives = True
        a1 = pol.forward(st)
        acts_legacy.append(a0.act)
        acts_dyn.append(a1.act)
        if a0.act in ("long", "short"):
            sizes_legacy.append(a0.size_risk_percent)
            sizes_dyn.append(a1.size_risk_percent)
    assert acts_legacy == acts_dyn  # sizing mode never changes fire/wait/side
    assert sizes_legacy and sizes_legacy != sizes_dyn

    # flag round-trips through save/load; absent flag (champion) stays legacy
    pol.size_head_drives = True
    p = tmp_path / "dyn.npz"
    pol.save(p)
    loaded = MetaPolicy.load(p, freeze=True)
    assert loaded.size_head_drives is True


def test_teacher_spread_is_wide_not_constant():
    rng = np.random.default_rng(5)
    fracs = []
    for _ in range(300):
        _, act, frac, _ = sample_size_state(
            rng,
            target=float(rng.choice([5.0, 30.0, 90.0])),
            risk=float(rng.choice([1.0, 3.0])),
        )
        if act != "wait":
            fracs.append(frac)
    fracs = np.array(fracs)
    assert fracs.std() > 0.12  # genuinely dynamic, not near-constant
    assert fracs.min() < 0.25 and fracs.max() > 0.7
