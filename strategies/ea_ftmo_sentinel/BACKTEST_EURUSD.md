# Sentinel backtest — EURUSD (Dukascopy M1, bar-accurate)

### EURUSD · variant `default`

signal funnel: {'A_fire': 2867, 'A_after_force': 493, 'B_fire': 3120, 'B_after_force': 518, 'union_or_conc': 925, 'after_mass': 408, 'after_shell': 176}
- trades: **77** (1.8/trading day, 43/183 days traded) · WR **67.5%** · concurrence fires: 9
- total P&L: **-9.50%** of initial over 183 days (-1.1%/month-ish) · mean day -0.052% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **20** (worst close -1.50%) · worst intraday float -1.49% · FTMO -5% breaches: **0**
- challenge walk-forward (183 starts): TIMEOUT 100%
- by month: 2026-01 -1.0% · 2026-02 -0.2% · 2026-03 -0.6% · 2026-04 -2.6% · 2026-05 -0.8% · 2026-06 -1.5% · 2026-07 -2.8% · 2026-08 +0.0%

### EURUSD · variant `no_mass`

signal funnel: {'A_fire': 2867, 'A_after_force': 493, 'B_fire': 3120, 'B_after_force': 518, 'union_or_conc': 925, 'after_shell': 404}
- trades: **186** (2.2/trading day, 85/183 days traded) · WR **70.4%** · concurrence fires: 20
- total P&L: **-18.49%** of initial over 183 days (-2.1%/month-ish) · mean day -0.101% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **42** (worst close -1.50%) · worst intraday float -1.49% · FTMO -5% breaches: **0**
- challenge walk-forward (183 starts): HALT_FUSE 37%, TIMEOUT 63%
- by month: 2026-01 -2.1% · 2026-02 +0.9% · 2026-03 +0.7% · 2026-04 -5.3% · 2026-05 -2.2% · 2026-06 -4.4% · 2026-07 -4.1% · 2026-08 -2.0%

### EURUSD · variant `cci_only`

signal funnel: {'A_fire': 2867, 'A_after_force': 493, 'union_or_conc': 493, 'after_shell': 194}
- trades: **99** (1.7/trading day, 58/183 days traded) · WR **71.7%** · concurrence fires: 0
- total P&L: **-8.07%** of initial over 183 days (-0.9%/month-ish) · mean day -0.044% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **25** (worst close -1.30%) · worst intraday float -1.30% · FTMO -5% breaches: **0**
- challenge walk-forward (183 starts): TIMEOUT 100%
- by month: 2026-01 -1.2% · 2026-02 +0.5% · 2026-03 -0.5% · 2026-04 -2.5% · 2026-05 +0.2% · 2026-06 -1.2% · 2026-07 -1.4% · 2026-08 -2.0%

### EURUSD · variant `cci_mass`

signal funnel: {'A_fire': 2867, 'A_after_force': 493, 'union_or_conc': 493, 'after_mass': 195, 'after_shell': 76}
- trades: **33** (1.4/trading day, 24/183 days traded) · WR **69.7%** · concurrence fires: 0
- total P&L: **-3.29%** of initial over 183 days (-0.4%/month-ish) · mean day -0.018% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **10** (worst close -0.80%) · worst intraday float -0.97% · FTMO -5% breaches: **0**
- challenge walk-forward (183 starts): TIMEOUT 100%
- by month: 2026-01 -0.8% · 2026-02 +0.0% · 2026-03 -0.4% · 2026-04 -2.3% · 2026-05 +0.9% · 2026-06 +0.4% · 2026-07 -1.2% · 2026-08 +0.0%

### EURUSD · variant `mcf_only`

signal funnel: {'B_fire': 3120, 'B_after_force': 518, 'union_or_conc': 518, 'after_shell': 255}
- trades: **127** (1.8/trading day, 69/183 days traded) · WR **68.5%** · concurrence fires: 0
- total P&L: **-12.51%** of initial over 183 days (-1.4%/month-ish) · mean day -0.068% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **28** (worst close -1.50%) · worst intraday float -1.49% · FTMO -5% breaches: **0**
- challenge walk-forward (183 starts): HALT_FUSE 16%, TIMEOUT 84%
- by month: 2026-01 -2.4% · 2026-02 +1.3% · 2026-03 +1.1% · 2026-04 -1.8% · 2026-05 -1.5% · 2026-06 -3.6% · 2026-07 -4.7% · 2026-08 -0.8%

### EURUSD · variant `a15`

signal funnel: {'A_fire': 938, 'A_after_force': 158, 'union_or_conc': 158, 'after_shell': 68}
- trades: **37** (1.1/trading day, 34/183 days traded) · WR **56.8%** · concurrence fires: 0
- total P&L: **-0.91%** of initial over 183 days (-0.1%/month-ish) · mean day -0.005% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **16** (worst close -0.80%) · worst intraday float -0.79% · FTMO -5% breaches: **0**
- challenge walk-forward (183 starts): TIMEOUT 100%
- by month: 2026-01 -0.8% · 2026-02 -0.4% · 2026-03 +0.8% · 2026-04 -0.4% · 2026-05 -0.2% · 2026-06 -1.4% · 2026-07 +1.0% · 2026-08 +0.6%

### EURUSD · variant `a15w`

signal funnel: {'A_fire': 938, 'A_after_force': 158, 'union_or_conc': 158, 'after_shell': 68}
- trades: **37** (1.1/trading day, 34/183 days traded) · WR **35.1%** · concurrence fires: 0
- total P&L: **-3.15%** of initial over 183 days (-0.4%/month-ish) · mean day -0.017% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 2
- red traded days: **21** (worst close -1.20%) · worst intraday float -1.16% · FTMO -5% breaches: **0**
- challenge walk-forward (183 starts): TIMEOUT 100%
- by month: 2026-01 -0.9% · 2026-02 +1.1% · 2026-03 +2.3% · 2026-04 -3.2% · 2026-05 -0.1% · 2026-06 -1.8% · 2026-07 -1.1% · 2026-08 +0.6%
