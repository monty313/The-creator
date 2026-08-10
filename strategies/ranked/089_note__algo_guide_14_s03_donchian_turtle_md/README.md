# Rank 89: `note__algo_guide_14_s03_donchian_turtle_md`

**Title:** s03_donchian_turtle.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s03_donchian_turtle.md`

**Score:** 75.6603

**PF / Return% / MaxDD% / Trades:** 0.787 / -2.356 / 2.833 / 3042

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s03_donchian_turtle_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 89 |
| Score | 75.6603 |
| Win rate % | 40.9890 |
| Profit factor | 0.7872 |
| Total return % | -2.3562 |
| Max DD % | 2.8326 |
| Trades | 3042 |
| Sharpe | -7.3689 |
| Sortino | -10.0601 |
| Calmar | -4.7203 |
| Profile | `guide_s03_donchian_turtle` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 21 |
| Win rate % | 74.3089 |
| Baseline WR % | 40.9890 |
| Trades | 573 |
| Total return % | -0.3791 |
| Max DD % | 0.7714 |
| Profit factor | 13.1957 |
| Sharpe | -1.5148 |
| Score | 1319.0011 |
| Tier | `A_first_breath` |
| Profile | `guide_s03_donchian_turtle` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s03_donchian_turtle_md.md`](../tweaks/note__algo_guide_14_s03_donchian_turtle_md.md)

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

**MC rank:** **42** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 573 |
| Mean trade return | -0.005318% |
| Hist terminal | 0.969839× |
| Hist max DD | 3.7575% |
| MC median terminal | 0.971142× |
| MC mean terminal | 0.970767× |
| MC p05 / p95 | 0.943607× / 0.997515× |
| P(loss) | 96.50% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 3.6201% |
| Shuffle median terminal | 0.969839× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
