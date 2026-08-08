# CASE-0018 — Day-path A17 regime channel (doctrine pack)

**case_id:** CASE-0018  
**status:** PROMOTED (narrow — inference regime channel; not final-boss hit-rate)  
**opened:** 2026-08-07 (scheduled Court fire)  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD  
**docket_rank:** 1  
**goal_gap:** trained policy must **see** A17 regime at day-path inference (train/infer alignment)  
**question:** What **measured** wire puts `classify_regime_court` into **day-path state/obs** the frozen meta-policy can use — shared with A18 curriculum — **without** expanding META_RL_DIM or paving thrash/pad cliffs?

**scope:** `meta_rl/regimes.py` encode/decode; `goal_path.py` day wire; `policy.py` curriculum doctrine pack  
**protected_invariants:** META_RL_DIM=176; Mark-168 layout; A14–A18; no PROVEN overwrite; no pad fills  

**Orientation:** `ROAD_FOR_THE_POLICY.md` — honest state channel for the learner.

---

## ROUND STRUCTURE (Law A10 + A15)

```
Creator opening + NEW test → Mark opening + NEW test
→ one counter each → Counsel → Critic → Optimist → Judge pretrial → units → IRAC
```

---

## Creator opening

### strongest_internet_argument

**Contextual / multi-task RL** requires the **same context features at train and inference** (Sodhani context MTL; Fu Meta-RL effective context). If curriculum labels by regime (A18) but day path omits regime from state, the frozen policy cannot condition — train/infer mismatch. Doctrine block of Mark-168 is the natural **additive pack site** without changing META_RL_DIM.

**claim:** `encode_regime_doctrine` into Mark doctrine (16) + decode round-trip gives a stable inference channel.

**new_test:** `test_creator_new_regime_doctrine_encode_decode_distinct`

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. Day path already reads `multi_set_consensus` + force — must map through **A17** `classify_regime_court`.  
2. **Kill** regimes (conflict, vol_compression) must **skip new risk** (road-sign, not pad).  
3. Efficiency proxy from Court sensors only (no look-ahead).  
4. Physics: incomplete eyes / conflict → wait; directed multi-set force → allow path.

**claim:** `regime_from_edge_sensors` + `day_path_regime_skip_new_risk` pin Mark playbook on the day path.

**new_test:** `test_mark_new_edge_sensors_map_to_a17_kill_playbook`

---

## Creator counter (exactly one)

**counter:** Packing must not break **META_RL_DIM=176**; doctrine at mark[32:48] must decode.

**newer_test:** `test_creator_new_state_with_doctrine_keeps_meta_rl_dim`

---

## Mark counter (exactly one)

**counter:** Curriculum (A18) and day path must share **identical doctrine layout** so training labels match inference features.

**newer_test:** `test_mark_new_curriculum_and_daypath_share_regime_doctrine_layout`

---

## Counsel opinion (Law A15)

### internet_sift

- Context features in multi-task RL must be present at deployment.  
- Meta-RL: effective task/regime context improves generalization without inference retrain.  
- Finance regime-aware models: condition on market state; pooled features without regime fail under shift.

### policy_recommendation

**Best policy:** Pack A17 into existing Mark **doctrine** (16 dims): one-hot + allow + kill + force + efficiency. Wire `goal_path` to classify → pack → `build_meta_rl_state(doctrine_vec=...)`. Align curriculum `sample_training_state` with same packer. Skip kill regimes on day path. **No** META_RL_DIM expansion; **no** residual thrash dials; **no** forward100 required for this channel pin.

### opinion

Creator right on train/infer channel + dim pin. Mark right on kill skip + sensor map. Counsel: **PROMOTE narrow channel law**; dual scoreboard later on this road.

### evidence

`tests/test_case0018_daypath_regime.py` (4 NEW). Code: regimes encode/decode; goal_path wire; policy curriculum doctrine.

### sources

- Sodhani et al. Multi-Task RL with Context (ICML 2021)  
- Fu et al. Effective Context for Meta-RL (AAAI 2021)  
- Court A17/A18; ROAD_FOR_THE_POLICY.md  

---

## Critic

| Check | Note |
|-------|------|
| Look-ahead | efficiency_proxy from snap counts/force only |
| Cliff | kill skip is road-sign, not pad-to-8 |
| Dim | META_RL_DIM 176 pinned |
| Dual | units only — no promote_ready claim |

---

## Optimist

Train/infer regime alignment 2x learnability of wait-vs-fire under A17.

---

## Judge pretrial

1. Run 4 NEW tests.  
2. Code: encode/decode + goal_path wire + curriculum doctrine pack.  
3. No forward100 this fire.  
4. PROMOTE narrow if green.  
5. Forbidden: pad, thrash residual, dim change.

---

## Results

`python -m pytest evidence_court/tests/test_case0018_daypath_regime.py -v` → **4/4 PASS**  
(with CASE-0017 regression: **8/8** joint green)

| Test | Role | Result |
|------|------|--------|
| `test_creator_new_regime_doctrine_encode_decode_distinct` | Creator | **PASS** |
| `test_mark_new_edge_sensors_map_to_a17_kill_playbook` | Mark | **PASS** |
| `test_creator_new_state_with_doctrine_keeps_meta_rl_dim` | Creator counter | **PASS** |
| `test_mark_new_curriculum_and_daypath_share_regime_doctrine_layout` | Mark counter | **PASS** |

---

## Judge IRAC

- **Issue:** Wire A17 into day-path state for frozen policy without cliffs?  
- **Rule:** A10+A15; A14 train; A17 catalog; A18 curriculum; ROAD; META_RL_DIM fixed.  
- **Application:** Units green; doctrine pack shared train/infer; kill skip; dim stable.  
- **Conclusion:**  
  1. **PROMOTE Law A19 (narrow)** — Day-path regime channel via Mark doctrine pack.  
  2. Code + tests as above.  
  3. Not dual/final-boss.  
  4. **Next CASE-0019:** learnable R / fill geometry for dual clears+A13 **on** this road (no residual thrash cliff).
