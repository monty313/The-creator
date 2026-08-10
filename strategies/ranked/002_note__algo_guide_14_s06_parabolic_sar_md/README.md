# Rank 2: `note__algo_guide_14_s06_parabolic_sar_md`

**Title:** s06_parabolic_sar.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s06_parabolic_sar.md`

**Score:** 1329.7459

**PF / Return% / MaxDD% / Trades:** 13.312 / -1.111 / 1.335 / 1222

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s06_parabolic_sar_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 2 |
| Score | 1329.7459 |
| Win rate % | 48.5119 |
| Profit factor | 13.3119 |
| Total return % | -1.1112 |
| Max DD % | 1.3346 |
| Trades | 1222 |
| Sharpe | -5.3358 |
| Sortino | -7.2649 |
| Calmar | -4.5661 |
| Profile | `guide_s06_psar` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 19 |
| Win rate % | 74.6956 |
| Baseline WR % | 48.5119 |
| Trades | 305 |
| Total return % | -0.1371 |
| Max DD % | 0.3644 |
| Profit factor | 0.6444 |
| Sharpe | -1.4960 |
| Score | 64.2096 |
| Tier | `A_first_breath` |
| Profile | `guide_s06_psar` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s06_parabolic_sar_md.md`](../tweaks/note__algo_guide_14_s06_parabolic_sar_md.md)

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

**MC rank:** **32** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 305 |
| Mean trade return | -0.003597% |
| Hist terminal | 0.989033× |
| Hist max DD | 1.1898% |
| MC median terminal | 0.989217× |
| MC mean terminal | 0.989245× |
| MC p05 / p95 | 0.972191× / 1.006270× |
| P(loss) | 85.50% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 1.7033% |
| Shuffle median terminal | 0.989033× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
