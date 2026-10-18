# Sentinel backtest — EURUSD_Y (Dukascopy M1, bar-accurate)

### EURUSD_Y · variant `default`

signal funnel: {'A_fire': 1136, 'A_after_force': 161, 'B_fire': 1249, 'B_after_force': 187, 'union_or_conc': 321, 'after_mass': 124, 'after_shell': 25}
- trades: **11** (1.4/trading day, 8/73 days traded) · WR **54.5%** · concurrence fires: 2
- total P&L: **-3.20%** of initial over 73 days (-0.9%/month-ish) · mean day -0.044% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **5** (worst close -1.00%) · worst intraday float -0.63% · FTMO -5% breaches: **0**
- challenge walk-forward (73 starts): TIMEOUT 100%
- by month: 2026-05 +0.0% · 2026-06 -0.3% · 2026-07 -3.0% · 2026-08 +0.0%

### EURUSD_Y · variant `no_mass`

signal funnel: {'A_fire': 1136, 'A_after_force': 161, 'B_fire': 1249, 'B_after_force': 187, 'union_or_conc': 321, 'after_shell': 75}
- trades: **42** (1.8/trading day, 24/73 days traded) · WR **61.9%** · concurrence fires: 5
- total P&L: **-7.06%** of initial over 73 days (-2.0%/month-ish) · mean day -0.097% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **12** (worst close -1.50%) · worst intraday float -1.37% · FTMO -5% breaches: **0**
- challenge walk-forward (73 starts): HALT_FUSE 25%, TIMEOUT 75%
- by month: 2026-05 +0.2% · 2026-06 -1.1% · 2026-07 -5.9% · 2026-08 -0.3%

### EURUSD_Y · variant `cci_only`

signal funnel: {'A_fire': 1136, 'A_after_force': 161, 'union_or_conc': 161, 'after_shell': 33}
- trades: **18** (1.8/trading day, 10/73 days traded) · WR **66.7%** · concurrence fires: 0
- total P&L: **-2.19%** of initial over 73 days (-0.6%/month-ish) · mean day -0.030% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **5** (worst close -1.15%) · worst intraday float -1.22% · FTMO -5% breaches: **0**
- challenge walk-forward (73 starts): TIMEOUT 100%
- by month: 2026-05 +0.0% · 2026-06 -0.8% · 2026-07 -1.8% · 2026-08 +0.4%

### EURUSD_Y · variant `cci_mass`

signal funnel: {'A_fire': 1136, 'A_after_force': 161, 'union_or_conc': 161, 'after_mass': 54, 'after_shell': 8}
- trades: **3** (1.0/trading day, 3/73 days traded) · WR **33.3%** · concurrence fires: 0
- total P&L: **-1.40%** of initial over 73 days (-0.4%/month-ish) · mean day -0.019% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **2** (worst close -0.80%) · worst intraday float -0.50% · FTMO -5% breaches: **0**
- challenge walk-forward (73 starts): TIMEOUT 100%
- by month: 2026-05 +0.0% · 2026-06 +0.0% · 2026-07 -1.4% · 2026-08 +0.0%

### EURUSD_Y · variant `mcf_only`

signal funnel: {'B_fire': 1249, 'B_after_force': 187, 'union_or_conc': 187, 'after_shell': 50}
- trades: **31** (1.5/trading day, 21/73 days traded) · WR **54.8%** · concurrence fires: 0
- total P&L: **-6.82%** of initial over 73 days (-2.0%/month-ish) · mean day -0.093% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **10** (worst close -1.50%) · worst intraday float -1.33% · FTMO -5% breaches: **0**
- challenge walk-forward (73 starts): HALT_FUSE 25%, TIMEOUT 75%
- by month: 2026-05 +0.2% · 2026-06 -1.0% · 2026-07 -5.3% · 2026-08 -0.7%

### EURUSD_Y · variant `a15`

signal funnel: {'A_fire': 360, 'A_after_force': 48, 'union_or_conc': 48, 'after_shell': 11}
- trades: **8** (1.0/trading day, 8/73 days traded) · WR **75.0%** · concurrence fires: 0
- total P&L: **+2.00%** of initial over 73 days (0.6%/month-ish) · mean day +0.027% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **2** (worst close -0.80%) · worst intraday float -0.61% · FTMO -5% breaches: **0**
- challenge walk-forward (73 starts): TIMEOUT 100%
- by month: 2026-05 +0.0% · 2026-06 -0.4% · 2026-07 +1.8% · 2026-08 +0.6%

### EURUSD_Y · variant `a15w`

signal funnel: {'A_fire': 360, 'A_after_force': 48, 'union_or_conc': 48, 'after_shell': 11}
- trades: **8** (1.0/trading day, 8/73 days traded) · WR **37.5%** · concurrence fires: 0
- total P&L: **-0.20%** of initial over 73 days (-0.1%/month-ish) · mean day -0.003% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **5** (worst close -0.80%) · worst intraday float -0.76% · FTMO -5% breaches: **0**
- challenge walk-forward (73 starts): TIMEOUT 100%
- by month: 2026-05 +0.0% · 2026-06 +0.9% · 2026-07 -1.8% · 2026-08 +0.7%
