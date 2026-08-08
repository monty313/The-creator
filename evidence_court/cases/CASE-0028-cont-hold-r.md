# CASE-0028 — Continuation min hold-R on A25 10m grid

**case_id:** CASE-0028  
**status:** CLOSED — **PROMOTE A26 cont min hold-R**; dual/final-boss **REJECT**; floor **held+exceeded**  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD / ISSUE-SIDE-R / ISSUE-DUAL  
**question:** Does a **continuation minimum hold of 30 minutes** (path time, not exit-floor dial) raise hits/R vs A25 **without** undoing floor (prefer hits≥7 / low_hr≥0.20; prefer a13≥27%) and without F-011…F-022 cliffs?

**scope:** `fill_hold_end_time` cont path only; pullback stays EOD; no residual multi; no BE/partial floors  
**protected:** A25 10m production; A21 1-sym; empty skip; PROVEN untouched  

**Baseline CASE-0027 (A25):** breach 0 | hits 7 | low_hr 0.20 | a13 27% | mean_tr 4.94 | max_pnl 50  

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → pretrial → units → measure → IRAC

---

## Creator opening

### strongest_internet_argument

MTF literature: LTF times entry; **HTF context supports holding longer** for better R:R. A25 densified the clock but cont next-slot = 10m clipped path R (max_pnl 70→50). Min cont hold **30m path** restores room without pad or residual multi.

**new_test:** `test_creator_new_cont_min_hold_30m_on_10m_grid` — **PASS**

---

## Mark Here, Esq. — opening

**new_test:** `test_mark_new_pullback_eod_last_slot_eod_preserved` — **PASS**

---

## Creator counter

**newer_test:** `test_creator_new_30m_lab_cont_still_next_slot` — **PASS**

---

## Mark counter

**newer_test:** `test_mark_new_a25_geometry_preserved` — **PASS**

---

## Counsel opinion (A15)

### policy_recommendation

`CONT_HOLD_MIN_MINUTES = 30` for cont fill path; forward100 seed=42.

### opinion

Hold-R is fill-path geometry not F-011 exit floor. **Post-measure:** hits+low_hr+max_pnl lift with a13 held — clean dual-on-road progress.

### evidence

Units 12/12; forward100 seed=42.

---

## Critic

a13 held at 27% (no starve). max_pnl restored. Dual still short of promote_ready.

---

## Optimist

A25 density + A26 hold-R is first joint density+conversion step since A22.

---

## Judge pretrial

1. Units — **PASS**  
2. Code cont hold 30m — **done**  
3. forward100 seed=42 — **DONE** ~2428s  

---

## Results (100d seed=42)

| Metric | CASE-0027 (A25) | **CASE-0028** | Delta |
|--------|----------------:|--------------:|------:|
| breach | 0 | **0** | = |
| hits | 7 | **9** | ↑↑ |
| low_hr | 0.20 | **0.24** | ↑ |
| low_hits | 5 | **6** | ↑ |
| mean_tr | 4.94 | **5.01** | ↑ |
| max_tr | 26 | **26** | = |
| a13_frac | 27% | **27%** | = held |
| max_pnl | 50.0 | **70.0** | ↑↑ restored |
| promote | false | **false** | — |

**SHA256:** `2d919bfe4649bd3dfb63f8d0aee6e8fb328fd437add0dc2a1518fd3876ba5cbf`  
**Elapsed:** ~2427.9s  

**Interpretation:** Cont min 30m hold is **Pareto-friendly**: hits 7→9, low_hr 0.20→0.24, max_pnl 50→70, a13 **held** 27%, breach 0. Not dual final-boss (hits 9≪12, a13 27%≪MUST).

---

## Judge IRAC

- **Issue:** Cont min hold-R dual/R progress vs A25 floor without cliffs?  
- **Rule:** A10+A15; ROAD; floor prefer ≥7/0.20 + a13≥27%; not F-011 exit floors; not residual multi.  
- **Application:** Units pin 30m cont / pb EOD / 30m lab next-slot. Measure: hits↑ low_hr↑ max_pnl restored; a13 held; breach 0; promote_ready false.  
- **Conclusion:**  
  1. **PROMOTE Law A26 (narrow)** — continuation fill path minimum hold 30 minutes; pullback EOD kept.  
  2. **REJECT** dual/final-boss / FINAL_BOT_SPEC.  
  3. **Next CASE-0029:** further dual-on-road (more real edges / a13 toward MUST / hits toward ≥12) under A25+A26 floor (prefer hits≥9 / low_hr≥0.24 / a13≥27%); avoid F-011…F-022.
