# CASE-0020 — Measure A20 dual-safe residual on 100d (scoreboard)

**case_id:** CASE-0020  
**status:** CLOSED — dual **REJECT** (F-020)  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-DUAL (on road A16–A20)  
**question:** Does profit-gated + continuation-only residual (A20) improve **joint** clears + A13 vs CASE-0013 ungated residual without breach or pad?

**scope:** measure only — no new thrash dials  
**protected_invariants:** A10–A20; no PROVEN overwrite; seed=42 comparable  

**Baseline CASE-0013:** breach 0 | hits 2 | low_hr 0.04 | a13_frac ~14.5% | mean_tr ~3.1  

---

## ROUND STRUCTURE (measure fire)

A10 openings filed at CASE-0019 for residual law. This fire: **Judge-ordered measurement** only.

### Acceptance (dual ADMIT / PROMOTE path)

| Metric | Keep / improve vs 0013 | Goal long-term |
|--------|------------------------|----------------|
| breach | =0 | =0 |
| hits | ≥2 (prefer ≥3 = 0012) | ≥12 |
| low_hr | ≥0.04 (prefer ≥0.08) | ≥0.18 |
| a13_frac | not collapse to ~0 | →100% MUST |
| promote_ready | if true → FINAL_BOT_SPEC path | true |

---

## Counsel (A15) — measure protocol

Re-measure after dual-safe residual wire before more dials. One seed=42 forward100; no mid-run code change.

---

## Pretrial

1. CASE-0019 units green — **PASS** (4/4)  
2. Price data present — **PASS**  
3. forward100 seed=42 use_goal_path=True — **DONE**  
4. IRAC on scoreboard  

---

## Results (100d seed=42)

| Metric | CASE-0013 | CASE-0020 (A20 path) | Delta |
|--------|----------:|---------------------:|------:|
| breach | 0 | **0** | = |
| hits | 2 | **2** | = |
| low_hr | 0.04 | **0.04** | = |
| mean_tr | ~3.1 | **0.66** | ↓↓ |
| max_tr | 21 | **3** | ↓↓ |
| a13_frac | ~14.5% | **0.0%** | ↓↓ collapse |
| l2l / senses | — | True / True | ok |
| promote_ready | false | **false** | — |

**SHA256:** `f48743a2a5c8283917718939599699dd3fc669c29ea2561c824f93d8edaa708e`  
**Elapsed:** ~1025s  

**Interpretation:** Profit-gated + continuation-only residual **kept conversion flat** (hits/low_hr unchanged) but **starved A13** (day-share 14.5%→0%, mean trades 3.1→0.66). Dual objective **failed** — not a Pareto win. Gate is dual-safe on paper but path-capacity cliff in practice (F-020).

---

## Judge IRAC

- **Issue:** Does A20 day-path residual improve joint clears + A13 vs 0013?  
- **Rule:** Dual win needs breach=0 and Pareto (hits↑ or hold with a13↑ / a13 hold with hits↑); A13 MUST still law; no pad.  
- **Application:** breach 0; hits/low_hr flat; a13_frac **collapsed to 0**; mean_tr collapsed. Conversion not improved; scalping cadence worse.  
- **Conclusion:**  
  1. **REJECT** dual win-path PROMOTE.  
  2. **ADMIT** A20 helpers as unit-pinned dual-safe **API** only — full day-path dual-gate is **not** production dual path.  
  3. **F-020** — profit+cont residual gates starve trade density without lifting hits.  
  4. **Next CASE-0021:** real edge density / fill-R on regime-aware road **without** residual multi thrash **and without** total residual starve — e.g. 1-sym micro residual on profit only (no multi), denser cont/pb real edges, or curriculum-driven fire rate. Prefer road geometry over another thrash dial.  
  5. Code left as measured experimental path (not silent revert mid-fire).
