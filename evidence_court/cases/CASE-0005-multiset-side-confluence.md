# CASE-0005 — Multi-set side confluence gate (A10 full Court)

**case_id:** CASE-0005  
**status:** CLOSED  
**opened:** 2026-08-07 (scheduled Court fire)  
**closed:** 2026-08-07  
**question:** What **measured** multi-set side / confluence rule raises low-band hit_rate and total_hits on the same 100d random protocol without breach, retrain, look-ahead, or Mark-law break?

**scope:** `evidence_court/meta_rl/edge.py`, `goal_path.py`, tests, forward eval measurement  
**protected_invariants:** MARK_SETS_LAW; Meta-RL 176; no-retrain; breach envelope; Law A10; A12 HTF completed-only; no live deploy; PROVEN untouched  

**Prior evidence (CASE-0004):** breach 0, hits **3**, low_hr **0.08**, promote_ready false. A12 promoted narrow. Bottleneck = side quality / clear frequency.

---

## ROUND STRUCTURE (Law A10) — binding

```
OPENING (Creator internet + new test) → OPENING (Mark knowledge + new test)
→ OPENING TESTS RUN → ONE COUNTER each + newer tests → Critic → Optimist → Judge IRAC
```

---

## Creator opening

### strongest_internet_argument

**Multi-timeframe confluence / multi-scale agreement is a standard quality filter: trade only when independent TF scales agree on side; single-scale screams are higher false-positive.**

Evidence class (not authority):

1. **MTF confluence literature:** top-down multi-TF analysis treats agreement across scales as higher-quality bias; conflicting or single-TF signals are discarded or downgraded (classic Elder-style multi-TF + confluence filters in retail/quant practice writeups).  
2. **Ensemble / vote filters:** independent estimators agreeing reduces noise vs one estimator alone (signal-processing design class applied to multi-set edges).  
3. **False-positive control under fixed risk:** when breach must stay 0, quality gates beat volume gates for clear % (trading systems design: fewer higher-quality entries under hard risk).

**claim (falsifiable):** Requiring **≥2 official Mark sets** to agree on the same actionable side (pullback_resume or continuation + htf_agree) before fire — with a narrow high-force consensus carve-out — improves side legitimacy vs single-set permission; measurable by (a) unit proof of gate logic, (b) 100d random hits / low_hr vs CASE-0004 baseline (hits=3, low_hr=0.08).

**mechanism:** `count_actionable_side_agree` + `side_permission_ok(min_sets=2)` in edge; goal_path uses gate instead of `n_side < 1`.

**web_evidence (design class):**
- Multi-timeframe confluence / agreement filters (tradeciety, BabyPips multi-TF, Investopedia multi-timeframe analysis — design class).  
- Ensemble agreement reduces false positives (general statistical design class).

**prediction:** Unit: 1-set snap → permission false; 2-set same side → true. Forward: breach stays 0; hit metrics re-measured.

**falsifier:** Gate allows 1-set without carve-out; OR breach > 0; OR “proof” is only CASE-0004 greens.

**new_test (opening):**
- path: `tests/test_case0005_side_confluence.py::test_creator_new_side_permission_requires_two_sets`
- why_new: never existed; CASE-0004 tested HTF completed-only / goal-lock, not multi-set side count gate
- result: **RUN in this case**

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

From **@physics** + pack (context for theory; **not** closing proof):

1. **Official four sets are law** — LTF timing + dual HTF confirmation per set; scanning all four is mandatory (`MARK_SETS_LAW`). A single set screaming is **incomplete force**, not full permission.  
2. **Gravity / multi-scale force** — independent confirmation stacks must co-align; fighting incomplete consensus is thrash (`PHYSICS_INFORMED_L2L`, multi-set conflict = wait).  
3. **Decision chain** — HTF agree first, then LTF timing; multi-set side agreement is the next permission ring after A12 completed HTF.  
4. **Flea-jar** — do not declare “impossible”; keep a narrow path when **full multi-set consensus** + strong force (not silence).

**claim:** Side permission requires multi-set actionable agreement (≥2 sets same act+htf_agree+actionable topology), OR full `agree_long`/`agree_short` consensus with strong |force|; proved only by **new** tests this case.

**law_physics:** multi_scale_force | official_sets | incomplete_not_permission  
**law_belief_paths:** MARK_SETS_LAW, PHYSICS_INFORMED_L2L, flea-jar doctrine  

**prediction:** Synthetic snap with 1 actionable set → `side_permission_ok` false; 2 sets same side → true; consensus agree_long + |force|≥0.40 with 1 set → true (flea-jar carve-out).

**falsifier:** Single weak set passes; OR consensus+strong force blocked with no path.

**new_test (opening):**
- path: `tests/test_case0005_side_confluence.py::test_mark_new_count_actionable_side_agree`
- why_new: new pure count assertion on SetEdge lists for this case
- result: **RUN in this case**

---

## Creator counter (exactly one)

**counter_argument:** Hard `n_sets≥2` alone can starve valid high-force days when only one set has LTF timing while all HTF forces agree. Internet ensemble literature allows **strong prior + one confirming likelihood**. Carve-out: `multi_set_consensus` matches side AND `abs(force)≥0.40` may pass with n=1.

**newer_test:** `test_creator_new_consensus_strong_force_carveout` — distinct from two-set requirement test.

**prediction:** agree_long + force 0.45 + one long set → permission true; incomplete + force 0.45 + one long → false.

**falsifier:** Carve-out fires on incomplete consensus; OR blocks strong consensus.

---

## Mark counter (exactly one)

**counter_argument:** Carve-out must not re-open thrash: force floor on single-set path must be **strict** (≥0.40) and consensus must be full agree_long/agree_short — not “incomplete” with one loud LTF.

**newer_test:** `test_mark_new_weak_single_set_blocked` — n=1, incomplete consensus, force 0.25 → permission false.

**prediction:** Weak single-set never passes.

**falsifier:** Weak single-set returns true.

---

## Critic cross-examination

| Check | Status |
|-------|--------|
| Look-ahead | Gate uses only already-computed set edges (A12 HTF completed-only upstream) |
| Flea-jar | Carve-out preserves path when full consensus + strong force |
| Risk | No change to envelope / size math |
| No-retrain | Inference-only filter |
| Sample starvation | Possible fewer fires — measure hits, not fire rate alone |
| Process | Full A10 before code land |

**failure_conditions:** breach>0; train_step; PROMOTE without 100d re-measure; silent weakening of MARK_SETS scan

---

## Optimist challenge

- Multi-set agreement can cut wrong-side thrash and raise low-band clear rate if wrong-side was the leak.  
- 2x test: same seed 100d vs CASE-0004 (hits=3, low_hr=0.08).  
- Threshold: total_hits ≥ 12 OR low_hit_rate ≥ 0.18; breach 0.

---

## Judge pretrial order (written BEFORE experiment)

1. Run all CASE-0005 **new** unit tests; record pass/fail.  
2. **Allowed code (smallest):** implement `count_actionable_side_agree` + `side_permission_ok` in `edge.py`; wire `goal_path` to use `side_permission_ok` instead of bare `n_side < 1`.  
3. **Measurement:**  
   `python -m evidence_court.meta_rl.cli forward100 --days 100`  
   (seed=42, pair_mode=random, goal path) → save `artifacts/forward100_report.json` + SHA256.  
4. **Pass thresholds for win-path PROMOTE consideration:**  
   - breach_count = 0  
   - no_retrain = true  
   - l2l_day_path_ok + senses_day_path_ok  
   - total_hits ≥ 12 OR low_hit_rate ≥ 0.18  
   - unit A10 tests green  
5. **If thresholds fail:** REJECT win-path PROMOTE; may ADMIT multi-set gate as experimental fragment if units prove logic and breach 0.  
6. **Forbidden:** more undirected dials without a new case.

---

## Opening + counter test results (execution record)

Command: `python -m pytest evidence_court/tests/test_case0005_side_confluence.py -v`

| Test | Side | Result |
|------|------|--------|
| `test_creator_new_side_permission_requires_two_sets` | Creator opening | **PASS** |
| `test_mark_new_count_actionable_side_agree` | Mark opening | **PASS** |
| `test_creator_new_consensus_strong_force_carveout` | Creator counter | **PASS** |
| `test_mark_new_weak_single_set_blocked` | Mark counter | **PASS** |

**Opening + counter unit evidence:** all 4 NEW tests green (2026-08-07).

---

## Code landed (Judge-ordered smallest experiment)

| Symbol | Path | Role |
|--------|------|------|
| `count_actionable_side_agree` | `meta_rl/edge.py` | Count sets with same act+htf_agree+actionable topo |
| `side_permission_ok` | `meta_rl/edge.py` | ≥2 sets OR consensus+force≥0.40 carve-out |
| wire | `meta_rl/goal_path.py` | Gate replaces bare `n_side < 1` |

---

## 100d measurement (Judge order step 3)

| Metric | CASE-0004 baseline | After CASE-0005 | Threshold |
|--------|-------------------:|----------------:|-----------|
| n_days | 100 | **100** | ≥100 |
| breach_count | 0 | **0** | =0 |
| no_retrain | true | true | true |
| l2l / senses | true | true | true |
| total_hits | 3 | **3** | ≥12 |
| low_hit_rate | 0.08 | **0.08** | ≥0.18 |
| low_fire_rate | 0.56 | **0.32** | — (dropped) |
| high_fire_rate | 0.51 | **0.22** | — (dropped) |
| max_day_pnl | 30.0 | **30.0** | — |
| promote_ready | false | **false** | true for FINAL |

Artifact: `evidence_court/artifacts/forward100_report.json`  
SHA256: `96bc6ee489c7846a7bf3caa5c09d211e333e18995a78675f145be9a351f47a52`

**Interpretation:** Confluence gate **reduced fire rate** (~half) but **did not raise hits**. Wrong-side thrash was not the binding constraint on clears under this seed/window — or the remaining trades are still insufficient R / wrong timing. Side-quality-as-count-filter alone is insufficient for final boss.

---

## Judge IRAC

- **Issue:** May multi-set side confluence (`side_permission_ok`) be PROMOTED as the consistent-winning path for the final boss?  
- **Rule:** A10 (openings+counters+new tests); flea-jar; no look-ahead; promote thresholds (hits≥12 or low_hr≥0.18; breach 0; no retrain; L2L/senses).  
- **Application:**  
  - Unit evidence **passed** (4/4 NEW tests) — two-set requirement, count purity, consensus carve-out, weak single-set blocked.  
  - 100d random matrix: breach 0, no retrain, L2L/senses OK — **safety holds**.  
  - Hit rate: **3/100 unchanged**; low_hr **0.08 unchanged**; fire rates fell. Claim “confluence gate wins consistent clears” is **not** supported.  
- **Conclusion / ruling:**  
  1. **REJECT** PROMOTE of multi-set confluence as final-boss / consistent target-hitter solution.  
  2. **ADMIT experimental only** (not architecture law): `count_actionable_side_agree` + `side_permission_ok` may remain in path (unit-proved, no breach harm) but **no win claim** and **not** MASTER_ARCHITECTURE law.  
  3. **Next case required under A10:** different measured lever — e.g. **R-capture / sizing-toward-goal under envelope**, **pullback-only first entry quality**, or **fill/exit path** that converts correct-side days into clears without inventing undirected dials. Bottleneck remains **clear frequency**, not structure/safety.

---

## Next

**CASE-0006** — open under full A10 before coding: what measured change raises **R-capture or low-band clear rate** on same 100d random protocol without breach (hits≥12 or low_hr≥0.18).
