# CASE-0004 — HTF completed-only force + side quality (A10 full Court)

**case_id:** CASE-0004  
**status:** IN_COURT  
**opened:** 2026-08-07 (resume)  
**question:** What measured change to HTF force / side permission raises **random-target hit rate** over forward days without breach, retrain, look-ahead, or Mark-law break — and may any already-landed experimental code be PROMOTED only after A10 evidence?

**scope:** `evidence_court/meta_rl/edge.py`, `goal_path.py`, tests, forward eval measurement  
**protected_invariants:** MARK_SETS_LAW; Meta-RL 176; no-retrain; breach envelope; Law A10; no live deploy; PROVEN untouched  

**Process note (Judge):** Prior session landed edge/path edits **without** completing A10 openings → counters → pretrial. That is a **process defect**. This case reopens under full A10. Experimental code is **not** law until PROMOTE on measured evidence.

---

## ROUND STRUCTURE (Law A10) — binding

```
OPENING (Creator internet + new test) → OPENING (Mark knowledge + new test)
→ OPENING TESTS RUN → ONE COUNTER each + newer tests → Critic → Optimist → Judge IRAC
```

---

## Creator opening

### strongest_internet_argument

**Multi-timeframe top-down confirmation uses completed higher-timeframe structure for bias; unfinished HTF bars repaint / bias entries.**

Evidence class (not authority):

1. **Elder / multi-TF principle:** higher TF sets direction; lower TF times entry in that direction (classic top-down MTF; Quantpedia Elder D1H1-style filter discussion).  
2. **Non-repainting HTF practice:** confirmed HTF offsets only — unfinished Daily/H4 candles must not publish premature zones (TradingView multi-TF design literature: confirmed source-TF, no look-ahead).  
3. **Goal-conditioned RL design class:** daily target is a goal state; subgoals under constraint (CoGHP / hierarchical GCRL — design class for *structuring* remaining-target behavior, not a claim of paper accuracy on XAU).

**claim (falsifiable):** Restricting HTF force inputs to **fully completed calendar periods** (date < decision date when deciding intraday) improves side legitimacy vs using partial same-day HTF buckets; measurable by (a) unit proof of exclusion, (b) forward hit_rate / side-agree rate vs pre-change artifact under same seed window **if** baseline re-runnable.

**mechanism:** `_htf_completed_only` + optional multi-day completed-close momentum gate; LTF may still use same-day bars before `asof_time` for timing only.

**web_evidence:**
- MTF top-down / HTF bias then LTF entry (tradeciety, VT Markets, Investopedia multi-timeframe guides — design class).  
- Non-repainting HTF: confirmed historical offsets, no unfinished D/H4 (TradingView multi-TF writeups).  
- Goal-conditioned hierarchical RL for long-horizon goals (CoGHP arxiv 2602.03389 — design class only).

**prediction:** Unit tests prove same-day HTF excluded under `asof_time`. Multi-day momentum returns non-zero signed tide on synthetic 3-up days. Forward 100d: breach stays 0; hit metrics **must be re-measured** — no promotion on hope.

**falsifier:** Same-day HTF still appears in HTF filter under asof_time; OR breach > 0; OR “proof” is only old CASE-0002 greens.

**new_test (opening):**
- path: `tests/test_case0004_edge_quality.py::test_creator_new_htf_excludes_same_day_when_asof_time`
- why_new: new fixture asserts date < asof_date for HTF under asof_time — never existed before CASE-0004
- result: **RUN in this case**

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

From **@physics** + pack (context for theory; **not** closing proof):

1. **HTF tide / gravity is law first** — LTF velocity must not own side against HTF (`PHYSICS_INFORMED_L2L.md`: PINN-style anti-HTF penalty; force before LTF).  
2. **Official sets:** LTF first for timing, last two TFs confirmation — incomplete confirmation = no permission (MARK_SETS_LAW / FULL_OBS).  
3. **Slingshot_load = wait** — inertia with + velocity against is load, not reverse thrash.  
4. **Flea-jar:** low hits are not “market impossible” without full action-space bound; but **wrong-side fire** is a policy defect, not a lid.

**claim:** Side permission requires HTF agreement from **completed** confirmation structure; multi-day completed closes as tide check; fighting multi-day tide must kill or wait — proved only by **new** tests this case.

**law_physics:** gravity_tide | official_sets | decision_chain  
**law_belief_paths:** `mark_here/knowledge/kag/army/PHYSICS_INFORMED_L2L.md`, `FULL_OBS_AND_TIMEFRAME_SETS`, flea-jar doctrine  

**prediction:** `multi_day_momentum` on 3 completed up-days → mom > 0. HTF incomplete + LTF scream must not force act without htf_agree.

**falsifier:** Momentum test fails on clear synthetic series; OR production path trades against completed multi-day tide with htf_agree true from partial day only.

**new_test (opening):**
- path: `tests/test_case0004_edge_quality.py::test_mark_new_multi_day_momentum_signed`
- why_new: new synthetic multi-day closed-bar momentum assertion for this case
- result: **RUN in this case**

---

## Opening test results (execution record)

Command: `python -m pytest evidence_court/tests/test_case0004_edge_quality.py -v`

| Test | Side | Result |
|------|------|--------|
| `test_creator_new_htf_excludes_same_day_when_asof_time` | Creator opening | **PASS** |
| `test_mark_new_multi_day_momentum_signed` | Mark opening | **PASS** |
| `test_creator_new_goal_lock_exits_at_remaining_target` | Creator counter | **PASS** |
| `test_mark_new_goal_lock_respects_stop_before_lock` | Mark counter | **PASS** |

**Opening + counter unit evidence:** all 4 NEW tests green (2026-08-07).

---

## Creator counter (exactly one)

**counter_argument:** Completed HTF alone is necessary but not sufficient for **hit rate**. Goal-conditioned **lock exit** when floating PnL reaches remaining target converts correct-side days into clears (GCRL “reach goal then stop”) without raising risk envelope.

**newer_test:** `test_creator_new_goal_lock_exits_at_remaining_target` — distinct from HTF exclusion test.

**prediction:** On synthetic +1% path with size 2.5% and lock 5%, fill returns exactly 5.0.

**falsifier:** Lock returns > remaining or ignores stop; OR uses future bar beyond path.

---

## Mark counter (exactly one)

**counter_argument:** Goal-lock using bar high/low is optimistic intra-bar fill; Mark requires it not become a force-side oracle and not breach envelope. Prefer lock only when size is risk-legal; stop still hard.

**newer_test:** (order) extend suite — `test_mark_new_goal_lock_respects_stop_before_lock` if missing: stop-out path still returns ≤ -size when adverse hits first.

**prediction:** Adverse bar hitting stop before lock → loss ≈ -size - friction; no phantom hit.

**falsifier:** Stop ignored when lock set.

---

## Critic cross-examination

| Check | Status |
|-------|--------|
| Look-ahead | HTF completed-only addresses partial-day 1d/4h; LTF still prior-only via asof_time |
| Goal-lock high/low | Optimistic vs touch-and-reject; must label `forward_sim_shadow` and not claim live MT5 |
| Risk | size still via envelope; lock does not increase risk % |
| No-retrain | inference-only |
| Flea-jar | must not shrink action space to “only micro targets”; high targets still attempted under envelope |
| Process | prior no-Court code = defect; this filing repairs procedure |

**failure_conditions:** breach>0; train_step; same-day HTF in force path; PROMOTE without 100d re-measure

---

## Optimist challenge

- Goal-lock can 2x low-band clear rate **if** side quality improved (correct-side days become hits).  
- Multi-day tide gate can cut thrash days.  
- 2x test: same seed 100d — compare total_hits and low_hit_rate **after** PROMOTE-eligible experiment vs last checkpoint numbers (hits=2, low_hr=0.08).  
- Do not relax breach=0.

---

## Judge pretrial order

**Before any further production feature invention:**

1. Run all CASE-0004 **new** unit tests; record pass/fail in this file + JSON.  
2. Add Mark newer-test for stop-before-lock if not present; run it.  
3. **Measurement experiment only (allowed code):** keep experimental HTF-completed + multi-day + goal-lock **if unit tests pass**; run  
   `run_forward_eval(n_days=100, seed=42, pair_mode='random', use_goal_path=True)`  
   Save `artifacts/forward100_report.json` + SHA256.  
4. **Pass thresholds for ADMIT_EXPERIMENT → PROMOTE consideration:**  
   - breach_count = 0  
   - no_retrain = true  
   - l2l_day_path_ok + senses_day_path_ok  
   - total_hits ≥ 12 OR low_hit_rate ≥ 0.18 (consistent spectrum path)  
   - unit A10 tests green  
5. **If thresholds fail:** REJECT promotion of experimental path as “winning bot”; may ADMIT components that unit-prove (HTF completed-only) as **law fragments** only if Critic agrees no harm; hit-rate claim stays unproven.  
6. **Forbidden:** more undirected dials without a new case + new tests.

---

## 100d measurement (Judge order step 3)

| Metric | Checkpoint before | After CASE-0004 experiment | Threshold |
|--------|------------------:|---------------------------:|-----------|
| n_days | 100 | 100 | ≥100 |
| breach_count | 0 | **0** | =0 |
| no_retrain | true | true | true |
| l2l / senses | true | true | true |
| total_hits | 2 | **3** | ≥12 |
| low_hit_rate | 0.08 | **0.08** | ≥0.18 |
| max_day_pnl | ~32 | **30.0** | — |
| promote_ready | false | **false** | true |

Artifact: `evidence_court/artifacts/forward100_report.json`  
SHA256: `cfb16cc34c2ad84e5eb730bf31acceb6841b3c8d8c15366f71287e91a11a0df0`

---

## Judge IRAC

- **Issue:** May CASE-0004 experimental side-quality + goal-lock be PROMOTED as the consistent-winning path for the final boss?  
- **Rule:** A10 (openings+counters+new tests); flea-jar; no look-ahead; promote thresholds (hits≥12 or low_hr≥0.18; breach 0; no retrain; L2L/senses).  
- **Application:**  
  - Unit evidence **passed** (4/4 NEW tests) — HTF completed-only exclusion, multi-day momentum sign, goal-lock exit, stop-before-lock.  
  - 100d random matrix: breach 0, no retrain, L2L/senses OK — **safety holds**.  
  - Hit rate: 3/100 (was 2/100) — **does not meet** consistent-clear thresholds. Claim “we have a consistent winning bot” is **not** supported.  
- **Conclusion / ruling:**  
  1. **PROMOTE (narrow law only):** HTF confirmation must use completed periods when deciding intraday (`_htf_completed_only`) — unit-proved anti-look-ahead / anti-repaint fragment.  
  2. **ADMIT only (not final path):** multi-day momentum assist + goal-lock exit remain experimental — allowed in code path but **not** a win claim.  
  3. **REJECT** PROMOTE of CASE-0004 as final-boss solution / consistent target-hitter.  
  4. **Next case required** under A10: new internet + Mark knowledge arguments for **side accuracy / edge edge** — measured, not invented dials.

---

## Process law reminder (this case)

**Creator may not ship major bot behavior outside Court.**  
Monty order 2026-08-07: work from evidence, full Court each major decision.
