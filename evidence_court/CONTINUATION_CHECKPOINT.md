# CONTINUATION CHECKPOINT — Evidence Court Meta-RL

**Updated:** 2026-08-07 (A31/A32/A33 goal-anchored legal process)  
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

Master: `schedules/SCHEDULE.md`

---

## Docket rank-1 (next Full Court)

| Field | Value |
|-------|--------|
| **item_id** | **C-001** |
| **case** | **CASE-0031** Sight + Opportunity Watch |
| **goal_axes** | G-SIGHT, G-A13, G-TRAIN |
| **blocks_metric** | miss_rate, a13_frac |
| **severity** | S3 (elevates if dual/A13 collapse) |

Then: C-002 → C-003 → C-004 → C-005 (0032–0034) → C-006…C-012.

Full table: `ISSUE_DOCKET.md`.

---

## Last scoreboard (floor)

| case | hits | low_hr | a13_frac | breach | promote_ready | seed |
|------|-----:|-------:|---------:|-------:|:-------------:|-----:|
| CASE-0029 | 11 | 0.28 | 0.28 | 0 | false | 42 |

History: `ledger/SCOREBOARD_HISTORY.jsonl`

---

## Evidence retention pointers

- Ledger: `ledger/EVIDENCE_LEDGER.jsonl` (events EVT-20260807-0001…0005 bootstrap A31–A33)
- Counsel cache: `ledger/COUNSEL_CACHE.jsonl`
- Precedents dir: `precedents/`
- Goal law: `GOAL_LAW.md` · Senses: `EMERGENT_SENSES_LAW.md` · Process: `GOAL_RELATIVE_COURT_LAW.md`

---

## Resume command

```text
# 1. Load goal + docket + checkpoint
# 2. Full Court CASE-0031 (C-001)
# 3. Pins:
python -m pytest evidence_court/tests/test_goal_law.py evidence_court/tests/test_emergent_senses_law.py evidence_court/tests/test_goal_relative_court_law.py evidence_court/tests/test_full_project_checklist_law.py -q
# 4. After verdict: append ledger, re-rank ISSUE_DOCKET, update this checkpoint
```

**Do not ask permission to continue the Court cycle.** Generate the next goal-relative issue after each measured verdict until final boss.
