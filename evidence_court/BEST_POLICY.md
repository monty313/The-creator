# BEST POLICY (production champion) — SSOT

**Status:** ACTIVE production brain  
**Do not confuse** with shadows, backups, or `game_train/*` experiments.

---

## Identity (this is the one)

| Field | Value |
|-------|--------|
| **Name** | CASE-0037 path-state champion |
| **Ruling** | **PROMOTE_NARROW** (density lever; **not** final boss) |
| **Weights** | `artifacts/meta_policy_champion.npz` |
| **Sidecar** | `artifacts/meta_policy_champion.json` |
| **Fingerprint** | `42:meta4275:inf0:bcfe6c74f68b7623` |
| **Meta-train steps** | 4275 |
| **Seed** | 42 |
| **Law class** | A14 trained meta-policy · A29 brain · frozen at inference |
| **Case file** | `cases/CASE-0037-path-state-teachers.md` |
| **Report** | `artifacts/forward100_report_case0037.json` |
| **Report SHA256** | `2e5533de02447d95149a04322a07f7c8030a1c6cfa6d1f1c3a669965db311515` |

**Same weights also saved as:**  
`artifacts/meta_policy_case0037_pathstate.npz` (source of promote; identical fingerprint).

**Load path (code):** `load_or_train_champion()` → `meta_policy_champion.npz`  
**CLI:** `python -m evidence_court.meta_rl.cli prove 15 2`

---

## What it is

- Multi-layer **MetaBrain** deciding wait / long / short + size from **packed 176-dim state**
- Production path: `brain_drives=True`, Watch observe-only (no live force-pad)
- Trained: base meta curriculum + **400 packed path-state teachers** (brain-wait → Mark side fire), 362 London/NY
- **Frozen** at prove/forward — target/risk change does **not** retrain weights

---

## Measured dual floor (seed=42, 100d) — do not regress without measure

| Metric | Value |
|--------|------:|
| hits (target-win days) | **11** |
| target-win rate (all days) | **11%** |
| low_hr | **0.28** |
| a13_frac | **0.64** |
| n_zero | **18** |
| mean_tr | **39.4** |
| green days (PnL > 0) | **47 / 100** |
| max_pnl | **70** |
| breach | **0** |
| no_retrain | **true** |
| promote_ready | **false** |

Day trade buckets: **0:** 18 · **1–7:** 18 · **8–400:** 64 · **>400:** 0

---

## What it is NOT (avoid confusion)

| Artifact | Role | Status |
|----------|------|--------|
| `meta_policy_champion_pre0037.npz` | **Backup only** (pre-promote, fp meta9600) | Not production |
| `meta_policy_case0035_opp.npz` | Synthetic opp shadow | **REJECT F-024** |
| `meta_policy_case0036_realbar.npz` | Real-bar label shadow | **REJECT F-025** |
| `artifacts/game_train/*.npz` | A34 game-ingest / lab | Not dual-promoted champion |
| Old `forward100_report.json` (meta2862) | Prior dual snapshot | Superseded floor |

**Forbidden as “the bot”:** untrained seed stub · hard-rule soup as decider · F-024/F-025 label→synthetic-state densify as win law.

---

## Gaps (why not final boss)

- Target clears still **11/100** (C-004 open)
- Not every-day A13 (18 zero + 18 partial) — C-003 residual
- High-target band weak; `promote_ready` false
- Full senses-drive series (CASE-0032…0034) not complete

---

## How THIS policy learns (simple SSOT)

**Learning = offline practice, then freeze.**  
Never “retrain while proving.” Target% / risk% only change **state**, not weights (A14).

### One picture

```text
1. Harvest  →  real path states where the brain WAITED but Mark had a fire edge
2. Teach    →  offline meta_update: those states → Mark side (long/short)
3. Freeze   →  champion weights locked for prove / forward100
4. Measure  →  dual must hold floor (hits / low_hr / a13 / breach 0)
5. Promote  →  only Court PROMOTE may replace this file’s weights
```

### What already taught the champion (CASE-0037)

| Piece | Meaning |
|-------|---------|
| **Where** | Exact **packed 176-dim** state the brain saw on the day path |
| **When** | Brain said **wait**, but Mark candidate was pullback/continuation |
| **What** | Teacher = Mark **side** (long/short) — not player thrash |
| **Weight** | London / NY prioritized |
| **Result** | a13 **0.28 → 0.64**, n_zero **39 → 18**, hits/low_hr held |

That is the **road**: teach on **visited path states**, not rebuilt fake states.

### What “learn more” means next (same class only)

| Goal | How to learn (allowed) | Not allowed |
|------|------------------------|-------------|
| Fewer silent days | More path-state harvest on zero/1–7 trade days | Force every bar live |
| Better high trend | Teachers = HTF force + LTF **load→launch** on **all 4 sets** | Fade trend / chase mid-leg labels as truth |
| More clears | Path teachers that size/hold toward target under risk | Exit-floor soup as brain |
| Multi-set skill | Same law on Set1…4 roles; multi-set agree = confidence | Average all TFs into mush “force” |

**Skill to master (human + curriculum):**  
Sight force → Feel load → Taste launch → Hearing consensus — on **every official set**.

### What must NEVER teach the champion

| Bad teacher class | Why |
|-------------------|-----|
| **F-024** synthetic densify | Active-day thrash; n_zero worse |
| **F-025** real label + **fake rebuilt state** | Wrong state distribution |
| **Game wait-copy** (`game_train` forge_v1 raw) as sole diet | Learns “WAIT wins CE”; quiet on path |
| Live force-pad trades | Fake A13; not learning |
| Untrained seed / hard-rule soup as decider | Not this policy |

**Lab only (not this SSOT until PROMOTE):**  
`artifacts/game_train/meta_policy_forge_v*.npz` — A34 practice tracks.  
May **inspire** curriculum design; must pass **path dual** before they can become BEST POLICY.

### Simple commands (measure only — no silent replace)

```text
# Identity check
python -m evidence_court.meta_rl.cli prove 15 2

# Full dual (slow) — compare to floor in this file
python -m evidence_court.meta_rl.cli forward100 --days 100 --out evidence_court/artifacts/forward100_report.json
```

**Replace champion weights only after:** Court case + dual vs this floor + update **this file** (fp + steps + report hash).

### Learning checklist (before claiming “smarter bot”)

- [ ] Teachers are **path-packed states** (176-dim), not names-only labels  
- [ ] Teachers include **London/NY** high-trend load→launch  
- [ ] Wait still correct on true load / conflict (not zero-wait thrash)  
- [ ] Shadow dual: breach **0**, no_retrain **true**  
- [ ] Prefer: hits ≥ **11**, low_hr ≥ **0.28**, a13_frac ≥ **0.64** (or Court re-floor)  
- [ ] This file updated on PROMOTE  

---

## When this file must be updated

1. Any **PROMOTE** that replaces `meta_policy_champion.npz`  
2. Any dual that sets a **new scoreboard floor**  
3. Any **rollback** to backup (document why + new fp)

**Checkpoint cross-link:** `CONTINUATION_CHECKPOINT.md`  
**Docket:** `ISSUE_DOCKET.md`  
**Architecture note:** `MASTER_ARCHITECTURE.md` (CASE-0037 section)  
**Senses / high-trend mastery (learn, don’t memorize):** `meta_rl/game_train/00_HIGH_TREND_MASTERY.html`

---

*Last updated: 2026-08-08 — CASE-0037 PROMOTE_NARROW + how-it-learns SSOT*
