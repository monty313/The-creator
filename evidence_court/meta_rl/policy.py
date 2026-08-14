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
from .regimes import (
    RegimeId,
    build_official_for_regime,
    encode_regime_doctrine,
    regime_sensor_template,
    sample_curriculum_regime,
    teacher_action_under_regime,
)
from .risk import DailyRiskLedger, size_position_risk_percent
from .state import META_RL_DIM, build_meta_rl_state, extract_goal_risk_context
from .types import StructureFlags

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
    # Dynamic-size lab mode: size head output drives sizing directly
    # (fraction of remaining envelope). False = legacy aggression mapping.
    size_head_drives: bool = False
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
        pol = MetaPolicy(brain=b)
        pol.size_head_drives = bool(self.size_head_drives)
        return pol

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
        # Monty EO: intelligent size-up — higher aggression under goal pressure,
        # still clamped by envelope in size_position_risk_percent (breach 0).
        sig = 1.0 / (1.0 + np.exp(-size_logit))
        pressure = float(ctx[IDX_GOAL_PRESSURE]) if ctx.size > IDX_GOAL_PRESSURE else 0.5
        if self.size_head_drives:
            # Dynamic-size lab: the trained size head IS the size — a direct
            # fraction of remaining budget, hard-clamped by the envelope.
            budget = float(remaining) - 0.03  # friction reserve
            cap = min(budget, max_risk * 0.98)
            size = float(np.clip(sig, 0.05, 0.98)) * max(cap, 0.0)
            aggression = sig
        else:
            # High pressure / remaining risk → more of budget per leg (legal)
            aggression = float(
                np.clip(
                    0.45 + 0.50 * sig + 0.22 * target_norm + 0.25 * pressure * risk_rem,
                    0.25,
                    1.0,
                )
            )
            size = size_position_risk_percent(
                max_daily_risk_percent=max_risk,
                remaining_budget_percent=remaining,
                stop_distance_pct=0.35,
                target_percent=target,
                aggression=aggression,
                max_single_fraction=0.98,  # EO: nearly full remaining budget when needed
                friction_reserve_percent=0.03,
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
            size_head_drives=np.array([1 if self.size_head_drives else 0]),
        )
        meta = {
            "seed": b.seed,
            "meta_train_steps": b.meta_train_steps,
            "trained": b.trained,
            "fingerprint": b.weight_fingerprint(),
            "law": "A29_brain_l2l",
            "format": 2,
            "size_head_drives": bool(self.size_head_drives),
        }
        path.with_suffix(".json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        return path

    @classmethod
    def load(
        cls,
        path: Path | str,
        *,
        freeze: bool = True,
        require_serious: bool = True,
    ) -> "MetaPolicy":
        """Load brain weights. Production champion uses require_serious=True (A29).

        Experimental tracks (e.g. Policy Forge forge_v1) may pass
        require_serious=False to continue offline ingest before 500 steps.
        """
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
        if require_serious and (not brain.trained or brain.meta_train_steps < 500):
            raise RuntimeError(f"Loaded brain not seriously trained: {path}")
        pol = cls(brain=brain)
        if "size_head_drives" in data:
            pol.size_head_drives = bool(int(data["size_head_drives"][0]))
        if freeze:
            if brain.trained:
                pol.freeze_for_inference()
            else:
                pol.frozen_for_inference = False
        return pol


FrozenMetaPolicy = MetaPolicy


def sample_training_state(
    rng: Any,
    *,
    target: float = 15.0,
    risk: float = 2.0,
    regime: Any = None,
    return_regime: bool = False,
    london_ny: bool = False,
) -> Tuple[Any, ...]:
    """CASE-0017/0018 curriculum sample: A17 regime + doctrine pack + teacher.

    Shared layout with day-path encode_regime_doctrine (doctrine at state[32:48]).
    Returns (state, teacher_act, topology) or (+ regime) if return_regime.
    """
    rid = regime if regime is not None else sample_curriculum_regime(rng)
    if not isinstance(rid, RegimeId):
        rid = RegimeId(str(rid))

    tpl = regime_sensor_template(rid)
    force = float(tpl["force"])
    efficiency = float(tpl["efficiency"])
    side = 1 if force >= 0 else -1
    strength = abs(force) if abs(force) > 0.15 else float(rng.uniform(0.45, 0.95))

    official = build_official_for_regime(rid, rng=rng, side=side, strength=strength)
    # Curriculum: random HTF source flags so retrain can learn wind provenance
    # (doctrine[12:15]); correlated with trend regimes when force is strong.
    if rid in (RegimeId.TREND_BULL, RegimeId.TREND_BEAR, RegimeId.VOL_EXPANSION):
        slope_on = 1.0 if float(rng.random()) > 0.25 else 0.0
        cci_on = 1.0 if float(rng.random()) > 0.45 else 0.0
        rsi_on = 1.0 if float(rng.random()) > 0.45 else 0.0
        if slope_on + cci_on + rsi_on < 1.0:
            slope_on = 1.0
    else:
        slope_on = 1.0 if float(rng.random()) > 0.7 else 0.0
        cci_on = 1.0 if float(rng.random()) > 0.85 else 0.0
        rsi_on = 1.0 if float(rng.random()) > 0.85 else 0.0
    doctrine = encode_regime_doctrine(
        rid,
        force=force,
        efficiency=efficiency,
        slope_on=slope_on,
        cci_on=cci_on,
        rsi_on=rsi_on,
    )

    if rid in (RegimeId.TREND_BULL, RegimeId.TREND_BEAR, RegimeId.VOL_EXPANSION):
        topology = "launch" if float(rng.random()) > 0.35 else "release"
        pullback = topology == "launch"
    elif rid == RegimeId.TRANSITION:
        topology = "launch"
        pullback = True
    else:
        topology = "chop"
        pullback = False

    progress = float(rng.uniform(0.0, 0.65))
    realized = float(rng.uniform(0.0, float(risk) * 0.45))
    session = (
        float(rng.uniform(0.35, 0.85)) if london_ny else float(rng.uniform(0.0, 1.0))
    )

    st = build_meta_rl_state(
        target_percent=float(target),
        max_daily_risk_percent=float(risk),
        official=official,
        doctrine_vec=doctrine,
        structure=StructureFlags(pullback=pullback, scale_conflict=rid == RegimeId.CONFLICT),
        progress_to_target=progress,
        realized_risk_percent=realized,
        session_phase=session,
    )

    dirs: List[float] = []
    for sid in (1, 2, 3, 4):
        c = official.get(sid)
        if c is not None:
            dirs.append(float(int(c.direction)))
    mean_dir = float(np.mean(dirs)) if dirs else float(force)

    ctx = extract_goal_risk_context(st)
    allow = float(ctx[IDX_ALLOW_FIRE]) >= 0.5
    risk_rem = float(ctx[IDX_RISK_REMAINING])
    hardness = float(ctx[IDX_HARDNESS])
    pressure = float(ctx[IDX_GOAL_PRESSURE])
    if london_ny:
        pressure = min(1.0, pressure * 1.15)

    topo_for_teacher = "launch" if topology == "release" else topology
    teacher = teacher_action_under_regime(
        rid,
        mean_dir=mean_dir,
        allow=allow,
        risk_rem=risk_rem,
        hardness=hardness,
        pressure=pressure,
        topology=topo_for_teacher,
    )

    if return_regime:
        return st, teacher, topology, rid
    return st, teacher, topology


def teacher_action_for_state(
    state: np.ndarray,
    *,
    topology: str = "chop",
    regime: Any = None,
) -> str:
    """Optional A17-gated teacher from a built state (CASE-0017 pin)."""
    ctx = extract_goal_risk_context(state)
    allow = float(ctx[IDX_ALLOW_FIRE]) >= 0.5
    risk_rem = float(ctx[IDX_RISK_REMAINING])
    hardness = float(ctx[IDX_HARDNESS])
    pressure = float(ctx[IDX_GOAL_PRESSURE])
    # mean direction from first four set-dir slots (channel1 layout)
    s = np.asarray(state, dtype=np.float64).reshape(-1)
    dirs = [float(s[i * 3]) for i in range(4) if i * 3 < s.size]
    mean_dir = float(np.mean(dirs)) if dirs else 0.0

    rid: RegimeId
    if regime is not None:
        rid = regime if isinstance(regime, RegimeId) else RegimeId(str(regime))
    else:
        from .regimes import decode_regime_from_doctrine

        rid = decode_regime_from_doctrine(s[32:48] if s.size >= 48 else s)

    return teacher_action_under_regime(
        rid,
        mean_dir=mean_dir,
        allow=allow,
        risk_rem=risk_rem,
        hardness=hardness,
        pressure=pressure,
        topology=str(topology or "chop"),
    )


def opportunity_label_to_training_example(
    label: Dict[str, Any],
    *,
    target: float = 15.0,
    risk: float = 2.0,
    rng: Optional[Any] = None,
) -> Tuple[np.ndarray, str, float]:
    """C-002: Watch miss curriculum_label → (state, teacher_act, size_frac).

    London/NY labels get stronger size target. No live force — offline only.
    """
    gen = rng if rng is not None else np.random.default_rng(0)
    side = str(label.get("teacher_act") or label.get("side") or "wait")
    if side not in ("long", "short", "wait"):
        side = "wait"
    band = str(label.get("session_band") or "other")
    weight = float(label.get("weight") or (1.5 if band == "london_ny" else 1.0))
    topology = str(label.get("topology") or "pullback_resume")
    london = band == "london_ny" or weight >= 1.4

    # Prefer fire regimes aligned with teacher side
    if side == "long":
        rid = RegimeId.TREND_BULL
        force = 0.5
    elif side == "short":
        rid = RegimeId.TREND_BEAR
        force = -0.5
    else:
        rid = RegimeId.RANGE_CHOP
        force = 0.0

    official = build_official_for_regime(
        rid, rng=gen, side=1 if side != "short" else -1, strength=0.75
    )
    doctrine = encode_regime_doctrine(
        rid, force=force, efficiency=0.6 if side != "wait" else 0.35
    )
    pullback = "pullback" in topology
    session = float(gen.uniform(0.4, 0.8)) if london else float(gen.uniform(0.0, 1.0))
    st = build_meta_rl_state(
        target_percent=float(target),
        max_daily_risk_percent=float(risk),
        official=official,
        doctrine_vec=doctrine,
        structure=StructureFlags(pullback=pullback),
        progress_to_target=float(gen.uniform(0.0, 0.4)),
        realized_risk_percent=float(gen.uniform(0.0, risk * 0.3)),
        session_phase=session,
    )
    if side == "wait":
        return st, "wait", 0.0
    t_norm = (float(target) - 5.0) / 85.0
    size_frac = float(
        np.clip(0.5 + 0.35 * t_norm + (0.12 if london else 0.0), 0.25, 0.95)
    )
    return st, side, size_frac


def apply_opportunity_labels_to_brain(
    brain: MetaBrain,
    labels: Sequence[Dict[str, Any]],
    *,
    target: float = 15.0,
    risk: float = 2.0,
    lr: float = 0.02,
    seed: int = 7,
    max_labels: int = 500,
) -> int:
    """Offline: feed Watch miss labels into meta_update (C-002). Returns update count."""
    if brain.frozen_for_inference:
        brain.unlock_for_meta_train()
    rng = np.random.default_rng(seed)
    n = 0
    for lab in list(labels)[: int(max_labels)]:
        st, teacher, sf = opportunity_label_to_training_example(
            lab, target=target, risk=risk, rng=rng
        )
        w = float(lab.get("weight") or 1.0)
        brain.meta_update(
            st,
            teacher_act=teacher,
            lr=lr,
            reward=1.0 + 0.25 * min(w, 2.0),
            teacher_size_frac=sf if teacher != "wait" else 0.0,
        )
        n += 1
    brain.trained = True
    return n


def silent_day_opportunity_curriculum(n: int = 64) -> List[Dict[str, Any]]:
    """CASE-0035: denser offline miss curriculum for silent-day unlock (C-002 residual).

    Synthetic Watch-class labels: multi-set HTF-agree PB/cont teachers, London/NY
    weighted. Offline only — never live force-pad. Used to retrain a *shadow*
    champion for dual measure; does not overwrite PROVEN until PROMOTE.
    """
    n = max(1, int(n))
    topos = ("pullback_resume", "continuation")
    sides = ("long", "short")
    # London/NY active band times + a few other-band controls
    times_ln = (
        "08:00:00",
        "09:30:00",
        "10:00:00",
        "11:00:00",
        "13:00:00",
        "14:00:00",
        "15:00:00",
        "16:00:00",
    )
    times_other = ("03:00:00", "05:00:00", "21:00:00")
    labels: List[Dict[str, Any]] = []
    i = 0
    while len(labels) < n:
        topo = topos[i % len(topos)]
        side = sides[(i // 2) % len(sides)]
        use_ln = (i % 5) != 0  # ~80% London/NY
        t = times_ln[i % len(times_ln)] if use_ln else times_other[i % len(times_other)]
        band = "london_ny" if use_ln else "other"
        w = 1.5 if use_ln else 1.0
        force = 0.42 if side == "long" else -0.42
        labels.append(
            {
                "teacher_act": side,
                "topology": topo,
                "session_band": band,
                "weight": float(w),
                "symbol": "XAUUSD" if (i % 3) == 0 else ("EURUSD" if (i % 3) == 1 else "GBPUSD"),
                "set_id": int(1 + (i % 4)),
                "sense_gap": "sight",
                "what_bot_did": "wait",
                "asof_date": "2026-02-01",
                "asof_time": t,
                "force": float(force),
                "complaint_id": f"CASE0035-syn-{i:04d}",
                "multi_set_agree": True,
            }
        )
        i += 1
    return labels


def train_silent_day_opportunity_policy(
    *,
    seed: int = 42,
    n_steps: int = 2500,
    n_labels: int = 64,
    opportunity_mix: float = 0.25,
    freeze: bool = True,
    save_path: Optional[Path] = None,
) -> MetaPolicy:
    """CASE-0035: train shadow policy with silent-day opportunity curriculum.

    Does **not** write DEFAULT_CHAMPION_PATH unless save_path points there.
    """
    labs = silent_day_opportunity_curriculum(n_labels)
    pol = train_goal_conditioned_meta_policy(
        seed=seed,
        n_steps=n_steps,
        freeze=freeze,
        opportunity_labels=labs,
        opportunity_mix=opportunity_mix,
    )
    if save_path is not None:
        pol.save(Path(save_path))
    return pol


def train_goal_conditioned_meta_policy(
    *,
    seed: int = 42,
    n_steps: int = 8000,
    lr: float = 0.025,
    targets: Sequence[float] = DEFAULT_TRAIN_TARGETS,
    risks: Sequence[float] = DEFAULT_TRAIN_RISKS,
    freeze: bool = True,
    opportunity_labels: Optional[Sequence[Dict[str, Any]]] = None,
    opportunity_mix: float = 0.15,
) -> MetaPolicy:
    """A29 serious training — multi-layer brain, L2L + London/NY + optional Watch labels (C-002)."""
    del targets, risks  # base curriculum fixed inside train_meta_brain
    brain = train_meta_brain(seed=seed, n_steps=n_steps, lr=lr, freeze=False)
    # C-002: mix opportunity miss labels into trained brain (offline only)
    if opportunity_labels:
        apply_opportunity_labels_to_brain(
            brain,
            opportunity_labels,
            lr=lr * 0.9,
            seed=seed + 11,
            max_labels=max(50, int(len(opportunity_labels))),
        )
        # Extra mix steps: re-sample labels into remaining curriculum feel
        rng = np.random.default_rng(seed + 3)
        n_extra = max(1, int(n_steps * float(opportunity_mix)))
        labs = list(opportunity_labels)
        for i in range(n_extra):
            lab = labs[int(rng.integers(0, len(labs)))]
            st, teacher, sf = opportunity_label_to_training_example(
                lab,
                target=float(rng.choice(DEFAULT_TRAIN_TARGETS)),
                risk=float(rng.choice(DEFAULT_TRAIN_RISKS)),
                rng=rng,
            )
            brain.meta_update(
                st,
                teacher_act=teacher,
                lr=lr * (0.95 ** (i // 50)),
                reward=1.15,
                teacher_size_frac=sf if teacher != "wait" else 0.0,
            )
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
