# ISSUE DOCKET — goal-relative (A31 + A33)

**Last updated:** 2026-08-07 (A31/A32/A33 goal-anchored Court)  
**goal_achieved:** **false**  
**Scoreboard floor:** CASE-0029 hits 11 / low_hr 0.28 / a13 0.28 / breach 0  
**Primary schedule:** `schedules/SCHEDULE.md` + `CREATOR_GOAL_CHECKLIST.md`  
**Laws:** A10 · A13 · A14 · A15 · A28 · A29 · A30 · **A31** · **A32** · **A33**

Every open row **must** list `goal_axes`. Rank = biggest blocker to final boss first. After each verdict / scoreboard, **regenerate** this table from measured gaps (A33).

| rank | severity | item_id | description | goal_axes | blocks_metric | status |
|-----:|----------|---------|-------------|-----------|---------------|--------|
| 1 | S3 | **C-001** | Close Watch→path→brain loop; misses → curriculum + decisions | G-SIGHT, G-A13, G-TRAIN | miss_rate, a13_frac | PENDING_COURT |
| 2 | S4 | **C-002** | Real-bar / opportunity-labeled meta-train; retrain champion | G-TRAIN, G-NO_RETRAIN, G-CLEAR | clear%, fingerprint | PENDING_COURT |
| 3 | S2 | **C-003** | A13 lived every day (London/NY no excuse); no pad | G-A13 | a13_frac | PENDING_COURT |
| 4 | S1 | **C-004** | Dual conversion under random [5–90]×[1–3] | G-CLEAR, G-BREACH0 | hits, low_hr, promote_ready | PENDING_COURT |
| 5 | S3 | **C-005** | Senses drive brain (Sight→Feel→Taste→Hearing pack into state) | G-SIGHT, G-FEEL, G-TASTE, G-HEAR, G-L2L | sense_fail, L2L | PENDING_COURT |
| 6 | S4 | **C-006** | Production path = brain only (quarantine rule soup) | G-L2L, G-TRAIN | brain_drives purity | PENDING_COURT |
| 7 | S1 | **C-007** | High-target band 50–90 under risk 1–3 | G-CLEAR, G-TASTE | high_band_hits | PENDING_COURT |
| 8 | S4 | **C-008** | Multi-seed / multi-window long-term eval | G-LONG, G-CLEAR | multi_seed promote | PENDING_COURT |
| 9 | S0 | **C-009** | Multi-symbol book risk integrity under density | G-BREACH0 | breach | PENDING_COURT |
| 10 | S4 | **C-010** | Fill realism (friction) re-measure dual | G-CLEAR, G-LONG | honest_clear | PENDING_COURT |
| 11 | S4 | **C-011** | Court brain ↔ single prove champion path | G-ONEBOT | dual_brain | PENDING_COURT |
| 12 | S1 | **C-012** | FINAL_BOT_SPEC gates = A13+dual+L2L+senses+no-retrain | G-CLEAR, G-A13, G-NO_RETRAIN | promote_ready | PENDING_COURT |
| — | S4 | **GAME-TRAIN** | Policy Forge human/oracle traj → game-ingest champion | G-TRAIN, G-SIGHT, G-FEEL, G-TASTE, G-HEAR, G-CLEAR | meta_train_steps, align | **ACTIVE** |
| — | S3 | **CASE-0031** | Sight + Opportunity Watch (serves C-001 / C-005) | G-SIGHT, G-A13 | miss_rate | OPEN_NEXT |
| — | S3 | **CASE-0032** | Feel (after 0031) | G-FEEL | false_launch / freeze | QUEUED |
| — | S3 | **CASE-0033** | Taste (after 0032) | G-TASTE | marginal_high_target | QUEUED |
| — | S3 | **CASE-0034** | Hearing (after 0033) | G-HEAR | thrash / a13 session | QUEUED |
| — | — | **Mark M-*** | Phase 2 KAG checklist | (Mark files axes) | — | **BLOCKED** |

## Next action (binding)

1. Open **Full Court** on **CASE-0031** with `item_id=C-001` (and C-005 sub-scope for sight).  
2. Append ledger events on verdict.  
3. Re-rank this docket from scoreboard.  
4. Do **not** open polish while rank-1 is open.

## Issue spawn reminder (A33)

New measurements that hurt clear%, A13, breach, no-retrain, or sense fail modes **must** create or escalate a row here. Issues that no longer block any **G-*** axis → close.
