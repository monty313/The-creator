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
  → updates evidence_court/artifacts/meta_policy_champion.npz  (or forge_v1 branch)
  → prove / forward100 unchanged contract (frozen inference)
```

## Fast loop (use this)

One command after you Export from the browser:

```bash
python -m evidence_court.meta_rl.cli forge go
```

That will:
1. **pull** exports from Downloads / `artifacts/` → `artifacts/game_train/`
2. **ingest** newest pack into **forge_v1 only** (champion untouched)
3. **score** fast (coach + opportunity + **8-day** forward, forge only)

| Command | What |
|---------|------|
| `forge go` | pull + ingest + fast score |
| `forge play` | open Policy Forge in browser |
| `forge pull` | only move/copy exports into game_train |
| `forge ingest` | only ingest newest pack |
| `forge score` | only fast score (`--days 8`, add `--vs-champion` if needed) |
| `forge status` | packs + forge steps |
| `forge train-v2` | Balanced force/load/launch → `meta_policy_forge_v2.npz` |
| `forge train-intense` | **Unhinged** train-time fire flood → `meta_policy_forge_intense.npz` |
| `forge train-learn` | **Learn not memorize** — unique teachers, holdout dates, L2L+goal aug → `meta_policy_forge_learn.npz` |
| `forge train-residual` | Residual: real path-state at Watch PB/cont misses (no multi-hit) → `meta_policy_forge_residual.npz` |

### forge_v2 (decision curriculum — not inference thrash)

Problem with v1: copied coach WAIT on game states; quiet on real path.  
**Wrong fix:** force long/short every bar at prove (pad thrash).  
**Right fix:** train-time rebalance — fire + load-wait + synthetic London/NY opportunity.

```bash
python -m evidence_court.meta_rl.cli forge train-v2 --steps 4000
```

### forge_intense (unhinged train-time aggression)

Starve WAIT CE. Flood fire offline: CASE-0036 real-bar PB/cont (multi-hit), pack
launch/LN-NY, guaranteed London/NY force_opp synth, pure-fire blitz blocks.
Never pad at inference. Champion untouched. Measure forward a13/n_zero — not coach CE.

```bash
python -m evidence_court.meta_rl.cli forge train-intense --steps 12000
# optional: --fire-frac 0.75 --real-bar-frac 0.45 --multi-hit 16 --warmstart-v2
```

### forge_learn (learn principles — not memorize answers)

Anti multi-hit. Unique path teachers only; **hold out dates**; each step **augments**
(goal×risk re-encode, L2L set permute, light noise). Principle synth + load-wait
contrast. Reports train vs hold agreement + mem_gap. Champion safe.

```bash
python -m evidence_court.meta_rl.cli forge train-learn --steps 30000
# optional: --noise 0.05 --holdout-frac 0.25 --path-frac 0.40
```

Keys in game: **A** long · **S** wait · **D** short · **C** coach · **N** next · **E** export.

Play tip: London/NY **launch/release** fire days; one Export at end of a run.

## Manual launch / CLI (legacy)

```bash
python evidence_court/meta_rl/game_train/launch_policy_forge.py

python -m evidence_court.meta_rl.cli game-ingest path/to/policy_forge_export.json \
  --out evidence_court/artifacts/game_train/meta_policy_forge_v1.npz \
  --lr 0.02
```

First pack on a new forge track: add `--from-prior`. Later packs omit it.

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
