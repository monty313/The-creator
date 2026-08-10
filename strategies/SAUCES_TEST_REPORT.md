# Sauces test report — McFlurry + Dimension Jump

**Not Court law.** Same contract as folder batch: 2 HTF + 1 LTF, 4 sets, PB+cont, vectorbt.

- Data: `C:\Users\user\Downloads\_OTHER_PROJECTS\ATI_FTMO_project\gravity_engine\data\EURUSD_M1_export.csv`
- Window: 2026-06-04 16:28:00 → 2026-07-17 22:27:00 (45000 M1)
- vectorbt: 1.1.0
- Sort: `score = 100*PF + avg_return% - 0.25*|maxDD%|`

## Ranking

| Rank | Strategy | Score | PF | Return% | MaxDD% | Win% | Trades |
|-----:|----------|------:|---:|--------:|-------:|-----:|-------:|
| 1 | `mcflurry_eddy_scalp` | 1334.93 | 13.364 | -1.088 | 1.499 | 55.31 | 1753 |
| 2 | `dimension_jump_sauce` | 63.93 | 0.683 | -3.350 | 3.928 | 43.16 | 3753 |

## Per set × mode

### `mcflurry_eddy_scalp` — McFlurry Eddy trend-pullback scalp (H001)

- Sources: ['strategies/sauces/H001_mcflurry_eddy_scalp.md', 'Fable5 MOMENTUM_ONE hypotheses/H001_mcflurry_eddy_scalp.md']
- Aggregate score: 1334.9308

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|
| set1_1m_15m_30m | continuation | 332 | -2.0142 | 2.0855 | 39.76 | 0.539 | -11.176 |
| set1_1m_15m_30m | pullback | 843 | -3.4274 | 3.4953 | 39.50 | 0.665 | -13.430 |
| set2_5m_30m_1h | continuation | 49 | 0.0772 | 0.3546 | 57.14 | 1.075 | 0.519 |
| set2_5m_30m_1h | pullback | 394 | -2.7817 | 3.2362 | 51.52 | 0.738 | -6.610 |
| set3_15m_1h_4h | continuation | 5 | 0.1987 | 0.2243 | 60.00 | 3.270 | 2.892 |
| set3_15m_1h_4h | pullback | 111 | -0.6815 | 1.5395 | 44.55 | 0.869 | -1.523 |
| set4_30m_4h_1d | continuation | 1 | 0.1629 | 0.0538 | 100.00 | 99.000 | 3.528 |
| set4_30m_4h_1d | pullback | 18 | -0.2357 | 1.0061 | 50.00 | 0.755 | -1.431 |

Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`):

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9657.262398383331
Total Return [%]: -3.4273760161666904
Benchmark Return [%]: -1.7230711056876014
Max Gross Exposure [%]: 100.0
Total Fees Paid: 330.41294305132584
Max Drawdown [%]: 3.495289202658346
Max Drawdown Duration: 0.0
Total Trades: 843
Total Closed Trades: 843
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.50177935943061
Best Trade [%]: 0.17795158903893077
Worst Trade [%]: -0.1867072689921965
Avg Winning Trade [%]: 0.020864881644000525
Avg Losing Trade [%]: -0.02045491344202942
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.665046205818059
Expectancy: -0.4065689224396827
Sharpe Ratio: -13.429857824642284
Calmar Ratio: -9.572690257549386
Omega Ratio: 0.8943145195201055
Sortino Ratio: -19.099532225062585
```

#### RL teaching (not hard-code)

McFlurry: multi-TF RSI momentum line as **feel of acceleration**; eddy = load, zero-cross reclaim = fire under HTF M>0. Teach as skill labels, not fixed +1.5 threshold law.

#### 10× better

10× McFlurry: session filter (London/NY), sweep M_htf threshold, ATR exits from H001, multi-asset, random-entry control.

### `dimension_jump_sauce` — Dimension Jump sauce (CCI + BB-on-CCI) — McFlurry pair

- Sources: ['strategies/sauces/DimensionJump_sauce.md', 'MOMENTUM_ONE OBSERVATIONAL_INDICATOR_UNIVERSE / ML_CONFIRMATION_FLOW', 'ADR-0004 sauces pair']
- Aggregate score: 63.9335

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|
| set1_1m_15m_30m | continuation | 956 | -7.4732 | 7.4897 | 34.55 | 0.465 | -23.933 |
| set1_1m_15m_30m | pullback | 1992 | -11.5313 | 11.5663 | 36.87 | 0.532 | -29.867 |
| set2_5m_30m_1h | continuation | 160 | -0.9388 | 2.3323 | 46.88 | 0.793 | -3.377 |
| set2_5m_30m_1h | pullback | 421 | -2.9714 | 3.7340 | 45.84 | 0.730 | -7.841 |
| set3_15m_1h_4h | continuation | 47 | -1.3397 | 1.8663 | 34.04 | 0.522 | -5.360 |
| set3_15m_1h_4h | pullback | 122 | -2.3699 | 2.5814 | 43.44 | 0.609 | -6.869 |
| set4_30m_4h_1d | continuation | 16 | -0.2973 | 0.8796 | 56.25 | 0.762 | -1.359 |
| set4_30m_4h_1d | pullback | 39 | 0.1185 | 0.9769 | 47.37 | 1.048 | 0.370 |

Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`):

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8846.872537499148
Total Return [%]: -11.531274625008518
Benchmark Return [%]: -1.7230711056876014
Max Gross Exposure [%]: 100.0
Total Fees Paid: 745.2607393666167
Max Drawdown [%]: 11.566346161500004
Max Drawdown Duration: 0.0
Total Trades: 1992
Total Closed Trades: 1991
Total Open Trades: 1
Open Trade PnL: 0.2761414622182201
Win Rate [%]: 36.865896534404826
Best Trade [%]: 0.14416530115389423
Worst Trade [%]: -0.5586682884434548
Avg Winning Trade [%]: 0.019124502564901186
Avg Losing Trade [%]: -0.020908596946273363
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5324518385711076
Expectancy: -0.5793086910914471
Sharpe Ratio: -29.86741416779739
Calmar Ratio: -6.579057163875651
Omega Ratio: 0.8285907999625647
Sortino Ratio: -38.64792369126282
```

#### RL teaching (not hard-code)

Dimension Jump: CCI dimension vs BB-on-CCI as **momentum mass**; LTF CCI30 dip/reclaim under dual HTF CCI100 mass. Pair with McFlurry as dual-sauce state channels.

#### 10× better

10× Dimension Jump: require both CCI30 and CCI100 dimension alignment strength; concurrence with Mark RSI-BB release; no lone oscillator fires.
