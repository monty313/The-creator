# Rank 13: `mt__ZeroLineRadar0works`

**Title:** ZeroLineRadar0works

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: ZeroLineRadar0works (.mq5)`

**Score:** 1305.9886

**PF / Return% / MaxDD% / Trades:** 13.075 / -1.152 / 1.552 / 1387

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__ZeroLineRadar0works`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 13 |
| Score | 1305.9886 |
| Win rate % | 52.1031 |
| Profit factor | 13.0753 |
| Total return % | -1.1519 |
| Max DD % | 1.5515 |
| Trades | 1387 |
| Sharpe | -5.1336 |
| Sortino | -6.4265 |
| Calmar | 1.1160 |
| Profile | `cci_gravity` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 34 |
| Win rate % | 73.2739 |
| Baseline WR % | 52.1031 |
| Trades | 449 |
| Total return % | -0.2725 |
| Max DD % | 0.5544 |
| Profit factor | 0.6620 |
| Sharpe | -2.4706 |
| Score | 65.7918 |
| Tier | `A_first_breath` |
| Profile | `cci_gravity` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__ZeroLineRadar0works.md`](../tweaks/mt__ZeroLineRadar0works.md)

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

**MC rank:** **10** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 44 |
| Mean trade return | 0.018498% |
| Hist terminal | 1.008170× |
| Hist max DD | 0.1055% |
| MC median terminal | 1.008296× |
| MC mean terminal | 1.008154× |
| MC p05 / p95 | 1.004684× / 1.010849× |
| P(loss) | 0.00% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 0.1055% |
| Shuffle median terminal | 1.008170× |
| Shuffle P(loss) | 0.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
