# Rank 20: `note__algo_guide_14_s12_zscore_reversion_md`

**Title:** s12_zscore_reversion.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s12_zscore_reversion.md`

**Score:** 92.4098

**PF / Return% / MaxDD% / Trades:** 0.949 / -1.777 / 2.819 / 3991

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s12_zscore_reversion_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 20 |
| Score | 92.4098 |
| Win rate % | 47.6239 |
| Profit factor | 0.9489 |
| Total return % | -1.7772 |
| Max DD % | 2.8186 |
| Trades | 3991 |
| Sharpe | -4.7225 |
| Sortino | -6.5416 |
| Calmar | -0.6037 |
| Profile | `guide_s12_zscore_mr` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 18 |
| Win rate % | 75.7353 |
| Baseline WR % | 47.6239 |
| Trades | 136 |
| Total return % | -0.1082 |
| Max DD % | 0.2591 |
| Profit factor | 49.8194 |
| Sharpe | 0.6335 |
| Score | 4981.7673 |
| Tier | `A_first_breath` |
| Profile | `guide_s12_zscore_mr` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s12_zscore_reversion_md.md`](../tweaks/note__algo_guide_14_s12_zscore_reversion_md.md)

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

**MC rank:** **31** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 136 |
| Mean trade return | -0.006391% |
| Hist terminal | 0.991319× |
| Hist max DD | 1.3159% |
| MC median terminal | 0.991648× |
| MC mean terminal | 0.991210× |
| MC p05 / p95 | 0.979232× / 1.002525× |
| P(loss) | 90.70% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 1.2066% |
| Shuffle median terminal | 0.991319× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
