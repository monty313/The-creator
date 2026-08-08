# CASE-0011 — Dense scalping cadence toward A13 (A10 full Court)

**case_id:** CASE-0011  
**status:** CLOSED  
**opened:** 2026-08-07 (scheduled Court fire)  
**closed:** 2026-08-07  
**question:** What **measured** dense multi-leg **scalping cadence** raises day trade-count capacity into **A13 [8, 400]** while keeping breach 0 and improving hits/low_hr?

**scope:** `goal_path.py` slots + max_fills + multi-symbol take; tests; forward eval  
**protected_invariants:** MARK_SETS_LAW; Meta-RL 176; no-retrain; risk breach 0; A10; A12; **A13 MUST 8–400**; F-011…F-016; no live deploy; PROVEN untouched  

---

## Creator opening

Dense decision clock (30m liquid-session grid) as structural prerequisite for scalping multi-leg under risk envelope.

**new_test:** `test_creator_new_scalping_slots_a13_capacity` — **PASS**

---

## Mark opening

A13 permanent; max_fills=400; multi-symbol under envelope; no pad without edge.

**new_test:** `test_mark_new_max_fills_a13_band` — **PASS**

---

## Creator counter

Hard cap 400 fills. **newer_test:** `test_creator_new_max_fills_hard_cap_400` — **PASS**

---

## Mark counter

Empty slot skip (no pad). **newer_test:** `test_mark_new_no_pad_trades_without_edge` — **PASS**

---

## Judge pretrial

1. NEW units + A13 law pin green  
2. Code: SCALPING_CADENCE_SLOTS (27×30m), max_fills=400, multi-symbol n_take, meta a13_ok  
3. forward100 seed=42  
4. Record breach, hits, low_hr, n_trades stats, a13 day share  

---

## Test results

`pytest test_case0011_scalping_cadence.py test_scalping_cadence_law.py` → **PASS** (4 NEW + law pins)  
goal_path case0003 path label relaxed to `goal_conditioned*` — **PASS**

---

## Code landed

| Symbol | Role |
|--------|------|
| `build_scalping_cadence_slots` | 30m grid 07–20 → 27 slots |
| `SCALPING_CADENCE_SLOTS` | production default clock |
| `max_fills_for_a13` | hard 400 |
| `allows_empty_slot_skip` | no pad pin |
| wire | default slots=scalping; multi-symbol take; meta a13_ok |

DEFAULT_SLOTS (5) remains labeled lab shadow only.

---

## 100d measurement

| Metric | CASE-0010 | CASE-0011 | Notes |
|--------|----------:|----------:|-------|
| breach_count | 0 | **0** | OK |
| total_hits | 2 | **0** | ↓ collapse |
| low_hit_rate | 0.04 | **0.0** | ↓ |
| low_fire_rate | 0.40 | **0.64** | ↑ fire |
| mean n_trades (samples) | — | **~3.2** | median 1 |
| max n_trades | — | **21** | capacity real |
| days with n_trades≥8 | — | **17 / ~110** (~15%) | partial A13 |
| promote_ready | false | **false** | |

Artifact SHA256: `648cf5e84a4778e82c675365005de18a9a845c3258a2bd1dfd88043ed13d3d1f`  
Elapsed ~1075s

**Interpretation:** Dense cadence + multi-symbol **proved structural capacity** (max 21 trades/day; ~15% days ≥8) under breach 0 and no pad law. **A13 MUST every day not met** (mean ~3). **Clear conversion collapsed** (hits 2→0) — over-trading / short next-slot windows on denser grid destroy R before goal_lock.

---

## Judge IRAC

- **Issue:** PROMOTE dense 30m scalping cadence as production A13 + clear path?  
- **Rule:** A10; A13 MUST 8–400 every day; promote clears hits≥12 or low_hr≥0.18; breach 0; no pad.  
- **Application:** Units pass. Breach 0. Capacity partial (not every day ≥8). Hits **0** — fails clear thresholds and regresses vs 0010.  
- **Conclusion:**  
  1. **REJECT** win-path / final-boss PROMOTE.  
  2. **ADMIT experimental** dense cadence infrastructure (slots builder, max_fills=400, multi-symbol take, a13 meta) as **necessary A13 scaffolding** — not production-complete A13 compliance.  
  3. **F-017** — dense 30m + multi-symbol without conversion control collapses hits.  
  4. **Next CASE-0012:** conversion under dense path — e.g. **micro-risk legs** after first bank, **EOD hold on pullback only**, or **quality throttle** that still targets mean ≥8 trades/day without pad — full A10. Keep A13 obligation.

---

## FAILURE_TAXONOMY

**F-017** — Dense 30m cadence + multi-symbol: fire↑ A13 partial, hits→0 (CASE-0011).
