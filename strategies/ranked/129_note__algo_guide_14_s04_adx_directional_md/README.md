# Rank 129: `note__algo_guide_14_s04_adx_directional_md`

**Title:** s04_adx_directional.md

**Kind:** note

**Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\algo_guide_14\s04_adx_directional.md`

**Score:** 53.5139

**PF / Return% / MaxDD% / Trades:** 0.557 / -1.686 / 1.973 / 1611

**Collapses:** []

See [STRATEGY_TEST_REPORT.md](../STRATEGY_TEST_REPORT.md)

<!-- ALL_SIM_RESULTS_BEGIN -->
## All simulation results (batch + accuracy + Monte Carlo)

**Family id:** `note__algo_guide_14_s04_adx_directional_md`  
**Not Court law.** Lab claims only.

### 1) Full-batch strategy test (1:1 families)

| Metric | Value |
|--------|------:|
| Batch rank | 129 |
| Score | 53.5139 |
| Win rate % | 40.5220 |
| Profit factor | 0.5569 |
| Total return % | -1.6858 |
| Max DD % | 1.9730 |
| Trades | 1611 |
| Sharpe | -7.9766 |
| Sortino | -10.4876 |
| Calmar | -7.5018 |
| Profile | `guide_s04_adx_di` |
| n_runs (sets×modes) | 8 |

Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source report: [`STRATEGY_TEST_REPORT.md`](../STRATEGY_TEST_REPORT.md)

### 2) Accuracy-tweak batch (WR > 60.4% gate)

| Metric | Value |
|--------|------:|
| Pass gate | YES |
| Rank by WR | 23 |
| Win rate % | 73.2984 |
| Baseline WR % | 40.5220 |
| Trades | 573 |
| Total return % | -0.5048 |
| Max DD % | 0.8166 |
| Profit factor | 12.9872 |
| Sharpe | -2.2957 |
| Score | 1298.0118 |
| Tier | `A_first_breath` |
| Profile | `guide_s04_adx_di` |

Win bar: 60.4 · min trades: 25  
Window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Source: [`TWEAKED_ACCURACY_REPORT.md`](../TWEAKED_ACCURACY_REPORT.md) · tweak file: [`../tweaks/note__algo_guide_14_s04_adx_directional_md.md`](../tweaks/note__algo_guide_14_s04_adx_directional_md.md)

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

**MC rank:** **74** / 139

| Metric | Value |
|--------|------:|
| Pooled trades | 573 |
| Mean trade return | -0.007071% |
| Hist terminal | 0.960129× |
| Hist max DD | 4.1930% |
| MC median terminal | 0.959583× |
| MC mean terminal | 0.959499× |
| MC p05 / p95 | 0.930743× / 0.988443× |
| P(loss) | 99.00% |
| P(DD ≥ 20%) | 0.00% |
| Median path max DD | 4.6405% |
| Shuffle median terminal | 0.960129× |
| Shuffle P(loss) | 100.00% |

Sims: 1000 · seed: 42 · window: 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)  
Full MC table: [`MONTE_CARLO_REPORT.md`](../MONTE_CARLO_REPORT.md) · by-file: [`MONTE_CARLO_BY_FILE.md`](../MONTE_CARLO_BY_FILE.md) · raw: [`MONTE_CARLO_RESULTS.json`](../MONTE_CARLO_RESULTS.json)

<!-- ALL_SIM_RESULTS_END -->
