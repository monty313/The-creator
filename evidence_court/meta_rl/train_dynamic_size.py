"""Dynamic lot-size lab recipe (SEAN size-budget class, dual #2 shape).

Diagnosis (measured): champion size head is saturated (sigmoid mean ~0.86,
weak teacher corr ~0.45) because the base curriculum's size teacher varied
only with target/session — never with edge strength, remaining risk budget,
or progress-to-target. Sizes come out near-constant → day conversion stuck.

Recipe: teach the SIZE HEAD ONLY a dynamic size law (conviction × need ×
budget discipline + near-target lock), warm-started from the champion. Trunk
and act head are untouched (``size_only=True``), so fire/wait decisions are
byte-identical to the king — this isolates the size lever, keeps breach-0
behavior, and honors "keep act head frozen; no densify CE flood".

Counsel classes mapped: fractional-Kelly budget discipline · goal-conditioned
sizing · target-benchmark need. Lab only — never overwrites the champion.

CLI:
  python -m evidence_court.meta_rl.train_dynamic_size --steps 4000
  python -m evidence_court.meta_rl.train_dynamic_size --measure-only \
      --weights evidence_court/artifacts/policies_lab/meta_policy_dynamic_size.npz
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from evidence_court.meta_rl.brain import LONDON_NY_PRESSURE, MetaBrain
from evidence_court.meta_rl.goal_risk import IDX_GOAL_PRESSURE
from evidence_court.meta_rl.policy import DEFAULT_CHAMPION_PATH, MetaPolicy
from evidence_court.meta_rl.state import META_RL_DIM, build_meta_rl_state
from evidence_court.meta_rl.types import (
    Direction,
    SetConfluence,
    StructureFlags,
    VelocityStrength,
)

LAB_OUT = (
    Path(__file__).resolve().parents[1]
    / "artifacts"
    / "policies_lab"
    / "meta_policy_dynamic_size.npz"
)

TARGETS = (5.0, 10.0, 15.0, 30.0, 50.0, 70.0, 90.0)
RISKS = (1.0, 1.5, 2.0, 2.5, 3.0)


def dynamic_size_teacher(
    *,
    edge_strength: float,
    target_norm: float,
    risk_remaining: float,
    progress: float,
    london_ny: bool = False,
    fire: bool = True,
) -> float:
    """Size fraction in [0,1] — the dynamic law the size head must learn.

    - conviction: stronger multi-set edge → bigger
    - need (size-until-win): far from typed target → bigger; keep pushing
      until essentially clear (the day path itself locks after the hit)
    - budget discipline (fractional-Kelly flavor): shrink with burnt budget
    - near-clear taper: progress ≥ 0.97 → small (path lock takes over)
    - marginal edge: small probe size only

    v2 (measured iteration): v1 lost the clear day by a hair (+4.38 vs 5.00)
    because a 0.9-progress lock starved the final push; v2 locks only at 0.97
    and tilts bigger when far + strong edge (Day-12 "SIZE UNTIL WIN" class).
    """
    if not fire:
        return 0.0
    e = float(np.clip(edge_strength, 0.0, 1.0))
    t = float(np.clip(target_norm, 0.0, 1.0))
    rr = float(np.clip(risk_remaining, 0.0, 1.0))
    pg = float(np.clip(progress, 0.0, 1.0))
    if e < 0.25:
        return float(np.clip(0.10 * np.sqrt(rr), 0.05, 0.15))
    conviction = 0.25 + 0.60 * e
    need = (0.20 + 0.45 * t) * (1.0 - 0.55 * pg)
    frac = (conviction + need) * (rr ** 0.4)
    if london_ny:
        frac += 0.08
    if pg >= 0.97:
        frac = min(frac, 0.25)
    return float(np.clip(frac, 0.05, 0.98))


def sample_size_state(
    rng: np.random.Generator,
    *,
    target: float,
    risk: float,
) -> Tuple[np.ndarray, str, float, Dict[str, float]]:
    """Curriculum state with WIDE coverage of progress / burnt budget / edge.

    (The base curriculum only sampled progress ∈ [0, 0.7] and realized risk
    ∈ [0, 0.5·risk] — the size head never saw late-day / low-budget states.)
    """
    strength = float(rng.uniform(0.0, 1.0))
    side = int(rng.choice([-1, 1]))
    fire = strength > 0.30 and rng.random() > 0.25
    london = bool(rng.random() > 0.45)

    official: Dict[int, SetConfluence] = {}
    for sid in (1, 2, 3, 4):
        s = side if rng.random() > 0.10 else -side
        if not fire or strength < 0.25:
            d, nb, nr, nn = Direction.NEUTRAL, 1, 1, 1
            vel = VelocityStrength.WEAK
        elif s > 0:
            d, nb, nr, nn = Direction.BULL, 3, 0, 0
            vel = VelocityStrength.STRONG if strength > 0.55 else VelocityStrength.MEDIUM
        else:
            d, nb, nr, nn = Direction.BEAR, 0, 3, 0
            vel = VelocityStrength.STRONG if strength > 0.55 else VelocityStrength.MEDIUM
        official[sid] = SetConfluence(
            set_key=f"set{sid}",
            direction=d,
            velocity=vel,
            n_bull=nb,
            n_bear=nr,
            n_neutral=nn,
        )

    progress = float(rng.uniform(0.0, 1.0))
    realized = float(rng.uniform(0.0, risk * 0.95))
    session = float(rng.uniform(0.35, 0.85)) if london else float(rng.uniform(0.0, 1.0))

    st = build_meta_rl_state(
        target_percent=target,
        max_daily_risk_percent=risk,
        official=official,
        structure=StructureFlags(pullback=fire and rng.random() > 0.4),
        progress_to_target=progress,
        realized_risk_percent=realized,
        session_phase=session,
    )
    # explicit set-dir channels (same layout as base curriculum)
    for i, sid in enumerate((1, 2, 3, 4)):
        c = official[sid]
        idx = i * 3
        if idx < st.size:
            st[idx] = float(int(c.direction)) * (0.5 + 0.5 * strength)
    if london:
        base = META_RL_DIM - 8
        st[base + IDX_GOAL_PRESSURE] = min(
            1.0, float(st[base + IDX_GOAL_PRESSURE]) * LONDON_NY_PRESSURE
        )

    risk_remaining = float(np.clip(1.0 - realized / max(risk, 1e-6), 0.0, 1.0))
    t_norm = (float(target) - 5.0) / 85.0
    fire_ok = fire and risk_remaining > 0.05
    frac = dynamic_size_teacher(
        edge_strength=strength,
        target_norm=t_norm,
        risk_remaining=risk_remaining,
        progress=progress,
        london_ny=london,
        fire=fire_ok,
    )
    teacher_act = ("long" if side > 0 else "short") if fire_ok else "wait"
    meta = {
        "edge_strength": strength,
        "risk_remaining": risk_remaining,
        "progress": progress,
        "target_norm": t_norm,
    }
    return st, teacher_act, frac, meta


def train_dynamic_size(
    *,
    champion_path: Optional[Path] = None,
    steps: int = 4000,
    lr: float = 0.03,
    seed: int = 42,
    out: Optional[Path] = None,
) -> Tuple[MetaPolicy, Dict[str, float]]:
    """Warm-start from champion, size-head-only updates, freeze, save to lab."""
    src = Path(champion_path) if champion_path else DEFAULT_CHAMPION_PATH
    pol = MetaPolicy.load(src, freeze=False)
    brain: MetaBrain = pol.brain
    act_probe_before = _act_probe(brain, seed=seed + 100)

    rng = np.random.default_rng(seed)
    losses = []
    for step in range(int(steps)):
        t = float(rng.choice(TARGETS))
        r = float(rng.choice(RISKS))
        st, teacher_act, frac, _ = sample_size_state(rng, target=t, risk=r)
        loss = brain.meta_update(
            st,
            teacher_act=teacher_act,
            lr=lr * (0.97 ** (step // 400)),
            reward=1.0,
            teacher_size_frac=frac,
            size_only=True,
        )
        losses.append(loss)

    act_probe_after = _act_probe(brain, seed=seed + 100)
    acts_identical = act_probe_before == act_probe_after

    pol = MetaPolicy(brain=brain)
    pol.trained = True
    pol.size_head_drives = True  # lab mode: trained size head drives sizing
    pol.freeze_for_inference()
    out_path = Path(out) if out else LAB_OUT
    if out_path.resolve() == DEFAULT_CHAMPION_PATH.resolve():
        raise RuntimeError("FORBIDDEN: dynamic-size lab may not overwrite the champion")
    pol.save(out_path)

    fit = size_fit_report(pol, seed=seed + 7)
    report = {
        "steps": int(steps),
        "mean_size_loss_last500": float(np.mean(losses[-500:])),
        "acts_identical_to_champion": bool(acts_identical),
        "fingerprint": pol.weight_fingerprint(),
        "saved": str(out_path),
        **fit,
    }
    return pol, report


def _act_probe(brain: MetaBrain, *, seed: int, n: int = 300) -> Tuple[str, ...]:
    """Deterministic act decisions on a probe set (frozen-act proof)."""
    rng = np.random.default_rng(seed)
    acts = []
    was = brain.frozen_for_inference
    brain.frozen_for_inference = False
    for _ in range(n):
        t = float(rng.choice(TARGETS))
        r = float(rng.choice(RISKS))
        st, _, _, _ = sample_size_state(rng, target=t, risk=r)
        act, _, _ = brain.predict_act(st)
        acts.append(act)
    brain.frozen_for_inference = was
    return tuple(acts)


def size_fit_report(pol: MetaPolicy, *, seed: int = 7, n: int = 500) -> Dict[str, float]:
    """How well the size head tracks the dynamic teacher on fresh states."""
    rng = np.random.default_rng(seed)
    teach, pred = [], []
    for _ in range(n):
        t = float(rng.choice(TARGETS))
        r = float(rng.choice(RISKS))
        st, teacher_act, frac, _ = sample_size_state(rng, target=t, risk=r)
        if teacher_act == "wait":
            continue
        _, size_logit, _ = pol.brain.forward_raw(st)
        teach.append(frac)
        pred.append(1.0 / (1.0 + np.exp(-size_logit)))
    teach_a, pred_a = np.array(teach), np.array(pred)
    return {
        "size_teacher_mean": float(teach_a.mean()),
        "size_teacher_std": float(teach_a.std()),
        "size_pred_mean": float(pred_a.mean()),
        "size_pred_std": float(pred_a.std()),
        "size_corr": float(np.corrcoef(teach_a, pred_a)[0, 1]),
        "size_mae": float(np.mean(np.abs(teach_a - pred_a))),
    }


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--lr", type=float, default=0.03)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=str, default=str(LAB_OUT))
    ap.add_argument("--champion", type=str, default="", help="warm-start source npz")
    ap.add_argument("--measure-only", action="store_true", help="fit report on existing weights")
    ap.add_argument("--weights", type=str, default=str(LAB_OUT), help="for --measure-only")
    args = ap.parse_args(argv)

    if args.measure_only:
        pol = MetaPolicy.load(Path(args.weights), freeze=True)
        rep = {"fingerprint": pol.weight_fingerprint(), **size_fit_report(pol)}
        print(json.dumps(rep, indent=2))
        return 0

    _, rep = train_dynamic_size(
        champion_path=Path(args.champion) if args.champion else None,
        steps=args.steps,
        lr=args.lr,
        seed=args.seed,
        out=Path(args.out),
    )
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
