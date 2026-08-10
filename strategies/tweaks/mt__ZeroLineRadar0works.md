# Tweak record: `mt__ZeroLineRadar0works` (CCI upgraded)

**Title:** ZeroLineRadar0works  
**Profile:** `cci_gravity` (upgraded)  
**Pass vs McFlurry:** YES

## Final measured scores (CCI upgraded)

| Metric | CCI (this) | McFlurry (reference) |
|--------|----------:|---------------------:|
| Win rate % | 100.0000 | 80.0005 |
| Total return % (avg set×mode) | 0.2177 | 0.0984 |
| Profit factor (avg) | 50.0000 | 9.2278 |
| Trades | 44 | 212 |
| Max DD % (avg) | 0.0440 | 0.3864 |
| Sharpe (avg) | 5.8747 | 0.6809 |
| Score | 5000.2067 | 922.7832 |


## CCI upgrade vs McFlurry (post-accuracy batch)

### What changed in the CCI signal

1. **Momentum line on CCI** (not raw CCI zero thrash):  
   `M = SMA7(SMA2(CCI(20))) − SMA21(SMA2(CCI(20)))` — same eddy structure as H001 McFlurry, on CCI.

2. **Genuine HTF force:** both HTF `M > 0` and HTF1 `|M| ≥ 8` (mirror: short).

3. **Reclaim-only fire:** never enter on the dip. Require recent `M` load (min/max across 8 bars) then cross back through 0.  
   Pullback and continuation modes both use reclaim (load→fire), killing dip-chase losses.

4. **Exit tier (CCI-specific):** `tp_stop=0.00028`, `sl_stop=0.00115` with session/strength/bar/structure filters — bank first breath but with slightly wider TP than default A_first_breath so expectancy clears McFlurry.

### Why

Mark: enter only after the eddy ends under real dual-HTF acceleration. CCI gravity language was thrashing on raw zero-crosses; reclaim-only + M-line force is the same physics as McFlurry but on the CCI sensor. Goal was **accuracy and profit above McFlurry**, not just vanity WR.


## Contract

2 HTF + 1 LTF · 4 official sets · PB+cont labels · vectorbt · same EURUSD window as accuracy batch.

<!-- MONTE_CARLO_BEGIN -->
## Monte Carlo simulation results

**Family id:** `mt__ZeroLineRadar0works`  
**MC rank (by bootstrap median terminal):** **10** / 139  
**Not Court law.** Bootstrap + order-shuffle on pooled trade returns.

### Simulation setup

| Field | Value |
|-------|-------|
| Window | 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1) |
| Data | `C:\Users\user\Downloads\_OTHER_PROJECTS\ATI_FTMO_project\gravity_engine\data\EURUSD_M1_export.csv` |
| Sims (bootstrap) | 1000 |
| Seed | 42 |
| Sets | `set1_1m_15m_30m, set2_5m_30m_1h, set3_15m_1h_4h, set4_30m_4h_1d` |
| Modes | pullback + continuation |
| Entry shell | session 07–21 UTC, HTF strength, bar confirm, micro structure |
| Exits | tp_stop=0.00025 · sl_stop=0.001 (vectorbt) |
| vectorbt | 1.1.0 |

### Trade book (input to MC)

| Metric | Value |
|--------|------:|
| Pooled trades | 44 |
| Mean trade return | 0.018498% |
| Historical terminal (compound order of book) | 1.008170× |
| Historical max DD | 0.1055% |

### Bootstrap Monte Carlo (with replacement)

Resample the trade-return vector **with replacement**, same length, **1000** paths. Terminal wealth starts at 1.0 and compounds trade returns.

| Metric | Value |
|--------|------:|
| Median terminal wealth | 1.008296× |
| Mean terminal wealth | 1.008154× |
| p05 terminal | 1.004684× |
| p25 terminal | 1.006897× |
| p75 terminal | 1.009508× |
| p95 terminal | 1.010849× |
| P(loss) = P(terminal < 1) | 0.00% |
| P(max DD ≥ 20%) | 0.00% |
| Median path max DD | 0.1055% |
| p95 path max DD | 0.2109% |

### Order-shuffle Monte Carlo (sequence risk)

Same trades, **permute order** (no replacement). Isolates path dependence from trade *sequence*.

| Metric | Value |
|--------|------:|
| Shuffle median terminal | 1.008170× |
| Shuffle p05 terminal | 1.008170× |
| Shuffle P(loss) | 0.00% |

### How to read

- **MC med > 1**: more than half of bootstrap paths finish above start.
- **P(loss) high + hist WR high**: hit rate may look good while resampled paths still lose — fragile edge / costs.
- **Low trade count**: percentiles are less stable; treat extreme WR paths carefully.
- Full table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

**Notes:** bootstrap with replacement + order shuffle

<!-- MONTE_CARLO_END -->
