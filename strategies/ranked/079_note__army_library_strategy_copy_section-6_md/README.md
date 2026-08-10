# Rank 79: `note__army_library_strategy_copy_section-6_md`

**Title:** section-6.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_library_strategy_copy\section-6.md`

**Score:** 77.2280

**PF / Return% / MaxDD% / Trades:** 0.820 / -3.621 / 4.412 / 5062

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__army_library_strategy_copy_section-6_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 79 |
| Score | 77.2280 |
| Win rate % | 46.6399 |
| Profit factor | 0.8195 |
| Total return % | -3.6207 |
| Max DD % | 4.4121 |
| Trades | 5062 |
| Sharpe | -10.3147 |
| Sortino | -14.0550 |
| Calmar | -3.1813 |
| Profile | `mark_rsi_bb` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 100 |
| Win rate % | 71.2119 |
| Baseline WR % | 46.6399 |
| Trades | 1295 |
| Total return % | -0.7631 |
| Max DD % | 1.2871 |
| Profit factor | 0.8121 |
| Sharpe | -3.2054 |
| Score | 80.1292 |
| Tier | `A_first_breath` |
| Profile | `mark_rsi_bb` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__army_library_strategy_copy_section-6_md.md`](../tweaks/note__army_library_strategy_copy_section-6_md.md)

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

**MC rank:** **121** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 1295 |
| Mean trade return | -0.004733% |
| Hist terminal | 0.940261× |
| Hist max DD | 6.3471% |
| MC median terminal | 0.939662× |
| MC mean terminal | 0.939567× |
| MC p05 / p95 | 0.902935× / 0.977502× |
| P(loss) | 99.70% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 6.7492% |
| Shuffle median terminal | 0.940261× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
