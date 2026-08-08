# CASE-0017 — Regime-aware meta curriculum (A17 → teacher)

**case_id:** CASE-0017  
**status:** PROMOTED (narrow — curriculum road; not final-boss hit-rate)  
**opened:** 2026-08-07 (scheduled Court fire)  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD  
**docket_rank:** 1  
**goal_gap:** trainability — meta curriculum must sample A17 regimes and label fire/kill honestly  
**question:** What **measured** curriculum change makes the **trained meta-policy’s job easier** by teaching A17 regime fire/kill playbook (conflict/compression → wait; trend → directed fire) **without** cliffs (pad, thrash multi-sym, gate-only, dim break)?

**scope:** `meta_rl/regimes.py` curriculum helpers; `meta_rl/policy.py` sample/teacher wire  
**protected_invariants:** META_RL_DIM=176; A14 train; A16 win/pass; A17 catalog; no goal_path thrash; no PROVEN overwrite  

**Orientation:** `ROAD_FOR_THE_POLICY.md` — pave learnable labels; weights still from meta-train.

---

## ROUND STRUCTURE (Law A10 + A15)

```
Creator opening + NEW test → Mark opening + NEW test
→ one counter each → Counsel opinion → Critic → Optimist → Judge pretrial → units → IRAC
```

---

## Creator opening

### strongest_internet_argument

**Context / multi-task RL** trains one policy across tasks by exposing **context features** (or task IDs) so the learner maps state+context → action (Sodhani et al., multi-task RL with context; Meta-RL effective context — Fu et al. AAAI). Finance meta-learning literature treats **regime shifts** as the reason pooled training fails — models should condition on market state / recent regime (regime-aware meta-learning; meta-learning for returns under shifting regimes).  

**claim:** Permanent meta curriculum must **cover all A17 regimes** and produce **stable teacher labels** (kill → wait) so weights learn when not to thrash — without expanding state dim or inventing pad fills.

**new_test:** `test_creator_new_curriculum_covers_all_a17_regimes`  

**prediction:** 400 samples cover all 8 RegimeId; each sample returns fixed META_RL_DIM state + legal teacher.

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. **A17 playbook is law:** conflict / vol_compression **kill** new risk; range_chop / incomplete **wait**; trend_bull/bear / vol_expansion **allow** directed fire.  
2. Teacher that fires into conflict is a **cliff label** — teaches noise thrash (F-017 class).  
3. Mark multi-set eyes already encode regime sensors; curriculum must **build official sets consistent with regime**, not random side noise.  
4. Intuition (A16) = trained weights over honest labels — not a second rule bot.

**claim:** `teacher_action_under_regime` must hard-wait on kill/no-fire; trend can teach long/short.

**new_test:** `test_mark_new_teacher_obeys_a17_fire_kill_playbook`

---

## Creator counter (exactly one)

**counter:** Templates must **round-trip** `classify_regime_court` so curriculum sensors stay honest (no invented orphan labels).

**newer_test:** `test_creator_new_sensor_templates_classify_to_declared_regime`

---

## Mark counter (exactly one)

**counter:** Wiring must not break **META_RL_DIM=176** or A14 train path; conflict samples always teacher=wait; short meta-train still yields trained champion.

**newer_test:** `test_mark_new_meta_train_uses_regime_labels_without_dim_change`

---

## Counsel opinion (Law A15)

### internet_sift

- Multi-task RL with context-based representations (Sodhani et al., ICML 2021): shared policy + context improves multi-task generalization.  
- Effective context for Meta-RL (Fu et al., AAAI 2021): conditioning on task context enables generalization.  
- Regime-aware / shifting-regime meta-learning in finance: pool-all-history fails when predictor relevance changes across regimes; condition on market state.  
- Finance RL meta-analysis: domain-specific regime handling > algorithm fashion; portfolio methods more regime-sensitive than market-making.

### policy_recommendation

**Best policy for this case:** (1) Sample curriculum **uniformly over A17 RegimeId**; (2) synthesize Mark-set confluence from regime templates; (3) teacher = A17 fire/kill gate then goal-conditioned side; (4) **do not** expand META_RL_DIM this case; (5) **do not** change goal_path residual thrash dials; (6) later case may wire `classify_regime_court` into live day state once curriculum road is stable.

### opinion

Creator is right on coverage + template honesty. Mark is right on playbook hard-wait. Counsel: **promote curriculum road only** — not dual-clear scoreboard. Weigh all three: hybrid already A17; this case **trains** to it.

### evidence

NEW tests path: `tests/test_case0017_regime_curriculum.py` (4 tests).  
Code: `regimes.py` curriculum helpers; `policy.sample_training_state` / `teacher_action_for_state(regime=)`.

### sources

- Sodhani et al., Multi-Task RL with Context-based Representations (ICML 2021)  
- Fu et al., Towards Effective Context for Meta-Reinforcement Learning (AAAI 2021)  
- Regime-aware meta-learning / shifting market regimes (finance meta-learning design class, 2025 surveys)  
- Court laws A14, A16, A17; ROAD_FOR_THE_POLICY.md  

---

## Critic

| Check | Status |
|-------|--------|
| Look-ahead | Curriculum synthetic only; no future prices |
| Cliff risk | Must not pad trades or full-size multi thrash |
| Dim cliff | META_RL_DIM stays 176 |
| Dual scoreboard | Units only — no false promote_ready claim |
| Flea-jar | Kill wait is road-sign, not “impossible high target” |

---

## Optimist

Regime-honest teachers 2x learnability of wait vs thrash; reduces F-017-class noise in meta gradients.

---

## Judge pretrial

1. Run CASE-0017 **4 NEW tests** only (no forward100 this fire).  
2. Code allowed: additive curriculum helpers in `regimes.py` + wire in `policy.py` sample/teacher.  
3. **Forbidden:** goal_path residual dials; pad-to-8; META_RL_DIM change; PROVEN overwrite.  
4. PROMOTE as **narrow curriculum law** if units green.  
5. Does **not** alone claim dual clears + A13.

---

## Results

`python -m pytest evidence_court/tests/test_case0017_regime_curriculum.py -v` → **4/4 PASS**  
Regression: `test_meta_policy_train.py` + `test_case0016_regimes.py` green.

| Test | Role | Result |
|------|------|--------|
| `test_creator_new_curriculum_covers_all_a17_regimes` | Creator opening | **PASS** |
| `test_mark_new_teacher_obeys_a17_fire_kill_playbook` | Mark opening | **PASS** |
| `test_creator_new_sensor_templates_classify_to_declared_regime` | Creator counter | **PASS** |
| `test_mark_new_meta_train_uses_regime_labels_without_dim_change` | Mark counter | **PASS** |

**Code landed (experimental → PROMOTED narrow):**

| Symbol | Role |
|--------|------|
| `sample_curriculum_regime` | Uniform A17 sample |
| `regime_sensor_template` / `build_official_for_regime` | Honest synthetic sensors |
| `teacher_action_under_regime` | Fire/kill teacher |
| `sample_training_state(..., regime=, return_regime=)` | Wired curriculum |
| `teacher_action_for_state(..., regime=)` | Optional A17 gate |

---

## Judge IRAC

- **Issue:** Does regime-aware curriculum improve the road for the trained meta-policy without cliffs?  
- **Rule:** A10 + A15 (three opinions); A14 must train; A17 playbook; ROAD not cliff; units as proof this fire.  
- **Application:** Creator coverage + templates green; Mark playbook + dim pin green; Counsel recommends curriculum-only promote. No goal_path thrash. No dim change. Kill labels wait.  
- **Conclusion:**  
  1. **PROMOTE Law A18 (narrow)** — Regime-aware meta curriculum: sample all A17 regimes; teacher obeys fire/kill; META_RL_DIM unchanged.  
  2. Code: `regimes.py` curriculum block + `policy.py` wire; tests `test_case0017_regime_curriculum.py`.  
  3. **Not** final-boss / dual promote.  
  4. **Next:** CASE-0018 — wire `classify_regime_court` into **day-path observation/state** (honest regime channel at inference) **or** fill/R road that preserves conversion + A13 — still ISSUE-ROAD first, dual on the road.
