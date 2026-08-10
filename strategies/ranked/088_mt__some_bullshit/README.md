# Rank 88: `mt__some_bullshit`

**Title:** some bullshit

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: some bullshit (.mq5)`

**Score:** 77.1113

**PF / Return% / MaxDD% / Trades:** 0.803 / -2.463 / 2.999 / 2997

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__some_bullshit`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 88 |
| Score | 77.1113 |
| Win rate % | 44.1320 |
| Profit factor | 0.8032 |
| Total return % | -2.4630 |
| Max DD % | 2.9988 |
| Trades | 2997 |
| Sharpe | -8.2677 |
| Sortino | -11.3745 |
| Calmar | -4.4087 |
| Profile | `macd` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 48 |
| Win rate % | 72.2450 |
| Baseline WR % | 44.1320 |
| Trades | 1018 |
| Total return % | -0.3952 |
| Max DD % | 1.0373 |
| Profit factor | 0.9335 |
| Sharpe | -1.3860 |
| Score | 92.7005 |
| Tier | `A_first_breath` |
| Profile | `macd` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__some_bullshit.md`](../tweaks/mt__some_bullshit.md)

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

**MC rank:** **59** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 1018 |
| Mean trade return | -0.003130% |
| Hist terminal | 0.968437× |
| Hist max DD | 4.0540% |
| MC median terminal | 0.966979× |
| MC mean terminal | 0.967680× |
| MC p05 / p95 | 0.936834× / 0.997505× |
| P(loss) | 95.60% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 4.1636% |
| Shuffle median terminal | 0.968437× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
