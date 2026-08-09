# CASE-0030 — Multi-set eases same-day session path confirm

**case_id:** CASE-0030  
**status:** CLOSED — units **PASS**; dual **REJECT (near-null)**; floor **held**  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD / ISSUE-A13 / ISSUE-DUAL  
**question:** Does **easing same-day session min_align to 0 when multi-set HTF agrees** raise a13 day-share and/or hits ≥12 **without** undoing floor (prefer hits≥11 / low_hr≥0.28 / a13≥28%; absolute ≥9/0.24) and without F-011…F-022?

**scope:** `session_min_align_for_path` + day-path wire only; keep A27 5m, A26 hold, A21 1-sym  
**protected:** empty skip; no pad; no residual multi; no exit floors; PROVEN untouched  

**Baseline CASE-0029:** breach 0 | hits 11 | low_hr 0.28 | a13 28% | mean_tr 7.27 | max_pnl 70  

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → pretrial → units → measure → IRAC

---

## Creator opening

**new_test:** `test_creator_new_multiset_eases_session_min_align` — **PASS**

---

## Mark Here, Esq. — opening

**new_test:** `test_mark_new_non_multiset_session_floor_kept` — **PASS**

---

## Creator counter

**newer_test:** `test_creator_new_session_confirm_zero_align_still_side_aware` — **PASS**

---

## Mark counter

**newer_test:** `test_mark_new_a27_a26_geometry_preserved` — **PASS**

---

## Counsel opinion (A15)

### policy_recommendation

Multi-set → session min_align 0; else DEFAULT; forward100 seed=42.

### opinion

**Post-measure:** near-null dual — multi-set edges already largely cleared default align; silent-day bottleneck is deeper than this gate.

---

## Critic

Hits/a13 flat; n_zero only 41→39. Not a cliff; not a dual climb.

---

## Optimist

Tiny mean_tr bump proves wire live; need different silent-day lever.

---

## Judge pretrial

1. Units — **12/12 PASS**  
2. Code session_min_align + wire — **done**  
3. forward100 seed=42 — **DONE** ~5557s  

---

## Results (100d seed=42)

| Metric | CASE-0029 | **CASE-0030** | Delta |
|--------|----------:|--------------:|------:|
| breach | 0 | **0** | = |
| hits | 11 | **11** | = |
| low_hr | 0.28 | **0.28** | = |
| mean_tr | 7.27 | **7.38** | +0.11 |
| max_tr | 47 | **47** | = |
| a13_frac | 28% | **28%** | = |
| n_zero | 41 | **39** | −2 |
| n_ge8 | 28 | **28** | = |
| max_pnl | 70.0 | **70.0** | = |
| promote | false | **false** | — |

**SHA256:** `f6fc9b32788d4a85874b704f2fc8017aad794a99d998808f360a870e8fe6bdf4`  
**Elapsed:** ~5557s  

**Interpretation:** Multi-set session-align ease is **legal** and **not a cliff** (floor held) but **near-null dual** (hits/a13 flat). Silent-day / a13 day-share bottleneck is not this gate. **F-023**.

---

## Judge IRAC

- **Issue:** Multi-set session min_align ease dual progress vs 0029 floor?  
- **Rule:** A10+A15; ROAD; floor prefer ≥11/0.28/a13≥28%; no F-011…F-022.  
- **Application:** Units prove multi-set→0 align, non-multi DEFAULT, side sign kept. Measure: hits/low_hr/a13 flat; mean_tr +0.11; n_zero −2; breach 0.  
- **Conclusion:**  
  1. **REJECT** Law A28 / dual promote of multi-set session-align ease (**F-023**).  
  2. Floor **held** — helper may remain (harmless).  
  3. **Next CASE-0031:** silent-day / a13 day-share structural lever under A27+A26 (e.g. first-entry multi-set cont ease, regime skip review, or curriculum) — not another near-null gate re-label; avoid F-011…F-023.
