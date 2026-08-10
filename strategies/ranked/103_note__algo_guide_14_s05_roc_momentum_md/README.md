# Rank 103: `note__algo_guide_14_s05_roc_momentum_md`

**Title:** s05_roc_momentum.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s05_roc_momentum.md`

**Score:** 72.2777

**PF / Return% / MaxDD% / Trades:** 0.751 / -2.159 / 2.728 / 2763

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s05_roc_momentum_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 103 |
| Score | 72.2777 |
| Win rate % | 43.1512 |
| Profit factor | 0.7512 |
| Total return % | -2.1587 |
| Max DD % | 2.7282 |
| Trades | 2763 |
| Sharpe | -8.1430 |
| Sortino | -11.1399 |
| Calmar | -5.6272 |
| Profile | `guide_s05_roc` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 40 |
| Win rate % | 72.8602 |
| Baseline WR % | 43.1512 |
| Trades | 827 |
| Total return % | -0.3653 |
| Max DD % | 0.8349 |
| Profit factor | 0.8908 |
| Sharpe | -1.6808 |
| Score | 88.5103 |
| Tier | `A_first_breath` |
| Profile | `guide_s05_roc` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s05_roc_momentum_md.md`](../tweaks/note__algo_guide_14_s05_roc_momentum_md.md)

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

**MC rank:** **43** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 827 |
| Mean trade return | -0.003540% |
| Hist terminal | 0.970979× |
| Hist max DD | 3.1098% |
| MC median terminal | 0.970505× |
| MC mean terminal | 0.970883× |
| MC p05 / p95 | 0.943268× / 0.999634× |
| P(loss) | 95.10% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 3.7601% |
| Shuffle median terminal | 0.970979× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
