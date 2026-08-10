# Rank 98: `mt__FTMO_Challenge_EA_FULL`

**Title:** FTMO_Challenge_EA_FULL

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_Challenge_EA_FULL (.mq5)`

**Score:** 72.3862

**PF / Return% / MaxDD% / Trades:** 0.754 / -2.326 / 2.667 / 2998

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__FTMO_Challenge_EA_FULL`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 98 |
| Score | 72.3862 |
| Win rate % | 42.5647 |
| Profit factor | 0.7538 |
| Total return % | -2.3264 |
| Max DD % | 2.6675 |
| Trades | 2998 |
| Sharpe | -7.9279 |
| Sortino | -11.0261 |
| Calmar | -7.1459 |
| Profile | `challenge` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 128 |
| Win rate % | 69.4649 |
| Baseline WR % | 42.5647 |
| Trades | 1172 |
| Total return % | -0.9494 |
| Max DD % | 1.4066 |
| Profit factor | 0.7201 |
| Sharpe | -4.3310 |
| Score | 70.7071 |
| Tier | `A_first_breath` |
| Profile | `challenge` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__FTMO_Challenge_EA_FULL.md`](../tweaks/mt__FTMO_Challenge_EA_FULL.md)

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

**MC rank:** **137** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 1172 |
| Mean trade return | -0.006537% |
| Hist terminal | 0.926002× |
| Hist max DD | 7.9880% |
| MC median terminal | 0.925601× |
| MC mean terminal | 0.926256× |
| MC p05 / p95 | 0.892565× / 0.962685× |
| P(loss) | 99.80% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 8.0165% |
| Shuffle median terminal | 0.926002× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
