# CASE-L2L-P10-residual — Density-preserving residual (Full Court)

**case_id:** CASE-L2L-P10-residual  
**opened:** 2026-08-09  
**depends_on:** CASE-L2L-P2-P10 (P10 REJECT full); CASE-0037 champion  
**goal_axes:** G-A13, G-CLEAR, G-TRAIN, G-NO_RETRAIN, G-L2L, G-BREACH0  
**docket:** rank-1 **L2L-P10** / **C-004**  
**status:** CLOSED — **ACCEPT_NARROW_LAB** (method + dual vs champ); production still CASE-0037  
 

---

## Claim

Process-only L2L curriculum (P2–P7) **washed A13 density** (n_zero↑, a13_frac↓ vs CASE-0037).  
Residual road: **warmstart champion + path-state fire teachers + density-mode process** (softer wait CE, fire-overweight scenarios) → freeze → dual same-window vs champion → **promote only if beats**.

**Forbidden:** pad thrash; inference retrain; replace champion without dual beat; claim final boss without §7.

---

## Creator opening (internet + new tests)

**Argument:** Intermediate process rewards work only when they do not starve the policy of positive fire examples. Over-weighting “wait process” is classic sparse-reward / class-imbalance collapse. Fix = **mix real packed path-state fire teachers** (CASE-0037 lever) with **density-aware process sampling**, not more wait CE.

**new_tests:**
- `tests/test_l2l_p10_residual.py::test_density_mode_raises_fire_frac_vs_balanced`
- `tests/test_l2l_p10_residual.py::test_density_mode_soft_wait_reward_lower`
- `tests/test_l2l_p10_residual.py::test_promote_decision_rejects_washout`
- `tests/test_l2l_p10_residual.py::test_promote_decision_accepts_beat`

**code:** `meta_rl/l2l_process.py` (`density_mode`), `meta_rl/train_l2l_p10_residual.py`

---

## Mark Here, Esq. opening (knowledge + new tests)

**Argument:** The champion already learned fire at brain-wait path states. Process senses must **read** structure/load/taste without **erasing** that map. Load→wait remains fail-mode law; density_mode only softens wait CE weight and oversamples launch/bb_cont episodes. Path-state teachers stay 100% long/short on HTF-active moments.

**new_tests:**
- `test_load_wait_still_wait_without_density_override` (fail-mode preserved)
- existing P2/P3 load wait still green under default mode

---

## Counters (one each)

**Creator counter:** Dual same seed/window is the only fair residual scoreboard; unit fire_frac alone is not PROMOTE.  
**newer test:** promote_decision requires residual a13≥champ, hits≥champ, n_zero≤champ, breach0, a13 hard floor ≥0.30.

**Mark counter (waive second counter):** Accept dual gate; refuse production replace without Court + 100d floor hold.

---

## Counsel opinion (A15 — internet sift)

**internet_sift:** Curriculum learning and process RL literature: auxiliary process losses help *when balanced*; imbalanced negative labels dominate CE and induce over-refusal. Replay of successful trajectories (path-state teachers) is the standard density preservative. Soft reward shaping on wait vs act is preferred over hard production if/then rules.

**policy_recommendation:**
1. Always warmstart from measured champion before process residual.  
2. Apply path-state fire pack first (multiple passes).  
3. Run **short** density process curriculum (not 4k wait-heavy).  
4. Freeze; dual residual vs champion same window; promote only on beat.  
5. Do not claim L2L §7 final gate on 30d single seed.

**opinion:** ACCEPT residual **method** if dual improves A13 without breach; REJECT production PROMOTE if dual washout or only unit greens.

**evidence:** Prior dual washout `l2l_p2_p10_report.json` (a13 0.13, n_zero 22) vs CASE-0037 floor (a13 0.64, n_zero 18).

**sources:** process-reward / curriculum balancing practice; project BEST_POLICY.md floor; A13/A14 laws.

---

## Critic

Risk: density override on patience invents fire process on marginal taste → thrash. Mitigate: only launch/topo + non-noise edge; dual n_zero and mean_tr watched; promote hard floor a13≥0.30.

## Optimist

Path-state 900 fire teachers + champion warmstart should restore density; process density_mode keeps sense reading without wait flood.

---

## Judge IRAC

**Issue:** Can residual train restore A13/clear path after process washout without inference retrain or thrash pad?

**Rule:** A13 must [8,400]/day; A14 train offline only; A10+A15 three opinions; A33 measure→promote only on beat; BEST_POLICY floor.

**Application:**  
- Creator: density_mode + path mix + new pins — accepted as method.  
- Mark: fail-mode load wait preserved; path teachers primary density lever — accepted.  
- Counsel: warmstart→path→light process→dual beat gate — adopted.  
- Prior P10 full Accept remains **REJECT** until dual proves a13_every_day + clears.  
- Production champion stays CASE-0037 unless `promote_decision.promote` **and** Court orders replace + 100d floor hold.

**Conclusion:** Method **ACCEPT_NARROW_LAB**. Terminal measured ruling:

### Dual 30d (north-star random T×R, seed=42, XAU 15m)

| | hits | a13_frac | n_zero | breach | mean_tr |
|--|-----:|---------:|-------:|-------:|--------:|
| **Residual** | 3 | **0.333** | 11 | 0 | 7.73 |
| Champion | 3 | 0.267 | 11 | 0 | 7.27 |

`promote_decision` (30d): **true** (beats champ a13; same hits/n_zero; breach 0)

### Dual 100d (same protocol)

| | hits | a13_frac | n_zero | breach | mean_tr |
|--|-----:|---------:|-------:|-------:|--------:|
| **Residual** | 7 | **0.42** | 35 | 0 | 10.37 |
| Champion same protocol | 7 | 0.41 | 35 | 0 | 10.08 |
| BEST_POLICY floor (forward100) | **11** | **0.64** | **18** | 0 | 39.4 |

`promote_vs_champ_100d`: **true** (marginal a13)  
`floor_100d_hold`: **false** (hits/a13/n_zero all miss BEST_POLICY forward100 floor)  
`production_replace`: **false**  
`final_promote_gate` (§7): **false** (a13_every_day false; multi-seed not run)

| Field | Value |
|-------|-------|
| fingerprint residual | `42:meta10835:inf0:441555412cf1e3ae` |
| production champion | **unchanged** CASE-0037 `42:meta4275:inf0:bcfe6c74f68b7623` |
| shadow | `artifacts/meta_policy_l2l_p10_residual.npz` |
| lab promote copy | `artifacts/meta_policy_l2l_p10_residual_LAB_PROMOTE.npz` |
| recipe | warmstart → light density process → **path re-anchor last** |
| P10 full Accept | **still REJECT** (not every-day 8–400) |

**Why north-star dual ≠ BEST_POLICY floor:** forward100 CASE-0037 used a different measured path (multi-sym / slot / pair setup). North-star dual is the L2L random T×R yardstick. Residual **must not** overwrite champion until it holds the documented forward100 floor **or** Court re-floors under a single SSOT dual.

---

## Code map

| Path | Role |
|------|------|
| `meta_rl/l2l_process.py` | `density_mode` process targets + scenario pool |
| `meta_rl/train_l2l_p10_residual.py` | residual train + dual + promote_decision |
| `tests/test_l2l_p10_residual.py` | unit pins |
| `artifacts/meta_policy_l2l_p10_residual.npz` | lab shadow |
| `artifacts/l2l_p10_residual_report.json` | measure report |

---

## Run

```text
pytest evidence_court/tests/test_l2l_p10_residual.py evidence_court/tests/test_l2l_p2_p10.py -q
python -m evidence_court.meta_rl.train_l2l_p10_residual --process-steps 2000 --dual-days 30
```
