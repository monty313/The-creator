# CASE-0021 — One-sym full-scale path + multi-set real edge density

**case_id:** CASE-0021  
**status:** PROMOTED (narrow path geometry; dual scoreboard deferred)  
**opened:** 2026-08-07  
**closed:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD  
**question:** What **measured** change restores trade density and real edges **without** residual multi thrash (F-017/019) **and without** residual starve (F-020)?

**scope:** `goal_path.py` production geometry + force floors  
**protected_invariants:** A10–A20 API; A19 regime channel; fill_hold 0012; no pad; PROVEN untouched  

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → pretrial → units → IRAC

---

## Creator opening

### strongest_internet_argument

After failed residual duals, **restore the best conversion path geometry** (CASE-0012: 1-symbol full scale + asymmetric hold) then densify **signals**, not noise. Literature: position sizing thrash ≠ edge density; quality entries at full unit beat averaging multi residual.

**claim:** Production `production_symbols_per_slot()==1` and `production_leg_size_scale==1.0` anti-starve.

**new_test:** `test_creator_new_production_one_sym_full_scale_anti_starve`

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

1. Multi-set HTF agree is real confluence — force floors can ease slightly when eyes agree.  
2. Pullback still primary; continuation prime-gated.  
3. Never pad: floors stay >0.  
4. Conflict kill remains (A17/A19).

**claim:** `real_edge_force_min` lower when multi_set_agree.

**new_test:** `test_mark_new_multiset_agree_lowers_real_force_floors`

---

## Creator counter

**counter:** Floors never pad-zero; continuation still prime-session gated.

**newer_test:** `test_creator_new_floors_never_pad_zero`

---

## Mark counter

**counter:** A20 residual helpers remain for lab; production path is not multi residual.

**newer_test:** `test_mark_new_a20_helpers_remain_but_production_not_multi`

---

## Counsel opinion (A15)

### internet_sift

Signal density via confluence thresholds beats residual pyramiding after dual residual failures. Path capacity (A13) needs **more true fires**, not multi thrash or zero residual scale after first fill.

### policy_recommendation

Wire day path to 0012-class 1-sym full-scale; keep A19 doctrine; ease force floors only under multi-set agree; unit-pin; **forward100 next fire** (CASE-0022) vs 0012/0013/0020 baselines.

### opinion

Creator restore geometry + Mark multi-set floors = hybrid road. Counsel agrees dual measure deferred.

### evidence

`tests/test_case0021_one_sym_edge_density.py` 4/4 + 0012/0019 regression.

### sources

- CASE-0012 conversion path; F-017…F-020 taxonomy  
- ROAD_FOR_THE_POLICY.md  
- Multi-TF confluence entry (design class)  

---

## Critic

| Check | Note |
|-------|------|
| F-020 | full scale after anchor — fixed starve |
| F-017/019 | no multi residual |
| Pad | floors > 0.05 |
| Dual | units only this fire |

---

## Optimist

Restoring 0012 geometry + real multi-set density 2x path to dual measure.

---

## Judge pretrial

1. 4 NEW + 0012/0019 regression.  
2. Code: production_* + real_edge_force_min + day path wire.  
3. No forward100 this fire.  
4. PROMOTE narrow if green.

---

## Results

`pytest test_case0021… + 0012 + 0019` → **12/12 PASS**

---

## Judge IRAC

- **Issue:** Road path geometry after residual dual failures?  
- **Rule:** A10+A15; ROAD; no F-017…F-020; A13 MUST still open.  
- **Application:** Units green; 1-sym full-scale restores anti-starve; multi-set floors densify real edges; A20 API preserved.  
- **Conclusion:**  
  1. **PROMOTE Law A21 (narrow)** — Production day path = 1-sym full-scale + multi-set real force floors; keep A19 channel + 0012 hold.  
  2. Dual scoreboard → **CASE-0022** forward100 seed=42.  
  3. Not final-boss promote_ready alone.
