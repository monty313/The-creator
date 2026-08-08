# CONTINUATION CHECKPOINT — Evidence Court Meta-RL

**Updated:** 2026-08-07 (Law **A30** full-project checklist schedule)  
**Do not re-run completed greenfield CASE-0001 / 0002.**

---

## Standing order (Monty)

**A30 PERMANENT:** Creator whole-project checklist → **each item Court**;  
then Mark whole-project + KAG checklist → **each item Court**.  
**A10+A15** on every item. Mark phase **blocked** until Creator checklist terminal.

Also in force: A13 MUST 8–400 · A14/A29 brain train · A15 Counsel · A28 Watch.

---

## Mission (final boss — not met)

100d random [5–90]×[1–3], breach 0, consistent hits, no retrain, L2L/senses, **A13 8–400/day** → `FINAL_BOT_SPEC.md`.

---

## Schedule (binding)

| Phase | Status | File |
|------:|--------|------|
| **1 Creator** | **IN PROGRESS** | `schedules/CREATOR_GOAL_CHECKLIST.md` |
| **2 Mark** | **BLOCKED** | `schedules/MARK_GOAL_CHECKLIST.md` |

Master: `schedules/SCHEDULE.md`

---

## Creator next Court items

| Priority | item_id | title |
|---------:|---------|-------|
| 1 | **C-001** | Watch→path→brain loop (CASE-0031 may serve) |
| 2 | C-002 | Real-bar meta-train |
| 3 | C-003 | A13 London/NY density |
| 4 | C-004 | Dual conversion |
| 5 | C-005 | Senses→brain (0031–0034) |
| 6–12 | C-006…C-012 | integrity / long-term / one-bot / FINAL gates |

---

## Scoreboard floor

CASE-0029: hits 11 / low_hr 0.28 / a13 28% / breach 0 — do not regress without measure.

---

## Resume

```powershell
cd "C:\Users\user\OneDrive\Desktop\The Creator"
# Read schedules/SCHEDULE.md + CREATOR_GOAL_CHECKLIST.md
# Fire Court on C-001 (CASE-0031 or new case with item_id=C-001)
python -m pytest evidence_court/tests/test_full_project_checklist_law.py -q
```
