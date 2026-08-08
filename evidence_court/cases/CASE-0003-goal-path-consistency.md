# CASE-0003 — Goal-conditioned multi-leg path for random-target consistency

**case_id:** CASE-0003  
**status:** ADMITTED (implementation in progress; final PROMOTE when 100d consistent hits)  
**question:** How should the frozen Meta-RL bot **consistently hit randomly assigned daily targets** over 100 forward days under risk [1–3], without retrain, while preserving Mark multi-TF edge, L2L, senses, flea-jar full action space, and breach=0?

**scope:** `evidence_court/meta_rl/goal_path.py`, `forward_eval.py`, `edge.py` (asof_time + lookback caps), tests  
**protected_invariants:** MARK_SETS_LAW; Meta-RL 176; no-retrain; daily risk envelope; no look-ahead; PROVEN untouched; Law A10 rounds

---

## ROUND STRUCTURE (Law A10)

### Creator opening — strongest internet argument + new test

- **strongest_internet_argument:** Hierarchical / **goal-conditioned RL** (subgoal chain under a hard constraint): treat the daily target as a goal state; break the day into sequential slots; size tickets from remaining goal distance under the risk budget; lock when goal reached. Design class: goal-conditioned policies + hierarchical trading RL (e.g. CoGHP / hierarchical QT literature) — **evidence class, not authority**.
- **claim:** Multi-slot M1 path with goal-conditioned sizing + target lock raises clear/hit rate vs single open→close day bar without breaching.
- **new_test:** `tests/test_goal_path_case0003.py` — multi-leg path runs; no look-ahead; goal size increases with remaining goal; lock when hit.
- **prediction:** 100d random matrix: breach=0; low-band hit_rate climbs vs pre-CASE-0003 (~2 hits total).

### Mark opening — strongest knowledge argument + new test

- **strongest_knowledge_argument:** Force owns side; LTF times; wait on slingshot_load; pullbacks **and** continuations on confirmed HTF; multi-symbol concurrent; 1:100 risk-legal lots; incomplete size/coverage ≠ impossible (flea-jar). Hitting target is **capability under full action space**, not a sermon.
- **claim:** Path must not fire against multi-set conflict; must prefer pullback_resume; session path before entry must not thrash against force; missing valid pullbacks is coverage failure.
- **new_test:** Mark NEW tests in `test_goal_path_case0003.py::test_mark_new_session_confirm_and_conflict_skip` — conflict skipped; slingshot not traded; session_confirm filter present.
- **prediction:** Senses/L2L day-path remain true; breach stays 0.

### Creator counter (1×)

- **counter_argument:** Mark wait purity alone under-covers; need multi-symbol concurrent + finishing size for near-target days.
- **newer_test:** multi-symbol pick top-2 when target≤30; finishing size when rem_goal small.

### Mark counter (1×)

- **counter_argument:** Finishing size must still respect envelope; never force_side oracle.
- **newer_test:** breach still 0 on path ledger under max risk 1–3; side from edge/state only.

---

## Implementation (Creator after ADMIT)

| Module | Role |
|--------|------|
| `goal_path.py` | Multi-slot path, goal size, M1 fill, lock |
| `forward_eval.py` | `pair_mode=random`, `use_goal_path=True` default |
| `edge.py` | `asof_time` filter + lookback caps |

## Pretrial metrics (final PROMOTE)

1. n_days ≥ 100  
2. breach_count = 0  
3. no_retrain = true  
4. l2l_day_path_ok + senses_day_path_ok  
5. random targets across 5–90 × risks 1–3  
6. **consistent hits:** low_hit_rate (≥ on ≤15% targets) ≥ 0.18 and total_hits ≥ 12 (or stricter climb)  
7. pullback+continuation coverage > 0; multi_symbol; leverage 100  

## IRAC (live)

- **Issue:** Consistent random-target clears over 100d.  
- **Rule:** A10 + flea-jar + no-retrain + breach 0 + measured hit spectrum.  
- **Application:** Goal path implemented; 100d remeasured; hit rates climbing; not yet final-boss PROMOTE until consistent_spectrum true.  
- **Ruling:** **ADMIT_EXPERIMENT** → continue CASE-0003 iterations / CASE-0004 edge sharpen until promote_ready.
