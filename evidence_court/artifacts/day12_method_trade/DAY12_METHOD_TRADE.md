# Day 12 — Policy traded the METHOD path

**Date:** 2026-01-21 · **Symbol:** XAUUSD  
**Mode:** METHOD (2 resume fires) · **Not** production thrash champion  
**Target:** 15.0% · **Risk:** 3.0%

## Result

| Metric | Method path | Bot thrash class |
|--------|------------:|-----------------:|
| n_trades | **2** | 50–97 |
| PnL % | **+1.418** | ~+2.9 to +3.2 |
| hit 15% | **False** | false |
| breach | **False** | false |

## Fills

| Name | Side | Entry | Exit | Hold min | Size risk % | PnL % |
|------|------|-------|------|----------:|------------:|------:|
| FIRE_1_RESUME_LAUNCH | long | 08:15:00 | 08:30:00 | 15 | 1.184 | +0.666 |
| FIRE_2_RESUME_PULLBACK | long | 09:15:00 | 09:50:00 | 35 | 1.197 | +0.752 |

## Policy log

- I am the Policy trading 2026-01-21 under METHOD (not thrash densify).
- Target=15.0%  Risk envelope=3.0%  breach must stay 0.
- Plan: 2 resume fires only. Wait Force / pullback / post-fire / done.
- WAIT [07:00:00–08:15:00]: Force on — wait for resume, no densify
- FIRE FIRE_1_RESUME_LAUNCH: long @08:15:00→08:30:00 hold=15m size_risk=1.184% lot=0.54 pnl=+0.666%  day_pnl=+0.666%
-   note: Hold launch; next 15m is NO thrash re-fire
- WAIT [08:30–08:45]: NO thrash re-fire (method hard rule).
- WAIT [08:45–09:15]: pullback vs Force — still WAIT.
- FIRE FIRE_2_RESUME_PULLBACK: long @09:15:00→09:50:00 hold=35m size_risk=1.197% lot=0.55 pnl=+0.752%  day_pnl=+1.418%
-   note: Second cycle only; then day is WAIT
- WAIT [09:50–EOD]: method day complete — no more entries.

**Lab only — not Court PROMOTE.**
