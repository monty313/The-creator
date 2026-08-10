# Rank 120: `mt__FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323`

**Title:** FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323 (.mq5)`

**Score:** 60.8905

**PF / Return% / MaxDD% / Trades:** 0.620 / -0.816 / 1.126 / 915

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 120 |
| Score | 60.8905 |
| Win rate % | 35.3054 |
| Profit factor | 0.6199 |
| Total return % | -0.8161 |
| Max DD % | 1.1260 |
| Trades | 915 |
| Sharpe | -4.5786 |
| Sortino | -6.2246 |
| Calmar | -5.0213 |
| Profile | `bb_mtf` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 12 |
| Win rate % | 75.8165 |
| Baseline WR % | 35.3054 |
| Trades | 261 |
| Total return % | 0.0360 |
| Max DD % | 0.3052 |
| Profit factor | 0.9994 |
| Sharpe | -0.3622 |
| Score | 99.9036 |
| Tier | `A_first_breath` |
| Profile | `bb_mtf` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323.md`](../tweaks/mt__FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323.md)

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

**MC rank:** **17** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 261 |
| Mean trade return | 0.001089% |
| Hist terminal | 1.002797× |
| Hist max DD | 1.3071% |
| MC median terminal | 1.003846× |
| MC mean terminal | 1.003588× |
| MC p05 / p95 | 0.987117× / 1.018753× |
| P(loss) | 34.10% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 0.9430% |
| Shuffle median terminal | 1.002797× |
| Shuffle P(loss) | 0.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
