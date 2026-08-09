# CASE-0035 — Silent-day unlock via opportunity curriculum (C-002 residual)

**case_id:** CASE-0035  
**status:** CLOSED — units **4/4 PASS**; shadow train **DONE**; dual **REJECT (F-024)**; PROVEN champion **untouched**  
**opened:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD / ISSUE-A13 / ISSUE-DUAL / C-002 residual  
**goal_axes:** G-A13, G-TRAIN, G-CLEAR, G-NO_RETRAIN, G-SIGHT  

**question:** Does **offline denser opportunity miss curriculum** (London/NY multi-set PB/cont teachers) + shadow champion retrain cut **n_zero** / raise **a13** and/or hits ≥12 **without** undoing floor (prefer hits≥11 / low_hr≥0.28 / a13≥28%) and without F-011…F-023?

**scope:** `silent_day_opportunity_curriculum` + `train_silent_day_opportunity_policy` + `run_forward_eval(policy|champion_path)`; **no** live force-pad; **no** PROVEN overwrite until PROMOTE; keep A27 5m + A26 hold  

**protected:** empty skip; no residual multi thrash; no exit floors; no F-023 re-label of session-align  

**Baseline CASE-0030 / 0029 floor:** breach 0 | hits 11 | low_hr 0.28 | a13 28% | mean_tr 7.38 | n_zero 39 | max_pnl 70  

**Evidence why this lever (not force gates):** forward100 zero-trade days often show **high n_pullback / n_continuation** with `act=wait` — sensors fire, **brain waits**. Hard floors / session-align (F-023) are near-null under `brain_drives=True`. Road = train the map on miss teachers (C-002 residual).

---

## ROUND STRUCTURE (A10 + A15)

```
Creator opening + NEW test → Mark opening + NEW test
→ one counter each → Counsel (internet best policy)
→ Critic → Optimist → Judge pretrial → experiment → measure → IRAC
```

---

## Creator opening

### strongest_internet_argument

Offline RL fails when datasets only log **taken** actions — missed opportunity states starve the policy of fire coverage (counterfactual / unlabeled offline RL class). Hierarchical goal-conditioned methods (HIQL / offline GCRL) use subgoal structure: high-level “this is a fire opportunity” is a trainable label separate from low-level size. London/NY misses dominate long-term expectancy; densifying those teachers is the correct density lever when sensors already print PB/cont.

**claim:** Synthetic denser London/NY multi-set PB/cont miss curriculum → offline train → more fires on opportunity days without live pad.

**new_test:** `test_creator_new_silent_day_curriculum_london_ny_fire_teachers`

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. Mark eyes: only **pullback_resume / continuation** with multi-set HTF agree are legal teachers.  
2. Chop/collapse never become fire teachers (anti-pad).  
3. London/NY weight > other (session truth).  
4. Both long and short teachers (side from force).  

**claim:** Curriculum topology set ⊆ {PB, cont}; multi_set_agree True; both sides present.

**new_test:** `test_mark_new_curriculum_only_pb_cont_no_chop_teacher`

---

## Creator counter (exactly one)

**counter:** After train, prove/inference must freeze — no retrain when target/risk changes (A14).  
**newer_test:** `test_creator_new_opp_train_freezes_no_retrain_at_prove`

---

## Mark counter (exactly one)

**counter:** A27 5m clock, A26 cont hold 30m, dual-on-agree, empty skip must remain (geometry not thrash).  
**newer_test:** `test_mark_new_a27_a26_geometry_preserved`

---

## Counsel opinion (A15)

### internet_sift

1. **Counterfactual / offline RL** — limited data forces counterfactual reasoning; labeling missed good actions expands coverage without online thrash (NeurIPS offline counterfactual class).  
2. **Offline goal-conditioned hierarchical RL (HIQL)** — high-level subgoal (“reach fire state”) + low-level act; opportunity labels are high-level fire subgoals.  
3. **CQL / BAIR conservatism** — do not invent live OOD force-fire; **complain + offline train** (matches A28).  
4. **Yu et al. unlabeled offline** — reward/label functions over passive logs.

### policy_recommendation

1. Keep production path `brain_drives=True` + Watch observe-only.  
2. Build denser offline miss curriculum (London/NY PB/cont multi-set).  
3. Train **shadow** champion; measure dual vs floor **without** overwriting PROVEN.  
4. PROMOTE champion replace only if dual improves without floor break / F-cliffs.  
5. Reject another hard gate densify (F-023 class).

### opinion

Creator curriculum + Mark Mark-only teachers + Counsel offline-not-live is the best policy class for silent days where sensors already see PB/CT.

### evidence

- Zero-day report sample: pb/ct >0 with wait  
- C-001/C-002 prior PROMOTE narrow  
- NEW unit tests this case  

### sources

- Liu et al., Budgeting Counterfactual for Offline RL (NeurIPS 2023)  
- Park et al., Offline Goal-Conditioned RL / HIQL (NeurIPS 2023)  
- BAIR CQL offline conservatism  
- ROAD_FOR_THE_POLICY.md · A14 · A28 · A29  

---

## Critic

- Synthetic labels ≠ full real-bar M1 harvest (still residual after this case).  
- Opportunity mix can over-fire → dual regression risk — measure required.  
- n_steps for shadow train must be serious enough (not 40-step vanity).  

---

## Optimist

- Directly targets measured wait-on-opportunity bottleneck.  
- Road not cliff: offline only; PROVEN untouched until PROMOTE.  
- Aligns C-002 residual + ISSUE-ROAD + A13.  

---

## Judge pretrial

1. Units CASE-0035 — **4/4 PASS**  
2. Code: curriculum + shadow train + forward_eval policy inject — **done**  
3. Shadow train n_steps=2500 + 64 labels → `artifacts/meta_policy_case0035_opp.npz` (fp `42:meta3689:…`) — **done** (PROVEN default champion **not** overwritten)  
4. forward100 seed=42 with shadow policy — **RE-LAUNCHED 2026-08-08** → `artifacts/forward100_report_case0035.json`  
   (Prior session left status RUNNING; `forward100_report.json` was still baseline champion meta2862, not shadow meta3689.)  
5. PROMOTE shadow→champion only if dual improves without floor break; else REJECT + F-tax if regress  

---

## Experiment results

| Metric | Baseline (meta2862) | Shadow opp (meta3689) | Δ |
|--------|--------------------:|----------------------:|---|
| hits | 11 | **11** | 0 |
| low_hr | 0.28 | **0.24** | −0.04 (prefer broken; absolute 0.24 held) |
| a13_frac | 0.28 | **0.38** | +0.10 |
| n_zero | 39 | **45** | **+6 worse** |
| mean_tr | 7.38 | **21.15** | +13.77 (denser on active days) |
| n_ge8 (8–400) | 28 | **38** | +10 |
| max_pnl | 70 | 70 | 0 |
| breach | 0 | 0 | held |
| promote_ready | false | false | — |

| Check | Result |
|-------|--------|
| Units 4/4 | **PASS** |
| Shadow train | **DONE** steps≈3689 · fp `42:meta3689:inf0:1b9503d1a537319d` |
| forward100 seed=42 shadow | **DONE** · SHA256 `099268c312335728c0ca53a99998cb3e46f4d91ba70ea367e7a55423c1f80bd4` |
| Trade buckets | 0: **45** · 1–7: 17 · 8–400: **38** · >400: 0 |
| PROVEN champion | **untouched** |

**Interpretation:** Synthetic denser London/NY miss teachers **densify active days** (mean_tr↑, a13_frac↑) but **do not unlock silent days** — n_zero **rose**. Prefer floor low_hr broken; hits flat. Dual climb failed; not a thrash cliff.

---

## Judge IRAC

### Issue
Does offline denser opportunity-miss curriculum + shadow retrain cut **n_zero** / raise **a13** and/or hits ≥12 without undoing prefer floor hits≥11 / low_hr≥0.28 / a13≥28%?

### Rule
A10+A15 · A14 offline train / no inference retrain · A28 Watch complain-not-force · ROAD (no pad) · floor prefer ≥11/0.28/a13≥28% · absolute ≥9/0.24 · no F-011…F-023 cliffs · PROVEN not overwritten without dual improve.

### Application
- **Creator / Mark / Counsel:** Units 4/4 prove curriculum topology (PB/cont London/NY multi-set), freeze at prove, A27/A26 geometry preserved. Offline path is the correct class (Counsel CQL: no live OOD force).  
- **Measure seed=42 100d shadow:** hits **11** flat; a13 **28%→38%**; mean_tr **7.38→21.15**; **n_zero 39→45 (wrong way)**; low_hr **0.28→0.24** (prefer break, absolute edge); breach 0; max_pnl 70.  
- Primary silent-day claim **fails**. A13 share rose only because remaining non-zero days got denser, not because silent days unlocked.  
- Prefer floor broken → **do not** replace PROVEN champion.

### Conclusion
1. **REJECT** shadow → champion replace.  
2. **F-024** — synthetic denser opportunity-miss curriculum alone densifies active days, raises n_zero, cuts low_hr prefer.  
3. **Keep** curriculum + `train_silent_day_opportunity_policy` + `champion_path` inject as **lab tools** (units stay green); not production champion.  
4. **C-002 residual** remains: **real-bar M1 harvest** of Watch labels (not synthetic-only) + measure again.  
5. **Next rank-1:** **C-003** A13 lived every day (London/NY no excuse) under structural levers — or C-002 real-bar harvest before another synthetic mix.  
6. PROVEN `meta_policy_champion.npz` **untouched**.
