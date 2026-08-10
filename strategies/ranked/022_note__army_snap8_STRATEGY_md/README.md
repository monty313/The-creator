# Rank 22: `note__army_snap8_STRATEGY_md`

**Title:** STRATEGY.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_snap8\STRATEGY.md`

**Score:** 88.2454

**PF / Return% / MaxDD% / Trades:** 0.896 / -0.958 / 1.503 / 1291

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__army_snap8_STRATEGY_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 22 |
| Score | 88.2454 |
| Win rate % | 41.2633 |
| Profit factor | 0.8958 |
| Total return % | -0.9584 |
| Max DD % | 1.5033 |
| Trades | 1291 |
| Sharpe | -4.2840 |
| Sortino | -5.3804 |
| Calmar | -1.5699 |
| Profile | `snap8` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 57 |
| Win rate % | 71.3992 |
| Baseline WR % | 41.2633 |
| Trades | 437 |
| Total return % | -0.3440 |
| Max DD % | 0.6872 |
| Profit factor | 12.9255 |
| Sharpe | -1.9071 |
| Score | 1292.0345 |
| Tier | `A_first_breath` |
| Profile | `snap8` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__army_snap8_STRATEGY_md.md`](../tweaks/note__army_snap8_STRATEGY_md.md)

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

**MC rank:** **41** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 437 |
| Mean trade return | -0.006366% |
| Hist terminal | 0.972467× |
| Hist max DD | 3.2665% |
| MC median terminal | 0.971810× |
| MC mean terminal | 0.972357× |
| MC p05 / p95 | 0.949797× / 0.995852× |
| P(loss) | 97.70% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 3.3074% |
| Shuffle median terminal | 0.972467× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
