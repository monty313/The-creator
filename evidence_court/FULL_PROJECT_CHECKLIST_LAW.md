# FULL-PROJECT CHECKLIST SCHEDULE — PERMANENT (Monty)

**Law id:** **A30**  
**Status:** PERMANENT  
**Human order:** Monty — Creator whole-project checklist → each item Court; then Mark whole-project + KAG checklist → each item Court.

---

## Standing rule

To reach **GOAL** (`mark_here/knowledge/lab/GOAL.md`), the Court runs a **two-phase full-project schedule**:

| Phase | Who | Scope | Output |
|-------|-----|--------|--------|
| **1 — CREATOR** | Creator | Entire project (Court package, meta_rl, laws, scoreboard, data, gaps) **from the internet + systems design** | Ordered **checklist** of what must happen to hit the goal |
| **2 — MARK** | Mark Here, Esq. | Entire project **+ his knowledge base / KAG** (@physics, soul, pack, doctrine) | Ordered **checklist** of what must happen to hit the goal |

### Hard process

1. **Every checklist item** becomes (or maps to) a Court case under **A10 + A15** (openings, counters, Counsel, Critic, Optimist, Judge IRAC, measure).  
2. **No item is “done”** without a case ruling: PROMOTE | REJECT | ADMIT_EXPERIMENT | INCONCLUSIVE.  
3. **Phase 2 (Mark) does not start** until **every Phase 1 (Creator) item** has a terminal ruling (not left OPEN forever without decision).  
4. After Mark’s full checklist is filed, **every Mark item** also runs Court the same way.  
5. Items may spawn **sub-cases**; parent checklist row tracks status.  
6. Checklists are **append-only**; completed rows keep history.

### Schedules (files)

| File | Role |
|------|------|
| `schedules/SCHEDULE.md` | Master phase status + next case |
| `schedules/CREATOR_GOAL_CHECKLIST.md` | Phase 1 — Creator whole-project checklist |
| `schedules/MARK_GOAL_CHECKLIST.md` | Phase 2 — Mark whole-project + KAG checklist |
| `schedules/CHECKLIST_ITEM_TEMPLATE.md` | How to open a case from one row |

### Case naming

- Creator items: `CASE-C##-…` or continue numeric series with tag `checklist=creator` / `item_id=C-0xx`  
- Mark items: `CASE-M##-…` or numeric with `checklist=mark` / `item_id=M-0xx`  

Prefer **item_id** field in every case file.

---

## Checklist row schema (required)

| Field | Meaning |
|-------|---------|
| `item_id` | Stable id (e.g. C-001) |
| `title` | One-line need |
| `why_for_goal` | Link to clear% / breach0 / A13 / no-retrain / L2L |
| `proposed_work` | What Creator/Mark thinks must happen |
| `court_case` | Case file path or TBD |
| `status` | PENDING_COURT \| IN_COURT \| PROMOTE \| REJECT \| ADMIT \| INCONCLUSIVE \| BLOCKED |
| `depends_on` | Other item_ids if any |

---

## Immutable

Permanent until Monty supercedes. Skipping Court on a checklist item is a Court defect.  
Starting Mark Phase 2 before Creator Phase 1 is complete is a Court defect (unless Monty waives on record).
