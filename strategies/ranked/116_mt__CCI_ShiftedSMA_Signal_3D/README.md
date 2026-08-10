# Rank 116: `mt__CCI_ShiftedSMA_Signal_3D`

**Title:** CCI_ShiftedSMA_Signal_3D

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: CCI_ShiftedSMA_Signal_3D (.mq5)`

**Score:** 63.9178

**PF / Return% / MaxDD% / Trades:** 0.676 / -2.799 / 3.434 / 3086

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__CCI_ShiftedSMA_Signal_3D`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 116 |
| Score | 63.9178 |
| Win rate % | 42.5614 |
| Profit factor | 0.6758 |
| Total return % | -2.7991 |
| Max DD % | 3.4338 |
| Trades | 3086 |
| Sharpe | -10.4777 |
| Sortino | -14.4268 |
| Calmar | -6.7522 |
| Profile | `ati_sma` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 49 |
| Win rate % | 71.8321 |
| Baseline WR % | 42.5614 |
| Trades | 857 |
| Total return % | -0.5250 |
| Max DD % | 1.0694 |
| Profit factor | 0.8714 |
| Sharpe | -2.4959 |
| Score | 86.3477 |
| Tier | `A_first_breath` |
| Profile | `ati_sma` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__CCI_ShiftedSMA_Signal_3D.md`](../tweaks/mt__CCI_ShiftedSMA_Signal_3D.md)

Tier params:

| Param | Value |
|-------|------:|
| tp | 0.00025 |
| sl | 0.001 |
| hold | 0 |
| session | True |
| strength | True |
| structure | True |

### 3) Monte Carlo (bootstrap + order-shuffle)

**MC rank:** **76** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 857 |
| Mean trade return | -0.004937% |
| Hist terminal | 0.958407× |
| Hist max DD | 4.5036% |
| MC median terminal | 0.957473× |
| MC mean terminal | 0.957783× |
| MC p05 / p95 | 0.927847× / 0.986828× |
| P(loss) | 98.90% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 4.8536% |
| Shuffle median terminal | 0.958407× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
