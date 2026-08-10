# Rank 127: `mt__KineticEdgeEA`

**Title:** KineticEdgeEA

**Kind:** mt

**Source:** `strategies/language/01_METATRADER_INDEX.md :: KineticEdgeEA (.mq5)`

**Score:** 59.9077

**PF / Return% / MaxDD% / Trades:** 0.622 / -1.726 / 2.131 / 1665

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `mt__KineticEdgeEA`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 127 |
| Score | 59.9077 |
| Win rate % | 42.1408 |
| Profit factor | 0.6217 |
| Total return % | -1.7259 |
| Max DD % | 2.1311 |
| Trades | 1665 |
| Sharpe | -7.4567 |
| Sortino | -10.0883 |
| Calmar | -7.4852 |
| Profile | `kinetic` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 139 |
| Win rate % | 68.6435 |
| Baseline WR % | 42.1408 |
| Trades | 522 |
| Total return % | -0.6665 |
| Max DD % | 0.8389 |
| Profit factor | 0.5838 |
| Sharpe | -3.3283 |
| Score | 57.5076 |
| Tier | `A_first_breath` |
| Profile | `kinetic` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/mt__KineticEdgeEA.md`](../tweaks/mt__KineticEdgeEA.md)

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

**MC rank:** **82** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 522 |
| Mean trade return | -0.010288% |
| Hist terminal | 0.947607× |
| Hist max DD | 5.7549% |
| MC median terminal | 0.947230× |
| MC mean terminal | 0.947673× |
| MC p05 / p95 | 0.926013× / 0.970210× |
| P(loss) | 99.90% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 5.5314% |
| Shuffle median terminal | 0.947607× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
