# Sentinel backtest — EURUSD (Dukascopy M1, bar-accurate)

### EURUSD · variant `no_mass`

signal funnel: {'A_fire': 205, 'A_after_force': 9, 'B_fire': 206, 'B_after_force': 22, 'union_or_conc': 29, 'after_shell': 12}
- trades: **6** (3.0/trading day, 2/2 days traded) · WR **50.0%** · concurrence fires: 0
- total P&L: **-1.06%** of initial over 2 days (-11.2%/month-ish) · mean day -0.531% · median day -0.531%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **1** (worst close -1.50%) · worst intraday float -1.47% · FTMO -5% breaches: **0**
- challenge walk-forward (2 starts): TIMEOUT 100%
- by month: 2026-01 -1.1%

### EURUSD · variant `conc_only`

signal funnel: {'A_fire': 205, 'A_after_force': 9, 'B_fire': 206, 'B_after_force': 22, 'union_or_conc': 2, 'after_shell': 0}
**NO TRADES** — gates never opened on this window.

### EURUSD · variant `cci_only`

signal funnel: {'A_fire': 205, 'A_after_force': 9, 'union_or_conc': 9, 'after_shell': 4}
- trades: **4** (4.0/trading day, 1/1 days traded) · WR **50.0%** · concurrence fires: 0
- total P&L: **-1.30%** of initial over 1 days (-27.3%/month-ish) · mean day -1.300% · median day -1.300%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **1** (worst close -1.30%) · worst intraday float -1.30% · FTMO -5% breaches: **0**
- challenge walk-forward (1 starts): TIMEOUT 100%
- by month: 2026-01 -1.3%

### EURUSD · variant `mcf_only`

signal funnel: {'B_fire': 206, 'B_after_force': 22, 'union_or_conc': 22, 'after_shell': 8}
- trades: **5** (2.5/trading day, 2/2 days traded) · WR **40.0%** · concurrence fires: 0
- total P&L: **-0.96%** of initial over 2 days (-10.1%/month-ish) · mean day -0.481% · median day -0.481%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **1** (worst close -1.40%) · worst intraday float -1.39% · FTMO -5% breaches: **0**
- challenge walk-forward (2 starts): TIMEOUT 100%
- by month: 2026-01 -1.0%
