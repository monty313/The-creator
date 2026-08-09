# CASE-C002 — Opportunity-labeled meta-train (C-002)

**case_id:** CASE-C002  
**status:** OPEN — **label→train path PROMOTED (narrow)**; dual / full real-bar M1 harvest **not claimed**  
**opened:** 2026-08-07  
**item_id:** C-002  
**goal_axes:** G-TRAIN, G-NO_RETRAIN, G-CLEAR  
**depends_on:** C-001 / CASE-0031 (Watch curriculum_labels)

**question:** Can Watch miss `curriculum_labels` be consumed offline into meta-train so the champion learns to fire opportunity sides (esp. London/NY) **without** live force-pad, while fingerprint stays stable across target/risk at prove?

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → pretrial → IRAC

---

## Creator opening

**strongest_internet_argument:** Offline RL labels passive logs (Yu et al.); miss→teacher is counterfactual coverage for goal-conditioned policies.

**new_test:** `test_case_c002_opportunity_train.py::test_creator_new_opportunity_label_to_example` — **PASS**

---

## Mark opening

**strongest_knowledge_argument:** Labels must keep Mark HTF+PB/cont teacher sides; London/NY higher weight; offline only (A28 no live override).

**new_test:** `test_mark_new_apply_labels_updates_brain` — **PASS**

---

## Creator counter

**counter:** After opportunity mix train, prove across pairs must not retrain (A14).  
**newer_test:** `test_creator_new_train_with_opportunity_labels_no_retrain_at_prove` — **PASS**

---

## Mark counter

**counter:** London/NY weight must exceed other band in exported labels.  
**newer_test:** `test_mark_new_london_ny_label_weight_higher` — **PASS**

---

## Counsel opinion (A15)

### internet_sift
Offline label-from-log + hierarchical GCRL: improve behavior coverage without online thrash; CQL warns against OOD force-fire.

### policy_recommendation
1. Keep C-001 Watch labels.  
2. `opportunity_label_to_training_example` + `apply_opportunity_labels_to_brain`.  
3. `train_goal_conditioned_meta_policy(..., opportunity_labels=...)` offline mix.  
4. Full historical M1 harvest + champion replace = follow-up measure (not this narrow).  
5. No live pad.

### opinion
Promote train-consume path; reject dual/final-boss.

### sources
- Yu et al. ICML 2022 unlabeled offline RL  
- A28 Watch law · A14 no retrain at prove · ROAD

---

## Critic

- Synthetic state from labels is **not** full real-bar M1 yet (C-002 residual).  
- Short n_steps lab pins ≠ production 8000 retrain of champion artifact.

---

## Optimist

- Loop Watch→labels→meta_update is closed.  
- Fingerprint stability across pairs pinned.  
- Ready for denser label harvest next.

---

## Judge IRAC

- **Issue:** Offline opportunity-label train path under A14/A28?  
- **Rule:** A10+A15; A14 no prove retrain; A28 complain not force; A29 trained brain.  
- **Application:** Units PASS; train consumes labels; prove frozen.  
- **Conclusion:**  
  1. **PROMOTE (narrow)** — opportunity-labeled meta-train API.  
  2. C-002 **PARTIAL** until real-bar harvest + champion re-save + dual non-regression.  
  3. **Next:** harvest labels from multi-day path / real M1; optional meta-train 8000 + prove pairs; then C-003 A13.

---

## Code

| Symbol | Role |
|--------|------|
| `opportunity_label_to_training_example` | label → state/teacher |
| `apply_opportunity_labels_to_brain` | offline meta_update batch |
| `train_goal_conditioned_meta_policy(opportunity_labels=)` | mix into curriculum |
