# CASE-0023 — Denser real 1-sym edges (15m cadence + multi-set cont window)

**case_id:** CASE-0023  
**status:** PROMOTED (narrow density geometry; dual scoreboard deferred)  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD / ISSUE-A13  
**question:** What **measured** change raises A13 path capacity via **real** decision density **without** undoing A21 conversion rails and without F-017…F-020 residual cliffs?

**scope:** production cadence 15m + continuation session window; keep A21 1-sym full-scale  
**protected_invariants:** empty-slot skip; 1-sym; no pad; A19 regime; 0012 hold; 0011 30m lab pin  

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → units → IRAC

---

## Creator opening

**Internet:** Higher decision frequency with **skip-if-no-edge** increases opportunity set without pad fills (scalping microstructure / hierarchical policies sample more often). 15m vs 30m doubles scan opportunities; capacity stays ≤400.

**new_test:** `test_creator_new_production_15m_a13_capacity`

---

## Mark opening

**Knowledge:** Continuation thrash outside liquid hours is bad; multi-set HTF agree + strong force can open **active band** (08–18) non-prime cont. Late thin (19:00) stays closed. Pullback any slot.

**new_test:** `test_mark_new_multiset_cont_opens_active_band_not_thin`

---

## Creator counter

entry_quality honors extended cont; empty skip; 1-sym production.

**newer_test:** `test_creator_new_entry_quality_extended_cont_and_no_pad`

---

## Mark counter

CASE-0011 30m `SCALPING_CADENCE_SLOTS` pin preserved.

**newer_test:** `test_mark_new_lab_30m_pin_preserved`

---

## Counsel (A15)

**Sift:** Frequency of honest evaluation ≠ thrash; residual multi already failed dual. Best policy: denser clock + confluence-gated cont expansion + keep conversion geometry (A21).

**Recommend:** Wire production default to 15m; `continuation_session_ok`; unit-pin; **forward100 next (CASE-0024)** vs A21 baseline (hits≥3, low_hr≥0.08 floor).

---

## Judge pretrial

1. NEW 4 + 0009/0011/0012/0021 regression  
2. Code only cadence + cont session helpers + day default slots  
3. No residual multi; no forward100 this fire  
4. PROMOTE narrow if green  

---

## Results

`pytest test_case0023 + 0009 + 0011 + 0012 + 0021` → **20/20 PASS**

---

## Judge IRAC

- **Issue:** Denser real edges for A13 without residual cliffs / conversion loss?  
- **Rule:** A10+A15; A13 MUST capacity; ROAD; keep A21 rails; no pad.  
- **Application:** 15m production grid capacity legal; multi-set cont window unit-pinned; lab 30m pin intact; empty skip.  
- **Conclusion:**  
  1. **PROMOTE Law A22 (narrow)** — Production 15m cadence + multi-set active-band continuation window.  
  2. Dual measure → **CASE-0024** forward100 seed=42 (must keep hits≥3 / low_hr≥0.08).  
  3. Not final-boss alone.
