# Rank 94: `note__algo_guide_14_s07_ema_ribbon_md`

**Title:** s07_ema_ribbon.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s07_ema_ribbon.md`

**Score:** 74.1532

**PF / Return% / MaxDD% / Trades:** 0.776 / -2.644 / 3.339 / 2941

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s07_ema_ribbon_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 94 |
| Score | 74.1532 |
| Win rate % | 36.2262 |
| Profit factor | 0.7763 |
| Total return % | -2.6439 |
| Max DD % | 3.3393 |
| Trades | 2941 |
| Sharpe | -7.8509 |
| Sortino | -10.3431 |
| Calmar | -3.4166 |
| Profile | `guide_s07_ema_ribbon` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 121 |
| Win rate % | 70.5925 |
| Baseline WR % | 36.2262 |
| Trades | 1585 |
| Total return % | -1.2125 |
| Max DD % | 1.6945 |
| Profit factor | 0.7929 |
| Sharpe | -4.1853 |
| Score | 77.6534 |
| Tier | `A_first_breath` |
| Profile | `guide_s07_ema_ribbon` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s07_ema_ribbon_md.md`](../tweaks/note__algo_guide_14_s07_ema_ribbon_md.md)

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

**MC rank:** **138** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 1585 |
| Mean trade return | -0.006164% |
| Hist terminal | 0.906548× |
| Hist max DD | 9.4364% |
| MC median terminal | 0.906686× |
| MC mean terminal | 0.907377× |
| MC p05 / p95 | 0.865345× / 0.948965× |
| P(loss) | 100.00% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 9.8770% |
| Shuffle median terminal | 0.906548× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
