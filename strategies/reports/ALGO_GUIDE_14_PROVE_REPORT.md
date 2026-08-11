# Algo Guide 14 — prove report

**Source HTML:** `strategies/Strategies to replicate in Algo Trading.docx.html`
**Notes:** `strategies/algo_guide_14/`
**Window:** 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1)
**Data:** `C:\Users\user\Downloads\_OTHER_PROJECTS\ATI_FTMO_project\gravity_engine\data\EURUSD_M1_export.csv`
**vectorbt:** 1.1.0
**Families proven this run:** 14
**Not Court law.**

## Baseline

| Family | Score | WR% | PF | Trades |
|--------|------:|----:|---:|-------:|
| `note__algo_guide_14_s11_keltner_reversion_md` | 3755.46 | 64.82 | 37.567 | 1939 |
| `note__algo_guide_14_s06_parabolic_sar_md` | 1329.75 | 48.51 | 13.312 | 1222 |
| `note__algo_guide_14_s10_vwap_reversion_md` | 1294.11 | 40.86 | 12.941 | 314 |
| `note__algo_guide_14_s08_bb_mean_reversion_md` | 267.42 | 49.16 | 2.680 | 920 |
| `note__algo_guide_14_s09_rsi_reversion_md` | 104.03 | 50.54 | 1.053 | 1753 |
| `note__algo_guide_14_s12_zscore_reversion_md` | 92.41 | 47.62 | 0.949 | 3991 |
| `note__algo_guide_14_s13_stochastic_reversion_md` | 88.92 | 49.36 | 0.933 | 6708 |
| `note__algo_guide_14_s14_williams_r_reversion_md` | 79.13 | 51.45 | 0.846 | 7346 |
| `note__algo_guide_14_s03_donchian_turtle_md` | 75.66 | 40.99 | 0.787 | 3042 |
| `note__algo_guide_14_s07_ema_ribbon_md` | 74.15 | 36.23 | 0.776 | 2941 |
| `note__algo_guide_14_s01_ma_crossover_md` | 73.64 | 26.49 | 0.746 | 809 |
| `note__algo_guide_14_s05_roc_momentum_md` | 72.28 | 43.15 | 0.751 | 2763 |
| `note__algo_guide_14_s02_breakout_trading_md` | 69.48 | 40.08 | 0.723 | 2231 |
| `note__algo_guide_14_s04_adx_directional_md` | 53.51 | 40.52 | 0.557 | 1611 |

## Accuracy tweaks (WR > 60.4%)

| Family | WR% | Trades | Tier | Pass |
|--------|----:|-------:|------|:----:|
| `note__algo_guide_14_s01_ma_crossover_md` | 77.44 | 133 | A_first_breath | Y |
| `note__algo_guide_14_s02_breakout_trading_md` | 74.57 | 1032 | A_first_breath | Y |
| `note__algo_guide_14_s03_donchian_turtle_md` | 74.31 | 573 | A_first_breath | Y |
| `note__algo_guide_14_s04_adx_directional_md` | 73.30 | 573 | A_first_breath | Y |
| `note__algo_guide_14_s05_roc_momentum_md` | 72.86 | 827 | A_first_breath | Y |
| `note__algo_guide_14_s06_parabolic_sar_md` | 74.70 | 305 | A_first_breath | Y |
| `note__algo_guide_14_s07_ema_ribbon_md` | 70.59 | 1585 | A_first_breath | Y |
| `note__algo_guide_14_s08_bb_mean_reversion_md` | 82.35 | 34 | C_scalp_breath | Y |
| `note__algo_guide_14_s09_rsi_reversion_md` | 76.47 | 34 | D_no_session | Y |
| `note__algo_guide_14_s10_vwap_reversion_md` | 91.04 | 480 | E_ultra_breath | Y |
| `note__algo_guide_14_s11_keltner_reversion_md` | 73.91 | 46 | A_first_breath | Y |
| `note__algo_guide_14_s12_zscore_reversion_md` | 75.74 | 136 | A_first_breath | Y |
| `note__algo_guide_14_s13_stochastic_reversion_md` | 71.00 | 408 | A_first_breath | Y |
| `note__algo_guide_14_s14_williams_r_reversion_md` | 71.69 | 560 | A_first_breath | Y |

## Monte Carlo

Sims=1000 seed=42

| Family | Trades | MC med | P(loss) |
|--------|-------:|-------:|--------:|
| `note__algo_guide_14_s01_ma_crossover_md` | 133 | 0.9997 | 51.5% |
| `note__algo_guide_14_s02_breakout_trading_md` | 1032 | 0.9580 | 96.4% |
| `note__algo_guide_14_s03_donchian_turtle_md` | 573 | 0.9711 | 96.5% |
| `note__algo_guide_14_s04_adx_directional_md` | 573 | 0.9596 | 99.0% |
| `note__algo_guide_14_s05_roc_momentum_md` | 827 | 0.9705 | 95.1% |
| `note__algo_guide_14_s06_parabolic_sar_md` | 305 | 0.9892 | 85.5% |
| `note__algo_guide_14_s07_ema_ribbon_md` | 1585 | 0.9067 | 100.0% |
| `note__algo_guide_14_s08_bb_mean_reversion_md` | 18 | 1.0000 | 49.6% |
| `note__algo_guide_14_s09_rsi_reversion_md` | 22 | 0.9959 | 84.3% |
| `note__algo_guide_14_s10_vwap_reversion_md` | 12 | 0.9950 | 95.8% |
| `note__algo_guide_14_s11_keltner_reversion_md` | 46 | 0.9953 | 86.4% |
| `note__algo_guide_14_s12_zscore_reversion_md` | 136 | 0.9916 | 90.7% |
| `note__algo_guide_14_s13_stochastic_reversion_md` | 408 | 0.9702 | 98.8% |
| `note__algo_guide_14_s14_williams_r_reversion_md` | 560 | 0.9794 | 90.2% |

## Gate checklist (guide14)

- `note__algo_guide_14_s01_ma_crossover_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s02_breakout_trading_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s03_donchian_turtle_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s04_adx_directional_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s05_roc_momentum_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s06_parabolic_sar_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s07_ema_ribbon_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s08_bb_mean_reversion_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s09_rsi_reversion_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s10_vwap_reversion_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s11_keltner_reversion_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s12_zscore_reversion_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s13_stochastic_reversion_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
- `note__algo_guide_14_s14_williams_r_reversion_md`: INV=Y · TWEAK_FILE=Y · WR_GATE=Y · MC=Y · MC_INJECT=Y
