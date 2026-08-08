# CASE-0025 — Dense NYLON prime band (real cont edges in liquid hours)

**case_id:** CASE-0025  
**status:** CLOSED — units **PASS**; dual/A23 **REJECT (measured null)**; floor **held**  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD / ISSUE-DUAL on A22 floor  
**question:** Does densifying **prime continuation** across the London–NY overlap band (hours 12–16) raise a13 day-share and/or hits **without** undoing CASE-0024 floor (prefer hits≥7 / low_hr≥0.20; absolute ≥3 / 0.08) and without F-017…F-020 residual cliffs?

**scope:** `is_prime_session_slot` / prime-band constants only; keep A21 1-sym full-scale; A22 15m + multi-set cont shoulders; A19 regime; 0012 hold  
**protected_invariants:** empty-slot skip; no pad; no residual multi; no exit-floor dials; PROVEN untouched; no live MT5  

**Baseline CASE-0024 (A22):** breach 0 | hits 7 | low_hr 0.20 | a13 19% | mean_tr 3.63  

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters + newer tests → Counsel → Critic → Optimist → pretrial → units → measure → IRAC

---

## Creator opening

### strongest_internet_argument

Scalping literature and session research put **peak liquidity / cleanest directional moves** in the **London–New York overlap** (often cited ~12:00–16:00 / 13:00–17:00 GMT depending on asset). Evaluating continuation more often **inside that liquid band** expands real opportunity without pad fills or multi-symbol thrash: empty slots still skip; force floors still gate; 1-sym full-scale stays.

Sparse three-point prime (10/13/16) under-samples the same liquid window on a 15m grid — density win class is the same as A22 (more honest scans), not F-017 thrash.

**claim:** Dense prime band hours [12, 16] raises cont session-ok capacity under liquid hours while thin open/late stay non-prime.

**new_test:** `test_creator_new_dense_nylon_prime_band_hours` — **PASS**

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. Mark session law: fire cont in liquid hours; thin open (07) and late fade (19) stay closed for cont without confluence.  
2. Shoulder hours (08–11, 17–18) keep **A22 multi-set + strong force** extended path — not free cont.  
3. Pullback any slot; force floors (A21) still apply inside prime.  
4. No residual multi (F-017/019); no dual residual starve (F-020).

**claim:** Classic named primes remain; mid-overlap slots become prime; 11:00 still multi-set-gated; 19:00 blocked.

**new_test:** `test_mark_new_shoulder_still_multiset_thin_blocked` — **PASS**

---

## Creator counter

**counter:** Force floors + empty skip + 1-sym production still hold under dense prime — denser prime is not pad-to-fire.

**newer_test:** `test_creator_new_dense_prime_still_force_floors_no_pad` — **PASS**

---

## Mark counter

**counter:** A22 15m production grid and CONT_EXTENDED lab pins preserved; non-band extended path unchanged semantics.

**newer_test:** `test_mark_new_a22_production_grid_and_extended_pin` — **PASS**

---

## Counsel opinion (A15)

### internet_sift

- Gold / FX scalping sources consistently rank **London–NY overlap** as highest liquidity and best high-frequency window; Asian/late thin is weaker for dense cont.  
- Multi-timeframe confluence + session filter is standard: denser evaluation in liquid hours ≠ averaging residual legs.  
- A22 already proved density-with-skip lifts dual metrics; next density should be **session geometry**, not residual multi (F-017…F-020).

### policy_recommendation

**Single lever:** expand prime cont session-ok to hour band **[12, 16]** inclusive (plus classic 10/13/16). Keep multi-set extended shoulders (A22), 1-sym full-scale (A21), asymmetric hold (0012), empty skip. Unit-pin; **forward100 seed=42** this fire vs 0024 floor.

### opinion

Creator density-in-liquid-band + Mark shoulder/thin discipline = hybrid road. Counsel preferred this over residual multi or exit-floor dials. **Post-measure:** session densification alone is **redundant** with A22 multi-set extended covering hours 8–18 — null dual signal.

### evidence

NEW tests in `tests/test_case0025_dense_nylon_prime.py` 4/4; regression 0009/0021/0023; forward100 seed=42.

### sources

- Session overlap / XAUUSD liquid hours (industry session guides)  
- ROAD_FOR_THE_POLICY.md — real edges, no pad  
- FAILURE_TAXONOMY F-017…F-020  
- CASE-0024 A22 measured Pareto baseline  

---

## Critic

| Check | Note |
|-------|------|
| F-017 multi thrash | not opening multi residual |
| F-018/020 | full-scale 1-sym kept |
| F-014 pure gate | this **opens** liquid cont capacity, not shrink |
| Bundled confound | single lever: prime band only |
| Dual | measure this fire — **null vs 0024** |

---

## Optimist

If liquid-band cont was the binding under-sample after A22, hits and a13 can joint-lift again without cliffs — same pattern as 15m densification.

**Post-measure:** under-sample was **not** prime-session gaps inside A22 active multi-set band; next need force/hold/R or denser real multi-set floors.

---

## Judge pretrial (BEFORE code)

1. NEW 4 tests + regression `test_case0009`, `0021`, `0023` green after code — **PASS 16/16**  
2. Code **only** prime-band helpers / `is_prime_session_slot` — **done**  
3. **forward100** seed=42 ordered this fire — **DONE** ~1364s  
4. **Floor:** prefer hits≥7 / low_hr≥0.20; absolute REJECT if hits&lt;3 or low_hr&lt;0.08 or breach&gt;0  
5. Success signal: a13_frac ↑ and/or hits ↑ without floor break  

---

## Results (100d seed=42)

| Metric | CASE-0024 (A22) | **CASE-0025** | Delta |
|--------|----------------:|--------------:|------:|
| breach | 0 | **0** | = |
| hits | 7 | **7** | = |
| low_hr | 0.20 | **0.20** | = |
| mean_tr | 3.63 | **3.63** | = |
| max_tr | 21 | **21** | = |
| a13_frac | 19% | **19%** | = |
| max_pnl | 70.0 | **70.0** | = |
| promote | false | **false** | — |
| l2l/senses | True | True | ok |

**SHA256:** `4aa8a76bd6caa91ca9e490a9dede1cc3a811e8971a4b6d54d8051d6ac1a59803` (**byte-identical** to CASE-0024 report)  
**Elapsed:** ~1363.7s  
**Units:** `test_case0025` + 0009/0021/0023 → **16/16 PASS**

**Interpretation:** Dense NYLON prime is **legal** (units) but **measured null** under A22: multi-set extended already allows cont in hours 8–18 when multi-set + force≥0.35; prime band only adds single-set cont ≥0.40 and multi-set [0.32,0.35) in 12–16 — **no extra fills cleared remaining gates**. Floor held. Not a dual climb. **F-021**.

---

## Judge IRAC

- **Issue:** Does dense NYLON prime lift dual metrics vs A22 floor without cliffs?  
- **Rule:** A10+A15; ROAD not residual thrash; floor prefer ≥7/0.20 absolute ≥3/0.08; breach 0; PROMOTE dual lever only if scoreboard moves.  
- **Application:** Units prove geometry (shoulders multi-set, thin blocked, force floors, A22 grid). Measure shows **exact 0024 scoreboard** (SHA match). No regression; no lift. Session densification without force/hold change is **redundant** with A22 extended active band.  
- **Conclusion:**  
  1. **REJECT** Law A23 / dual promote of dense-prime-as-win-lever (**F-021**).  
  2. Floor **held** (hits 7 / low_hr 0.20 / breach 0) — no undo of 0024.  
  3. Code may remain as honest session vocabulary (null under current floors); **not** final-boss / FINAL_BOT_SPEC.  
  4. **Next CASE-0026:** stronger road lever — multi-set **force densification** and/or cont **hold-R** and/or 10m real grid — not another pure session re-label of A22 coverage; keep F-017…F-020 + F-021 out.
