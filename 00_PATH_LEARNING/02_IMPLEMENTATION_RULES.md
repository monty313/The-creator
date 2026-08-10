# Implementation rules — PATH LEARNING

These rules bind **code**, **Court**, and **docs**. Violating them = out of path (cliff, not road).

---

## R1 — Court before production behavior

| Rule | Detail |
|------|--------|
| Full Court | **A10** openings + counters + **A15** Counsel; Judge IRAC names three opinions |
| goal_axes | At least G-TRAIN, G-L2L, G-A13, G-CLEAR, G-NO_RETRAIN, G-BREACH0 |
| New tests | Each side / claim needs **new** tests for this case (not old greens alone) |
| Docket | Rank-aware: serves L2L-P10 / C-004; no freestyle final boss claim |

**Forbidden:** shipping production brain behavior changes mid-session without case + ledger.

---

## R2 — Offline train only; freeze at inference

| Rule | Detail |
|------|--------|
| Train | `meta_update` / curriculum only when unlocked offline |
| Prove / forward | `freeze_for_inference`; target/risk change **state only** (**A14**) |
| Fingerprint | Stable across T×R after freeze |

**Forbidden:** inference retrain; “practice” stub as production brain (**A14/A29**).

---

## R3 — Dual SSOT / floor or re-floor

| Rule | Detail |
|------|--------|
| Floor numbers | hits ≥ **11**, low_hr ≥ **0.28**, a13 ≥ **0.64**, n_zero ≤ **18**, breach **0** |
| Protocol | Same dual that set BEST_POLICY floor **or** Full Court re-floor first |
| Named report | Dual JSON must state protocol name |

**Forbidden:** promote on north-star marginal win alone without floor hold or re-floor (`DETHRONE_THE_KING.md`).

---

## R4 — Ledger and SSOT retention (**A33**)

| On event | Append / update |
|----------|-----------------|
| Court ruling | `ledger/EVIDENCE_LEDGER.jsonl` |
| Dual measure | `ledger/SCOREBOARD_HISTORY.jsonl` + artifact report |
| PROMOTE only | `BEST_POLICY.md` + champion npz + sidecar |

**Forbidden:** silent overwrite of `meta_policy_champion.npz`.

---

## R5 — Forbidden teacher / densify classes

| ID | Forbidden |
|----|-----------|
| **F-024** | Synthetic silent-day densify as win law |
| **F-025** | Real labels + **fake rebuilt** state |
| Process-washout promote | Pure process wait flood as production |
| Pure path-clone promote | Answer-copy only with no outcome/conversion/holdout mix claimed as “learning” |
| Pad thrash | Live force-pad to fake A13 |
| Inference retrain | Weights change at prove |

---

## R6 — Mix ratios (default lab)

| Component | Default share of updates | Notes |
|-----------|--------------------------|--------|
| Goal/risk + conversion + outcome | **0.55–0.70** | Primary learning diet |
| Light density process | **0.10–0.20** | Senses reading; density_mode OK |
| Path-state anchors | **0.15–0.25** | Sparse; **re-anchor last** |
| Holdout (high T) | **0.10–0.20** of process/goal | Separate stats |

Path re-anchor **last** if process ran (R6a).

---

## R7 — Lab vs production

| Artifact | When |
|----------|------|
| `meta_policy_path_learning.npz` | Lab shadow after ACCEPT* + train |
| `meta_policy_champion.npz` | Only after PROMOTE + floor hold + BEST_POLICY rewrite |

Lab ACCEPT_NARROW ≠ production replace.

---

## R8 — Code map (shipped entry points)

| Module | Role |
|--------|------|
| `meta_rl/path_learning.py` | Steps 1–6 helpers: outcome, conversion, mix, holdout train, promote_guard |
| `meta_rl/train_path_learning.py` | End-to-end lab train + dual + guard |
| `meta_rl/l2l_process.py` | Process targets (density_mode) |
| `meta_rl/path_state_harvest.py` | Path filter/apply anchors |
| `tests/test_path_learning.py` | Pins on **shipped** functions |

---

## R9 — Predicted-outcome honesty

If dual does **not** move hits/holdout as `03_PREDICTED_OUTCOMES.md` expects, **do not** claim learning succeeded — report failure mode (washout / clone / flat hits) and keep champion.
