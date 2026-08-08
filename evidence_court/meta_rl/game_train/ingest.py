"""Ingest Policy Forge exports into MetaBrain via offline meta_update (A14/A29)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np

from evidence_court.meta_rl.policy import MetaPolicy, load_or_train_champion
from evidence_court.meta_rl.state import META_RL_DIM

ACTS = {"wait", "long", "short"}


@dataclass
class IngestReport:
    n_traj: int
    n_applied: int
    skipped: int
    meta_train_steps_before: int
    meta_train_steps_after: int
    fingerprint_before: str
    fingerprint_after: str
    saved: Optional[str]
    mean_loss: float


def load_pack(path: Path | str) -> Dict[str, Any]:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") not in ("policy_forge_game_train_v1", "policy_forge_v1"):
        # still accept if trajectories present
        if "trajectories" not in data:
            raise ValueError(f"Unknown pack format: {data.get('format')}")
    return data


def _pad_state(raw: Sequence[float]) -> np.ndarray:
    s = np.asarray(raw, dtype=np.float64).reshape(-1)
    out = np.zeros(META_RL_DIM, dtype=np.float64)
    n = min(META_RL_DIM, int(s.size))
    out[:n] = s[:n]
    return out


def ingest_game_pack(
    pack_path: Path | str,
    *,
    champion_path: Optional[Path | str] = None,
    out_path: Optional[Path | str] = None,
    lr: float = 0.02,
    max_steps: Optional[int] = None,
    seed: int = 42,
    include_browser_brain_warmstart: bool = False,
) -> IngestReport:
    """Offline: unlock champion → meta_update on each trajectory → freeze → save.

    This is **not** inference retrain. Target/risk remain context in state.
    """
    pack = load_pack(pack_path)
    trajs: List[Dict[str, Any]] = list(pack.get("trajectories") or [])
    if max_steps is not None:
        trajs = trajs[: int(max_steps)]

    champ_p = Path(champion_path) if champion_path else None
    try:
        pol = load_or_train_champion(champ_p, seed=seed, force_retrain=False)
    except Exception:
        pol = MetaPolicy.untrained_prior(seed=seed)

    # Optional: if pack embeds browser weights and champion is young, warm-start
    brain_snap = pack.get("brain")
    if (
        include_browser_brain_warmstart
        and isinstance(brain_snap, dict)
        and brain_snap.get("format") == 2
        and pol.meta_train_steps < 500
        and brain_snap.get("meta_train_steps", 0) >= 50
    ):
        from evidence_court.meta_rl.brain import MetaBrain

        b = MetaBrain(
            W1=np.asarray(brain_snap["W1"], dtype=np.float64).reshape(64, META_RL_DIM),
            b1=np.asarray(brain_snap["b1"], dtype=np.float64).reshape(64),
            W2=np.asarray(brain_snap["W2"], dtype=np.float64).reshape(3, 64),
            b2=np.asarray(brain_snap["b2"], dtype=np.float64).reshape(3),
            W_size=np.asarray(brain_snap["W_size"], dtype=np.float64).reshape(64),
            b_size=float(brain_snap.get("b_size", 0.0)),
            seed=int(brain_snap.get("seed", seed)),
            meta_train_steps=int(brain_snap.get("meta_train_steps", 0)),
            trained=bool(brain_snap.get("trained", True)),
            frozen_for_inference=False,
        )
        pol = MetaPolicy(brain=b)

    pol.unlock_for_meta_train()
    fp_before = pol.weight_fingerprint()
    steps_before = int(pol.meta_train_steps)

    losses: List[float] = []
    applied = 0
    skipped = 0
    for row in trajs:
        act = str(row.get("teacher_act") or row.get("act") or "wait")
        if act not in ACTS:
            skipped += 1
            continue
        state = _pad_state(row.get("state") or [])
        if state.size != META_RL_DIM:
            skipped += 1
            continue
        reward = float(row.get("reward", 1.0))
        size = row.get("teacher_size_frac")
        size_f = float(size) if size is not None else None
        loss = pol.meta_update(
            state,
            teacher_act=act,
            lr=lr,
            reward=reward,
            teacher_size_frac=size_f,
        )
        losses.append(float(loss))
        applied += 1

    pol.freeze_for_inference()
    fp_after = pol.weight_fingerprint()
    saved: Optional[str] = None
    dest = Path(out_path) if out_path else (
        Path(champion_path) if champion_path else Path("evidence_court/artifacts/meta_policy_champion.npz")
    )
    if applied > 0:
        saved = str(pol.save(dest))
        # also write sidecar pack receipt
        receipt = dest.with_name(dest.stem + "_game_ingest.json")
        receipt.write_text(
            json.dumps(
                {
                    "source_pack": str(pack_path),
                    "n_traj": len(trajs),
                    "n_applied": applied,
                    "skipped": skipped,
                    "meta_train_steps": pol.meta_train_steps,
                    "fingerprint": fp_after,
                    "law": "A14_offline_game_ingest_not_inference_retrain",
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    return IngestReport(
        n_traj=len(trajs),
        n_applied=applied,
        skipped=skipped,
        meta_train_steps_before=steps_before,
        meta_train_steps_after=int(pol.meta_train_steps),
        fingerprint_before=fp_before,
        fingerprint_after=fp_after,
        saved=saved,
        mean_loss=float(np.mean(losses)) if losses else 0.0,
    )
