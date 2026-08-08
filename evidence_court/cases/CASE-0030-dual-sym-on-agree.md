# CASE-0030 — Dual-symbol only when multi-set agrees (A13 density on road)

**case_id:** CASE-0030  
**status:** IN_COURT  
**opened:** 2026-08-07 (immediate after 0029 — no 5m wait)  
**docket_issue_id:** ISSUE-DUAL / ISSUE-A13  
**question:** Does allowing **2 symbols per slot only when multi-set consensus is agree_long/short** raise a13_frac and/or hits vs A27 floor **without** undoing prefer hits≥11 / low_hr≥0.28 / a13≥28% (absolute ≥9/0.24) and without residual thrash cliffs?

**scope:** `production_symbols_per_slot` + day-path n_take wire; tests; forward100 seed=42  
**protected:** A25–A27 clock/hold; empty skip; full-scale legs; no profit-residual multi (F-020); no pad  

**Baseline CASE-0029:** breach 0 | hits 11 | low_hr 0.28 | a13 28% | mean_tr 7.27 | max_pnl 70  

---

## A10 openings (summary)

**Creator:** Multi-symbol concurrent under flea-jar when HTF multi-set agrees is real opportunity book (not pad); can lift days to ≥8 trades.  
**new_test:** `test_creator_new_dual_on_agree_long_short`

**Mark:** Dual only on agree; incomplete/chop/conflict stay 1-sym. Same-side filter on picks.  
**new_test:** `test_mark_new_one_sym_when_incomplete_chop_conflict`

**Counters:** disable dual flag; default incomplete → 1.  
**tests:** `test_creator_new_dual_can_be_disabled`, `test_mark_new_default_still_one_without_agree`

---

## Judge pretrial

1. Units green.  
2. Wire dual on agree only.  
3. forward100 seed=42.  
4. PROMOTE dual if (hits≥12 OR low_hr≥0.28 with hits≥11) AND a13 lift vs 28% without floor break.  
5. Else ADMIT/REJECT with F-tax if regress.

---

## Results / IRAC

_(after measure)_
