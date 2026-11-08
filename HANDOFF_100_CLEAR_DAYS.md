# HANDOFF — Reach 100 clear days

**For:** next agent / session
**Authority:** Monty · **Enforcer:** SEAN
**Updated:** 2026-08-12
**goal_achieved:** **false**

Read this first when continuing the **100 clear-day** mission. Do not invent a softer goal.

> **REPO SYNC NOTE (cloud, 2026-08-12):** This handoff was filed into the repository verbatim by a
> cloud session for durable retention (A33). The session state it references (king `meta5465`,
> size-budget recipes, SEAN orders, cycle JSONs) exists on Monty's local machine and is **not yet
> pushed** to this repository. See `evidence_court/REPO_SYNC_AUDIT_2026-08-12_HANDOFF_100D.md`
> before acting on any path in this file.

---

## 0) The only win condition

```text
WIN = measured 100-day dual (random target∈[5,90] × risk∈[1,3], same frozen weights):
  • CLEAR DAYS → climb toward 100 (hit typed target that day)
  • BREACH DAYS = 0
  • NO RETRAIN at prove when target/risk changes (A14)
  • SCALPER: trades/day ∈ [8, 400] on production path (A13)
  • Method: FORCE → PULLBACK → CONTINUATION (not densify pad)
```

**Owner bar to install a new king:** `hits > live king hits` · **breach 0** — nothing else.
Full orders: `evidence_court/SEAN_GOAL_ORDERS.md` · thrash catalog: `SEAN/NEVER_AGAIN.md`

---

## 1) Where we are (honest)

| Layer                                   | Status                                                                                  |
| --------------------------------------- | --------------------------------------------------------------------------------------- |
| **Production king**               | **SIZE UNTIL WIN** · Day-12 **15% CLEAR · breach 0**                      |
| **Weights**                       | `evidence_court/artifacts/meta_policy_champion.npz`                                   |
| **Fingerprint**                   | `42:meta5465:inf0:33bffec3f1c84656`                                                   |
| **SSOT**                          | `evidence_court/BEST_POLICY.md`                                                       |
| **Predecessor (learn-from only)** | meta4275 · old forward100**11 hits** · **NOT king**                       |
| **Rank-1 gap**                    | **Day conversion** under random T×R — fires exist; days rarely hit typed target |
| **Fast sensor protocol**          | `forward40_random_seed42_XAU_end2026-05-26` (XAU-only, end pin `2026-05-26`)        |
| **North-star protocol**           | `forward100_random_seed42_end2026-05-26` (multi-sym when ready)                       |

### Live scoreboard (40d sensor — same dual for all climb cycles)

| Who                                                  |           hits |      breach | mean_pnl | mean_tr | fingerprint | verdict            |
| ---------------------------------------------------- | -------------: | ----------: | -------: | ------: | ----------- | ------------------ |
| **King**                                       | **1**/40 | **0** |   ~0.895 |   ~18.2 | meta5465    | crowned            |
| Throne climb size (`meta7957`)                     |           1/40 |           0 |   ~0.894 |   ~18.2 | meta7957    | KEEP lab           |
| **size_budget_goal_curriculum** (`meta8465`) | **1**/40 | **0** |   ~0.785 |   ~22.6 | meta8465    | **KEEP lab** |

**Distance to 100:** sensor shows **~1 clear / 40** ≈ **~2–3% hit rate**. Path is conversion under envelope, not method rewrite.

---

## 2) What this session already did (do not redo blindly)

### A) Internet Counsel (A15) — filed

| Artifact     | Path                                                                       |
| ------------ | -------------------------------------------------------------------------- |
| Counsel sift | `evidence_court/artifacts/day12/sean_goal/COUNSEL_100D_INTERNET_SIFT.md` |
| Cache row    | `ledger/COUNSEL_CACHE.jsonl` topic `sean_100d_conversion_counsel`      |

**Recommendation class:** conversion = **size under remaining risk budget** + **goal-conditioned / GOID curriculum** + **target-benchmark reward** — **not** entry densify. Aligns with SIZE UNTIL WIN king.

Research classes mapped: CMDP episode-wise safety · fractional Kelly · meta-RL task dist · GOID · TSCL teacher-student · RiskawareTrader target reward.

### B) ONE recipe run — flat dual #1

| Field       | Value                                                                  |
| ----------- | ---------------------------------------------------------------------- |
| Recipe      | `size_budget_goal_curriculum`                                        |
| Code        | `python -m evidence_court.meta_rl.train_size_budget_goal_curriculum` |
| Lab weights | `artifacts/policies_lab/meta_policy_size_budget_goal_curriculum.npz` |
| Train       | 3000 size-overkill · 194 teachers (14 Day-12 + 180 GOID)              |
| Dual        | 40d XAU · hits**1** · breach **0**                       |
| Decision    | **KEEP_lab_no_install** (hits ≯ king)                           |
| Cycle JSON  | `artifacts/size_budget_goal_curriculum/CLIMB_CYCLE.json`             |
| Ledger      | `EVIDENCE_LEDGER.jsonl` event `SIZE_BUDGET_GOAL_CURRICULUM_CYCLE`  |

**Read:** trades denser (18→23), hits flat, mean_pnl slightly down → **not progress on owner bar**. Do not call denser trades a win.

### C) Prior climb (same day, earlier)

| Field  | Value                                                         |
| ------ | ------------------------------------------------------------- |
| Recipe | `train_size_until_win` throne climb                         |
| Lab    | `policies_lab/meta_policy_throne_climb_size.npz` (meta7957) |
| Cycle  | `artifacts/throne_climb/CLIMB_CYCLE.json`                   |
| Result | 1 hit · breach 0 · KEEP                                     |

---

## 3) Loop position (SEAN §5)

```text
A MEASURE   ✓  king 1/40 · challengers 1/40 · breach 0
B DIAGNOSE  ✓  conversion / size under random T×R (not densify)
C CV2 LOOK  ○  not run this cycle (optional next if path stuck)
D TRAIN     ✓  size_budget_goal_curriculum (dual #1 flat)
E RE-MEASURE✓  same 40d protocol
F KEEP/DISC ✓  KEEP lab · no install
G DETHRONE  ○  no — hits not greater
H SWITCH    →  dual #1 only; ONE more coherent size-budget variant allowed
               if dual #2 still flat → SWITCH recipe class (path mult / stuck-day)
```

**Recipe strike count:** `size_budget_goal_curriculum` = **1 dual, no hit gain**.
After **2** flats → stop this recipe class (SEAN H).

---

## 4) Next efficient moves (ordered)

Do **one** at a time. Measure after each.

### Option 1 — Dual #2 of size-budget class (allowed once)

Tweak **student**, not entries:

- Path-level **stuck-day size mult retry** at measure time (`mission_100_random` style `stuck_mult_retry`) **and/or**
- Stronger **remaining-risk** size teachers harvested from **near-clear** real days (not only synth GOID)
- Keep act head frozen; no densify CE flood

```text
# remeasure lab only
python -m evidence_court.meta_rl.train_size_budget_goal_curriculum --measure-only --weights evidence_court/artifacts/policies_lab/meta_policy_size_budget_goal_curriculum.npz --king-hits 1

# or retrain with stronger recipe then same 40d
python -m evidence_court.meta_rl.train_size_budget_goal_curriculum --steps 3000 --days 40 --king-hits 1
```

### Option 2 — Switch if dual #2 flat (preferred switch class)

| Switch to                                                                        | Why                                                       |
| -------------------------------------------------------------------------------- | --------------------------------------------------------- |
| **Path `TRADE_SIZE_MULT` / intelligent_size_toward_clear** on stuck days | Day-12 win was path size mult, not only offline size head |
| **Harvest size teachers from real dual fills** (miss days → climb frac)   | Synth GOID may not transfer to XAU window                 |
| **CV2 Outer light: left_R / size only** (not thrash-heavy CE)              | Lab history: conversion CE mix**8→6 REJECT**       |

### Option 3 — North-star when 40d hits climb

Only after 40d sensor prints **hits > 1** (or clear lift):

```text
python -m evidence_court.meta_rl.mission_100_random --baseline
# or forward100 with champion_path + window_end_date 2026-05-26
```

Do **not** thrash 100d as a vanity loop while 40d stuck at 1.

### Install rule (never silent)

```text
IF measured hits > king hits AND breach == 0:
  install champion + rewrite BEST_POLICY
ELSE:
  KEEP lab only
```

---

## 5) Environment / how to run

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& "c:\Users\user\OneDrive\Desktop\The Creator\.venv\Scripts\Activate.ps1"
cd "c:\Users\user\OneDrive\Desktop\The Creator"
```

| Task               | Command                                                                                                     |
| ------------------ | ----------------------------------------------------------------------------------------------------------- |
| King identity      | `python -m evidence_court.meta_rl.cli prove 15 2`                                                         |
| Size-budget cycle  | `python -m evidence_court.meta_rl.train_size_budget_goal_curriculum --steps 3000 --days 40 --king-hits 1` |
| Classic size teach | `python -m evidence_court.meta_rl.train_size_until_win --steps 2000`                                      |
| 100d mission       | `python -m evidence_court.meta_rl.mission_100_random --baseline`                                          |

---

## 6) Pillars (must all agree)

| Pillar             | Owner | SSOT                                                                     |
| ------------------ | ----- | ------------------------------------------------------------------------ |
| Method F→PB→CONT | Mark  | `00_POLICY_CREATION/01_METHOD.md`                                      |
| How to learn       | Aaron | `00_POLICY_CREATION/02_LEARNING.md` · `Aaron_here/`                 |
| Goal / thrash      | SEAN  | `00_POLICY_CREATION/03_GOAL_CONSISTENCY.md` · `SEAN_GOAL_ORDERS.md` |

Front door: `00_POLICY_CREATION/00_READ_FIRST.md`

---

## 7) Forbidden (kill on sight)

| Trick                                            | Why                                        |
| ------------------------------------------------ | ------------------------------------------ |
| Densify entries when method green                | Wrong student — size was Day-12 win lever |
| Soft lot mult ceilings / mult theater            | Size not real under envelope               |
| Multi-metric dethrone veto                       | Owner bar = hits + breach only             |
| Silent champion overwrite                        | Court / O1+O2 dual first                   |
| Call meta4275 “the king”                       | Predecessor only                           |
| Fixed 15/3 dual-loop as substitute for 100d GOAL | Thrash                                     |
| CV2 thrash-heavy conversion CE                   | Already measured**8→6 REJECT**      |
| Docs-only “done” with hits flat                | No scoreboard                              |
| Parallel tip wars                                | One recipe · one measure · write JSON    |

Full: `SEAN/NEVER_AGAIN.md` · `00_POLICY_CREATION/04_ANTI_THRASH.md` · Day-12 arc `artifacts/day12/SEAN_WHAT_WORKED_AND_LLM_TRAPS.md`

---

## 8) Pin map (read order for next session)

```text
1. This file — HANDOFF_100_CLEAR_DAYS.md
2. 00_POLICY_CREATION/00_READ_FIRST.md
3. evidence_court/BEST_POLICY.md          (who is king)
4. evidence_court/SEAN_GOAL_ORDERS.md     (loop A→H)
5. SEAN/NEVER_AGAIN.md                    (do not repeat traps)
6. artifacts/size_budget_goal_curriculum/CLIMB_CYCLE.json   (last dual)
7. artifacts/throne_climb/CLIMB_CYCLE.json                  (prior dual)
8. artifacts/day12/sean_goal/COUNSEL_100D_INTERNET_SIFT.md  (internet map)
9. meta_rl/SIZE_UNTIL_WIN_LAW.md
10. mark_here/knowledge/lab/GOAL.md
```

---

## 9) One-sentence rank-1 for the next agent

> **Conversion:** same F→PB→CONT method must hit typed targets more often under random T×R by **sizing under the risk envelope and teaching that size** — offline GOID size-head alone did not lift 40d hits above 1; next move is path-level size-until-win on stuck days or real-fill size harvest, then re-measure the **same 40d protocol**, install only if hits strictly rise at breach 0, then climb the 100d north-star dual toward **100 clear days**.

---

## 10) Session end checklist (when you work next)

```text
[ ] Load this handoff + SEAN orders + NEVER_AGAIN
[ ] State king fp (must be meta5465 until dual beats it)
[ ] Name one recipe in one sentence
[ ] Train offline OR path measure — not both thrash paths
[ ] Same 40d sensor first
[ ] Write JSON under artifacts/ + ledger if material
[ ] KEEP/DISCARD by hits · breach only
[ ] If install: backup champion + rewrite BEST_POLICY
[ ] Update THIS handoff §1 scoreboard + §3 loop position
```

— **SEAN 🕵** · Counsel filed · Creator coded one flat dual · **mission continues until 100 clear days or Monty `/stop`**
