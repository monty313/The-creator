# Rank 108: `mt__AutoGKCloseIntegral`

**Title:** AutoGKCloseIntegral

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: AutoGKCloseIntegral (.mq5)`

**Score:** 68.8368

**PF / Return% / MaxDD% / Trades:** 0.740 / -3.945 / 4.797 / 4675

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__AutoGKCloseIntegral`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 108 |
| Score | 68.8368 |
| Win rate % | 40.4012 |
| Profit factor | 0.7398 |
| Total return % | -3.9453 |
| Max DD % | 4.7972 |
| Trades | 4675 |
| Sharpe | -12.5015 |
| Sortino | -17.0826 |
| Calmar | -5.2295 |
| Profile | `ma_sample` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 52 |
| Win rate % | 71.5070 |
| Baseline WR % | 40.4012 |
| Trades | 1153 |
| Total return % | -0.6512 |
| Max DD % | 1.3318 |
| Profit factor | 0.7472 |
| Sharpe | -3.3836 |
| Score | 73.7394 |
| Tier | `A_first_breath` |
| Profile | `ma_sample` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__AutoGKCloseIntegral.md`](../tweaks/mt__AutoGKCloseIntegral.md)

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

**MC rank:** **80** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 1153 |
| Mean trade return | -0.004523% |
| Hist terminal | 0.948933× |
| Hist max DD | 5.2312% |
| MC median terminal | 0.949154× |
| MC mean terminal | 0.949558× |
| MC p05 / p95 | 0.912134× / 0.986433× |
| P(loss) | 99.00% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 5.8389% |
| Shuffle median terminal | 0.948933× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
