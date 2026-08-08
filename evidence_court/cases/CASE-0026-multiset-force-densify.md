# CASE-0026 — Multi-set force densification (real confluence, lower floors)

**case_id:** CASE-0026  
**status:** CLOSED — units **PASS**; dual densify **REJECT (near-null)**; floor **held**  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD / ISSUE-DUAL on A22 floor  
**question:** Does **lowering multi-set-agree force floors** (still strictly >0, non-multi unchanged) raise a13 and/or hits **without** undoing CASE-0024 floor (prefer hits≥7 / low_hr≥0.20; absolute ≥3 / 0.08) and without F-017…F-021?

**scope:** `real_edge_force_min` / `first_entry_cont_force_min` / `CONT_EXTENDED_FORCE_MIN` / multi-set cont entry floor only  
**protected:** A21 1-sym full-scale; A22 15m; empty skip; no residual multi; no pad; no exit-floor dials; PROVEN untouched  

**Baseline CASE-0024/0025:** breach 0 | hits 7 | low_hr 0.20 | a13 19% | mean_tr 3.63  

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → pretrial → units → measure → IRAC

---

## Creator opening

### strongest_internet_argument

MTF confluence systems use a **configurable sensitivity threshold**: when more timeframes agree, practitioners allow a lower signal bar because confluence itself is the quality filter — not a single absolute force cut. Denser multi-set floors increase opportunity **only when Mark eyes agree**, unlike pad thrash or multi-symbol residual.

F-021 showed session re-label is null when A22 extended already covers the band; the binding constraint is **force gate height**, not hour labels.

**claim:** Multi-set force floors can be lowered while non-multi floors stay; floors remain >0.05 (no pad).

**new_test:** `test_creator_new_multiset_force_floors_denser_than_a21` — **PASS**

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. Multi-set HTF agree = real permission (MARK_SETS); slightly lower force still a real edge.  
2. Single-set / incomplete HTF keeps **higher** floors (no densify without eyes).  
3. Chop still never fires.  
4. No residual multi; pullback still primary topology.

**claim:** agree < no_agree for pb and cont; first-entry cont multi < non-multi; chop blocked.

**new_test:** `test_mark_new_non_multiset_floors_unchanged_chop_blocked` — **PASS**

---

## Creator counter

**counter:** Extended cont still multi-set-only; empty skip; 1-sym; floors never ≤0.05.

**newer_test:** `test_creator_new_floors_never_pad_extended_still_gated` — **PASS**

---

## Mark counter

**counter:** A22 15m production grid + 1-sym production geometry preserved.

**newer_test:** `test_mark_new_a22_a21_geometry_preserved` — **PASS**

---

## Counsel opinion (A15)

### internet_sift

Confluence-scored systems adjust weak/mild/strong thresholds; multi-TF agree justifies mild sensitivity without abandoning filters. After F-021, force densification was the logical next density lever on the A21/A22 road.

### policy_recommendation

Single family: lower **multi-set-only** force floors. Non-multi floors unchanged. Unit-pin; forward100 seed=42 vs 0024 floor.

### opinion

Creator sensitivity + Mark multi-set-only densify was best dual-on-road candidate among force dials. **Post-measure:** near-null — force slice between old and new floors rarely clears remaining gates (session confirm, regime, policy wait).

### evidence

NEW tests 4/4; regression; forward100 seed=42.

### sources

- MTF confluence threshold / sensitivity literature class  
- ROAD_FOR_THE_POLICY.md  
- F-017…F-021  
- CASE-0024 A22 baseline  

---

## Critic

| Check | Note |
|-------|------|
| Pad | floors > 0.05 — held |
| Non-multi thrash | non-agree floors unchanged |
| F-021 | not session re-label |
| F-017 multi | 1-sym kept |
| Dual | near-null measure |

---

## Optimist

If force height blocked real multi-set edges after A22, a13 and hits can joint-lift like 0022→0024.

**Post-measure:** only +1 a13 day / +0.03 mean_tr; hits flat — under-sample is deeper than multi-set force delta.

---

## Judge pretrial (BEFORE code)

1. NEW 4 + regression 0021/0023/0025 — **16/16 PASS**  
2. Code only multi-set force constants — **done**  
3. forward100 seed=42 — **DONE** ~1713s  
4. Floor prefer ≥7/0.20; absolute ≥3/0.08  

---

## Results (100d seed=42)

| Metric | CASE-0024 (A22) | **CASE-0026** | Delta |
|--------|----------------:|--------------:|------:|
| breach | 0 | **0** | = |
| hits | 7 | **7** | = |
| low_hr | 0.20 | **0.20** | = |
| mean_tr | 3.63 | **3.66** | +0.03 |
| max_tr | 21 | **21** | = |
| a13_frac | 19% | **20%** | +1pp |
| sum_tr | ~363 | **366** | +3 |
| max_pnl | 70.0 | **70.0** | = |
| promote | false | **false** | — |

**SHA256:** `08988733f6411d1b9545e9c4db00d37a07bdb9f2acc6fdbd28cf7f9e672a255e`  
**Elapsed:** ~1713s  
**Units:** 0026+0021/23/25 → **16/16 PASS**

**Interpretation:** Multi-set force densify is **not a cliff** (floor held, tiny a13/mean bump) but **not a dual climb** (hits flat, a13 20% still ≪ MUST). Binding constraints after A22 are not this force slice. **F-022**.

---

## Judge IRAC

- **Issue:** Multi-set force densify dual progress vs A22 floor?  
- **Rule:** A10+A15; ROAD; floor ≥7/0.20 preferred; no F-017…F-021; PROMOTE dual lever only if scoreboard meaningfully moves.  
- **Application:** Units prove multi-set denser, non-multi unchanged, no pad. Measure: hits/low_hr flat; a13 19→20%; mean_tr 3.63→3.66; breach 0. Floor held. Dual unmet.  
- **Conclusion:**  
  1. **REJECT** Law A24 / dual promote of multi-set force densify (**F-022**).  
  2. Floor **held** — keep densify as optional harmless path geometry or leave as experimental; **not** final-boss.  
  3. **Next CASE-0027:** cont **hold-R** (multi-set cont longer horizon) or **10m production clock** with empty skip — structural capacity/R, not another micro force dial. Avoid F-017…F-022.
