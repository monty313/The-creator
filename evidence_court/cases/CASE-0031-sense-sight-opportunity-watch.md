# CASE-0031 — Sense SIGHT + Opportunity Watch Agent (A28) · **C-001**

**case_id:** CASE-0031  
**status:** OPEN — **path wire PROMOTED (narrow)**; dual / miss-rate 100d / final-boss **not claimed**  
**opened:** 2026-08-07 (Monty permanent order — senses docket)  
**fired:** 2026-08-07  
**checklist:** creator  
**item_id:** C-001  
**also_serves:** C-005 (sight slice)  
**docket:** `SENSES_CASE_DOCKET.md` · Law **A28** · schedule **A30**  

**question:** Does the always-on **Opportunity Watch Agent** correctly detect **missed** HTF-trend + LTF RSI5/BB10 **pullback_resume / continuation** opportunities (esp. **London/NY**), file **multiple complaints** with `how_to_sense_next` (sight), **wire into every `run_goal_path_day` decision**, export **curriculum labels** for offline meta, and can measured miss-rate fall without dual regression?

**scope:** `opportunity_watch.py` wire into day-path/forward meta; curriculum label export; sight sense use of complaints; units + optional 100d  
**protected:** A13 MUST; A14 trained meta; A26/A27 path laws; no pad; no F-011…F-022 rehash; PROVEN untouched; Watch does **not** force trades  
**horizon:** long-term performance  

**Baseline CASE-0029:** breach 0 | hits 11 | low_hr 0.28 | a13 28% | mean_tr 7.27 | max_pnl 70  

---

## ROUND STRUCTURE (A10 + A15)

```
Creator opening + NEW test → Mark opening + NEW test
→ one counter each → Counsel (internet best policy)
→ Critic → Optimist → Judge pretrial → experiment → IRAC
```

**Complaints:** many Watch complaints may attach to this case.

---

## Creator opening

### strongest_internet_argument

**Opportunity-cost / regret logging in hierarchical control:** systems that only optimize taken actions under-sample **missed state-action pairs**. An always-on detector that labels “HTF trend + LTF timing present, policy waited” supplies supervised / meta targets for **sight** (structure perception) — standard in goal-conditioned and offline RL (conservative Q / advantage from counterfactuals). London/NY is the high-liquidity window where miss cost dominates long-term expectancy.

**claim:** `OpportunityWatchAgent` + `edge_is_opportunity` + miss complaints when bot waits on PB/cont.

**new_test:** `tests/test_case0031_sense_sight_watch.py::test_creator_new_watch_flags_miss_on_wait` — **PASS**

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. Mark law: HTF force permission + LTF RSI5/BB10 on **set entry TF** for pullback_resume and continuation (A7).  
2. Miss = eyes saw bread-and-butter, bot flat — **sight failure**, not “no edge.”  
3. London/NY = most activity; watch weight there is Mark-session truth.  
4. Multiple set misses same clock → multiple complaints (four sets).

**claim:** Opportunity definition matches Mark topologies only when `htf_agree` + PB/cont; multi-set multi-complaint.

**new_test:** `tests/test_case0031_sense_sight_watch.py::test_mark_new_multi_set_multi_complaint` — **PASS**

---

## Creator counter (exactly one)

**counter:** Watch must not invent opportunities without HTF agree (anti-pad).  
**newer_test:** `test_creator_new_no_opportunity_without_htf_agree` — **PASS**

---

## Mark counter (exactly one)

**counter:** Taken matching side is **hit**, not miss (no false complaint).  
**newer_test:** `test_mark_new_taken_is_hit_not_complaint` — **PASS**

---

## Counsel opinion (A15)

### internet_sift

Sifted offline RL + goal-conditioned hierarchical design classes (2020–2026):

1. **Missed-action / counterfactual coverage** — offline RL fails when the dataset only logs taken actions; policies never learn “what should have fired.” Logging counterfactual opportunities (states where a better action existed) is the standard fix class (Levine offline RL survey line; CQL conservatism about OOD actions is the dual problem — we must **label** the good missed acts so the behavior dataset is not only waits).  
2. **Unlabeled → labeled offline data** — Yu et al. (ICML 2022): reward/label functions over passive logs turn unlabeled trajectories into training signal. Watch complaints are exactly that labeler for Mark PB/cont.  
3. **Goal-conditioned offline / hierarchical GCRL** — Park et al. (NeurIPS 2023) and later OGCRL work: long-horizon goal agents need hierarchical subgoal structure; high-level “should fire opportunity” is a subgoal signal separate from low-level size.  
4. **Conservative offline RL (CQL / BAIR)** — do not invent force-fire overrides from OOD Q overestimation; **complain + offline train**, do not silently pad live path. Matches A28 “no production override alone.”

### policy_recommendation

**Best policy for C-001:**

1. **Always-on Watch inside `run_goal_path_day`** every decision slot (including empty / wait slots).  
2. **Log** `n_opportunities / n_misses / n_hits / n_london_ny_misses` + sample complaints into day `meta`.  
3. **Export curriculum labels** from misses (`teacher_act` = opportunity side; **London/NY weight > other**).  
4. **Do not force trades** from Watch (A28 + CQL anti-thrash). Live path stays brain + risk rails.  
5. **C-002** consumes labels for real-bar / opportunity-weighted meta-train (out of scope for this narrow wire).  
6. Optional later: aggregate miss-rate on 100d vs CASE-0029 floor without dual regression.

### opinion

**Weighs:** Creator’s counterfactual-logging argument is correct for learning loop closure. Mark’s HTF-first opportunity definition is the only legal opportunity ontology (anti-pad). Counsel science agrees: label misses offline; do not live-force. Judge should **PROMOTE the path wire + label export** as C-001 loop-close infrastructure, **reject** dual/final-boss claims until C-002/C-003/C-004 measure.

### evidence

- Unit openings/counters: `test_case0031_sense_sight_watch.py` (4 A10 + 3 C-001 wire) — all **PASS**  
- Code: `opportunity_watch.py` (`curriculum_labels_from_report`, `watch_day_summary`)  
- Wire: `goal_path.run_goal_path_day(..., watch_enabled=True)` default  
- Champion prove `15/2`: trained, no-retrain, fingerprint stable (pre-measure)

### sources

- Yu et al., “How to Leverage Unlabeled Data in Offline Reinforcement Learning” (ICML 2022) — https://proceedings.mlr.press/v162/yu22c.html  
- BAIR / CQL offline RL conservatism — https://bair.berkeley.edu/blog/2020/12/07/offline/  
- Park et al., Offline Goal-Conditioned RL with Latent States as Actions (NeurIPS 2023)  
- Hierarchical offline control class (Guider / IJCAI 2023 offline hierarchical RL)  
- Repo law A28 `OPPORTUNITY_WATCH_LAW.md` · ROAD_FOR_THE_POLICY (miss labels = road, force-pad = cliff)

---

## Critic

- Wire alone does **not** drop London/NY miss-rate on real bars — that needs C-002 retrain + 100d.  
- Multi-symbol multi-set Watch can emit **high complaint volume**; meta must not treat volume as thrash incentive.  
- Pre-existing suite break: `sample_training_state` missing → test_case0017 / 0018 collection ERROR (unrelated to this wire; still a Court hygiene defect).  
- forward100 not re-run this fire (~80 min); dual floor held only by non-regression of path logic (Watch is observe-only).

---

## Optimist

- Learning loop is **closed for observation + labels** — the single highest-leverage C-001 unlock.  
- London/NY weight already in label export → C-002 can drill the right band immediately.  
- Empty-slot Watch catches “no candidate / wait while Mark eyes saw PB” — flea-jar evidence, not silence.  
- Units prove: no HTF pad, taken=hit, multi-complaint, path meta always_on, no force-fill.

---

## Judge pretrial

1. Confirm A10 unit openings/counters — **PASS** (4 tests).  
2. Order experiment: wire Watch into `run_goal_path_day` every slot; export curriculum labels; **no force trade**.  
3. New integration tests: path meta always_on; London/NY weight; lab opt-out — **PASS**.  
4. Optional 100d miss metrics — **deferred** to after C-002 or next measure window (not blocking narrow wire).  
5. Dual promote_ready — **not in scope**.

---

## Experiment results (this fire)

| Check | Result |
|-------|--------|
| prove 15 2 | trained, no_retrain, fp `42:meta9600:…` |
| A10 unit 4 | **PASS** |
| C-001 curriculum labels weight | **PASS** |
| C-001 goal_path watch meta | **PASS** |
| C-001 watch opt-out lab | **PASS** |
| opportunity_watch_law + goal_path_case0003 | **PASS** (with case0031 = 18 passed) |
| forward100 dual remeasure | **not run** this fire (Watch observe-only; dual claim not asserted) |

**Code landed (Judge-ordered experiment):**

| File | Change |
|------|--------|
| `meta_rl/opportunity_watch.py` | `curriculum_labels_from_report`, `watch_day_summary` |
| `meta_rl/goal_path.py` | `watch_enabled=True` default; every slot scan; meta watch + labels |
| `tests/test_case0031_sense_sight_watch.py` | +3 C-001 wire tests |

---

## Judge IRAC

- **Issue:** Can C-001 close Watch→path→brain **observation/label loop** under A28 without pad, dual regression, or force-fire cliffs?  
- **Rule:** A10+A15 three opinions; A28 always-on Watch, no production override alone; A13 no pad; A14 no retrain at prove; ROAD (labels = road; thrash force = cliff); A30 C-001 first.  
- **Application:**  
  - **Creator:** counterfactual miss logging — proved; path wire lands labels.  
  - **Mark:** HTF+PB/cont only, multi-complaint, taken=hit — proved.  
  - **Counsel:** offline label-from-passive-log + no live force — adopted.  
  - Measure: units green; path emits `meta["watch"]` + `curriculum_labels`; Watch cannot pad fills.  
- **Conclusion:**  
  1. **PROMOTE (narrow) — C-001 path wire + curriculum label export** as production always-on behavior (`watch_enabled=True` default).  
  2. **C-001 checklist row → IN_COURT / partial:** loop-close for **logging+labels** done; **miss-rate drop on 100d** and **labels→meta-train** remain (C-002 owns retrain).  
  3. **REJECT** dual / final-boss / promote_ready from this case.  
  4. **Next:** **C-002** real-bar / opportunity-labeled meta-train consuming `curriculum_labels`; then C-003 A13 density. Optional CASE-0031 follow-up measure: 100d miss aggregates without dual regression.  
  5. **Sight (C-005 slice):** Watch complaints available; packing into state channels still CASE-0031 residual / C-005.

---

## Complaints log (attach from Watch runs)

| complaint_id | topology | session | sense_gap | how_to_sense_next |
|--------------|----------|---------|-----------|-------------------|
| *(runtime via meta["watch"]["sample_complaints"])* | | | | |

---

## Next after this case

**C-002** opportunity-labeled meta-train · **CASE-0032 Feel** · **0033 Taste** · **0034 Hearing** per `SENSES_CASE_DOCKET.md`.
