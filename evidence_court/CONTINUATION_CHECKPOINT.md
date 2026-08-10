# CONTINUATION CHECKPOINT — Evidence Court Meta-RL

**Updated:** 2026-08-09 (CASE-L2L-P10-residual ACCEPT_NARROW_LAB; champion still 0037)  
**Do not re-run completed greenfield CASE-0001 / 0002.**

---

## goal_achieved

**false**

## Mission

One bot · any target% [5–90] × risk% [1–3] · no retrain after final policy · breach 0 · scalping 8–400/day · trained meta-brain · **senses sight/feel/taste/hearing drive decisions** (A32).

---

## Standing orders (Monty)

| Law | Meaning |
|-----|---------|
| **A31** | Goal is north star of every Court action |
| **A32** | Emergent senses full definitions + fail modes permanent |
| **A33** | Court never stops; generates goal-relative issues; ledger + tiered Court |
| **A34** | Policy Forge game-train → offline game-ingest into champion |
| **A30** | Creator checklist each item Court; then Mark |
| **A13** | MUST 8–400 trades/day |
| **A14/A29** | Meta-policy must be trained; brain decides |
| **A15** | Counsel three-opinion deliberation |
| **A28** | Opportunity Watch always on |
| **A10** | Adversarial rounds permanent |

---

## Schedule

| Phase | Status | File |
|------:|--------|------|
| **1 Creator** | **IN PROGRESS** | `schedules/CREATOR_GOAL_CHECKLIST.md` |
| **2 Mark** | **BLOCKED** | `schedules/MARK_GOAL_CHECKLIST.md` |

---

## Docket status

| Field | Value |
|-------|--------|
| **CASE-0037** | **PROMOTE_NARROW** — production champion meta4275 |
| **CASE-L2L-P10-residual** | **ACCEPT_NARROW_LAB** — meta10835 shadow; no production replace |
| **C-003** | **PARTIAL** — a13 64% floor on forward100; north-star dual weaker |
| **rank-1 next** | **L2L-P10 / C-004** — a13_every_day + hits→11 under one dual SSOT |
| **Forbidden** | F-024/F-025; process washout as champion; pad thrash |

Full table: `ISSUE_DOCKET.md`.

---

## Last scoreboard (**new floor** — CASE-0037 champion)

| case | hits | low_hr | a13_frac | n_zero | mean_tr | breach | promote_ready | seed |
|------|-----:|-------:|---------:|-------:|--------:|-------:|:-------------:|-----:|
| **CASE-0037** | **11** | **0.28** | **0.64** | **18** | **39.4** | **0** | false | 42 |

Prior floor (pre-0037): hits 11 / low_hr 0.28 / a13 0.28 / n_zero 39 / mean_tr 7.38  

**BEST POLICY SSOT:** `BEST_POLICY.md` (read first — champion identity + floor)  
**Legal dethrone path:** `DETHRONE_THE_KING.md` (how to replace king — not yet done)  
**Learn-not-copy road:** `00_PATH_LEARNING/` · CASE-PATH-LEARNING ACCEPT_NARROW · lab `meta_policy_path_learning.npz`  
**2× dethrone arbitration:** `ARBITRATION_2X_DETHRONE.md` (unanimous method; king still meta4275)  
**2× execute lab:** forward100 hits 11 / a13 0.64 (floor match; Milestone A miss) · `execute_2x_clear_road_report.json`  
**Day-12 arbitration:** `ARBITRATION_DAY12_CLEAR.md` — personified Policy + counsel; 15%/3% miss; **DAY-12 CLEAR ROAD**  
**Learn phase:** Teacher→Counsel compact · 20d **any better** a13 0.25→0.35 · `ARBITRATION_LEARN_PHASE.md`  
Champion: `artifacts/meta_policy_champion.npz` fp `42:meta4275:inf0:bcfe6c74f68b7623`  
Backup: `artifacts/meta_policy_champion_pre0037.npz`

---

## Working code paths

| Path | Status |
|------|--------|
| `collect_path_state_teachers` in goal_path | **lab harvest** (default False) |
| `path_state_harvest` train | **PROMOTED train class** |
| Watch + curriculum_labels | **live** |
| Label→synthetic state densify | **F-024/F-025 closed** |

---

## Resume command

```text
python -m pytest evidence_court/tests/test_case0037_path_state_teachers.py -q
python -m evidence_court.meta_rl.cli prove 15 2

# Next Full Court (pick rank by severity):
# 1. C-004 dual conversion — hits / low_hr / promote_ready under new density
# 2. C-003 residual — remaining zero + 1-7 days (more path-state / partial densify / A34)
```

**Do not ask permission to continue the Court cycle.**
