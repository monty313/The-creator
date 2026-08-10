# Rank 36: `note__algo_guide_14_s14_williams_r_reversion_md`

**Title:** s14_williams_r_reversion.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s14_williams_r_reversion.md`

**Score:** 79.1276

**PF / Return% / MaxDD% / Trades:** 0.846 / -4.132 / 5.261 / 7346

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s14_williams_r_reversion_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 36 |
| Score | 79.1276 |
| Win rate % | 51.4488 |
| Profit factor | 0.8457 |
| Total return % | -4.1317 |
| Max DD % | 5.2605 |
| Trades | 7346 |
| Sharpe | -10.1489 |
| Sortino | -13.6785 |
| Calmar | -1.7737 |
| Profile | `guide_s14_willr_mr` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 51 |
| Win rate % | 71.6921 |
| Baseline WR % | 51.4488 |
| Trades | 560 |
| Total return % | -0.2563 |
| Max DD % | 0.6041 |
| Profit factor | 1.0083 |
| Sharpe | -1.2839 |
| Score | 100.4266 |
| Tier | `A_first_breath` |
| Profile | `guide_s14_willr_mr` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s14_williams_r_reversion_md.md`](../tweaks/note__algo_guide_14_s14_williams_r_reversion_md.md)

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

**MC rank:** **38** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 560 |
| Mean trade return | -0.003670% |
| Hist terminal | 0.979544× |
| Hist max DD | 2.8134% |
| MC median terminal | 0.979436× |
| MC mean terminal | 0.979405× |
| MC p05 / p95 | 0.953324× / 1.004413× |
| P(loss) | 90.20% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 2.7952% |
| Shuffle median terminal | 0.979544× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
