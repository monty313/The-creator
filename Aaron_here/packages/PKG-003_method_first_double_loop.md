# PKG-003 — Method-first double-loop (critique of PKG-002 train)

**Teacher:** Aaron (@Aaron_here)  
**Student:** MetaBrain (CASE-0037 warmstart)  
**Trigger:** PKG-002 train left 20d dual **identical** to baseline → method did not stick  

---

## Honesty of scores (trace)

| Window | Baseline | After PKG-002 train |
|--------|----------|---------------------|
| 20d north-star | hits 2 · a13 0.25 | hits 2 · a13 0.25 (Δ0) |

**Critique:** Process FLR was taught, then **heavy path re-anchor last** re-imposed answer-copy fire labels. Method washed. Student looked frozen-trained but behaved like the king on that window.

```text
WRONG ORDER (PKG-002 run):
  FLR process  →  path fire anchors LAST  →  dual (copy wins)

RIGHT ORDER (this package):
  light path density  →  staged FLR LAST  →  micro path  →  FLR seal  →  dual
```

---

## Method first (again — for *future* problems)

Before any new day / target / sensor set, the student must answer:

1. **Force?** Higher-context side agreement? If no → wait.  
2. **Load?** Productive tension against Force? If yes and no reclaim → wait.  
3. **Reclaim?** Resolution **with** Force? If yes → fire Force side.  
4. **Objective?** Remaining target under remaining risk (size under envelope).

Same four questions on **unseen** targets, pairs, days — **no retrain at inference**.

```text
        FORCE?
       /      \
     no        yes
     |          |
   WAIT      LOAD only?
              /     \
            yes      no → RECLAIM?
            |              /    \
          WAIT           no     yes
                         |       |
                       WAIT    FIRE + size by rails
```

---

## Curriculum stages (preparation for novelty)

| Stage | What student practices | Done when |
|------:|------------------------|-----------|
| 1 Force | Wait when no consensus / conflict | force_wait dominant on those packs |
| 2 Load | Wait on slingshot / load_building | load_wait, not thrash fire |
| 3 Reclaim | Fire only with Force + launch/BB | reclaim_fire on reclaim packs |
| 4 Mixed | Random FLR episodes | shapes cohere |
| 5 Seal | After any path anchors, short FLR again | method not washed |

## reward_sketch

- **Process first:** high reward for correct shape (wait on load, fire on reclaim).  
- **Not:** “copy Mark long because path-state said so” as the only diet.  
- Path anchors: sparse, never last without FLR seal.

## positive / negative

| + | − |
|---|---|
| Dual Force + reclaim fire | Fire with no Force |
| Load wait then reclaim | Fire on load bottom |
| Same method new target% | Path-only wash after FLR |

## stage_recommendation

**Advance to staged FLR-last train** (`train_aaron_reason` recipe v2).  
Do **not** claim PROMOTE from 20d vanity. Re-measure 20d; if process shapes stick, then longer dual.

## Self-critique rule

Every train report with Δ≈0 → rewrite order (this package). Double-loop mandatory.
