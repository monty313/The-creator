# CASE-0016 — Regime catalog: who defines them, TF+indicators, do they work?

**case_id:** CASE-0016  
**status:** PROMOTED (hybrid regime catalog — unit-tested)  
**opened:** 2026-08-07  
**docket_issue_id:** ISSUE-ROAD  
**goal_gap:** learnable regime labels for meta-policy + Court  
**question:** What **complete set of regimes** will we use; how is each defined with **indicator groups + Mark timeframes**; and whose catalog wins (Creator internet vs Mark physics vs hybrid) under **measured unit discrimination**?

**scope:** `meta_rl/regimes.py`, tests, A16 ontology link  
**protected_invariants:** MARK_SETS_LAW; A10; A14 train; A16 win/pass; no goal_path thrash cliffs; no final-boss hit claim from this case alone  

---

## ROUND STRUCTURE (Law A10)

```
Creator opening + NEW test → Mark opening + NEW test
→ one counter each → Critic → Optimist → Judge → units → IRAC
```

---

## Creator opening — internet catalog

**strongest_internet_argument:** Regime literature classifies markets as **trend / range / volatility expansion / compression / transition** so strategies can adapt (trend-follow vs mean-revert vs wait). Multi-TF alignment and vol state are standard.

**claim:** Production catalog must include at least: trend_bull, trend_bear, range_chop, vol_expansion, vol_compression, transition (+ conflict for multi-TF systems).

**new_test:** `test_creator_new_internet_regime_catalog_coverage`

**prediction:** Creator name set ⊆ hybrid `RegimeId`.

---

## Mark Here, Esq. — opening

**strongest_knowledge_argument:**
1. Regime is **multi-set HTF force consensus** (agree_long/short/conflict/incomplete/chop) — eyes on official stacks.  
2. **Entropy/chop** → wait (PHYSICS_INFORMED_L2L).  
3. **Conflict** → kill new risk.  
4. Incomplete eyes ≠ fire.  
5. Each regime bound to **all 4 Mark sets** HTFs:  
   `1m|15m,30m · 5m|30m,1h · 15m|1h,4h · 30m|4h,1d` with `trend_dir` on confirm TFs.

**claim:** Mark catalog + TF bindings are non-negotiable for production; internet names map onto them.

**new_test:** `test_mark_new_physics_regime_catalog_and_tfs`

---

## Creator counter

**counter:** Classifier must **discriminate** regimes on synthetic sensor tuples (not just enum names).  

**newer_test:** `test_creator_new_classifier_discriminates_regimes`

---

## Mark counter

**counter:** Playbook road-signs: conflict/compression **kill**; trend **allows fire** (still needs structure trigger).  

**newer_test:** `test_mark_new_fire_kill_playbook_by_regime`

---

## Critic

| Check | Note |
|-------|------|
| Look-ahead | Classifier uses completed multi_set_consensus + efficiency only |
| Cliff | Regime is filter/context, not a thrash pad generator |
| Overlap | VOL_EXPANSION refines TREND when efficiency high — priority order fixed in code |
| A16 | Win/pass remain scoreboard, not regimes |

---

## Optimist

Clear regimes 2x curriculum labeling and let meta-train condition on regime-like state later.

---

## Judge pretrial

1. Run CASE-0016 NEW tests.  
2. Code: additive `regimes.py` only.  
3. PROMOTE hybrid catalog if units green and every regime has TF+indicator binding.  
4. “Who has best definition” → **hybrid Court catalog** if both catalogs ⊆ hybrid and classifier discriminates.  
5. Not a final-boss hit-rate claim.

---

## Results

`python -m pytest evidence_court/tests/test_case0016_regimes.py -v` → **4/4 PASS**  
(with ontology TF suite: **10/10** green in joint run)

| Test | Role | Result |
|------|------|--------|
| `test_creator_new_internet_regime_catalog_coverage` | Creator opening | **PASS** |
| `test_mark_new_physics_regime_catalog_and_tfs` | Mark opening | **PASS** |
| `test_creator_new_classifier_discriminates_regimes` | Creator counter | **PASS** |
| `test_mark_new_fire_kill_playbook_by_regime` | Mark counter | **PASS** |

**Code:** `meta_rl/regimes.py`

---

## Who has the best definition? (Judge)

| Source | Contribution | Result |
|--------|--------------|--------|
| **Creator / internet** | trend, range, vol expansion/compression, transition | Names ⊆ hybrid |
| **Mark / physics** | multi-set consensus, conflict, incomplete, chop mask, HTF force on official stacks | Eyes + kill rules |
| **Hybrid (PROMOTED)** | Union of both + fixed classifier priority + TF/indicator bindings on all 4 Mark sets | **Wins** |

Neither side alone: internet lacks Mark incomplete/conflict discipline; Mark alone under-names vol expansion/compression. **Hybrid Court catalog is the production definition.**

---

## Production regimes (8)

| RegimeId | Indicators (group) | Timeframes | Fire road-sign |
|----------|-------------------|------------|----------------|
| `trend_bull` | trend_dir HTF + multi_set_consensus | All 4 sets HTF | allow |
| `trend_bear` | same | All 4 sets HTF | allow |
| `range_chop` | consensus chop + efficiency | All 4 sets HTF | wait |
| `conflict` | multi_set conflict | All 4 sets HTF | **kill** |
| `incomplete` | incomplete HTF eyes | All 4 sets HTF | wait |
| `vol_expansion` | efficiency≥0.70 + directed force | All 4 sets full | allow |
| `vol_compression` | efficiency≤0.25 | All 4 sets full | **kill** |
| `transition` | incomplete + directed force | All 4 sets HTF | cautious allow |

**Mark stacks (every regime):**  
set1 `1m|15m,30m` · set2 `5m|30m,1h` · set3 `15m|1h,4h` · set4 `30m|4h,1d`

---

## Judge IRAC

- **Issue:** Complete regime set; best definition; unit-test that regimes discriminate.  
- **Rule:** A10; MARK_SETS_LAW; ROAD; each regime = indicators + TFs; hybrid if both catalogs map and classifier works.  
- **Application:** 4 NEW tests green; catalog 8 regimes; fire/kill playbook pinned.  
- **Conclusion:**  
  1. **PROMOTE Law A17 — Official regime catalog (hybrid).**  
  2. Module `regimes.py`; tests `test_case0016_regimes.py`.  
  3. Forward path may later **wire** `classify_regime_court` into day meta (separate case).  
  4. Does not alone promote final-boss hit-rate.
