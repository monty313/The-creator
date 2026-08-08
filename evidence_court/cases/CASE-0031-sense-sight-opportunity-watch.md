# CASE-0031 — Sense SIGHT + Opportunity Watch Agent (A28)

**case_id:** CASE-0031  
**status:** OPEN  
**opened:** 2026-08-07 (Monty permanent order — senses docket)  
**checklist:** creator  
**item_id:** C-001  
**also_serves:** C-005 (sight slice)  
**docket:** `SENSES_CASE_DOCKET.md` · Law **A28** · schedule **A30**  

**question:** Does the always-on **Opportunity Watch Agent** correctly detect **missed** HTF-trend + LTF RSI5/BB10 **pullback_resume / continuation** opportunities (esp. **London/NY**), file **multiple complaints** with `how_to_sense_next` (sight), and can measured miss-rate fall without dual regression?

**scope:** `opportunity_watch.py` wire into day-path/forward meta; sight sense use of complaints; units + optional 100d  
**protected:** A13 MUST; A14 trained meta; A26/A27 path laws; no pad; no F-011…F-022 rehash; PROVEN untouched  
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

**new_test:** `tests/test_case0031_sense_sight_watch.py::test_creator_new_watch_flags_miss_on_wait`

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. Mark law: HTF force permission + LTF RSI5/BB10 on **set entry TF** for pullback_resume and continuation (A7).  
2. Miss = eyes saw bread-and-butter, bot flat — **sight failure**, not “no edge.”  
3. London/NY = most activity; watch weight there is Mark-session truth.  
4. Multiple set misses same clock → multiple complaints (four sets).

**claim:** Opportunity definition matches Mark topologies only when `htf_agree` + PB/cont; multi-set multi-complaint.

**new_test:** `tests/test_case0031_sense_sight_watch.py::test_mark_new_multi_set_multi_complaint`

---

## Creator counter (exactly one)

**counter:** Watch must not invent opportunities without HTF agree (anti-pad).  
**newer_test:** `test_creator_new_no_opportunity_without_htf_agree`

---

## Mark counter (exactly one)

**counter:** Taken matching side is **hit**, not miss (no false complaint).  
**newer_test:** `test_mark_new_taken_is_hit_not_complaint`

---

## Counsel opinion (A15)

### internet_sift
*(file at fire — sift best policy for miss-aware meta / sight attention)*

### policy_recommendation
*(wire watch into day path meta; train/sense on London/NY miss rate)*

### opinion
*(weigh Creator counterfactual logging vs Mark HTF-first eyes)*

### evidence / sources
*(to be filed at fire)*

---

## Complaints log (attach from Watch runs)

| complaint_id | topology | session | sense_gap | how_to_sense_next |
|--------------|----------|---------|-----------|-------------------|
| *(filled when agent runs)* | | | | |

---

## Judge pretrial / measure

- Units for Watch + sight miss/hit.  
- Optional 100d: miss metrics + dual floor (hits/a13).  
- IRAC must name Creator, Mark, Counsel.

---

## Next after this case

**CASE-0032 Feel** · **0033 Taste** · **0034 Hearing** per `SENSES_CASE_DOCKET.md`.
