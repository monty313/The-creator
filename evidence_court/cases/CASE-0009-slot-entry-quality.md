# CASE-0009 — Slot / entry R quality (A10 full Court)

**case_id:** CASE-0009  
**status:** CLOSED  
**opened:** 2026-08-07 (scheduled Court fire)  
**closed:** 2026-08-07  
**question:** What **measured** change raises hits/low_hr via **slot/entry R quality** (prime session slots, stronger prior-path confirm, pullback-first entry gate) on the same 100d random protocol without breach?

**scope:** `evidence_court/meta_rl/goal_path.py` (entry/slot selection only); tests; forward eval  
**protected_invariants:** MARK_SETS_LAW; Meta-RL 176; no-retrain; breach; A10; A12; F-011/12/13; no live deploy; PROVEN untouched  

**Prior:** Exit-floor family (0006–0008) exhausted at hits=3 / low_hr=0.08.

---

## Creator opening

**Time-of-day / session liquidity:** concentrate entries in London–NY active windows.

**new_test:** `test_creator_new_prime_session_slot_set` — **PASS**

---

## Mark opening

**Pullback-first + stronger session path confirm** (`entry_quality_ok`, `min_align`).

**new_test:** `test_mark_new_entry_quality_pullback_first` — **PASS**

---

## Creator counter

Later pullback any slot (residual multi-leg). **newer_test:** `test_creator_new_later_pullback_any_slot_ok` — **PASS**

---

## Mark counter

Mild min_align still passes lean path. **newer_test:** `test_mark_new_session_confirm_min_align` — **PASS**

---

## Judge pretrial

1. NEW units green  
2. Code: prime slots, entry_quality_ok, min_align=1.5e-4 wire  
3. forward100 seed=42  
4. PROMOTE if hits≥12 OR low_hr≥0.18 + breach0  

---

## Test results

`python -m pytest evidence_court/tests/test_case0009_slot_entry.py -v` → **4/4 PASS**  
Regression goal_path case0003: green.

---

## Code landed

| Symbol | Role |
|--------|------|
| `PRIME_SESSION_SLOTS` / `is_prime_session_slot` | 10/13/16h prime |
| `entry_quality_ok` | pullback any; cont prime+force≥0.40 |
| `session_confirms_side(min_align=)` | wire 1.5e-4 |
| quality +0.25 | prime slot boost |

---

## 100d measurement

| Metric | CASE-0008 | CASE-0009 | Threshold |
|--------|----------:|----------:|-----------|
| breach_count | 0 | **0** | =0 |
| total_hits | 3 | **2** | ≥12 |
| low_hit_rate | 0.08 | **0.04** | ≥0.18 |
| low_fire_rate | 0.32 | **0.28** | — (↓) |
| promote_ready | false | **false** | true |

Artifact SHA256: `17186CBD7FF39349B6DD5A4125D9A715C5CE7F7E7F620239F0E8E152CEF678BD`

**Interpretation:** Another **permission/quality shrink** cut fire slightly and **lowered** hits (3→2). Same failure mode as CASE-0005 confluence: filtering entries does not raise clear rate when the binding problem is insufficient favorable R on the remaining paths, not excess thrash volume alone.

---

## Judge IRAC

- **Issue:** PROMOTE prime-slot + min_align + entry_quality as final-boss clear path?  
- **Rule:** A10; promote thresholds; flea-jar.  
- **Application:** Units 4/4; breach 0; hits **worse** (2 / 0.04).  
- **Conclusion:**  
  - **REJECT** win-path PROMOTE.  
  - **ADMIT experimental only** (unit-proved helpers; production wire left for further case to re-open or strip).  
  - **F-014** — slot/entry quality filters alone reduce fire and can cut hits.  
  - **Next CASE-0010:** stop pure entry-shrink. Measure **pullback single-set carve-out** (raise pullback fire count under A12) **or** **path-to-next-slot multi-leg compounding** so residual goal uses banked size-R — under full A10. Prefer a hypothesis that **increases** achievable day PnL paths, not further gates.

---

## FAILURE_TAXONOMY

**F-014** — Prime-slot / min_align / entry_quality gates alone hurt hits (CASE-0009).
