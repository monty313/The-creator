# Rank 16: `note__algo_guide_14_s08_bb_mean_reversion_md`

**Title:** s08_bb_mean_reversion.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s08_bb_mean_reversion.md`

**Score:** 267.4175

**PF / Return% / MaxDD% / Trades:** 2.680 / -0.346 / 0.983 / 920

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s08_bb_mean_reversion_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 16 |
| Score | 267.4175 |
| Win rate % | 49.1595 |
| Profit factor | 2.6801 |
| Total return % | -0.3462 |
| Max DD % | 0.9828 |
| Trades | 920 |
| Sharpe | -1.4441 |
| Sortino | -1.6856 |
| Calmar | 2.4638 |
| Profile | `guide_s08_bb_mr` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 2 |
| Win rate % | 82.3529 |
| Baseline WR % | 49.1595 |
| Trades | 34 |
| Total return % | -0.0292 |
| Max DD % | 0.1223 |
| Profit factor | 49.6105 |
| Sharpe | 0.8128 |
| Score | 4960.9864 |
| Tier | `C_scalp_breath` |
| Profile | `guide_s08_bb_mr` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s08_bb_mean_reversion_md.md`](../tweaks/note__algo_guide_14_s08_bb_mean_reversion_md.md)

Tier params:

| Param | Value |
|-------|------:|
| tp | 0.00012 |
| sl | 0.0014 |
| hold | 0 |
| session | True |
| strength | True |
| structure | False |

### 3) Monte Carlo (bootstrap + order-shuffle)

**MC rank:** **26** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 18 |
| Mean trade return | -0.001416% |
| Hist terminal | 0.999740× |
| Hist max DD | 0.2279% |
| MC median terminal | 1.000028× |
| MC mean terminal | 0.999833× |
| MC p05 / p95 | 0.994538× / 1.004344× |
| P(loss) | 49.60% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 0.2738% |
| Shuffle median terminal | 0.999740× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
