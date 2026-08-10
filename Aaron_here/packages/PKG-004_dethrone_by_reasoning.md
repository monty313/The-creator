# PKG-004 — Dethrone by fixing reasoning (not instructions alone)

**Teacher:** Aaron (@Aaron_here)  
**Goal:** Fix policy *reasoning* (Force→Load→Reclaim) so floor dual can beat CASE-0037  
**Student:** MetaBrain warmstart meta4275 + Monty EO intelligent size-up at path  

---

## Method first

| Shape | Student must do |
|-------|-----------------|
| Force | Wait if multi-set incomplete / conflict |
| Load | Wait while tension builds (no dip-chase fire) |
| Reclaim | Fire **with** Force on launch/cont — this is the clear skill |
| Objective | Size under risk rails toward remaining target (EO) |

**Fail of prior loops:**  
- Path-copy alone → hits flat  
- Size-up alone → hits↑ a13↓  
- FLR wait-heavy → a13 collapse  

**This package balance:** path density foundation → staged FLR (reclaim **55%**) → density seal → short FLR → micro path. Dual with EO size-up live.

```text
Reason:  Force? → Load? → Reclaim? → FIRE
Density: path anchors keep A13 alive
Size:    EO intelligent under envelope (breach 0)
Measure: forward100 vs floor hits>11 · a13≥0.64 · n_zero≤18
```

## curriculum

1. Outcome-tagged path anchors (real states)  
2. Staged FLR (method) reclaim-weighted  
3. Path seal + FLR seal + micro path  
4. Freeze  
5. Floor dual — promote only if dethrone_decision true  

## honesty

Vanity 20d lift is not dethrone. Report blockers if a13 or hits fail.

## stage_recommendation

Run `python -m evidence_court.meta_rl.train_aaron_reason --floor-dual --flr-steps 4500`
