# CASE-PATH-LEARNING — Learn the map (steps 1–6), not only copy answers

**case_id:** CASE-PATH-LEARNING  
**opened:** 2026-08-09  
**docs:** `00_PATH_LEARNING/`  
**goal_axes:** G-TRAIN, G-L2L, G-A13, G-CLEAR, G-NO_RETRAIN, G-BREACH0  
**docket service:** L2L-P10 / C-004 / DETHRONE path  
**status:** CLOSED — **ACCEPT_NARROW** lab; steps 1–6 executed offline; production unchanged  

---

## Claim

Adopt **PATH LEARNING** as the legal **lab road** beyond path-state answer-copy:  
outcome-shaped offline updates; goal/risk curriculum primary with sparse path anchors; holdout that bites; conversion teachers; senses process+outcome with path re-anchor last; promote_guard blocking washout/clone-without-floor.

**Production champion stays CASE-0037** unless a later PROMOTE holds BEST_POLICY floor.

---

## Creator opening (internet + new tests)

**Argument:** Behavioral cloning on path-state raises density but stalls conversion (hits flat at 11). Outcome-shaped losses + conversion curricula + holdout are standard ways to push policies past pure imitation without live pad thrash.

**new_tests:**
- `test_step1_outcome_scale_clear_beats_breach`
- `test_step1_outcome_shaped_update_runs_on_brain`
- `test_steps_2_3_curriculum_mix_not_path_only_clone`
- `test_step6_promote_guard_rejects_washout_and_clone`

**code:** `meta_rl/path_learning.py`, `meta_rl/train_path_learning.py`, `00_PATH_LEARNING/*`

---

## Mark Here, Esq. opening (knowledge + new tests)

**Argument:** Mark path physics still apply: load→wait, risk floor→wait, continuation mid-progress→hold size. Conversion teachers encode that knowledge offline; path-state remains sparse **anchors** so A13 density from CASE-0037 is not erased. Process alone is known washout (L2L residual lesson).

**new_tests:**
- `test_step4_conversion_load_wait_and_hold_fire`
- `test_step4_sample_conversion_episode_shapes`
- `test_step3_freeze_fingerprint_stable_across_target_risk`

---

## Counters (one each)

**Creator:** Dual must name protocol; floor hold required for production; lab ACCEPT ≠ king dethrone.  
**newer test:** `test_step6_promote_guard_blocks_production_without_floor`

**Mark (waive second):** Accept path re-anchor last; forbid F-024/F-025.

---

## Counsel opinion (A15)

**internet_sift:** Imitation + sparse RL / reward shaping / curriculum learning — pure BC plateaus; auxiliary outcome and goal-conditioned curricula improve transfer when freeze + eval holdout are honest.

**policy_recommendation:**
1. ACCEPT PATH LEARNING as **lab road** with shipped helpers.  
2. Warmstart 0037; mix conversion/outcome primary; path anchors sparse; process light; re-anchor last.  
3. Dual lab vs champ; promote_guard; **no** production replace without floor + PROMOTE.  
4. Reject pure process or pure path-clone as “learning complete.”

**opinion:** **ACCEPT_NARROW** for lab machinery + train; production unchanged.

**evidence:** CASE-0037 hits flat; L2L process washout; residual re-anchor last restored density.

**sources:** project BEST_POLICY / DETHRONE_THE_KING; process-RL / curriculum practice.

---

## Critic

Risk: conversion synthetics still not real path outcomes → hits may not move. Mitigate: dual honesty; later harvest real outcome fields into path packs.

## Optimist

Outcome scale + conversion wait/hold gives a learnable clear signal path-state alone lacked.

---

## Judge IRAC

**Issue:** May Court adopt PATH LEARNING (steps 1–6) as the offline lab road past answer-copy, and execute lab train under those rules without replacing the king?

**Rule:** A10+A15; A14 offline/freeze; A13 density without pad; A33 ledger; BEST_POLICY floor for production; DETHRONE gates.

**Application:**  
- Creator: outcome/conversion/holdout/guard + new tests — **accepted**.  
- Mark: load/risk conversion physics + freeze pin — **accepted**.  
- Counsel: lab ACCEPT_NARROW; no production without floor — **adopted**.  
- Forbidden: F-024/F-025, silent overwrite, process-washout promote, inference retrain.

**Conclusion: ACCEPT_NARROW (lab road + execute 1–6 offline)**

| Field | Ruling |
|-------|--------|
| Docs `00_PATH_LEARNING` | **PROMOTE as path SSOT** (analysis + implement rules) |
| Code helpers | **Lab allowed** |
| Lab shadow train/dual | **Ordered** under steps 1–6 |
| Production champion | **Unchanged** CASE-0037 meta4275 |
| production_replace | **false** unless later floor hold + PROMOTE |
| Final boss / §7 | **false** |

---

## Post-ruling execution log

| Item | Value |
|------|-------|
| dual protocol | north_star_random_TxR_XAU_15m (seed=42, 30d) |
| dual lab | hits **3** · a13 **0.30** · n_zero **11** · breach **0** · frozen yes · mean_tr 7.33 |
| dual champ same window | hits **3** · a13 **0.267** · n_zero **11** · breach **0** |
| promote_guard | promote_lab **true** · production_replace **false** · floor_hold **false** |
| fingerprint lab | 42:meta9625:inf0:f7d02a98e2a3aaa8 |
| shadow | `artifacts/meta_policy_path_learning.npz` |
| production champion | **unchanged** CASE-0037 meta4275 |
| steps 1-6 executed | yes (offline lab) |
