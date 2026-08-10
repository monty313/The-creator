# Rank 115: `mt__coolboolinger`

**Title:** coolboolinger

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: coolboolinger (.mq5)`

**Score:** 65.6030

**PF / Return% / MaxDD% / Trades:** 0.690 / -2.617 / 3.037 / 2845

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__coolboolinger`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 115 |
| Score | 65.6030 |
| Win rate % | 43.0299 |
| Profit factor | 0.6898 |
| Total return % | -2.6173 |
| Max DD % | 3.0367 |
| Trades | 2845 |
| Sharpe | -8.4938 |
| Sortino | -11.6612 |
| Calmar | -7.0798 |
| Profile | `cool_bb` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 125 |
| Win rate % | 69.8878 |
| Baseline WR % | 43.0299 |
| Trades | 902 |
| Total return % | -0.8134 |
| Max DD % | 1.0442 |
| Profit factor | 0.7951 |
| Sharpe | -3.5803 |
| Score | 78.4375 |
| Tier | `A_first_breath` |
| Profile | `cool_bb` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__coolboolinger.md`](../tweaks/mt__coolboolinger.md)

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

**MC rank:** **128** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 902 |
| Mean trade return | -0.007265% |
| Hist terminal | 0.936377× |
| Hist max DD | 6.5566% |
| MC median terminal | 0.936239× |
| MC mean terminal | 0.935587× |
| MC p05 / p95 | 0.904353× / 0.964687× |
| P(loss) | 100.00% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 6.8830% |
| Shuffle median terminal | 0.936377× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
