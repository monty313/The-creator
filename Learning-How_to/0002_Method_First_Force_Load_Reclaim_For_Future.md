# 0002 — Method first: Force → Load → Reclaim (prep for future problems)

**Teacher:** @Aaron_here  
**Student:** any model that must act under new targets, days, sensors — **without retrain**  

---

## Why this lesson exists

Handing “take more size” or “copy this long” solves **today’s** scoreboard only.  
Future days change target%, risk%, bars, sensor noise.  

**Method-first** means: on a brand-new problem, name the same four shapes **before** you invent a trade.

---

## The method (memorize this, not a trade list)

| Name | Question | If answer is no |
|------|----------|-----------------|
| **Force** | Does higher context agree on a side? | **Wait** — no permission |
| **Load** | Is there productive tension *against* Force? | Stay ready; **do not fire yet** |
| **Reclaim** | Did structure return **with** Force? | Still wait |
| **Objective** | What remaining goal under remaining risk? | Size / exit under rails |

```text
FORCE? ──no──► WAIT
  │yes
  ▼
LOAD only? ──yes──► WAIT (loading)
  │no
  ▼
RECLAIM with Force? ──no──► WAIT
  │yes
  ▼
FIRE Force-side · size by risk rails · manage when Force dies
```

---

## How this prepares for *future* problems

| Future change | Same method |
|---------------|-------------|
| New target 70 instead of 15 | Force/Load/Reclaim still order; objective updates in **state** |
| New day never seen | Re-check Force each day; no memorized date |
| New indicator names | Roles stay Force/Load/Reclaim; sensors are coordinates |
| Stress / chop | No Force → wait (not thrash) |

**No retrain at inference** when only target/risk context changes (L2L law).

---

## Rewards and penalties (same order)

```text
1) METHOD path rewards/penalties   Force → Load → Reclaim → rails
2) GOAL context                    target / risk / scaled PnL  (small)
3) Never                           win-rate alone as the objective
```

If the method is **broken** this step → **goal candy = 0**.  
`compose_method_goal_reward` enforces that in meta-train.

## Code home (Court lab)

| Piece | Path |
|-------|------|
| Compose method+goal | `evidence_court/meta_rl/path_learning.py` → `compose_method_goal_reward` |
| FLR labels + staged train | `evidence_court/meta_rl/aaron_reason_curriculum.py` |
| Shape rewards (top-5) | `Aaron_here/tools/top5_shape_observe.py` → `shape_reward` |
| Train + dual runner | `evidence_court/meta_rl/train_aaron_reason.py` |
| Packages | `Aaron_here/packages/PKG-002…` · `PKG-005` (method first) |

---

## Honesty

EO size-up improved 100d **hits** (11→13) but not full floor (a13 dipped).  
Aaron FLR train is **method preparation**; short 20d duals have not yet beaten the king.  
Do not call that PROMOTE. Keep double-loop: train → measure → rewrite package order.
