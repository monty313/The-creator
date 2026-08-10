# Rank 95: `note__algo_guide_14_s01_ma_crossover_md`

**Title:** s01_ma_crossover.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s01_ma_crossover.md`

**Score:** 73.6365

**PF / Return% / MaxDD% / Trades:** 0.746 / -0.696 / 0.890 / 809

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s01_ma_crossover_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 95 |
| Score | 73.6365 |
| Win rate % | 26.4940 |
| Profit factor | 0.7456 |
| Total return % | -0.6961 |
| Max DD % | 0.8898 |
| Trades | 809 |
| Sharpe | -3.5639 |
| Sortino | -4.4155 |
| Calmar | -1.3171 |
| Profile | `guide_s01_ma_cross` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 7 |
| Win rate % | 77.4436 |
| Baseline WR % | 26.4940 |
| Trades | 133 |
| Total return % | -0.0077 |
| Max DD % | 0.2118 |
| Profit factor | 12.7827 |
| Sharpe | 0.0424 |
| Score | 1278.2132 |
| Tier | `A_first_breath` |
| Profile | `guide_s01_ma_cross` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s01_ma_crossover_md.md`](../tweaks/note__algo_guide_14_s01_ma_crossover_md.md)

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

**MC rank:** **27** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 133 |
| Mean trade return | -0.000440% |
| Hist terminal | 0.999382× |
| Hist max DD | 0.6071% |
| MC median terminal | 0.999743× |
| MC mean terminal | 0.999763× |
| MC p05 / p95 | 0.986136× / 1.013020× |
| P(loss) | 51.50% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 0.8153% |
| Shuffle median terminal | 0.999382× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
