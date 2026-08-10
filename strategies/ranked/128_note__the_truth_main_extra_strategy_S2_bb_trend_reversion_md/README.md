# Rank 128: `note__the_truth_main_extra_strategy_S2_bb_trend_reversion_md`

**Title:** strategy_S2_bb_trend_reversion.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\the_truth_main_extra\strategy_S2_bb_trend_reversion.md`

**Score:** 59.1781

**PF / Return% / MaxDD% / Trades:** 0.609 / -1.341 / 1.529 / 1205

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__the_truth_main_extra_strategy_S2_bb_trend_reversion_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 128 |
| Score | 59.1781 |
| Win rate % | 35.5283 |
| Profit factor | 0.6090 |
| Total return % | -1.3414 |
| Max DD % | 1.5295 |
| Trades | 1205 |
| Sharpe | -7.6055 |
| Sortino | -10.1288 |
| Calmar | -8.2876 |
| Profile | `truth_s2_bb` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 39 |
| Win rate % | 72.9201 |
| Baseline WR % | 35.5283 |
| Trades | 481 |
| Total return % | -0.2396 |
| Max DD % | 0.5789 |
| Profit factor | 0.7047 |
| Sharpe | -1.0059 |
| Score | 70.0888 |
| Tier | `A_first_breath` |
| Profile | `truth_s2_bb` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__the_truth_main_extra_strategy_S2_bb_trend_reversion_md.md`](../tweaks/note__the_truth_main_extra_strategy_S2_bb_trend_reversion_md.md)

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

**MC rank:** **37** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 481 |
| Mean trade return | -0.004004% |
| Hist terminal | 0.980818× |
| Hist max DD | 2.7937% |
| MC median terminal | 0.980315× |
| MC mean terminal | 0.980578× |
| MC p05 / p95 | 0.956767× / 1.004477× |
| P(loss) | 90.60% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 2.7047% |
| Shuffle median terminal | 0.980818× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
