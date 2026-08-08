# ROAD FOR THE POLICY — permanent orientation (Monty)

**Status:** BINDING ORIENTATION for Court, loop workers, and Creator  
**Companion laws:** A14 (meta-policy **must be trained**), A2 (no retrain **at inference**), A13 (scalping 8–400), A10 (Court)

---

## The point

These policies **get their weights from training** (A14).  
Your job is **not** to hand-author a brittle rule tree that “is” the bot.

Your job is to **make the policy’s job easy**:

> Build a **road** for it to drive on.  
> **Do not** build a road that leads off a **cliff**.

---

## Road (build these)

| Piece | Meaning |
|-------|---------|
| **Honest state** | Goal/risk in context (non-saturating); Mark eyes (sets law, A12 completed HTF); L2L roles not name memorization |
| **Trainable curriculum** | Multi target×risk episodes offline; `meta-train` improves champion; frozen only at prove/forward |
| **Clear rails** | Daily risk envelope hard; leverage 1:100 math; no look-ahead; declared friction |
| **Learnability** | Dense enough path (A13) with **real edges**, not pad; stable labels / reward that don’t thrash; side from state not oracles |
| **Feedback** | Scoreboard that the meta map can improve on (clear %, breach 0, goal progress) |

If the trained policy can’t see the goal, can’t get clean R, or is gated into silence, the road is broken.

---

## Cliff (do not pave these as “the bot”)

| Cliff | Why it kills learning / final boss |
|-------|-------------------------------------|
| Untrained seed stub as production | No weights that generalize (A14 defect) |
| Full-size multi-symbol thrash on dense clock | Noise labels; A13 without conversion (F-017) |
| Exit floors that scratch runners | Kill R the policy needs to clear (F-011…) |
| Gate-only shrink (fewer fires) | Hides failure as “safe”; starves gradient/signal (F-014) |
| Bundled confounds (two levers one case) | Can’t learn which part of the road worked (F-016) |
| Path that structurally can’t hit ≥8 trades | A13 non-compliant; incomplete flea-jar (F-015) |
| Invented dials without Court | Road built off-map (F-007) |

**Cliff pattern:** optimize a handcrafted day path until the **number** looks good for one lever while the **learner** has nothing stable to fit.

---

## Court implication (issue cycle)

When goal is not achieved, Judge ranks issues. Prefer issues that are **road failures** over **more cliff dials**:

1. Can the policy be **trained** and loaded for every forward? (A14)  
2. Is state + fill **honest** (no look-ahead, no force oracle)?  
3. Is there **enough clean opportunity** (pullbacks/continuations, A13 capacity without pad)?  
4. Is the dual (clears + A13) a **road geometry** problem (hold, residual, curriculum) — not another thrash gate?  

Then try **biggest → smallest** under A10.  
**Do not** open a case whose only product is a clever cliff.

---

## One sentence for every fire

> Does this change make the **trained meta-policy’s** job easier on a **safe, honest** road — or does it pave a path off a cliff?
