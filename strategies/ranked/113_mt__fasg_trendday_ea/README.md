# Rank 113: `mt__fasg_trendday_ea`

**Title:** fasg_trendday_ea

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: fasg_trendday_ea (.mq5)`

**Score:** 66.9106

**PF / Return% / MaxDD% / Trades:** 0.717 / -3.761 / 4.207 / 4559

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__fasg_trendday_ea`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 113 |
| Score | 66.9106 |
| Win rate % | 40.4861 |
| Profit factor | 0.7172 |
| Total return % | -3.7609 |
| Max DD % | 4.2065 |
| Trades | 4559 |
| Sharpe | -11.2213 |
| Sortino | -15.5247 |
| Calmar | -6.4855 |
| Profile | `fasg` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 122 |
| Win rate % | 70.4794 |
| Baseline WR % | 40.4861 |
| Trades | 1403 |
| Total return % | -0.9186 |
| Max DD % | 1.3544 |
| Profit factor | 0.8442 |
| Sharpe | -3.2838 |
| Score | 83.1664 |
| Tier | `A_first_breath` |
| Profile | `fasg` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__fasg_trendday_ea.md`](../tweaks/mt__fasg_trendday_ea.md)

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

**MC rank:** **130** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 1403 |
| Mean trade return | -0.005261% |
| Hist terminal | 0.928544× |
| Hist max DD | 7.2840% |
| MC median terminal | 0.929340× |
| MC mean terminal | 0.929148× |
| MC p05 / p95 | 0.891275× / 0.966302× |
| P(loss) | 99.60% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 7.7912% |
| Shuffle median terminal | 0.928544× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
