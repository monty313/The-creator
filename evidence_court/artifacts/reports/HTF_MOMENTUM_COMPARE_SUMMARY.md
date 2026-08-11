# HTF momentum compare — summary (experimental)

**Status:** lab measure only. Does **not** change the champion edge.  
**Report JSON:** `htf_momentum_compare_report.json`  
**Code:** `evidence_court/meta_rl/htf_momentum_compare.py`  
**Window:** ~90 calendar days · XAUUSD / EURUSD / GBPUSD · official sets  

---

## 1) How Court **slope** is calculated (exact)

On one higher timeframe, using **completed closes** only:

```text
lookback = 5 bars

a = close from 5 bars before the current bar
b = current completed close

ret   = (b - a) / |a|
score = clip(ret × 50,  into range -1 … +1)
```

| score | meaning |
|------:|---------|
| > 0 | price up over those 5 HTF bars |
| < 0 | price down |
| near 0 | weak / flat |

### Two HTFs of one official set

```text
f1 = score on HTF1
f2 = score on HTF2

agree = (same sign) AND |f1| ≥ 0.12 AND |f2| ≥ 0.12
force = (f1 + f2) / 2
if not agree: force = force × 0.35

STRONG bull (this study): agree AND force ≥ +0.20
STRONG bear (this study): agree AND force ≤ -0.20
```

This slope score is what production edge uses as **HTF force** (with the agree rule).

It is **not** SMA structure. It is **recent return**, scaled.

---

## 2) Monty definitions (as tested)

### Condition 1 — CCI + Bollinger (both HTFs)

- CCI periods **10, 30, 100**
- On each CCI: Bollinger **period 10, dev 0.5** (mid = SMA of that CCI)
- **Strong bull:** all 3 CCI **above** their BB mid on **both** HTFs  
- **Strong bear:** all 3 CCI **below** their BB mid on **both** HTFs  

### Condition 2 — RSI + Bollinger (both HTFs)

- RSI periods **5, 15**
- On each RSI: BB **10, 0.5**
- **Bull:** both RSI **above** BB mid on **both** HTFs  
- **Bear:** both RSI **below** BB mid on **both** HTFs  

### Strong trending market (Monty)

**Condition 1 OR Condition 2** active (same side).

---

## 3) What we measured

| Metric | Meaning |
|--------|---------|
| **Predictive hit rate (fwd5)** | When strong bull/bear is on, does price move that way over the **next 5 HTF2 bars**? |
| **Coverage** | How often the signal is on |
| **Trade proxy** | Strong HTF side **and** LTF RSI5+BB same-side fire → win if next 5 HTF bars agree |

---

## 4) Aggregate results (this run)

| Method | Pred. hit (fwd5) | Coverage | Trade proxy win | Trade n | Mean proxy pnl |
|--------|-----------------:|---------:|----------------:|--------:|---------------:|
| **slope** (Court) | 0.477 | 0.136 | 0.472 | 1830 | ~0.00012 |
| **CCI+BB (cond1)** | **0.489** | 0.372 | 0.468 | 1249 | ~0.00044 |
| **RSI+BB (cond2)** | 0.486 | 0.572 | 0.473 | 1639 | ~0.00016 |
| **Monty OR (1 or 2)** | 0.488 | **0.607** | **0.473** | 1671 | ~0.00015 |

**Winner predictive (this run):** `cci_bb_cond1` (slight edge)  
**Winner trade proxy (this run):** `monty_or_cond1_or_cond2` (tiny edge on win rate)

---

## 5) Plain-English reading

- All methods sit near **~48–49%** predictive hit on 5-bar HTF forward moves → **none is a magic crystal ball** on this window.  
- **Slope** is **rarest** (coverage ~14%) — strict.  
- **Monty OR** is **on most often** (~61%).  
- **CCI cond1** edges predictive hit and best mean proxy pnl in this sample.  
- Differences are **small** — need more days / Court case before replacing production force.

---

## 6) Re-run

```bash
python -m evidence_court.meta_rl.htf_momentum_compare --days 90
python -m pytest evidence_court/tests/test_htf_momentum_compare.py -q
```

---

## 7) Production note

Champion edge still uses **slope force** until a Full Court case measures a swap and PROMOTE.
