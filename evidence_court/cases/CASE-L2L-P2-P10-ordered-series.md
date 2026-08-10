# CASE-L2L-P2…P10 — Ordered L2L series through Court

**case_id:** CASE-L2L-P2-P10  
**instruction:** `L2L_PROJECT__ONE_BOT_100_DAYS.md`  
**opened/closed:** 2026-08-09  
**depends_on:** CASE-L2L-P1 ACCEPT (senses pack)  
**status:** CLOSED — per-proposal rulings below (not final mission PROMOTE)

---

## Shared Court process (each proposal)

Creator opening + new test → Mark opening + new test → one counter each (or waive) → Counsel → Critic → Optimist → Judge IRAC  

**Three opinions weighed:** Creator, Mark Here, Esq., Counsel (A15).

**North star scoreboard (only success):** 100d random target∈[5,90] × risk∈[1,3], breach 0 every day, trades∈[8,400] every day, PB+cont, frozen weights.

**Measured dual (this case):** seed=42, 30d XAU 15m, L2L shadow `meta_policy_l2l_p2_p10.npz`  
| hits | hit_rate | a13_frac | n_zero | breach | pb | cont | frozen |
|-----:|---------:|---------:|-------:|-------:|---:|-----:|:------:|
| 1 | 0.033 | 0.133 | 22 | **0** | 186 | 473 | **yes** |

---

## Proposal 2 — Sight alive (G-SIGHT)

### Creator opening
Process target from sight topology/consensus without hard trade rule at inference; soft wait on incomplete consensus.  
**new_test:** `test_p2_p3_load_wait_not_fire`, `sample_l2l_process_episode`

### Mark Here, Esq. opening
Sight must read force+timing on official sets; process wait on load/incomplete is correct physics, not a frozen if/then production path.  
**new_test:** process tags include `P2_sight`

### Counters
Creator: process_reward scales CE, not pad trades. Mark: waive second counter.

### Counsel
Process supervision of structure reading is standard intermediate-reward RL; ACCEPT infrastructure; full “not flat on B&B days” needs denser dual residual.

### Judge IRAC — **ACCEPT_NARROW**
Issue: process sight reading without final-label path.  
Rule: L2L P2 Accept/Reject.  
Application: units prove load→wait process; dual still high n_zero → not full Accept.  
**Conclusion: ACCEPT_NARROW** (process curriculum shipped; residual C-004 / denser dual).

---

## Proposal 3 — Feel alive (G-FEEL)

### Creator / Mark
Load → wait; collapse → wait; launch contributes to fire process.  
**tests:** load wait; launch path in process_target.

### Counsel
Dual-clock tension as train-time process matches A32 Feel fail modes.

### Judge — **ACCEPT_NARROW**
Units prove load/collapse wait process. Dual thrash not fully killed (n_zero high). Residual P3 measure.

---

## Proposal 4 — Taste alive (G-TASTE, G-CLEAR)

### Creator / Mark
patience_preferred / noise → wait; conviction sizes process fire.  
**tests:** high_target_patience scenario; process_target taste tags.

### Judge — **ACCEPT_NARROW**
Process taste gates shipped. Dual hit_rate 0.033 — full Accept fails. Residual C-004.

---

## Proposal 5 — Hearing alive (G-HEAR, G-A13)

### Creator / Mark
wait_subtype kill / no_trade → process wait; day_story in multi-sense boost.  
**tests:** conflict_wait; tags P5_*.

### Judge — **ACCEPT_NARROW**
Hearing process tags live. Dual a13_every_day false → not full P5/P10 Accept.

---

## Proposal 6 — Step-by-step multi-sense process (G-L2L)

### Creator / Mark
`process_reward` rises when launch + B&B + day_story cohere (P6_multi_sense_agree).  
**tests:** curriculum tag_counts; multi-sense path.

### Judge — **ACCEPT_NARROW**
Process multi-sense reward shipped. Not full “clear step-by-step improves 100d” without better dual.

---

## Proposal 7 — L2L holdout novel target/risk (G-L2L, G-NO_RETRAIN)

### Creator / Mark
`holdout_mode` samples high targets; curriculum holdout steps.  
**tests:** `test_p6_p7_curriculum_trains_and_p8_freezes`

### Judge — **ACCEPT_NARROW**
Holdout curriculum exists offline. Dual novelty not multi-window 100d yet.

---

## Proposal 8 — Lock weights (G-NO_RETRAIN)

### Creator / Mark
`freeze_for_inference`; meta_update raises NO_RETRAIN; fingerprint stable across target/risk contexts.  
**tests:** `test_p6_p7_curriculum_trains_and_p8_freezes`, `test_p8_fingerprint_stable_across_target_risk_context`

### Judge — **ACCEPT**
Full Accept: frozen, no inference update, context-only pairs.

---

## Proposal 9 — Breach 0 (G-BREACH0)

### Creator / Mark
Risk envelope hard wait; dual breach_count=0 on measured window.  
**tests:** dual metric + existing risk envelope pins.

### Judge — **ACCEPT** (this measured window)
breach=0 on 30d dual. Residual: multi-seed 100d still required for §7 final gate.

---

## Proposal 10 — 8–400 every day + clear (G-A13, G-CLEAR)

### Creator / Mark
North-star dual measures a13_every_day, hit_rate, pb+cont.  
**measure:** a13_every_day=false, a13_frac=0.13, hits=1/30, both_pb_and_cont=true.

### Judge — **REJECT** full Accept; **PARTIAL** evidence
PB+cont present; breach 0; **not** 8–400 every day; clear vacuous. Residual blocks final PROMOTE.

---

## Final promote gate (§7)

| Requirement | Status |
|-------------|--------|
| All 10 proposals fully accepted | **No** (P2–P7 narrow; P10 reject full) |
| 100d multi-seed random T×R | **Not yet** (30d single-seed) |
| breach 0 every day | **Yes on 30d** |
| 8–400 every day | **No** |
| PB+cont | **Yes** |
| frozen weights | **Yes** |
| senses change decisions | **Yes (P1 unit)** |

**final_promote_gate.ready = false**  
Shadow: `artifacts/meta_policy_l2l_p2_p10.npz` (experimental; champion still CASE-0037)

---

## Code map

| Module | Role |
|--------|------|
| `meta_rl/l2l_process.py` | Process targets P2–P7 |
| `meta_rl/train_l2l_full.py` | Curriculum + freeze + dual |
| `tests/test_l2l_p2_p10.py` | Unit pins |
| `tests/test_l2l_proposal1_senses_drive_brain.py` | P1 |

---

## Ordered next work (binding)

1. Densify dual path / process curriculum so a13_every_day and hits climb without breach.  
2. Re-open P10 with 100d multi-symbol multi-seed when units + dual improve.  
3. Do **not** skip to champion PROMOTE until §7 gate true.
