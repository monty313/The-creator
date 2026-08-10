# Rank 15: `note__algo_guide_14_s10_vwap_reversion_md`

**Title:** s10_vwap_reversion.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s10_vwap_reversion.md`

**Score:** 1294.1084

**PF / Return% / MaxDD% / Trades:** 12.941 / 0.194 / 0.576 / 314

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s10_vwap_reversion_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 15 |
| Score | 1294.1084 |
| Win rate % | 40.8648 |
| Profit factor | 12.9406 |
| Total return % | 0.1936 |
| Max DD % | 0.5759 |
| Trades | 314 |
| Sharpe | 0.8911 |
| Sortino | 1.5951 |
| Calmar | 7.9697 |
| Profile | `guide_s10_vwap_mr` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 1 |
| Win rate % | 91.0417 |
| Baseline WR % | 40.8648 |
| Trades | 480 |
| Total return % | 0.3832 |
| Max DD % | 0.3582 |
| Profit factor | 25.4242 |
| Sharpe | 1.7009 |
| Score | 2542.7144 |
| Tier | `E_ultra_breath` |
| Profile | `guide_s10_vwap_mr` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s10_vwap_reversion_md.md`](../tweaks/note__algo_guide_14_s10_vwap_reversion_md.md)

Tier params:

| Param | Value |
|-------|------:|
| tp | 0.0001 |
| sl | 0.0015 |
| hold | 0 |
| session | False |
| strength | False |
| structure | False |

### 3) Monte Carlo (bootstrap + order-shuffle)

**MC rank:** **30** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 12 |
| Mean trade return | -0.042803% |
| Hist terminal | 0.994871× |
| Hist max DD | 0.5415% |
| MC median terminal | 0.994952× |
| MC mean terminal | 0.994795× |
| MC p05 / p95 | 0.989763× / 0.999723× |
| P(loss) | 95.80% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 0.5492% |
| Shuffle median terminal | 0.994871× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
