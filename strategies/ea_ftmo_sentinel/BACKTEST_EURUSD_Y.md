# Sentinel backtest — EURUSD_Y (Dukascopy M1, bar-accurate)

### EURUSD_Y · variant `default`

signal funnel: {'A_fire': 1136, 'A_after_force': 161, 'B_fire': 1249, 'B_after_force': 187, 'union_or_conc': 321, 'after_mass': 124, 'after_shell': 25}
- trades: **11** (1.4/trading day, 8/8 days traded) · WR **54.5%** · concurrence fires: 2
- total P&L: **-3.20%** of initial over 8 days (-8.4%/month-ish) · mean day -0.400% · median day -0.745%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **5** (worst close -1.00%) · worst intraday float -0.63% · FTMO -5% breaches: **0**
- challenge walk-forward (8 starts): TIMEOUT 100%
- by month: 2026-06 -0.3% · 2026-07 -3.0%

### EURUSD_Y · variant `no_mass`

signal funnel: {'A_fire': 1136, 'A_after_force': 161, 'B_fire': 1249, 'B_after_force': 187, 'union_or_conc': 321, 'after_shell': 75}
- trades: **42** (1.8/trading day, 24/24 days traded) · WR **61.9%** · concurrence fires: 5
- total P&L: **-7.06%** of initial over 24 days (-6.2%/month-ish) · mean day -0.294% · median day -0.138%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **12** (worst close -1.50%) · worst intraday float -1.37% · FTMO -5% breaches: **0**
- challenge walk-forward (24 starts): HALT_FUSE 46%, TIMEOUT 54%
- by month: 2026-05 +0.2% · 2026-06 -1.1% · 2026-07 -5.9% · 2026-08 -0.3%

### EURUSD_Y · variant `conc_only`

signal funnel: {'A_fire': 1136, 'A_after_force': 161, 'B_fire': 1249, 'B_after_force': 187, 'union_or_conc': 27, 'after_shell': 8}
- trades: **5** (1.0/trading day, 5/5 days traded) · WR **40.0%** · concurrence fires: 5
- total P&L: **-2.50%** of initial over 5 days (-10.5%/month-ish) · mean day -0.500% · median day -1.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **3** (worst close -1.00%) · worst intraday float -0.80% · FTMO -5% breaches: **0**
- challenge walk-forward (5 starts): TIMEOUT 100%
- by month: 2026-06 -1.0% · 2026-07 -1.5%

### EURUSD_Y · variant `cci_only`

signal funnel: {'A_fire': 1136, 'A_after_force': 161, 'union_or_conc': 161, 'after_shell': 33}
- trades: **18** (1.8/trading day, 10/10 days traded) · WR **66.7%** · concurrence fires: 0
- total P&L: **-2.19%** of initial over 10 days (-4.6%/month-ish) · mean day -0.219% · median day -0.150%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **5** (worst close -1.15%) · worst intraday float -1.22% · FTMO -5% breaches: **0**
- challenge walk-forward (10 starts): TIMEOUT 100%
- by month: 2026-06 -0.8% · 2026-07 -1.8% · 2026-08 +0.4%

### EURUSD_Y · variant `mcf_only`

signal funnel: {'B_fire': 1249, 'B_after_force': 187, 'union_or_conc': 187, 'after_shell': 50}
- trades: **31** (1.5/trading day, 21/21 days traded) · WR **54.8%** · concurrence fires: 0
- total P&L: **-6.82%** of initial over 21 days (-6.8%/month-ish) · mean day -0.325% · median day +0.200%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **10** (worst close -1.50%) · worst intraday float -1.33% · FTMO -5% breaches: **0**
- challenge walk-forward (21 starts): HALT_FUSE 52%, TIMEOUT 48%
- by month: 2026-05 +0.2% · 2026-06 -1.0% · 2026-07 -5.3% · 2026-08 -0.7%
