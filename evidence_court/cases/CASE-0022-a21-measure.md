# CASE-0022 — Measure A21 one-sym full-scale + multi-set floors (100d)

**case_id:** CASE-0022  
**status:** CLOSED — A21 path **ADMIT baseline**; dual **REJECT** (not promote_ready)  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-DUAL / ISSUE-ROAD  
**question:** Does A21 production path improve dual metrics vs 0012/0013/0020 without breach or pad?

---

## Pretrial

1. CASE-0021 units green — **PASS**  
2. Price data present — **PASS**  
3. forward100 seed=42 — **DONE** ~922s  

---

## Results (100d seed=42)

| Metric | 0012 | 0013 | 0020 | **0022 A21** |
|--------|-----:|-----:|-----:|-------------:|
| breach | 0 | 0 | 0 | **0** |
| hits | 3 | 2 | 2 | **3** |
| low_hr | 0.08 | 0.04 | 0.04 | **0.08** |
| mean_tr | ~2.4 | ~3.1 | 0.66 | **2.43** |
| max_tr | 15 | 21 | 3 | **15** |
| a13_frac | ~6% | ~14.5% | 0% | **7.0%** |
| max_pnl | — | — | — | **55.6** |
| promote | false | false | false | **false** |
| l2l/senses | — | — | — | True/True |

**SHA256:** `e1b830dd9205ef8456a4145b3c94a5b8f56bbcd613f55b778886c51c8165c91b`  
**Elapsed:** ~921.5s  

**Interpretation:** A21 **restored CASE-0012 conversion** (hits 3, low_hr 0.08) and escaped F-020 starve. a13_frac ~7% ≈ 0012 (slightly up), far below A13 MUST and below 0013 residual thrash density. Clear win vs 0020. **Not** dual/final-boss.

---

## Judge IRAC

- **Issue:** Is A21 dual-ready production path?  
- **Rule:** breach 0; dual needs joint clears+A13; promote_ready thresholds unmet if hits≪12 / a13≪1.0.  
- **Application:** breach 0; conversion restored to best measured (0012 class); a13 ~7% only; promote false.  
- **Conclusion:**  
  1. **ADMIT A21** as **production road baseline** (geometry + multi-set floors measured).  
  2. **REJECT** dual / promote_ready / FINAL_BOT_SPEC.  
  3. Residual multi thrash (0013) still only a13 lever that worked and it cut hits — do not rebuild F-019.  
  4. **Next CASE-0023:** denser **real** edge opportunities (A13 path) **without** multi residual thrash — e.g. more quality slots when multi-set agrees, policy-driven fire rate under A18/A19, or second 1-sym leg only on profit with full EOD pullback hold — measure carefully.
