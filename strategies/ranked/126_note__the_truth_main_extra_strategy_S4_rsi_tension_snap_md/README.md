# Rank 126: `note__the_truth_main_extra_strategy_S4_rsi_tension_snap_md`

**Title:** strategy_S4_rsi_tension_snap.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\the_truth_main_extra\strategy_S4_rsi_tension_snap.md`

**Score:** 60.3028

**PF / Return% / MaxDD% / Trades:** 0.625 / -1.649 / 2.163 / 1874

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__the_truth_main_extra_strategy_S4_rsi_tension_snap_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 126 |
| Score | 60.3028 |
| Win rate % | 39.7631 |
| Profit factor | 0.6249 |
| Total return % | -1.6494 |
| Max DD % | 2.1628 |
| Trades | 1874 |
| Sharpe | -7.6891 |
| Sortino | -10.4476 |
| Calmar | -8.1635 |
| Profile | `truth_s4_rsi_snap` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 123 |
| Win rate % | 70.0609 |
| Baseline WR % | 39.7631 |
| Trades | 416 |
| Total return % | -0.3821 |
| Max DD % | 0.6024 |
| Profit factor | 0.8387 |
| Sharpe | -2.0021 |
| Score | 83.3342 |
| Tier | `A_first_breath` |
| Profile | `truth_s4_rsi_snap` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__the_truth_main_extra_strategy_S4_rsi_tension_snap_md.md`](../tweaks/note__the_truth_main_extra_strategy_S4_rsi_tension_snap_md.md)

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

**MC rank:** **46** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 416 |
| Mean trade return | -0.007429% |
| Hist terminal | 0.969488× |
| Hist max DD | 3.7521% |
| MC median terminal | 0.969408× |
| MC mean terminal | 0.969424× |
| MC p05 / p95 | 0.949040× / 0.989429× |
| P(loss) | 99.60% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 3.4101% |
| Shuffle median terminal | 0.969488× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
