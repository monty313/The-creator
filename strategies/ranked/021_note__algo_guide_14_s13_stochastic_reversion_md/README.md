# Rank 21: `note__algo_guide_14_s13_stochastic_reversion_md`

**Title:** s13_stochastic_reversion.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s13_stochastic_reversion.md`

**Score:** 88.9215

**PF / Return% / MaxDD% / Trades:** 0.933 / -3.243 / 4.615 / 6708

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s13_stochastic_reversion_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 21 |
| Score | 88.9215 |
| Win rate % | 49.3553 |
| Profit factor | 0.9332 |
| Total return % | -3.2426 |
| Max DD % | 4.6150 |
| Trades | 6708 |
| Sharpe | -7.6406 |
| Sortino | -10.3170 |
| Calmar | 1.2581 |
| Profile | `guide_s13_stoch_mr` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 103 |
| Win rate % | 70.9957 |
| Baseline WR % | 49.3553 |
| Trades | 408 |
| Total return % | -0.3801 |
| Max DD % | 0.6676 |
| Profit factor | 0.8476 |
| Sharpe | -2.5872 |
| Score | 84.2163 |
| Tier | `A_first_breath` |
| Profile | `guide_s13_stoch_mr` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s13_stochastic_reversion_md.md`](../tweaks/note__algo_guide_14_s13_stochastic_reversion_md.md)

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

**MC rank:** **44** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 408 |
| Mean trade return | -0.007497% |
| Hist terminal | 0.969786× |
| Hist max DD | 3.3605% |
| MC median terminal | 0.970183× |
| MC mean terminal | 0.970185× |
| MC p05 / p95 | 0.947893× / 0.992086× |
| P(loss) | 98.80% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 3.3861% |
| Shuffle median terminal | 0.969786× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
