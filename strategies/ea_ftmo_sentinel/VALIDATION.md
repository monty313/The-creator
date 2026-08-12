# FTMO Sentinel — governor Monte Carlo (measured-parameter validation)

**Not Court law.** Summary-Court measurement artifact. Trade model from `strategies/reports` measured books; win = +0.243R, loss = -1R, cost = 0.05R/trade.

Days per scenario: 20000 · challenges: 2000 · seed 42

| Scenario | WR | sig/day | mean day | med day | P(day>=+2.5%) | P(red day) | worst day | P(day<=-5%) FTMO |
|---|---|---|---|---|---|---|---|---|
| A_cci_LB_1symbol | 0.920 | 20 | +1.266% | +2.512% | 50.56% | 37.20% | -1.540% | 0.00% |
| A3_cci_LB_3symbols | 0.920 | 40 | +1.396% | +2.673% | 58.19% | 35.60% | -1.540% | 0.00% |
| B_cci_LB_sparse | 0.920 | 8 | +0.760% | +0.767% | 12.14% | 38.03% | -1.540% | 0.00% |
| C_mcflurry_base | 0.800 | 20 | -0.513% | -1.183% | 12.34% | 80.61% | -1.540% | 0.00% |
| D_stress | 0.700 | 20 | -1.162% | -1.511% | 3.00% | 94.65% | -1.540% | 0.00% |

## FTMO challenge outcomes (target +10%, min 4 trading days, 60-day cap)

`halted @-6% fuse` = EA stops itself before the FTMO -10% breach: challenge not passed, account preserved.

| Scenario | P(pass) | P(FTMO daily breach) | P(FTMO total breach) | P(halted @-6% fuse) | P(timeout) | median days to pass |
|---|---|---|---|---|---|---|
| A_cci_LB_1symbol | 99.95% | 0.00% | 0.00% | 0.05% | 0.00% | 8 |
| A3_cci_LB_3symbols | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% | 7 |
| B_cci_LB_sparse | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% | 13 |
| C_mcflurry_base | 0.80% | 0.00% | 0.00% | 99.05% | 0.15% | 11 |
| D_stress | 0.00% | 0.00% | 0.00% | 100.00% | 0.00% | nan |

## Read this honestly

- The governor **caps** every red day near the soft stop; an FTMO daily breach (-5%) requires an intraday gap far past the hard flatten — the sim shows 0 at trade-close granularity, live requires the hard-stop watchdog plus sane position sizing (which the EA enforces).
- '+2.5% every single day' is not physically guaranteeable: on sparse-signal or low-WR days the governor banks smaller greens or scratches flat instead of forcing thrash. The design maximizes P(green) first, goal-hit second.
- WR inputs are from one EURUSD window (June-July 2026). Re-measure per symbol/window before believing the absolute pass-time numbers (corpus law: distrust specific pips until they survive new windows).
