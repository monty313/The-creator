# Rank 137: `note__local_desktop_factory_full_GV-014-XAU-L1_md`

**Title:** GV-014-XAU-L1.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\factory_full\GV-014-XAU-L1.md`

**Score:** 33.5833

**PF / Return% / MaxDD% / Trades:** 0.353 / -1.276 / 1.609 / 1398

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__local_desktop_factory_full_GV-014-XAU-L1_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 137 |
| Score | 33.5833 |
| Win rate % | 21.0704 |
| Profit factor | 0.3526 |
| Total return % | -1.2757 |
| Max DD % | 1.6087 |
| Trades | 1398 |
| Sharpe | -4.9424 |
| Sortino | -6.7976 |
| Calmar | -3.1707 |
| Profile | `gv014` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 38 |
| Win rate % | 72.9632 |
| Baseline WR % | 21.0704 |
| Trades | 415 |
| Total return % | -0.1866 |
| Max DD % | 0.4953 |
| Profit factor | 0.4464 |
| Sharpe | -0.9399 |
| Score | 44.3254 |
| Tier | `A_first_breath` |
| Profile | `gv014` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__local_desktop_factory_full_GV-014-XAU-L1_md.md`](../tweaks/note__local_desktop_factory_full_GV-014-XAU-L1_md.md)

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

**MC rank:** **33** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 415 |
| Mean trade return | -0.003606% |
| Hist terminal | 0.985060× |
| Hist max DD | 1.9402% |
| MC median terminal | 0.985491× |
| MC mean terminal | 0.985325× |
| MC p05 / p95 | 0.962538× / 1.006019× |
| P(loss) | 86.60% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 2.2132% |
| Shuffle median terminal | 0.985060× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
