# HTF blend dual result (lab)

**Date:** 2026-08-08  
**Test:** Same frozen champion, same 20 days, same target×risk schedule  
**Only change:** `monty_htf_blend` OFF vs ON  
**Not a PROMOTE** — weights were **not** retrained on the new force/flags  

**Full JSON:** `htf_blend_dual_compare.json`  
**Runner:** `python -m evidence_court.meta_rl.htf_blend_dual_compare --days 20`

---

## Verdict

**BLEND_BETTER** on this 20-day window  
(better density + mean PnL + fewer silent days; hits flat; breach still 0)

---

## Scoreboard

| Metric | Slope only (OFF) | Blend ON | Change |
|--------|-----------------:|---------:|-------:|
| **hit rate** | 10% (2/20) | 10% (2/20) | 0 |
| **low_hr** (target ≤15) | 33% | 33% | 0 |
| **a13_frac** (8–400 trades/day) | **40%** | **60%** | **+20 pts** |
| **silent days (0 trades)** | 5 | **2** | **−3** |
| **mean trades/day** | 11.7 | **25.7** | **+14** |
| **total trades** | 234 | **513** | **+279** |
| **mean day PnL %** | 4.50 | **5.50** | **+1.0** |
| **green days** | 7 (35%) | **8 (40%)** | +1 day |
| **breach** | 0 | **0** | held |
| max day PnL | 48.9 | 46.6 | −2.2 |
| min day PnL | −3.0 | −3.0 | ~same |

---

## Plain English

With the **same brain weights**:

- Blend made the bot **trade more often** (good for A13 scalping band).  
- **Fewer dead days.**  
- **Average day PnL a bit higher.**  
- **Did not hit target more often** (still 2/20 clears).  
- **Still safe** (no risk breach).

So: **better activity / density road**, not yet a conversion (hits) breakthrough.

---

## Caveats (honest)

1. **20 days only** — not full 100-day dual.  
2. Champion was trained on **slope-only** force; blend changes candidates the frozen brain sees.  
3. Doctrine flags 12–14 are new; this brain barely “learned” them.  
4. More trades ≠ always smarter — but here mean PnL and green days also ticked up.  
5. **Not production law** until longer dual + retrain option + Court.

---

## Suggested next

| Step | Why |
|------|-----|
| Longer dual (e.g. 50–100d) | Confirm not luck on 20d |
| Shadow retrain **with blend on** | Teach brain the new wind + flags |
| Then dual again | Fair “learned blend” vs slope champ |
| Court if floor improves | PROMOTE path |

Re-run:

```bash
python -m evidence_court.meta_rl.htf_blend_dual_compare --days 20 --seed 42
# fixed pair:
python -m evidence_court.meta_rl.htf_blend_dual_compare --days 20 --target 15 --risk 2
```
