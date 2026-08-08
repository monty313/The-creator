# Policy Forge → MetaBrain (additive game-train)

## What this is

**Doctrine:** teach **principles** (sight/feel/taste/hearing + goal context)
via **soft labels** — never hard if/then recipes. Risk envelope is the only hard safety.

A **browser trading game** trains a real MetaBrain (176-dim state, wait/long/short)
using sense-aligned teacher labels (A32) under any target×risk (A31). Export packs
fold into the champion **offline** with `meta_update` — never weight updates at
inference when Monty changes target/risk.

## Flow

```text
Policy Forge (browser)
  → decisions + state vectors + teacher_act
  → export policy_forge_export_*.json
  → python -m evidence_court.meta_rl.cli game-ingest path/to/export.json
  → updates evidence_court/artifacts/meta_policy_champion.npz
  → prove / forward100 unchanged contract (frozen inference)
```

## CLI

```bash
python -m evidence_court.meta_rl.cli game-ingest path/to/policy_forge_export.json \
  --out evidence_court/artifacts/meta_policy_champion.npz \
  --lr 0.02
```

Optional: `--warmstart-browser-brain` only if champion is young (`meta_train_steps < 500`).

## Pack schema (v1)

```json
{
  "format": "policy_forge_game_train_v1",
  "meta_rl_dim": 176,
  "brain": { "W1": [...], "format": 2, "source": "policy_forge_browser" },
  "trajectories": [
    {
      "state": [/* 176 floats */],
      "teacher_act": "long|short|wait",
      "teacher_size_frac": 0.0,
      "reward": 1.2,
      "target_percent": 15,
      "max_daily_risk_percent": 2,
      "goal_axes": ["G-CLEAR", "G-TRAIN", "G-SIGHT", "..."]
    }
  ]
}
```

## Court linkage

- **C-001 / C-002 / C-005** — Watch/senses labels + real curriculum
- Laws **A31–A33**, **A14**, **A29**, **A32**
- Does **not** replace Full Court measurement for promote_ready
