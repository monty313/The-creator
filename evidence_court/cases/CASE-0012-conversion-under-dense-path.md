# CASE-0012 — Conversion under dense scalping path (A10 full Court)

**case_id:** CASE-0012  
**status:** CLOSED  
**opened:** 2026-08-07 (scheduled Court fire)  
**closed:** 2026-08-07  
**question:** What **measured** conversion control under dense scalping cadence raises hits/low_hr **and** share of days with n_trades∈[8,400] without risk breach or pad fills?

**scope:** `goal_path.py` hold-end by topology + symbols-per-slot; tests; forward eval  
**protected_invariants:** A10; A12; A13 MUST 8–400; A14; F-011…F-017; no pad; breach 0; PROVEN untouched  

---

## Creator opening

Asymmetric hold: pullback runners EOD; continuation next-slot (anti F-017 thrash).

**new_test:** `test_creator_new_pullback_holds_eod` — **PASS**

---

## Mark opening

One best symbol per slot; multi-symbol via later slots only.

**new_test:** `test_mark_new_one_symbol_per_slot` — **PASS**

---

## Creator counter

Last slot EOD both topologies. **newer_test:** `test_creator_new_last_slot_eod_both_topologies` — **PASS**

---

## Mark counter

Per-slot cap only. **newer_test:** `test_mark_new_later_slots_allow_other_symbols` — **PASS**

---

## Judge pretrial

1. NEW units green  
2. Code: `fill_hold_end_time` + `n_symbols_per_slot()==1` wire  
3. forward100 seed=42  
4. Metrics: hits, low_hr, mean trades, a13 day-share, breach  

---

## Test results

`pytest test_case0012_conversion_dense.py` → **4/4 PASS** (+ related regression green)

---

## Code landed

| Symbol | Role |
|--------|------|
| `fill_hold_end_time` | pb→EOD; cont→next slot |
| `n_symbols_per_slot` | returns 1 |
| wire | day path uses both |

---

## 100d measurement

| Metric | CASE-0011 | CASE-0012 | Threshold |
|--------|----------:|----------:|-----------|
| breach | 0 | **0** | =0 |
| total_hits | 0 | **3** | ≥12 |
| low_hit_rate | 0.0 | **0.08** | ≥0.18 |
| low_fire | 0.64 | **0.64** | — |
| mean n_trades | ~3.2 | **~2.4** | — |
| max n_trades | 21 | **15** | — |
| a13 day-share (≥8) | ~15% | **~6.4%** | →100% MUST |
| promote_ready | false | **false** | true |

Artifact SHA256: `c7727f901c63fdb8500e5fc356e9b69135fd5283d430c8df44e77ce9a7c87098`  
Elapsed ~698s

**Interpretation:** Conversion control **recovered clears** from F-017 collapse (hits 0→3, low_hr 0→0.08) back to CASE-0005 scoreboard. **A13 day-share fell** (15%→6%) — one-symbol + EOD pullback reduces ticket count. Dual objective (hits **and** A13 every day) not met.

---

## Judge IRAC

- **Issue:** PROMOTE asymmetric hold + one-symbol as final-boss clear + A13 path?  
- **Rule:** A10; A13 MUST 8–400 every day; hits≥12 or low_hr≥0.18; breach 0.  
- **Application:** Units pass; breach 0; hits improved vs 0011 but still 3≪12; A13 share worsened.  
- **Conclusion:**  
  1. **REJECT** win-path PROMOTE.  
  2. **ADMIT experimental:** `fill_hold_end_time` + single-symbol per slot as **conversion fragment** (measured recovery from F-017).  
  3. **F-018** — conversion recovered hits but cut A13 day-share; dual objective unmet.  
  4. **Next CASE-0013:** **micro-risk residual legs** after pullback bank / under dense clock to raise n_trades toward ≥8/day **without** undoing EOD pullback conversion — full A10.

---

## FAILURE_TAXONOMY

**F-018** — Asymmetric hold + 1-symbol recovers hits, worsens A13 day-share (CASE-0012).
