# ISSUE DOCKET — goal-relative (A31 + A33)

**Last updated:** 2026-08-09 (COURT_TRIALS_AUDIT: not all trials full Court; production still 0037)  
**goal_achieved:** **false**  
**Trials audit:** `COURT_TRIALS_AUDIT.md` — honest gap list (C-006…C-012 PENDING; 0032–0034 no files; L2L P1–P10 series filed)  
**Arbitration (2× dethrone method):** `ARBITRATION_2X_DETHRONE.md` — unanimous **2× CLEAR ROAD**  
**2× execute (lab):** `artifacts/execute_2x_clear_road_report.json` — forward100 dual hits **11** / a13 **0.64** / n_zero **18** (floor match; **Milestone A miss**; production still 0037)  
**Day-12 arbitration:** `ARBITRATION_DAY12_CLEAR.md` — 2026-01-21 **15%/3%** miss (~2.9%); unanimous **DAY-12 CLEAR ROAD** (conversion not lot cosplay)  
**Learn phase:** 20d density-only lift; hits stuck on short window.  
**Monty EO size-up:** forward100 hits **11→13**, a13 **0.64→0.61**, breach 0 — **partial progress, not full dethrone** (`eo_intelligent_size_up_forward100.json`).  
**Aaron dethrone attempt:** floor dual hits **12** · a13 **0.61** · dethrone false.  
**Teacher day-12 until-pass:** 2026-01-21 15/3 — **25+15 rounds failed**; PnL stuck **~1.29%** (path sequence unmoved by offline teach); report `day12_teacher_train_report.json`.  
**Instruction SSOT:** `L2L_PROJECT__ONE_BOT_100_DAYS.md` · **`00_PATH_LEARNING/`** (learn-not-copy road)  
**Scoreboard floor (BEST_POLICY forward100):** CASE-0037 — hits 11 / low_hr 0.28 / a13 **0.64** / n_zero **18** / mean_tr 39.4 / breach 0  
**PATH LEARNING lab 30d north-star:** hits 3 · a13 **0.30** · n_zero 11 · breach 0 (champ same window a13 0.27) — promote_lab true · **production_replace false**  
**Primary schedule:** `schedules/SCHEDULE.md` + `CREATOR_GOAL_CHECKLIST.md`  
**Laws:** A10 · A13 · A14 · A15 · A28 · A29 · A30 · **A31** · **A32** · **A33**

Every open row **must** list `goal_axes`. Rank = biggest blocker to final boss first. After each verdict / scoreboard, **regenerate** this table from measured gaps (A33).

| rank | severity | item_id | description | goal_axes | blocks_metric | status |
|-----:|----------|---------|-------------|-----------|---------------|--------|
| 1 | S0 | **L2L-P10** | 8–400 every day + random clear (north star residual) | G-A13, G-CLEAR | a13_every_day, hit_rate | **OPEN** — residual lab a13↑ vs washout; still not every-day |
| 2 | S1 | **C-004** | Dual conversion under density (hits / low_hr / promote_ready) | G-CLEAR, G-BREACH0 | hits, low_hr, promote_ready | **OPEN** — residual hits 7/100 north-star; floor 11 open |
| 3 | S2 | **C-003** | A13 residual: zero + 1–7 days → every-day [8,400] | G-A13 | n_zero, a13_frac | **PARTIAL** — 0037 path-state; residual n_zero 35 on north-star |
| 4 | S4 | **C-002** | Packed-state offline train class (path-state PROMOTED; label-class closed) | G-TRAIN, G-NO_RETRAIN, G-CLEAR | clear%, fingerprint | **PARTIAL** |
| 5 | S3 | **C-001** | Close Watch→path→brain loop | G-SIGHT, G-A13, G-TRAIN | miss_rate, a13_frac | **PARTIAL** — wire+labels live |
| 6 | S3 | **C-005** | Senses drive brain (Sight→Feel→Taste→Hearing) | G-SIGHT, G-FEEL, G-TASTE, G-HEAR, G-L2L | sense_fail, L2L | **PARTIAL** — P1 ACCEPT; P2–P7 NARROW process |
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
| — | S3 | **CASE-L2L-P1** | Senses pack into Meta-RL state; logits react | G-SIGHT, G-FEEL, G-TASTE, G-HEAR, G-L2L | probe-only | **ACCEPT** |
| — | S2 | **CASE-L2L-P2-P10** | Ordered series process curriculum + freeze + dual | (all L2L axes) | final_gate | **CLOSED MIXED** — P10 REJECT full |
| — | S1 | **CASE-L2L-P10-residual** | Density process + path re-anchor residual | G-A13, G-CLEAR, G-TRAIN, G-L2L | a13 vs washout | **CLOSED ACCEPT_NARROW_LAB** — no production replace |
| — | S1 | **CASE-PATH-LEARNING** | Learn-not-copy steps 1–6 road + lab execute | G-TRAIN, G-L2L, G-A13, G-CLEAR, G-NO_RETRAIN | hits vs clone; floor | **CLOSED ACCEPT_NARROW** — lab shadow; king unchanged |
| — | S0 | **L2L-FINAL-GATE** | §7 multi-seed 100d random T×R + all proposals full Accept | G-CLEAR, G-A13, G-NO_RETRAIN | promote_ready | **OPEN** |
| — | S3 | **CASE-0032** | Feel (after 0031 / maps L2L-P3) | G-FEEL | false_launch / freeze | QUEUED |
| — | S3 | **CASE-0033** | Taste (after 0032) | G-TASTE | marginal_high_target | QUEUED |
| — | S3 | **CASE-0034** | Hearing (after 0033) | G-HEAR | thrash / a13 session | QUEUED |
| — | — | **Mark M-*** | Phase 2 KAG checklist | (Mark files axes) | — | **BLOCKED** |

## Next action (binding)

1. **C-004 conversion** — 2× CLEAR ROAD **executed** but hits still **11** on forward100 (floor match only). Improve **real outcome diversity** / conversion teachers to reach Milestone A (hits≥15).  
2. Lab shadow: `meta_policy_2x_clear_road.npz` — not production.  
3. Do **not** open C-006…C-012 freestyle; do **not** open 0032–0034 until dual fail-modes demand.  
4. Do **not** replace CASE-0037 until Milestone A / 2× + PROMOTE + BEST_POLICY.  
5. **Forbidden:** F-024/F-025; pad thrash; process washout; pure path-clone as “2×”; silent overwrite.

## Issue spawn reminder (A33)

New measurements that hurt clear%, A13, breach, no-retrain, or sense fail modes **must** create or escalate a row here. Issues that no longer block any **G-*** axis → close.
