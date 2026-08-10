# Rank 17: `note__algo_guide_14_s09_rsi_reversion_md`

**Title:** s09_rsi_reversion.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s09_rsi_reversion.md`

**Score:** 104.0321

**PF / Return% / MaxDD% / Trades:** 1.053 / -0.789 / 1.718 / 1753

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s09_rsi_reversion_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 17 |
| Score | 104.0321 |
| Win rate % | 50.5403 |
| Profit factor | 1.0525 |
| Total return % | -0.7890 |
| Max DD % | 1.7184 |
| Trades | 1753 |
| Sharpe | -2.7383 |
| Sortino | -4.0001 |
| Calmar | 1.5556 |
| Profile | `guide_s09_rsi_mr` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 8 |
| Win rate % | 76.4706 |
| Baseline WR % | 50.5403 |
| Trades | 34 |
| Total return % | -0.0856 |
| Max DD % | 0.1634 |
| Profit factor | 37.1797 |
| Sharpe | -0.7256 |
| Score | 3717.8444 |
| Tier | `D_no_session` |
| Profile | `guide_s09_rsi_mr` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s09_rsi_reversion_md.md`](../tweaks/note__algo_guide_14_s09_rsi_reversion_md.md)

Tier params:

| Param | Value |
|-------|------:|
| tp | 0.00012 |
| sl | 0.0014 |
| hold | 0 |
| session | False |
| strength | True |
| structure | False |

### 3) Monte Carlo (bootstrap + order-shuffle)

**MC rank:** **28** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 22 |
| Mean trade return | -0.018469% |
| Hist terminal | 0.995937× |
| Hist max DD | 0.5373% |
| MC median terminal | 0.995916× |
| MC mean terminal | 0.995902× |
| MC p05 / p95 | 0.989353× / 1.002231× |
| P(loss) | 84.30% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 0.5594% |
| Shuffle median terminal | 0.995937× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
