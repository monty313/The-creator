# CASE-0013 — Micro-risk residual legs under dense path (A10 full Court)

**case_id:** CASE-0013  
**status:** CLOSED  
**opened:** 2026-08-07 (scheduled Court fire)  
**closed:** 2026-08-07  
**question:** What **measured** micro-risk residual-leg policy under dense cadence raises **a13 day-share** without undoing CASE-0012 conversion (hits≥3 / low_hr≥0.08)?

---

## Creator opening

Micro residual / fractional add-on after core risk unit.

**new_test:** `test_creator_new_residual_size_scale` — **PASS**

---

## Mark opening

Multi-symbol only when residual/micro; anchor 1-symbol full.

**new_test:** `test_mark_new_residual_multi_symbol_when_micro` — **PASS**

---

## Creator counter

micro_scale ∈ (0,1). **newer_test:** `test_creator_new_micro_scale_strictly_below_one` — **PASS**

---

## Mark counter

Anchor 1-sym full scale. **newer_test:** `test_mark_new_anchor_one_symbol_full_scale` — **PASS**

---

## Judge pretrial

1. NEW units green  
2. Code: residual_size_scale + symbols_per_slot_for_leg; keep fill_hold_end_time  
3. forward100 seed=42  

---

## Test results

**4/4 NEW PASS** + case0012 regression green.

---

## Code landed

| Symbol | Role |
|--------|------|
| `residual_size_scale` | 1.0 then 0.25 after anchor |
| `symbols_per_slot_for_leg` | 1 then 3 after anchor |
| wire | size *= scale; n_take from helper |

---

## 100d measurement

| Metric | CASE-0012 | CASE-0013 | Goal |
|--------|----------:|----------:|------|
| breach | 0 | **0** | =0 |
| hits | 3 | **2** | ≥12 / keep ≥3 |
| low_hr | 0.08 | **0.04** | ≥0.18 / keep ≥0.08 |
| mean_tr | ~2.4 | **~3.1** | ↑ |
| max_tr | 15 | **21** | — |
| a13_frac | ~6% | **~14.5%** | →100% MUST |
| promote | false | **false** | true |

SHA256: `abd9b76d449a031230fc413fa10dd6e28a7a4e0a3d3f3e689fb1fb7dbb7b0a7a`  
Elapsed ~979s

**Interpretation:** Micro residual **raised A13 day-share** (6%→14.5%) and mean trades, but **undid conversion** (hits 3→2, low_hr 0.08→0.04). Dual objective still failed — residual multi-sym micro still leaks expectancy after anchor.

---

## Judge IRAC

- **Issue:** PROMOTE micro residual as dual A13+clear path?  
- **Rule:** A10; A13 MUST; keep hits≥3 baseline; promote clears need ≥12/0.18.  
- **Application:** Units pass; breach 0; a13_frac↑; hits/low_hr **regressed** vs 0012.  
- **Conclusion:**  
  1. **REJECT** dual win-path PROMOTE.  
  2. **ADMIT experimental** residual helpers as **A13 progress fragment** only.  
  3. **F-019** — micro residual after any fill raises a13_frac but cuts hits.  
  4. **Next CASE-0014:** residual only when **realized_pnl > 0** (profit-gated micro) and/or residual **continuation-only** (never micro multi on pullback EOD path) — protect conversion while climbing A13.

---

## FAILURE_TAXONOMY

**F-019** — Unconditional micro residual after anchor: a13↑ hits↓ (CASE-0013).
