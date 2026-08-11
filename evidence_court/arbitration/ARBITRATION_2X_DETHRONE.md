# Arbitration meeting — all Court roles / LLM seats

**case_id:** ARBITRATION-2X-DETHRONE  
**opened/closed:** 2026-08-09  
**Purpose:** From **ruled cases first**, agree the **most efficient** way for the policy to **learn and reason** so a challenger can **dethrone the king by ~2×** (lawful dual, not slogans).  
**King:** CASE-0037 · `42:meta4275:…` · floor hits **11** / low_hr **0.28** / a13 **0.64** / n_zero **18** / breach **0**  
**2× bar (consensus definition):** under **same dual SSOT that set the floor (forward100 class)**:

| Metric | King floor | **2× dethrone target** |
|--------|------------:|------------------------:|
| hits | 11 | **≥ 22** |
| low_hr | 0.28 | **≥ 0.50** (≈1.8×; full 2×=0.56 preferred) |
| a13_frac | 0.64 | **≥ 0.85** (not 1.28 — capped; “2× density residual” = cut zeros+partials ~in half) |
| n_zero | 18 | **≤ 9** |
| breach | 0 | **0** (absolute) |
| no_retrain | true | **true** |

**Not claimed done.** This document is **agreement on method**, not a production PROMOTE.

### Execute log (2026-08-09)

| Field | Value |
|-------|--------|
| Runner | `meta_rl/train_2x_clear_road.py` |
| Shadow | `artifacts/meta_policy_2x_clear_road.npz` |
| Report | `artifacts/execute_2x_clear_road_report.json` |
| Dual protocol | forward100_class (100d) |
| Dual result | hits **11** · low_hr **0.28** · a13 **0.64** · n_zero **18** · breach **0** · frozen |
| Milestone A (hits≥15) | **false** |
| Target 2× (hits≥22) | **false** |
| Production replace | **false** (king meta4275 unchanged) |

**Inputs:** `COURT_TRIALS_AUDIT.md` · ruled case files · `BEST_POLICY.md` · `DETHRONE_THE_KING.md` · `00_PATH_LEARNING/` · L2L series · residual/PATH_LEARNING duals  

---

## Part A — Look at ruled cases first (lessons all seats must share)

### A1. What PROMOTE / ACCEPT taught (keep)

| Case cluster | Ruling | Lesson for learning |
|--------------|--------|---------------------|
| **0001–0002** | PROMOTE | Real multi-TF state + edges beat freestyle indicators |
| **0003–0013** | mostly PROMOTE (path geometry, R, size, cadence) | **Road rails** for the brain: capacity, partials, A13 band — not the decider |
| **0015–0019** | PROMOTE narrow | Ontology + regime curriculum = structure the policy can *read* |
| **0021, 0023, 0028, 0029** | PROMOTE narrow | Density geometry + cont hold-R + **5m clock** raise *opportunity surface* |
| **0031 / C002** | PROMOTE narrow (wire/API) | Watch→labels→offline train path exists; not enough alone for dual clear |
| **0037** | **PROMOTE_NARROW** **king** | **Path-packed 176-d teachers at brain-wait** = only density leap that held floor dual (a13↑, n_zero↓, hits flat) |
| **L2L-P1** | ACCEPT | Senses **in state** change logits — required for “reason” |
| **L2L P2–P9** | ACCEPT / NARROW | Process reading is real; freeze + no-retrain work |
| **L2L-P10 residual** | ACCEPT_NARROW_LAB | Process then **path re-anchor last** anti-washout |
| **PATH_LEARNING** | ACCEPT_NARROW lab | Outcome + conversion mix is the **stated** learn-not-copy road |

### A2. What REJECT taught (do not repeat)

| Case | Ruling | Lesson |
|------|--------|--------|
| **0020, 0022, 0024, 0025–0027, 0030-session** | dual REJECT / near-null | Geometry/clock alone ≠ clear%; dual is the truth |
| **0035 F-024** | REJECT | Synthetic densify → thrash / worse zeros |
| **0036 F-025** | REJECT | Labels + **fake rebuilt state** = wrong distribution |
| **L2L process-only** | P10 REJECT full | Wait-process CE **washes A13** (n_zero↑) |
| Pure path-clone forever | hits stuck **11** | Answer-copy densifies; **does not 2× hits** |

### A3. What is still not ruled / not through Court

C-004 conversion · C-006…C-012 · CASE-0032…0034 · L2L §7 — **no freestyle skip**; efficient path must still serve **rank-1 L2L-P10 / C-004** and legal dethrone gates.

### A4. King diagnosis (all seats agree)

```text
King strength:  A13 density from path-state BC on real wait states; breach 0; frozen.
King weakness:  hits=11 (conversion); 18 zero + 18 partial days; high-T weak; senses not fully Feel/Taste/Hearing cases.
2× means:      primarily DOUBLE HITS (11→22) while holding a13 high, cutting zeros ~half, breach 0 — not more BC only.
```

---

## Part B — Arbitration seats (all LLMs / Court roles)

Each seat speaks once after Part A. Then **binding consensus**.

---

### Creator (internet + engineering efficiency)

**Thesis:** Most efficient 2× is **not** more path-state clone volume. It is:

1. **Harvest outcome-labeled path trajectories** (real day path: packed state + act + **post-hoc outcome** clear/R/breach/dead) — still offline.  
2. **Primary diet = conversion + outcome-shaped updates** under varying goal/risk (PATH_LEARNING 1–4), path anchors **sparse**.  
3. **Holdout + forward100 dual only** for promote claims (one SSOT).  
4. **Skip** reopening densify geometry cases that already dual-rejected unless they feed new **conversion teachers**.

**Efficiency order (compute / Court time):**  
Outcome harvest on existing path clock → warmstart 0037 → conversion curriculum → light process → path re-anchor last → forward100 dual → only then Feel/Taste cases if dual shows sense fail modes.

**Disagree with:** Opening CASE-0032–0034 before conversion dual proves hits move (senses help reason, but 2× is clear-limited).

---

### Mark Here, Esq. (physics / knowledge)

**Thesis:** 2× hits without blowing risk is **release timing + hold-R + size under remaining risk**, not thrash density.

Agreed efficient stack:

1. Keep **load→wait**, **collapse→wait**, **risk floor→wait** (Feel/Taste physics) as **teachers**, not live if/then soup.  
2. Conversion teachers: mid-progress **hold_convert** + cont min hold-R (0028) must be in the offline map.  
3. Path-state stays **anchor of truth** (real states); never F-025 rebuild.  
4. London/NY weight on harvest — where clears are born.

**Disagree with:** Pure goal-synthetic curriculum without path anchors (washes Mark’s real setup distribution).

---

### Counsel (A15 — best policy from external + project evidence)

**internet_sift:** Imitation→plateau; reward shaping + goal-conditioned offline RL + trajectory outcome feedback are the efficient stack for conversion after BC densify. Multi-seed eval before claim.

**policy_recommendation — single stack all seats can sign:**

| Priority | Action | Why efficient |
|--------:|--------|----------------|
| **1** | **Outcome-tagged path harvest** (same `collect_path_state` moments + day PnL/progress/R) | Uses existing path; no new live pad; teaches clear not side-only |
| **2** | **PATH_LEARNING execute harder on conversion** (steps 1,4 primary; 2,3,5 anti-washout; 6 guard) | Code already Court-ACCEPT_NARROW |
| **3** | **forward100 dual as only promote SSOT** (lock dual; re-floor only by Court) | Ends north-star vs floor confusion |
| **4** | **Hold density:** path re-anchor last; a13 hard floor 0.30 lab / 0.64 promote | 2× hits useless if A13 dies |
| **5** | **Senses 0032–0034 only after hits move or dual fail-modes name them** | Avoid Court thrash on queued cases while C-004 open |
| **6** | Legal dethrone G1–G7; 2× bar = new BEST_POLICY floor only after PROMOTE | No silent 2× claim |

**opinion:** **UNANIMOUS METHOD** if Critic/Optimist accept efficiency order above.

---

### Critic

**Risks:**  
- Synthetic conversion teachers alone → dual hits flat (PATH_LEARNING 30d hits still 3).  
- “2× a13” misread as 1.28 — impossible/ill-defined.  
- Multi-seed before single-seed 2× wastes compute.  
- Opening all pending C-006…C-012 now is **anti-efficient**.

**Requirement for agreement:** First milestone dual must show **hits ↑ on forward100** vs 11, not only north-star a13 nudges. Real **outcome fields on path packs** mandatory within one lab cycle.

---

### Optimist

**Why 2× is reachable without cliff:** Opportunity surface already dense (mean_tr ~39, a13 0.64). Missing map is **which fires convert under T×R**. Outcome-shaped path + hold_convert is the smallest delta. Residual/PATH_LEARNING already prove anti-washout recipe works.

---

### Judge (IRAC + binding consensus)

**Issue:** Most efficient lawful path for the policy to learn/reason so dual can dethrone king by ~2×.

**Rule:** A10/A15 agreement weight; A14 offline/freeze; A13 no pad; A33 rank (C-004/L2L-P10 first); DETHRONE gates; PATH_LEARNING ACCEPT_NARROW lab; ruled REJECT cliffs binding.

**Application:**  
- Creator efficiency + Counsel stack **aligned**.  
- Mark physics constraints **accepted** (anchors + wait fail-modes).  
- Critic: real outcomes + forward100 first — **adopted**.  
- Optimist: density already there — **adopted** as reason to prioritize conversion not densify cases.

**Conclusion — BINDING ARBITRATION RULING: AGREE**

### The agreed most efficient path (all seats)

```text
NAME:  2× CLEAR ROAD  (conversion-first learning, density-preserving)

0. READ ruled cases (this Part A) — never re-try F-024/F-025/process-washout/geometry dual-null as main path.

1. HARVEST (offline): path-packed states + teacher side + OUTCOME tags
   (progress, day clear, R-capture, breach-near, dead-fire)
   Prefer London/NY · HTF-active · existing 5m/15m production clock.

2. TRAIN (offline, warmstart meta4275):
   PRIMARY  (~60%): outcome-shaped conversion teachers (PATH_LEARNING 1+4)
   SECOND   (~15%): goal/risk holdout high-T (step 3)
   SPARSE   (~15%): path-state fire anchors
   LIGHT    (~10%): density process senses (step 5)
   LAST:    path re-anchor (anti-washout)
   FREEZE.

3. MEASURE: forward100-class dual ONLY for 2× claim
   Targets: hits≥22 · low_hr≥0.50 · a13≥0.85 · n_zero≤9 · breach0
   Milestone A (efficient gate): hits≥15 and a13≥0.64 before chasing 22.
   Multi-seed only after Milestone A.

4. REASON surface: senses stay in state (P1); open 0032–0034 only if dual
   fail-modes show Feel/Taste/Hearing defects blocking conversion.

5. PROMOTE: only DETHRONE G1–G7 + 2× (or Milestone) floor hold + BEST_POLICY rewrite.
   Lab shadows OK anytime under promote_guard.

FORBIDDEN as “efficient”:
  more pure path-clone · process-only · F-024/F-025 · pad thrash ·
  freestyle C-006…C-012 · inference retrain · north-star-only PROMOTE
```

**Efficiency claim (why this is fastest):** Reuses proven density lever and production clock; attacks the **only flat metric under the king (hits)**; avoids re-Court of dual-REJECT densify; uses already-ACCEPTED PATH_LEARNING machinery; single dual SSOT ends measurement thrash.

**What “learn and reason” means under this agreement:**  
- **Learn** = offline map improves **clear under goal/risk** from outcomes, not only match Mark side.  
- **Reason** = packed state + senses + goal context drive act/size; freeze at prove; no hard-rule soup as decider.

---

## Part C — Ranked next actions (binding order)

| # | Action | Owner seat | Docket |
|---|--------|------------|--------|
| 1 | Implement/extend **outcome-tagged path harvest** into path packs | Creator | C-004 / PATH_LEARNING |
| 2 | Lab train cycle under **2× CLEAR ROAD** recipe | Creator | L2L-P10 residual |
| 3 | **forward100 dual** vs king; report hits/a13/n_zero | Creator | C-004 |
| 4 | If Milestone A miss: diagnose conversion vs density; **do not** densify-pad | All | — |
| 5 | If Milestone A hit: push toward hits≥22; then multi-seed | Creator | C-008 later |
| 6 | Full Court PROMOTE only at 2× or Court-agreed re-floor | Judge | DETHRONE |
| 7 | CASE-0032…0034 only if dual fail-modes demand | Court | C-005 |

---

## Part D — Sign-off matrix

| Seat | Agrees to 2× CLEAR ROAD? |
|------|--------------------------|
| Creator | **YES** |
| Mark Here, Esq. | **YES** (with path anchors + wait physics) |
| Counsel | **YES** (recommended stack) |
| Critic | **YES** (conditional: real outcomes + forward100 first) |
| Optimist | **YES** |
| Judge | **YES — BINDING** |

**Unanimous agreement recorded.**  
**Production champion unchanged** until lawful PROMOTE after measured 2× (or Milestone + later Court order).

---

## Pin paths

| Path | Role |
|------|------|
| This file | Arbitration SSOT |
| `COURT_TRIALS_AUDIT.md` | Ruled / unruled inventory |
| `DETHRONE_THE_KING.md` | Legal replace gates |
| `00_PATH_LEARNING/` | Learn-not-copy steps |
| `BEST_POLICY.md` | King floor |
