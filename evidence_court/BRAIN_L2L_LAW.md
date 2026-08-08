# BRAIN + LEARN-TO-LEARN LAW — PERMANENT (Monty — no Judge required)

**Law id:** **A29**  
**Status:** PERMANENT OWNER ORDER  
**Human:** Monty — fix now. No Court delay.

---

## THE LAW

1. **We need a brain.** Production decisions are driven by a **trained learn-to-learn meta-brain**, not a pile of hard if-rules.  
2. **Learn to learn** is permanent: roles/topology transfer across renames, family swaps, novel compositions — not memorized indicator recipes.  
3. **No hard-rule production path** as the decider. Market structure (Mark HTF+LTF sensors) **feeds the state**; the **brain** chooses wait / long / short / size.  
   - Only **hard** remain: **risk envelope / breach 0**, no look-ahead, Mark observation layout.  
4. **London / New York:** there are **plenty** of pullback/continuation opportunities for **≥8 trades**. Low trade count in that band is **no excuse** — training + brain must capture them (A13 + A28 watch).  
5. **Training must be real and good** — multi-target, multi-risk, L2L transfer drills, opportunity-fire drills (esp. London/NY). Thin synthetic stubs are not “a trained policy.”  
6. **No-retrain at inference** still holds: after offline train, target/risk changes use **context**, not a new full retrain.

---

## Code

| Piece | Path |
|-------|------|
| Brain | `meta_rl/brain.py` — multi-layer meta net + L2L train |
| Policy API | `meta_rl/policy.py` — wraps trained brain |
| Path | `goal_path.py` — `brain_drives=True` (default) |
| Champion | `artifacts/meta_policy_champion.npz` (retrain after this law) |
| CLI | `python -m evidence_court.meta_rl.cli meta-train --steps 8000` |

---

## Forbidden

- Shipping **untrained** weights  
- Calling linear prior + hard gates “the brain”  
- Excusing &lt;8 trades in London/NY as “no opportunity”  
- Retraining at prove when Monty changes target/risk  

---

## Immutable

Permanent until Monty supercedes. Silent return to hard-rule-only path is a defect.
