# Rank 1: `note__algo_guide_14_s11_keltner_reversion_md`

**Title:** s11_keltner_reversion.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s11_keltner_reversion.md`

**Score:** 3755.4605

**PF / Return% / MaxDD% / Trades:** 37.567 / -0.944 / 1.355 / 1939

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s11_keltner_reversion_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 1 |
| Score | 3755.4605 |
| Win rate % | 64.8188 |
| Profit factor | 37.5674 |
| Total return % | -0.9445 |
| Max DD % | 1.3545 |
| Trades | 1939 |
| Sharpe | -1.6530 |
| Sortino | -0.9544 |
| Calmar | 5.9969 |
| Profile | `guide_s11_keltner_mr` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 22 |
| Win rate % | 73.9130 |
| Baseline WR % | 64.8188 |
| Trades | 46 |
| Total return % | -0.0633 |
| Max DD % | 0.1498 |
| Profit factor | 62.0534 |
| Sharpe | 0.8575 |
| Score | 6205.2430 |
| Tier | `A_first_breath` |
| Profile | `guide_s11_keltner_mr` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s11_keltner_reversion_md.md`](../tweaks/note__algo_guide_14_s11_keltner_reversion_md.md)

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

**MC rank:** **29** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 46 |
| Mean trade return | -0.011000% |
| Hist terminal | 0.994941× |
| Hist max DD | 0.6985% |
| MC median terminal | 0.995268× |
| MC mean terminal | 0.994936× |
| MC p05 / p95 | 0.986613× / 1.002098× |
| P(loss) | 86.40% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 0.7062% |
| Shuffle median terminal | 0.994941× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
