# CASE-0008 — Size-R progressive floor (A10 full Court)

**case_id:** CASE-0008  
**status:** CLOSED  
**opened:** 2026-08-07 (scheduled Court fire)  
**closed:** 2026-08-07  
**question:** What **measured** change raises hits/low_hr via **size-R-based progressive floor** (bank ~1.0R floating when path reaches +1R, independent of huge rem_goal) on the same 100d random protocol without breach?

**scope:** `evidence_court/meta_rl/goal_path.py` (exit path); tests; forward eval  
**protected_invariants:** MARK_SETS_LAW; Meta-RL 176; no-retrain; breach envelope; A10; A12; F-011; F-012; no live deploy; PROVEN untouched  

**Prior:**
| Case | Lever | hits | low_hr |
|------|-------|-----:|-------:|
| 0005 | multi-set permission | 3 | 0.08 |
| 0006 | full BE | 2 | 0.04 |
| 0007 | 50% rem_goal floor | 3 | 0.08 |

---

## Creator opening

**R-multiple scale-out at +1R** banks fixed risk-units independent of day goal (Van Tharp design class). Fixes F-012 (half rem_goal unreachable). Not full BE (F-011).

**new_test:** `test_creator_new_size_r_floor_banks_1r_on_stop` — **PASS**

---

## Mark opening

**Slingshot 1R bank** — bank first R of expansion path-only; leave runner for goal_lock; pure helper `size_r_partial_floor`.

**new_test:** `test_mark_new_size_r_partial_floor_pure` — **PASS**

---

## Creator counter

Arm_r ≥ 1.0 (not 0.5R noise). **newer_test:** `test_creator_new_size_r_not_armed_below_1r` — **PASS**

---

## Mark counter

Floor ≤ floating seen; capped by lock. **newer_test:** `test_mark_new_size_r_floor_capped_by_floating` — **PASS**

---

## Judge pretrial

1. NEW units green  
2. Code: `size_r_partial_floor` + `size_r_arm_r=1.0` wire; keep partial 0.5 secondary; trail=False  
3. forward100 seed=42  
4. PROMOTE if hits≥12 OR low_hr≥0.18 + breach0  

---

## Test results

Command: `python -m pytest evidence_court/tests/test_case0008_size_r_floor.py -v` → **4/4 PASS**  
Regression case0006/0007: green.

---

## Code landed

| Symbol | Role |
|--------|------|
| `size_r_partial_floor` | Pure size×arm_r − fr floor |
| `simulate_fill_m1_path` + `size_r_arm_r` | Path arm + max with rem_goal floor |
| wire | size_r_arm_r=1.0, partial_lock_frac=0.5, trail=False |

---

## 100d measurement

| Metric | CASE-0007 | CASE-0008 | Threshold |
|--------|----------:|----------:|-----------|
| breach_count | 0 | **0** | =0 |
| total_hits | 3 | **3** | ≥12 |
| low_hit_rate | 0.08 | **0.08** | ≥0.18 |
| low_hits | 2 | **2** | — |
| low_mean_goal_progress | ~0.098 | **~0.108** | — (slight ↑) |
| promote_ready | false | **false** | true |

Artifact SHA256: `37B260179A310EF66ED39E15B4EECA7C1DE225BDDFCC9A83DE0294FDE89B2D40`

**Interpretation:** Size-R floor unit-correct and slightly raises mean low-band progress, but **hits/low_hr unchanged** vs 0005/0007. Exit-floor family (BE, rem_goal frac, size-R) is **exhausted** as sole clear lever on this seed/window — binding constraint is **entry quality / fire selection / achievable path R before stop**, not banking intermediate excursions.

---

## Judge IRAC

- **Issue:** PROMOTE size-R floor as final-boss clear path?  
- **Rule:** A10; F-011/F-012; thresholds hits≥12 or low_hr≥0.18.  
- **Application:** Units 4/4; breach 0; hits=3, low_hr=0.08 — fail promote; no hit climb.  
- **Conclusion:**  
  - **REJECT** win-path PROMOTE.  
  - **ADMIT experimental only** size-R floor API (breach-safe, unit-proved).  
  - **F-013** — size-R floor alone does not raise hit count on this protocol.  
  - **Next CASE-0009:** **slot/entry R quality** (session phase, stronger session_confirm, pullback-slot priority, or multi-leg residual after banked R) under full A10 — stop pure exit-floor dials without entry hypothesis.

---

## FAILURE_TAXONOMY

**F-013** — Size-R progressive floor (1.0R) alone insufficient for hit climb (CASE-0008).
