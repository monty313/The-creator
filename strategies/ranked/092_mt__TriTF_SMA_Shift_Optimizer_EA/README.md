# Rank 92: `mt__TriTF_SMA_Shift_Optimizer_EA`

**Title:** TriTF_SMA_Shift_Optimizer_EA

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: TriTF_SMA_Shift_Optimizer_EA (.mq5)`

**Score:** 74.4812

**PF / Return% / MaxDD% / Trades:** 0.761 / -1.205 / 1.686 / 1412

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__TriTF_SMA_Shift_Optimizer_EA`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 92 |
| Score | 74.4812 |
| Win rate % | 42.2103 |
| Profit factor | 0.7611 |
| Total return % | -1.2050 |
| Max DD % | 1.6858 |
| Trades | 1412 |
| Sharpe | -6.4428 |
| Sortino | -8.5462 |
| Calmar | -4.2805 |
| Profile | `sma_scalp` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 6 |
| Win rate % | 78.3520 |
| Baseline WR % | 42.2103 |
| Trades | 250 |
| Total return % | 0.1241 |
| Max DD % | 0.3991 |
| Profit factor | 13.3673 |
| Sharpe | 1.2273 |
| Score | 1336.7516 |
| Tier | `A_first_breath` |
| Profile | `sma_scalp` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__TriTF_SMA_Shift_Optimizer_EA.md`](../tweaks/mt__TriTF_SMA_Shift_Optimizer_EA.md)

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

**MC rank:** **2** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 250 |
| Mean trade return | 0.003957% |
| Hist terminal | 1.009880× |
| Hist max DD | 0.9388% |
| MC median terminal | 1.010017× |
| MC mean terminal | 1.010086× |
| MC p05 / p95 | 0.991531× / 1.028884× |
| P(loss) | 19.50% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 0.8926% |
| Shuffle median terminal | 1.009880× |
| Shuffle P(loss) | 0.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
