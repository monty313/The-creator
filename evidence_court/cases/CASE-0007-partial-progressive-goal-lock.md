# CASE-0007 — Partial progressive goal lock (A10 full Court)

**case_id:** CASE-0007  
**status:** CLOSED  
**opened:** 2026-08-07 (scheduled Court fire)  
**closed:** 2026-08-07  
**question:** What **measured** change raises low-band hit_rate and total_hits via **partial progressive goal lock** (bank a fraction of rem_goal at intermediate floating; leave runner for full lock) on the same 100d random protocol without breach — **without** re-promoting full BE (F-011)?

**scope:** `evidence_court/meta_rl/goal_path.py` (exit path only); tests; forward eval  
**protected_invariants:** MARK_SETS_LAW; Meta-RL 176; no-retrain; breach envelope; Law A10; A12; F-011 (no full-BE win claim); no live deploy; PROVEN untouched  

**Prior evidence:**
| Case | Lever | hits | low_hr |
|------|-------|-----:|-------:|
| 0005 | multi-set permission | 3 | 0.08 |
| 0006 | full BE @1.5R + pb size 1R | **2** | **0.04** |

Full BE scratched runners (F-011). This case: **partial floor** + trail off.

---

## ROUND STRUCTURE (Law A10) — binding

```
OPENING (Creator internet + new test) → OPENING (Mark knowledge + new test)
→ ONE COUNTER each + newer tests → Critic → Optimist → Judge IRAC
```

---

## Creator opening

### strongest_internet_argument

**Partial scale-out / multi-target exit management banks a fraction of the planned objective when price reaches an intermediate level, then leaves a runner for the full target — improving day-clear rate without the premature full-BE scratch mode that cuts expectancy.**

Evidence class (not authority):

1. **Scale-out / partial take-profit design class** (retail + systematic trade management): take ½ at intermediate objective; remainder targets full objective.  
2. **Contrast with full BE (F-011 measured fail):** full stop-to-entry after +1.5R zeros retest trades; partial **floor at 50% of remaining day goal** keeps banked equity-% when path later hits original stop.  
3. **Goal-conditioned hierarchical control:** intermediate subgoal (50% of rem_goal) then residual subgoal.

**claim:** `partial_lock_frac=0.5` progressive floor (trail **off**) improves clears vs CASE-0006 and aims at promote thresholds; unit-proved.

**new_test:** `test_creator_new_partial_floor_saves_after_half_goal` — **PASS**

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. **Slingshot partial release** — bank half remaining goal after expansion; leave force-runner.  
2. **F-011 binding** — no full-BE win re-argument.  
3. Pure helper `progressive_partial_floor` is path-only.

**new_test:** `test_mark_new_progressive_partial_floor_pure` — **PASS**

---

## Creator counter (exactly one)

**counter:** frac ≥ 1.0 collapses to invalid early full lock; require 0 &lt; frac &lt; 1.  
**newer_test:** `test_creator_new_partial_frac_invalid_no_floor` — **PASS**

---

## Mark counter (exactly one)

**counter:** Floor only after floating reaches threshold; never free PnL / look-ahead.  
**newer_test:** `test_mark_new_floor_not_above_seen_floating` — **PASS**

---

## Critic

| Check | Status |
|-------|--------|
| Look-ahead | Floor only after path floating ≥ threshold |
| F-011 | trail=False on goal_path wire |
| Risk | Floor reduces loss severity vs −size |
| No-retrain | Inference-only |

---

## Optimist

Thresholds: hits≥12 OR low_hr≥0.18; breach 0; compare 0005/0006.

---

## Judge pretrial order (BEFORE experiment)

1. Run CASE-0007 NEW unit tests.  
2. Code: `progressive_partial_floor` + `partial_lock_frac` in simulate; wire trail=False, frac=0.5.  
3. Measure forward100 seed=42.  
4. PROMOTE only if hits≥12 OR low_hr≥0.18 + breach0 + L2L/senses.  
5. Else REJECT win-path; ADMIT experimental if units + breach0.

---

## Opening + counter test results

Command: `python -m pytest evidence_court/tests/test_case0007_partial_lock.py -v`

| Test | Side | Result |
|------|------|--------|
| `test_creator_new_partial_floor_saves_after_half_goal` | Creator opening | **PASS** |
| `test_mark_new_progressive_partial_floor_pure` | Mark opening | **PASS** |
| `test_creator_new_partial_frac_invalid_no_floor` | Creator counter | **PASS** |
| `test_mark_new_floor_not_above_seen_floating` | Mark counter | **PASS** |

**4/4 NEW tests green.** Regression: case0006 + goal_path case0003 still green.

---

## Code landed

| Symbol | Path | Role |
|--------|------|------|
| `progressive_partial_floor` | `goal_path.py` | Pure frac×lock floor |
| `simulate_fill_m1_path` + `partial_lock_frac` | `goal_path.py` | Floor on stop/EOD |
| wire | `run_goal_path_day` | trail=False, partial_lock_frac=0.5 |

---

## 100d measurement

| Metric | CASE-0005 | CASE-0006 | CASE-0007 | Threshold |
|--------|----------:|----------:|----------:|-----------|
| breach_count | 0 | 0 | **0** | =0 |
| total_hits | 3 | 2 | **3** | ≥12 |
| low_hit_rate | 0.08 | 0.04 | **0.08** | ≥0.18 |
| low_hits | — | 1 | **2** | — |
| low_fire_rate | 0.32 | 0.32 | **0.32** | — |
| promote_ready | false | false | **false** | true |

Artifact: `evidence_court/artifacts/forward100_report.json`  
SHA256: `96BC6EE489C7846A7BF3CAA5C09D211E333E18995A78675F145BE9A351F47A52`

**Interpretation:** Partial floor + BE-off **recovered** CASE-0005 hit metrics from CASE-0006 regression (2→3 hits, 0.04→0.08 low_hr) but **did not improve** beyond 0005. On this seed/window, half-rem_goal threshold rarely changes day outcomes (floating seldom reaches 50% of rem_goal before stop, or days that do already clear/fail similarly). Win-path thresholds still far away.

---

## Judge IRAC

- **Issue:** May partial progressive goal lock (frac=0.5, no full BE) be PROMOTED as the final-boss clear path?  
- **Rule:** A10; F-011; promote thresholds hits≥12 or low_hr≥0.18; breach 0; no retrain; L2L/senses.  
- **Application:** Units 4/4 pass; breach 0; safety OK. Hits=3, low_hr=0.08 — **fails promote thresholds** and **matches** CASE-0005 (no climb). Recovers F-011 damage only.  
- **Conclusion:**  
  - **REJECT** win-path PROMOTE.  
  - **ADMIT experimental only:** partial floor API + trail=False production wire — not MASTER_ARCHITECTURE law.  
  - **Taxonomy:** F-012 — half-rem_goal-only partial floor insufficient for clear climb on this protocol.  
  - **Next CASE-0008:** arm partial floor on **size-R basis** (e.g. bank 1.0×size when floating ≥1.0R) independent of huge rem_goal, **and/or** slot/entry quality that raises mean favorable R — full A10 before code.

---

## FAILURE_TAXONOMY

**F-012** — Partial floor only at 50% rem_goal does not raise hits beyond CASE-0005 baseline on seed=42.
