# CASE-0027 — Production 10m decision clock (structural density, empty skip)

**case_id:** CASE-0027  
**status:** CLOSED — **ADMIT A25 narrow density** (a13/mean_tr lift); dual/final-boss **REJECT**; floor **held**  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD / ISSUE-DUAL on A22 floor  
**question:** Does a **10m production decision clock** (empty skip, no pad) raise a13 and/or hits vs A22 **without** undoing floor (prefer hits≥7 / low_hr≥0.20; absolute ≥3 / 0.08) and without F-017…F-022?

**scope:** production default slots only (`PRODUCTION_SCALPING_SLOTS` → 10m); keep 15m pin + 30m lab; A21 1-sym; multi-set cont; no residual multi  
**protected:** empty skip; no pad; PROVEN untouched; no exit-floor dials  

**Baseline:** CASE-0024 hits 7 / low_hr 0.20 / a13 19%; CASE-0026 a13 20% / mean 3.66  

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → pretrial → units → measure → IRAC

---

## Creator opening

### strongest_internet_argument

A22 proved **denser honest evaluation** (30m→15m) joint-lifts dual. Scalping MTF stacks often sample LTF at 5–15m under HTF context; next structural step on the same road is **10m scan grid** with skip-if-no-edge.

**claim:** Production 10m grid has more slots than 15m; capacity ∈ [8,400]; empty skip.

**new_test:** `test_creator_new_production_10m_a13_capacity` — **PASS**

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. denser clock ≠ pad: only fire when edge clears (empty skip).  
2. CASE-0023 **15m grid preserved as named pin**.  
3. CASE-0011 **30m lab** preserved.  
4. Cont multi-set + thin block + 1-sym unchanged.

**new_test:** `test_mark_new_15m_and_30m_pins_preserved` — **PASS**

---

## Creator counter

**newer_test:** `test_creator_new_10m_still_gated_no_pad_1sym` — **PASS**

---

## Mark counter

**newer_test:** `test_mark_new_hold_on_10m_grid_next_slot` — **PASS**

---

## Counsel opinion (A15)

### internet_sift

MTF day-trading stacks use finer LTF sample rates under HTF bias; hierarchical policies evaluate more often when skip is free. Same class as A22 measured win.

### policy_recommendation

Single lever: default production 10m; keep 15m/30m pins; forward100 seed=42.

### opinion

Creator denser clock + Mark pins = A22 road continuation. **Post-measure:** a13/mean_tr lift confirms density class; hits flat + max_pnl ceiling drop → dual incomplete; next hold-R on denser clock.

### evidence

Units 24/24 related; forward100 seed=42.

### sources

MTF LTF sample frequency; ROAD; A22; F-017…F-022

---

## Critic

Cont hold next-slot on 10m is **shorter than 15m** — risk clipping cont R (max_pnl **70→50** observed). Density ok; conversion still stuck.

---

## Optimist

a13 20→27% and mean_tr 3.66→4.94 restart A22-class density progress after F-021/F-022 nulls.

---

## Judge pretrial

1. NEW 4 + regression — **PASS** (24 tests)  
2. Code 10m default + 15m pin — **done**  
3. forward100 seed=42 — **DONE** ~2429s  
4. Floor prefer ≥7/0.20  

---

## Results (100d seed=42)

| Metric | CASE-0026 | **CASE-0027** | Delta |
|--------|----------:|--------------:|------:|
| breach | 0 | **0** | = |
| hits | 7 | **7** | = |
| low_hr | 0.20 | **0.20** | = |
| mean_tr | 3.66 | **4.94** | ↑↑ |
| max_tr | 21 | **26** | ↑ |
| a13_frac | 20% | **27%** | ↑↑ |
| max_pnl | 70.0 | **50.0** | ↓ |
| sum_tr | 366 | **494** | ↑ |
| promote | false | **false** | — |

**SHA256:** `554ccdf4b985c2fd9cf59884f5d024f46b840365c9f98c4e55a2cacccb12dde2`  
**Elapsed:** ~2429s  
**Signals:** pb 1968 / ct 6094 (↑ scans)

**Interpretation:** 10m is **A22-class density win** for a13/mean_tr; **hits flat**; **max_pnl ceiling down** (shorter cont hold). Floor held. Dual not met. Promote A25 narrow density only.

---

## Judge IRAC

- **Issue:** 10m production clock dual/density progress vs floor without cliffs?  
- **Rule:** A10+A15; ROAD; floor ≥7/0.20 preferred; no F-017…F-022; A22 density class may PROMOTE narrow if a13 lifts without floor break.  
- **Application:** Units pin 10m capacity + 15m/30m. Measure: a13 20→**27%**, mean_tr 3.66→**4.94**, hits/low_hr **held**, breach 0; max_pnl 70→50 (cont clip). Not dual/final-boss.  
- **Conclusion:**  
  1. **PROMOTE Law A25 (narrow)** — production default 10m decision clock; empty skip; 15m pin retained.  
  2. **REJECT** dual/final-boss / FINAL_BOT_SPEC.  
  3. **Next CASE-0028:** multi-set cont **hold-R** on 10m grid (restore/improve cont R without undoing a13 lift); avoid residual multi thrash. Floor prefer ≥7/0.20 and a13 ≥27% if possible.
