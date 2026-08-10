# Rank 107: `note__algo_guide_14_s02_breakout_trading_md`

**Title:** s02_breakout_trading.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s02_breakout_trading.md`

**Score:** 69.4843

**PF / Return% / MaxDD% / Trades:** 0.723 / -2.202 / 2.484 / 2231

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s02_breakout_trading_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 107 |
| Score | 69.4843 |
| Win rate % | 40.0755 |
| Profit factor | 0.7231 |
| Total return % | -2.2022 |
| Max DD % | 2.4836 |
| Trades | 2231 |
| Sharpe | -7.1498 |
| Sortino | -10.1421 |
| Calmar | -7.0165 |
| Profile | `guide_s02_breakout` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 20 |
| Win rate % | 74.5659 |
| Baseline WR % | 40.0755 |
| Trades | 1032 |
| Total return % | -0.5215 |
| Max DD % | 1.1443 |
| Profit factor | 0.9051 |
| Sharpe | -1.8972 |
| Score | 89.7067 |
| Tier | `A_first_breath` |
| Profile | `guide_s02_breakout` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s02_breakout_trading_md.md`](../tweaks/note__algo_guide_14_s02_breakout_trading_md.md)

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

**MC rank:** **75** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 1032 |
| Mean trade return | -0.004039% |
| Hist terminal | 0.958897× |
| Hist max DD | 4.5713% |
| MC median terminal | 0.958035× |
| MC mean terminal | 0.958309× |
| MC p05 / p95 | 0.917903× / 0.997153× |
| P(loss) | 96.40% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 5.1321% |
| Shuffle median terminal | 0.958897× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
