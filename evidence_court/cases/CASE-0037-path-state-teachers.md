# CASE-0037 — Packed path-state teachers at brain-wait (C-003 residual)

**case_id:** CASE-0037  
**status:** CLOSED — units **4/4 PASS**; dual **PROMOTE_NARROW** (champion replace); C-003 residual remains (n_zero 18 / hits 11)  
**opened:** 2026-08-08  
**docket_issue_id:** C-003 residual / C-002 residual  
**goal_axes:** G-A13, G-TRAIN, G-CLEAR, G-NO_RETRAIN, G-SIGHT  

**question:** Does offline train on **exact packed path states** where the brain waited on real Mark candidates (state, teacher_act) raise **a13_frac** and/or cut **n_zero** vs floor without undoing prefer hits≥11 / low_hr≥0.28 / a13≥28% and without F-011…F-025?

**scope:** `collect_path_state_teachers` in `run_goal_path_day` + `path_state_harvest` + shadow train + dual; **no** live force; **no** PROVEN overwrite until PROMOTE; **no** `opportunity_label_to_training_example` rebuild  

**protected:** empty skip; no residual multi thrash; no F-024/F-025 class  

**Baseline floor:** breach 0 | hits 11 | low_hr 0.28 | a13 28% | mean_tr 7.38 | n_zero 39 | max_pnl 70  

**Evidence why this lever:** F-024 synthetic densify and F-025 real-bar **labels** with synthetic state rebuild both densified active days only (n_zero↑). Offline RL coverage literature requires teachers on **visited states**. Dump the state the brain actually saw when it waited.

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → pretrial → measure → IRAC

---

## Creator opening

### strongest_internet_argument

Offline RL improvement requires action labels on states in the **behavior support**. Rebuilding a proxy official vector from miss metadata (F-025) leaves a distribution gap vs silent-day decisions. BC / offline actor-critic and counterfactual offline methods train on logged states. Path dump closes the gap: teacher fire on the exact wait-state.

**claim:** Packed path-state teachers at brain-wait → offline train → better silent-day fire map without pad.

**new_test:** `test_creator_new_filter_requires_full_dim_path_state`

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. Teacher topology ⊆ {PB, cont}.  
2. Teacher side = Mark edge act on that candidate.  
3. State must be full META_RL_DIM packed eyes + goal context.  
4. London/NY weight higher.  
5. No live force; empty skip remains.

**claim:** apply_path_state uses packed vector; filter rejects wrong dim / chop / synthetic source.

**new_test:** `test_mark_new_apply_path_state_updates_on_packed_state`

---

## Creator counter

**counter:** Freeze at prove across pairs (A14).  
**newer_test:** `test_creator_new_path_state_train_freezes_no_retrain`

---

## Mark counter

**counter:** collect flag default off for production dual speed; empty skip true.  
**newer_test:** `test_mark_new_goal_path_exposes_collect_flag_no_pad`

---

## Counsel opinion (A15)

### internet_sift
Offline RL coverage / CQL pessimism; behavior-cloned states; F-024/F-025 Court self-evidence.

### policy_recommendation
1. Collect path-state teachers only in harvest (flag).  
2. Train shadow on packed states.  
3. Dual vs floor.  
4. PROMOTE champion only if dual improves without prefer floor break.  
5. Reject label→synthetic rebuild class.

### opinion
This is the correct residual after F-025.

### sources
Offline RL coverage; A14/A28/A29; F-025 remedy text.

---

## Critic
- Harvest may still under-cover pure empty-candidate days (no brain state).  
- Over-fire risk if teachers dense.

## Optimist
- Directly attacks F-025 root cause.  
- Road not cliff.

---

## Judge pretrial

1. Units 4/4  
2. Harvest n_days≈30  
3. Shadow train  
4. forward100 dual  
5. PROMOTE only on dual improve  

---

## Experiment results

| Metric | Floor (pre-0037) | Path-state meta4275 | Δ | F-024/F-025 ref |
|--------|-----------------:|--------------------:|---|----------------:|
| hits | 11 | **11** | 0 | 11 |
| low_hr | 0.28 | **0.28** | **prefer held** | 0.24 break |
| a13_frac | 0.28 | **0.64** | **+0.36** | 0.38 |
| n_zero | 39 | **18** | **−21** | 45 worse |
| mean_tr | 7.38 | **39.4** | +32 | ~21 |
| buckets | 0:39 / 1–7:33 / 8+:28 | **0:18 / 1–7:18 / 8+:64** | — | — |
| max_pnl | 70 | 70 | 0 | 70 |
| breach | 0 | 0 | held | 0 |
| promote_ready | false | false | (hits still short) | — |

| Check | Result |
|-------|--------|
| Units 4/4 | **PASS** |
| Harvest | **DONE** 400 packed states (362 LN) · dim 176 ok |
| Shadow train | **DONE** meta4275 |
| forward100 | **DONE** SHA256 `2e5533de02447d95149a04322a07f7c8030a1c6cfa6d1f1c3a669965db311515` |
| Champion | **PROMOTED** from shadow (prior backed up `meta_policy_champion_pre0037.npz`) |

**Interpretation:** Packed path-state teachers fix F-025 root cause. Silent days cut hard; A13 day-share more than doubles; prefer floor held (unlike F-024/F-025). Hits flat — conversion residual → C-004.

---

## Judge IRAC

### Issue
Does offline train on exact packed path wait-states raise a13 / cut n_zero without undoing prefer floor?

### Rule
A10+A15 · A13 · A14 freeze · A28 offline · ROAD · floor prefer ≥11/0.28/a13≥28% · no F-011…F-025 · PROVEN replace only on dual improve.

### Application
- Units prove full-dim path_state filter, packed meta_update, freeze, collect flag default off.  
- Harvest: 400 path states (362 LN) from real brain-wait candidates.  
- Dual seed=42: a13 **28%→64%**; n_zero **39→18**; mean_tr **7.38→39.4**; hits **11**; low_hr **0.28 prefer held**; breach 0.  
- Contrasts F-024/F-025 (n_zero worse, low_hr prefer break).

### Conclusion
1. **PROMOTE_NARROW** — path-state teacher train is production champion path for C-003 density lever.  
2. Champion artifact replaced with meta4275 path-state shadow (prior champion backup retained).  
3. `collect_path_state_teachers` remains harvest-only (default False on dual).  
4. **C-003 residual open:** 18 zero + 18 partial days; not every-day A13 yet.  
5. **C-004** still blocks hits/promote_ready.  
6. Next levers: more path-state coverage / partial-day geometry / A34 game-train / conversion — **not** F-024/F-025 class.