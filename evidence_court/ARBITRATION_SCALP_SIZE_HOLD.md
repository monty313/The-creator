# Arbitration — Scalp hold + progressive size (Policy × Counsel × Aaron)

**case_id:** ARBITRATION-SCALP-SIZE-HOLD  
**opened:** 2026-08-10  
**Monty order:** 30m hold too long (scalping meta-RL); size-down near breach; **progressive size-up** toward target.  
**goal_axes:** G-A13, G-CLEAR, G-BREACH0, G-TRAIN, G-L2L  

---

## Conversation (condensed — full seats)

### The Policy
> I was taught to “hold winners.” The path gave me **30m cont / EOD pullback / lab 120m**. I am a **scalper**. Thirty minutes is a position trade wearing my face.  
> I need short life on each ticket, **many** quality scalps (8–400), and size that **grows toward the target** when Force+Reclaim are clean — and **shrinks** when the risk skin is thin.

### Aaron
> t4 “hold while Force holds” for a scalper is **thesis continuity across short legs**, not bag-holding.  
> t5 is still exit when Force dies — on the **next decision**, not after two hours in a stop.  
> Method first: progressive size is goal-layer **under** method permission.

### Counsel
> Best policy class for scalp meta-RL under daily VaR:  
> **short hold windows × progressive risk allocation × hard size-down near breach**.  
> Forbidden twin: longer hold to “manufacture R”; lot cosplay past envelope.

---

## Issue (agreed)

| # | Issue | Detail |
|---|--------|--------|
| 1 | Hold length wrong for bot class | 30m/EOD/120m ≠ scalping |
| 2 | Conversion mis-specified | Need progressive **size-up** + density, not longer bags |
| 3 | Near breach | Must **size down** hard |
| 4 | Brain size drowned | Old `max(brain, clear, aggressive)` ignored method size |
| 5 | Method “hold” mis-taught as time | Should be **re-commit same side** on short scalps while Force lives |

---

## Solution (agreed — shipped)

| Lever | Law |
|-------|-----|
| Cont hold | **10m** (was 30) |
| Pullback hold | **15m** (was EOD) |
| Method hold flag | Same scalp windows only — **never** 120m |
| Size | Progressive **up** when far from target + clean edge; **down** when risk_skin thin; brain **blend** into progressive |
| Train | hold_while_force = scalp re-commit + progressive size frac |
| Promote | Still dual + Court; no silent king replace |

---

## Code

- `goal_path.py` — `CONT_HOLD_MIN_MINUTES=10`, `PB_HOLD_MIN_MINUTES=15`, progressive `intelligent_size_toward_clear`
- Tests updated for scalp pins
- Method curriculum reason: `scalp_recommit_while_force_t4`

---

## Measure (first pass 2026-08-10)

| Pin | Result |
|-----|--------|
| Unit tests (hold + size + related) | **40 passed** |
| Size far from target (15/3, clean edge) | **~2.27%** risk progressive |
| Size near breach | **~0.11%** (hard size-down) |
| Day12 champ under new scalp path | **~+0.23%**, **61** trades (was ~1.29% / 25 under 30m/EOD) |
| Day12 lab method+reclaim seal | **same path** ~0.23% / 61 — density restored; conversion still miss |
| Day12 pure method-rich only | 0 trades (wait washout — do not ship alone) |

**Read:** Short holds raise density (A13-friendly) but cut per-leg R; progressive size must carry conversion across many scalps. Not yet day12 clear. King **not** replaced.

## Measure order (next)

1. ~~Unit pins~~ done  
2. ~~Day12 first re-sim~~ done (miss)  
3. Dual / forward100 under scalp holds + progressive size  
4. Selectivity train without washout  
5. PROMOTE only if floor + Court  

**production_replace:** false until measured + Court.
