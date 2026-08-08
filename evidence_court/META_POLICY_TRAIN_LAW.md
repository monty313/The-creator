# META POLICY TRAIN LAW — PERMANENT (Monty)

**Law id:** **A14**  
**Status:** PERMANENT  
**Human order:** Monty — meta-learning is **permanent**, not a temporary “practice” phase.  
**Fix:** untrained seed stubs are **not** production brains.

---

## THE LAW

1. **The policy must be meta-trained** before prove / forward / production use.  
2. **Meta-learning is permanent architecture** — one trained map that **automatically** conditions on target/risk context to pursue different daily targets.  
3. **No-retrain at inference:** when Monty changes target % or risk %, **weights do not update**. Adaptation is via goal/risk state channels + the already-trained meta map.  
4. **Offline meta-train** (`meta_update` / `train_goal_conditioned_meta_policy` / CLI `meta-train`) is the permanent way weights improve.  
5. Calling `train_step` / `meta_update` while **frozen for inference** is a **NO_RETRAIN_VIOLATION**.

| Mode | Allowed |
|------|---------|
| Meta curriculum (unlocked) | `meta_update`, multi-target training, save champion |
| Prove / forward (frozen) | `forward` only; fingerprint stable across pairs |
| Untrained prior | **Forbidden** for freeze/forward/production |

---

## Code

| Piece | Path |
|-------|------|
| Policy | `meta_rl/policy.py` — `MetaPolicy`, `train_goal_conditioned_meta_policy` |
| Champion | `artifacts/meta_policy_champion.npz` |
| CLI | `python -m evidence_court.meta_rl.cli meta-train` |
| Load path | `load_or_train_champion` used by prove / forward100 |
| Tests | `tests/test_meta_policy_train.py`, `tests/test_goal_risk_no_retrain.py` |

---

## Relationship to A2

**A2 clarified:** “no retrain” means **no inference-time retrain when target/risk changes**.  
It does **not** mean “never train a policy.”  
Untrained frozen stubs are a defect (corrected by A14).
