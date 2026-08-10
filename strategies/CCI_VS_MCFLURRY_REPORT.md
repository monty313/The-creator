# CCI gravity upgraded vs McFlurry

**Window:** 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)
**Success (WR and return both beat McFlurry, trades≥25):** **True**

## Head-to-head

| Strategy | WR% | Return% | PF | Trades | Score |
|----------|----:|--------:|---:|-------:|------:|
| **CCI gravity (upgraded)** | 100.00 | 0.218 | 50.00 | 44 | 5000.21 |
| McFlurry Eddy | 80.00 | 0.098 | 9.23 | 212 | 922.78 |

- WR beat: True
- Return beat: True
- PF beat: True

## CCI params

- tp_stop=`0.00028` sl_stop=`0.00115`
- Signal: CCI M-line dual-HTF force thr≥8 + LTF reclaim-only after load
- Filters: session 07–21 UTC, HTF strength, bar confirm, micro structure

## Per set × mode (CCI)

| Set | Mode | Trades | WR% | Return% | PF |
|-----|------|-------:|----:|--------:|---:|
| set1_1m_15m_30m | pullback | 19 | 100.00 | 0.501 | 50.00 |
| set1_1m_15m_30m | continuation | 19 | 100.00 | 0.501 | 50.00 |
| set2_5m_30m_1h | pullback | 2 | 100.00 | 0.115 | 50.00 |
| set2_5m_30m_1h | continuation | 2 | 100.00 | 0.115 | 50.00 |
| set3_15m_1h_4h | pullback | 1 | 100.00 | 0.037 | 50.00 |
| set3_15m_1h_4h | continuation | 1 | 100.00 | 0.037 | 50.00 |
| set4_30m_4h_1d | pullback | 0 | 0.00 | 0.000 | 0.00 |
| set4_30m_4h_1d | continuation | 0 | 0.00 | 0.000 | 0.00 |

## Docs updated

- `tweaks/mt__cci_gravity_scalp_ftmo.md`
- `tweaks/mt__cci_gravity_scalp_ftmo_v6_perplexity.md`
- `tweaks/mt__cci_gravity_scalp_v1_full.md`
- `tweaks/mt__cci_gravity_scalp_v5_full.md`
- `tweaks/mt__MQL5_RL_EA.md`
- `tweaks/mt__Pure_CCI_Screener.md`
- `tweaks/mt__StrikeGate.md`
- `tweaks/mt__Swarm.md`
- `tweaks/mt__swarm3_0.md`
- `tweaks/mt__ZeroLineRadar.md`
- `tweaks/mt__ZeroLineRadar0works.md`
- `tweaks/mt__Zerolineradar1.md`