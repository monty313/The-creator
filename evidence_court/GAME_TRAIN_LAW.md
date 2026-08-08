# GAME TRAIN LAW — Additive (Law A34)

**Status:** PERMANENT (Monty) · Promoted 2026-08-07 as **Law A34**  
**Depends on:** A14, A29, A31, A32, A33

## Law

Human-in-the-loop **Policy Forge** gameplay may produce training trajectories that
**offline** improve the meta-policy toward the mission (any target×risk, breach 0,
A13 density, senses-drive-brain). Ingest is **meta_update only while unlocked** —
never a substitute for frozen inference when target/risk changes.

| Required | Forbidden |
|----------|-----------|
| Export includes META_RL_DIM states + teacher_act | Calling browser play "live retrain at prove" |
| Ingest via `game-ingest` then freeze | Mutating champion during forward100/prove |
| Goal axes on each trajectory | Freestyle labels with no sense/goal context |
| Court still measures dual/A13 for promote | Skipping Court because the game felt good |

## Issue generation

If game align-rate is high but dual conversion is low → spawn residual **G-CLEAR**
curriculum issues. If game fires density but a13_frac low on real bars → **G-A13**
real-bar path (C-003). Game is a **road**, not the final boss.

Canonical: `meta_rl/game_train/README.md`
