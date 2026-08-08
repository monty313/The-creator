# CASE-0024 — Measure A22 dense real edges (100d)

**case_id:** CASE-0024  
**status:** CLOSED — A22 **ADMIT measured lift**; dual/final-boss **REJECT**  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-A13 / ISSUE-DUAL on A21+A22 road  
**question:** Does 15m cadence + multi-set cont window raise a13 day-share **without** breaking A21 conversion floor (hits≥3 / low_hr≥0.08)?

**Baseline CASE-0022 (A21):** breach 0 | hits 3 | low_hr 0.08 | a13 7% | mean_tr 2.43  

**Floor:** hits≥3 and low_hr≥0.08 — else REJECT density lever.

---

## Pretrial

1. CASE-0023 units green — **PASS**  
2. Price data present — **PASS**  
3. forward100 seed=42 — **DONE** ~1645s  

---

## Results (100d seed=42)

| Metric | CASE-0022 (A21) | **CASE-0024 (A22)** | Delta |
|--------|----------------:|--------------------:|------:|
| breach | 0 | **0** | = |
| hits | 3 | **7** | ↑↑ |
| low_hr | 0.08 | **0.20** | ↑↑ |
| mean_tr | 2.43 | **3.63** | ↑ |
| max_tr | 15 | **21** | ↑ |
| a13_frac | 7% | **19%** | ↑↑ |
| max_pnl | 55.6 | **70.0** | ↑ |
| promote | false | **false** | — |
| l2l/senses | True | True | ok |

**SHA256:** `4aa8a76bd6caa91ca9e490a9dede1cc3a811e8971a4b6d54d8051d6ac1a59803`  
**Elapsed:** ~1644.8s  

**Interpretation:** A22 **clears conversion floor** and **jointly lifts** hits, low_hr, a13_frac, and mean trades vs A21 — first clean Pareto density win without residual thrash/starve. Still far from final boss (hits 7≪12, a13 19%≪100% MUST days).

---

## Judge IRAC

- **Issue:** A22 density measured dual progress vs A21 floor?  
- **Rule:** Floor hits≥3 / low_hr≥0.08; dual promote needs much higher clears+A13; ROAD no F-017…F-020.  
- **Application:** Floor **held and exceeded** (7 / 0.20); a13 7%→19%; mean_tr↑; breach 0; promote_ready false.  
- **Conclusion:**  
  1. **ADMIT A22 as measured production density path** (strengthen narrow PROMOTE with scoreboard).  
  2. **REJECT** dual/final-boss / FINAL_BOT_SPEC (thresholds unmet).  
  3. Residual multi thrash path remains forbidden (F-019); 15m+multi-set cont is preferred density road.  
  4. **Next CASE-0025:** further real-edge / R / policy path to push a13 toward MUST and hits toward ≥12 **without** undoing 0024 floor (hits≥7 / low_hr≥0.20 preferred; absolute floor hits≥3 / 0.08).
