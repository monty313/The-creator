# CASE-0010 — Path capacity: pullback carve-out + next-slot multi-leg (A10)

**case_id:** CASE-0010  
**status:** CLOSED  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**question:** What **measured** change raises hits/low_hr by **increasing day-PnL path capacity** via (a) **pullback single-set carve-out** under A12 HTF completed-only and (b) **path-to-next-slot** multi-leg without breach?

**scope:** `edge.py` path permission; `goal_path.py` fill window; tests; forward eval  
**protected_invariants:** MARK_SETS_LAW; Meta-RL 176; no-retrain; breach; A10; A12; F-011…F-014; no live deploy; PROVEN untouched  

**Prior:** Gates (0005/0009) and exit floors (0006–0008) failed to climb clears; hits=2 after 0009.

---

## ROUND STRUCTURE (Law A10)

```
Creator opening + NEW test → Mark opening + NEW test
→ one counter each → Critic → Optimist → Judge pretrial → experiment → IRAC
```

---

## Creator opening

### strongest_internet_argument

**Hierarchical multi-leg / sequential subgoals under a risk budget:** shorter hold windows (leg ends at next decision slot) free capital and allow residual legs to compound toward the day goal (goal-conditioned hierarchical control design class; scale-in / multi-leg residual risk practice).

Holding every leg to EOD blocks re-entry after early bank/stop within the same session cluster. Scale-in after partial progress is a standard residual-risk technique (not a claim that any paper proves XAU clears).

**claim:** `next_slot_end_time` fill windows raise multi-leg capacity vs EOD-only; unit-proved; measured on 100d.

**web_evidence (design class, not authority):** capital.com scale-in/out residual risk; goal-conditioned hierarchical RL subgoal chains (CoGHP class).

**new_test:** `tests/test_case0010_path_capacity.py::test_creator_new_next_slot_end_time` → **PASS**

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. **Pullback_resume is Mark LTF timing** after HTF force (A12 completed-only). A single official set with pullback + htf_agree is **complete Mark timing**, not thrash — multi-set gate (CASE-0005) starves slingshot launches.  
2. **Flea-jar:** missing valid pullbacks on confirmed force is **coverage failure**, not market refusal (`FLEA_JAR_COURT_LAW.md`).  
3. **Continuation** still needs multi-set or strong consensus (keep CASE-0005 for cont).  
4. **path_side_permission_ok** = side_permission_ok OR (pullback_resume ∧ n≥1 ∧ force≥0.15 ∧ htf_agree).

**law_physics:** gravity_tide | official_sets | decision_chain  
**law_belief_paths:** flea-jar; MARK_SETS; PHYSICS_INFORMED_L2L  

**claim:** Pullback single-set carve-out increases quality fire capacity; continuation remains gated.

**new_test:** `tests/test_case0010_path_capacity.py::test_mark_new_pullback_single_set_carveout` → **PASS**

---

## Creator counter (exactly one)

**counter:** Last slot of day must still path to EOD (no invented post-session bars).  

**newer_test:** `test_creator_new_last_slot_ends_eod` → **PASS**

---

## Mark counter (exactly one)

**counter:** Carve-out must **not** open single-set **continuation** (thrash).  

**newer_test:** `test_mark_new_continuation_single_set_still_blocked` → **PASS**

---

## Critic

| Check | Status |
|-------|--------|
| Look-ahead | next slot is scheduled decision time; bars only until end_time |
| Flea-jar | more pullback paths intended; multi-leg residual |
| CASE-0005 | base `side_permission_ok` unchanged for continuation |
| A12 | HTF completed-only unchanged |
| Risk | envelope still hard |

---

## Optimist

Hits≥12 OR low_hr≥0.18; breach 0; beat CASE-0009 (2 / 0.04) and prefer ≥ CASE-0005 (3 / 0.08). Fire capacity ↑ without hit conversion is **incomplete win**.

---

## Judge pretrial (BEFORE experiment)

1. Run CASE-0010 NEW tests.  
2. **Code:** `path_side_permission_ok` in edge; `next_slot_end_time` in goal_path; wire day path to both.  
3. Measure forward100 seed=42.  
4. PROMOTE win-path only if hits≥12 OR low_hr≥0.18 + breach0 + L2L/senses.  
5. Else REJECT; ADMIT experimental if units + breach0.  
6. Forbidden: full BE re-PROMOTE; undirected dials; live MT5.

---

## Test results

Command: `python -m pytest evidence_court/tests/test_case0010_path_capacity.py evidence_court/tests/test_case0005_side_confluence.py evidence_court/tests/test_goal_path_case0003.py -v`

| Test | Role | Result |
|------|------|--------|
| `test_creator_new_next_slot_end_time` | Creator opening | **PASS** |
| `test_mark_new_pullback_single_set_carveout` | Mark opening | **PASS** |
| `test_creator_new_last_slot_ends_eod` | Creator counter | **PASS** |
| `test_mark_new_continuation_single_set_still_blocked` | Mark counter | **PASS** |
| CASE-0005 suite | regression | **PASS** |
| goal_path case0003 | regression | **PASS** |

**12/12 PASS**

---

## Code landed (Judge-ordered only — no extra dials)

| Symbol | Path | Role |
|--------|------|------|
| `path_side_permission_ok` | `meta_rl/edge.py` | multi-set OR pullback single-set carve-out |
| `next_slot_end_time` | `meta_rl/goal_path.py` | fill ends at next slot; last → EOD |
| wire | `run_goal_path_day` | uses both |

---

## 100d measurement (Judge order)

| Metric | CASE-0009 | CASE-0010 | Threshold |
|--------|----------:|----------:|-----------|
| n_days | 100 | 100 | ≥100 |
| breach_count | 0 | **0** | =0 |
| no_retrain | true | true | true |
| l2l / senses | true | true | true |
| total_hits | 2 | **2** | ≥12 |
| low_hit_rate | 0.04 | **0.04** | ≥0.18 |
| low_fire_rate | 0.28 | **0.40** | — (↑ capacity) |
| max_day_pnl | — | **30.0** | — |
| promote_ready | false | **false** | true |

Artifact: `evidence_court/artifacts/forward100_report.json`  
SHA256: `8bd5597eb0cc43048bc10ae4aa99842ee664c231603d1934ede809de2474f0f9`

---

## Judge IRAC

- **Issue:** Do pullback single-set carve-out + next-slot multi-leg promote as the consistent-clear path?  
- **Rule:** A10 evidence; flea-jar; promote if hits≥12 OR low_hr≥0.18 with breach0; do not re-PROMOTE pure gates/floors (F-011…F-014).  
- **Application:**  
  - Units **proved** both mechanisms.  
  - 100d: breach **0**, L2L/senses OK.  
  - **low_fire_rate 0.28→0.40** — path capacity **did increase** (hypothesis direction on fire).  
  - **hits still 2 / low_hr still 0.04** — no conversion climb; fails promote thresholds. Extra fires are not extra clears.  
- **Conclusion / ruling:**  
  1. **REJECT** win-path / final-boss PROMOTE.  
  2. **ADMIT experimental only:** `path_side_permission_ok` + `next_slot_end_time` may stay in code (unit-proved, no breach harm) — **no win claim**, not MASTER law.  
  3. **F-016** — bundled pullback carve-out + next-slot: fire↑ hits flat (conversion bottleneck). Note **F-015/A13**: 5-slot path is non-compliant production identity (must 8–400 trades/day).  
  4. **Next CASE-0011** under A10: **dense scalping cadence** toward A13 [8,400] (multi-leg clock) **and/or** isolate carve-out+EOD; not pure gates/floors.

---

## Process

No undirected dials. Court-complete. Loop may open CASE-0011 under A10 only.
