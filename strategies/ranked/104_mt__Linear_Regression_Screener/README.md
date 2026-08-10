# Rank 104: `mt__Linear_Regression_Screener`

**Title:** Linear_Regression_Screener

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: Linear_Regression_Screener (.mq5)`

**Score:** 70.1264

**PF / Return% / MaxDD% / Trades:** 0.714 / -0.899 / 1.340 / 1043

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__Linear_Regression_Screener`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 104 |
| Score | 70.1264 |
| Win rate % | 42.8944 |
| Profit factor | 0.7136 |
| Total return % | -0.8994 |
| Max DD % | 1.3401 |
| Trades | 1043 |
| Sharpe | -4.6933 |
| Sortino | -6.2203 |
| Calmar | -5.6220 |
| Profile | `linreg` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 117 |
| Win rate % | 70.7195 |
| Baseline WR % | 42.8944 |
| Trades | 251 |
| Total return % | -0.2416 |
| Max DD % | 0.4290 |
| Profit factor | 0.4524 |
| Sharpe | -1.7668 |
| Score | 44.8959 |
| Tier | `A_first_breath` |
| Profile | `linreg` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__Linear_Regression_Screener.md`](../tweaks/mt__Linear_Regression_Screener.md)

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

**MC rank:** **34** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 251 |
| Mean trade return | -0.007755% |
| Hist terminal | 0.980664× |
| Hist max DD | 2.0091% |
| MC median terminal | 0.981366× |
| MC mean terminal | 0.981223× |
| MC p05 / p95 | 0.963568× / 0.998274× |
| P(loss) | 96.40% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 2.2839% |
| Shuffle median terminal | 0.980664× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
