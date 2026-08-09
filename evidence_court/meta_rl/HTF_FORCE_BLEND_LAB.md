# HTF force blend lab (Monty CCI/RSI + slope)

**Status:** LAB / SHADOW — default **off** on production path  
**Does not replace champion** until Court PROMOTE + retrain dual.

---

## What was added

### Blend force (`monty_htf_blend=True`)

On each official set’s **two HTFs**:

| Source | Rule |
|--------|------|
| **Slope** (Court) | `trend_dir` lookback 5; pair agree |
| **Cond1 CCI+BB** | CCI 10/30/100 each vs BB mid 10/0.5 on **both** HTFs |
| **Cond2 RSI+BB** | RSI 5/15 each vs BB mid on **both** HTFs |
| **Monty side** | Cond1 **OR** Cond2; Cond1 vs Cond2 fight → 0 |

**Combine:**

| Case | Result |
|------|--------|
| Slope + Monty same side | Permission; force = mix |
| Monty only | Permission; force = 0.65 × side |
| Slope only | Permission (as today) |
| Slope vs Monty fight | **No** permission (weak force) |

### Doctrine source flags (brain can see wind type)

Mark doctrine is still **16 floats** at state `[32:48]`.

| Index | Flag | Meaning |
|------:|------|---------|
| 12 | `slope_on` | Court slope pair agree |
| 13 | `cci_on` | Cond1 active |
| 14 | `rsi_on` | Cond2 active |
| 15 | pad | unused |

So the model can learn *which* HTF definition is talking.

---

## Production vs lab

| Setting | Production (default) | Lab / shadow |
|---------|----------------------|--------------|
| `monty_htf_blend` | **False** | **True** |
| HTF force | Slope (+ multi-day tide) | Slope **+** Monty blend |
| Flags 12–14 | Usually 0 (or slope_on only if set later) | Real slope/cci/rsi |
| Champion weights | Unchanged path | Needs **retrain** to use flags/force well |

```python
# day path lab
fills, ledger, meta = run_goal_path_day(
    policy,
    date=...,
    m1_by_symbol=...,
    target_percent=15,
    max_daily_risk_percent=2,
    symbols=[...],
    monty_htf_blend=True,  # ← lab
)
```

```python
# edge scan only
snap = scan_all_sets(m1, symbol="XAUUSD", monty_htf_blend=True)
print(snap.slope_on, snap.cci_on, snap.rsi_on, snap.best)
```

---

## Code map

| File | Role |
|------|------|
| `meta_rl/htf_force.py` | Blend + Cond1/2 + flags |
| `meta_rl/edge.py` | `SetEdge` sources; `monty_htf_blend` on scan |
| `meta_rl/regimes.py` | `encode_regime_doctrine(..., slope_on, cci_on, rsi_on)` |
| `meta_rl/goal_path.py` | Flag on day path; packs doctrine |
| `meta_rl/policy.py` | Curriculum random source flags for retrain |
| `tests/test_htf_force_blend.py` | Unit pins |

---

## Next steps (before production)

1. Shadow dual with `monty_htf_blend=True`  
2. Offline meta-train / path-state teachers **with blend on** so weights see flags  
3. Compare floor: hits / a13 / n_zero / breach 0  
4. Full Court A10+A15 → PROMOTE only if dual improves  

**Re-run units:**

```bash
python -m pytest evidence_court/tests/test_htf_force_blend.py evidence_court/tests/test_htf_momentum_compare.py -q
```
