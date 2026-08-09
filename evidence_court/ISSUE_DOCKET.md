# ISSUE DOCKET — goal-relative (A31 + A33)

**Last updated:** 2026-08-08 (CASE-0037 PROMOTE_NARROW; re-rank on new floor)  
**goal_achieved:** **false**  
**Scoreboard floor:** CASE-0037 champion — hits 11 / low_hr 0.28 / a13 **0.64** / n_zero **18** / mean_tr 39.4 / breach 0  
**Primary schedule:** `schedules/SCHEDULE.md` + `CREATOR_GOAL_CHECKLIST.md`  
**Laws:** A10 · A13 · A14 · A15 · A28 · A29 · A30 · **A31** · **A32** · **A33**

Every open row **must** list `goal_axes`. Rank = biggest blocker to final boss first. After each verdict / scoreboard, **regenerate** this table from measured gaps (A33).

| rank | severity | item_id | description | goal_axes | blocks_metric | status |
|-----:|----------|---------|-------------|-----------|---------------|--------|
| 1 | S1 | **C-004** | Dual conversion under density (hits / low_hr / promote_ready) | G-CLEAR, G-BREACH0 | hits, low_hr, promote_ready | PENDING_COURT |
| 2 | S2 | **C-003** | A13 residual: zero + 1–7 days → every-day [8,400] | G-A13 | n_zero, a13_frac | **PARTIAL** — 0037 path-state PROMOTED (a13 64%) |
| 3 | S4 | **C-002** | Packed-state offline train class (path-state PROMOTED; label-class closed) | G-TRAIN, G-NO_RETRAIN, G-CLEAR | clear%, fingerprint | **PARTIAL** |
| 4 | S3 | **C-001** | Close Watch→path→brain loop | G-SIGHT, G-A13, G-TRAIN | miss_rate, a13_frac | **PARTIAL** — wire+labels live |
| 5 | S3 | **C-005** | Senses drive brain (Sight→Feel→Taste→Hearing pack into state) | G-SIGHT, G-FEEL, G-TASTE, G-HEAR, G-L2L | sense_fail, L2L | PENDING_COURT |
| 6 | S4 | **C-006** | Production path = brain only (quarantine rule soup) | G-L2L, G-TRAIN | brain_drives purity | PENDING_COURT |
| 7 | S1 | **C-007** | High-target band 50–90 under risk 1–3 | G-CLEAR, G-TASTE | high_band_hits | PENDING_COURT |
| 8 | S4 | **C-008** | Multi-seed / multi-window long-term eval | G-LONG, G-CLEAR | multi_seed promote | PENDING_COURT |
| 9 | S0 | **C-009** | Multi-symbol book risk integrity under density | G-BREACH0 | breach | PENDING_COURT |
| 10 | S4 | **C-010** | Fill realism (friction) re-measure dual | G-CLEAR, G-LONG | honest_clear | PENDING_COURT |
| 11 | S4 | **C-011** | Court brain ↔ single prove champion path | G-ONEBOT | dual_brain | PENDING_COURT |
| 12 | S1 | **C-012** | FINAL_BOT_SPEC gates = A13+dual+L2L+senses+no-retrain | G-CLEAR, G-A13, G-NO_RETRAIN | promote_ready | PENDING_COURT |
| — | S4 | **GAME-TRAIN** | Policy Forge human/oracle traj → game-ingest champion | G-TRAIN, G-SIGHT, G-FEEL, G-TASTE, G-HEAR, G-CLEAR | meta_train_steps, align | **ACTIVE** |
| — | S3 | **CASE-0031** | Sight + Opportunity Watch (serves C-001 / C-005) | G-SIGHT, G-A13 | miss_rate | **WIRE PROMOTED (narrow)** |
| — | S4 | **CASE-C002** | Opportunity-labeled meta-train | G-TRAIN, G-NO_RETRAIN | clear% | **API PROMOTED (narrow)** |
| — | S4 | **CASE-0035** | Silent-day synthetic opp curriculum | G-A13, G-TRAIN, G-CLEAR | n_zero, a13 | **CLOSED REJECT F-024** |
| — | S4 | **CASE-0036** | Real-bar Watch harvest (synth state rebuild) | G-A13, G-TRAIN, G-CLEAR | n_zero, a13 | **CLOSED REJECT F-025** |
| — | S2 | **CASE-0037** | Packed path-state teachers at brain-wait | G-A13, G-TRAIN, G-CLEAR | n_zero, a13 | **PROMOTE_NARROW** champion meta4275 |
| — | S3 | **CASE-0032** | Feel (after 0031) | G-FEEL | false_launch / freeze | QUEUED |
| — | S3 | **CASE-0033** | Taste (after 0032) | G-TASTE | marginal_high_target | QUEUED |
| — | S3 | **CASE-0034** | Hearing (after 0033) | G-HEAR | thrash / a13 session | QUEUED |
| — | — | **Mark M-*** | Phase 2 KAG checklist | (Mark files axes) | — | **BLOCKED** |

## Next action (binding)

1. **C-004** Full Court — dual conversion under new density (hits≥12 / low_hr climb / promote_ready path) **without** undoing a13≥64% / n_zero≤18 floor.  
2. **C-003 residual** — remaining 18 zero + 18 partial days (more path-state coverage, partial densify, or A34).  
3. Append ledger events on verdict.  
4. Re-rank from scoreboard.  
5. **Forbidden:** F-024/F-025 label→synthetic-state densify; pad thrash.

## Issue spawn reminder (A33)

New measurements that hurt clear%, A13, breach, no-retrain, or sense fail modes **must** create or escalate a row here. Issues that no longer block any **G-*** axis → close.
