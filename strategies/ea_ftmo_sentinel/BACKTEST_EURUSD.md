# Sentinel backtest — EURUSD (Dukascopy M1, bar-accurate)

### EURUSD · variant `default`

signal funnel: {'A_fire': 1753, 'A_after_force': 302, 'B_fire': 1922, 'B_after_force': 322, 'union_or_conc': 570, 'after_mass': 244, 'after_shell': 113}
- trades: **55** (1.9/trading day, 29/114 days traded) · WR **70.9%** · concurrence fires: 7
- total P&L: **-5.12%** of initial over 114 days (-0.9%/month-ish) · mean day -0.045% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **12** (worst close -1.50%) · worst intraday float -1.49% · FTMO -5% breaches: **0**
- challenge walk-forward (114 starts): TIMEOUT 100%
- by month: 2026-01 -1.0% · 2026-02 -0.2% · 2026-03 -0.6% · 2026-04 -2.6% · 2026-05 -0.7%

### EURUSD · variant `no_mass`

signal funnel: {'A_fire': 1753, 'A_after_force': 302, 'B_fire': 1922, 'B_after_force': 322, 'union_or_conc': 570, 'after_shell': 264}
- trades: **122** (2.2/trading day, 55/114 days traded) · WR **73.8%** · concurrence fires: 13
- total P&L: **-7.53%** of initial over 114 days (-1.4%/month-ish) · mean day -0.066% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **25** (worst close -1.50%) · worst intraday float -1.49% · FTMO -5% breaches: **0**
- challenge walk-forward (114 starts): HALT_FUSE 20%, TIMEOUT 80%
- by month: 2026-01 -2.1% · 2026-02 +0.9% · 2026-03 +0.7% · 2026-04 -5.3% · 2026-05 -1.8%

### EURUSD · variant `cci_only`

signal funnel: {'A_fire': 1753, 'A_after_force': 302, 'union_or_conc': 302, 'after_shell': 130}
- trades: **66** (1.6/trading day, 41/114 days traded) · WR **75.8%** · concurrence fires: 0
- total P&L: **-2.60%** of initial over 114 days (-0.5%/month-ish) · mean day -0.023% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **15** (worst close -1.30%) · worst intraday float -1.30% · FTMO -5% breaches: **0**
- challenge walk-forward (114 starts): TIMEOUT 100%
- by month: 2026-01 -1.2% · 2026-02 +0.5% · 2026-03 -0.5% · 2026-04 -2.5% · 2026-05 +1.1%

### EURUSD · variant `cci_mass`

signal funnel: {'A_fire': 1753, 'A_after_force': 302, 'union_or_conc': 302, 'after_mass': 117, 'after_shell': 49}
- trades: **23** (1.4/trading day, 17/114 days traded) · WR **69.6%** · concurrence fires: 0
- total P&L: **-2.41%** of initial over 114 days (-0.4%/month-ish) · mean day -0.021% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **7** (worst close -0.80%) · worst intraday float -0.97% · FTMO -5% breaches: **0**
- challenge walk-forward (114 starts): TIMEOUT 100%
- by month: 2026-01 -0.8% · 2026-02 +0.0% · 2026-03 -0.4% · 2026-04 -2.3% · 2026-05 +1.0%

### EURUSD · variant `mcf_only`

signal funnel: {'B_fire': 1922, 'B_after_force': 322, 'union_or_conc': 322, 'after_shell': 162}
- trades: **80** (1.8/trading day, 45/114 days traded) · WR **73.8%** · concurrence fires: 0
- total P&L: **-3.65%** of initial over 114 days (-0.7%/month-ish) · mean day -0.032% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **15** (worst close -1.50%) · worst intraday float -1.49% · FTMO -5% breaches: **0**
- challenge walk-forward (114 starts): TIMEOUT 100%
- by month: 2026-01 -2.4% · 2026-02 +1.3% · 2026-03 +1.1% · 2026-04 -1.8% · 2026-05 -1.8%

### EURUSD · variant `a15`

signal funnel: {'A_fire': 581, 'A_after_force': 100, 'union_or_conc': 100, 'after_shell': 42}
- trades: **23** (1.1/trading day, 20/114 days traded) · WR **56.5%** · concurrence fires: 0
- total P&L: **-0.91%** of initial over 114 days (-0.2%/month-ish) · mean day -0.008% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 0
- red traded days: **10** (worst close -0.80%) · worst intraday float -0.79% · FTMO -5% breaches: **0**
- challenge walk-forward (114 starts): TIMEOUT 100%
- by month: 2026-01 -0.8% · 2026-02 -0.4% · 2026-03 +0.8% · 2026-04 -0.4% · 2026-05 -0.0%

### EURUSD · variant `a15w`

signal funnel: {'A_fire': 581, 'A_after_force': 100, 'union_or_conc': 100, 'after_shell': 42}
- trades: **23** (1.1/trading day, 20/114 days traded) · WR **34.8%** · concurrence fires: 0
- total P&L: **-1.43%** of initial over 114 days (-0.3%/month-ish) · mean day -0.013% · median day +0.000%
- P(day >= +2.5%): **0.0%** of traded days · banked-green days: 2
- red traded days: **12** (worst close -1.20%) · worst intraday float -1.16% · FTMO -5% breaches: **0**
- challenge walk-forward (114 starts): TIMEOUT 100%
- by month: 2026-01 -0.9% · 2026-02 +1.1% · 2026-03 +2.3% · 2026-04 -3.2% · 2026-05 -0.7%
