# MASTER SCHEDULE — Goal-relative Court → Final bot

**Laws:** **A30** checklists · **A31** goal · **A32** senses · **A33** continuous goal-relative process  
**Updated:** 2026-08-07  
**goal_achieved:** **false**

---

## Mission (read first)

One bot · any target% [5–90] × risk% [1–3] at inference · **no retrain** after final policy · **breach 0** · scalping **8–400 trades/day** · trained meta-brain · **emergent senses** (sight/feel/taste/hearing) drive decisions.

---

## Phase status

| Phase | Owner | Checklist | Status | Next action |
|------:|-------|-----------|--------|-------------|
| **1** | **Creator** | `CREATOR_GOAL_CHECKLIST.md` | **IN PROGRESS** | C-001/C-002 APIs **PARTIAL**; next Court **C-003** A13 density (or C-002 harvest) |
| **2** | **Mark** | `MARK_GOAL_CHECKLIST.md` | **BLOCKED** | After Phase 1 all terminal |

---

## Binding cycle (never stops until goal)

```text
measure scoreboard
  → goal_achieved? NO
  → generate/refresh ISSUE_DOCKET from G-* axes (A33)
  → Full Court on rank-1 (A10+A15)
  → ledger + scoreboard history + precedent card
  → loop
```

---

## Creator queue (Court next)

| Priority | item_id | title | goal_axes | case |
|---------:|---------|-------|-----------|------|
| 1 | C-003 | A13 density | G-A13 | + CASE-0034 |
| 2 | C-002 | Opportunity meta-train residual | G-TRAIN, G-NO_RETRAIN, G-CLEAR | CASE-C002 **PARTIAL** |
| 3 | C-001 | Watch→path→brain | G-SIGHT, G-A13, G-TRAIN | CASE-0031 **PARTIAL** |
| 4 | C-004 | Dual conversion | G-CLEAR, G-BREACH0 | + CASE-0033 |
| 5 | C-005 | Senses→brain A32 | G-SIGHT…G-HEAR | 0031–0034 |
| 6–12 | C-006…C-012 | integrity / long-term / FINAL | see checklist | after conversion path |

Full rows: `CREATOR_GOAL_CHECKLIST.md`.

---

## Sense series (parallel spine of C-001/C-005)

| Case | Sense | Status |
|------|-------|--------|
| CASE-0031 | Sight + Watch | **WIRE PROMOTED (narrow)**; miss 100d deferred |
| CASE-0032 | Feel | QUEUED |
| CASE-0033 | Taste | QUEUED |
| CASE-0034 | Hearing | QUEUED |

---

## Standing laws in force

A10 adversarial · A13 scalping MUST · A14/A29 train brain · A15 Counsel · A28 Watch · A30 checklists · **A31 goal** · **A32 senses** · **A33 goal-relative Court + ledger**

---

## Evidence retention (A33)

| Artifact | Path |
|----------|------|
| Ledger | `ledger/EVIDENCE_LEDGER.jsonl` |
| Scoreboard history | `ledger/SCOREBOARD_HISTORY.jsonl` |
| Counsel cache | `ledger/COUNSEL_CACHE.jsonl` |
| Precedent cards | `precedents/` |

---

## Resume

```text
1. Read GOAL_LAW.md + ISSUE_DOCKET.md + CONTINUATION_CHECKPOINT.md
2. Open Full Court on C-003 (A13 density) or finish C-002 real-bar harvest
3. After IRAC: append ledger, update checklist row, re-rank docket
4. Continue until goal_achieved
```
