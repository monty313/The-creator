# Rank 31: `mt__JordanMomentumScreener_v9_Wave`

**Title:** JordanMomentumScreener_v9_Wave

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: JordanMomentumScreener_v9_Wave (.mq5)`

**Score:** 82.5338

**PF / Return% / MaxDD% / Trades:** 0.856 / -2.308 / 3.024 / 3121

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__JordanMomentumScreener_v9_Wave`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 31 |
| Score | 82.5338 |
| Win rate % | 46.9550 |
| Profit factor | 0.8560 |
| Total return % | -2.3079 |
| Max DD % | 3.0242 |
| Trades | 3121 |
| Sharpe | -7.8394 |
| Sortino | -10.4937 |
| Calmar | -2.9037 |
| Profile | `jordan` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 112 |
| Win rate % | 70.8864 |
| Baseline WR % | 46.9550 |
| Trades | 882 |
| Total return % | -0.4596 |
| Max DD % | 0.8518 |
| Profit factor | 0.9412 |
| Sharpe | -1.7456 |
| Score | 93.4468 |
| Tier | `A_first_breath` |
| Profile | `jordan` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__JordanMomentumScreener_v9_Wave.md`](../tweaks/mt__JordanMomentumScreener_v9_Wave.md)

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

**MC rank:** **63** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 882 |
| Mean trade return | -0.004215% |
| Hist terminal | 0.963339× |
| Hist max DD | 4.1046% |
| MC median terminal | 0.964217× |
| MC mean terminal | 0.964897× |
| MC p05 / p95 | 0.935658× / 0.993708× |
| P(loss) | 97.70% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 4.2255% |
| Shuffle median terminal | 0.963339× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
