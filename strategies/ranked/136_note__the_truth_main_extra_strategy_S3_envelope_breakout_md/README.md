# Rank 136: `note__the_truth_main_extra_strategy_S3_envelope_breakout_md`

**Title:** strategy_S3_envelope_breakout.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\the_truth_main_extra\strategy_S3_envelope_breakout.md`

**Score:** 40.3529

**PF / Return% / MaxDD% / Trades:** 0.417 / -1.025 / 1.246 / 730

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__the_truth_main_extra_strategy_S3_envelope_breakout_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 136 |
| Score | 40.3529 |
| Win rate % | 31.9951 |
| Profit factor | 0.4169 |
| Total return % | -1.0252 |
| Max DD % | 1.2461 |
| Trades | 730 |
| Sharpe | -6.2190 |
| Sortino | -8.2543 |
| Calmar | -9.7202 |
| Profile | `truth_s3_env` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 41 |
| Win rate % | 72.5572 |
| Baseline WR % | 31.9951 |
| Trades | 481 |
| Total return % | -0.4255 |
| Max DD % | 0.7350 |
| Profit factor | 0.5816 |
| Sharpe | -2.2854 |
| Score | 57.5500 |
| Tier | `A_first_breath` |
| Profile | `truth_s3_env` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__the_truth_main_extra_strategy_S3_envelope_breakout_md.md`](../tweaks/note__the_truth_main_extra_strategy_S3_envelope_breakout_md.md)

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

**MC rank:** **57** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 481 |
| Mean trade return | -0.007083% |
| Hist terminal | 0.966379× |
| Hist max DD | 4.2359% |
| MC median terminal | 0.967245× |
| MC mean terminal | 0.967230× |
| MC p05 / p95 | 0.942161× / 0.993285× |
| P(loss) | 97.90% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 3.8379% |
| Shuffle median terminal | 0.966379× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
