# CASE-0015 — Market ontology: win/pass, momentum, regimes, triggers, pullbacks, senses, intuition

**case_id:** CASE-0015  
**status:** PROMOTED (vocabulary + **TF/indicator bindings** — Court tested)  
**opened:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD  
**docket_rank:** 1  
**goal_gap:** learnability — shared vocabulary for trained meta-policy + Court  
**question:** How do we **define** (as shared road signs): momentum, regimes, triggers, pullbacks, **winning = reach target**, **passing = no breach**, intuition, senses — each bound to **groups of indicators** and **Mark timeframe sets** — so curriculum, edge, senses, and scoreboard speak one language?

**scope:** `evidence_court/meta_rl/market_ontology.py`, tests, case glossary  
**protected_invariants:** MARK_SETS_LAW; A10–A15; A14 train; no PROVEN overwrite; does **not** claim final-boss hit-rate alone  

**Orientation:** `ROAD_FOR_THE_POLICY.md` — names the road; weights still come from meta-train.

---

## ROUND STRUCTURE (Law A10)

```
Creator opening + NEW test → Mark opening + NEW test
→ one counter each → Critic → Optimist → Judge pretrial → experiment → IRAC
```

---

## Creator opening

### strongest_internet_argument

**Goal-conditioned RL needs an explicit outcome vocabulary:** success = reach goal state; constraint violation = failure of a separate class (risk floor). Hierarchical / goal-conditioned literature separates **goal achievement** from **constraint satisfaction**. Multi-TF practice separates **bias (HTF)** from **timing (LTF)** and names regimes (trend vs chop) so features are relational, not folklore levels.

**claim:** Machine-readable definitions for WIN/PASS/MISS/BREACH and structure/regime/trigger enums improve shared curriculum language without replacing training.

**new_test:** `test_creator_new_win_and_pass_definitions`

**prediction:** Win iff pnl≥target; pass iff not breach; joint classify_day_outcome matches table.

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. **Momentum = HTF force** (tide/gravity), not RSI alone (`PHYSICS_INFORMED_L2L`, sets law).  
2. **Pullback_resume** = dip against force then resume; **slingshot_load** = wait.  
3. **Continuation** = with force without deep dip.  
4. **Regime** = multi-set consensus (agree_long/short/conflict/incomplete).  
5. **Trigger** = fire only when HTF agrees and structure is not wait-class; conflict → kill.  
6. **Senses** = sight/feel/taste/hearing already Court law (CASE-0001).  
7. **Intuition** = what training puts in weights over senses — not a second rule bot.

**claim:** Ontology maps existing Mark/edge/senses vocabulary; pullback vs load vs fire is pin-tested.

**new_test:** `test_mark_new_momentum_regime_pullback_trigger`

---

## Creator counter (exactly one)

**counter:** Senses and intuition must be **named** so training docs and Court do not invent a fifth “magic” sense.  

**newer_test:** `test_creator_new_senses_and_intuition_vocabulary`

---

## Mark counter (exactly one)

**counter:** Policy aliases `launch`/`release` must map to pullback/continuation so ontology matches day path.  

**newer_test:** `test_mark_new_structure_event_aliases`

---

## Critic

| Check | Status |
|-------|--------|
| Look-ahead | Definitions only; no fill change |
| Cliff risk | Ontology must not become a frozen rule tree that replaces A14 train |
| Alignment | Win/pass match forward_eval hit_target / breach |
| Flea-jar | Does not claim high targets impossible |

---

## Optimist

Clear glossary 2x’s human+agent agreement on what to train for; reduces ISSUE-ROAD vocabulary fog.

---

## Judge pretrial

1. Run CASE-0015 NEW tests (4).  
2. **Code allowed:** additive `market_ontology.py` only (no goal_path thrash dials).  
3. PROMOTE as **narrow vocabulary law** if units green and glossary complete.  
4. Does **not** alone promote final-boss hit-rate.  
5. Forbidden: using this case to re-PROMOTE residual thrash cliffs.

---

## Results (vocabulary round)

Command: `python -m pytest evidence_court/tests/test_case0015_market_ontology.py -v` → **4/4 PASS**

| Test | Role | Result |
|------|------|--------|
| `test_creator_new_win_and_pass_definitions` | Creator opening | **PASS** |
| `test_mark_new_momentum_regime_pullback_trigger` | Mark opening | **PASS** |
| `test_creator_new_senses_and_intuition_vocabulary` | Creator counter | **PASS** |
| `test_mark_new_structure_event_aliases` | Mark counter | **PASS** |

**Code:** `meta_rl/market_ontology.py` (additive; no goal_path thrash).

---

## Amendment — TF + indicator groups (Court requirement)

Monty: terms **must** be defined with **groups of indicators** and **timeframes**.

### Creator amendment opening
**claim:** Each term carries `IndicatorGroup` + `TimeframeBinding` on all four MARK_SETS_LAW stacks (or scoreboard for win/pass).

**new_tests (suite `test_case0015_tf_indicator_bindings.py`):**
| Test | Role |
|------|------|
| `test_creator_new_mark_sets_law_stacks_pinned` | Creator |
| `test_mark_new_momentum_htf_indicators_and_tfs` | Mark |
| `test_mark_new_pullback_ltf_rsi_bb_on_each_set` | Mark |
| `test_creator_new_trigger_and_win_pass_indicator_groups` | Creator counter |
| `test_mark_new_senses_intuition_bound_to_all_sets` | Mark counter |
| `test_creator_new_htf_force_group_matches_edge_recipe` | Creator |

### Binding table (Law A16)

| Term | Indicator group | Timeframes |
|------|-----------------|------------|
| **Momentum** | `trend_dir(5)`, `trend_dir(10)`, `multi_day_momentum(3)` | HTF only on each set: set1 **15m+30m**, set2 **30m+1h**, set3 **1h+4h**, set4 **4h+1d** |
| **Regime** | multi-set `trend_dir` + consensus + efficiency | All 4 sets HTF |
| **Pullback / continuation / load** | **RSI(5)** + **BB(10, dev=0.5, shift=+2)** on LTF; force from HTF | All 4 sets: LTF **1m/5m/15m/30m** + that set’s HTFs |
| **Trigger** | htf_agree + structure_event + multi_set_consensus | All 4 sets |
| **Winning / passing** | realized_pnl, target_percent, risk, breach | **Scoreboard only** (day) — not chart TFs |
| **Senses** | htf_force, ltf_velocity, inertia, goal_risk channels | All 4 sets |
| **Intuition** | meta_rl_state_176 + set dirs + goal_risk_8 + sense probes | All 4 sets (learned A14) |

### Amendment results

`python -m pytest evidence_court/tests/test_case0015_tf_indicator_bindings.py evidence_court/tests/test_case0015_market_ontology.py -v` → **10/10 PASS**

---

## Judge IRAC

- **Issue:** Shared definitions for win/pass, momentum, regime, trigger, pullback, senses, intuition — **with indicator groups + Mark TFs**.  
- **Rule:** A10; MARK_SETS_LAW; ROAD; A14 train owns weights; every market term must bind TFs+indicators and be unit-tested.  
- **Application:** Vocabulary units + TF/indicator binding suite pin stacks and RSI/BB/trend_dir recipes.  
- **Conclusion / ruling:**  
  1. **PROMOTE Law A16 (amended)** — Market ontology with **TF + indicator bindings**.  
  2. Canonical `market_ontology.term_definitions()` + both test files.  
  3. Does **not** alone close ISSUE-DUAL or final boss.  
  4. Curriculum/edge must not redefine terms without a new Court case.
