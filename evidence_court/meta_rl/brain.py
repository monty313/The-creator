"""Learn-to-learn meta-brain (Law A29) — trained network, not hard rules.

- Multi-layer net over META_RL_DIM state → act logits (wait/long/short) + size head.
- Offline curriculum: goal×risk band, L2L channel renames, London/NY opportunity fire.
- Inference: freeze weights; target/risk only via state context (no retrain).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .goal_risk import (
    IDX_ALLOW_FIRE,
    IDX_GOAL_PRESSURE,
    IDX_HARDNESS,
    IDX_RISK_NORM,
    IDX_RISK_REMAINING,
    IDX_TARGET_NORM,
)
from .state import META_RL_DIM, build_meta_rl_state, extract_goal_risk_context
from .types import Direction, SetConfluence, StructureFlags, VelocityStrength

HIDDEN = 64
ACT_WAIT, ACT_LONG, ACT_SHORT = 0, 1, 2
ACT_NAMES = ("wait", "long", "short")

# London/NY: plenty of opportunity — train to fire when structure says so
LONDON_NY_PRESSURE = 1.15


def _relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(x, 0.0)


def _softmax(z: np.ndarray) -> np.ndarray:
    z = z - np.max(z)
    e = np.exp(np.clip(z, -40, 40))
    return e / (np.sum(e) + 1e-12)


def _pad(state: np.ndarray) -> np.ndarray:
    s = np.asarray(state, dtype=np.float64).reshape(-1)
    if s.size < META_RL_DIM:
        t = np.zeros(META_RL_DIM, dtype=np.float64)
        t[: s.size] = s
        return t
    return s[:META_RL_DIM].astype(np.float64)


@dataclass
class MetaBrain:
    """Two-layer meta-network: learn-to-learn attention over Mark+goal state."""

    W1: np.ndarray  # (H, D)
    b1: np.ndarray  # (H,)
    W2: np.ndarray  # (3, H) act logits
    b2: np.ndarray  # (3,)
    W_size: np.ndarray  # (H,) size aggression
    b_size: float = 0.0
    seed: int = 0
    meta_train_steps: int = 0
    trained: bool = False
    frozen_for_inference: bool = False
    inference_updates: int = 0
    _fingerprint: str = field(default="", repr=False)

    @classmethod
    def create(cls, seed: int = 42) -> "MetaBrain":
        rng = np.random.default_rng(seed)
        d, h = META_RL_DIM, HIDDEN
        # Xavier-ish
        w1 = rng.normal(0, np.sqrt(2.0 / d), size=(h, d))
        # Prior: boost set-dir and goal channels into first layer
        for i in (0, 3, 6, 9):
            w1[:, i] += 0.15
        base = META_RL_DIM - 8
        w1[:, base + IDX_ALLOW_FIRE] += 0.2
        w1[:, base + IDX_GOAL_PRESSURE] += 0.15
        b1 = np.zeros(h)
        w2 = rng.normal(0, np.sqrt(2.0 / h), size=(3, h))
        b2 = np.array([0.3, 0.0, 0.0])  # slight wait prior before train
        ws = rng.normal(0, 0.05, size=(h,))
        brain = cls(
            W1=w1,
            b1=b1,
            W2=w2,
            b2=b2,
            W_size=ws,
            b_size=0.0,
            seed=seed,
            meta_train_steps=0,
            trained=False,
        )
        brain._fingerprint = brain.weight_fingerprint()
        return brain

    def weight_fingerprint(self) -> str:
        blob = b"".join(
            [
                self.W1.tobytes(),
                self.b1.tobytes(),
                self.W2.tobytes(),
                self.b2.tobytes(),
                self.W_size.tobytes(),
                np.array([self.b_size], dtype=np.float64).tobytes(),
            ]
        )
        digest = hashlib.sha256(blob).hexdigest()[:16]
        return f"{self.seed}:meta{self.meta_train_steps}:inf{self.inference_updates}:{digest}"

    def params_vector(self) -> np.ndarray:
        return np.concatenate(
            [
                self.W1.ravel(),
                self.b1.ravel(),
                self.W2.ravel(),
                self.b2.ravel(),
                self.W_size.ravel(),
                np.array([self.b_size]),
            ]
        )

    def freeze_for_inference(self) -> "MetaBrain":
        if not self.trained:
            raise RuntimeError("POLICY_NOT_TRAINED: brain must complete meta curriculum first")
        self.frozen_for_inference = True
        self.inference_updates = 0
        self._fingerprint = self.weight_fingerprint()
        return self

    def unlock_for_meta_train(self) -> "MetaBrain":
        self.frozen_for_inference = False
        return self

    def assert_frozen(self) -> None:
        if not self.frozen_for_inference:
            raise RuntimeError("NO_RETRAIN_VIOLATION: brain not frozen for inference")
        if self.inference_updates != 0:
            raise RuntimeError("NO_RETRAIN_VIOLATION: inference_updates != 0")
        if self.weight_fingerprint() != self._fingerprint:
            raise RuntimeError("NO_RETRAIN_VIOLATION: brain weights mutated at inference")

    def forward_raw(self, state: np.ndarray) -> Tuple[np.ndarray, float, np.ndarray]:
        """Return act_logits (3,), size_logit, hidden."""
        s = _pad(state)
        h = _relu(self.W1 @ s + self.b1)
        logits = self.W2 @ h + self.b2
        size_logit = float(self.W_size @ h + self.b_size)
        return logits, size_logit, h

    def predict_act(self, state: np.ndarray) -> Tuple[str, float, np.ndarray]:
        logits, size_logit, h = self.forward_raw(state)
        probs = _softmax(logits)
        idx = int(np.argmax(probs))
        return ACT_NAMES[idx], size_logit, probs

    def meta_update(
        self,
        state: np.ndarray,
        *,
        teacher_act: str,
        lr: float = 0.02,
        reward: float = 1.0,
        teacher_size_frac: Optional[float] = None,
    ) -> float:
        """One supervised meta step (cross-entropy act + size). Forbidden if frozen."""
        if self.frozen_for_inference:
            raise RuntimeError(
                "NO_RETRAIN_VIOLATION: meta_update forbidden at inference"
            )
        s = _pad(state)
        y = {"wait": ACT_WAIT, "long": ACT_LONG, "short": ACT_SHORT}.get(
            teacher_act, ACT_WAIT
        )

        # Forward
        h_pre = self.W1 @ s + self.b1
        h = _relu(h_pre)
        logits = self.W2 @ h + self.b2
        probs = _softmax(logits)
        size_logit = float(self.W_size @ h + self.b_size)

        # dL/dlogits for CE
        dlogits = probs.copy()
        dlogits[y] -= 1.0
        dlogits *= float(reward)

        # size target in [0,1] aggression
        if teacher_size_frac is None:
            teacher_size_frac = 0.0 if y == ACT_WAIT else 0.65
        size_err = float(teacher_size_frac) - 1.0 / (1.0 + np.exp(-size_logit))
        d_size = -float(reward) * size_err  # gradient on size_logit via sigmoid residual

        # Backprop W2, b2
        dW2 = np.outer(dlogits, h)
        db2 = dlogits
        dh = self.W2.T @ dlogits + self.W_size * d_size
        # ReLU
        dh_pre = dh * (h_pre > 0).astype(np.float64)
        dW1 = np.outer(dh_pre, s)
        db1 = dh_pre
        dWs = h * d_size
        dbs = d_size

        lr = float(lr)
        self.W2 = self.W2 - lr * dW2
        self.b2 = self.b2 - lr * db2
        self.W1 = self.W1 - lr * dW1
        self.b1 = self.b1 - lr * db1
        self.W_size = self.W_size - lr * dWs
        self.b_size = float(self.b_size - lr * dbs)
        # clip
        for arr in (self.W1, self.W2, self.W_size):
            np.clip(arr, -8.0, 8.0, out=arr)

        self.meta_train_steps += 1
        self.trained = True
        self._fingerprint = self.weight_fingerprint()
        return float(-np.log(probs[y] + 1e-12))


def sample_brain_state(
    rng: np.random.Generator,
    *,
    target: float,
    risk: float,
    london_ny: bool = False,
    force_opp: bool = False,
    l2l_permute: bool = False,
) -> Tuple[np.ndarray, str, float]:
    """Synthetic state + teacher for serious curriculum."""
    if force_opp:
        strength = float(rng.uniform(0.45, 1.0))
        side = int(rng.choice([-1, 1]))
        topo_fire = True
    else:
        strength = float(rng.uniform(0.0, 1.0))
        side = int(rng.choice([-1, 1]))
        topo_fire = strength > 0.35 and rng.random() > 0.35

    official: Dict[int, SetConfluence] = {}
    for sid in (1, 2, 3, 4):
        s = side if rng.random() > 0.12 else -side
        if not topo_fire or strength < 0.25:
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

    progress = float(rng.uniform(0.0, 0.7))
    realized = float(rng.uniform(0.0, risk * 0.5))
    session = float(rng.uniform(0.35, 0.85)) if london_ny else float(rng.uniform(0.0, 1.0))

    state = build_meta_rl_state(
        target_percent=target,
        max_daily_risk_percent=risk,
        official=official,
        structure=StructureFlags(pullback=topo_fire and rng.random() > 0.4),
        progress_to_target=progress,
        realized_risk_percent=realized,
        session_phase=session,
    )
    st = state.copy()

    # Explicit set dir channels
    dirs = []
    for i, sid in enumerate((1, 2, 3, 4)):
        c = official[sid]
        val = float(int(c.direction)) * (0.5 + 0.5 * strength)
        dirs.append(val)
        idx = i * 3
        if idx < st.size:
            st[idx] = val

    if l2l_permute:
        # Learn-to-learn: shuffle which set slot carries the signal (rename drill)
        order = rng.permutation(4)
        vals = [float(st[i * 3]) for i in range(4)]
        for i, j in enumerate(order):
            st[i * 3] = vals[j]

    mean_dir = float(np.mean(dirs)) if dirs else 0.0
    ctx = extract_goal_risk_context(st)
    allow = float(ctx[IDX_ALLOW_FIRE]) >= 0.5
    risk_rem = float(ctx[IDX_RISK_REMAINING])

    # Teacher: structure + goal (not a frozen hard path recipe)
    if not allow or risk_rem < 0.08 or not topo_fire or abs(mean_dir) < 0.25:
        teacher = "wait"
        size_frac = 0.0
    else:
        teacher = "long" if mean_dir > 0 else "short"
        # Higher targets → more aggression (goal-conditioned)
        t_norm = (target - 5.0) / 85.0
        size_frac = float(np.clip(0.45 + 0.4 * t_norm + (0.1 if london_ny else 0.0), 0.2, 0.95))
        if london_ny and force_opp:
            # No excuse: London/NY opportunity → fire
            size_frac = max(size_frac, 0.55)

    # Session phase flag in structure danger channel already; boost goal pressure feel
    if london_ny:
        base = META_RL_DIM - 8
        st[base + IDX_GOAL_PRESSURE] = min(
            1.0, float(st[base + IDX_GOAL_PRESSURE]) * LONDON_NY_PRESSURE
        )

    return st, teacher, size_frac


def train_meta_brain(
    *,
    seed: int = 42,
    n_steps: int = 8000,
    lr: float = 0.025,
    freeze: bool = True,
) -> MetaBrain:
    """Serious permanent curriculum — required for production brain.

    Lab pins may use n_steps >= 50. Production champion load still requires
    meta_train_steps >= 500 (MetaPolicy.load).
    """
    if n_steps < 50:
        raise ValueError("A29: n_steps must be >= 50 (lab pin); production >= 500")
    rng = np.random.default_rng(seed)
    brain = MetaBrain.create(seed)
    targets = (5.0, 10.0, 15.0, 30.0, 50.0, 70.0, 90.0)
    risks = (1.0, 2.0, 3.0)
    losses: List[float] = []

    for step in range(int(n_steps)):
        t = float(rng.choice(targets))
        r = float(rng.choice(risks))
        # Mix: 40% London/NY opportunity drills, 25% L2L permute, rest general
        u = rng.random()
        if u < 0.40:
            st, teacher, sf = sample_brain_state(
                rng, target=t, risk=r, london_ny=True, force_opp=True, l2l_permute=False
            )
        elif u < 0.65:
            st, teacher, sf = sample_brain_state(
                rng, target=t, risk=r, london_ny=rng.random() > 0.5, force_opp=False, l2l_permute=True
            )
        else:
            st, teacher, sf = sample_brain_state(
                rng, target=t, risk=r, london_ny=False, force_opp=False, l2l_permute=False
            )
        loss = brain.meta_update(
            st, teacher_act=teacher, lr=lr * (0.97 ** (step // 500)), reward=1.0, teacher_size_frac=sf
        )
        losses.append(loss)
        # Extra London/NY fire reinforcement every 5 steps
        if step % 5 == 0:
            st2, teacher2, sf2 = sample_brain_state(
                rng, target=t, risk=r, london_ny=True, force_opp=True
            )
            brain.meta_update(
                st2, teacher_act=teacher2, lr=lr * 0.8, reward=1.2, teacher_size_frac=sf2
            )

    brain.trained = True
    if freeze:
        brain.freeze_for_inference()
    return brain


def brain_act_match_rate(brain: MetaBrain, *, seed: int = 1, n: int = 200) -> float:
    rng = np.random.default_rng(seed)
    ok = 0
    for _ in range(n):
        t = float(rng.choice([5.0, 30.0, 90.0]))
        r = float(rng.choice([1.0, 2.0, 3.0]))
        st, teacher, _ = sample_brain_state(
            rng, target=t, risk=r, london_ny=rng.random() > 0.5, force_opp=rng.random() > 0.5
        )
        # eval unlocked
        was = brain.frozen_for_inference
        brain.frozen_for_inference = False
        act, _, _ = brain.predict_act(st)
        brain.frozen_for_inference = was
        if act == teacher:
            ok += 1
    return ok / float(n)
