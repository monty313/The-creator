# Rank 19: `note__the_truth_main_extra_strategy_S1_cci_slingshot_md`

**Title:** strategy_S1_cci_slingshot.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\the_truth_main_extra\strategy_S1_cci_slingshot.md`

**Score:** 99.7065

**PF / Return% / MaxDD% / Trades:** 1.024 / -2.022 / 2.825 / 3210

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__the_truth_main_extra_strategy_S1_cci_slingshot_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 19 |
| Score | 99.7065 |
| Win rate % | 45.2699 |
| Profit factor | 1.0244 |
| Total return % | -2.0224 |
| Max DD % | 2.8253 |
| Trades | 3210 |
| Sharpe | -6.8939 |
| Sortino | -9.0364 |
| Calmar | -1.7249 |
| Profile | `truth_s1_cci` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 37 |
| Win rate % | 73.1980 |
| Baseline WR % | 45.2699 |
| Trades | 390 |
| Total return % | -0.3040 |
| Max DD % | 0.5560 |
| Profit factor | 13.2248 |
| Sharpe | -1.8011 |
| Score | 1322.0418 |
| Tier | `A_first_breath` |
| Profile | `truth_s1_cci` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__the_truth_main_extra_strategy_S1_cci_slingshot_md.md`](../tweaks/note__the_truth_main_extra_strategy_S1_cci_slingshot_md.md)

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

**MC rank:** **39** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 390 |
| Mean trade return | -0.006241% |
| Hist terminal | 0.975864× |
| Hist max DD | 2.7654% |
| MC median terminal | 0.975084× |
| MC mean terminal | 0.975441× |
| MC p05 / p95 | 0.954957× / 0.997230× |
| P(loss) | 97.00% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 2.9508% |
| Shuffle median terminal | 0.975864× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
