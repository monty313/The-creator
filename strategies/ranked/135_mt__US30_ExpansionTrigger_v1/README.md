# Rank 135: `mt__US30_ExpansionTrigger_v1`

**Title:** US30_ExpansionTrigger_v1

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: US30_ExpansionTrigger_v1 (.mq5)`

**Score:** 42.6705

**PF / Return% / MaxDD% / Trades:** 0.438 / -0.819 / 1.247 / 1163

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__US30_ExpansionTrigger_v1`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 135 |
| Score | 42.6705 |
| Win rate % | 25.3811 |
| Profit factor | 0.4380 |
| Total return % | -0.8194 |
| Max DD % | 1.2468 |
| Trades | 1163 |
| Sharpe | -4.4561 |
| Sortino | -6.1215 |
| Calmar | -5.1440 |
| Profile | `momentum` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 138 |
| Win rate % | 69.1404 |
| Baseline WR % | 25.3811 |
| Trades | 351 |
| Total return % | -0.4081 |
| Max DD % | 0.5327 |
| Profit factor | 12.6861 |
| Sharpe | -2.1804 |
| Score | 1268.0638 |
| Tier | `A_first_breath` |
| Profile | `momentum` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__US30_ExpansionTrigger_v1.md`](../tweaks/mt__US30_ExpansionTrigger_v1.md)

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

**MC rank:** **52** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 351 |
| Mean trade return | -0.009325% |
| Hist terminal | 0.967718× |
| Hist max DD | 3.5107% |
| MC median terminal | 0.968205× |
| MC mean terminal | 0.967990× |
| MC p05 / p95 | 0.948587× / 0.987059× |
| P(loss) | 99.70% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 3.5359% |
| Shuffle median terminal | 0.967718× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
