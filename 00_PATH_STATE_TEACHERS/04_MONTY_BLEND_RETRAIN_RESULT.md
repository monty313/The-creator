# Path-state retrain + Monty HTF blend — lab result

**Date:** 2026-08-09  
**Process:** same as this folder (harvest → train → measure)  
**Plus:** `monty_htf_blend=True` (slope + CCI/RSI HTF force + source flags)  
**Promote:** **No** — shadow only  

---

## What we did (simple)

```text
1. Harvest  →  brain WAIT + Mark fire, under blend HTF force
2. Train    →  warmstart champion + path-state teachers offline
3. Measure  →  same 16 days:
                 champ  = slope only (production style)
                 shadow = new weights + blend ON
```

---

## Harvest

| Field | Value |
|-------|------:|
| Days | 16 |
| Teachers kept | **46** |
| London / NY | **46 / 46** |
| Full 176-dim | **yes** |
| Blend on harvest | **yes** |

Pack: `evidence_court/artifacts/path_state_teachers_monty_blend.json`

*(Fewer teachers than CASE-0037’s 400 — shorter window + fewer wait-misses.)*

---

## Train

| Field | Value |
|-------|--------|
| Start from | production champion (meta4275) |
| End | shadow **meta4567** |
| Weights changed | **yes** |
| Shadow file | `meta_policy_pathstate_monty_blend.npz` |

---

## Dual (16 days, seed 42)

| Metric | Champ (slope) | Shadow (blend) | Change |
|--------|--------------:|---------------:|-------:|
| **a13_frac** | 43.8% | **68.8%** | **+25 pts** |
| **silent days** | 4 | **2** | **−2** |
| mean trades/day | 11.9 | **22.1** | **+10** |
| total trades | 190 | **353** | **+163** |
| hits | 1 | 1 | 0 |
| mean day PnL % | **2.61** | 2.40 | **−0.21** |
| green days | 4 | 4 | 0 |
| breach | 0 | **0** | safe |

**Control:** shadow weights + slope-only edge looked almost like the champ (a13 43.8%).  
So the **big density jump needs blend on at prove**, not only retrain.

---

## Verdict

**SHADOW_MIXED**

| Better | Worse / flat |
|--------|----------------|
| A13 density | Hits flat |
| Fewer silent days | Mean PnL slightly lower |
| More trades | — |
| Breach still 0 | Not promote-ready |

**Plain English:**  
Retrain + blend still improves **how often** the bot trades (scalping band).  
It did **not** improve **target clears**.  
Mean PnL dipped a little vs champ on this short window.

---

## Compared to blend *without* retrain (earlier 20d test)

| | Blend ON, old weights | Blend + path-state retrain (this) |
|--|----------------------:|----------------------------------:|
| a13 lift | +20 pts (20d) | +25 pts (16d) |
| mean PnL | +1.0 | −0.2 |
| hits | flat | flat |

Retrain on **46** teachers kept the density story; did not beat the earlier “blend only” PnL tick.  
More harvest days / more teachers may help.

---

## Files

| File | Role |
|------|------|
| `artifacts/path_state_teachers_monty_blend.json` | Teacher pack |
| `artifacts/meta_policy_pathstate_monty_blend.npz` | Shadow brain |
| `artifacts/path_state_monty_blend_train_report.json` | Full report |
| `meta_rl/train_path_state_monty_blend.py` | Pipeline |

Re-run:

```bash
python -m evidence_court.meta_rl.train_path_state_monty_blend --harvest-days 30 --dual-days 20
```

---

## Rule (still true)

- **Do not** replace champion yet  
- Need longer dual + Court before PROMOTE  
- Path-state process = real visited states only (no F-025 rebuild)
