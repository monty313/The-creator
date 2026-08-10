# Strategy batch test report — **1:1 no-collapse** (every MT name + every note)

**Not Court law.** Each MT index name and each strategy note is its **own family** (no merges).

## Run configuration

| Field | Value |
|-------|-------|
| Symbol | `EURUSD` |
| Data | `C:\Users\user\Downloads\_OTHER_PROJECTS\ATI_FTMO_project\gravity_engine\data\EURUSD_M1_export.csv` |
| Window | 2026-06-10 03:48:00 → 2026-07-17 22:27:00 (40000 M1 bars) |
| MT names | 95 |
| Note files | 28 |
| Total families (1:1) | 123 |
| Collapse entries | 0 (must be 0) |
| Sets | `set1_1m_15m_30m, set2_5m_30m_1h, set3_15m_1h_4h, set4_30m_4h_1d` |
| Modes | `pullback`, `continuation` |
| Hold bars | 12 |
| vectorbt | 1.1.0 |
| Primary sort | `score = 100*PF + avg_return% - 0.25*|maxDD%|` |

## Ranking (most accurate/profitable → least)

| Rank | Family id | Title | Kind | Score | PF | Return% | MaxDD% | Win% | Trades |
|-----:|-----------|-------|------|------:|---:|--------:|-------:|-----:|-------:|
| 1 | `mt__cci_gravity_scalp_ftmo` | cci_gravity_scalp_ftmo | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 2 | `mt__cci_gravity_scalp_ftmo_v6_perplexity` | cci_gravity_scalp_ftmo_v6_perplexity | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 3 | `mt__cci_gravity_scalp_v1_full` | cci_gravity_scalp_v1_full | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 4 | `mt__cci_gravity_scalp_v5_full` | cci_gravity_scalp_v5_full | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 5 | `mt__MQL5_RL_EA` | MQL5 RL EA | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 6 | `mt__Pure_CCI_Screener` | Pure_CCI_Screener | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 7 | `mt__StrikeGate` | StrikeGate | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 8 | `mt__Swarm` | Swarm | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 9 | `mt__swarm3_0` | swarm3.0 | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 10 | `mt__ZeroLineRadar` | ZeroLineRadar | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 11 | `mt__ZeroLineRadar0works` | ZeroLineRadar0works | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 12 | `mt__Zerolineradar1` | Zerolineradar1 | mt | 1305.99 | 13.075 | -1.152 | 1.552 | 52.10 | 1387 |
| 13 | `note__the_truth_main_extra_ADR-0004-strategies_md` | ADR-0004-strategies.md | note | 99.71 | 1.024 | -2.022 | 2.825 | 45.27 | 3210 |
| 14 | `note__the_truth_main_extra_strategy_S1_cci_slingshot_md` | strategy_S1_cci_slingshot.md | note | 99.71 | 1.024 | -2.022 | 2.825 | 45.27 | 3210 |
| 15 | `note__army_snap8_STRATEGY_md` | STRATEGY.md | note | 88.25 | 0.896 | -0.958 | 1.503 | 41.26 | 1291 |
| 16 | `mt__JordanMomentumScreener_v10` | JordanMomentumScreener_v10 | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 17 | `mt__JordanMomentumScreener_v11` | JordanMomentumScreener_v11 | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 18 | `mt__JordanMomentumScreener_v2_MT5` | JordanMomentumScreener_v2_MT5 | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 19 | `mt__JordanMomentumScreener_v4_MT5` | JordanMomentumScreener_v4_MT5 | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 20 | `mt__JordanMomentumScreener_v5_MT5` | JordanMomentumScreener_v5_MT5 | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 21 | `mt__JordanMomentumScreener_v7_HUD` | JordanMomentumScreener_v7_HUD | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 22 | `mt__JordanMomentumScreener_v8_HUD` | JordanMomentumScreener_v8_HUD | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 23 | `mt__JordanMomentumScreener_v9_HUD` | JordanMomentumScreener_v9_HUD | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 24 | `mt__JordanMomentumScreener_v9_Wave` | JordanMomentumScreener_v9_Wave | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 25 | `mt__Momentum_Matrix_Screener` | Momentum_Matrix_Screener | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 26 | `mt__play_4_2` | play 4.2 | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 27 | `mt__play_4_3` | play 4.3 | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 28 | `mt__Unity_Play` | Unity Play | mt | 82.53 | 0.856 | -2.308 | 3.024 | 46.95 | 3121 |
| 29 | `mt__FTMO_DQN` | @@FTMO_DQN@@ | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 30 | `mt__agent_teacher` | agent teacher | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 31 | `mt__AutoTradingBot_RF` | AutoTradingBot_RF | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 32 | `mt__FTMO_DQN_2` | FTMO_DQN | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 33 | `mt__MetaLearningEA` | MetaLearningEA | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 34 | `mt__MultiTimeframe_LRL_BB_CCI_Screener` | MultiTimeframe_LRL_BB_CCI_Screener | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 35 | `mt__MultiTimeframe_LRL_BB_CCI_Screener_v2` | MultiTimeframe_LRL_BB_CCI_Screener_v2 | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 36 | `mt__MultiTimeframe_NN_EA` | MultiTimeframe_NN_EA | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 37 | `mt__MultiTimeframe_NN_EA_v2` | MultiTimeframe_NN_EA_v2 | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 38 | `mt__NeuralNetworkScreener` | NeuralNetworkScreener | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 39 | `mt__NeuralNetworkScreener_Simple` | NeuralNetworkScreener_Simple | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 40 | `mt__NeuralNetworkScreener_Simple_Updated` | NeuralNetworkScreener_Simple_Updated | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 41 | `mt__NN_CCI_Screener` | NN_CCI_Screener | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 42 | `mt__NN_CCI_Screener_Simple` | NN_CCI_Screener_Simple | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 43 | `mt__OnlineLearnerEA` | OnlineLearnerEA | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 44 | `mt__OnlineLearnerEA_v5_Fixed` | OnlineLearnerEA_v5_Fixed | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 45 | `mt__PDF_MultiStrategy_MTF_EA_v1` | PDF_MultiStrategy_MTF_EA_v1 | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 46 | `mt__PDF_MultiStrategy_MTF_EA_v2` | PDF_MultiStrategy_MTF_EA_v2 | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 47 | `mt__PDF_MultiStrategy_VotingForest_EA_v4` | PDF_MultiStrategy_VotingForest_EA_v4 | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 48 | `mt__RegressionlineEA` | RegressionlineEA | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 49 | `mt__RL_PropTrader_Final` | RL_PropTrader_Final | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 50 | `mt__RL_PropTrader_MVP_v2` | RL_PropTrader_MVP_v2 | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 51 | `mt__rsi_bb_extreme` | rsi_bb_extreme | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 52 | `mt__to_opimize_ea` | to opimize ea | mt | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 53 | `note__local_desktop_new_trading_strategies_1_md` | new_trading_strategies (1).md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 54 | `note__local_desktop_new_trading_strategies_md` | new_trading_strategies.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 55 | `note__local_desktop_rsi_bb_strategy_txt` | rsi + bb strategy.txt | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 56 | `note__local_desktop_section-1_md` | section-1.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 57 | `note__local_desktop_section-2_md` | section-2.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 58 | `note__local_desktop_section-3_md` | section-3.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 59 | `note__local_desktop_section-4_md` | section-4.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 60 | `note__local_desktop_section-5_md` | section-5.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 61 | `note__local_desktop_section-6_md` | section-6.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 62 | `note__local_desktop_section-8_md` | section-8.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 63 | `note__army_library_strategy_copy_new_trading_strategies_1_md` | new_trading_strategies (1).md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 64 | `note__army_library_strategy_copy_new_trading_strategies_md` | new_trading_strategies.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 65 | `note__army_library_strategy_copy_rsi_bb_strategy_txt` | rsi + bb strategy.txt | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 66 | `note__army_library_strategy_copy_section-1_md` | section-1.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 67 | `note__army_library_strategy_copy_section-2_md` | section-2.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 68 | `note__army_library_strategy_copy_section-3_md` | section-3.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 69 | `note__army_library_strategy_copy_section-4_md` | section-4.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 70 | `note__army_library_strategy_copy_section-5_md` | section-5.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 71 | `note__army_library_strategy_copy_section-6_md` | section-6.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 72 | `note__army_library_strategy_copy_section-8_md` | section-8.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 73 | `note__mark_doctrine_refs_RSI_BB_L2L_SKILL_md` | RSI_BB_L2L_SKILL.md | note | 77.23 | 0.820 | -3.621 | 4.412 | 46.64 | 5062 |
| 74 | `mt__crossenteopy` | crossenteopy | mt | 77.11 | 0.803 | -2.463 | 2.999 | 44.13 | 2997 |
| 75 | `mt__kmeans` | kmeans | mt | 77.11 | 0.803 | -2.463 | 2.999 | 44.13 | 2997 |
| 76 | `mt__MACD_Sample` | MACD Sample | mt | 77.11 | 0.803 | -2.463 | 2.999 | 44.13 | 2997 |
| 77 | `mt__PerceptronEA` | PerceptronEA | mt | 77.11 | 0.803 | -2.463 | 2.999 | 44.13 | 2997 |
| 78 | `mt__Q-learning` | Q-learning | mt | 77.11 | 0.803 | -2.463 | 2.999 | 44.13 | 2997 |
| 79 | `mt__some_bs` | some bs | mt | 77.11 | 0.803 | -2.463 | 2.999 | 44.13 | 2997 |
| 80 | `mt__some_bullshit` | some bullshit | mt | 77.11 | 0.803 | -2.463 | 2.999 | 44.13 | 2997 |
| 81 | `mt__FTMO_SMA_Scalper` | FTMO_SMA_Scalper | mt | 74.48 | 0.761 | -1.205 | 1.686 | 42.21 | 1412 |
| 82 | `mt__SMA_Fan_MTF_BBExit_v1` | SMA_Fan_MTF_BBExit_v1 | mt | 74.48 | 0.761 | -1.205 | 1.686 | 42.21 | 1412 |
| 83 | `mt__TriTF_SMA_Shift_Optimizer_EA` | TriTF_SMA_Shift_Optimizer_EA | mt | 74.48 | 0.761 | -1.205 | 1.686 | 42.21 | 1412 |
| 84 | `mt__MA_ribbon_filled_Alerts` | MA ribbon filled_Alerts | mt | 74.15 | 0.776 | -2.644 | 3.339 | 36.23 | 2941 |
| 85 | `mt__ATI_FTMO_EA` | ATI_FTMO_EA | mt | 72.39 | 0.754 | -2.326 | 2.667 | 42.56 | 2998 |
| 86 | `mt__FTMO_Challenge_EA` | FTMO_Challenge_EA | mt | 72.39 | 0.754 | -2.326 | 2.667 | 42.56 | 2998 |
| 87 | `mt__FTMO_Challenge_EA_FULL` | FTMO_Challenge_EA_FULL | mt | 72.39 | 0.754 | -2.326 | 2.667 | 42.56 | 2998 |
| 88 | `mt__ftmo_challenge_ea_v3` | ftmo_challenge_ea_v3 | mt | 72.39 | 0.754 | -2.326 | 2.667 | 42.56 | 2998 |
| 89 | `mt__FTMO_Challenge_v4` | FTMO_Challenge_v4 | mt | 72.39 | 0.754 | -2.326 | 2.667 | 42.56 | 2998 |
| 90 | `mt__FtmoDecisionTree` | FtmoDecisionTree | mt | 72.39 | 0.754 | -2.326 | 2.667 | 42.56 | 2998 |
| 91 | `mt__S11_Runner` | S11_Runner | mt | 72.39 | 0.754 | -2.326 | 2.667 | 42.56 | 2998 |
| 92 | `mt__Linear_Regression_Screener` | Linear_Regression_Screener | mt | 70.13 | 0.714 | -0.899 | 1.340 | 42.89 | 1043 |
| 93 | `mt__LinearRegressionLine` | LinearRegressionLine | mt | 70.13 | 0.714 | -0.899 | 1.340 | 42.89 | 1043 |
| 94 | `mt__LinearRegressionRSI_EA` | LinearRegressionRSI_EA | mt | 70.13 | 0.714 | -0.899 | 1.340 | 42.89 | 1043 |
| 95 | `mt__AutoGKCloseIntegral` | AutoGKCloseIntegral | mt | 68.84 | 0.740 | -3.945 | 4.797 | 40.40 | 4675 |
| 96 | `mt__ErrorRatePlot` | ErrorRatePlot | mt | 68.84 | 0.740 | -3.945 | 4.797 | 40.40 | 4675 |
| 97 | `mt__Moving_Average` | Moving Average | mt | 68.84 | 0.740 | -3.945 | 4.797 | 40.40 | 4675 |
| 98 | `mt__Slope_Screener` | Slope_Screener | mt | 68.84 | 0.740 | -3.945 | 4.797 | 40.40 | 4675 |
| 99 | `mt__Slope_Screener_Fixed` | Slope_Screener_Fixed | mt | 68.84 | 0.740 | -3.945 | 4.797 | 40.40 | 4675 |
| 100 | `mt__fasg_trendday_ea` | fasg_trendday_ea | mt | 66.91 | 0.717 | -3.761 | 4.207 | 40.49 | 4559 |
| 101 | `mt__CoolBollingerTrendEA` | CoolBollingerTrendEA | mt | 65.60 | 0.690 | -2.617 | 3.037 | 43.03 | 2845 |
| 102 | `mt__coolboolinger` | coolboolinger | mt | 65.60 | 0.690 | -2.617 | 3.037 | 43.03 | 2845 |
| 103 | `mt__CCI_ShiftedSMA_Signal_3D` | CCI_ShiftedSMA_Signal_3D | mt | 63.92 | 0.676 | -2.799 | 3.434 | 42.56 | 3086 |
| 104 | `mt__fixed_FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323` | fixed_FTMO_BB_MTF_EA_Strategy4_v2_202607 | mt | 60.89 | 0.620 | -0.816 | 1.126 | 35.31 | 915 |
| 105 | `mt__FTMO_BB_MTF_EA_Strategy4` | FTMO_BB_MTF_EA_Strategy4 | mt | 60.89 | 0.620 | -0.816 | 1.126 | 35.31 | 915 |
| 106 | `mt__FTMO_BB_MTF_EA_Strategy4_20260705_1210` | FTMO_BB_MTF_EA_Strategy4_20260705_1210 | mt | 60.89 | 0.620 | -0.816 | 1.126 | 35.31 | 915 |
| 107 | `mt__FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323` | FTMO_BB_MTF_EA_Strategy4_v2_20260705_132 | mt | 60.89 | 0.620 | -0.816 | 1.126 | 35.31 | 915 |
| 108 | `mt__FTMO_BB_MTF_EA_Strategy4_v5` | FTMO_BB_MTF_EA_Strategy4_v5 | mt | 60.89 | 0.620 | -0.816 | 1.126 | 35.31 | 915 |
| 109 | `mt__FTMO_BB_MTF_EA_Strategy4_v6` | FTMO_BB_MTF_EA_Strategy4_v6 | mt | 60.89 | 0.620 | -0.816 | 1.126 | 35.31 | 915 |
| 110 | `mt__FTMO_BB_MTF_EA_Strategy4_v7` | FTMO_BB_MTF_EA_Strategy4_v7 | mt | 60.89 | 0.620 | -0.816 | 1.126 | 35.31 | 915 |
| 111 | `mt__FTMO_CCI_MTF_BB_EA_Part2` | FTMO_CCI_MTF_BB_EA_Part2 | mt | 60.89 | 0.620 | -0.816 | 1.126 | 35.31 | 915 |
| 112 | `mt__FTMO_CCI_MTF_BB_EA_PART3` | FTMO_CCI_MTF_BB_EA_PART3 | mt | 60.89 | 0.620 | -0.816 | 1.126 | 35.31 | 915 |
| 113 | `note__the_truth_main_extra_strategy_S4_rsi_tension_snap_md` | strategy_S4_rsi_tension_snap.md | note | 60.30 | 0.625 | -1.649 | 2.163 | 39.76 | 1874 |
| 114 | `mt__KineticEdgeEA` | KineticEdgeEA | mt | 59.91 | 0.622 | -1.726 | 2.131 | 42.14 | 1665 |
| 115 | `note__the_truth_main_extra_strategy_S2_bb_trend_reversion_md` | strategy_S2_bb_trend_reversion.md | note | 59.18 | 0.609 | -1.341 | 1.529 | 35.53 | 1205 |
| 116 | `mt__ftmo_ultra` | ftmo ultra | mt | 42.67 | 0.438 | -0.819 | 1.247 | 25.38 | 1163 |
| 117 | `mt__ftmo_all_assets_momentum_scalper` | ftmo_all_assets_momentum_scalper | mt | 42.67 | 0.438 | -0.819 | 1.247 | 25.38 | 1163 |
| 118 | `mt__HurstX` | HurstX | mt | 42.67 | 0.438 | -0.819 | 1.247 | 25.38 | 1163 |
| 119 | `mt__Momentum` | Momentum | mt | 42.67 | 0.438 | -0.819 | 1.247 | 25.38 | 1163 |
| 120 | `mt__Simple_scalper` | Simple scalper | mt | 42.67 | 0.438 | -0.819 | 1.247 | 25.38 | 1163 |
| 121 | `mt__US30_ExpansionTrigger_v1` | US30_ExpansionTrigger_v1 | mt | 42.67 | 0.438 | -0.819 | 1.247 | 25.38 | 1163 |
| 122 | `note__the_truth_main_extra_strategy_S3_envelope_breakout_md` | strategy_S3_envelope_breakout.md | note | 40.35 | 0.417 | -1.025 | 1.246 | 32.00 | 730 |
| 123 | `note__local_desktop_factory_full_GV-014-XAU-L1_md` | GV-014-XAU-L1.md | note | 33.58 | 0.353 | -1.276 | 1.609 | 21.07 | 1398 |

## Per-family detail

### 1. `mt__cci_gravity_scalp_ftmo`

- **Title:** cci_gravity_scalp_ftmo
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: cci_gravity_scalp_ftmo (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `cci_gravity_scalp_ftmo`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 2. `mt__cci_gravity_scalp_ftmo_v6_perplexity`

- **Title:** cci_gravity_scalp_ftmo_v6_perplexity
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: cci_gravity_scalp_ftmo_v6_perplexity (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `cci_gravity_scalp_ftmo_v6_perplexity`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 3. `mt__cci_gravity_scalp_v1_full`

- **Title:** cci_gravity_scalp_v1_full
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: cci_gravity_scalp_v1_full (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `cci_gravity_scalp_v1_full`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 4. `mt__cci_gravity_scalp_v5_full`

- **Title:** cci_gravity_scalp_v5_full
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: cci_gravity_scalp_v5_full (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `cci_gravity_scalp_v5_full`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 5. `mt__MQL5_RL_EA`

- **Title:** MQL5 RL EA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: MQL5 RL EA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `MQL5 RL EA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 6. `mt__Pure_CCI_Screener`

- **Title:** Pure_CCI_Screener
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Pure_CCI_Screener (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `Pure_CCI_Screener`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 7. `mt__StrikeGate`

- **Title:** StrikeGate
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: StrikeGate (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `StrikeGate`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 8. `mt__Swarm`

- **Title:** Swarm
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Swarm (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `Swarm`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 9. `mt__swarm3_0`

- **Title:** swarm3.0
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: swarm3.0 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `swarm3.0`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 10. `mt__ZeroLineRadar`

- **Title:** ZeroLineRadar
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: ZeroLineRadar (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `ZeroLineRadar`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 11. `mt__ZeroLineRadar0works`

- **Title:** ZeroLineRadar0works
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: ZeroLineRadar0works (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `ZeroLineRadar0works`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 12. `mt__Zerolineradar1`

- **Title:** Zerolineradar1
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Zerolineradar1 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cci_gravity`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 1305.9886

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.151934 |
| Max Drawdown [%] (avg) | 1.551517 |
| Win Rate [%] (avg) | 52.103064 |
| Profit Factor (avg) | 13.075284 |
| Sharpe (avg) | -5.133605 |
| Sortino (avg) | -6.426501 |
| Calmar (avg) | 1.115960 |
| Total Trades (sum) | 1387 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 552 | -3.7641 | 3.8226 | 36.78 | 0.514 | -19.163 |  |
| set1_1m_15m_30m | pullback | 516 | -2.7642 | 2.8844 | 41.09 | 0.597 | -14.420 |  |
| set2_5m_30m_1h | continuation | 127 | -0.9510 | 1.4453 | 45.67 | 0.706 | -5.056 |  |
| set2_5m_30m_1h | pullback | 121 | -1.9395 | 2.0221 | 47.11 | 0.507 | -7.756 |  |
| set3_15m_1h_4h | continuation | 39 | 0.0807 | 0.8772 | 43.59 | 1.050 | 0.354 |  |
| set3_15m_1h_4h | pullback | 22 | -0.5285 | 1.0111 | 45.45 | 0.635 | -3.247 |  |
| set4_30m_4h_1d | continuation | 7 | 0.1899 | 0.1939 | 57.14 | 1.594 | 1.651 |  |
| set4_30m_4h_1d | pullback | 3 | 0.4612 | 0.1555 | 100.00 | 99.000 | 6.569 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9723.579526764477
Total Return [%]: -2.764204732355229
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 203.27454393000093
Max Drawdown [%]: 2.8844284893840153
Max Drawdown Duration: 0.0
Total Trades: 516
Total Closed Trades: 516
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.08527131782946
Best Trade [%]: 0.11527663369866599
Worst Trade [%]: -0.28327385927830606
Avg Winning Trade [%]: 0.01963999914243639
Avg Losing Trade [%]: -0.022908564670891505
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5972525966785928
Expectancy: -0.5356985915416712
Sharpe Ratio: -14.420243722232373
Calmar Ratio: -10.684554722383277
Omega Ratio: 0.8666434627073444
Sortino Ratio: -19.91942196536785
```

#### RL teaching value (not hard-coded instructions)

Measured score=1305.99, PF=13.075, avg return%=-1.152, trades=1387 over 8 set×mode runs. Fidelity=medium; profile=cci_gravity. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `Zerolineradar1`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cci_gravity` rules.

### 13. `note__the_truth_main_extra_ADR-0004-strategies_md`

- **Title:** ADR-0004-strategies.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\the_truth_main_extra\ADR-0004-strategies.md`
- **Adapter profile (logic only; family not collapsed):** `truth_s1_cci`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 99.7065

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.022395 |
| Max Drawdown [%] (avg) | 2.825315 |
| Win Rate [%] (avg) | 45.269924 |
| Profit Factor (avg) | 1.024352 |
| Sharpe (avg) | -6.893905 |
| Sortino (avg) | -9.036393 |
| Calmar (avg) | -1.724904 |
| Total Trades (sum) | 3210 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1741 | -8.3913 | 8.5706 | 34.54 | 0.574 | -26.854 |  |
| set1_1m_15m_30m | pullback | 726 | -3.5657 | 3.8910 | 41.05 | 0.611 | -15.293 |  |
| set2_5m_30m_1h | continuation | 394 | -3.2878 | 3.9288 | 37.82 | 0.653 | -9.545 |  |
| set2_5m_30m_1h | pullback | 156 | 0.4687 | 0.9154 | 46.15 | 1.135 | 1.938 |  |
| set3_15m_1h_4h | continuation | 106 | -1.2140 | 2.6507 | 46.23 | 0.763 | -3.244 |  |
| set3_15m_1h_4h | pullback | 42 | -0.9351 | 1.2490 | 47.62 | 0.557 | -5.616 |  |
| set4_30m_4h_1d | continuation | 31 | 0.0408 | 0.9060 | 51.61 | 1.024 | 0.203 |  |
| set4_30m_4h_1d | pullback | 14 | 0.7053 | 0.4911 | 57.14 | 2.877 | 3.259 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9643.42689265155
Total Return [%]: -3.565731073484494
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 285.47304750884
Max Drawdown [%]: 3.890960814703877
Max Drawdown Duration: 0.0
Total Trades: 726
Total Closed Trades: 726
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.04683195592286
Best Trade [%]: 0.18099830365598
Worst Trade [%]: -0.12128402567955233
Avg Winning Trade [%]: 0.01911508207480703
Avg Losing Trade [%]: -0.021785475887887405
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.6112546013898824
Expectancy: -0.4911475307830311
Sharpe Ratio: -15.29250707305942
Calmar Ratio: -9.753502358398537
Omega Ratio: 0.8789514156561635
Sortino Ratio: -21.196122928057743
```

#### RL teaching value (not hard-coded instructions)

Measured score=99.71, PF=1.024, avg return%=-2.022, trades=3210 over 8 set×mode runs. Fidelity=medium; profile=truth_s1_cci. Truth-line geometry (CCI/BB/envelope/RSI snap) is good state/label material for L2L; do not freeze thresholds as production law.

#### 10× better

10× for `ADR-0004-strategies.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`truth_s1_cci` rules.

### 14. `note__the_truth_main_extra_strategy_S1_cci_slingshot_md`

- **Title:** strategy_S1_cci_slingshot.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\the_truth_main_extra\strategy_S1_cci_slingshot.md`
- **Adapter profile (logic only; family not collapsed):** `truth_s1_cci`
- **Fidelity:** high
- **Collapses:** `[]` (empty)
- **Aggregate score:** 99.7065

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.022395 |
| Max Drawdown [%] (avg) | 2.825315 |
| Win Rate [%] (avg) | 45.269924 |
| Profit Factor (avg) | 1.024352 |
| Sharpe (avg) | -6.893905 |
| Sortino (avg) | -9.036393 |
| Calmar (avg) | -1.724904 |
| Total Trades (sum) | 3210 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1741 | -8.3913 | 8.5706 | 34.54 | 0.574 | -26.854 |  |
| set1_1m_15m_30m | pullback | 726 | -3.5657 | 3.8910 | 41.05 | 0.611 | -15.293 |  |
| set2_5m_30m_1h | continuation | 394 | -3.2878 | 3.9288 | 37.82 | 0.653 | -9.545 |  |
| set2_5m_30m_1h | pullback | 156 | 0.4687 | 0.9154 | 46.15 | 1.135 | 1.938 |  |
| set3_15m_1h_4h | continuation | 106 | -1.2140 | 2.6507 | 46.23 | 0.763 | -3.244 |  |
| set3_15m_1h_4h | pullback | 42 | -0.9351 | 1.2490 | 47.62 | 0.557 | -5.616 |  |
| set4_30m_4h_1d | continuation | 31 | 0.0408 | 0.9060 | 51.61 | 1.024 | 0.203 |  |
| set4_30m_4h_1d | pullback | 14 | 0.7053 | 0.4911 | 57.14 | 2.877 | 3.259 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9643.42689265155
Total Return [%]: -3.565731073484494
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 285.47304750884
Max Drawdown [%]: 3.890960814703877
Max Drawdown Duration: 0.0
Total Trades: 726
Total Closed Trades: 726
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.04683195592286
Best Trade [%]: 0.18099830365598
Worst Trade [%]: -0.12128402567955233
Avg Winning Trade [%]: 0.01911508207480703
Avg Losing Trade [%]: -0.021785475887887405
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.6112546013898824
Expectancy: -0.4911475307830311
Sharpe Ratio: -15.29250707305942
Calmar Ratio: -9.753502358398537
Omega Ratio: 0.8789514156561635
Sortino Ratio: -21.196122928057743
```

#### RL teaching value (not hard-coded instructions)

Measured score=99.71, PF=1.024, avg return%=-2.022, trades=3210 over 8 set×mode runs. Fidelity=high; profile=truth_s1_cci. Truth-line geometry (CCI/BB/envelope/RSI snap) is good state/label material for L2L; do not freeze thresholds as production law.

#### 10× better

10× for `strategy_S1_cci_slingshot.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`truth_s1_cci` rules.

### 15. `note__army_snap8_STRATEGY_md`

- **Title:** STRATEGY.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_snap8\STRATEGY.md`
- **Adapter profile (logic only; family not collapsed):** `snap8`
- **Fidelity:** high
- **Collapses:** `[]` (empty)
- **Aggregate score:** 88.2454

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.958408 |
| Max Drawdown [%] (avg) | 1.503276 |
| Win Rate [%] (avg) | 41.263322 |
| Profit Factor (avg) | 0.895796 |
| Sharpe (avg) | -4.284050 |
| Sortino (avg) | -5.380417 |
| Calmar (avg) | -1.569868 |
| Total Trades (sum) | 1291 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 897 | -7.0999 | 7.1161 | 35.79 | 0.469 | -25.269 |  |
| set1_1m_15m_30m | pullback | 43 | -0.4065 | 0.4261 | 27.91 | 0.302 | -7.354 |  |
| set2_5m_30m_1h | continuation | 230 | -1.1128 | 1.6466 | 48.47 | 0.794 | -4.380 |  |
| set2_5m_30m_1h | pullback | 16 | -0.0895 | 0.2213 | 33.33 | 0.612 | -1.649 |  |
| set3_15m_1h_4h | continuation | 69 | 0.7318 | 1.0159 | 49.28 | 1.331 | 2.258 |  |
| set3_15m_1h_4h | pullback | 6 | 0.1555 | 0.1485 | 50.00 | 2.316 | 2.473 |  |
| set4_30m_4h_1d | continuation | 26 | 0.3350 | 1.0597 | 52.00 | 1.251 | 1.676 |  |
| set4_30m_4h_1d | pullback | 4 | -0.1808 | 0.3919 | 33.33 | 0.092 | -2.027 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9959.346383005477
Total Return [%]: -0.4065361699452296
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 17.16535520674628
Max Drawdown [%]: 0.42614245426169084
Max Drawdown Duration: 0.0
Total Trades: 43
Total Closed Trades: 43
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 27.906976744186046
Best Trade [%]: 0.03959500192836373
Worst Trade [%]: -0.07438346421353959
Avg Winning Trade [%]: 0.014664076325788158
Avg Losing Trade [%]: -0.018813835814437872
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.3016366081308451
Expectancy: -0.9454329533609748
Sharpe Ratio: -7.354126008230191
Calmar Ratio: -12.23430584453777
Omega Ratio: 0.7653563452043503
Sortino Ratio: -9.821876010219524
```

#### RL teaching value (not hard-coded instructions)

Measured score=88.25, PF=0.896, avg return%=-0.958, trades=1291 over 8 set×mode runs. Fidelity=high; profile=snap8. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `STRATEGY.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`snap8` rules.

### 16. `mt__JordanMomentumScreener_v10`

- **Title:** JordanMomentumScreener_v10
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: JordanMomentumScreener_v10 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `JordanMomentumScreener_v10`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 17. `mt__JordanMomentumScreener_v11`

- **Title:** JordanMomentumScreener_v11
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: JordanMomentumScreener_v11 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `JordanMomentumScreener_v11`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 18. `mt__JordanMomentumScreener_v2_MT5`

- **Title:** JordanMomentumScreener_v2_MT5
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: JordanMomentumScreener_v2_MT5 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `JordanMomentumScreener_v2_MT5`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 19. `mt__JordanMomentumScreener_v4_MT5`

- **Title:** JordanMomentumScreener_v4_MT5
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: JordanMomentumScreener_v4_MT5 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `JordanMomentumScreener_v4_MT5`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 20. `mt__JordanMomentumScreener_v5_MT5`

- **Title:** JordanMomentumScreener_v5_MT5
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: JordanMomentumScreener_v5_MT5 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `JordanMomentumScreener_v5_MT5`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 21. `mt__JordanMomentumScreener_v7_HUD`

- **Title:** JordanMomentumScreener_v7_HUD
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: JordanMomentumScreener_v7_HUD (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `JordanMomentumScreener_v7_HUD`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 22. `mt__JordanMomentumScreener_v8_HUD`

- **Title:** JordanMomentumScreener_v8_HUD
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: JordanMomentumScreener_v8_HUD (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `JordanMomentumScreener_v8_HUD`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 23. `mt__JordanMomentumScreener_v9_HUD`

- **Title:** JordanMomentumScreener_v9_HUD
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: JordanMomentumScreener_v9_HUD (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `JordanMomentumScreener_v9_HUD`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 24. `mt__JordanMomentumScreener_v9_Wave`

- **Title:** JordanMomentumScreener_v9_Wave
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: JordanMomentumScreener_v9_Wave (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `JordanMomentumScreener_v9_Wave`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 25. `mt__Momentum_Matrix_Screener`

- **Title:** Momentum_Matrix_Screener
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Momentum_Matrix_Screener (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `Momentum_Matrix_Screener`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 26. `mt__play_4_2`

- **Title:** play 4.2
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: play 4.2 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `play 4.2`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 27. `mt__play_4_3`

- **Title:** play 4.3
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: play 4.3 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `play 4.3`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 28. `mt__Unity_Play`

- **Title:** Unity Play
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Unity Play (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `jordan`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 82.5338

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.307887 |
| Max Drawdown [%] (avg) | 3.024180 |
| Win Rate [%] (avg) | 46.954980 |
| Profit Factor (avg) | 0.855978 |
| Sharpe (avg) | -7.839406 |
| Sortino (avg) | -10.493682 |
| Calmar (avg) | -2.903684 |
| Total Trades (sum) | 3121 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 912 | -6.2938 | 6.3362 | 36.40 | 0.515 | -24.639 |  |
| set1_1m_15m_30m | pullback | 1406 | -7.1807 | 7.2612 | 44.67 | 0.597 | -21.965 |  |
| set2_5m_30m_1h | continuation | 197 | -1.4768 | 1.8881 | 41.84 | 0.690 | -6.776 |  |
| set2_5m_30m_1h | pullback | 375 | -4.0460 | 4.2408 | 53.07 | 0.604 | -11.633 |  |
| set3_15m_1h_4h | continuation | 64 | -0.0795 | 1.7380 | 48.44 | 0.973 | -0.243 |  |
| set3_15m_1h_4h | pullback | 108 | 0.2946 | 0.8325 | 48.60 | 1.071 | 0.754 |  |
| set4_30m_4h_1d | continuation | 20 | 0.3023 | 0.4427 | 52.63 | 1.406 | 1.702 |  |
| set4_30m_4h_1d | pullback | 39 | 0.0169 | 1.4540 | 50.00 | 0.992 | 0.085 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9281.933033841255
Total Return [%]: -7.180669661587453
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 541.1804793427272
Max Drawdown [%]: 7.261209344812297
Max Drawdown Duration: 0.0
Total Trades: 1406
Total Closed Trades: 1406
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.66571834992888
Best Trade [%]: 0.19633257568260712
Worst Trade [%]: -0.4919545718572539
Avg Winning Trade [%]: 0.017585435141377573
Avg Losing Trade [%]: -0.023763692387543143
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5968960597473161
Expectancy: -0.510716192147051
Sharpe Ratio: -21.964848589431494
Calmar Ratio: -8.600121450816816
Omega Ratio: 0.8703744845328494
Sortino Ratio: -29.820966865220836
```

#### RL teaching value (not hard-coded instructions)

Measured score=82.53, PF=0.856, avg return%=-2.308, trades=3121 over 8 set×mode runs. Fidelity=medium; profile=jordan. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `Unity Play`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`jordan` rules.

### 29. `mt__FTMO_DQN`

- **Title:** @@FTMO_DQN@@
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: @@FTMO_DQN@@ (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `@@FTMO_DQN@@`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 30. `mt__agent_teacher`

- **Title:** agent teacher
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: agent teacher (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `agent teacher`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 31. `mt__AutoTradingBot_RF`

- **Title:** AutoTradingBot_RF
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: AutoTradingBot_RF (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `AutoTradingBot_RF`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 32. `mt__FTMO_DQN_2`

- **Title:** FTMO_DQN
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_DQN (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `FTMO_DQN`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 33. `mt__MetaLearningEA`

- **Title:** MetaLearningEA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: MetaLearningEA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `MetaLearningEA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 34. `mt__MultiTimeframe_LRL_BB_CCI_Screener`

- **Title:** MultiTimeframe_LRL_BB_CCI_Screener
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: MultiTimeframe_LRL_BB_CCI_Screener (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `MultiTimeframe_LRL_BB_CCI_Screener`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 35. `mt__MultiTimeframe_LRL_BB_CCI_Screener_v2`

- **Title:** MultiTimeframe_LRL_BB_CCI_Screener_v2
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: MultiTimeframe_LRL_BB_CCI_Screener_v2 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `MultiTimeframe_LRL_BB_CCI_Screener_v2`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 36. `mt__MultiTimeframe_NN_EA`

- **Title:** MultiTimeframe_NN_EA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: MultiTimeframe_NN_EA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `MultiTimeframe_NN_EA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 37. `mt__MultiTimeframe_NN_EA_v2`

- **Title:** MultiTimeframe_NN_EA_v2
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: MultiTimeframe_NN_EA_v2 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `MultiTimeframe_NN_EA_v2`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 38. `mt__NeuralNetworkScreener`

- **Title:** NeuralNetworkScreener
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: NeuralNetworkScreener (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `NeuralNetworkScreener`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 39. `mt__NeuralNetworkScreener_Simple`

- **Title:** NeuralNetworkScreener_Simple
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: NeuralNetworkScreener_Simple (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `NeuralNetworkScreener_Simple`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 40. `mt__NeuralNetworkScreener_Simple_Updated`

- **Title:** NeuralNetworkScreener_Simple_Updated
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: NeuralNetworkScreener_Simple_Updated (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `NeuralNetworkScreener_Simple_Updated`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 41. `mt__NN_CCI_Screener`

- **Title:** NN_CCI_Screener
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: NN_CCI_Screener (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `NN_CCI_Screener`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 42. `mt__NN_CCI_Screener_Simple`

- **Title:** NN_CCI_Screener_Simple
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: NN_CCI_Screener_Simple (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `NN_CCI_Screener_Simple`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 43. `mt__OnlineLearnerEA`

- **Title:** OnlineLearnerEA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: OnlineLearnerEA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `OnlineLearnerEA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 44. `mt__OnlineLearnerEA_v5_Fixed`

- **Title:** OnlineLearnerEA_v5_Fixed
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: OnlineLearnerEA_v5_Fixed (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `OnlineLearnerEA_v5_Fixed`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 45. `mt__PDF_MultiStrategy_MTF_EA_v1`

- **Title:** PDF_MultiStrategy_MTF_EA_v1
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: PDF_MultiStrategy_MTF_EA_v1 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `PDF_MultiStrategy_MTF_EA_v1`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 46. `mt__PDF_MultiStrategy_MTF_EA_v2`

- **Title:** PDF_MultiStrategy_MTF_EA_v2
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: PDF_MultiStrategy_MTF_EA_v2 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `PDF_MultiStrategy_MTF_EA_v2`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 47. `mt__PDF_MultiStrategy_VotingForest_EA_v4`

- **Title:** PDF_MultiStrategy_VotingForest_EA_v4
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: PDF_MultiStrategy_VotingForest_EA_v4 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `PDF_MultiStrategy_VotingForest_EA_v4`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 48. `mt__RegressionlineEA`

- **Title:** RegressionlineEA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: RegressionlineEA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `RegressionlineEA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 49. `mt__RL_PropTrader_Final`

- **Title:** RL_PropTrader_Final
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: RL_PropTrader_Final (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `RL_PropTrader_Final`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 50. `mt__RL_PropTrader_MVP_v2`

- **Title:** RL_PropTrader_MVP_v2
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: RL_PropTrader_MVP_v2 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `RL_PropTrader_MVP_v2`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 51. `mt__rsi_bb_extreme`

- **Title:** rsi_bb_extreme
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: rsi_bb_extreme (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `rsi_bb_extreme`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 52. `mt__to_opimize_ea`

- **Title:** to opimize ea
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: to opimize ea (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `rl_proxy`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=low; profile=rl_proxy. Black-box EA name only — teaching value is A14 meta-train reminder; do not re-import MQL as hard rules.

#### 10× better

10× for `to opimize ea`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`rl_proxy` rules.

### 53. `note__local_desktop_new_trading_strategies_1_md`

- **Title:** new_trading_strategies (1).md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\new_trading_strategies (1).md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `new_trading_strategies (1).md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 54. `note__local_desktop_new_trading_strategies_md`

- **Title:** new_trading_strategies.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\new_trading_strategies.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `new_trading_strategies.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 55. `note__local_desktop_rsi_bb_strategy_txt`

- **Title:** rsi + bb strategy.txt
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\rsi + bb strategy.txt`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** high
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=high; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `rsi + bb strategy.txt`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 56. `note__local_desktop_section-1_md`

- **Title:** section-1.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\section-1.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-1.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 57. `note__local_desktop_section-2_md`

- **Title:** section-2.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\section-2.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-2.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 58. `note__local_desktop_section-3_md`

- **Title:** section-3.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\section-3.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-3.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 59. `note__local_desktop_section-4_md`

- **Title:** section-4.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\section-4.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-4.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 60. `note__local_desktop_section-5_md`

- **Title:** section-5.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\section-5.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-5.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 61. `note__local_desktop_section-6_md`

- **Title:** section-6.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\section-6.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-6.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 62. `note__local_desktop_section-8_md`

- **Title:** section-8.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\section-8.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-8.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 63. `note__army_library_strategy_copy_new_trading_strategies_1_md`

- **Title:** new_trading_strategies (1).md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_library_strategy_copy\new_trading_strategies (1).md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `new_trading_strategies (1).md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 64. `note__army_library_strategy_copy_new_trading_strategies_md`

- **Title:** new_trading_strategies.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_library_strategy_copy\new_trading_strategies.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `new_trading_strategies.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 65. `note__army_library_strategy_copy_rsi_bb_strategy_txt`

- **Title:** rsi + bb strategy.txt
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_library_strategy_copy\rsi + bb strategy.txt`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** high
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=high; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `rsi + bb strategy.txt`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 66. `note__army_library_strategy_copy_section-1_md`

- **Title:** section-1.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_library_strategy_copy\section-1.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-1.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 67. `note__army_library_strategy_copy_section-2_md`

- **Title:** section-2.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_library_strategy_copy\section-2.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-2.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 68. `note__army_library_strategy_copy_section-3_md`

- **Title:** section-3.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_library_strategy_copy\section-3.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-3.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 69. `note__army_library_strategy_copy_section-4_md`

- **Title:** section-4.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_library_strategy_copy\section-4.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-4.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 70. `note__army_library_strategy_copy_section-5_md`

- **Title:** section-5.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_library_strategy_copy\section-5.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-5.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 71. `note__army_library_strategy_copy_section-6_md`

- **Title:** section-6.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_library_strategy_copy\section-6.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-6.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 72. `note__army_library_strategy_copy_section-8_md`

- **Title:** section-8.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\army_library_strategy_copy\section-8.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=medium; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `section-8.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 73. `note__mark_doctrine_refs_RSI_BB_L2L_SKILL_md`

- **Title:** RSI_BB_L2L_SKILL.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\mark_doctrine_refs\RSI_BB_L2L_SKILL.md`
- **Adapter profile (logic only; family not collapsed):** `mark_rsi_bb`
- **Fidelity:** high
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.2280

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.620680 |
| Max Drawdown [%] (avg) | 4.412063 |
| Win Rate [%] (avg) | 46.639871 |
| Profit Factor (avg) | 0.819517 |
| Sharpe (avg) | -10.314685 |
| Sortino (avg) | -14.055029 |
| Calmar (avg) | -3.181302 |
| Total Trades (sum) | 5062 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1930 | -11.7134 | 11.7287 | 34.40 | 0.508 | -35.292 |  |
| set1_1m_15m_30m | pullback | 1939 | -11.1065 | 11.1368 | 39.40 | 0.529 | -31.025 |  |
| set2_5m_30m_1h | continuation | 399 | -2.8519 | 3.0875 | 43.86 | 0.699 | -7.807 |  |
| set2_5m_30m_1h | pullback | 429 | -2.5727 | 2.5826 | 46.26 | 0.748 | -6.358 |  |
| set3_15m_1h_4h | continuation | 113 | -1.5955 | 2.6735 | 43.36 | 0.683 | -5.040 |  |
| set3_15m_1h_4h | pullback | 147 | 0.6213 | 1.1485 | 56.85 | 1.125 | 1.582 |  |
| set4_30m_4h_1d | continuation | 49 | 0.8093 | 0.8725 | 48.98 | 1.463 | 3.439 |  |
| set4_30m_4h_1d | pullback | 56 | -0.5561 | 2.0664 | 60.00 | 0.800 | -2.016 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8889.351434818393
Total Return [%]: -11.106485651816074
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 729.8154638250415
Max Drawdown [%]: 11.136815420213717
Max Drawdown Duration: 0.0
Total Trades: 1939
Total Closed Trades: 1939
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 39.40175348117587
Best Trade [%]: 0.15817548021062858
Worst Trade [%]: -0.5886277112438143
Avg Winning Trade [%]: 0.017310011662957838
Avg Losing Trade [%]: -0.021266571577838195
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5291736832800703
Expectancy: -0.5727945153076657
Sharpe Ratio: -31.025315944992126
Calmar Ratio: -7.068537860016588
Omega Ratio: 0.8328060597832059
Sortino Ratio: -41.427810669671494
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.23, PF=0.820, avg return%=-3.621, trades=5062 over 8 set×mode runs. Fidelity=high; profile=mark_rsi_bb. Teach as skill-id curriculum (wait_loaded vs fire) under HTF mass — concurrence with Mark, not hard-coded entries.

#### 10× better

10× for `RSI_BB_L2L_SKILL.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`mark_rsi_bb` rules.

### 74. `mt__crossenteopy`

- **Title:** crossenteopy
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: crossenteopy (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `macd`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.1113

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.462982 |
| Max Drawdown [%] (avg) | 2.998798 |
| Win Rate [%] (avg) | 44.132004 |
| Profit Factor (avg) | 0.803240 |
| Sharpe (avg) | -8.267706 |
| Sortino (avg) | -11.374531 |
| Calmar (avg) | -4.408707 |
| Total Trades (sum) | 2997 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 841 | -5.6429 | 5.6594 | 37.10 | 0.534 | -20.004 |  |
| set1_1m_15m_30m | pullback | 1521 | -9.1950 | 9.2043 | 37.54 | 0.532 | -28.437 |  |
| set2_5m_30m_1h | continuation | 167 | -2.3048 | 2.6220 | 38.92 | 0.533 | -9.585 |  |
| set2_5m_30m_1h | pullback | 280 | -2.3208 | 2.7242 | 43.73 | 0.633 | -8.085 |  |
| set3_15m_1h_4h | continuation | 47 | -0.1115 | 1.2857 | 51.06 | 0.952 | -0.393 |  |
| set3_15m_1h_4h | pullback | 88 | -0.2943 | 1.2347 | 45.45 | 0.910 | -0.818 |  |
| set4_30m_4h_1d | continuation | 14 | 0.2329 | 0.4498 | 57.14 | 1.379 | 1.474 |  |
| set4_30m_4h_1d | pullback | 39 | -0.0675 | 0.8103 | 42.11 | 0.953 | -0.294 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9080.499289044537
Total Return [%]: -9.195007109554625
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 578.3737641301541
Max Drawdown [%]: 9.204346791878834
Max Drawdown Duration: 0.0
Total Trades: 1521
Total Closed Trades: 1521
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.54109138724523
Best Trade [%]: 0.20256066797235492
Worst Trade [%]: -0.527964497974417
Avg Winning Trade [%]: 0.019245237960648896
Avg Losing Trade [%]: -0.02171288553289409
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5319963311843554
Expectancy: -0.6045369565782029
Sharpe Ratio: -28.437069916721715
Calmar Ratio: -7.806670002058159
Omega Ratio: 0.8354277105220917
Sortino Ratio: -38.2118523230565
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.11, PF=0.803, avg return%=-2.463, trades=2997 over 8 set×mode runs. Fidelity=medium; profile=macd. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `crossenteopy`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`macd` rules.

### 75. `mt__kmeans`

- **Title:** kmeans
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: kmeans (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `macd`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.1113

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.462982 |
| Max Drawdown [%] (avg) | 2.998798 |
| Win Rate [%] (avg) | 44.132004 |
| Profit Factor (avg) | 0.803240 |
| Sharpe (avg) | -8.267706 |
| Sortino (avg) | -11.374531 |
| Calmar (avg) | -4.408707 |
| Total Trades (sum) | 2997 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 841 | -5.6429 | 5.6594 | 37.10 | 0.534 | -20.004 |  |
| set1_1m_15m_30m | pullback | 1521 | -9.1950 | 9.2043 | 37.54 | 0.532 | -28.437 |  |
| set2_5m_30m_1h | continuation | 167 | -2.3048 | 2.6220 | 38.92 | 0.533 | -9.585 |  |
| set2_5m_30m_1h | pullback | 280 | -2.3208 | 2.7242 | 43.73 | 0.633 | -8.085 |  |
| set3_15m_1h_4h | continuation | 47 | -0.1115 | 1.2857 | 51.06 | 0.952 | -0.393 |  |
| set3_15m_1h_4h | pullback | 88 | -0.2943 | 1.2347 | 45.45 | 0.910 | -0.818 |  |
| set4_30m_4h_1d | continuation | 14 | 0.2329 | 0.4498 | 57.14 | 1.379 | 1.474 |  |
| set4_30m_4h_1d | pullback | 39 | -0.0675 | 0.8103 | 42.11 | 0.953 | -0.294 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9080.499289044537
Total Return [%]: -9.195007109554625
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 578.3737641301541
Max Drawdown [%]: 9.204346791878834
Max Drawdown Duration: 0.0
Total Trades: 1521
Total Closed Trades: 1521
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.54109138724523
Best Trade [%]: 0.20256066797235492
Worst Trade [%]: -0.527964497974417
Avg Winning Trade [%]: 0.019245237960648896
Avg Losing Trade [%]: -0.02171288553289409
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5319963311843554
Expectancy: -0.6045369565782029
Sharpe Ratio: -28.437069916721715
Calmar Ratio: -7.806670002058159
Omega Ratio: 0.8354277105220917
Sortino Ratio: -38.2118523230565
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.11, PF=0.803, avg return%=-2.463, trades=2997 over 8 set×mode runs. Fidelity=medium; profile=macd. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `kmeans`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`macd` rules.

### 76. `mt__MACD_Sample`

- **Title:** MACD Sample
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: MACD Sample (.mq4)`
- **Adapter profile (logic only; family not collapsed):** `macd`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.1113

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.462982 |
| Max Drawdown [%] (avg) | 2.998798 |
| Win Rate [%] (avg) | 44.132004 |
| Profit Factor (avg) | 0.803240 |
| Sharpe (avg) | -8.267706 |
| Sortino (avg) | -11.374531 |
| Calmar (avg) | -4.408707 |
| Total Trades (sum) | 2997 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 841 | -5.6429 | 5.6594 | 37.10 | 0.534 | -20.004 |  |
| set1_1m_15m_30m | pullback | 1521 | -9.1950 | 9.2043 | 37.54 | 0.532 | -28.437 |  |
| set2_5m_30m_1h | continuation | 167 | -2.3048 | 2.6220 | 38.92 | 0.533 | -9.585 |  |
| set2_5m_30m_1h | pullback | 280 | -2.3208 | 2.7242 | 43.73 | 0.633 | -8.085 |  |
| set3_15m_1h_4h | continuation | 47 | -0.1115 | 1.2857 | 51.06 | 0.952 | -0.393 |  |
| set3_15m_1h_4h | pullback | 88 | -0.2943 | 1.2347 | 45.45 | 0.910 | -0.818 |  |
| set4_30m_4h_1d | continuation | 14 | 0.2329 | 0.4498 | 57.14 | 1.379 | 1.474 |  |
| set4_30m_4h_1d | pullback | 39 | -0.0675 | 0.8103 | 42.11 | 0.953 | -0.294 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9080.499289044537
Total Return [%]: -9.195007109554625
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 578.3737641301541
Max Drawdown [%]: 9.204346791878834
Max Drawdown Duration: 0.0
Total Trades: 1521
Total Closed Trades: 1521
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.54109138724523
Best Trade [%]: 0.20256066797235492
Worst Trade [%]: -0.527964497974417
Avg Winning Trade [%]: 0.019245237960648896
Avg Losing Trade [%]: -0.02171288553289409
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5319963311843554
Expectancy: -0.6045369565782029
Sharpe Ratio: -28.437069916721715
Calmar Ratio: -7.806670002058159
Omega Ratio: 0.8354277105220917
Sortino Ratio: -38.2118523230565
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.11, PF=0.803, avg return%=-2.463, trades=2997 over 8 set×mode runs. Fidelity=medium; profile=macd. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `MACD Sample`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`macd` rules.

### 77. `mt__PerceptronEA`

- **Title:** PerceptronEA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: PerceptronEA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `macd`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.1113

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.462982 |
| Max Drawdown [%] (avg) | 2.998798 |
| Win Rate [%] (avg) | 44.132004 |
| Profit Factor (avg) | 0.803240 |
| Sharpe (avg) | -8.267706 |
| Sortino (avg) | -11.374531 |
| Calmar (avg) | -4.408707 |
| Total Trades (sum) | 2997 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 841 | -5.6429 | 5.6594 | 37.10 | 0.534 | -20.004 |  |
| set1_1m_15m_30m | pullback | 1521 | -9.1950 | 9.2043 | 37.54 | 0.532 | -28.437 |  |
| set2_5m_30m_1h | continuation | 167 | -2.3048 | 2.6220 | 38.92 | 0.533 | -9.585 |  |
| set2_5m_30m_1h | pullback | 280 | -2.3208 | 2.7242 | 43.73 | 0.633 | -8.085 |  |
| set3_15m_1h_4h | continuation | 47 | -0.1115 | 1.2857 | 51.06 | 0.952 | -0.393 |  |
| set3_15m_1h_4h | pullback | 88 | -0.2943 | 1.2347 | 45.45 | 0.910 | -0.818 |  |
| set4_30m_4h_1d | continuation | 14 | 0.2329 | 0.4498 | 57.14 | 1.379 | 1.474 |  |
| set4_30m_4h_1d | pullback | 39 | -0.0675 | 0.8103 | 42.11 | 0.953 | -0.294 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9080.499289044537
Total Return [%]: -9.195007109554625
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 578.3737641301541
Max Drawdown [%]: 9.204346791878834
Max Drawdown Duration: 0.0
Total Trades: 1521
Total Closed Trades: 1521
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.54109138724523
Best Trade [%]: 0.20256066797235492
Worst Trade [%]: -0.527964497974417
Avg Winning Trade [%]: 0.019245237960648896
Avg Losing Trade [%]: -0.02171288553289409
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5319963311843554
Expectancy: -0.6045369565782029
Sharpe Ratio: -28.437069916721715
Calmar Ratio: -7.806670002058159
Omega Ratio: 0.8354277105220917
Sortino Ratio: -38.2118523230565
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.11, PF=0.803, avg return%=-2.463, trades=2997 over 8 set×mode runs. Fidelity=medium; profile=macd. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `PerceptronEA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`macd` rules.

### 78. `mt__Q-learning`

- **Title:** Q-learning
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Q-learning (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `macd`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.1113

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.462982 |
| Max Drawdown [%] (avg) | 2.998798 |
| Win Rate [%] (avg) | 44.132004 |
| Profit Factor (avg) | 0.803240 |
| Sharpe (avg) | -8.267706 |
| Sortino (avg) | -11.374531 |
| Calmar (avg) | -4.408707 |
| Total Trades (sum) | 2997 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 841 | -5.6429 | 5.6594 | 37.10 | 0.534 | -20.004 |  |
| set1_1m_15m_30m | pullback | 1521 | -9.1950 | 9.2043 | 37.54 | 0.532 | -28.437 |  |
| set2_5m_30m_1h | continuation | 167 | -2.3048 | 2.6220 | 38.92 | 0.533 | -9.585 |  |
| set2_5m_30m_1h | pullback | 280 | -2.3208 | 2.7242 | 43.73 | 0.633 | -8.085 |  |
| set3_15m_1h_4h | continuation | 47 | -0.1115 | 1.2857 | 51.06 | 0.952 | -0.393 |  |
| set3_15m_1h_4h | pullback | 88 | -0.2943 | 1.2347 | 45.45 | 0.910 | -0.818 |  |
| set4_30m_4h_1d | continuation | 14 | 0.2329 | 0.4498 | 57.14 | 1.379 | 1.474 |  |
| set4_30m_4h_1d | pullback | 39 | -0.0675 | 0.8103 | 42.11 | 0.953 | -0.294 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9080.499289044537
Total Return [%]: -9.195007109554625
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 578.3737641301541
Max Drawdown [%]: 9.204346791878834
Max Drawdown Duration: 0.0
Total Trades: 1521
Total Closed Trades: 1521
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.54109138724523
Best Trade [%]: 0.20256066797235492
Worst Trade [%]: -0.527964497974417
Avg Winning Trade [%]: 0.019245237960648896
Avg Losing Trade [%]: -0.02171288553289409
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5319963311843554
Expectancy: -0.6045369565782029
Sharpe Ratio: -28.437069916721715
Calmar Ratio: -7.806670002058159
Omega Ratio: 0.8354277105220917
Sortino Ratio: -38.2118523230565
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.11, PF=0.803, avg return%=-2.463, trades=2997 over 8 set×mode runs. Fidelity=medium; profile=macd. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `Q-learning`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`macd` rules.

### 79. `mt__some_bs`

- **Title:** some bs
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: some bs (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `macd`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.1113

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.462982 |
| Max Drawdown [%] (avg) | 2.998798 |
| Win Rate [%] (avg) | 44.132004 |
| Profit Factor (avg) | 0.803240 |
| Sharpe (avg) | -8.267706 |
| Sortino (avg) | -11.374531 |
| Calmar (avg) | -4.408707 |
| Total Trades (sum) | 2997 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 841 | -5.6429 | 5.6594 | 37.10 | 0.534 | -20.004 |  |
| set1_1m_15m_30m | pullback | 1521 | -9.1950 | 9.2043 | 37.54 | 0.532 | -28.437 |  |
| set2_5m_30m_1h | continuation | 167 | -2.3048 | 2.6220 | 38.92 | 0.533 | -9.585 |  |
| set2_5m_30m_1h | pullback | 280 | -2.3208 | 2.7242 | 43.73 | 0.633 | -8.085 |  |
| set3_15m_1h_4h | continuation | 47 | -0.1115 | 1.2857 | 51.06 | 0.952 | -0.393 |  |
| set3_15m_1h_4h | pullback | 88 | -0.2943 | 1.2347 | 45.45 | 0.910 | -0.818 |  |
| set4_30m_4h_1d | continuation | 14 | 0.2329 | 0.4498 | 57.14 | 1.379 | 1.474 |  |
| set4_30m_4h_1d | pullback | 39 | -0.0675 | 0.8103 | 42.11 | 0.953 | -0.294 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9080.499289044537
Total Return [%]: -9.195007109554625
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 578.3737641301541
Max Drawdown [%]: 9.204346791878834
Max Drawdown Duration: 0.0
Total Trades: 1521
Total Closed Trades: 1521
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.54109138724523
Best Trade [%]: 0.20256066797235492
Worst Trade [%]: -0.527964497974417
Avg Winning Trade [%]: 0.019245237960648896
Avg Losing Trade [%]: -0.02171288553289409
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5319963311843554
Expectancy: -0.6045369565782029
Sharpe Ratio: -28.437069916721715
Calmar Ratio: -7.806670002058159
Omega Ratio: 0.8354277105220917
Sortino Ratio: -38.2118523230565
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.11, PF=0.803, avg return%=-2.463, trades=2997 over 8 set×mode runs. Fidelity=medium; profile=macd. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `some bs`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`macd` rules.

### 80. `mt__some_bullshit`

- **Title:** some bullshit
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: some bullshit (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `macd`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 77.1113

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.462982 |
| Max Drawdown [%] (avg) | 2.998798 |
| Win Rate [%] (avg) | 44.132004 |
| Profit Factor (avg) | 0.803240 |
| Sharpe (avg) | -8.267706 |
| Sortino (avg) | -11.374531 |
| Calmar (avg) | -4.408707 |
| Total Trades (sum) | 2997 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 841 | -5.6429 | 5.6594 | 37.10 | 0.534 | -20.004 |  |
| set1_1m_15m_30m | pullback | 1521 | -9.1950 | 9.2043 | 37.54 | 0.532 | -28.437 |  |
| set2_5m_30m_1h | continuation | 167 | -2.3048 | 2.6220 | 38.92 | 0.533 | -9.585 |  |
| set2_5m_30m_1h | pullback | 280 | -2.3208 | 2.7242 | 43.73 | 0.633 | -8.085 |  |
| set3_15m_1h_4h | continuation | 47 | -0.1115 | 1.2857 | 51.06 | 0.952 | -0.393 |  |
| set3_15m_1h_4h | pullback | 88 | -0.2943 | 1.2347 | 45.45 | 0.910 | -0.818 |  |
| set4_30m_4h_1d | continuation | 14 | 0.2329 | 0.4498 | 57.14 | 1.379 | 1.474 |  |
| set4_30m_4h_1d | pullback | 39 | -0.0675 | 0.8103 | 42.11 | 0.953 | -0.294 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9080.499289044537
Total Return [%]: -9.195007109554625
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 578.3737641301541
Max Drawdown [%]: 9.204346791878834
Max Drawdown Duration: 0.0
Total Trades: 1521
Total Closed Trades: 1521
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.54109138724523
Best Trade [%]: 0.20256066797235492
Worst Trade [%]: -0.527964497974417
Avg Winning Trade [%]: 0.019245237960648896
Avg Losing Trade [%]: -0.02171288553289409
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5319963311843554
Expectancy: -0.6045369565782029
Sharpe Ratio: -28.437069916721715
Calmar Ratio: -7.806670002058159
Omega Ratio: 0.8354277105220917
Sortino Ratio: -38.2118523230565
```

#### RL teaching value (not hard-coded instructions)

Measured score=77.11, PF=0.803, avg return%=-2.463, trades=2997 over 8 set×mode runs. Fidelity=medium; profile=macd. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `some bullshit`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`macd` rules.

### 81. `mt__FTMO_SMA_Scalper`

- **Title:** FTMO_SMA_Scalper
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_SMA_Scalper (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `sma_scalp`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 74.4812

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.204983 |
| Max Drawdown [%] (avg) | 1.685812 |
| Win Rate [%] (avg) | 42.210349 |
| Profit Factor (avg) | 0.761077 |
| Sharpe (avg) | -6.442822 |
| Sortino (avg) | -8.546206 |
| Calmar (avg) | -4.280539 |
| Total Trades (sum) | 1412 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 484 | -3.4462 | 3.5126 | 37.81 | 0.519 | -16.416 |  |
| set1_1m_15m_30m | pullback | 574 | -4.4602 | 4.4767 | 37.80 | 0.447 | -22.776 |  |
| set2_5m_30m_1h | continuation | 107 | -0.4446 | 1.1597 | 39.25 | 0.829 | -2.625 |  |
| set2_5m_30m_1h | pullback | 144 | -0.8456 | 0.9650 | 43.06 | 0.732 | -4.513 |  |
| set3_15m_1h_4h | continuation | 33 | -0.8100 | 1.4340 | 43.75 | 0.573 | -4.674 |  |
| set3_15m_1h_4h | pullback | 46 | 0.6901 | 0.7231 | 48.89 | 1.425 | 2.637 |  |
| set4_30m_4h_1d | continuation | 12 | 0.1645 | 0.4703 | 41.67 | 1.296 | 1.071 |  |
| set4_30m_4h_1d | pullback | 12 | -0.4879 | 0.7450 | 45.45 | 0.267 | -4.245 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9553.979130233569
Total Return [%]: -4.460208697664311
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 223.72586815275835
Max Drawdown [%]: 4.476719303044434
Max Drawdown Duration: 0.0
Total Trades: 574
Total Closed Trades: 574
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.80487804878049
Best Trade [%]: 0.12861378243047536
Worst Trade [%]: -0.49801396825984673
Avg Winning Trade [%]: 0.01708767724740592
Avg Losing Trade [%]: -0.0231582586088537
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.4474697381824634
Expectancy: -0.7770398427986627
Sharpe Ratio: -22.77632572636287
Calmar Ratio: -10.075158696961767
Omega Ratio: 0.8047566088252608
Sortino Ratio: -29.88059503877321
```

#### RL teaching value (not hard-coded instructions)

Measured score=74.48, PF=0.761, avg return%=-1.205, trades=1412 over 8 set×mode runs. Fidelity=medium; profile=sma_scalp. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_SMA_Scalper`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`sma_scalp` rules.

### 82. `mt__SMA_Fan_MTF_BBExit_v1`

- **Title:** SMA_Fan_MTF_BBExit_v1
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: SMA_Fan_MTF_BBExit_v1 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `sma_scalp`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 74.4812

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.204983 |
| Max Drawdown [%] (avg) | 1.685812 |
| Win Rate [%] (avg) | 42.210349 |
| Profit Factor (avg) | 0.761077 |
| Sharpe (avg) | -6.442822 |
| Sortino (avg) | -8.546206 |
| Calmar (avg) | -4.280539 |
| Total Trades (sum) | 1412 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 484 | -3.4462 | 3.5126 | 37.81 | 0.519 | -16.416 |  |
| set1_1m_15m_30m | pullback | 574 | -4.4602 | 4.4767 | 37.80 | 0.447 | -22.776 |  |
| set2_5m_30m_1h | continuation | 107 | -0.4446 | 1.1597 | 39.25 | 0.829 | -2.625 |  |
| set2_5m_30m_1h | pullback | 144 | -0.8456 | 0.9650 | 43.06 | 0.732 | -4.513 |  |
| set3_15m_1h_4h | continuation | 33 | -0.8100 | 1.4340 | 43.75 | 0.573 | -4.674 |  |
| set3_15m_1h_4h | pullback | 46 | 0.6901 | 0.7231 | 48.89 | 1.425 | 2.637 |  |
| set4_30m_4h_1d | continuation | 12 | 0.1645 | 0.4703 | 41.67 | 1.296 | 1.071 |  |
| set4_30m_4h_1d | pullback | 12 | -0.4879 | 0.7450 | 45.45 | 0.267 | -4.245 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9553.979130233569
Total Return [%]: -4.460208697664311
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 223.72586815275835
Max Drawdown [%]: 4.476719303044434
Max Drawdown Duration: 0.0
Total Trades: 574
Total Closed Trades: 574
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.80487804878049
Best Trade [%]: 0.12861378243047536
Worst Trade [%]: -0.49801396825984673
Avg Winning Trade [%]: 0.01708767724740592
Avg Losing Trade [%]: -0.0231582586088537
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.4474697381824634
Expectancy: -0.7770398427986627
Sharpe Ratio: -22.77632572636287
Calmar Ratio: -10.075158696961767
Omega Ratio: 0.8047566088252608
Sortino Ratio: -29.88059503877321
```

#### RL teaching value (not hard-coded instructions)

Measured score=74.48, PF=0.761, avg return%=-1.205, trades=1412 over 8 set×mode runs. Fidelity=medium; profile=sma_scalp. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `SMA_Fan_MTF_BBExit_v1`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`sma_scalp` rules.

### 83. `mt__TriTF_SMA_Shift_Optimizer_EA`

- **Title:** TriTF_SMA_Shift_Optimizer_EA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: TriTF_SMA_Shift_Optimizer_EA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `sma_scalp`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 74.4812

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.204983 |
| Max Drawdown [%] (avg) | 1.685812 |
| Win Rate [%] (avg) | 42.210349 |
| Profit Factor (avg) | 0.761077 |
| Sharpe (avg) | -6.442822 |
| Sortino (avg) | -8.546206 |
| Calmar (avg) | -4.280539 |
| Total Trades (sum) | 1412 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 484 | -3.4462 | 3.5126 | 37.81 | 0.519 | -16.416 |  |
| set1_1m_15m_30m | pullback | 574 | -4.4602 | 4.4767 | 37.80 | 0.447 | -22.776 |  |
| set2_5m_30m_1h | continuation | 107 | -0.4446 | 1.1597 | 39.25 | 0.829 | -2.625 |  |
| set2_5m_30m_1h | pullback | 144 | -0.8456 | 0.9650 | 43.06 | 0.732 | -4.513 |  |
| set3_15m_1h_4h | continuation | 33 | -0.8100 | 1.4340 | 43.75 | 0.573 | -4.674 |  |
| set3_15m_1h_4h | pullback | 46 | 0.6901 | 0.7231 | 48.89 | 1.425 | 2.637 |  |
| set4_30m_4h_1d | continuation | 12 | 0.1645 | 0.4703 | 41.67 | 1.296 | 1.071 |  |
| set4_30m_4h_1d | pullback | 12 | -0.4879 | 0.7450 | 45.45 | 0.267 | -4.245 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9553.979130233569
Total Return [%]: -4.460208697664311
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 223.72586815275835
Max Drawdown [%]: 4.476719303044434
Max Drawdown Duration: 0.0
Total Trades: 574
Total Closed Trades: 574
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.80487804878049
Best Trade [%]: 0.12861378243047536
Worst Trade [%]: -0.49801396825984673
Avg Winning Trade [%]: 0.01708767724740592
Avg Losing Trade [%]: -0.0231582586088537
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.4474697381824634
Expectancy: -0.7770398427986627
Sharpe Ratio: -22.77632572636287
Calmar Ratio: -10.075158696961767
Omega Ratio: 0.8047566088252608
Sortino Ratio: -29.88059503877321
```

#### RL teaching value (not hard-coded instructions)

Measured score=74.48, PF=0.761, avg return%=-1.205, trades=1412 over 8 set×mode runs. Fidelity=medium; profile=sma_scalp. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `TriTF_SMA_Shift_Optimizer_EA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`sma_scalp` rules.

### 84. `mt__MA_ribbon_filled_Alerts`

- **Title:** MA ribbon filled_Alerts
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: MA ribbon filled_Alerts (.mq4)`
- **Adapter profile (logic only; family not collapsed):** `ma_ribbon`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 74.1532

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.643899 |
| Max Drawdown [%] (avg) | 3.339307 |
| Win Rate [%] (avg) | 36.226157 |
| Profit Factor (avg) | 0.776320 |
| Sharpe (avg) | -7.850883 |
| Sortino (avg) | -10.343129 |
| Calmar (avg) | -3.416641 |
| Total Trades (sum) | 2941 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 918 | -6.3563 | 6.3880 | 28.65 | 0.609 | -15.492 |  |
| set1_1m_15m_30m | pullback | 1290 | -9.5351 | 9.5677 | 34.42 | 0.462 | -31.251 |  |
| set2_5m_30m_1h | continuation | 216 | -3.2093 | 3.6580 | 31.16 | 0.620 | -7.647 |  |
| set2_5m_30m_1h | pullback | 288 | -2.0601 | 2.1595 | 41.81 | 0.676 | -7.809 |  |
| set3_15m_1h_4h | continuation | 66 | -0.4974 | 1.4719 | 33.33 | 0.862 | -1.173 |  |
| set3_15m_1h_4h | pullback | 101 | 1.2179 | 0.8061 | 45.54 | 1.354 | 3.205 |  |
| set4_30m_4h_1d | continuation | 25 | -0.3277 | 1.3741 | 36.00 | 0.802 | -1.076 |  |
| set4_30m_4h_1d | pullback | 37 | -0.3832 | 1.2891 | 38.89 | 0.825 | -1.564 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9046.487052750517
Total Return [%]: -9.535129472494827
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 489.71735512408316
Max Drawdown [%]: 9.567684778873373
Max Drawdown Duration: 0.0
Total Trades: 1290
Total Closed Trades: 1290
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 34.418604651162795
Best Trade [%]: 0.19984338273868013
Worst Trade [%]: -0.6183535970507261
Avg Winning Trade [%]: 0.019433726507744286
Avg Losing Trade [%]: -0.022035737525336493
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.46233180352626496
Expectancy: -0.7391573234492032
Sharpe Ratio: -31.251020328795
Calmar Ratio: -7.651783235453483
Omega Ratio: 0.7908495620280552
Sortino Ratio: -40.24955116514
```

#### RL teaching value (not hard-coded instructions)

Measured score=74.15, PF=0.776, avg return%=-2.644, trades=2941 over 8 set×mode runs. Fidelity=medium; profile=ma_ribbon. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `MA ribbon filled_Alerts`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`ma_ribbon` rules.

### 85. `mt__ATI_FTMO_EA`

- **Title:** ATI_FTMO_EA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: ATI_FTMO_EA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `challenge`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 72.3862

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.326354 |
| Max Drawdown [%] (avg) | 2.667493 |
| Win Rate [%] (avg) | 42.564747 |
| Profit Factor (avg) | 0.753795 |
| Sharpe (avg) | -7.927864 |
| Sortino (avg) | -11.026114 |
| Calmar (avg) | -7.145943 |
| Total Trades (sum) | 2998 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 981 | -5.7467 | 5.8357 | 37.82 | 0.577 | -21.254 |  |
| set1_1m_15m_30m | pullback | 1168 | -4.7898 | 4.9571 | 41.61 | 0.665 | -16.366 |  |
| set2_5m_30m_1h | continuation | 251 | -2.5733 | 2.5933 | 39.60 | 0.624 | -8.462 |  |
| set2_5m_30m_1h | pullback | 368 | -3.2213 | 3.4666 | 44.84 | 0.692 | -7.853 |  |
| set3_15m_1h_4h | continuation | 72 | -1.2723 | 1.4074 | 40.28 | 0.614 | -4.876 |  |
| set3_15m_1h_4h | pullback | 123 | -0.7288 | 1.5599 | 52.46 | 0.869 | -1.947 |  |
| set4_30m_4h_1d | continuation | 13 | 0.2570 | 0.5171 | 38.46 | 1.452 | 1.725 |  |
| set4_30m_4h_1d | pullback | 22 | -0.5355 | 1.0029 | 45.45 | 0.536 | -4.389 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9521.017311229478
Total Return [%]: -4.789826887705222
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 454.57067157289737
Max Drawdown [%]: 4.957108461251716
Max Drawdown Duration: 0.0
Total Trades: 1168
Total Closed Trades: 1168
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.60958904109589
Best Trade [%]: 0.15817548021064193
Worst Trade [%]: -0.22369274979601664
Avg Winning Trade [%]: 0.020119455831101942
Avg Losing Trade [%]: -0.02152675132969531
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.6651236269493471
Expectancy: -0.4100879184679087
Sharpe Ratio: -16.366428849872438
Calmar Ratio: -9.590586502274059
Omega Ratio: 0.8971511066506718
Sortino Ratio: -23.305120129095236
```

#### RL teaching value (not hard-coded instructions)

Measured score=72.39, PF=0.754, avg return%=-2.326, trades=2998 over 8 set×mode runs. Fidelity=medium; profile=challenge. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `ATI_FTMO_EA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`challenge` rules.

### 86. `mt__FTMO_Challenge_EA`

- **Title:** FTMO_Challenge_EA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_Challenge_EA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `challenge`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 72.3862

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.326354 |
| Max Drawdown [%] (avg) | 2.667493 |
| Win Rate [%] (avg) | 42.564747 |
| Profit Factor (avg) | 0.753795 |
| Sharpe (avg) | -7.927864 |
| Sortino (avg) | -11.026114 |
| Calmar (avg) | -7.145943 |
| Total Trades (sum) | 2998 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 981 | -5.7467 | 5.8357 | 37.82 | 0.577 | -21.254 |  |
| set1_1m_15m_30m | pullback | 1168 | -4.7898 | 4.9571 | 41.61 | 0.665 | -16.366 |  |
| set2_5m_30m_1h | continuation | 251 | -2.5733 | 2.5933 | 39.60 | 0.624 | -8.462 |  |
| set2_5m_30m_1h | pullback | 368 | -3.2213 | 3.4666 | 44.84 | 0.692 | -7.853 |  |
| set3_15m_1h_4h | continuation | 72 | -1.2723 | 1.4074 | 40.28 | 0.614 | -4.876 |  |
| set3_15m_1h_4h | pullback | 123 | -0.7288 | 1.5599 | 52.46 | 0.869 | -1.947 |  |
| set4_30m_4h_1d | continuation | 13 | 0.2570 | 0.5171 | 38.46 | 1.452 | 1.725 |  |
| set4_30m_4h_1d | pullback | 22 | -0.5355 | 1.0029 | 45.45 | 0.536 | -4.389 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9521.017311229478
Total Return [%]: -4.789826887705222
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 454.57067157289737
Max Drawdown [%]: 4.957108461251716
Max Drawdown Duration: 0.0
Total Trades: 1168
Total Closed Trades: 1168
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.60958904109589
Best Trade [%]: 0.15817548021064193
Worst Trade [%]: -0.22369274979601664
Avg Winning Trade [%]: 0.020119455831101942
Avg Losing Trade [%]: -0.02152675132969531
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.6651236269493471
Expectancy: -0.4100879184679087
Sharpe Ratio: -16.366428849872438
Calmar Ratio: -9.590586502274059
Omega Ratio: 0.8971511066506718
Sortino Ratio: -23.305120129095236
```

#### RL teaching value (not hard-coded instructions)

Measured score=72.39, PF=0.754, avg return%=-2.326, trades=2998 over 8 set×mode runs. Fidelity=medium; profile=challenge. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_Challenge_EA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`challenge` rules.

### 87. `mt__FTMO_Challenge_EA_FULL`

- **Title:** FTMO_Challenge_EA_FULL
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_Challenge_EA_FULL (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `challenge`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 72.3862

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.326354 |
| Max Drawdown [%] (avg) | 2.667493 |
| Win Rate [%] (avg) | 42.564747 |
| Profit Factor (avg) | 0.753795 |
| Sharpe (avg) | -7.927864 |
| Sortino (avg) | -11.026114 |
| Calmar (avg) | -7.145943 |
| Total Trades (sum) | 2998 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 981 | -5.7467 | 5.8357 | 37.82 | 0.577 | -21.254 |  |
| set1_1m_15m_30m | pullback | 1168 | -4.7898 | 4.9571 | 41.61 | 0.665 | -16.366 |  |
| set2_5m_30m_1h | continuation | 251 | -2.5733 | 2.5933 | 39.60 | 0.624 | -8.462 |  |
| set2_5m_30m_1h | pullback | 368 | -3.2213 | 3.4666 | 44.84 | 0.692 | -7.853 |  |
| set3_15m_1h_4h | continuation | 72 | -1.2723 | 1.4074 | 40.28 | 0.614 | -4.876 |  |
| set3_15m_1h_4h | pullback | 123 | -0.7288 | 1.5599 | 52.46 | 0.869 | -1.947 |  |
| set4_30m_4h_1d | continuation | 13 | 0.2570 | 0.5171 | 38.46 | 1.452 | 1.725 |  |
| set4_30m_4h_1d | pullback | 22 | -0.5355 | 1.0029 | 45.45 | 0.536 | -4.389 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9521.017311229478
Total Return [%]: -4.789826887705222
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 454.57067157289737
Max Drawdown [%]: 4.957108461251716
Max Drawdown Duration: 0.0
Total Trades: 1168
Total Closed Trades: 1168
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.60958904109589
Best Trade [%]: 0.15817548021064193
Worst Trade [%]: -0.22369274979601664
Avg Winning Trade [%]: 0.020119455831101942
Avg Losing Trade [%]: -0.02152675132969531
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.6651236269493471
Expectancy: -0.4100879184679087
Sharpe Ratio: -16.366428849872438
Calmar Ratio: -9.590586502274059
Omega Ratio: 0.8971511066506718
Sortino Ratio: -23.305120129095236
```

#### RL teaching value (not hard-coded instructions)

Measured score=72.39, PF=0.754, avg return%=-2.326, trades=2998 over 8 set×mode runs. Fidelity=medium; profile=challenge. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_Challenge_EA_FULL`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`challenge` rules.

### 88. `mt__ftmo_challenge_ea_v3`

- **Title:** ftmo_challenge_ea_v3
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: ftmo_challenge_ea_v3 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `challenge`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 72.3862

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.326354 |
| Max Drawdown [%] (avg) | 2.667493 |
| Win Rate [%] (avg) | 42.564747 |
| Profit Factor (avg) | 0.753795 |
| Sharpe (avg) | -7.927864 |
| Sortino (avg) | -11.026114 |
| Calmar (avg) | -7.145943 |
| Total Trades (sum) | 2998 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 981 | -5.7467 | 5.8357 | 37.82 | 0.577 | -21.254 |  |
| set1_1m_15m_30m | pullback | 1168 | -4.7898 | 4.9571 | 41.61 | 0.665 | -16.366 |  |
| set2_5m_30m_1h | continuation | 251 | -2.5733 | 2.5933 | 39.60 | 0.624 | -8.462 |  |
| set2_5m_30m_1h | pullback | 368 | -3.2213 | 3.4666 | 44.84 | 0.692 | -7.853 |  |
| set3_15m_1h_4h | continuation | 72 | -1.2723 | 1.4074 | 40.28 | 0.614 | -4.876 |  |
| set3_15m_1h_4h | pullback | 123 | -0.7288 | 1.5599 | 52.46 | 0.869 | -1.947 |  |
| set4_30m_4h_1d | continuation | 13 | 0.2570 | 0.5171 | 38.46 | 1.452 | 1.725 |  |
| set4_30m_4h_1d | pullback | 22 | -0.5355 | 1.0029 | 45.45 | 0.536 | -4.389 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9521.017311229478
Total Return [%]: -4.789826887705222
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 454.57067157289737
Max Drawdown [%]: 4.957108461251716
Max Drawdown Duration: 0.0
Total Trades: 1168
Total Closed Trades: 1168
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.60958904109589
Best Trade [%]: 0.15817548021064193
Worst Trade [%]: -0.22369274979601664
Avg Winning Trade [%]: 0.020119455831101942
Avg Losing Trade [%]: -0.02152675132969531
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.6651236269493471
Expectancy: -0.4100879184679087
Sharpe Ratio: -16.366428849872438
Calmar Ratio: -9.590586502274059
Omega Ratio: 0.8971511066506718
Sortino Ratio: -23.305120129095236
```

#### RL teaching value (not hard-coded instructions)

Measured score=72.39, PF=0.754, avg return%=-2.326, trades=2998 over 8 set×mode runs. Fidelity=medium; profile=challenge. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `ftmo_challenge_ea_v3`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`challenge` rules.

### 89. `mt__FTMO_Challenge_v4`

- **Title:** FTMO_Challenge_v4
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_Challenge_v4 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `challenge`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 72.3862

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.326354 |
| Max Drawdown [%] (avg) | 2.667493 |
| Win Rate [%] (avg) | 42.564747 |
| Profit Factor (avg) | 0.753795 |
| Sharpe (avg) | -7.927864 |
| Sortino (avg) | -11.026114 |
| Calmar (avg) | -7.145943 |
| Total Trades (sum) | 2998 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 981 | -5.7467 | 5.8357 | 37.82 | 0.577 | -21.254 |  |
| set1_1m_15m_30m | pullback | 1168 | -4.7898 | 4.9571 | 41.61 | 0.665 | -16.366 |  |
| set2_5m_30m_1h | continuation | 251 | -2.5733 | 2.5933 | 39.60 | 0.624 | -8.462 |  |
| set2_5m_30m_1h | pullback | 368 | -3.2213 | 3.4666 | 44.84 | 0.692 | -7.853 |  |
| set3_15m_1h_4h | continuation | 72 | -1.2723 | 1.4074 | 40.28 | 0.614 | -4.876 |  |
| set3_15m_1h_4h | pullback | 123 | -0.7288 | 1.5599 | 52.46 | 0.869 | -1.947 |  |
| set4_30m_4h_1d | continuation | 13 | 0.2570 | 0.5171 | 38.46 | 1.452 | 1.725 |  |
| set4_30m_4h_1d | pullback | 22 | -0.5355 | 1.0029 | 45.45 | 0.536 | -4.389 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9521.017311229478
Total Return [%]: -4.789826887705222
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 454.57067157289737
Max Drawdown [%]: 4.957108461251716
Max Drawdown Duration: 0.0
Total Trades: 1168
Total Closed Trades: 1168
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.60958904109589
Best Trade [%]: 0.15817548021064193
Worst Trade [%]: -0.22369274979601664
Avg Winning Trade [%]: 0.020119455831101942
Avg Losing Trade [%]: -0.02152675132969531
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.6651236269493471
Expectancy: -0.4100879184679087
Sharpe Ratio: -16.366428849872438
Calmar Ratio: -9.590586502274059
Omega Ratio: 0.8971511066506718
Sortino Ratio: -23.305120129095236
```

#### RL teaching value (not hard-coded instructions)

Measured score=72.39, PF=0.754, avg return%=-2.326, trades=2998 over 8 set×mode runs. Fidelity=medium; profile=challenge. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_Challenge_v4`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`challenge` rules.

### 90. `mt__FtmoDecisionTree`

- **Title:** FtmoDecisionTree
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FtmoDecisionTree (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `challenge`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 72.3862

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.326354 |
| Max Drawdown [%] (avg) | 2.667493 |
| Win Rate [%] (avg) | 42.564747 |
| Profit Factor (avg) | 0.753795 |
| Sharpe (avg) | -7.927864 |
| Sortino (avg) | -11.026114 |
| Calmar (avg) | -7.145943 |
| Total Trades (sum) | 2998 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 981 | -5.7467 | 5.8357 | 37.82 | 0.577 | -21.254 |  |
| set1_1m_15m_30m | pullback | 1168 | -4.7898 | 4.9571 | 41.61 | 0.665 | -16.366 |  |
| set2_5m_30m_1h | continuation | 251 | -2.5733 | 2.5933 | 39.60 | 0.624 | -8.462 |  |
| set2_5m_30m_1h | pullback | 368 | -3.2213 | 3.4666 | 44.84 | 0.692 | -7.853 |  |
| set3_15m_1h_4h | continuation | 72 | -1.2723 | 1.4074 | 40.28 | 0.614 | -4.876 |  |
| set3_15m_1h_4h | pullback | 123 | -0.7288 | 1.5599 | 52.46 | 0.869 | -1.947 |  |
| set4_30m_4h_1d | continuation | 13 | 0.2570 | 0.5171 | 38.46 | 1.452 | 1.725 |  |
| set4_30m_4h_1d | pullback | 22 | -0.5355 | 1.0029 | 45.45 | 0.536 | -4.389 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9521.017311229478
Total Return [%]: -4.789826887705222
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 454.57067157289737
Max Drawdown [%]: 4.957108461251716
Max Drawdown Duration: 0.0
Total Trades: 1168
Total Closed Trades: 1168
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.60958904109589
Best Trade [%]: 0.15817548021064193
Worst Trade [%]: -0.22369274979601664
Avg Winning Trade [%]: 0.020119455831101942
Avg Losing Trade [%]: -0.02152675132969531
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.6651236269493471
Expectancy: -0.4100879184679087
Sharpe Ratio: -16.366428849872438
Calmar Ratio: -9.590586502274059
Omega Ratio: 0.8971511066506718
Sortino Ratio: -23.305120129095236
```

#### RL teaching value (not hard-coded instructions)

Measured score=72.39, PF=0.754, avg return%=-2.326, trades=2998 over 8 set×mode runs. Fidelity=medium; profile=challenge. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FtmoDecisionTree`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`challenge` rules.

### 91. `mt__S11_Runner`

- **Title:** S11_Runner
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: S11_Runner (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `challenge`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 72.3862

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.326354 |
| Max Drawdown [%] (avg) | 2.667493 |
| Win Rate [%] (avg) | 42.564747 |
| Profit Factor (avg) | 0.753795 |
| Sharpe (avg) | -7.927864 |
| Sortino (avg) | -11.026114 |
| Calmar (avg) | -7.145943 |
| Total Trades (sum) | 2998 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 981 | -5.7467 | 5.8357 | 37.82 | 0.577 | -21.254 |  |
| set1_1m_15m_30m | pullback | 1168 | -4.7898 | 4.9571 | 41.61 | 0.665 | -16.366 |  |
| set2_5m_30m_1h | continuation | 251 | -2.5733 | 2.5933 | 39.60 | 0.624 | -8.462 |  |
| set2_5m_30m_1h | pullback | 368 | -3.2213 | 3.4666 | 44.84 | 0.692 | -7.853 |  |
| set3_15m_1h_4h | continuation | 72 | -1.2723 | 1.4074 | 40.28 | 0.614 | -4.876 |  |
| set3_15m_1h_4h | pullback | 123 | -0.7288 | 1.5599 | 52.46 | 0.869 | -1.947 |  |
| set4_30m_4h_1d | continuation | 13 | 0.2570 | 0.5171 | 38.46 | 1.452 | 1.725 |  |
| set4_30m_4h_1d | pullback | 22 | -0.5355 | 1.0029 | 45.45 | 0.536 | -4.389 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9521.017311229478
Total Return [%]: -4.789826887705222
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 454.57067157289737
Max Drawdown [%]: 4.957108461251716
Max Drawdown Duration: 0.0
Total Trades: 1168
Total Closed Trades: 1168
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.60958904109589
Best Trade [%]: 0.15817548021064193
Worst Trade [%]: -0.22369274979601664
Avg Winning Trade [%]: 0.020119455831101942
Avg Losing Trade [%]: -0.02152675132969531
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.6651236269493471
Expectancy: -0.4100879184679087
Sharpe Ratio: -16.366428849872438
Calmar Ratio: -9.590586502274059
Omega Ratio: 0.8971511066506718
Sortino Ratio: -23.305120129095236
```

#### RL teaching value (not hard-coded instructions)

Measured score=72.39, PF=0.754, avg return%=-2.326, trades=2998 over 8 set×mode runs. Fidelity=medium; profile=challenge. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `S11_Runner`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`challenge` rules.

### 92. `mt__Linear_Regression_Screener`

- **Title:** Linear_Regression_Screener
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Linear_Regression_Screener (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `linreg`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 70.1264

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.899432 |
| Max Drawdown [%] (avg) | 1.340093 |
| Win Rate [%] (avg) | 42.894354 |
| Profit Factor (avg) | 0.713608 |
| Sharpe (avg) | -4.693339 |
| Sortino (avg) | -6.220305 |
| Calmar (avg) | -5.621998 |
| Total Trades (sum) | 1043 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 611 | -4.9488 | 5.0800 | 37.32 | 0.479 | -20.490 |  |
| set1_1m_15m_30m | pullback | 174 | -0.8457 | 0.9101 | 43.10 | 0.650 | -7.130 |  |
| set2_5m_30m_1h | continuation | 138 | -0.7167 | 1.6065 | 45.65 | 0.774 | -3.366 |  |
| set2_5m_30m_1h | pullback | 48 | -0.4598 | 0.7031 | 60.42 | 0.786 | -2.328 |  |
| set3_15m_1h_4h | continuation | 40 | 0.4870 | 0.8796 | 50.00 | 1.300 | 1.865 |  |
| set3_15m_1h_4h | pullback | 12 | -0.2097 | 0.3822 | 41.67 | 0.636 | -2.099 |  |
| set4_30m_4h_1d | continuation | 16 | -0.4195 | 0.8686 | 40.00 | 0.576 | -3.089 |  |
| set4_30m_4h_1d | pullback | 4 | -0.0823 | 0.2908 | 25.00 | 0.508 | -0.909 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9915.43250205778
Total Return [%]: -0.8456749794222014
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 69.22183642064579
Max Drawdown [%]: 0.9100636833549903
Max Drawdown Duration: 0.0
Total Trades: 174
Total Closed Trades: 174
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 43.103448275862064
Best Trade [%]: 0.06287203151437902
Worst Trade [%]: -0.09964945141224066
Avg Winning Trade [%]: 0.021040134005632607
Avg Losing Trade [%]: -0.024510036955371878
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.649796019832006
Expectancy: -0.4860201031162308
Sharpe Ratio: -7.130485655988867
Calmar Ratio: -11.606092998741563
Omega Ratio: 0.8863268234040681
Sortino Ratio: -9.797226688946848
```

#### RL teaching value (not hard-coded instructions)

Measured score=70.13, PF=0.714, avg return%=-0.899, trades=1043 over 8 set×mode runs. Fidelity=medium; profile=linreg. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `Linear_Regression_Screener`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`linreg` rules.

### 93. `mt__LinearRegressionLine`

- **Title:** LinearRegressionLine
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: LinearRegressionLine (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `linreg`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 70.1264

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.899432 |
| Max Drawdown [%] (avg) | 1.340093 |
| Win Rate [%] (avg) | 42.894354 |
| Profit Factor (avg) | 0.713608 |
| Sharpe (avg) | -4.693339 |
| Sortino (avg) | -6.220305 |
| Calmar (avg) | -5.621998 |
| Total Trades (sum) | 1043 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 611 | -4.9488 | 5.0800 | 37.32 | 0.479 | -20.490 |  |
| set1_1m_15m_30m | pullback | 174 | -0.8457 | 0.9101 | 43.10 | 0.650 | -7.130 |  |
| set2_5m_30m_1h | continuation | 138 | -0.7167 | 1.6065 | 45.65 | 0.774 | -3.366 |  |
| set2_5m_30m_1h | pullback | 48 | -0.4598 | 0.7031 | 60.42 | 0.786 | -2.328 |  |
| set3_15m_1h_4h | continuation | 40 | 0.4870 | 0.8796 | 50.00 | 1.300 | 1.865 |  |
| set3_15m_1h_4h | pullback | 12 | -0.2097 | 0.3822 | 41.67 | 0.636 | -2.099 |  |
| set4_30m_4h_1d | continuation | 16 | -0.4195 | 0.8686 | 40.00 | 0.576 | -3.089 |  |
| set4_30m_4h_1d | pullback | 4 | -0.0823 | 0.2908 | 25.00 | 0.508 | -0.909 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9915.43250205778
Total Return [%]: -0.8456749794222014
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 69.22183642064579
Max Drawdown [%]: 0.9100636833549903
Max Drawdown Duration: 0.0
Total Trades: 174
Total Closed Trades: 174
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 43.103448275862064
Best Trade [%]: 0.06287203151437902
Worst Trade [%]: -0.09964945141224066
Avg Winning Trade [%]: 0.021040134005632607
Avg Losing Trade [%]: -0.024510036955371878
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.649796019832006
Expectancy: -0.4860201031162308
Sharpe Ratio: -7.130485655988867
Calmar Ratio: -11.606092998741563
Omega Ratio: 0.8863268234040681
Sortino Ratio: -9.797226688946848
```

#### RL teaching value (not hard-coded instructions)

Measured score=70.13, PF=0.714, avg return%=-0.899, trades=1043 over 8 set×mode runs. Fidelity=medium; profile=linreg. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `LinearRegressionLine`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`linreg` rules.

### 94. `mt__LinearRegressionRSI_EA`

- **Title:** LinearRegressionRSI_EA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: LinearRegressionRSI_EA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `linreg`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 70.1264

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.899432 |
| Max Drawdown [%] (avg) | 1.340093 |
| Win Rate [%] (avg) | 42.894354 |
| Profit Factor (avg) | 0.713608 |
| Sharpe (avg) | -4.693339 |
| Sortino (avg) | -6.220305 |
| Calmar (avg) | -5.621998 |
| Total Trades (sum) | 1043 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 611 | -4.9488 | 5.0800 | 37.32 | 0.479 | -20.490 |  |
| set1_1m_15m_30m | pullback | 174 | -0.8457 | 0.9101 | 43.10 | 0.650 | -7.130 |  |
| set2_5m_30m_1h | continuation | 138 | -0.7167 | 1.6065 | 45.65 | 0.774 | -3.366 |  |
| set2_5m_30m_1h | pullback | 48 | -0.4598 | 0.7031 | 60.42 | 0.786 | -2.328 |  |
| set3_15m_1h_4h | continuation | 40 | 0.4870 | 0.8796 | 50.00 | 1.300 | 1.865 |  |
| set3_15m_1h_4h | pullback | 12 | -0.2097 | 0.3822 | 41.67 | 0.636 | -2.099 |  |
| set4_30m_4h_1d | continuation | 16 | -0.4195 | 0.8686 | 40.00 | 0.576 | -3.089 |  |
| set4_30m_4h_1d | pullback | 4 | -0.0823 | 0.2908 | 25.00 | 0.508 | -0.909 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9915.43250205778
Total Return [%]: -0.8456749794222014
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 69.22183642064579
Max Drawdown [%]: 0.9100636833549903
Max Drawdown Duration: 0.0
Total Trades: 174
Total Closed Trades: 174
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 43.103448275862064
Best Trade [%]: 0.06287203151437902
Worst Trade [%]: -0.09964945141224066
Avg Winning Trade [%]: 0.021040134005632607
Avg Losing Trade [%]: -0.024510036955371878
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.649796019832006
Expectancy: -0.4860201031162308
Sharpe Ratio: -7.130485655988867
Calmar Ratio: -11.606092998741563
Omega Ratio: 0.8863268234040681
Sortino Ratio: -9.797226688946848
```

#### RL teaching value (not hard-coded instructions)

Measured score=70.13, PF=0.714, avg return%=-0.899, trades=1043 over 8 set×mode runs. Fidelity=medium; profile=linreg. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `LinearRegressionRSI_EA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`linreg` rules.

### 95. `mt__AutoGKCloseIntegral`

- **Title:** AutoGKCloseIntegral
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: AutoGKCloseIntegral (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `ma_sample`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 68.8368

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.945259 |
| Max Drawdown [%] (avg) | 4.797242 |
| Win Rate [%] (avg) | 40.401202 |
| Profit Factor (avg) | 0.739814 |
| Sharpe (avg) | -12.501506 |
| Sortino (avg) | -17.082571 |
| Calmar (avg) | -5.229533 |
| Total Trades (sum) | 4675 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1565 | -10.1951 | 10.2333 | 34.63 | 0.494 | -33.000 |  |
| set1_1m_15m_30m | pullback | 2026 | -13.0537 | 13.0729 | 32.13 | 0.465 | -41.340 |  |
| set2_5m_30m_1h | continuation | 308 | -2.4845 | 2.9873 | 40.39 | 0.659 | -8.685 |  |
| set2_5m_30m_1h | pullback | 447 | -4.2541 | 4.3076 | 36.55 | 0.593 | -13.006 |  |
| set3_15m_1h_4h | continuation | 98 | -0.4300 | 1.9793 | 44.90 | 0.890 | -1.131 |  |
| set3_15m_1h_4h | pullback | 139 | -1.2213 | 2.2147 | 42.75 | 0.760 | -3.260 |  |
| set4_30m_4h_1d | continuation | 40 | 0.1983 | 1.4951 | 48.72 | 1.091 | 0.838 |  |
| set4_30m_4h_1d | pullback | 52 | -0.1216 | 2.0878 | 43.14 | 0.966 | -0.429 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8694.625507275332
Total Return [%]: -13.05374492724668
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 752.7008028778866
Max Drawdown [%]: 13.072867085535798
Max Drawdown Duration: 0.0
Total Trades: 2026
Total Closed Trades: 2026
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 32.13228035538006
Best Trade [%]: 0.24149175420761412
Worst Trade [%]: -0.4693638950042799
Avg Winning Trade [%]: 0.01874654218289474
Avg Losing Trade [%]: -0.019042994744739666
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.465363819634436
Expectancy: -0.6443112007525348
Sharpe Ratio: -41.33965485099452
Calmar Ratio: -6.432835960966412
Omega Ratio: 0.784156863102999
Sortino Ratio: -55.89976218939863
```

#### RL teaching value (not hard-coded instructions)

Measured score=68.84, PF=0.740, avg return%=-3.945, trades=4675 over 8 set×mode runs. Fidelity=low; profile=ma_sample. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `AutoGKCloseIntegral`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`ma_sample` rules.

### 96. `mt__ErrorRatePlot`

- **Title:** ErrorRatePlot
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: ErrorRatePlot (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `ma_sample`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 68.8368

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.945259 |
| Max Drawdown [%] (avg) | 4.797242 |
| Win Rate [%] (avg) | 40.401202 |
| Profit Factor (avg) | 0.739814 |
| Sharpe (avg) | -12.501506 |
| Sortino (avg) | -17.082571 |
| Calmar (avg) | -5.229533 |
| Total Trades (sum) | 4675 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1565 | -10.1951 | 10.2333 | 34.63 | 0.494 | -33.000 |  |
| set1_1m_15m_30m | pullback | 2026 | -13.0537 | 13.0729 | 32.13 | 0.465 | -41.340 |  |
| set2_5m_30m_1h | continuation | 308 | -2.4845 | 2.9873 | 40.39 | 0.659 | -8.685 |  |
| set2_5m_30m_1h | pullback | 447 | -4.2541 | 4.3076 | 36.55 | 0.593 | -13.006 |  |
| set3_15m_1h_4h | continuation | 98 | -0.4300 | 1.9793 | 44.90 | 0.890 | -1.131 |  |
| set3_15m_1h_4h | pullback | 139 | -1.2213 | 2.2147 | 42.75 | 0.760 | -3.260 |  |
| set4_30m_4h_1d | continuation | 40 | 0.1983 | 1.4951 | 48.72 | 1.091 | 0.838 |  |
| set4_30m_4h_1d | pullback | 52 | -0.1216 | 2.0878 | 43.14 | 0.966 | -0.429 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8694.625507275332
Total Return [%]: -13.05374492724668
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 752.7008028778866
Max Drawdown [%]: 13.072867085535798
Max Drawdown Duration: 0.0
Total Trades: 2026
Total Closed Trades: 2026
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 32.13228035538006
Best Trade [%]: 0.24149175420761412
Worst Trade [%]: -0.4693638950042799
Avg Winning Trade [%]: 0.01874654218289474
Avg Losing Trade [%]: -0.019042994744739666
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.465363819634436
Expectancy: -0.6443112007525348
Sharpe Ratio: -41.33965485099452
Calmar Ratio: -6.432835960966412
Omega Ratio: 0.784156863102999
Sortino Ratio: -55.89976218939863
```

#### RL teaching value (not hard-coded instructions)

Measured score=68.84, PF=0.740, avg return%=-3.945, trades=4675 over 8 set×mode runs. Fidelity=low; profile=ma_sample. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `ErrorRatePlot`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`ma_sample` rules.

### 97. `mt__Moving_Average`

- **Title:** Moving Average
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Moving Average (.mq4)`
- **Adapter profile (logic only; family not collapsed):** `ma_sample`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 68.8368

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.945259 |
| Max Drawdown [%] (avg) | 4.797242 |
| Win Rate [%] (avg) | 40.401202 |
| Profit Factor (avg) | 0.739814 |
| Sharpe (avg) | -12.501506 |
| Sortino (avg) | -17.082571 |
| Calmar (avg) | -5.229533 |
| Total Trades (sum) | 4675 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1565 | -10.1951 | 10.2333 | 34.63 | 0.494 | -33.000 |  |
| set1_1m_15m_30m | pullback | 2026 | -13.0537 | 13.0729 | 32.13 | 0.465 | -41.340 |  |
| set2_5m_30m_1h | continuation | 308 | -2.4845 | 2.9873 | 40.39 | 0.659 | -8.685 |  |
| set2_5m_30m_1h | pullback | 447 | -4.2541 | 4.3076 | 36.55 | 0.593 | -13.006 |  |
| set3_15m_1h_4h | continuation | 98 | -0.4300 | 1.9793 | 44.90 | 0.890 | -1.131 |  |
| set3_15m_1h_4h | pullback | 139 | -1.2213 | 2.2147 | 42.75 | 0.760 | -3.260 |  |
| set4_30m_4h_1d | continuation | 40 | 0.1983 | 1.4951 | 48.72 | 1.091 | 0.838 |  |
| set4_30m_4h_1d | pullback | 52 | -0.1216 | 2.0878 | 43.14 | 0.966 | -0.429 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8694.625507275332
Total Return [%]: -13.05374492724668
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 752.7008028778866
Max Drawdown [%]: 13.072867085535798
Max Drawdown Duration: 0.0
Total Trades: 2026
Total Closed Trades: 2026
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 32.13228035538006
Best Trade [%]: 0.24149175420761412
Worst Trade [%]: -0.4693638950042799
Avg Winning Trade [%]: 0.01874654218289474
Avg Losing Trade [%]: -0.019042994744739666
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.465363819634436
Expectancy: -0.6443112007525348
Sharpe Ratio: -41.33965485099452
Calmar Ratio: -6.432835960966412
Omega Ratio: 0.784156863102999
Sortino Ratio: -55.89976218939863
```

#### RL teaching value (not hard-coded instructions)

Measured score=68.84, PF=0.740, avg return%=-3.945, trades=4675 over 8 set×mode runs. Fidelity=medium; profile=ma_sample. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `Moving Average`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`ma_sample` rules.

### 98. `mt__Slope_Screener`

- **Title:** Slope_Screener
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Slope_Screener (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `ma_sample`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 68.8368

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.945259 |
| Max Drawdown [%] (avg) | 4.797242 |
| Win Rate [%] (avg) | 40.401202 |
| Profit Factor (avg) | 0.739814 |
| Sharpe (avg) | -12.501506 |
| Sortino (avg) | -17.082571 |
| Calmar (avg) | -5.229533 |
| Total Trades (sum) | 4675 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1565 | -10.1951 | 10.2333 | 34.63 | 0.494 | -33.000 |  |
| set1_1m_15m_30m | pullback | 2026 | -13.0537 | 13.0729 | 32.13 | 0.465 | -41.340 |  |
| set2_5m_30m_1h | continuation | 308 | -2.4845 | 2.9873 | 40.39 | 0.659 | -8.685 |  |
| set2_5m_30m_1h | pullback | 447 | -4.2541 | 4.3076 | 36.55 | 0.593 | -13.006 |  |
| set3_15m_1h_4h | continuation | 98 | -0.4300 | 1.9793 | 44.90 | 0.890 | -1.131 |  |
| set3_15m_1h_4h | pullback | 139 | -1.2213 | 2.2147 | 42.75 | 0.760 | -3.260 |  |
| set4_30m_4h_1d | continuation | 40 | 0.1983 | 1.4951 | 48.72 | 1.091 | 0.838 |  |
| set4_30m_4h_1d | pullback | 52 | -0.1216 | 2.0878 | 43.14 | 0.966 | -0.429 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8694.625507275332
Total Return [%]: -13.05374492724668
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 752.7008028778866
Max Drawdown [%]: 13.072867085535798
Max Drawdown Duration: 0.0
Total Trades: 2026
Total Closed Trades: 2026
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 32.13228035538006
Best Trade [%]: 0.24149175420761412
Worst Trade [%]: -0.4693638950042799
Avg Winning Trade [%]: 0.01874654218289474
Avg Losing Trade [%]: -0.019042994744739666
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.465363819634436
Expectancy: -0.6443112007525348
Sharpe Ratio: -41.33965485099452
Calmar Ratio: -6.432835960966412
Omega Ratio: 0.784156863102999
Sortino Ratio: -55.89976218939863
```

#### RL teaching value (not hard-coded instructions)

Measured score=68.84, PF=0.740, avg return%=-3.945, trades=4675 over 8 set×mode runs. Fidelity=low; profile=ma_sample. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `Slope_Screener`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`ma_sample` rules.

### 99. `mt__Slope_Screener_Fixed`

- **Title:** Slope_Screener_Fixed
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Slope_Screener_Fixed (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `ma_sample`
- **Fidelity:** low
- **Collapses:** `[]` (empty)
- **Aggregate score:** 68.8368

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.945259 |
| Max Drawdown [%] (avg) | 4.797242 |
| Win Rate [%] (avg) | 40.401202 |
| Profit Factor (avg) | 0.739814 |
| Sharpe (avg) | -12.501506 |
| Sortino (avg) | -17.082571 |
| Calmar (avg) | -5.229533 |
| Total Trades (sum) | 4675 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1565 | -10.1951 | 10.2333 | 34.63 | 0.494 | -33.000 |  |
| set1_1m_15m_30m | pullback | 2026 | -13.0537 | 13.0729 | 32.13 | 0.465 | -41.340 |  |
| set2_5m_30m_1h | continuation | 308 | -2.4845 | 2.9873 | 40.39 | 0.659 | -8.685 |  |
| set2_5m_30m_1h | pullback | 447 | -4.2541 | 4.3076 | 36.55 | 0.593 | -13.006 |  |
| set3_15m_1h_4h | continuation | 98 | -0.4300 | 1.9793 | 44.90 | 0.890 | -1.131 |  |
| set3_15m_1h_4h | pullback | 139 | -1.2213 | 2.2147 | 42.75 | 0.760 | -3.260 |  |
| set4_30m_4h_1d | continuation | 40 | 0.1983 | 1.4951 | 48.72 | 1.091 | 0.838 |  |
| set4_30m_4h_1d | pullback | 52 | -0.1216 | 2.0878 | 43.14 | 0.966 | -0.429 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 8694.625507275332
Total Return [%]: -13.05374492724668
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 752.7008028778866
Max Drawdown [%]: 13.072867085535798
Max Drawdown Duration: 0.0
Total Trades: 2026
Total Closed Trades: 2026
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 32.13228035538006
Best Trade [%]: 0.24149175420761412
Worst Trade [%]: -0.4693638950042799
Avg Winning Trade [%]: 0.01874654218289474
Avg Losing Trade [%]: -0.019042994744739666
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.465363819634436
Expectancy: -0.6443112007525348
Sharpe Ratio: -41.33965485099452
Calmar Ratio: -6.432835960966412
Omega Ratio: 0.784156863102999
Sortino Ratio: -55.89976218939863
```

#### RL teaching value (not hard-coded instructions)

Measured score=68.84, PF=0.740, avg return%=-3.945, trades=4675 over 8 set×mode runs. Fidelity=low; profile=ma_sample. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `Slope_Screener_Fixed`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`ma_sample` rules.

### 100. `mt__fasg_trendday_ea`

- **Title:** fasg_trendday_ea
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: fasg_trendday_ea (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `fasg`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 66.9106

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -3.760879 |
| Max Drawdown [%] (avg) | 4.206528 |
| Win Rate [%] (avg) | 40.486110 |
| Profit Factor (avg) | 0.717231 |
| Sharpe (avg) | -11.221317 |
| Sortino (avg) | -15.524738 |
| Calmar (avg) | -6.485527 |
| Total Trades (sum) | 4559 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 2345 | -13.7535 | 13.7554 | 31.09 | 0.477 | -40.337 |  |
| set1_1m_15m_30m | pullback | 1127 | -5.9856 | 6.0134 | 41.26 | 0.587 | -20.129 |  |
| set2_5m_30m_1h | continuation | 528 | -5.0826 | 5.2074 | 36.81 | 0.592 | -13.061 |  |
| set2_5m_30m_1h | pullback | 252 | -2.3858 | 2.8411 | 49.21 | 0.623 | -8.934 |  |
| set3_15m_1h_4h | continuation | 137 | -1.8933 | 2.1118 | 35.77 | 0.700 | -4.555 |  |
| set3_15m_1h_4h | pullback | 83 | -0.6838 | 1.4105 | 38.55 | 0.834 | -1.713 |  |
| set4_30m_4h_1d | continuation | 55 | -0.5950 | 1.4497 | 36.36 | 0.759 | -2.377 |  |
| set4_30m_4h_1d | pullback | 32 | 0.2925 | 0.8628 | 54.84 | 1.165 | 1.335 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9401.438433940932
Total Return [%]: -5.985615660590684
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 436.3101912978054
Max Drawdown [%]: 6.013445699865794
Max Drawdown Duration: 0.0
Total Trades: 1127
Total Closed Trades: 1127
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 41.25998225377107
Best Trade [%]: 0.19633257568260165
Worst Trade [%]: -0.48324980807405904
Avg Winning Trade [%]: 0.01893433778929474
Avg Losing Trade [%]: -0.022615017081071533
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5873636047889973
Expectancy: -0.5311105288900816
Sharpe Ratio: -20.129165133257306
Calmar Ratio: -9.241108312558588
Omega Ratio: 0.8619539762925061
Sortino Ratio: -27.396117976481577
```

#### RL teaching value (not hard-coded instructions)

Measured score=66.91, PF=0.717, avg return%=-3.761, trades=4559 over 8 set×mode runs. Fidelity=medium; profile=fasg. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `fasg_trendday_ea`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`fasg` rules.

### 101. `mt__CoolBollingerTrendEA`

- **Title:** CoolBollingerTrendEA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: CoolBollingerTrendEA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cool_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 65.6030

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.617337 |
| Max Drawdown [%] (avg) | 3.036652 |
| Win Rate [%] (avg) | 43.029884 |
| Profit Factor (avg) | 0.689795 |
| Sharpe (avg) | -8.493809 |
| Sortino (avg) | -11.661200 |
| Calmar (avg) | -7.079821 |
| Total Trades (sum) | 2845 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 687 | -4.6651 | 4.6876 | 39.74 | 0.543 | -16.627 |  |
| set1_1m_15m_30m | pullback | 1438 | -7.2835 | 7.3651 | 44.65 | 0.588 | -21.995 |  |
| set2_5m_30m_1h | continuation | 174 | -2.7817 | 2.9291 | 37.93 | 0.488 | -10.240 |  |
| set2_5m_30m_1h | pullback | 331 | -3.9910 | 4.2132 | 50.15 | 0.562 | -12.417 |  |
| set3_15m_1h_4h | continuation | 60 | -1.6409 | 1.9641 | 38.33 | 0.563 | -5.186 |  |
| set3_15m_1h_4h | pullback | 97 | -0.5817 | 1.2442 | 44.79 | 0.876 | -1.383 |  |
| set4_30m_4h_1d | continuation | 20 | -0.1909 | 0.6401 | 40.00 | 0.816 | -0.903 |  |
| set4_30m_4h_1d | pullback | 38 | 0.1960 | 1.2496 | 48.65 | 1.081 | 0.801 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9271.652190121325
Total Return [%]: -7.283478098786746
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 552.8605310844356
Max Drawdown [%]: 7.365147738435769
Max Drawdown Duration: 0.0
Total Trades: 1438
Total Closed Trades: 1438
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.645340751043115
Best Trade [%]: 0.19633257568258922
Worst Trade [%]: -0.5060595386804977
Avg Winning Trade [%]: 0.016888490686801934
Avg Losing Trade [%]: -0.023113097369056687
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5884800810768674
Expectancy: -0.5065005631979532
Sharpe Ratio: -21.99477710624695
Calmar Ratio: -8.552487085414352
Omega Ratio: 0.869128605674161
Sortino Ratio: -29.87834193680804
```

#### RL teaching value (not hard-coded instructions)

Measured score=65.60, PF=0.690, avg return%=-2.617, trades=2845 over 8 set×mode runs. Fidelity=medium; profile=cool_bb. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `CoolBollingerTrendEA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cool_bb` rules.

### 102. `mt__coolboolinger`

- **Title:** coolboolinger
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: coolboolinger (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `cool_bb`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 65.6030

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.617337 |
| Max Drawdown [%] (avg) | 3.036652 |
| Win Rate [%] (avg) | 43.029884 |
| Profit Factor (avg) | 0.689795 |
| Sharpe (avg) | -8.493809 |
| Sortino (avg) | -11.661200 |
| Calmar (avg) | -7.079821 |
| Total Trades (sum) | 2845 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 687 | -4.6651 | 4.6876 | 39.74 | 0.543 | -16.627 |  |
| set1_1m_15m_30m | pullback | 1438 | -7.2835 | 7.3651 | 44.65 | 0.588 | -21.995 |  |
| set2_5m_30m_1h | continuation | 174 | -2.7817 | 2.9291 | 37.93 | 0.488 | -10.240 |  |
| set2_5m_30m_1h | pullback | 331 | -3.9910 | 4.2132 | 50.15 | 0.562 | -12.417 |  |
| set3_15m_1h_4h | continuation | 60 | -1.6409 | 1.9641 | 38.33 | 0.563 | -5.186 |  |
| set3_15m_1h_4h | pullback | 97 | -0.5817 | 1.2442 | 44.79 | 0.876 | -1.383 |  |
| set4_30m_4h_1d | continuation | 20 | -0.1909 | 0.6401 | 40.00 | 0.816 | -0.903 |  |
| set4_30m_4h_1d | pullback | 38 | 0.1960 | 1.2496 | 48.65 | 1.081 | 0.801 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9271.652190121325
Total Return [%]: -7.283478098786746
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 552.8605310844356
Max Drawdown [%]: 7.365147738435769
Max Drawdown Duration: 0.0
Total Trades: 1438
Total Closed Trades: 1438
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 44.645340751043115
Best Trade [%]: 0.19633257568258922
Worst Trade [%]: -0.5060595386804977
Avg Winning Trade [%]: 0.016888490686801934
Avg Losing Trade [%]: -0.023113097369056687
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5884800810768674
Expectancy: -0.5065005631979532
Sharpe Ratio: -21.99477710624695
Calmar Ratio: -8.552487085414352
Omega Ratio: 0.869128605674161
Sortino Ratio: -29.87834193680804
```

#### RL teaching value (not hard-coded instructions)

Measured score=65.60, PF=0.690, avg return%=-2.617, trades=2845 over 8 set×mode runs. Fidelity=medium; profile=cool_bb. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `coolboolinger`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`cool_bb` rules.

### 103. `mt__CCI_ShiftedSMA_Signal_3D`

- **Title:** CCI_ShiftedSMA_Signal_3D
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: CCI_ShiftedSMA_Signal_3D (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `ati_sma`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 63.9178

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -2.799142 |
| Max Drawdown [%] (avg) | 3.433800 |
| Win Rate [%] (avg) | 42.561406 |
| Profit Factor (avg) | 0.675754 |
| Sharpe (avg) | -10.477666 |
| Sortino (avg) | -14.426755 |
| Calmar (avg) | -6.752182 |
| Total Trades (sum) | 3086 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1013 | -7.3189 | 7.3445 | 35.54 | 0.488 | -28.097 |  |
| set1_1m_15m_30m | pullback | 1343 | -8.9693 | 8.9875 | 35.52 | 0.489 | -31.396 |  |
| set2_5m_30m_1h | continuation | 198 | -1.4846 | 1.7384 | 41.62 | 0.689 | -6.693 |  |
| set2_5m_30m_1h | pullback | 310 | -2.5199 | 2.6809 | 40.13 | 0.645 | -8.850 |  |
| set3_15m_1h_4h | continuation | 62 | -0.8409 | 2.2752 | 44.26 | 0.748 | -2.999 |  |
| set3_15m_1h_4h | pullback | 96 | 0.2616 | 1.5732 | 49.47 | 1.074 | 0.825 |  |
| set4_30m_4h_1d | continuation | 26 | -0.7560 | 1.1524 | 48.00 | 0.585 | -3.522 |  |
| set4_30m_4h_1d | pullback | 38 | -0.7652 | 1.7183 | 45.95 | 0.688 | -3.090 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9103.072875491987
Total Return [%]: -8.969271245080126
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 511.5460494458294
Max Drawdown [%]: 8.987501343115913
Max Drawdown Duration: 0.0
Total Trades: 1343
Total Closed Trades: 1343
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 35.51749813849591
Best Trade [%]: 0.18741096147729988
Worst Trade [%]: -0.16644835047036638
Avg Winning Trade [%]: 0.01885693660714375
Avg Losing Trade [%]: -0.021232202533181484
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.4886973054403183
Expectancy: -0.6678534061861834
Sharpe Ratio: -31.396157221842778
Calmar Ratio: -7.891142910310927
Omega Ratio: 0.8097059795632361
Sortino Ratio: -43.331433421235936
```

#### RL teaching value (not hard-coded instructions)

Measured score=63.92, PF=0.676, avg return%=-2.799, trades=3086 over 8 set×mode runs. Fidelity=medium; profile=ati_sma. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `CCI_ShiftedSMA_Signal_3D`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`ati_sma` rules.

### 104. `mt__fixed_FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323`

- **Title:** fixed_FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: fixed_FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `bb_mtf`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 60.8905

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.816063 |
| Max Drawdown [%] (avg) | 1.126024 |
| Win Rate [%] (avg) | 35.305364 |
| Profit Factor (avg) | 0.619881 |
| Sharpe (avg) | -4.578582 |
| Sortino (avg) | -6.224590 |
| Calmar (avg) | -5.021299 |
| Total Trades (sum) | 915 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 575 | -2.9028 | 3.0020 | 39.30 | 0.624 | -14.377 |  |
| set1_1m_15m_30m | pullback | 112 | -1.0958 | 1.2288 | 37.50 | 0.422 | -9.112 |  |
| set2_5m_30m_1h | continuation | 141 | -0.7820 | 1.1925 | 40.43 | 0.774 | -3.607 |  |
| set2_5m_30m_1h | pullback | 35 | -1.8136 | 2.0686 | 37.14 | 0.207 | -8.714 |  |
| set3_15m_1h_4h | continuation | 38 | 0.2835 | 0.4603 | 44.74 | 1.250 | 1.465 |  |
| set3_15m_1h_4h | pullback | 6 | 0.0604 | 0.4571 | 50.00 | 1.161 | 0.610 |  |
| set4_30m_4h_1d | continuation | 6 | -0.2529 | 0.4826 | 33.33 | 0.520 | -2.225 |  |
| set4_30m_4h_1d | pullback | 2 | -0.0252 | 0.1162 | 0.00 | 0.000 | -0.668 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9890.41854046494
Total Return [%]: -1.0958145953506029
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 44.57173476616428
Max Drawdown [%]: 1.2288276241153977
Max Drawdown Duration: 0.0
Total Trades: 112
Total Closed Trades: 112
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.5
Best Trade [%]: 0.05451985944776561
Worst Trade [%]: -0.22369274979601506
Avg Winning Trade [%]: 0.019187967574531773
Avg Losing Trade [%]: -0.027243130959410743
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.42248456312549604
Expectancy: -0.9784058887058739
Sharpe Ratio: -9.111799090668418
Calmar Ratio: -10.972174303969698
Omega Ratio: 0.7959972636823066
Sortino Ratio: -12.711336865730953
```

#### RL teaching value (not hard-coded instructions)

Measured score=60.89, PF=0.620, avg return%=-0.816, trades=915 over 8 set×mode runs. Fidelity=medium; profile=bb_mtf. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `fixed_FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`bb_mtf` rules.

### 105. `mt__FTMO_BB_MTF_EA_Strategy4`

- **Title:** FTMO_BB_MTF_EA_Strategy4
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_BB_MTF_EA_Strategy4 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `bb_mtf`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 60.8905

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.816063 |
| Max Drawdown [%] (avg) | 1.126024 |
| Win Rate [%] (avg) | 35.305364 |
| Profit Factor (avg) | 0.619881 |
| Sharpe (avg) | -4.578582 |
| Sortino (avg) | -6.224590 |
| Calmar (avg) | -5.021299 |
| Total Trades (sum) | 915 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 575 | -2.9028 | 3.0020 | 39.30 | 0.624 | -14.377 |  |
| set1_1m_15m_30m | pullback | 112 | -1.0958 | 1.2288 | 37.50 | 0.422 | -9.112 |  |
| set2_5m_30m_1h | continuation | 141 | -0.7820 | 1.1925 | 40.43 | 0.774 | -3.607 |  |
| set2_5m_30m_1h | pullback | 35 | -1.8136 | 2.0686 | 37.14 | 0.207 | -8.714 |  |
| set3_15m_1h_4h | continuation | 38 | 0.2835 | 0.4603 | 44.74 | 1.250 | 1.465 |  |
| set3_15m_1h_4h | pullback | 6 | 0.0604 | 0.4571 | 50.00 | 1.161 | 0.610 |  |
| set4_30m_4h_1d | continuation | 6 | -0.2529 | 0.4826 | 33.33 | 0.520 | -2.225 |  |
| set4_30m_4h_1d | pullback | 2 | -0.0252 | 0.1162 | 0.00 | 0.000 | -0.668 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9890.41854046494
Total Return [%]: -1.0958145953506029
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 44.57173476616428
Max Drawdown [%]: 1.2288276241153977
Max Drawdown Duration: 0.0
Total Trades: 112
Total Closed Trades: 112
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.5
Best Trade [%]: 0.05451985944776561
Worst Trade [%]: -0.22369274979601506
Avg Winning Trade [%]: 0.019187967574531773
Avg Losing Trade [%]: -0.027243130959410743
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.42248456312549604
Expectancy: -0.9784058887058739
Sharpe Ratio: -9.111799090668418
Calmar Ratio: -10.972174303969698
Omega Ratio: 0.7959972636823066
Sortino Ratio: -12.711336865730953
```

#### RL teaching value (not hard-coded instructions)

Measured score=60.89, PF=0.620, avg return%=-0.816, trades=915 over 8 set×mode runs. Fidelity=medium; profile=bb_mtf. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_BB_MTF_EA_Strategy4`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`bb_mtf` rules.

### 106. `mt__FTMO_BB_MTF_EA_Strategy4_20260705_1210`

- **Title:** FTMO_BB_MTF_EA_Strategy4_20260705_1210
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_BB_MTF_EA_Strategy4_20260705_1210 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `bb_mtf`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 60.8905

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.816063 |
| Max Drawdown [%] (avg) | 1.126024 |
| Win Rate [%] (avg) | 35.305364 |
| Profit Factor (avg) | 0.619881 |
| Sharpe (avg) | -4.578582 |
| Sortino (avg) | -6.224590 |
| Calmar (avg) | -5.021299 |
| Total Trades (sum) | 915 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 575 | -2.9028 | 3.0020 | 39.30 | 0.624 | -14.377 |  |
| set1_1m_15m_30m | pullback | 112 | -1.0958 | 1.2288 | 37.50 | 0.422 | -9.112 |  |
| set2_5m_30m_1h | continuation | 141 | -0.7820 | 1.1925 | 40.43 | 0.774 | -3.607 |  |
| set2_5m_30m_1h | pullback | 35 | -1.8136 | 2.0686 | 37.14 | 0.207 | -8.714 |  |
| set3_15m_1h_4h | continuation | 38 | 0.2835 | 0.4603 | 44.74 | 1.250 | 1.465 |  |
| set3_15m_1h_4h | pullback | 6 | 0.0604 | 0.4571 | 50.00 | 1.161 | 0.610 |  |
| set4_30m_4h_1d | continuation | 6 | -0.2529 | 0.4826 | 33.33 | 0.520 | -2.225 |  |
| set4_30m_4h_1d | pullback | 2 | -0.0252 | 0.1162 | 0.00 | 0.000 | -0.668 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9890.41854046494
Total Return [%]: -1.0958145953506029
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 44.57173476616428
Max Drawdown [%]: 1.2288276241153977
Max Drawdown Duration: 0.0
Total Trades: 112
Total Closed Trades: 112
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.5
Best Trade [%]: 0.05451985944776561
Worst Trade [%]: -0.22369274979601506
Avg Winning Trade [%]: 0.019187967574531773
Avg Losing Trade [%]: -0.027243130959410743
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.42248456312549604
Expectancy: -0.9784058887058739
Sharpe Ratio: -9.111799090668418
Calmar Ratio: -10.972174303969698
Omega Ratio: 0.7959972636823066
Sortino Ratio: -12.711336865730953
```

#### RL teaching value (not hard-coded instructions)

Measured score=60.89, PF=0.620, avg return%=-0.816, trades=915 over 8 set×mode runs. Fidelity=medium; profile=bb_mtf. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_BB_MTF_EA_Strategy4_20260705_1210`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`bb_mtf` rules.

### 107. `mt__FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323`

- **Title:** FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `bb_mtf`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 60.8905

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.816063 |
| Max Drawdown [%] (avg) | 1.126024 |
| Win Rate [%] (avg) | 35.305364 |
| Profit Factor (avg) | 0.619881 |
| Sharpe (avg) | -4.578582 |
| Sortino (avg) | -6.224590 |
| Calmar (avg) | -5.021299 |
| Total Trades (sum) | 915 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 575 | -2.9028 | 3.0020 | 39.30 | 0.624 | -14.377 |  |
| set1_1m_15m_30m | pullback | 112 | -1.0958 | 1.2288 | 37.50 | 0.422 | -9.112 |  |
| set2_5m_30m_1h | continuation | 141 | -0.7820 | 1.1925 | 40.43 | 0.774 | -3.607 |  |
| set2_5m_30m_1h | pullback | 35 | -1.8136 | 2.0686 | 37.14 | 0.207 | -8.714 |  |
| set3_15m_1h_4h | continuation | 38 | 0.2835 | 0.4603 | 44.74 | 1.250 | 1.465 |  |
| set3_15m_1h_4h | pullback | 6 | 0.0604 | 0.4571 | 50.00 | 1.161 | 0.610 |  |
| set4_30m_4h_1d | continuation | 6 | -0.2529 | 0.4826 | 33.33 | 0.520 | -2.225 |  |
| set4_30m_4h_1d | pullback | 2 | -0.0252 | 0.1162 | 0.00 | 0.000 | -0.668 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9890.41854046494
Total Return [%]: -1.0958145953506029
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 44.57173476616428
Max Drawdown [%]: 1.2288276241153977
Max Drawdown Duration: 0.0
Total Trades: 112
Total Closed Trades: 112
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.5
Best Trade [%]: 0.05451985944776561
Worst Trade [%]: -0.22369274979601506
Avg Winning Trade [%]: 0.019187967574531773
Avg Losing Trade [%]: -0.027243130959410743
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.42248456312549604
Expectancy: -0.9784058887058739
Sharpe Ratio: -9.111799090668418
Calmar Ratio: -10.972174303969698
Omega Ratio: 0.7959972636823066
Sortino Ratio: -12.711336865730953
```

#### RL teaching value (not hard-coded instructions)

Measured score=60.89, PF=0.620, avg return%=-0.816, trades=915 over 8 set×mode runs. Fidelity=medium; profile=bb_mtf. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`bb_mtf` rules.

### 108. `mt__FTMO_BB_MTF_EA_Strategy4_v5`

- **Title:** FTMO_BB_MTF_EA_Strategy4_v5
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_BB_MTF_EA_Strategy4_v5 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `bb_mtf`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 60.8905

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.816063 |
| Max Drawdown [%] (avg) | 1.126024 |
| Win Rate [%] (avg) | 35.305364 |
| Profit Factor (avg) | 0.619881 |
| Sharpe (avg) | -4.578582 |
| Sortino (avg) | -6.224590 |
| Calmar (avg) | -5.021299 |
| Total Trades (sum) | 915 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 575 | -2.9028 | 3.0020 | 39.30 | 0.624 | -14.377 |  |
| set1_1m_15m_30m | pullback | 112 | -1.0958 | 1.2288 | 37.50 | 0.422 | -9.112 |  |
| set2_5m_30m_1h | continuation | 141 | -0.7820 | 1.1925 | 40.43 | 0.774 | -3.607 |  |
| set2_5m_30m_1h | pullback | 35 | -1.8136 | 2.0686 | 37.14 | 0.207 | -8.714 |  |
| set3_15m_1h_4h | continuation | 38 | 0.2835 | 0.4603 | 44.74 | 1.250 | 1.465 |  |
| set3_15m_1h_4h | pullback | 6 | 0.0604 | 0.4571 | 50.00 | 1.161 | 0.610 |  |
| set4_30m_4h_1d | continuation | 6 | -0.2529 | 0.4826 | 33.33 | 0.520 | -2.225 |  |
| set4_30m_4h_1d | pullback | 2 | -0.0252 | 0.1162 | 0.00 | 0.000 | -0.668 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9890.41854046494
Total Return [%]: -1.0958145953506029
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 44.57173476616428
Max Drawdown [%]: 1.2288276241153977
Max Drawdown Duration: 0.0
Total Trades: 112
Total Closed Trades: 112
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.5
Best Trade [%]: 0.05451985944776561
Worst Trade [%]: -0.22369274979601506
Avg Winning Trade [%]: 0.019187967574531773
Avg Losing Trade [%]: -0.027243130959410743
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.42248456312549604
Expectancy: -0.9784058887058739
Sharpe Ratio: -9.111799090668418
Calmar Ratio: -10.972174303969698
Omega Ratio: 0.7959972636823066
Sortino Ratio: -12.711336865730953
```

#### RL teaching value (not hard-coded instructions)

Measured score=60.89, PF=0.620, avg return%=-0.816, trades=915 over 8 set×mode runs. Fidelity=medium; profile=bb_mtf. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_BB_MTF_EA_Strategy4_v5`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`bb_mtf` rules.

### 109. `mt__FTMO_BB_MTF_EA_Strategy4_v6`

- **Title:** FTMO_BB_MTF_EA_Strategy4_v6
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_BB_MTF_EA_Strategy4_v6 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `bb_mtf`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 60.8905

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.816063 |
| Max Drawdown [%] (avg) | 1.126024 |
| Win Rate [%] (avg) | 35.305364 |
| Profit Factor (avg) | 0.619881 |
| Sharpe (avg) | -4.578582 |
| Sortino (avg) | -6.224590 |
| Calmar (avg) | -5.021299 |
| Total Trades (sum) | 915 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 575 | -2.9028 | 3.0020 | 39.30 | 0.624 | -14.377 |  |
| set1_1m_15m_30m | pullback | 112 | -1.0958 | 1.2288 | 37.50 | 0.422 | -9.112 |  |
| set2_5m_30m_1h | continuation | 141 | -0.7820 | 1.1925 | 40.43 | 0.774 | -3.607 |  |
| set2_5m_30m_1h | pullback | 35 | -1.8136 | 2.0686 | 37.14 | 0.207 | -8.714 |  |
| set3_15m_1h_4h | continuation | 38 | 0.2835 | 0.4603 | 44.74 | 1.250 | 1.465 |  |
| set3_15m_1h_4h | pullback | 6 | 0.0604 | 0.4571 | 50.00 | 1.161 | 0.610 |  |
| set4_30m_4h_1d | continuation | 6 | -0.2529 | 0.4826 | 33.33 | 0.520 | -2.225 |  |
| set4_30m_4h_1d | pullback | 2 | -0.0252 | 0.1162 | 0.00 | 0.000 | -0.668 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9890.41854046494
Total Return [%]: -1.0958145953506029
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 44.57173476616428
Max Drawdown [%]: 1.2288276241153977
Max Drawdown Duration: 0.0
Total Trades: 112
Total Closed Trades: 112
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.5
Best Trade [%]: 0.05451985944776561
Worst Trade [%]: -0.22369274979601506
Avg Winning Trade [%]: 0.019187967574531773
Avg Losing Trade [%]: -0.027243130959410743
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.42248456312549604
Expectancy: -0.9784058887058739
Sharpe Ratio: -9.111799090668418
Calmar Ratio: -10.972174303969698
Omega Ratio: 0.7959972636823066
Sortino Ratio: -12.711336865730953
```

#### RL teaching value (not hard-coded instructions)

Measured score=60.89, PF=0.620, avg return%=-0.816, trades=915 over 8 set×mode runs. Fidelity=medium; profile=bb_mtf. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_BB_MTF_EA_Strategy4_v6`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`bb_mtf` rules.

### 110. `mt__FTMO_BB_MTF_EA_Strategy4_v7`

- **Title:** FTMO_BB_MTF_EA_Strategy4_v7
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_BB_MTF_EA_Strategy4_v7 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `bb_mtf`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 60.8905

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.816063 |
| Max Drawdown [%] (avg) | 1.126024 |
| Win Rate [%] (avg) | 35.305364 |
| Profit Factor (avg) | 0.619881 |
| Sharpe (avg) | -4.578582 |
| Sortino (avg) | -6.224590 |
| Calmar (avg) | -5.021299 |
| Total Trades (sum) | 915 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 575 | -2.9028 | 3.0020 | 39.30 | 0.624 | -14.377 |  |
| set1_1m_15m_30m | pullback | 112 | -1.0958 | 1.2288 | 37.50 | 0.422 | -9.112 |  |
| set2_5m_30m_1h | continuation | 141 | -0.7820 | 1.1925 | 40.43 | 0.774 | -3.607 |  |
| set2_5m_30m_1h | pullback | 35 | -1.8136 | 2.0686 | 37.14 | 0.207 | -8.714 |  |
| set3_15m_1h_4h | continuation | 38 | 0.2835 | 0.4603 | 44.74 | 1.250 | 1.465 |  |
| set3_15m_1h_4h | pullback | 6 | 0.0604 | 0.4571 | 50.00 | 1.161 | 0.610 |  |
| set4_30m_4h_1d | continuation | 6 | -0.2529 | 0.4826 | 33.33 | 0.520 | -2.225 |  |
| set4_30m_4h_1d | pullback | 2 | -0.0252 | 0.1162 | 0.00 | 0.000 | -0.668 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9890.41854046494
Total Return [%]: -1.0958145953506029
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 44.57173476616428
Max Drawdown [%]: 1.2288276241153977
Max Drawdown Duration: 0.0
Total Trades: 112
Total Closed Trades: 112
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.5
Best Trade [%]: 0.05451985944776561
Worst Trade [%]: -0.22369274979601506
Avg Winning Trade [%]: 0.019187967574531773
Avg Losing Trade [%]: -0.027243130959410743
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.42248456312549604
Expectancy: -0.9784058887058739
Sharpe Ratio: -9.111799090668418
Calmar Ratio: -10.972174303969698
Omega Ratio: 0.7959972636823066
Sortino Ratio: -12.711336865730953
```

#### RL teaching value (not hard-coded instructions)

Measured score=60.89, PF=0.620, avg return%=-0.816, trades=915 over 8 set×mode runs. Fidelity=medium; profile=bb_mtf. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_BB_MTF_EA_Strategy4_v7`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`bb_mtf` rules.

### 111. `mt__FTMO_CCI_MTF_BB_EA_Part2`

- **Title:** FTMO_CCI_MTF_BB_EA_Part2
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_CCI_MTF_BB_EA_Part2 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `bb_mtf`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 60.8905

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.816063 |
| Max Drawdown [%] (avg) | 1.126024 |
| Win Rate [%] (avg) | 35.305364 |
| Profit Factor (avg) | 0.619881 |
| Sharpe (avg) | -4.578582 |
| Sortino (avg) | -6.224590 |
| Calmar (avg) | -5.021299 |
| Total Trades (sum) | 915 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 575 | -2.9028 | 3.0020 | 39.30 | 0.624 | -14.377 |  |
| set1_1m_15m_30m | pullback | 112 | -1.0958 | 1.2288 | 37.50 | 0.422 | -9.112 |  |
| set2_5m_30m_1h | continuation | 141 | -0.7820 | 1.1925 | 40.43 | 0.774 | -3.607 |  |
| set2_5m_30m_1h | pullback | 35 | -1.8136 | 2.0686 | 37.14 | 0.207 | -8.714 |  |
| set3_15m_1h_4h | continuation | 38 | 0.2835 | 0.4603 | 44.74 | 1.250 | 1.465 |  |
| set3_15m_1h_4h | pullback | 6 | 0.0604 | 0.4571 | 50.00 | 1.161 | 0.610 |  |
| set4_30m_4h_1d | continuation | 6 | -0.2529 | 0.4826 | 33.33 | 0.520 | -2.225 |  |
| set4_30m_4h_1d | pullback | 2 | -0.0252 | 0.1162 | 0.00 | 0.000 | -0.668 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9890.41854046494
Total Return [%]: -1.0958145953506029
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 44.57173476616428
Max Drawdown [%]: 1.2288276241153977
Max Drawdown Duration: 0.0
Total Trades: 112
Total Closed Trades: 112
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.5
Best Trade [%]: 0.05451985944776561
Worst Trade [%]: -0.22369274979601506
Avg Winning Trade [%]: 0.019187967574531773
Avg Losing Trade [%]: -0.027243130959410743
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.42248456312549604
Expectancy: -0.9784058887058739
Sharpe Ratio: -9.111799090668418
Calmar Ratio: -10.972174303969698
Omega Ratio: 0.7959972636823066
Sortino Ratio: -12.711336865730953
```

#### RL teaching value (not hard-coded instructions)

Measured score=60.89, PF=0.620, avg return%=-0.816, trades=915 over 8 set×mode runs. Fidelity=medium; profile=bb_mtf. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_CCI_MTF_BB_EA_Part2`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`bb_mtf` rules.

### 112. `mt__FTMO_CCI_MTF_BB_EA_PART3`

- **Title:** FTMO_CCI_MTF_BB_EA_PART3
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: FTMO_CCI_MTF_BB_EA_PART3 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `bb_mtf`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 60.8905

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.816063 |
| Max Drawdown [%] (avg) | 1.126024 |
| Win Rate [%] (avg) | 35.305364 |
| Profit Factor (avg) | 0.619881 |
| Sharpe (avg) | -4.578582 |
| Sortino (avg) | -6.224590 |
| Calmar (avg) | -5.021299 |
| Total Trades (sum) | 915 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 575 | -2.9028 | 3.0020 | 39.30 | 0.624 | -14.377 |  |
| set1_1m_15m_30m | pullback | 112 | -1.0958 | 1.2288 | 37.50 | 0.422 | -9.112 |  |
| set2_5m_30m_1h | continuation | 141 | -0.7820 | 1.1925 | 40.43 | 0.774 | -3.607 |  |
| set2_5m_30m_1h | pullback | 35 | -1.8136 | 2.0686 | 37.14 | 0.207 | -8.714 |  |
| set3_15m_1h_4h | continuation | 38 | 0.2835 | 0.4603 | 44.74 | 1.250 | 1.465 |  |
| set3_15m_1h_4h | pullback | 6 | 0.0604 | 0.4571 | 50.00 | 1.161 | 0.610 |  |
| set4_30m_4h_1d | continuation | 6 | -0.2529 | 0.4826 | 33.33 | 0.520 | -2.225 |  |
| set4_30m_4h_1d | pullback | 2 | -0.0252 | 0.1162 | 0.00 | 0.000 | -0.668 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9890.41854046494
Total Return [%]: -1.0958145953506029
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 44.57173476616428
Max Drawdown [%]: 1.2288276241153977
Max Drawdown Duration: 0.0
Total Trades: 112
Total Closed Trades: 112
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.5
Best Trade [%]: 0.05451985944776561
Worst Trade [%]: -0.22369274979601506
Avg Winning Trade [%]: 0.019187967574531773
Avg Losing Trade [%]: -0.027243130959410743
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.42248456312549604
Expectancy: -0.9784058887058739
Sharpe Ratio: -9.111799090668418
Calmar Ratio: -10.972174303969698
Omega Ratio: 0.7959972636823066
Sortino Ratio: -12.711336865730953
```

#### RL teaching value (not hard-coded instructions)

Measured score=60.89, PF=0.620, avg return%=-0.816, trades=915 over 8 set×mode runs. Fidelity=medium; profile=bb_mtf. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `FTMO_CCI_MTF_BB_EA_PART3`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`bb_mtf` rules.

### 113. `note__the_truth_main_extra_strategy_S4_rsi_tension_snap_md`

- **Title:** strategy_S4_rsi_tension_snap.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\the_truth_main_extra\strategy_S4_rsi_tension_snap.md`
- **Adapter profile (logic only; family not collapsed):** `truth_s4_rsi_snap`
- **Fidelity:** high
- **Collapses:** `[]` (empty)
- **Aggregate score:** 60.3028

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.649377 |
| Max Drawdown [%] (avg) | 2.162775 |
| Win Rate [%] (avg) | 39.763096 |
| Profit Factor (avg) | 0.624929 |
| Sharpe (avg) | -7.689085 |
| Sortino (avg) | -10.447583 |
| Calmar (avg) | -8.163460 |
| Total Trades (sum) | 1874 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 726 | -4.4917 | 4.5319 | 35.95 | 0.536 | -20.883 |  |
| set1_1m_15m_30m | pullback | 441 | -2.5929 | 2.6831 | 37.64 | 0.592 | -14.850 |  |
| set2_5m_30m_1h | continuation | 277 | -2.2142 | 2.6904 | 38.63 | 0.720 | -6.811 |  |
| set2_5m_30m_1h | pullback | 277 | -2.7079 | 3.2281 | 38.63 | 0.671 | -7.851 |  |
| set3_15m_1h_4h | continuation | 61 | -0.5140 | 1.5799 | 52.46 | 0.834 | -1.848 |  |
| set3_15m_1h_4h | pullback | 74 | 0.3895 | 1.4786 | 47.30 | 1.149 | 1.661 |  |
| set4_30m_4h_1d | continuation | 10 | -0.6233 | 0.6233 | 30.00 | 0.220 | -5.839 |  |
| set4_30m_4h_1d | pullback | 8 | -0.4405 | 0.4868 | 37.50 | 0.276 | -5.091 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9740.709776997173
Total Return [%]: -2.5929022300282667
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 174.6806950590559
Max Drawdown [%]: 2.683094393343903
Max Drawdown Duration: 0.0
Total Trades: 441
Total Closed Trades: 441
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 37.641723356009074
Best Trade [%]: 0.2972708022159645
Worst Trade [%]: -0.11259532074664536
Avg Winning Trade [%]: 0.022892278222739842
Avg Losing Trade [%]: -0.023362841975996675
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5923840172985034
Expectancy: -0.587959689348775
Sharpe Ratio: -14.849669229609317
Calmar Ratio: -10.882817710712674
Omega Ratio: 0.8546981193260085
Sortino Ratio: -20.481700417349625
```

#### RL teaching value (not hard-coded instructions)

Measured score=60.30, PF=0.625, avg return%=-1.649, trades=1874 over 8 set×mode runs. Fidelity=high; profile=truth_s4_rsi_snap. Truth-line geometry (CCI/BB/envelope/RSI snap) is good state/label material for L2L; do not freeze thresholds as production law.

#### 10× better

10× for `strategy_S4_rsi_tension_snap.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`truth_s4_rsi_snap` rules.

### 114. `mt__KineticEdgeEA`

- **Title:** KineticEdgeEA
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: KineticEdgeEA (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `kinetic`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 59.9077

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.725909 |
| Max Drawdown [%] (avg) | 2.131105 |
| Win Rate [%] (avg) | 42.140795 |
| Profit Factor (avg) | 0.621664 |
| Sharpe (avg) | -7.456738 |
| Sortino (avg) | -10.088329 |
| Calmar (avg) | -7.485169 |
| Total Trades (sum) | 1665 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 329 | -2.9535 | 2.9930 | 37.69 | 0.447 | -16.424 |  |
| set1_1m_15m_30m | pullback | 727 | -4.0798 | 4.1252 | 40.72 | 0.555 | -18.232 |  |
| set2_5m_30m_1h | continuation | 143 | -2.3839 | 2.5502 | 41.26 | 0.484 | -9.123 |  |
| set2_5m_30m_1h | pullback | 332 | -2.6923 | 3.1934 | 48.94 | 0.683 | -8.147 |  |
| set3_15m_1h_4h | continuation | 37 | -0.6347 | 1.3019 | 45.95 | 0.665 | -2.722 |  |
| set3_15m_1h_4h | pullback | 80 | -0.9453 | 1.6451 | 39.24 | 0.757 | -2.688 |  |
| set4_30m_4h_1d | continuation | 3 | -0.2220 | 0.4171 | 33.33 | 0.254 | -3.078 |  |
| set4_30m_4h_1d | pullback | 14 | 0.1043 | 0.8229 | 50.00 | 1.128 | 0.759 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9592.01693804019
Total Return [%]: -4.079830619598106
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 283.2295605519594
Max Drawdown [%]: 4.125249146496511
Max Drawdown Duration: 0.0
Total Trades: 727
Total Closed Trades: 727
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 40.715268225584595
Best Trade [%]: 0.09656365641760592
Worst Trade [%]: -0.16780151969410154
Avg Winning Trade [%]: 0.01768433573749172
Avg Losing Trade [%]: -0.021803563527746993
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5550713767391254
Expectancy: -0.5611871553779736
Sharpe Ratio: -18.23181724539375
Calmar Ratio: -10.220087077355496
Omega Ratio: 0.8601136640492015
Sortino Ratio: -25.547244363554857
```

#### RL teaching value (not hard-coded instructions)

Measured score=59.91, PF=0.622, avg return%=-1.726, trades=1665 over 8 set×mode runs. Fidelity=medium; profile=kinetic. CCI/momentum feel features for the brain; optional aux labels, not sole decider.

#### 10× better

10× for `KineticEdgeEA`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`kinetic` rules.

### 115. `note__the_truth_main_extra_strategy_S2_bb_trend_reversion_md`

- **Title:** strategy_S2_bb_trend_reversion.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\the_truth_main_extra\strategy_S2_bb_trend_reversion.md`
- **Adapter profile (logic only; family not collapsed):** `truth_s2_bb`
- **Fidelity:** high
- **Collapses:** `[]` (empty)
- **Aggregate score:** 59.1781

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.341448 |
| Max Drawdown [%] (avg) | 1.529458 |
| Win Rate [%] (avg) | 35.528334 |
| Profit Factor (avg) | 0.609019 |
| Sharpe (avg) | -7.605531 |
| Sortino (avg) | -10.128847 |
| Calmar (avg) | -8.287633 |
| Total Trades (sum) | 1205 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 305 | -1.7288 | 1.8708 | 40.98 | 0.582 | -10.732 |  |
| set1_1m_15m_30m | pullback | 531 | -3.2474 | 3.3375 | 40.11 | 0.557 | -16.029 |  |
| set2_5m_30m_1h | continuation | 90 | -1.9799 | 2.2993 | 32.22 | 0.395 | -11.469 |  |
| set2_5m_30m_1h | pullback | 194 | -1.6425 | 1.6529 | 41.24 | 0.725 | -5.429 |  |
| set3_15m_1h_4h | continuation | 17 | 0.2981 | 0.3686 | 52.94 | 1.767 | 2.321 |  |
| set3_15m_1h_4h | pullback | 53 | -1.3823 | 1.5088 | 43.40 | 0.539 | -5.250 |  |
| set4_30m_4h_1d | continuation | 6 | -0.6404 | 0.6609 | 0.00 | 0.000 | -8.871 |  |
| set4_30m_4h_1d | pullback | 9 | -0.4084 | 0.5371 | 33.33 | 0.308 | -5.386 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9675.264791969164
Total Return [%]: -3.2473520803083558
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 208.18504240158376
Max Drawdown [%]: 3.337450941757182
Max Drawdown Duration: 0.0
Total Trades: 531
Total Closed Trades: 531
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 40.11299435028249
Best Trade [%]: 0.14416530115388965
Worst Trade [%]: -0.16780151969411247
Avg Winning Trade [%]: 0.019540339129238533
Avg Losing Trade [%]: -0.023462260381148604
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5565538683157272
Expectancy: -0.6115540640882169
Sharpe Ratio: -16.029006948017738
Calmar Ratio: -10.547935583037493
Omega Ratio: 0.8510194399335459
Sortino Ratio: -22.74426302313869
```

#### RL teaching value (not hard-coded instructions)

Measured score=59.18, PF=0.609, avg return%=-1.341, trades=1205 over 8 set×mode runs. Fidelity=high; profile=truth_s2_bb. Truth-line geometry (CCI/BB/envelope/RSI snap) is good state/label material for L2L; do not freeze thresholds as production law.

#### 10× better

10× for `strategy_S2_bb_trend_reversion.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`truth_s2_bb` rules.

### 116. `mt__ftmo_ultra`

- **Title:** ftmo ultra
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: ftmo ultra (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `momentum`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 42.6705

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.819440 |
| Max Drawdown [%] (avg) | 1.246760 |
| Win Rate [%] (avg) | 25.381116 |
| Profit Factor (avg) | 0.438017 |
| Sharpe (avg) | -4.456102 |
| Sortino (avg) | -6.121478 |
| Calmar (avg) | -5.143959 |
| Total Trades (sum) | 1163 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 846 | -5.1481 | 5.4517 | 38.06 | 0.551 | -20.139 |  |
| set1_1m_15m_30m | pullback | 20 | -0.2241 | 0.2692 | 25.00 | 0.231 | -7.137 |  |
| set2_5m_30m_1h | continuation | 210 | -0.9979 | 1.4982 | 41.15 | 0.788 | -4.246 |  |
| set2_5m_30m_1h | pullback | 1 | -0.0450 | 0.1023 | 0.00 | 0.000 | -2.199 |  |
| set3_15m_1h_4h | continuation | 67 | 0.0119 | 1.9188 | 43.28 | 1.004 | 0.059 |  |
| set3_15m_1h_4h | pullback | 0 | 0.0000 | 0.0000 | 0.00 | 0.000 | 0.000 |  |
| set4_30m_4h_1d | continuation | 18 | -0.0669 | 0.5259 | 55.56 | 0.929 | -0.345 |  |
| set4_30m_4h_1d | pullback | 1 | -0.0852 | 0.2080 | 0.00 | 0.000 | -1.642 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9977.587359069652
Total Return [%]: -0.22412640930348063
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 7.989303477423205
Max Drawdown [%]: 0.26915244829491825
Max Drawdown Duration: 0.0
Total Trades: 20
Total Closed Trades: 20
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 25.0
Best Trade [%]: 0.03441952541089717
Worst Trade [%]: -0.053402809278552135
Avg Winning Trade [%]: 0.013524227026982149
Avg Losing Trade [%]: -0.019462994979351
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.2314719172367835
Expectancy: -1.120632046517223
Sharpe Ratio: -7.137055197221927
Calmar Ratio: -10.797398250033037
Omega Ratio: 0.7172300468634831
Sortino Ratio: -9.175110294967265
```

#### RL teaching value (not hard-coded instructions)

Measured score=42.67, PF=0.438, avg return%=-0.819, trades=1163 over 8 set×mode runs. Fidelity=medium; profile=momentum. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `ftmo ultra`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`momentum` rules.

### 117. `mt__ftmo_all_assets_momentum_scalper`

- **Title:** ftmo_all_assets_momentum_scalper
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: ftmo_all_assets_momentum_scalper (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `momentum`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 42.6705

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.819440 |
| Max Drawdown [%] (avg) | 1.246760 |
| Win Rate [%] (avg) | 25.381116 |
| Profit Factor (avg) | 0.438017 |
| Sharpe (avg) | -4.456102 |
| Sortino (avg) | -6.121478 |
| Calmar (avg) | -5.143959 |
| Total Trades (sum) | 1163 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 846 | -5.1481 | 5.4517 | 38.06 | 0.551 | -20.139 |  |
| set1_1m_15m_30m | pullback | 20 | -0.2241 | 0.2692 | 25.00 | 0.231 | -7.137 |  |
| set2_5m_30m_1h | continuation | 210 | -0.9979 | 1.4982 | 41.15 | 0.788 | -4.246 |  |
| set2_5m_30m_1h | pullback | 1 | -0.0450 | 0.1023 | 0.00 | 0.000 | -2.199 |  |
| set3_15m_1h_4h | continuation | 67 | 0.0119 | 1.9188 | 43.28 | 1.004 | 0.059 |  |
| set3_15m_1h_4h | pullback | 0 | 0.0000 | 0.0000 | 0.00 | 0.000 | 0.000 |  |
| set4_30m_4h_1d | continuation | 18 | -0.0669 | 0.5259 | 55.56 | 0.929 | -0.345 |  |
| set4_30m_4h_1d | pullback | 1 | -0.0852 | 0.2080 | 0.00 | 0.000 | -1.642 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9977.587359069652
Total Return [%]: -0.22412640930348063
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 7.989303477423205
Max Drawdown [%]: 0.26915244829491825
Max Drawdown Duration: 0.0
Total Trades: 20
Total Closed Trades: 20
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 25.0
Best Trade [%]: 0.03441952541089717
Worst Trade [%]: -0.053402809278552135
Avg Winning Trade [%]: 0.013524227026982149
Avg Losing Trade [%]: -0.019462994979351
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.2314719172367835
Expectancy: -1.120632046517223
Sharpe Ratio: -7.137055197221927
Calmar Ratio: -10.797398250033037
Omega Ratio: 0.7172300468634831
Sortino Ratio: -9.175110294967265
```

#### RL teaching value (not hard-coded instructions)

Measured score=42.67, PF=0.438, avg return%=-0.819, trades=1163 over 8 set×mode runs. Fidelity=medium; profile=momentum. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `ftmo_all_assets_momentum_scalper`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`momentum` rules.

### 118. `mt__HurstX`

- **Title:** HurstX
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: HurstX (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `momentum`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 42.6705

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.819440 |
| Max Drawdown [%] (avg) | 1.246760 |
| Win Rate [%] (avg) | 25.381116 |
| Profit Factor (avg) | 0.438017 |
| Sharpe (avg) | -4.456102 |
| Sortino (avg) | -6.121478 |
| Calmar (avg) | -5.143959 |
| Total Trades (sum) | 1163 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 846 | -5.1481 | 5.4517 | 38.06 | 0.551 | -20.139 |  |
| set1_1m_15m_30m | pullback | 20 | -0.2241 | 0.2692 | 25.00 | 0.231 | -7.137 |  |
| set2_5m_30m_1h | continuation | 210 | -0.9979 | 1.4982 | 41.15 | 0.788 | -4.246 |  |
| set2_5m_30m_1h | pullback | 1 | -0.0450 | 0.1023 | 0.00 | 0.000 | -2.199 |  |
| set3_15m_1h_4h | continuation | 67 | 0.0119 | 1.9188 | 43.28 | 1.004 | 0.059 |  |
| set3_15m_1h_4h | pullback | 0 | 0.0000 | 0.0000 | 0.00 | 0.000 | 0.000 |  |
| set4_30m_4h_1d | continuation | 18 | -0.0669 | 0.5259 | 55.56 | 0.929 | -0.345 |  |
| set4_30m_4h_1d | pullback | 1 | -0.0852 | 0.2080 | 0.00 | 0.000 | -1.642 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9977.587359069652
Total Return [%]: -0.22412640930348063
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 7.989303477423205
Max Drawdown [%]: 0.26915244829491825
Max Drawdown Duration: 0.0
Total Trades: 20
Total Closed Trades: 20
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 25.0
Best Trade [%]: 0.03441952541089717
Worst Trade [%]: -0.053402809278552135
Avg Winning Trade [%]: 0.013524227026982149
Avg Losing Trade [%]: -0.019462994979351
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.2314719172367835
Expectancy: -1.120632046517223
Sharpe Ratio: -7.137055197221927
Calmar Ratio: -10.797398250033037
Omega Ratio: 0.7172300468634831
Sortino Ratio: -9.175110294967265
```

#### RL teaching value (not hard-coded instructions)

Measured score=42.67, PF=0.438, avg return%=-0.819, trades=1163 over 8 set×mode runs. Fidelity=medium; profile=momentum. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `HurstX`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`momentum` rules.

### 119. `mt__Momentum`

- **Title:** Momentum
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Momentum (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `momentum`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 42.6705

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.819440 |
| Max Drawdown [%] (avg) | 1.246760 |
| Win Rate [%] (avg) | 25.381116 |
| Profit Factor (avg) | 0.438017 |
| Sharpe (avg) | -4.456102 |
| Sortino (avg) | -6.121478 |
| Calmar (avg) | -5.143959 |
| Total Trades (sum) | 1163 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 846 | -5.1481 | 5.4517 | 38.06 | 0.551 | -20.139 |  |
| set1_1m_15m_30m | pullback | 20 | -0.2241 | 0.2692 | 25.00 | 0.231 | -7.137 |  |
| set2_5m_30m_1h | continuation | 210 | -0.9979 | 1.4982 | 41.15 | 0.788 | -4.246 |  |
| set2_5m_30m_1h | pullback | 1 | -0.0450 | 0.1023 | 0.00 | 0.000 | -2.199 |  |
| set3_15m_1h_4h | continuation | 67 | 0.0119 | 1.9188 | 43.28 | 1.004 | 0.059 |  |
| set3_15m_1h_4h | pullback | 0 | 0.0000 | 0.0000 | 0.00 | 0.000 | 0.000 |  |
| set4_30m_4h_1d | continuation | 18 | -0.0669 | 0.5259 | 55.56 | 0.929 | -0.345 |  |
| set4_30m_4h_1d | pullback | 1 | -0.0852 | 0.2080 | 0.00 | 0.000 | -1.642 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9977.587359069652
Total Return [%]: -0.22412640930348063
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 7.989303477423205
Max Drawdown [%]: 0.26915244829491825
Max Drawdown Duration: 0.0
Total Trades: 20
Total Closed Trades: 20
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 25.0
Best Trade [%]: 0.03441952541089717
Worst Trade [%]: -0.053402809278552135
Avg Winning Trade [%]: 0.013524227026982149
Avg Losing Trade [%]: -0.019462994979351
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.2314719172367835
Expectancy: -1.120632046517223
Sharpe Ratio: -7.137055197221927
Calmar Ratio: -10.797398250033037
Omega Ratio: 0.7172300468634831
Sortino Ratio: -9.175110294967265
```

#### RL teaching value (not hard-coded instructions)

Measured score=42.67, PF=0.438, avg return%=-0.819, trades=1163 over 8 set×mode runs. Fidelity=medium; profile=momentum. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `Momentum`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`momentum` rules.

### 120. `mt__Simple_scalper`

- **Title:** Simple scalper
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: Simple scalper (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `momentum`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 42.6705

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.819440 |
| Max Drawdown [%] (avg) | 1.246760 |
| Win Rate [%] (avg) | 25.381116 |
| Profit Factor (avg) | 0.438017 |
| Sharpe (avg) | -4.456102 |
| Sortino (avg) | -6.121478 |
| Calmar (avg) | -5.143959 |
| Total Trades (sum) | 1163 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 846 | -5.1481 | 5.4517 | 38.06 | 0.551 | -20.139 |  |
| set1_1m_15m_30m | pullback | 20 | -0.2241 | 0.2692 | 25.00 | 0.231 | -7.137 |  |
| set2_5m_30m_1h | continuation | 210 | -0.9979 | 1.4982 | 41.15 | 0.788 | -4.246 |  |
| set2_5m_30m_1h | pullback | 1 | -0.0450 | 0.1023 | 0.00 | 0.000 | -2.199 |  |
| set3_15m_1h_4h | continuation | 67 | 0.0119 | 1.9188 | 43.28 | 1.004 | 0.059 |  |
| set3_15m_1h_4h | pullback | 0 | 0.0000 | 0.0000 | 0.00 | 0.000 | 0.000 |  |
| set4_30m_4h_1d | continuation | 18 | -0.0669 | 0.5259 | 55.56 | 0.929 | -0.345 |  |
| set4_30m_4h_1d | pullback | 1 | -0.0852 | 0.2080 | 0.00 | 0.000 | -1.642 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9977.587359069652
Total Return [%]: -0.22412640930348063
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 7.989303477423205
Max Drawdown [%]: 0.26915244829491825
Max Drawdown Duration: 0.0
Total Trades: 20
Total Closed Trades: 20
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 25.0
Best Trade [%]: 0.03441952541089717
Worst Trade [%]: -0.053402809278552135
Avg Winning Trade [%]: 0.013524227026982149
Avg Losing Trade [%]: -0.019462994979351
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.2314719172367835
Expectancy: -1.120632046517223
Sharpe Ratio: -7.137055197221927
Calmar Ratio: -10.797398250033037
Omega Ratio: 0.7172300468634831
Sortino Ratio: -9.175110294967265
```

#### RL teaching value (not hard-coded instructions)

Measured score=42.67, PF=0.438, avg return%=-0.819, trades=1163 over 8 set×mode runs. Fidelity=medium; profile=momentum. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `Simple scalper`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`momentum` rules.

### 121. `mt__US30_ExpansionTrigger_v1`

- **Title:** US30_ExpansionTrigger_v1
- **Kind:** mt
- **Source:** `strategies/language/01_METATRADER_INDEX.md :: US30_ExpansionTrigger_v1 (.mq5)`
- **Adapter profile (logic only; family not collapsed):** `momentum`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 42.6705

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -0.819440 |
| Max Drawdown [%] (avg) | 1.246760 |
| Win Rate [%] (avg) | 25.381116 |
| Profit Factor (avg) | 0.438017 |
| Sharpe (avg) | -4.456102 |
| Sortino (avg) | -6.121478 |
| Calmar (avg) | -5.143959 |
| Total Trades (sum) | 1163 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 846 | -5.1481 | 5.4517 | 38.06 | 0.551 | -20.139 |  |
| set1_1m_15m_30m | pullback | 20 | -0.2241 | 0.2692 | 25.00 | 0.231 | -7.137 |  |
| set2_5m_30m_1h | continuation | 210 | -0.9979 | 1.4982 | 41.15 | 0.788 | -4.246 |  |
| set2_5m_30m_1h | pullback | 1 | -0.0450 | 0.1023 | 0.00 | 0.000 | -2.199 |  |
| set3_15m_1h_4h | continuation | 67 | 0.0119 | 1.9188 | 43.28 | 1.004 | 0.059 |  |
| set3_15m_1h_4h | pullback | 0 | 0.0000 | 0.0000 | 0.00 | 0.000 | 0.000 |  |
| set4_30m_4h_1d | continuation | 18 | -0.0669 | 0.5259 | 55.56 | 0.929 | -0.345 |  |
| set4_30m_4h_1d | pullback | 1 | -0.0852 | 0.2080 | 0.00 | 0.000 | -1.642 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9977.587359069652
Total Return [%]: -0.22412640930348063
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 7.989303477423205
Max Drawdown [%]: 0.26915244829491825
Max Drawdown Duration: 0.0
Total Trades: 20
Total Closed Trades: 20
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 25.0
Best Trade [%]: 0.03441952541089717
Worst Trade [%]: -0.053402809278552135
Avg Winning Trade [%]: 0.013524227026982149
Avg Losing Trade [%]: -0.019462994979351
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.2314719172367835
Expectancy: -1.120632046517223
Sharpe Ratio: -7.137055197221927
Calmar Ratio: -10.797398250033037
Omega Ratio: 0.7172300468634831
Sortino Ratio: -9.175110294967265
```

#### RL teaching value (not hard-coded instructions)

Measured score=42.67, PF=0.438, avg return%=-0.819, trades=1163 over 8 set×mode runs. Fidelity=medium; profile=momentum. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `US30_ExpansionTrigger_v1`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`momentum` rules.

### 122. `note__the_truth_main_extra_strategy_S3_envelope_breakout_md`

- **Title:** strategy_S3_envelope_breakout.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\the_truth_main_extra\strategy_S3_envelope_breakout.md`
- **Adapter profile (logic only; family not collapsed):** `truth_s3_env`
- **Fidelity:** high
- **Collapses:** `[]` (empty)
- **Aggregate score:** 40.3529

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.025220 |
| Max Drawdown [%] (avg) | 1.246136 |
| Win Rate [%] (avg) | 31.995111 |
| Profit Factor (avg) | 0.416897 |
| Sharpe (avg) | -6.219049 |
| Sortino (avg) | -8.254258 |
| Calmar (avg) | -9.720200 |
| Total Trades (sum) | 730 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 259 | -1.7656 | 1.9895 | 37.07 | 0.571 | -11.030 |  |
| set1_1m_15m_30m | pullback | 189 | -1.1755 | 1.3197 | 40.21 | 0.580 | -8.780 |  |
| set2_5m_30m_1h | continuation | 128 | -1.6257 | 1.9866 | 40.62 | 0.653 | -6.468 |  |
| set2_5m_30m_1h | pullback | 90 | -1.0623 | 1.5334 | 43.33 | 0.679 | -4.907 |  |
| set3_15m_1h_4h | continuation | 35 | -1.2528 | 1.4752 | 48.57 | 0.423 | -5.168 |  |
| set3_15m_1h_4h | pullback | 26 | -1.0627 | 1.2668 | 46.15 | 0.429 | -5.639 |  |
| set4_30m_4h_1d | continuation | 2 | -0.1346 | 0.1989 | 0.00 | 0.000 | -3.672 |  |
| set4_30m_4h_1d | pullback | 1 | -0.1225 | 0.1989 | 0.00 | 0.000 | -4.089 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `pullback`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9882.449211906509
Total Return [%]: -1.1755078809349107
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 75.19919748861241
Max Drawdown [%]: 1.3197056365321087
Max Drawdown Duration: 0.0
Total Trades: 189
Total Closed Trades: 189
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 40.21164021164021
Best Trade [%]: 0.1086512875856221
Worst Trade [%]: -0.12836255096228372
Avg Winning Trade [%]: 0.021468008260699365
Avg Losing Trade [%]: -0.024894336602420665
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.5799692128307965
Expectancy: -0.6219618417645181
Sharpe Ratio: -8.780024331709184
Calmar Ratio: -10.90753453324413
Omega Ratio: 0.8662677456037038
Sortino Ratio: -12.066649539560933
```

#### RL teaching value (not hard-coded instructions)

Measured score=40.35, PF=0.417, avg return%=-1.025, trades=730 over 8 set×mode runs. Fidelity=high; profile=truth_s3_env. Truth-line geometry (CCI/BB/envelope/RSI snap) is good state/label material for L2L; do not freeze thresholds as production law.

#### 10× better

10× for `strategy_S3_envelope_breakout.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`truth_s3_env` rules.

### 123. `note__local_desktop_factory_full_GV-014-XAU-L1_md`

- **Title:** GV-014-XAU-L1.md
- **Kind:** note
- **Source:** `C:\Users\user\OneDrive\Desktop\The Creator\strategies\local_desktop\factory_full\GV-014-XAU-L1.md`
- **Adapter profile (logic only; family not collapsed):** `gv014`
- **Fidelity:** medium
- **Collapses:** `[]` (empty)
- **Aggregate score:** 33.5833

#### Vectorbt aggregate (mean across 4 sets × 2 modes)

| Metric | Value |
|--------|------:|
| Total Return [%] (avg) | -1.275651 |
| Max Drawdown [%] (avg) | 1.608656 |
| Win Rate [%] (avg) | 21.070375 |
| Profit Factor (avg) | 0.352611 |
| Sharpe (avg) | -4.942404 |
| Sortino (avg) | -6.797614 |
| Calmar (avg) | -3.170727 |
| Total Trades (sum) | 1398 |
| Runs | 8 |

#### Per set × mode

| Set | Mode | Trades | Return% | MaxDD% | Win% | PF | Sharpe | Error |
|-----|------|-------:|--------:|-------:|-----:|---:|-------:|-------|
| set1_1m_15m_30m | continuation | 1091 | -7.6528 | 7.6678 | 35.84 | 0.494 | -28.630 |  |
| set1_1m_15m_30m | pullback | 0 | 0.0000 | 0.0000 | 0.00 | 0.000 | 0.000 |  |
| set2_5m_30m_1h | continuation | 212 | -1.8734 | 2.1192 | 42.45 | 0.628 | -8.216 |  |
| set2_5m_30m_1h | pullback | 0 | 0.0000 | 0.0000 | 0.00 | 0.000 | 0.000 |  |
| set3_15m_1h_4h | continuation | 68 | -0.2646 | 1.9293 | 44.12 | 0.913 | -0.862 |  |
| set3_15m_1h_4h | pullback | 0 | 0.0000 | 0.0000 | 0.00 | 0.000 | 0.000 |  |
| set4_30m_4h_1d | continuation | 27 | -0.4144 | 1.1530 | 46.15 | 0.786 | -1.832 |  |
| set4_30m_4h_1d | pullback | 0 | 0.0000 | 0.0000 | 0.00 | 0.000 | 0.000 |  |

#### Sample full vectorbt stats (`set1_1m_15m_30m` / `continuation`)

```
Start: 0.0
End: 0.0
Period: 0.0
Start Value: 10000.0
End Value: 9234.719206585267
Total Return [%]: -7.65280793414733
Benchmark Return [%]: -0.9184088999018569
Max Gross Exposure [%]: 100.0
Total Fees Paid: 419.5689538155285
Max Drawdown [%]: 7.66781451607169
Max Drawdown Duration: 0.0
Total Trades: 1091
Total Closed Trades: 1091
Total Open Trades: 0
Open Trade PnL: 0.0
Win Rate [%]: 35.83868010999083
Best Trade [%]: 0.14293274779791396
Worst Trade [%]: -0.16644835047034917
Avg Winning Trade [%]: 0.019814288068540874
Avg Losing Trade [%]: -0.022434739235686632
Avg Winning Trade Duration: 0.0
Avg Losing Trade Duration: 0.0
Profit Factor: 0.49366842129775684
Expectancy: -0.7014489398851865
Sharpe Ratio: -28.630180156230853
Calmar Ratio: -8.461589693942921
Omega Ratio: 0.8114333480244578
Sortino Ratio: -39.201845943571215
```

#### RL teaching value (not hard-coded instructions)

Measured score=33.58, PF=0.353, avg return%=-1.276, trades=1398 over 8 set×mode runs. Fidelity=medium; profile=gv014. Use as alternate geometry features on the shared PB/cont scaffold; prefer soft teaching labels over shipping if-rules.

#### 10× better

10× for `GV-014-XAU-L1.md`: keep as **separate** teaching channel named by this source; add London/NY session weight, kill thrash (min travel), pair with risk envelope (breach0), and train the meta-policy on path state rather than freezing profile=`gv014` rules.

## Method notes

- **No collapses:** inventory forbids merging multiple MT names or notes into one family.
- Adapter *profiles* may be shared for thin language; each **family_id** still runs and ranks alone.
- HTF: completed bar only (shift+1 ffill). Exits: hold + opposite signal.
