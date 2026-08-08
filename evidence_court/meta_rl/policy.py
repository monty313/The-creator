"""Production policy API — wraps trained learn-to-learn MetaBrain (Law A29).

Monty permanent:
  - Real brain (multi-layer meta net), not hard-rule soup.
  - Must be well trained offline (goal×risk + L2L + London/NY opportunity).
  - No retrain at inference when target/risk changes.
  - Hard rules do not decide; brain does (risk envelope still hard).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .brain import MetaBrain, train_meta_brain, _pad
from .goal_risk import (
    IDX_ALLOW_FIRE,
    IDX_GOAL_PRESSURE,
    IDX_HARDNESS,
    IDX_RISK_NORM,
    IDX_RISK_REMAINING,
    IDX_TARGET_NORM,
)
from .risk import DailyRiskLedger, size_position_risk_percent
from .state import META_RL_DIM, extract_goal_risk_context

DEFAULT_CHAMPION_PATH = (
    Path(__file__).resolve().parents[1] / "artifacts" / "meta_policy_champion.npz"
)

DEFAULT_TRAIN_TARGETS = (5.0, 10.0, 15.0, 30.0, 50.0, 70.0, 90.0)
DEFAULT_TRAIN_RISKS = (1.0, 2.0, 3.0)

_TRAINED_CACHE: Dict[Any, "MetaPolicy"] = {}


@dataclass
class PolicyAction:
    act: str  # wait | long | short
    size_risk_percent: float
    reason: str
    wait_subtype: str = ""
    topology: str = "chop"
    roles_cited: Tuple[str, ...] = ()


@dataclass
class MetaPolicy:
    """Trained meta-brain wrapper. ``weights`` kept for fingerprint/compat (flat export)."""

    brain: MetaBrain
    seed: int = 0
    # legacy flat view
    weights: np.ndarray = field(default_factory=lambda: np.zeros(META_RL_DIM))
    meta_train_steps: int = 0
    frozen_for_inference: bool = False
    trained: bool = False
    inference_updates: int = 0
    _fingerprint: str = field(default="", repr=False)

    def __post_init__(self) -> None:
        self.seed = int(self.brain.seed)
        self.meta_train_steps = int(self.brain.meta_train_steps)
        self.trained = bool(self.brain.trained)
        self.frozen_for_inference = bool(self.brain.frozen_for_inference)
        self.inference_updates = int(self.brain.inference_updates)
        self.weights = self.brain.params_vector()[:META_RL_DIM].copy()
        if self.weights.size < META_RL_DIM:
            w = np.zeros(META_RL_DIM)
            w[: self.weights.size] = self.weights
            self.weights = w
        self._fingerprint = self.weight_fingerprint()

    @property
    def train_steps(self) -> int:
        return int(self.inference_updates)

    @classmethod
    def untrained_prior(cls, seed: int = 42) -> "MetaPolicy":
        return cls(brain=MetaBrain.create(seed), trained=False)

    @classmethod
    def from_seed(cls, seed: int = 42, *, n_steps: int = 4000) -> "MetaPolicy":
        key = ("brain", int(seed), int(n_steps))
        if key in _TRAINED_CACHE:
            return _TRAINED_CACHE[key]._copy_frozen()
        pol = train_goal_conditioned_meta_policy(seed=seed, n_steps=n_steps, freeze=True)
        _TRAINED_CACHE[key] = pol
        return pol._copy_frozen()

    def _copy_frozen(self) -> "MetaPolicy":
        b = MetaBrain(
            W1=self.brain.W1.copy(),
            b1=self.brain.b1.copy(),
            W2=self.brain.W2.copy(),
            b2=self.brain.b2.copy(),
            W_size=self.brain.W_size.copy(),
            b_size=float(self.brain.b_size),
            seed=self.brain.seed,
            meta_train_steps=self.brain.meta_train_steps,
            trained=True,
            frozen_for_inference=True,
            inference_updates=0,
        )
        b._fingerprint = b.weight_fingerprint()
        return MetaPolicy(brain=b)

    def weight_fingerprint(self) -> str:
        return self.brain.weight_fingerprint()

    def freeze_for_inference(self) -> "MetaPolicy":
        self.brain.freeze_for_inference()
        self.frozen_for_inference = True
        self.trained = True
        self.meta_train_steps = self.brain.meta_train_steps
        self.inference_updates = 0
        self._fingerprint = self.weight_fingerprint()
        return self

    def unlock_for_meta_train(self) -> "MetaPolicy":
        self.brain.unlock_for_meta_train()
        self.frozen_for_inference = False
        return self

    def assert_frozen(self) -> None:
        self.brain.assert_frozen()
        self.frozen_for_inference = True

    def meta_update(self, state: np.ndarray, *, teacher_act: str, lr: float = 0.02, reward: float = 1.0, **kwargs: Any) -> float:
        out = self.brain.meta_update(state, teacher_act=teacher_act, lr=lr, reward=reward, **kwargs)
        self.meta_train_steps = self.brain.meta_train_steps
        self.trained = self.brain.trained
        self.weights = self.brain.params_vector()[:META_RL_DIM]
        return out

    def train_step(self, *args: Any, **kwargs: Any) -> Any:
        if self.brain.frozen_for_inference:
            raise RuntimeError(
                "NO_RETRAIN_VIOLATION: train_step forbidden at inference. "
                "target/risk changes are inference-time context only."
            )
        if args:
            state = args[0]
            teacher_act = kwargs.get("teacher_act", args[1] if len(args) > 1 else "wait")
            return self.meta_update(state, teacher_act=str(teacher_act), **{k: v for k, v in kwargs.items() if k != "teacher_act"})
        return self.meta_update(**kwargs)

    def score(self, state: np.ndarray) -> float:
        logits, _, _ = self.brain.forward_raw(state)
        # fire score: long - short magnitude
        return float(logits[1] - logits[2])

    def forward(
        self,
        state: np.ndarray,
        *,
        ledger: Optional[DailyRiskLedger] = None,
        topology: str = "chop",
        roles: Optional[Tuple[str, ...]] = None,
    ) -> PolicyAction:
        """Brain decides. Topology is a *hint in state/caller*, not a hard veto (A29)."""
        if self.brain.frozen_for_inference:
            self.brain.assert_frozen()
        elif not self.brain.trained:
            raise RuntimeError(
                "POLICY_NOT_TRAINED: brain requires serious meta curriculum (A29)"
            )

        ctx = extract_goal_risk_context(state)
        target_norm = float(ctx[IDX_TARGET_NORM])
        risk_norm = float(ctx[IDX_RISK_NORM])
        allow = float(ctx[IDX_ALLOW_FIRE]) >= 0.5
        risk_rem = float(ctx[IDX_RISK_REMAINING])
        roles_t = roles or ("force", "velocity")
        top = str(topology or "chop")

        # Only hard safety: risk envelope
        if not allow or risk_rem <= 0:
            return PolicyAction(
                act="wait",
                size_risk_percent=0.0,
                reason="risk_envelope_exhausted",
                wait_subtype="kill",
                topology=top,
                roles_cited=roles_t,
            )

        act, size_logit, probs = self.brain.predict_act(state)
        # Soft topology hint: if caller says collapse and brain barely confident, wait
        conf = float(np.max(probs))
        if top == "collapse" and conf < 0.45 and act != "wait":
            act = "wait"

        if act == "wait":
            subtype = "loaded_not_yet" if top == "slingshot_load" else "no_trade"
            return PolicyAction(
                act="wait",
                size_risk_percent=0.0,
                reason=f"brain_wait conf={conf:.2f} topo={top}",
                wait_subtype=subtype,
                topology=top,
                roles_cited=roles_t,
            )

        max_risk = 1.0 + 2.0 * risk_norm
        if ledger is not None:
            max_risk = ledger.max_daily_risk_percent
            remaining = ledger.remaining_risk_budget_percent()
        else:
            remaining = max_risk * risk_rem

        target = 5.0 + target_norm * 85.0
        # Size from brain head + goal pressure
        sig = 1.0 / (1.0 + np.exp(-size_logit))
        aggression = float(np.clip(0.35 + 0.55 * sig + 0.15 * target_norm, 0.2, 1.0))
        size = size_position_risk_percent(
            max_daily_risk_percent=max_risk,
            remaining_budget_percent=remaining,
            stop_distance_pct=0.35,
            target_percent=target,
            aggression=aggression,
            max_single_fraction=0.95,
            friction_reserve_percent=0.04,
        )
        if size <= 0:
            return PolicyAction(
                act="wait",
                size_risk_percent=0.0,
                reason="size_zero_under_envelope",
                wait_subtype="kill",
                topology=top,
                roles_cited=roles_t,
            )
        return PolicyAction(
            act=act,
            size_risk_percent=float(size),
            reason=f"brain_l2l act={act} conf={conf:.2f} agg={aggression:.2f} target~{target:.1f}",
            wait_subtype="",
            topology=top,
            roles_cited=roles_t,
        )

    def act(self, state: np.ndarray, **kwargs: Any) -> PolicyAction:
        return self.forward(state, **kwargs)

    def save(self, path: Path | str) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        b = self.brain
        np.savez_compressed(
            path,
            W1=b.W1,
            b1=b.b1,
            W2=b.W2,
            b2=b.b2,
            W_size=b.W_size,
            b_size=np.array([b.b_size]),
            seed=np.array([b.seed]),
            meta_train_steps=np.array([b.meta_train_steps]),
            trained=np.array([1 if b.trained else 0]),
            format=np.array([2]),  # brain format v2
        )
        meta = {
            "seed": b.seed,
            "meta_train_steps": b.meta_train_steps,
            "trained": b.trained,
            "fingerprint": b.weight_fingerprint(),
            "law": "A29_brain_l2l",
            "format": 2,
        }
        path.with_suffix(".json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        return path

    @classmethod
    def load(cls, path: Path | str, *, freeze: bool = True) -> "MetaPolicy":
        path = Path(path)
        data = np.load(path, allow_pickle=False)
        if "W1" not in data:
            raise RuntimeError(
                f"Champion at {path} is legacy linear format — retrain with meta-train (A29)"
            )
        brain = MetaBrain(
            W1=np.asarray(data["W1"], dtype=np.float64),
            b1=np.asarray(data["b1"], dtype=np.float64),
            W2=np.asarray(data["W2"], dtype=np.float64),
            b2=np.asarray(data["b2"], dtype=np.float64),
            W_size=np.asarray(data["W_size"], dtype=np.float64),
            b_size=float(data["b_size"][0]),
            seed=int(data["seed"][0]),
            meta_train_steps=int(data["meta_train_steps"][0]),
            trained=bool(int(data["trained"][0])),
            frozen_for_inference=False,
        )
        if not brain.trained or brain.meta_train_steps < 500:
            raise RuntimeError(f"Loaded brain not seriously trained: {path}")
        pol = cls(brain=brain)
        if freeze:
            pol.freeze_for_inference()
        return pol


FrozenMetaPolicy = MetaPolicy


def train_goal_conditioned_meta_policy(
    *,
    seed: int = 42,
    n_steps: int = 8000,
    lr: float = 0.025,
    targets: Sequence[float] = DEFAULT_TRAIN_TARGETS,
    risks: Sequence[float] = DEFAULT_TRAIN_RISKS,
    freeze: bool = True,
) -> MetaPolicy:
    """A29 serious training — multi-layer brain, L2L + London/NY drills."""
    del targets, risks  # curriculum fixed inside train_meta_brain
    brain = train_meta_brain(seed=seed, n_steps=n_steps, lr=lr, freeze=False)
    pol = MetaPolicy(brain=brain)
    pol.trained = True
    pol.meta_train_steps = brain.meta_train_steps
    if freeze:
        pol.freeze_for_inference()
    return pol


def load_or_train_champion(
    path: Optional[Path] = None,
    *,
    seed: int = 42,
    n_steps: int = 8000,
    force_retrain: bool = False,
) -> MetaPolicy:
    path = Path(path) if path else DEFAULT_CHAMPION_PATH
    cache_key = ("champ_brain", int(seed), str(path.resolve()))
    if not force_retrain and cache_key in _TRAINED_CACHE:
        return _TRAINED_CACHE[cache_key]._copy_frozen()
    if path.exists() and not force_retrain:
        try:
            pol = MetaPolicy.load(path, freeze=True)
            _TRAINED_CACHE[cache_key] = pol
            return pol._copy_frozen()
        except Exception:
            pass
    pol = train_goal_conditioned_meta_policy(seed=seed, n_steps=n_steps, freeze=True)
    pol.save(path)
    _TRAINED_CACHE[cache_key] = pol
    return pol._copy_frozen()


def weights_unchanged(before_fp: str, policy: MetaPolicy) -> bool:
    return before_fp == policy.weight_fingerprint() and policy.inference_updates == 0
