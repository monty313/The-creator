# CASE-0029 — Production 5m decision clock (A25 density class under A26 hold)

**case_id:** CASE-0029  
**status:** CLOSED — **PROMOTE A27 5m production clock**; dual/final-boss **REJECT**; floor **held+exceeded**  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD / ISSUE-A13 / ISSUE-DUAL  
**question:** Does a **5m production decision clock** (empty skip, A26 cont hold 30m kept) raise a13 and/or hits vs A25+A26 **without** undoing floor (prefer hits≥9 / low_hr≥0.24 / a13≥27%; absolute ≥7/0.20) and without F-011…F-022?

**scope:** production default slots → 5m; pin 10m (A25) + 15m + 30m; keep A26 hold-R; A21 1-sym  
**protected:** empty skip; no pad; no residual multi; no exit-floor dials; PROVEN untouched  

**Baseline CASE-0028:** breach 0 | hits 9 | low_hr 0.24 | a13 27% | mean_tr 5.01 | max_pnl 70  

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → pretrial → units → measure → IRAC

---

## Creator opening

**new_test:** `test_creator_new_production_5m_a13_capacity` — **PASS**

---

## Mark Here, Esq. — opening

**new_test:** `test_mark_new_10m_15m_30m_pins_and_a26_hold` — **PASS**

---

## Creator counter

**newer_test:** `test_creator_new_5m_still_gated_1sym_no_pad` — **PASS**

---

## Mark counter

**newer_test:** `test_mark_new_cont_hold_30m_on_5m_grid` — **PASS**

---

## Counsel opinion (A15)

### policy_recommendation

Production default 5m; keep pins; A26 hold; forward100 seed=42.

### opinion

**Post-measure:** density class continues under A26 hold — joint hits+a13+mean_tr lift; max_pnl held. Dual incomplete vs MUST/final-boss.

---

## Critic

a13 only +1pp (27→28) despite mean_tr 5→7.3 — more trades on already-firing days more than new a13 days. Still not thrash (hits↑).

---

## Optimist

Hits 9→11 approaching ≥12 band; mean_tr 7.27 near A13 min 8 mean.

---

## Judge pretrial

1. Units — **16/16 PASS**  
2. Code 5m + 10m pin — **done**  
3. forward100 seed=42 — **DONE** ~4748s  

---

## Results (100d seed=42)

| Metric | CASE-0028 | **CASE-0029** | Delta |
|--------|----------:|--------------:|------:|
| breach | 0 | **0** | = |
| hits | 9 | **11** | ↑↑ |
| low_hr | 0.24 | **0.28** | ↑ |
| low_hits | 6 | **7** | ↑ |
| mean_tr | 5.01 | **7.27** | ↑↑ |
| max_tr | 26 | **47** | ↑ |
| a13_frac | 27% | **28%** | ↑ |
| max_pnl | 70.0 | **70.0** | = held |
| sum_tr | 501 | **727** | ↑ |
| promote | false | **false** | — |

**SHA256:** `001b72cae9d1c90353d03fc44b7039e186eceaa9efa5f5e7db931eb9726484e3`  
**Elapsed:** ~4747.6s  
**Signals:** pb 3415 / ct 9809  

**Interpretation:** 5m under A26 is **Pareto dual progress** (hits, low_hr, a13, mean_tr up; max_pnl held; breach 0). Not final-boss (hits 11≪12 promote band, a13 28%≪MUST every day).

---

## Judge IRAC

- **Issue:** 5m production clock dual/density vs A25+A26 floor without cliffs?  
- **Rule:** A10+A15; ROAD density class; floor prefer ≥9/0.24/a13≥27%; A26 hold kept; no residual multi.  
- **Application:** Units pin 5m + pins + A26. Measure: hits 9→**11**, low_hr 0.24→**0.28**, a13 27→**28%**, mean_tr 5.01→**7.27**, max_pnl **70** held, breach 0.  
- **Conclusion:**  
  1. **PROMOTE Law A27 (narrow)** — production default 5m decision clock; 10m/15m/30m pins retained; A26 hold kept.  
  2. **REJECT** dual/final-boss / FINAL_BOT_SPEC.  
  3. **Next CASE-0030:** dual-on-road under floor prefer hits≥11 / low_hr≥0.28 / a13≥28%; push a13 toward MUST and hits ≥12 without F-011…F-022 / residual multi.
