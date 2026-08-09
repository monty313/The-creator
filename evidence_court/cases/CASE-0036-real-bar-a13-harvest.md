# CASE-0036 — Real-bar Watch harvest for A13 every-day density (C-003)

**case_id:** CASE-0036  
**status:** CLOSED — units **4/4 PASS**; harvest **DONE**; dual **REJECT (F-025)**; PROVEN **untouched**  
**opened:** 2026-08-08  
**docket_issue_id:** C-003 / C-002 residual  
**goal_axes:** G-A13, G-TRAIN, G-CLEAR, G-NO_RETRAIN, G-SIGHT  

**question:** Does **real-bar** multi-day harvest of Watch `curriculum_labels` (missed Mark PB/cont on live M1 path) + offline shadow meta-train raise **a13_frac** and/or cut **n_zero** vs floor **without** undoing prefer hits≥11 / low_hr≥0.28 / a13≥28% and without F-011…F-024?

**scope:** `real_bar_harvest` + `filter_real_bar_a13_labels` + `train_real_bar_a13_policy` + `run_forward_eval(champion_path=shadow)`; **no** live force-pad; **no** PROVEN overwrite until PROMOTE; keep A27 5m + A26 hold + empty skip  

**protected:** empty skip; no residual multi thrash; no exit floors; no synthetic-only densify as sole lever (F-024); no session-align re-label (F-023)

**Baseline floor:** breach 0 | hits 11 | low_hr 0.28 | a13 28% | mean_tr 7.38 | n_zero 39 | max_pnl 70  

**Evidence why this lever:**  
- Zero-trade days often show high `n_pullback`/`n_continuation` with brain wait.  
- CASE-0035 synthetic densify → F-024 (active-day densify, n_zero worse).  
- C-002 API exists; residual is **real** path-dated misses, not invented teachers.  
- Road: train the map on actual miss distribution under London/NY priority.

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

Offline RL fails when coverage of **good actions at states the agent actually visits** is thin. Counterfactual / unlabeled offline methods expand coverage from passive logs — but the labels must come from the **behavior distribution** (real trajectories), not invented state proxies. EarnHFT / hierarchical HFT literature densifies high-frequency decisions via teacher signals grounded in real market steps. F-024 already showed pure synthetic PB/cont densify does not unlock silent days.

**claim:** Real-bar Watch miss harvest (dated asof, real force/topo/session) → offline train → higher a13 day-share / lower n_zero without live pad.

**new_test:** `test_creator_new_filter_keeps_dated_pb_cont_only`

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. Teachers ⊆ {pullback_resume, continuation} only.  
2. Undated / synthetic-only rows must not smuggle in as “real-bar.”  
3. London/NY weight > other (session truth).  
4. Chop never becomes a fire teacher.  
5. Harvest observes path; empty skip remains — no pad fills.

**claim:** Filter enforces Mark topology + dated provenance + London/NY weight order.

**new_test:** `test_mark_new_london_ny_weight_preserved_and_no_chop`

---

## Creator counter (exactly one)

**counter:** After real-bar mix train, prove/inference must freeze across target/risk (A14).  
**newer_test:** `test_creator_new_real_bar_train_freezes_no_retrain`

---

## Mark counter (exactly one)

**counter:** A13 band helpers + empty skip must remain; harvest must not invent pad trades.  
**newer_test:** `test_mark_new_empty_skip_and_a13_band_geometry_preserved`

---

## Counsel opinion (A15)

### internet_sift

1. **Offline RL coverage** — improve on logged states; pessimistic methods warn against OOD force actions (CQL / MAHALO class).  
2. **Counterfactual labels on passive logs** — miss→teacher only when opportunity truly present in log (matches A28).  
3. **EarnHFT hierarchical density** — high-frequency capacity needs real market-step teachers, not day-level abstraction alone.  
4. **F-024 Court self-evidence** — synthetic densify failed silent-day unlock; switch provenance class.

### policy_recommendation

1. Harvest Watch labels from real `run_goal_path_day` multi-day window.  
2. Filter PB/cont + dated only; London/NY weighted.  
3. Train **shadow** offline; dual measure vs floor.  
4. PROMOTE champion replace only if dual improves without floor prefer break.  
5. Reject live force-fire and re-running synthetic-only densify.

### opinion

Creator real-bar provenance + Mark topology gate + Counsel offline-not-live is the correct next lever after F-024.

### evidence

- Zero-day sensor≠fire pattern (forward100 baseline)  
- F-024  
- C-001/C-002 narrow PROMOTEs  
- NEW units this case  

### sources

- Offline RL coverage / CQL pessimism literature  
- EarnHFT hierarchical HFT (AAAI/arXiv)  
- ROAD_FOR_THE_POLICY.md · A13 · A14 · A28 · A29 · F-024  

---

## Critic

- Harvest window may under-cover rare regimes vs full 100d.  
- `opportunity_label_to_training_example` still builds state proxies from label fields (not full packed path state) — stronger than pure synthetic times, weaker than full state dump.  
- Dual risk: over-fire → low_hr regression (F-024 pattern).

---

## Optimist

- Closes C-002 residual class F-024 named.  
- Serves C-003 A13 without pad.  
- PROVEN safe until measure.

---

## Judge pretrial

1. Units CASE-0036 — **4/4 PASS**  
2. Harvest n_days=30 → `artifacts/real_bar_opp_labels_case0036.json` — **DONE**  
   - raw 805 · filtered 300 · London/NY 237 · zero-trade harvest days 15/30  
   - window 2026-04-15…2026-05-26 · real force/topo/asof  
3. Shadow train → `meta_policy_case0036_realbar.npz` fp `42:meta4050:…` — **DONE** (PROVEN untouched)  
4. forward100 seed=42 shadow — **RUNNING** → `forward100_report_case0036.json`  
5. PROMOTE only if dual improves without floor prefer break  

---

## Experiment results

| Metric | Baseline floor | Shadow real-bar meta4050 | Δ | F-024 synthetic (ref) |
|--------|---------------:|-------------------------:|---|----------------------:|
| hits | 11 | **11** | 0 | 11 |
| low_hr | 0.28 | **0.24** | −0.04 prefer break | 0.24 |
| a13_frac | 0.28 | **0.38** | +0.10 | 0.38 |
| n_zero | 39 | **45** | **+6 worse** | 45 |
| mean_tr | 7.38 | **21.23** | +13.85 | 21.15 |
| max_pnl | 70 | 70 | 0 | 70 |
| breach | 0 | 0 | held | 0 |

| Check | Result |
|-------|--------|
| Units 4/4 | **PASS** |
| Harvest | **DONE** 300 labels (237 LN) · raw 805 · window Apr15–May26 |
| Shadow train | **DONE** steps=4050 · fp `42:meta4050:inf0:6d6ce7c566f61497` |
| forward100 shadow | **DONE** SHA256 `efc88555fdaedadf53ee49a2a048d03bd74bdcbdddce359959dd8ad6973b2020` |
| PROVEN champion | **untouched** |

**Interpretation:** Real-dated Watch labels ≈ F-024 dual. Active-day densify only; silent days worse. Provenance upgrade alone fails while train path still rebuilds **synthetic** official state from label fields.

---

## Judge IRAC

### Issue
Does real-bar multi-day Watch miss harvest + offline shadow train raise a13 / cut n_zero without undoing prefer floor?

### Rule
A10+A15 · A13 must · A14 offline train / freeze at prove · A28 complain-not-force · ROAD · floor prefer ≥11/0.28/a13≥28% · absolute ≥9/0.24 · no F-011…F-024 cliffs · PROVEN safe until dual improve.

### Application
- **Creator / Mark / Counsel:** Units prove dated PB/cont filter, London/NY weight, freeze, empty-skip. Harvest produced 300 real-dated labels (237 LN). Offline class correct.  
- **Measure seed=42 100d:** hits **11**; a13 **38%**; mean_tr **21.23**; n_zero **45**; low_hr **0.24**; breach 0 — **statistically same class as F-024**.  
- Root cause: labels are real, but `opportunity_label_to_training_example` still synthesizes official state → map does not learn silent-day **visited** states.

### Conclusion
1. **REJECT** shadow → champion replace.  
2. **F-025** — real-bar labels + synthetic state rebuild densifies active days like F-024.  
3. **Keep** harvest/filter/train tooling as lab (units green).  
4. **Next C-003 levers (binding residual):**  
   - **(state, teacher)** pairs dumped from actual path `build_meta_rl_state` at miss slots, **or**  
   - structural partial-day densify (1–7 → 8+) without pad, **or**  
   - game-train human traj (A34) into offline updates.  
5. PROVEN **untouched**. C-003 remains rank-1 open.