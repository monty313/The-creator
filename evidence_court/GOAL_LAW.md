# GOAL LAW — PERMANENT (Law A31)

**Status:** PERMANENT COURT LAW  
**Promoted:** 2026-08-07 as **Law A31** (Monty standing order)  
**SSOT mission text:** `mark_here/knowledge/lab/GOAL.md`  
**Machine pin:** `GOAL_LAW.json` · test: `tests/test_goal_law.py`

This law is the **north star of every Court action**. The legal process does not exist for its own sake. It exists **only** to produce and improve **one bot** that meets the mission. If a case, docket item, or process change cannot be mapped to a goal gap, it is **out of Court**.

---

## The mission (immutable wording)

**Build and improve one bot that solves for whatever target % and risk % Monty types in — without having to retrain after the final policy is created.**

| Constraint | Rule |
|------------|------|
| **Target %** | Daily profit goal at inference — range **[5, 90]** |
| **Risk %** | Daily max loss floor at inference — range **[1, 3]** |
| **No retrain** | Same trained weights adapt via goal/risk **context**; no gradient update when Monty changes numbers |
| **Breach** | **Must stay 0** on measured scoreboards |
| **Bot class** | **Scalper** — **MUST** land **[8, 400]** trades every day (Law **A13**) |
| **Meta-policy** | **Must be trained** (Law **A14** / **A29**); meta-learning is permanent architecture |
| **Senses** | Emergent **sight / feel / taste / hearing** on **every official timeframe set** (Law **A32**) — relative to edge and reasoning, not indicator names |

### How we know we won

| Metric | Meaning | Direction |
|--------|---------|-----------|
| **Clear %** | Days that hit typed target **and** never hit typed floor | **Climb** |
| **Breach %** | Days that hit the floor | **Stay 0** |
| **A13 day-share** | Fraction of days with trades ∈ [8, 400] | **Climb toward ~1.0** |
| **Streak** | Clears in a row at the pair under test | **Climb** |
| **L2L / senses** | Held-out role/topology + sense failure checks pass | **Required for PROMOTE** |

Final boss: multi-seed 100-forward-day matrix across target×risk, breach 0, consistent clear %, no retrain, A13 lived, senses not probe-only → `FINAL_BOT_SPEC.md`.

---

## Goal axes (every issue must map to at least one)

When the Judge builds or refreshes the docket, **every open issue** must declare one or more of:

| axis_id | Name | Blocks when missing |
|---------|------|---------------------|
| **G-NO_RETRAIN** | Goal/risk context generalization | Weights update when pair changes; frozen stub |
| **G-BREACH0** | Risk envelope integrity | Any breach day |
| **G-CLEAR** | Target hit / dual conversion | Low hits / low_hr on random pairs |
| **G-A13** | Scalping cadence density | Days outside [8,400] trades |
| **G-L2L** | Learn-to-learn (roles/topology) | Act-copy only / COPYING_FAIL |
| **G-SIGHT** | Structure perception | Flat on bread-and-butter pullback days |
| **G-FEEL** | Relational tension | Lone oscillator fires / freeze on load |
| **G-TASTE** | Edge quality + goal/risk pressure | All bars equal / marginal high-target fires |
| **G-HEAR** | Regime / day-story / wait skill | Thrash reverse / stale story |
| **G-TRAIN** | Serious meta curriculum + champion | Untrained prior as production |
| **G-LONG** | Multi-seed multi-window honesty | Single-seed vanity |
| **G-ONEBOT** | Single champion prove path | Dual silent brains |

---

## Court binding rules under A31

1. **No freestyle cases.** Every case sets `goal_axes: [...]` and `blocks_metric` from measured gaps.  
2. **Biggest goal gap first.** Rank docket by how much the issue blocks final-boss metrics (breach > clear > A13 > senses-as-probes > polish).  
3. **After every verdict:** re-measure scoreboard → regenerate issues that are **still relevant to the goal** → drop issues that no longer block the goal → open next rank-1.  
4. **Process keeps going** until final boss PROMOTE + empty blocker docket. Court is not optional theater; it is the engine that **generates and retires** goal-relative issues.  
5. **Senses are first-class goal axes**, not optional flavor. A promote path that ignores A32 fails A31.  
6. **Road not cliff** (A14 companion): Court paves learnable road for the trained policy; handcrafted thrash that cannot be learned is forbidden as production law.

---

## What is forbidden as “progress”

- Cases that only redecorate docs while dual/A13/senses gaps stay open  
- Density via pad trades  
- Clear % via frictionless fantasy without declared costs  
- “Impossible day” without flea-jar full action space  
- PROMOTE without three opinions (A15) on production/brain/A13/dual/senses-drive changes  
- Calling the mission complete while any **G-*** blocker remains open

---

## Immutable

Append-only permanent. May only be amended by a later PROMOTE + Monty approval that supercedes A31 with a new Law id. Silent weakening is a Court defect.
