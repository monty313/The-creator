# MetaTrader strategy language (with sources)

Language only. No code stored here. Each entry cites the original file path on this machine.

Generated: 2026-08-09

## How sources are cited

- **Source path** = absolute path to the .mq4 / .mq5 that was read.
- Terminal data: %APPDATA%\MetaQuotes\Terminal\<ID>\MQL5|MQL4\
- Install: C:\Program Files\FTMO MetaTrader 5 (no custom strategy language there).

## MT4 terminal

| Item | Finding | Source |
|------|---------|--------|
| Custom strategy EAs | None | Terminal 2C68BEE3A904BDCEE3EEF5A5A77EC162\MQL4\Experts |
| Stock samples | MACD Sample; Moving Average | same terminal MQL4\Experts\*.mq4 |
| Stock indicators | MetaQuotes default set | same terminal MQL4\Indicators |

## Entries (deduped by name)

### @@FTMO_DQN@@

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\@@FTMO_DQN@@.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: FTMO DQN Agent
- Language tags: RSI, FTMO, DQN
- Header notes (from source comments): +------------------------------------------------------------------+ | | FTMO_DQN.mq5                                                     | | | DQN-driven FTMO EA â€” communicates with Python via shared files   | | |                                                                  | | | SETUP:                                                           | | |  1. Start live_agent.py first (wait for "Ready" message)         | | |  2. Attach this EA to ANY 1m chart (e.g. EURUSD.sim M1)         | | |  3. EA trades ALL symbols in the list below                      |
- Input labels (from source): Shared folder path (must match Python); FTMO account size ($); Hard stop: max daily drawdown %; Hard stop: max daily profit %; Maximum lot size per trade; Forex: max spread in pips; Hard cap on trades per day; EA magic number; Print debug messages

### agent teacher

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\agent teacher.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: User Strategy Spec
- Language tags: RSI, BB, Bollinger, CCI, SMA, MTF, FTMO, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                    FTMO_CCI_MTF_BB_EA.mq5         | | |  Multi-timeframe CCI alignment + M1 Bollinger volatility stops   | | |  Dynamic risk-based sizing + FTMO daily/trailing DD circuit      | | |  breaker + Custom Max OnTester() scoring for 2.5%/day @ 40 days  | | +------------------------------------------------------------------+ | ================== INPUTS ==================// | ================== GLOBALS ==================//
- Input labels (from source): InpCCIPeriodFast; InpCCIPeriodSlow; InpCCISmaPeriod; InpCCISmaShift; InpM5M30Threshold; InpH4Threshold; InpBBPeriod; InpBBDeviation; InpBBBuyPrice; InpBBSellPrice

### ATI_FTMO_EA

- Source: `C:\Users\user\Downloads\_OTHER_PROJECTS\ATI_FTMO_project\ati_ftmo\mql5\ATI_FTMO_EA.mq5`
- Platform file type: .mq5
- Version tag: 0.90
- Author/copyright tag: ATI-FTMO project
- Language tags: RSI, FTMO, session
- Header notes (from source comments): +------------------------------------------------------------------+ | | ATI_FTMO_EA.mq5 â€” the hands. The brain is the Python sidecar.    | | |                                                                  | | | Architecture (spec Sections 5, 8, 11):                           | | |   - This EA never decides trades. It streams completed M1 bars   | | |     and account state to the Python sidecar over a local TCP     | | |     socket and executes the intents that come back.              | | |   - DEFENSE IN DEPTH: the hard rails live in BOTH processes.     |
- Input labels (from source): InpHost; InpPort; InpMagic; challenge initial (rails base); server(EET/EEST summer)=CEST+1 â†’ -1; InpHeartbeatSecs; InpHeartbeatTimeout

### AutoGKCloseIntegral

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\AutoGKCloseIntegral.mq5`
- Platform file type: .mq5
- Language tags: SMA
- Header notes (from source comments): --- indicator buffer | --- parameters (user inputs) | --- helper: linear interpolation of close price between times t0..t1 | --- function to be integrated: maps x in [0,1] to time in [t0,t1] and returns interpolated close | We'll use a small wrapper to carry context | The CAutoGK API drives integration by requesting values at state.m_x in the original x domain we choose. | We will map domain [0,1] -> [t0,t1] and evaluate interpolated close price at the corresponding time. | Closed bars in MQL5: indices 1..rates_total-1
- Input labels (from source): number of recent closed bars to integrate over (1 = last closed bar); if true, compute only for the newest closed bar; otherwise compute for all closed bars; if true, integrate piecewise per-bar linear segments (default); (reserved) absolute tolerance for integration (uses library defaults); (reserved) relative tolerance for integration (uses library defaults)

### AutoTradingBot_RF

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\RandomForest_Project\AutoTradingBot_RF.mq5`
- Platform file type: .mq5
- Description: Bot's job: Figure out everything else automatically
- Version tag: 1.00
- Author/copyright tag: Autonomous Trading Systems
- Language tags: RSI, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                           AutoTradingBot_RF.mq5 | | |                      Autonomous Random Forest Trading Bot       | | |                           Main Expert Advisor File              | | +------------------------------------------------------------------+ | Include our Random Forest system | +------------------------------------------------------------------+ | | INPUT PARAMETERS - Your Only Job!                               |
- Input labels (from source): Daily profit target (%); Maximum drawdown risk (%); Show real-time dashboard; Dashboard update frequency; Enable debug logging; Trading symbols

### cci_gravity_scalp_ftmo

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\cci_gravity_scalp_ftmo.mq5`
- Platform file type: .mq5
- Version tag: 6.00
- Author/copyright tag: CCI Gravity Scalp â€” FTMO build
- Language tags: RSI, CCI, SMA, EMA, scalp, momentum, FTMO, gravity, session, London, breakout, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |  cci_gravity_scalp_ftmo.mq5                                      | | |  FTMO-mode rebuild of "CCI Gravity Scalp v5"                     | | |                                                                  | | |  Strategy core (kept from v5):                                   | | |    H1 regime gate using shifted SMA envelopes + slow CCI         | | |    M1 entry using fast + slow CCI (slingshot or deep gravity)    | | |    Rolling 2-candle active-candle structure exit (no fixed TP)   |
- Input labels (from source): master FTMO switch; daily profit target as % of initial balance; trailing daily DD from today high equity, as %; % equity risked per trade (account-size independent); global cap on combined open risk across all symbols; long entry CCI floor  | start 40 step 5 stop 70; short entry CCI floor | start -70 step 5 stop -40; base stop pips        | start 4 step 1 stop 8

### cci_gravity_scalp_ftmo_v6_perplexity

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\cci_gravity_scalp_ftmo_v6_perplexity.mq5`
- Platform file type: .mq5
- Version tag: 6.00
- Author/copyright tag: CCI Gravity Scalp â€” FTMO build
- Language tags: RSI, CCI, SMA, EMA, scalp, momentum, FTMO, gravity, session, London, breakout, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |  cci_gravity_scalp_ftmo.mq5                                      | | |  FTMO-mode rebuild of "CCI Gravity Scalp v5"                     | | |                                                                  | | |  Strategy core (kept from v5):                                   | | |    H1 regime gate using shifted SMA envelopes + slow CCI         | | |    M1 entry using fast + slow CCI (slingshot or deep gravity)    | | |    Rolling 2-candle active-candle structure exit (no fixed TP)   |
- Input labels (from source): master FTMO switch; daily profit target as % of initial balance; trailing daily DD from today high equity, as %; % equity risked per trade (account-size independent); global cap on combined open risk across all symbols; long entry CCI floor  | start 40 step 5 stop 70; short entry CCI floor | start -70 step 5 stop -40; base stop pips        | start 4 step 1 stop 8

### cci_gravity_scalp_v1_full

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\cci_gravity_scalp_v1_full.mq5`
- Platform file type: .mq5
- Version tag: 5.00
- Language tags: RSI, CCI, SMA, scalp, momentum, FTMO, gravity, session, London, shift
- Header notes (from source comments): KEY: "input" = optimizer will vary this parameter | "sinput" = locked forever, optimizer ignores it | HTF CCI — locked: these define the strategy architecture, not tuned per-symbol | LTF CCI — locked: same architecture on both timeframes | === OPTIMIZABLE: CCI entry threshold === | Controls how strong momentum must be before entering | Range: 40 to 70, step 5 — tighter = fewer but cleaner trades | === OPTIMIZABLE: CCI gravity lookback ===
- Input labels (from source): optimize: 40 to 70 step 5; optimize: -70 to -40 step 5; optimize: 5 to 12 step 1; optimize: 5 to 10 step 1; optimize: 4 to 8 step 1; optimize: 3 to 8 step 1

### cci_gravity_scalp_v5_full

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\cci_gravity_scalp_v5_full.mq5`
- Platform file type: .mq5
- Version tag: 5.00
- Language tags: RSI, CCI, SMA, pullback, scalp, FTMO, gravity, session, London, shift
- Header notes (from source comments): Goal: hit +2.5%/day, stay above -1% DD | Load preset: CCI_Gravity_V5_Optimizer.set | H1 must be in a clear bull or bear trend before M1 trades. | Bull = longs only. Bear = shorts only. Neutral = no trades. | Bull: H1 close above BOTH shifted envelopes + H1 slow CCI > 0 | Bear: H1 close below BOTH shifted envelopes + H1 slow CCI < 0 | Once H1 regime is confirmed, M1 slingshot fires the entry. | Slingshot long : M1 slow CCI > 0 + M1 close above both envelopes
- Input labels (from source): Long entry CCI floor   | Start=40  Step=5  Stop=70; Short entry CCI floor  | Start=-70 Step=5  Stop=-40; CCI gravity lookback   | Start=5   Step=1  Stop=12; Stop loss pips         | Start=4   Step=1  Stop=8

### CCI_ShiftedSMA_Signal_3D

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\CCI_ShiftedSMA_Signal_3D.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2026
- Language tags: RSI, CCI, SMA, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | | CCI_ShiftedSMA_Signal_3D.mq5 | | Multi-Timeframe CCI vs Shifted SMA Indicator with 3D Labels | | Two timeframes, three CCI conditions each, score -6 to +6 | +------------------------------------------------------------------+ | Plot for colored candles | --- Indicator buffers | +------------------------------------------------------------------+
- Input labels (from source): Timeframe1; Timeframe2; CCI1_Period_TF1; SMA1_Period_TF1; SMA1_Shift_TF1; CCI2_Period_TF1; SMA2_Period_TF1; SMA2_Shift_TF1; CCI3_Period_TF1; SMA3_Period_TF1

### CoolBollingerTrendEA

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO CUSTOM EA\CoolBollingerTrendEA.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: CoolBollingerTrendEA
- Language tags: RSI, BB, Bollinger, SMA, EMA, breakout, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                         CoolBollingerTrendEA.mq5 | | |   Trend breakout on M5 with 200 SMA + 20-period Bollinger Bands  | | |   Exit on RSI(5) cross signals                                   | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Utility: read one buffer value                                    | | +------------------------------------------------------------------+
- Input labels (from source): empty = chart symbol; timeframe for signals; moving average period; Bollinger Bands period; Bollinger Bands deviation; RSI period for exit; close buy when RSI crosses below; close sell when RSI crosses above; fixed lot size; expert magic number

### coolboolinger

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\coolboolinger.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: CoolBollingerTrendEA
- Language tags: RSI, BB, Bollinger, SMA, EMA, breakout, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                         CoolBollingerTrendEA.mq5 | | |   Trend breakout on M5 with 200 SMA + 20-period Bollinger Bands  | | |   Exit on RSI(5) cross signals                                   | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Utility: read one buffer value                                    | | +------------------------------------------------------------------+
- Input labels (from source): empty = chart symbol; timeframe for signals; moving average period; Bollinger Bands period; Bollinger Bands deviation; RSI period for exit; close buy when RSI crosses below; close sell when RSI crosses above; fixed lot size; expert magic number

### crossenteopy

- Source: `C:\Users\user\OneDrive\Desktop\ARMY\00_DROP_GOALS_AND_IDEAS_HERE\_library\2024\jordan 2.0\crossenteopy.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2022, DNG
- Language tags: RSI, CCI, shift, ATR, MACD
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                 crossenteopy.mq5 | | |                                              Copyright 2022, DNG | | |                                https://www.mql5.com/ru/users/dng | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Includes                                                         | | +------------------------------------------------------------------+
- Input labels (from source): Study period, years; Depth of history; Clusters; Samples; Percentile; Period; Applied price; Period; Applied price; Period

### ErrorRatePlot

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\ErrorRatePlot.mq5`
- Platform file type: .mq5
- Language tags: SMA
- Header notes (from source comments): +------------------------------------------------------------------+ | | ErrorRatePlot.mq5                                                | | | Reads ml_error_rate.csv from Files (common) and plots line       | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Custom indicator initialization                                  | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+

### fasg_trendday_ea

- Source: `C:\Users\user\FableAutonomousStrategyGenerator\fasg\export\fasg_trendday_ea.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: FASG
- Language tags: RSI, SMA, pullback, FTMO, breakout, shift, ATR, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | | FASG Trend-Day Range Expansion EA                                 | | | The four verified specs (S1-S4) of the Fable Autonomous Strategy  | | | Generator, as one EA. Evidence of record:                         | | |   fasg_data/fasg_four_strategies.json  (commit 4b3c797)           | | |                                                                   | | | THE STRATEGY IN PLAIN ENGLISH                                     | | |  1. Only trade when gold is in an uptrend: yesterday's daily      |
- Input labels (from source): SWING overlay instead of trend-day; N-day close breakout; stop = k * ATR(14); time exit after N days; long side enabled; short side enabled; strategy spec; challenge initial balance ($); balance when THIS challenge started (0 = use initial); stop distance as fraction of range height

### fixed_FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\fixed_FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323.mq5`
- Platform file type: .mq5
- Version tag: 6.00
- Author/copyright tag: User Strategy Spec - Strategy 4 v6
- Language tags: RSI, BB, Bollinger, CCI, MTF, FTMO, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                          FTMO_BB_MTF_EA_Strategy4.mq5              | | |  STRATEGY 4 (v6): Multi-timeframe Bollinger Band trend alignment   | | |  entry, using the SAME exit/risk/scoring framework as the CCI-     | | |  based Part 3 EA.                                                  | | |                                                                    | | |  v2 CHANGE: Exit trigger band is now INDEPENDENT for buy vs sell   | | |  side (Base/Upper/Lower selectable per side).                      |
- Input labels (from source): long BB period, all timeframes; short BB period, all timeframes; deviation, all entry BBs; applied to High, per spec; 0=Middle,1=Upper,2=Lower -- "x level" for 1M BB20 BUY check, INDEPENDENT of sell; 0=Middle,1=Upper,2=Lower -- "x level" for 1M BB20 SELL check, INDEPENDENT of buy; InpExitBBPeriod; InpExitBBDeviation; InpExitBBBuyPrice; InpExitBBSellPrice

### ftmo ultra

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\ftmo ultra.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Language tags: RSI, BB, CCI, SMA, FTMO, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |  FTMO Ultra.mq5                                                  | | |  Brand-new build — all indicator params are inputs               | | +------------------------------------------------------------------+ | GENERAL SETTINGS | TP / SL — COST MULTIPLIERS | LTF MODULE 1 — BB PRICE POSITION  [TRIGGER] | BB_Level:  1 = upper band,  0 = middle band,  -1 = lower band
- Input labels (from source): _sep_gen; Lot_Size; Magic_Number; Enable_Buys; Enable_Sells; Max open positions at once; One-way broker commission (account currency); Hard spread ceiling in points; _sep_cost; TP = live cost x this value

### ftmo_all_assets_momentum_scalper

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\ftmo_all_assets_momentum_scalper.mq5`
- Platform file type: .mq5
- Description: Attach to one chart; scans Market Watch or a SymbolList.
- Version tag: 1.00
- Author/copyright tag: FTMO Strategy Lab - all assets momentum scalper
- Language tags: RSI, BB, CCI, SMA, EMA, pullback, scalp, momentum, FTMO, gravity, session, breakout, shift, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | |                    ftmo_all_assets_momentum_scalper.mq5          | | |  All-assets, single-chart, momentum-pullback scalper for MT5     | | |  with FTMO-style risk management.                                | | |                                                                  | | |  Architecture: Envelope/MA + RSI/CCI + ADX/ATR momentum window   | | |  on HTF (RegimeTF/MidTF) with M1-style entry trigger (pullback   | | |  / rejoin / breakout). Derived from the EnvelopeRSICCI +         |
- Input labels (from source): % equity at risk per trade; FTMO daily target (% of B0); intraday DD cap from day high (%); OPT_RegimeTF; OPT_MidTF; OPT_EntryTF; CCI/ADX threshold magnitude; OPT_ADX_Min; ATR vs ref multiplier; long pullback level

### FTMO_BB_MTF_EA_Strategy4

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_BB_MTF_EA_Strategy4.mq5`
- Platform file type: .mq5
- Version tag: 4.30
- Author/copyright tag: User Strategy Spec - Strategy 4 v4
- Language tags: RSI, BB, Bollinger, CCI, MTF, FTMO, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                          FTMO_BB_MTF_EA_Strategy4.mq5              | | |  STRATEGY 4 (v4): Multi-timeframe Bollinger Band trend alignment   | | |  entry, using the SAME exit/risk/scoring framework as the CCI-     | | |  based Part 3 EA.                                                  | | |                                                                    | | |  v2 CHANGE: Exit trigger band is now INDEPENDENT for buy vs sell   | | |  side. Previously a single InpExitBBTriggerBand input mirrored     |
- Input labels (from source): long BB period, all timeframes; short BB period, all timeframes; deviation, all entry BBs; applied to High, per spec; 0=Middle,1=Upper,2=Lower -- "x level" for 1M BB20 BUY check, INDEPENDENT of sell; 0=Middle,1=Upper,2=Lower -- "x level" for 1M BB20 SELL check, INDEPENDENT of buy; InpExitBBPeriod; InpExitBBDeviation; InpExitBBBuyPrice; InpExitBBSellPrice

### FTMO_BB_MTF_EA_Strategy4_20260705_1210

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_BB_MTF_EA_Strategy4_20260705_1210.mq5`
- Platform file type: .mq5
- Version tag: 4.00
- Author/copyright tag: User Strategy Spec - Strategy 4
- Language tags: RSI, BB, Bollinger, CCI, MTF, FTMO, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                          FTMO_BB_MTF_EA_Strategy4.mq5              | | |  NEW STRATEGY (Strategy 4): Multi-timeframe Bollinger Band trend   | | |  alignment entry, using the SAME exit/risk/scoring framework as    | | |  the CCI-based Part 3 EA.                                          | | |                                                                    | | |  TIMEFRAMES USED: 4H, 30M, 5M (trend alignment), 1M (entry trigger)| | |                                                                    |
- Input labels (from source): long BB period, all timeframes; short BB period, all timeframes; deviation, all entry BBs; applied to High, per spec; 0=Middle,1=Upper,2=Lower -- the "x level" used ONLY on the 1M BB20 check; InpExitBBPeriod; InpExitBBDeviation; InpExitBBBuyPrice; InpExitBBSellPrice; 0=Base,1=Upper,2=Lower

### FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_BB_MTF_EA_Strategy4_v2_20260705_1323.mq5`
- Platform file type: .mq5
- Version tag: 4.10
- Author/copyright tag: User Strategy Spec - Strategy 4 v2
- Language tags: RSI, BB, Bollinger, CCI, MTF, FTMO, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                          FTMO_BB_MTF_EA_Strategy4.mq5              | | |  STRATEGY 4 (v2): Multi-timeframe Bollinger Band trend alignment   | | |  entry, using the SAME exit/risk/scoring framework as the CCI-     | | |  based Part 3 EA.                                                  | | |                                                                    | | |  v2 CHANGE: Exit trigger band is now INDEPENDENT for buy vs sell   | | |  side. Previously a single InpExitBBTriggerBand input mirrored     |
- Input labels (from source): long BB period, all timeframes; short BB period, all timeframes; deviation, all entry BBs; applied to High, per spec; 0=Middle,1=Upper,2=Lower -- the "x level" used ONLY on the 1M BB20 check; InpExitBBPeriod; InpExitBBDeviation; InpExitBBBuyPrice; InpExitBBSellPrice; 0=Base,1=Upper,2=Lower -- BUY side SL band, INDEPENDENT of sell

### FTMO_BB_MTF_EA_Strategy4_v5

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_BB_MTF_EA_Strategy4_v5.mq5`
- Platform file type: .mq5
- Version tag: 5.00
- Author/copyright tag: User Strategy Spec - Strategy 4 v5
- Language tags: RSI, BB, Bollinger, CCI, MTF, FTMO, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                          FTMO_BB_MTF_EA_Strategy4.mq5              | | |  STRATEGY 4 (v5): Multi-timeframe Bollinger Band trend alignment   | | |  entry, using the SAME exit/risk/scoring framework as the CCI-     | | |  based Part 3 EA.                                                  | | |                                                                    | | |  v2 CHANGE: Exit trigger band is now INDEPENDENT for buy vs sell   | | |  side (Base/Upper/Lower selectable per side).                      |
- Input labels (from source): long BB period, all timeframes; short BB period, all timeframes; deviation, all entry BBs; applied to High, per spec; 0=Middle,1=Upper,2=Lower -- "x level" for 1M BB20 BUY check, INDEPENDENT of sell; 0=Middle,1=Upper,2=Lower -- "x level" for 1M BB20 SELL check, INDEPENDENT of buy; InpExitBBPeriod; InpExitBBDeviation; InpExitBBBuyPrice; InpExitBBSellPrice

### FTMO_BB_MTF_EA_Strategy4_v6

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_BB_MTF_EA_Strategy4_v6.mq5`
- Platform file type: .mq5
- Version tag: 6.00
- Author/copyright tag: User Strategy Spec - Strategy 4 v6
- Language tags: RSI, BB, Bollinger, CCI, MTF, FTMO, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                          FTMO_BB_MTF_EA_Strategy4.mq5              | | |  STRATEGY 4 (v6): Multi-timeframe Bollinger Band trend alignment   | | |  entry, using the SAME exit/risk/scoring framework as the CCI-     | | |  based Part 3 EA.                                                  | | |                                                                    | | |  v2 CHANGE: Exit trigger band is now INDEPENDENT for buy vs sell   | | |  side (Base/Upper/Lower selectable per side).                      |
- Input labels (from source): long BB period, all timeframes; short BB period, all timeframes; deviation, all entry BBs; applied to High, per spec; 0=Middle,1=Upper,2=Lower -- "x level" for 1M BB20 BUY check, INDEPENDENT of sell; 0=Middle,1=Upper,2=Lower -- "x level" for 1M BB20 SELL check, INDEPENDENT of buy; InpExitBBPeriod; InpExitBBDeviation; InpExitBBBuyPrice; InpExitBBSellPrice

### FTMO_BB_MTF_EA_Strategy4_v7

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_BB_MTF_EA_Strategy4_v7.mq5`
- Platform file type: .mq5
- Version tag: 7.00
- Author/copyright tag: User Strategy Spec - Strategy 4 v7
- Language tags: RSI, BB, Bollinger, CCI, MTF, FTMO, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                          FTMO_BB_MTF_EA_Strategy4.mq5              | | |  STRATEGY 4 (v7): Multi-timeframe Bollinger Band trend alignment   | | |  entry, using the SAME exit/risk/scoring framework as the CCI-     | | |  based Part 3 EA.                                                  | | |                                                                    | | |  v2 CHANGE: Exit trigger band is now INDEPENDENT for buy vs sell   | | |  side (Base/Upper/Lower selectable per side).                      |
- Input labels (from source): long BB period, all timeframes; short BB period, all timeframes; deviation, all entry BBs; applied to High, per spec; 0=Middle,1=Upper,2=Lower -- "x level" for 1M BB20 BUY check, INDEPENDENT of sell; 0=Middle,1=Upper,2=Lower -- "x level" for 1M BB20 SELL check, INDEPENDENT of buy; InpExitBBPeriod; InpExitBBDeviation; InpExitBBBuyPrice; InpExitBBSellPrice

### FTMO_CCI_MTF_BB_EA_Part2

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_CCI_MTF_BB_EA_Part2.mq5`
- Platform file type: .mq5
- Version tag: 2.00
- Author/copyright tag: User Strategy Spec - Part 2
- Language tags: RSI, BB, Bollinger, CCI, SMA, MTF, FTMO, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                          FTMO_CCI_MTF_BB_EA_Part2.mq5             | | |  PART 2: Same strategy as Part 1, with two hardcoded changes:     | | |                                                                    | | |  1) HARD-CODED GLOBAL RULE: if trailing daily DD reaches 4% on     | | |     any given day, the EA stops taking new trades for the REST    | | |     of that day and only resumes at the next daily rollover.      | | |     This is NOT an input -- it is a fixed constant so it cannot   |
- Input labels (from source): InpCCIPeriodFast; InpCCIPeriodSlow; InpCCISmaPeriod; InpCCISmaShift; InpM5M30Threshold; InpH4Threshold; InpBBPeriod; InpBBDeviation; InpBBBuyPrice; InpBBSellPrice

### FTMO_CCI_MTF_BB_EA_PART3

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_CCI_MTF_BB_EA_PART3.mq5`
- Platform file type: .mq5
- Version tag: 3.00
- Author/copyright tag: User Strategy Spec - Part 3
- Language tags: RSI, BB, Bollinger, CCI, SMA, EMA, MTF, FTMO, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                          FTMO_CCI_MTF_BB_EA_Part3.mq5             | | |  PART 3: Builds on Part 2 with two updates:                       | | |                                                                    | | |  1) TRUE TRAILING DAILY DRAWDOWN (equity-peak based):              | | |     The daily DD is now measured from the HIGHEST intraday        | | |     equity reached during the day (a trailing peak), not just     | | |     the fixed balance the day opened with. This matches how       |
- Input labels (from source): InpCCIPeriodFast; InpCCIPeriodSlow; InpCCISmaPeriod; InpCCISmaShift; InpM5M30Threshold; InpH4Threshold; InpBBPeriod; InpBBDeviation; InpBBBuyPrice; InpBBSellPrice

### FTMO_Challenge_EA

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_Challenge_EA.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Language tags: RSI, BB, CCI, SMA, FTMO, shift, ATR
- Input labels (from source): Inp_FTMO_Mode; Inp_Initial_Balance; Inp_Daily_Loss_Limit_Pct; Inp_Max_Loss_Limit_Pct; Inp_Daily_Target_Pct; Inp_Daily_Catchup_Max_Pct; Inp_Trade_Risk_Pct; Inp_Max_Open_Trades; Inp_Max_Open_Risk_Pct; Inp_Use_FTMO_Time

### FTMO_Challenge_EA_FULL

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_Challenge_EA_FULL.mq5`
- Platform file type: .mq5
- Description: FTMO EA one-file build incorporating steps 1-17
- Version tag: 2.00
- Language tags: RSI, BB, CCI, SMA, EMA, FTMO, shift, ATR
- Input labels (from source): Inp_FTMO_Mode; Inp_Initial_Balance; Inp_Daily_Loss_Limit_Pct; Inp_Max_Loss_Limit_Pct; Inp_Daily_Target_Pct; Inp_Daily_Catchup_Max_Pct; Inp_Trade_Risk_Pct; Inp_Max_Open_Trades; Inp_Max_Open_Risk_Pct; Inp_Use_FTMO_Time

### ftmo_challenge_ea_v3

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\ftmo_challenge_ea_v3.mq5`
- Platform file type: .mq5
- Description: FTMO Challenge EA v3 - Steps 1-17 Cycle2 Fix
- Version tag: 3.15
- Language tags: RSI, BB, CCI, SMA, momentum, FTMO, session, breakout, ATR, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |  FTMO Challenge EA v3                                            | | |  Steps 1-17. Step-17 is master authority.                        | | |  Two layers: Live FTMO control (Steps 1-8) vs                    | | |              Optimizer scoring (Steps 9-17, OnTester only)       | | +------------------------------------------------------------------+ | Week tracking for Best Day Rule | Minimum trading days tracking
- Input labels (from source): _sep_gen; Inp_FTMO_Mode; Inp_Initial_Balance; Inp_Magic; Inp_Slippage; Inp_Symbol_Group; Inp_Symbol_Suffix; Inp_Symbol_Prefix; _sep_ftmo; Daily hard loss stop (%) - buffer before FTMO 2% limit

### FTMO_Challenge_v4

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_Challenge_v4.mq5`
- Platform file type: .mq5
- Version tag: 4.02
- Language tags: RSI, BB, Bollinger, CCI, SMA, FTMO, shift, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | | FTMO-Challenge-EA-v4                                            | | | RSI entry + multi-timeframe SMA bias + FTMO daily pass scoring  | | | Multi-symbol engine: one EA instance trades all Market Watch    | | | assets with one shared FTMO state machine per MagicNumber.      | | +------------------------------------------------------------------+ | Entry: RSI + timeframe | Multi-timeframe bias: 3 timeframes, same SMA settings
- Input labels (from source): FTMOModeOn; EntryTimeframe; RSIPeriod; BuyRSILevel; SellRSILevel; UseBias1; BiasTimeframe1; UseBias2; BiasTimeframe2; UseBias3

### FTMO_DQN

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO_DQN.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: FTMO DQN Agent
- Language tags: RSI, BB, FTMO, DQN
- Header notes (from source comments): +------------------------------------------------------------------+ | | FTMO_DQN.mq5                                                     | | | DQN-driven FTMO EA â€” communicates with Python via shared files   | | |                                                                  | | | SETUP:                                                           | | |  1. Start live_agent.py first (wait for "Ready" message)         | | |  2. Attach this EA to ANY 1m chart (e.g. EURUSD.sim M1)         | | |  3. EA trades ALL symbols in the list below                      |
- Input labels (from source): DEPRECATED (kept for reference only); FTMO account size ($); Hard stop: max daily drawdown %; Hard stop: max daily profit %; Maximum lot size per trade; Forex: max spread in pips; Hard cap on trades per day; EA magic number; Print debug messages

### FTMO_SMA_Scalper

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\FTMO CUSTOM EA\FTMO_SMA_Scalper.mq5`
- Platform file type: .mq5
- Description: SMA cascade entry + RSI exit + BB trailing stop with FTMO rules
- Version tag: 1.00
- Author/copyright tag: FTMO SMA Scalper EA v1.0
- Language tags: RSI, BB, Bollinger, SMA, scalp, FTMO, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                           FTMO_SMA_Scalper.mq5    | | |                  FTMO SMA Scalper EA â€” SMA Cascade + RSI Exit    | | |              FTMO-Compliant Risk Management | v1.0               | | +------------------------------------------------------------------+ | OPTIMIZER NOTE: Attach to M1 chart. Use Inp_Symbols for multi-symbol. | Targets FTMO 1-Step: 10% profit over 4 days, 2.5%/day, with smooth equity. | +------------------------------------------------------------------+
- Input labels (from source): empty = use chart symbol (recommended for optimizer); Inp_MagicNumber; must match tester deposit; optimizer: 0 or 1; 0=M1, 1=M5 (only used when TFSet=1); offset on LowerTF  (optimizer: 0â€“4); offset on HigherTF (optimizer: 0â€“4); optimizer: 5â€“30; optimizer: 10â€“45 step 5; optimizer: 10â€“40

### FtmoDecisionTree

- Source: `C:\Users\user\OneDrive\Desktop\ARMY\01_SYSTEM\labs\decision_tree\ftmo_dt_bot\ftmo_dt_bot\ea\FtmoDecisionTree.mq5`
- Platform file type: .mq5
- Language tags: RSI, BB, CCI, SMA, FTMO, session, shift, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | |  FtmoDecisionTree.mq5                                            | | |  AUTO-GENERATED frozen decision tree + FTMO risk manager.        | | |  One tree, identical to the Python backtest & RL alpha.          | | |  Attach to ONE chart per symbol (M1). Tree is symbol-agnostic.   | | +------------------------------------------------------------------+ | ------------------------------------------------------------------ helpers | ------------------------------------------------------------------ the frozen tree
- Input labels (from source): % equity risked / trade (0.01 = 0.01%); InpMaxTradesPerDay; InpMaxDailyLossPct; InpMaxTotalLossPct; InpDailyStopPct; InpDailyLockPct; InpTotalStopPct; InpAtrPeriod; InpSlAtrMult; InpTpAtrMult

### HurstX

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\HurstX.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2025, Hurst Exponent Screener
- Language tags: RSI, EMA, momentum
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                       HurstX.mq5 | | |                        Copyright 2025, Hurst Exponent Screener   | | |                                                 https://mql5.com | | | 16.09.2025 - Multi-Timeframe Hurst Exponent Screener            | | +------------------------------------------------------------------+ | --- Input parameters | --- Data structures
- Input labels (from source): Analysis timeframe; Lookback period for Hurst calculation; Mask range minimum (0.40); Mask range maximum (0.60); Moving Average period for slope; Enable alert notifications; Update interval in seconds; Base font size for display; Minimum font size (adaptive sizing); Trending signal color (brighter)

### JordanMomentumScreener_v10

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\JordanMomentumScreener_v10.mq5`
- Platform file type: .mq5
- Description: Jordan Momentum Screener v10 â€” strategy matrix (CCI / SMA / BB x TREND / MOMO / PULL) + The Wave (BB-on-CCI, 5 TF sets, Pullback=GOLD), BBs shifted +2, click-safe charts, self-healing HUD, persistent track record
- Version tag: 10.00
- Author/copyright tag: Jordan
- Language tags: RSI, BB, Bollinger, CCI, SMA, EMA, MTF, pullback, momentum, gravity, shift, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | |              JordanMomentumScreener_v10.mq5                  | | |                                                                  | | |  V10 â€” STRATEGY MATRIX + THE WAVE + ALWAYS-ON HUD | |                                                                  | | |  V10 CHANGES                                                     | | |  - ALL Bollinger Bands plot-shifted +2 (InpBBshift): the price   | | |    BBs of the Bollinger strategy / BB-gravity AND the Wave's     |
- Input labels (from source): InpUseMarketWatch; InpSymbolsCSV; up to 50; InpRefreshSeconds; InpRowsVisible; BB gravity ticks column; ATR/price volatility scale; LOWER = more "tradeable"; tradeability below this reads DEAD; Higher timeframe; Middle timeframe

### JordanMomentumScreener_v11

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\JordanMomentumScreener_v11.mq5`
- Platform file type: .mq5
- Description: Jordan Momentum Screener v11 â€” SMA Channel pullbacks (GOLD), strategy matrix (CCI / SMA / BB x TREND / MOMO / PULL) + The Wave (BB-on-CCI, 5 TF sets, Pullback=GOLD), BBs shifted +2, click-safe charts, self-healing HUD, persistent track record
- Version tag: 11.00
- Author/copyright tag: Jordan
- Language tags: RSI, BB, Bollinger, CCI, SMA, EMA, MTF, pullback, momentum, gravity, shift, ATR, channel
- Header notes (from source comments): +------------------------------------------------------------------+ | |              JordanMomentumScreener_v11.mq5                  | | |                                                                  | | |  V11 â€” STRATEGY MATRIX + THE WAVE + SMA CHANNEL + HUD | |                                                                  | | |  V11 NEW â€” SHIFTED SMA CHANNEL (independent 5th engine)          | | |  Price channel of SMA(4) on High + SMA(4) on Low:                | | |   2 higher TFs (macro): both SMAs shifted +8.                    |
- Input labels (from source): InpUseMarketWatch; InpSymbolsCSV; up to 50; InpRefreshSeconds; InpRowsVisible; BB gravity ticks column; ATR/price volatility scale; LOWER = more "tradeable"; tradeability below this reads DEAD; Higher timeframe; Middle timeframe

### JordanMomentumScreener_v2_MT5

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\JordanMomentumScreener_v2_MT5.mq5`
- Platform file type: .mq5
- Description: Jordan Momentum Screener â€” MT5 (handle-based), alerts, signal age, rolling hit-rate
- Version tag: 2.02
- Language tags: RSI, BB, CCI, EMA, momentum, gravity, shift, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | |              JordanMomentumScreener_v2_MT5.mq5                    | | |   Multi-timeframe momentum signals screener â€” proper MQL5 (MT5). | | |                                                                  | | |   v2.00 changes vs the v1.10 prototype:                          | | |     * Proper MT5 indicator access: iMA/iATR/iCCI now return      | | |       HANDLES, read with CopyBuffer (handles created once and    | | |       cached per symbol/timeframe/params, released on deinit).   |
- Input labels (from source): InpUseMarketWatch; InpSymbolsCSV; up to 50; InpRefreshSeconds; InpRowsVisible; InpUseBBGravity; composite score needed for BUY/SELL (lower = more signals); ATR/price volatility scale; LOWER = more "tradeable" (try 6-8 on FX majors); tradeability below this reads DEAD; timeframes that must agree: 3 = strict, 2 = relaxed (more signals)

### JordanMomentumScreener_v4_MT5

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\JordanMomentumScreener_v4_MT5.mq5`
- Platform file type: .mq5
- Description: Jordan Momentum Screener â€” MT5 v4: 3 strategies (CCI Â· BB Â· SMA channel) + GOLD confluence, alerts, age, hit-rate
- Version tag: 4.00
- Language tags: RSI, BB, CCI, SMA, EMA, MTF, momentum, gravity, breakout, shift, ATR, channel
- Header notes (from source comments): +------------------------------------------------------------------+ | |              JordanMomentumScreener_v2_MT5.mq5                    | | |   Multi-timeframe momentum signals screener â€” proper MQL5 (MT5). | | |                                                                  | | |   v2.00 changes vs the v1.10 prototype:                          | | |     * Proper MT5 indicator access: iMA/iATR/iCCI now return      | | |       HANDLES, read with CopyBuffer (handles created once and    | | |       cached per symbol/timeframe/params, released on deinit).   |
- Input labels (from source): InpUseMarketWatch; InpSymbolsCSV; up to 50; InpRefreshSeconds; InpRowsVisible; InpUseBBGravity; composite score needed for BUY/SELL (lower = more signals); ATR/price volatility scale; LOWER = more "tradeable" (try 6-8 on FX majors); tradeability below this reads DEAD; timeframes that must agree: 3 = strict, 2 = relaxed (more signals)

### JordanMomentumScreener_v5_MT5

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\JordanMomentumScreener_v5_MT5.mq5`
- Platform file type: .mq5
- Description: Jordan Momentum Screener â€” MT5 v4: 3 strategies (CCI Â· BB Â· SMA channel) + GOLD confluence, alerts, age, hit-rate
- Version tag: 4.00
- Language tags: RSI, BB, CCI, SMA, EMA, MTF, momentum, gravity, breakout, shift, ATR, channel
- Header notes (from source comments): +------------------------------------------------------------------+ | |              JordanMomentumScreener_v2_MT5.mq5                    | | |   Multi-timeframe momentum signals screener â€” proper MQL5 (MT5). | | |                                                                  | | |   v2.00 changes vs the v1.10 prototype:                          | | |     * Proper MT5 indicator access: iMA/iATR/iCCI now return      | | |       HANDLES, read with CopyBuffer (handles created once and    | | |       cached per symbol/timeframe/params, released on deinit).   |
- Input labels (from source): InpUseMarketWatch; InpSymbolsCSV; up to 50; InpRefreshSeconds; InpRowsVisible; InpUseBBGravity; composite score needed for BUY/SELL (lower = more signals); ATR/price volatility scale; LOWER = more "tradeable" (try 6-8 on FX majors); tradeability below this reads DEAD; timeframes that must agree: 3 = strict, 2 = relaxed (more signals)

### JordanMomentumScreener_v7_HUD

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\JordanMomentumScreener_v7_HUD.mq5`
- Platform file type: .mq5
- Description: Jordan Momentum Screener v7 TACTICAL HUD â€” v4 engine (CCI Â· BB Â· SMA channel + GOLD) with radar, arc gauge, boot sequence, ticker, corr guard, signal log
- Version tag: 7.00
- Language tags: RSI, BB, CCI, SMA, EMA, MTF, momentum, gravity, shift, ATR, channel
- Header notes (from source comments): +------------------------------------------------------------------+ | |              JordanMomentumScreener_v7_HUD.mq5                    | | |   Multi-timeframe momentum signals screener â€” "TACTICAL HUD".    | | |   v7 = v4 engine (unchanged math) + JARVIS-style HUD chrome.     | | |                                                                  | | |  ============================================================    | | |  HOW TO INSTALL                                                  | | |  ============================================================    |
- Input labels (from source): InpUseMarketWatch; InpSymbolsCSV; up to 50; InpRefreshSeconds; InpRowsVisible; InpUseBBGravity; composite score needed for BUY/SELL; ATR/price volatility scale; LOWER = more "tradeable"; tradeability below this reads DEAD; timeframes that must agree

### JordanMomentumScreener_v8_HUD

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\JordanMomentumScreener_v8_HUD.mq5`
- Platform file type: .mq5
- Description: Jordan Momentum Screener v8 TACTICAL HUD â€” strategy matrix (CCI / SMA / BB x TREND / MOMO / PULL), MOMO=GOLD, self-healing always-on radar, flicker-free GUI, persistent track record
- Version tag: 8.00
- Author/copyright tag: Jordan
- Language tags: RSI, BB, Bollinger, CCI, SMA, EMA, MTF, pullback, momentum, gravity, shift, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | |              JordanMomentumScreener_v8_HUD.mq5                   | | |                                                                  | | |  V8 â€” STRATEGY MATRIX + ALWAYS-ON HUD                            | | |                                                                  | | |  HOW TO INSTALL                                                  | | |  1. MetaEditor: File > Open Data Folder > MQL5\Indicators        | | |  2. Copy this file there, open in MetaEditor, press F7.          |
- Input labels (from source): InpUseMarketWatch; InpSymbolsCSV; up to 50; InpRefreshSeconds; InpRowsVisible; BB gravity ticks column; ATR/price volatility scale; LOWER = more "tradeable"; tradeability below this reads DEAD; Higher timeframe; Middle timeframe

### JordanMomentumScreener_v9_HUD

- Source: `C:\Users\user\Downloads\_CODE\JordanMomentumScreener_v9_HUD.mq5`
- Platform file type: .mq5
- Description: Jordan Momentum Screener v9 TACTICAL HUD â€” strategy matrix (CCI / SMA / BB x TREND / MOMO / PULL), MOMO=GOLD, PB pullback radar column + symbol glow, self-healing always-on radar, flicker-free GUI, persistent track record
- Version tag: 9.00
- Author/copyright tag: Jordan
- Language tags: RSI, BB, Bollinger, CCI, SMA, EMA, MTF, pullback, momentum, gravity, shift, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | |              JordanMomentumScreener_v9_HUD.mq5                   | | |                                                                  | | |  V9 â€” STRATEGY MATRIX + PULLBACK RADAR + ALWAYS-ON HUD           | | |                                                                  | | |  HOW TO INSTALL                                                  | | |  1. MetaEditor: File > Open Data Folder > MQL5\Indicators        | | |  2. Copy this file there, open in MetaEditor, press F7.          |
- Input labels (from source): InpUseMarketWatch; InpSymbolsCSV; up to 50; InpRefreshSeconds; InpRowsVisible; BB gravity ticks column; ATR/price volatility scale; LOWER = more "tradeable"; tradeability below this reads DEAD; Higher timeframe; Middle timeframe

### JordanMomentumScreener_v9_Wave

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\JordanMomentumScreener_v9_Wave.mq5`
- Platform file type: .mq5
- Description: Jordan Momentum Screener v9 WAVE â€” strategy matrix (CCI / SMA / BB x TREND / MOMO / PULL) + The Wave (BB-on-CCI, 5 TF sets, Pullback=GOLD), self-healing HUD, persistent track record
- Version tag: 9.00
- Author/copyright tag: Jordan
- Language tags: RSI, BB, Bollinger, CCI, SMA, EMA, MTF, pullback, momentum, gravity, shift, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | |              JordanMomentumScreener_v9_Wave.mq5                  | | |                                                                  | | |  V9 â€” STRATEGY MATRIX + THE WAVE + ALWAYS-ON HUD                 | | |                                                                  | | |  HOW TO INSTALL                                                  | | |  1. MetaEditor: File > Open Data Folder > MQL5\Indicators        | | |  2. Copy this file there, open in MetaEditor, press F7.          |
- Input labels (from source): InpUseMarketWatch; InpSymbolsCSV; up to 50; InpRefreshSeconds; InpRowsVisible; BB gravity ticks column; ATR/price volatility scale; LOWER = more "tradeable"; tradeability below this reads DEAD; Higher timeframe; Middle timeframe

### KineticEdgeEA

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\KineticEdgeEA.mq5`
- Platform file type: .mq5
- Description: BB breakout + Triple CCI momentum scalping with FTMO rules
- Version tag: 1.00
- Author/copyright tag: KineticEdge EA v1.0
- Language tags: RSI, BB, Bollinger, CCI, scalp, momentum, FTMO, session, breakout, shift, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                            KineticEdgeEA.mq5     | | |          Impulse Momentum Scalping — BB Breakout + Triple CCI    | | |              FTMO-Compliant Risk Management | v1.0               | | +------------------------------------------------------------------+ | OPTIMIZER NOTE: Attach to M1 chart of the symbol you want to test. | Leave Inp_Symbols blank to use the chart symbol (recommended for optimizer). | For live multi-symbol, list symbols comma-separated in Inp_Symbols.
- Input labels (from source): Symbols: blank=chart symbol, or "EURUSD,GBPUSD"; Risk per trade (% of equity); Max total open risk (% equity); Max simultaneous positions; EA magic number; Bollinger Band 1 period; Bollinger Band 2 period; Bollinger Band deviation; CCI momentum fast period; CCI momentum mid period

### kmeans

- Source: `C:\Users\user\OneDrive\Desktop\ARMY\00_DROP_GOALS_AND_IDEAS_HERE\_library\2024\jordan 2.0\kmeans.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2021, DNG
- Language tags: RSI, CCI, shift, ATR, MACD
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                       kmeans.mq5 | | |                                              Copyright 2021, DNG | | |                                https://www.mql5.com/ru/users/dng | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Includes                                                         | | +------------------------------------------------------------------+
- Input labels (from source): Study period, years; Depth of history; Period; Applied price; Period; Applied price; Period; Fast; Slow; Signal

### Linear_Regression_Screener

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\screeners\Linear_Regression_Screener.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2025, Linear Regression Trader
- Language tags: RSI, CCI, SMA, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                    Linear_Regression_Screener.mq5| | |                        Copyright 2025, Linear Regression Trader  | | +------------------------------------------------------------------+ | Indicator handles for all symbols | +------------------------------------------------------------------+ | | Custom indicator initialization function                         | | +------------------------------------------------------------------+
- Input labels (from source): LR1 Period; LR1 Shift; LR2 Period; LR2 Shift; SMA Period; SMA Shift; CCI Period; Lower Timeframe; Upper Timeframe; Broker suffix to append (e.g., ".sim" or "_otc")

### LinearRegressionLine

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\LinearRegressionLine.mq5`
- Platform file type: .mq5
- Version tag: 1.01
- Author/copyright tag: Linear Regression Trader
- Language tags: RSI, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                   LinearRegressionLine.mq5       | | |                        Copyright 2025, Linear Regression Trader  | | +------------------------------------------------------------------+ | --- input parameters | --- indicator buffers | --- initialization function | --- calculation function
- Input labels (from source): Number of bars for regression calculation; Shift for regression line

### LinearRegressionRSI_EA

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\LinearRegressionRSI_EA.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Linear Regression RSI Trader
- Language tags: RSI, SMA, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                         LinearRegressionRSI_EA.mq5 | | |                        Copyright 2025, Linear Regression RSI Trader | | |                                             https://www.mql5.com | | +------------------------------------------------------------------+ | --- Input parameters | --- Timeframes | --- LinearRegressionLine parameters for Lower Timeframe
- Input labels (from source): Lower Timeframe; Higher Timeframe; LRL1 Period (Lower TF); LRL1 Shift (Lower TF); LRL2 Period (Lower TF); LRL2 Shift (Lower TF); LRL3 Period (Lower TF); LRL3 Shift (Lower TF); LRL1 Period (Higher TF); LRL1 Shift (Higher TF)

### MA ribbon filled_Alerts

- Source: `C:\Users\user\OneDrive\Desktop\ARMY\00_DROP_GOALS_AND_IDEAS_HERE\_library\09_trading_templates_ex4\MA ribbon filled_Alerts.mq4`
- Platform file type: .mq4
- Author/copyright tag: mladen
- Language tags: BB, SMA, EMA, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                    MA ribbon.mq4 | | |                                               mladenfx@gmail.com | | |                                                                  | | | original idea by Jose Silva                                      | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | |                                                                  |

### MACD Sample

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\2C68BEE3A904BDCEE3EEF5A5A77EC162\MQL4\Experts\MACD Sample.mq4`
- Platform file type: .mq4
- Author/copyright tag: 2000-2026, MetaQuotes Ltd.
- Language tags: EMA, ATR, MACD, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                  MACD Sample.mq4 | | |                             Copyright 2000-2026, MetaQuotes Ltd. | | |                                              http://www.mql5.com | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | |                                                                  | | +------------------------------------------------------------------+
- Input labels (from source): TakeProfit; Lots; TrailingStop; MACDOpenLevel; MACDCloseLevel; MATrendPeriod

### MetaLearningEA

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\The _Meta-Learning_ EA\MetaLearningEA.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Meta-Learning Trading Bot
- Language tags: RSI, FTMO, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                          MetaLearningEA.mq5      | | |                     Copyright 2025, Meta-Learning Trading Bot    | | |                                   Progressive AI Trading System  | | +------------------------------------------------------------------+ | --- Include core files | +------------------------------------------------------------------+ | | USER INPUTS - Only Two Required Parameters                       |
- Input labels (from source): Daily profit goal (starts at 10%, then progressive); Maximum trailing drawdown from peak; Enable training mode (overrides trading); Bars to look ahead for correct action (increased for better prediction); Minimum movement to learn from (pips) - lower to capture more patterns; Process every N bars during training (more frequent learning); Enable -3% auto-close; Max losses before retraining prompt; Maximum daily trades; Magic number for position identification

### Momentum

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\Momentum.mq5`
- Platform file type: .mq5
- Language tags: RSI, BB, Bollinger, CCI, SMA, MTF, momentum, FTMO, breakout, shift, ATR, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                        FTMO MTF Momentum EA     | | |   Rule-based multi-symbol momentum with FTMO 1-Step controls    | | |   Optimization-ready: every meaningful parameter is an input    | | +------------------------------------------------------------------+ | SHADOW GLOBALS  (ApplyRiskProfile writes; preset can override) | SECTION 0 â€” FTMO CONTROL | SECTION 1 â€” RISK MANAGEMENT
- Input labels (from source): â•â•â•â•â•â•â•â• 0. FTMO Control â•â•â•â•â•â•â•â•; ON = enforce FTMO profit/loss rules; OFF = trade freely with no FTMO shutdowns; Starting balance of the FTMO challenge account; Scale all dollar limits for larger accounts (1.0 = no scaling); Stop new trades when daily profit reaches this % of challenge balance; EA daily loss stop in % of challenge balance (FTMO hard limit = 3%); EA total loss stop in % of challenge balance (FTMO hard limit = 10%); Hours to add to broker time to reach UTC+2 (CEST). E.g. broker=UTC+3 â†’ set -1; ON = recalculate daily floor at 00:00 CEST; OFF = use server-time midnight; Close all positions at FTMO midnight before the new day starts

### Momentum_Matrix_Screener

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\screeners\Momentum_Matrix_Screener.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Momentum Matrix Trader
- Language tags: RSI, CCI, SMA, momentum, shift, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                         Momentum_Matrix_Screener.mq5 | | |                        Copyright 2025, Momentum Matrix Trader     | | |                                             https://www.mql5.com | | +------------------------------------------------------------------+ | --- Input parameters | --- Signal types | --- Structure for signal data
- Input labels (from source): CCI Period; SMA Period for CCI smoothing; SMA Shift (0 = current bar); Timeframe to analyze; Starting X position; Starting Y position; Panel background color; Panel border color; Buy signal color; Sell signal color

### Moving Average

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\2C68BEE3A904BDCEE3EEF5A5A77EC162\MQL4\Experts\Moving Average.mq4`
- Platform file type: .mq4
- Description: Moving Average sample expert advisor
- Author/copyright tag: 2000-2026, MetaQuotes Ltd.
- Language tags: SMA, EMA, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                               Moving Average.mq4 | | |                             Copyright 2000-2026, MetaQuotes Ltd. | | |                                              http://www.mql5.com | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Calculate open positions                                         | | +------------------------------------------------------------------+
- Input labels (from source): Lots; MaximumRisk; DecreaseFactor; MovingPeriod; MovingShift

### MQL5 RL EA

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\MQL5 RL EA.mq5`
- Platform file type: .mq5
- Version tag: 1.001
- Language tags: RSI, CCI, SMA, FTMO
- Input labels (from source): FTMO_Mode; Daily_Profit_Target_Pct; Daily_Risk_Target_Pct; Max_Trades_Per_Day; Alpha; Gamma; Epsilon; Max_Symbols; SaveFileName

### MultiTimeframe_LRL_BB_CCI_Screener

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\screeners\MultiTimeframe_LRL_BB_CCI_Screener.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2025, MetaQuotes Software Corp.
- Language tags: RSI, BB, Bollinger, CCI, SMA, MTF, pullback, momentum, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                       MultiTimeframe_LRL_BB_CCI_Screener.mq5    | | |                        Copyright 2025, MetaQuotes Software Corp. | | +------------------------------------------------------------------+ | === PULLBACK STRATEGY SETTINGS === | === MOMENTUM STRATEGY SETTINGS === | === PURE MOMENTUM STRATEGY SETTINGS === | === DISPLAY SETTINGS ===
- Input labels (from source): Pullback Strategy; Lower Timeframe (for BB); Higher Timeframe (for LRL); LRL1 Period (Faster); LRL2 Period (Slower); Linear Regression Shift; Bollinger Bands Period; Bollinger Bands Deviation; Price type for BB; CCI Period for Pullback

### MultiTimeframe_LRL_BB_CCI_Screener_v2

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\screeners\MultiTimeframe_LRL_BB_CCI_Screener_v2.mq5`
- Platform file type: .mq5
- Version tag: 2.00
- Author/copyright tag: Copyright 2025, MetaQuotes Software Corp.
- Language tags: RSI, BB, Bollinger, CCI, MTF
- Header notes (from source comments): +------------------------------------------------------------------+ | |                       MultiTimeframe_LRL_BB_CCI_Screener_v2.mq5 | | |                        Copyright 2025, MetaQuotes Software Corp. | | +------------------------------------------------------------------+ | --- Plot settings | --- Input Parameters | --- Indicator buffers | --- Global variables
- Input labels (from source): Higher Timeframe for LRL; Lower Timeframe for BB/CCI; LRL1 Period; LRL2 Period; Bollinger Bands Period; BB Standard Deviation; CCI Period; Max signals to display

### MultiTimeframe_NN_EA

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\MultiTimeframe_NN_EA\MultiTimeframe_NN_EA.mq5`
- Platform file type: .mq5
- Language tags: RSI, SMA, neural, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                MultiTimeframe_NN_EA.mq5         | | |                    Multi-Timeframe Neural Network EA            | | |  Uses 5 indicators on 2 timeframes (5M & 15M) = 10 features     | | +------------------------------------------------------------------+ | --- Global safety utilities | --- Model selection enum | --- EA Inputs
- Input labels (from source): Which neural network model to use?; Set to true for initial training, false for deployment; Train until the average error is below this value (lower = more accurate); Safety break for training loop (increased for better accuracy); How many bars into the future to predict; Fixed lookback window for the model; Trading lot size

### MultiTimeframe_NN_EA_v2

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\MultiTimeframe_NN_EA_v2\MultiTimeframe_NN_EA_v2.mq5`
- Platform file type: .mq5
- Description: Features: Daily percentage targets, trailing drawdown protection, smart exit logic
- Version tag: 2.00
- Author/copyright tag: Copyright 2025, MetaQuotes Software Corp.
- Language tags: RSI, BB, Bollinger, CCI, SMA, neural, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                    MultiTimeframe_NN_EA_v2.mq5 | | |                        Copyright 2025, MetaQuotes Software Corp. | | |                                             https://www.mql5.com | | +------------------------------------------------------------------+ | --- Forward declarations | --- Normalization helpers | --- Helper function to check for finite numbers
- Input labels (from source): Which neural network model to use?; Set to true for training, false for live trading; Train until the average error is below this value; Maximum training epochs; How many bars into the future to predict; Lookback window for the model; Daily profit target (2%); Maximum daily drawdown before halting (1%); Minimum lot size; Maximum lot size per trade

### NeuralNetworkScreener

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\NeuralNetworkScreener.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Neural Network Trading Screener
- Language tags: RSI, CCI, neural, perceptron
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                         NeuralNetworkScreener.mq5 | | |                                 Neural Network Trading Screener | | |                                             https://www.mql5.com | | +------------------------------------------------------------------+ | Include available math libraries | --- External parameters | --- Dashboard layout constants
- Input labels (from source): Train neural network on startup; Days of historical data for training; Signal strength threshold (0-1); Dashboard update interval; Maximum symbols to scan; Enable sound alerts for strong signals; Enable detailed logging

### NeuralNetworkScreener_Simple

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\NeuralNetworkScreener_Simple.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Neural Network Trading Screener
- Language tags: RSI, CCI, neural
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                 NeuralNetworkScreener_Simple.mq5 | | |                                 Neural Network Trading Screener | | |                                             https://www.mql5.com | | +------------------------------------------------------------------+ | Use built-in MQL5 math functions only (no external dependencies) | --- Input parameters | --- Neural network parameters
- Input labels (from source): Train neural network on startup; Days of historical data for training; Signal strength threshold (0-1); Dashboard update interval; Maximum symbols to scan; Enable sound alerts for strong signals; Enable detailed logging; Seconds between auto-training (0 to disable, 3600 = 1 hour); Prefix for saved models (will add timestamp)

### NeuralNetworkScreener_Simple_Updated

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\NeuralNetworkScreener_Simple_Updated.mq5`
- Platform file type: .mq5
- Version tag: 1.10
- Author/copyright tag: Neural Network Trading Screener
- Language tags: RSI, CCI, neural
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                 NeuralNetworkScreener_Simple.mq5 | | |                                 Neural Network Trading Screener | | |                                             https://www.mql5.com | | +------------------------------------------------------------------+ | Use built-in MQL5 math functions only (no external dependencies) | --- Input parameters | --- Neural network parameters
- Input labels (from source): Train neural network on startup; Days of historical data for training; Signal strength threshold (0-1); Dashboard update interval; Maximum symbols to scan; Enable sound alerts for strong signals; Enable detailed logging; Seconds between auto-training (0 to disable, 3600 = 1 hour); Prefix for saved models (will add timestamp); Number of training epochs

### NN_CCI_Screener

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\NN_CCI_Screener.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Neural Network Trader
- Language tags: RSI, CCI, SMA, neural
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                           NN_CCI_Screener.mq5   | | |                        Copyright 2025, Neural Network Trader    | | |                                             https://www.mql5.com | | +------------------------------------------------------------------+ | Include necessary libraries for basic functionality | --- Input parameters | --- Global variables
- Input labels (from source): Primary timeframe; Secondary timeframe; CCI Period; SMA Period; Regression Period; Maximum symbols to scan; Play alert sounds; Show neutral signals

### NN_CCI_Screener_Simple

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\NN_CCI_Screener_Simple.mq5`
- Platform file type: .mq5
- Version tag: 2.00
- Author/copyright tag: Neural Network Trader
- Language tags: RSI, CCI, SMA, neural
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                   NN_CCI_Screener_Complete.mq5  | | |                        Copyright 2025, Neural Network Trader    | | |                                             https://www.mql5.com | | +------------------------------------------------------------------+ | Removed ALGLIB include - using simplified neural network approach | --- Input parameters | --- Global variables
- Input labels (from source): Primary timeframe; Secondary timeframe; CCI Period; SMA Period; Linear Regression Period; Input neurons (4 CCI/SMA + 2 regression); Hidden layer neurons; Output neurons (Buy/Sell/Neutral); Retrain every N bars; Enable neural network predictions

### OnlineLearnerEA

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\OnlineLearnerEA.mq5`
- Platform file type: .mq5
- Version tag: 5.00
- Author/copyright tag: OnlineLearnerEA v5.00 - 100% Functional
- Language tags: RSI, neural
- Header notes (from source comments): +------------------------------------------------------------------+ | | OnlineLearnerEA_v5_Fixed.mq5                                     | | | Advanced ML Trading Laboratory - 100% Functional Implementation | | | Real Neural Networks, Decision Trees, Clustering & Fuzzy Logic  | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Color Constants                                                  | | +------------------------------------------------------------------+
- Input labels (from source): Neural network learning rate; L2 regularization factor; predict direction after this many bars; number of past returns used as features; sliding window for error rate; saved in Files (common); write CSV header; show prediction arrows on chart; show performance dashboard; use ensemble learning

### OnlineLearnerEA_v5_Fixed

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\OnlineLearnerEA_v5_Fixed.mq5`
- Platform file type: .mq5
- Version tag: 5.00
- Author/copyright tag: OnlineLearnerEA v5.00 - 100% Functional
- Language tags: RSI, neural
- Header notes (from source comments): +------------------------------------------------------------------+ | | OnlineLearnerEA_v5_Fixed.mq5                                     | | | Advanced ML Trading Laboratory - 100% Functional Implementation | | | Real Neural Networks, Decision Trees, Clustering & Fuzzy Logic  | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Color Constants                                                  | | +------------------------------------------------------------------+
- Input labels (from source): Neural network learning rate; L2 regularization factor; predict direction after this many bars; number of past returns used as features; sliding window for error rate; saved in Files (common); write CSV header; show prediction arrows on chart; show performance dashboard; use ensemble learning

### PDF_MultiStrategy_MTF_EA_v1

- Source: `C:\Users\user\Downloads\_CODE\PDF_MultiStrategy_MTF_EA_v1.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: User Strategy Spec - PDF MultiStrategy MTF EA v1
- Language tags: RSI, BB, CCI, SMA, MTF, pullback, momentum, session, breakout, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                    PDF_MultiStrategy_MTF_EA_v1.mq5                | | +------------------------------------------------------------------+ | | ONE EA covering every fully-specified indicator strategy from the | | | "Example trading strategies portfolio v2" PDF, each wrapped in    | | | the SAME dual-timeframe (5m + 30m) trigger rule:                  | | |                                                                    | | |   A strategy fires ONLY when its own buy (or sell) condition is   |
- Input labels (from source): InpMagic; InpUseSTRAT001; RANGE 10-40 step 5; RANGE 1.0-3.0 step 0.5; InpUseSTRAT002; RANGE 10-50 step 10; RANGE 60-150 step 10; InpUseSTRAT003; RANGE 10-30 step 5; RANGE 60-150 step 10

### PDF_MultiStrategy_MTF_EA_v2

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\PDF_MultiStrategy_MTF_EA_v2.mq5`
- Platform file type: .mq5
- Version tag: 2.00
- Author/copyright tag: User Strategy Spec - PDF MultiStrategy MTF EA v2 (audited)
- Language tags: RSI, BB, CCI, SMA, MTF, momentum, session, breakout, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                    PDF_MultiStrategy_MTF_EA_v2.mq5                | | +------------------------------------------------------------------+ | | v2 = audited/corrected version of v1. Same architecture:          | | |  - 8 indicator strategies from the PDF, each with symmetric        | | |    buy/sell conditions (mirror thresholds/comparisons).            | | |  - A strategy fires only when its condition is true on M5 AND M30  | | |    at the same time. Each strategy toggleable; settings = inputs.  |
- Input labels (from source): InpMagic; InpUseSTRAT001; RANGE 10-40 step 5; RANGE 1.0-3.0 step 0.5; RANGE 100-300 step 50 -- [F1] BB(200) middle regime filter; InpUseSTRAT002; RANGE 10-50 step 10; RANGE 60-150 step 10; InpUseSTRAT003; RANGE 10-30 step 5

### PDF_MultiStrategy_VotingForest_EA_v4

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\PDF_MultiStrategy_VotingForest_EA_v4.mq5`
- Platform file type: .mq5
- Version tag: 4.00
- Author/copyright tag: User Strategy Spec - PDF MultiStrategy Voting Forest EA v4
- Language tags: RSI, BB, CCI, SMA, EMA, momentum, session, breakout, shift, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                PDF_MultiStrategy_VotingForest_EA_v4.mq5           | | +------------------------------------------------------------------+ | | v4 = v3 with the entry engine changed from "first match wins" to  | | | a STRATEGY-VOTING FOREST:                                          | | |                                                                    | | |   - Every ENABLED strategy is a "tree". Each tick it votes         | | |     BUY, SELL, or abstains (its condition must be true on M5 AND   |
- Input labels (from source): Magic number; Risk % of equity per trade (0.05-1.0 step 0.05); Forest: min votes on one side to trade (1-8 step 1); Forest: votes must beat the other side by this many (1-8 step 1); Log per-strategy votes per M5 bar to CSV (training data for the agent; OFF while optimizing); S001: ON/OFF; S001: breakout BB period (10-40 step 5); S001: regime BB period, middle band filter (100-300 step 50); S001: BUY when close > UPPER band at this deviation (1.0-3.0 step 0.5); S001: SELL when close < LOWER band at this deviation (1.0-3.0 step 0.5)

### PerceptronEA

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\PerceptronEA.mq5`
- Platform file type: .mq5
- Version tag: 5.00
- Author/copyright tag: 2024
- Language tags: RSI, BB, Bollinger, SMA, momentum, perceptron, shift, ATR, MACD
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                           PerceptronEA.mq5       | | |  Three-layer ML pipeline  v5.00                                  | | |                                                                   | | |  LAYER 1 — Perceptron  (entry confidence gate)                  | | |  LAYER 2 — Naive Bayes (pattern win-probability gate)           | | |  LAYER 3 — Linear Regression (exit timing)                      | | |                                                                   |
- Input labels (from source): Risk per trade (fraction of equity); Reward target  (fraction of equity); Hard stop-loss distance in points; Perceptron weight update step (0.001–0.01); Forward M1 bars for outcome label (5–200); Historical M1 bars to replay on init (0=skip); Min |pred| to trade or update weights (0.05–0.50); Min samples in bin before NB is trusted (10–100); Min win probability to allow trade (0.50–0.75); LR lookback period (10–50)

### play 4.2

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\screeners\play 4.2.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2025, Grok Assisted Development
- Language tags: RSI, CCI, SMA, momentum, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                           CustomScreener v4.mq5  | | |                        Copyright 2025, Grok Assisted Development | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Custom indicator initialization function                         | | +------------------------------------------------------------------+ | Set timer for updates
- Input labels (from source): Broker suffix to append (e.g., ".sim" or "_otc"); Lower timeframe; Upper timeframe; First CCI period; Second CCI period; Momentum CCI timeframe; Momentum CCI period; Lower timeframe Buy level; Lower timeframe Sell level; Upper timeframe Buy level

### play 4.3

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\screeners\play 4.3.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2025, Grok Assisted Development
- Language tags: RSI, BB, CCI, SMA, momentum, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                           CustomScreener v4.3.mq5| | |                        Copyright 2025, Grok Assisted Development | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Custom indicator initialization function                         | | +------------------------------------------------------------------+ | Set timer for updates
- Input labels (from source): Broker suffix to append (e.g., ".sim" or "_otc"); Lower timeframe; Upper timeframe; First CCI period; Second CCI period; Momentum CCI timeframe; Momentum CCI period; Lower timeframe Buy level; Lower timeframe Sell level; Upper timeframe Buy level

### Pure_CCI_Screener

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\Pure_CCI_Screener.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Pure CCI Trader
- Language tags: RSI, CCI, SMA, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                             Pure_CCI_Screener.mq5 | | |                        Copyright 2025, Pure CCI Trader          | | |                                             https://www.mql5.com | | +------------------------------------------------------------------+ | --- Input parameters | --- Signal types | --- Structure for signal data
- Input labels (from source): CCI Period; SMA Period for CCI smoothing; SMA Shift (0 = current bar); Timeframe to analyze; Max symbols to display; Starting X position; Starting Y position; Height between rows; Buy signal color; Sell signal color

### Q-learning

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\Q-learning.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2022, DNG
- Language tags: RSI, CCI, Q-learning, ATR, MACD
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                   Q-Learning.mq5 | | |                                              Copyright 2022, DNG | | |                                https://www.mql5.com/ru/users/dng | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Includes                                                         | | +------------------------------------------------------------------+
- Input labels (from source): Study period, years; Batch; UpdateTarget; Iterations; DiscountFactor; Period; Applied price; Period; Applied price; Period

### RegressionlineEA

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\RegressionlineEA.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2025, YourName
- Language tags: RSI
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                             RegressionlineEA.mq5 | | |                                         Copyright 2025, YourName | | |                                                 https://mql5.com | | | 13.09.2025 - Initial release                                     | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Expert initialization function                                   |

### RL_PropTrader_Final

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\RL_PropTrader_Final.mq5`
- Platform file type: .mq5
- Version tag: 1.020
- Author/copyright tag: Copyright 2026
- Language tags: RSI, CCI, FTMO
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                          RL_PropTrader_Final.mq5 | | |                        Pure MQL5 multi-symbol RL EA (Phase 5)   | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Q-table helpers                                                  | | +------------------------------------------------------------------+
- Input labels (from source): FTMO_Mode; Training_Mode; Daily_Profit_Target_Pct; Daily_Risk_Target_Pct; Max_Total_Loss_Pct; Max_Trades_Per_Day; Winning_Days_Before_Save; DayEndFlattenMinutes; Alpha; Gamma

### RL_PropTrader_MVP_v2

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\RL_PropTrader_MVP_v2.mq5`
- Platform file type: .mq5
- Version tag: 1.002
- Author/copyright tag: Copyright 2026
- Language tags: RSI, CCI, SMA, FTMO
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                          RL_PropTrader_Final.mq5 | | |                         Pure MQL5 multi-symbol RL EA foundation  | | +------------------------------------------------------------------+
- Input labels (from source): FTMO_Mode; Daily_Profit_Target_Pct; Daily_Risk_Target_Pct; Max_Trades_Per_Day; Winning_Days_Before_Save; Alpha; Gamma; Epsilon; Max_Symbols; SaveFileName

### rsi_bb_extreme

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\rsi_bb_extreme.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Custom Strategy
- Language tags: RSI, BB, Bollinger, SMA, scalp, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                ExtremeBandMeanReversion.mq5      | | |                        Extreme Band Mean-Reversion Scalp EA      | | |                     Bollinger Bands + RSI Mean Reversion         | | +------------------------------------------------------------------+ | --- Input parameters (all optimizable) | --- Global variables | +------------------------------------------------------------------+
- Input labels (from source): BB Period; BB Deviation; BB Shift (forward/back); RSI Period; RSI Oversold level; RSI Overbought level; Risk percent of balance per trade; SL distance = BB width * this multiplier; TP Mode: 0=Middle BB, 1=Risk:Reward; Risk:Reward ratio (if TPMode=1)

### S11_Runner

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\S11_Runner.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: DECISON TREE project - S11 Runner
- Language tags: RSI, CCI, FTMO, session, ATR, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                   S11_Runner.mq5 | | +------------------------------------------------------------------+ | | STRATEGY: "S11 Runner" -- long-only NY-session drift capture.     | | |                                                                    | | | PROVENANCE: the single validated config from the DECISON TREE     | | | research project (s11.py honest harness, runner_config.json).     | | | Verified backtest numbers this EA must reproduce (OOS 2024-07..   |
- Input labels (from source): first permissible DECISION minute (16:30); decisions allowed while minute < this (23:00); force-flat everything at/after this minute (23:55); M5 CCI period (PRICE_TYPICAL); M5 Wilder ATR period; stop = this x Wilder ATR(14, M5); refuse trade if stop distance <= this (index points); % of current balance risked per trade; day-lock: close + halt at +2.5% of day-start balance; trailing-DD safety halt (true FTMO fail line = 4.0)

### Simple scalper

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\Simple scalper.mq5`
- Platform file type: .mq5
- Language tags: RSI, BB, CCI, SMA, EMA, MTF, scalp, FTMO, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                          Simple Scalper v3.mq5  | | |                                    Multi-TF Slope Scalper + FTMO | | +------------------------------------------------------------------+ | === GENERAL SETTINGS === | === LTF — TRIGGER (TF1) === | === MTF — SETUP (TF2) === | === HTF — TREND (TF3) ===
- Input labels (from source): _sep_gen; Lot_Size; Magic_Number; Enable_Buys; Enable_Sells; Max_Open_Trades_Per_Symbol; _sep_ltf; LTF; LTF_MA_Period; LTF_MA_Method

### Slope_Screener

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\screeners\Slope_Screener.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2025, Slope Screener Trader
- Language tags: RSI
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                           Slope_Screener.mq5     | | |                        Copyright 2025, Slope Screener Trader     | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Custom indicator initialization function                         | | +------------------------------------------------------------------+ | Set timer for updates
- Input labels (from source): Period for slope calculation (Timeframe1); First Timeframe for slope calculation; Period for slope calculation (Timeframe2); Second Timeframe for slope calculation; Broker suffix to append (e.g., ".sim" or "_otc"); Font size for labels; Color for positive slope; Color for negative slope; Color for neutral/no slope; Update interval in seconds

### Slope_Screener_Fixed

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\screeners\Slope_Screener_Fixed.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2025, Slope Screener Trader
- Language tags: RSI
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                           Slope_Screener.mq5     | | |                        Copyright 2025, Slope Screener Trader     | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Custom indicator initialization function                         | | +------------------------------------------------------------------+ | Set timer for updates
- Input labels (from source): Period for slope calculation (Timeframe1); First Timeframe for slope calculation; Period for slope calculation (Timeframe2); Second Timeframe for slope calculation; Broker suffix to append (e.g., ".sim" or "_otc"); Font size for labels; Color for positive slope; Color for negative slope; Color for neutral/no slope; Update interval in seconds

### SMA_Fan_MTF_BBExit_v1

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\SMA_Fan_MTF_BBExit_v1.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: User Strategy Spec - SMA Fan MTF + BB Exit v1
- Language tags: RSI, BB, Bollinger, SMA, MTF, shift, ATR, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                         SMA_Fan_MTF_BBExit_v1.mq5                 | | +------------------------------------------------------------------+ | | STRATEGY: Ascending/Descending SMA Fan (dual timeframe 5m+15m)   | | |           entry, single-timeframe (1m) Bollinger Band exit.      | | |                                                                    | | | ENTRY LOGIC:                                                      | | |   4 SMAs, each with its OWN period and its OWN forward shift.     |
- Input labels (from source): Fastest SMA period. RANGE 1-4 step 1; Fastest SMA forward shift. RANGE 0-3 step 1; 2nd SMA period. RANGE 1-6 step 1; 2nd SMA forward shift. RANGE 0-4 step 1; 3rd SMA period. RANGE 1-8 step 1; 3rd SMA forward shift. RANGE 0-5 step 1; Slowest SMA period. RANGE 1-10 step 1; Slowest SMA forward shift. RANGE 0-6 step 1; Applied price for all 4 SMAs, all timeframes; BB period, M1. RANGE 10-40 step 5

### some bs

- Source: `C:\Users\user\OneDrive\Desktop\ARMY\00_DROP_GOALS_AND_IDEAS_HERE\_library\2026 files\FTMO EA\some bs.mq5`
- Platform file type: .mq5
- Version tag: 1.20
- Author/copyright tag: Copyright 2021, MetaQuotes Ltd.
- Language tags: RSI, neural, MACD
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                  some bullshit.mq5 | |                     1M neural EA with arrows + TP line | +------------------------------------------------------------------+
- Input labels (from source): TimeFrame; TradeLevel; Lot; MaxTP; ProfitMultiply; MinTarget; StopLoss

### some bullshit

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\some bullshit.mq5`
- Platform file type: .mq5
- Version tag: 1.20
- Author/copyright tag: Copyright 2021, MetaQuotes Ltd.
- Language tags: RSI, neural, MACD
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                  some bullshit.mq5 | |                     1M neural EA with arrows + TP line | +------------------------------------------------------------------+
- Input labels (from source): TimeFrame; TradeLevel; Lot; MaxTP; ProfitMultiply; MinTarget; StopLoss

### StrikeGate

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\StrikeGate.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: FTMO CUSTOM EA
- Language tags: RSI, CCI, SMA, pullback, FTMO, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                    CCI Strike Gate EA | | |                                      Copyright 2024, FTMO CUSTOM EA | | |                                      https://www.ftmo.com | | +------------------------------------------------------------------+ | --- Global variables | --- Data structure | +------------------------------------------------------------------+
- Input labels (from source): InpMagicNumber; InpManageOnlyOwnMagic; InpCloseOnSignalLoss; InpAllowOppositeHedge; InpSignalBarShift; InpRunOncePerBar; InpTF1; InpTF2; InpCCI1_Period; InpCCI1_SMAPeriod

### Swarm

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\Swarm.mq5`
- Platform file type: .mq5
- Version tag: 1.02
- Author/copyright tag: OpenAI, 2024
- Language tags: RSI, CCI
- Header notes (from source comments): +------------------------------------------------------------------+ | |       CCI Crowd Sync Screener v1.0 (MT5 EA, bugfixed version)    | | +------------------------------------------------------------------+ | |       Attach to any chart. Scans all Market Watch symbols        | | +------------------------------------------------------------------+ | --- Table cache for ranking | +------------------------------------------------------------------+ | | Expert initialization function                                   |
- Input labels (from source): Lower TF (e.g., H1); Higher TF (e.g., H4); Fast CCI; Medium CCI; Slow CCI; Friends threshold; Smoothing (bars); Display top N

### swarm3.0

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\swarm3.0.mq5`
- Platform file type: .mq5
- Version tag: 3.0
- Author/copyright tag: OpenAI, 2024
- Language tags: RSI, CCI
- Header notes (from source comments): +------------------------------------------------------------------+ | |       CCI Crowd Sync Screener v3.0 (MT5 EA with Visual Table)    | | +------------------------------------------------------------------+ | |       Attach to any chart. Scans all Market Watch symbols        | | +------------------------------------------------------------------+ | --- Global variables for visual table | +------------------------------------------------------------------+ | | Expert initialization function                                   |
- Input labels (from source): Lower TF (e.g., H1); Higher TF (e.g., H4); Fast CCI period; Medium CCI period; Slow CCI period; Friends threshold; Smoothing length; Max rows to display

### to opimize ea

- Source: `C:\Users\user\OneDrive\Desktop\ARMY\00_DROP_GOALS_AND_IDEAS_HERE\_library\2026 files\FTMO EA\to opimize ea.mq5`
- Platform file type: .mq5
- Version tag: Version = 1.00
- Author/copyright tag: Copyright 2025, Mark Montgomery jr
- Language tags: RSI
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                to opimize ea.mq5 | | |                               Copyright 2025, Mark Montgomery jr | | |                                                    igridcoin.com | | +------------------------------------------------------------------+ | +------------------------------------------------------------------+ | | Expert initialization function                                   | | +------------------------------------------------------------------+

### TriTF_SMA_Shift_Optimizer_EA

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\TriTF_SMA_Shift_Optimizer_EA.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: 2026
- Language tags: RSI, SMA, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |              TriTF_SMA_Shift_Optimizer_EA.mq5                    | | |         3-Timeframe SMA Shift Optimizer EA with RSI Exit         | | |                                                                  | | |  STRATEGY SUMMARY:                                               | | |  - Entry TF (default M1): SMA shift stack determines direction   | | |  - TF1 (default M5):  optional higher-TF confirmation filter     | | |  - TF2 (default M15): optional higher-TF confirmation filter     |
- Input labels (from source): Entry timeframe; TF0 SMA period; TF0 Shift 1 (most recent closed bar); TF0 Shift 2; TF0 Shift 3; TF0 Shift 4 (oldest); Enable TF1 filter; TF1 timeframe; TF1 SMA period; TF1 Shift 1

### Unity Play

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Indicators\screeners\Unity Play.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: Copyright 2025, MetaQuotes Software Corp.
- Language tags: RSI, BB, Bollinger, CCI, SMA, MTF, pullback, momentum, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                       MultiTimeframe_LRL_BB_CCI_Screener.mq5    | | |                        Copyright 2025, MetaQuotes Software Corp. | | +------------------------------------------------------------------+ | === PULLBACK STRATEGY SETTINGS === | === MOMENTUM STRATEGY SETTINGS === | === PURE MOMENTUM STRATEGY SETTINGS === | === DISPLAY SETTINGS ===
- Input labels (from source): Pullback Strategy; Lower Timeframe (for BB); Higher Timeframe (for LRL); LRL1 Period (Faster); LRL2 Period (Slower); Linear Regression Shift; Bollinger Bands Period; Bollinger Bands Deviation; Price type for BB; CCI Period for Pullback

### US30_ExpansionTrigger_v1

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\US30_ExpansionTrigger_v1.mq5`
- Platform file type: .mq5
- Version tag: 1.00
- Author/copyright tag: User Strategy Spec - Expansion Trigger v1
- Language tags: RSI, SMA, MTF, FTMO, session, breakout, shift, ATR, trail
- Header notes (from source comments): +------------------------------------------------------------------+ | |                         US30_ExpansionTrigger_v1.mq5              | | +------------------------------------------------------------------+ | | STRATEGY: Expansion Trigger -- NY Opening-Range Breakout          | | |           + Prior-Day Level Sweep-and-Reject (two-sided)          | | |                                                                    | | | PURPOSE (per user spec): predicts expansion BEFORE the move,      | | | instead of confirming multi-timeframe agreement about a move      |
- Input labels (from source): broker-server HOUR of NY 9:30 AM cash open (GMT+2 broker example: 15); broker-server MINUTE of NY 9:30 AM cash open; Opening-range window length in minutes. RANGE 10-30 step 5; Max allowed OR range width, in ATR units. Skip breakout if wider (move already happened). RANGE 1.0-2.5 step 0.25; Stop-loss distance, in ATR units (volatility-scaled, not fixed points). RANGE 1.0-3.0 step 0.5; Force-close a trade after this many minutes if neither SL nor TP hit. RANGE 60-240 step 30; Risk % of equity per trade, used for ATR-based lot sizing. RANGE 0.25-1.0 step 0.25; ATR period, M15, used for all volatility scaling; Take-profit = InpTPRewardMult x SL distance (fixed 1:2 RR logic, not swept); Hard cap: selective, 1-2 quality setups/day (ORB + Sweep-Reject, one each)

### ZeroLineRadar

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\ZeroLineRadar.mq5`
- Platform file type: .mq5
- Description: Multi-symbol, multi-timeframe CCI screener with alerts and optional auto-close.
- Version tag: 2.0
- Author/copyright tag: You
- Language tags: RSI, BB, Bollinger, CCI, SMA, EMA, FTMO, session, shift, ATR
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                   ZeroLineRadar  | | |                         CCI Multi-Timeframe Screener Pro v2      | | +------------------------------------------------------------------+ | SMA(1, shift) filter: | For each lower timeframe CCI line, the EA reads the current CCI value | and a shifted signal line that is effectively CCI[shift] for period=1. | When InpUseLowerCCISignal=true, the lower TF buy condition requires
- Input labels (from source): InpLowerTF; InpHigherTF; InpCCIFast; InpCCIMed; InpCCISlow; InpScanMode; InpRefreshSeconds; InpRowsPerPage; InpHideChartStuff; InpPanelX

### ZeroLineRadar0works

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\ZeroLineRadar0works.mq5`
- Platform file type: .mq5
- Description: Multi-symbol, multi-timeframe CCI screener with alerts and optional auto-close.
- Version tag: 2.0
- Author/copyright tag: You
- Language tags: RSI, CCI, EMA, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                   ZeroLineRadar  | | |                         CCI Multi-Timeframe Screener Pro v2      | | +------------------------------------------------------------------+ | --- inputs: timeframes & CCI | --- scan & refresh | --- lower timeframe signal-line filter | --- higher timeframe signal-line filter
- Input labels (from source): InpLowerTF; InpHigherTF; InpCCIFast; InpCCIMed; InpCCISlow; InpScanMode; InpRefreshSeconds; InpRowsPerPage; InpHideChartStuff; InpPanelX

### Zerolineradar1

- Source: `C:\Users\user\AppData\Roaming\MetaQuotes\Terminal\49CDDEAA95A409ED22BD2287BB67CB9C\MQL5\Experts\Zerolineradar1.mq5`
- Platform file type: .mq5
- Description: Multi-symbol, multi-timeframe CCI screener with alerts and optional auto-close.
- Version tag: 2.0
- Author/copyright tag: You
- Language tags: RSI, BB, Bollinger, CCI, SMA, EMA, FTMO, session, shift
- Header notes (from source comments): +------------------------------------------------------------------+ | |                                                   ZeroLineRadar  | | |                         CCI Multi-Timeframe Screener Pro v2      | | +------------------------------------------------------------------+ | SMA(1, shift) filter: | For each lower timeframe CCI line, the EA reads the current CCI value | and a shifted signal line that is effectively CCI[shift] for period=1. | When InpUseLowerCCISignal=true, the lower TF buy condition requires
- Input labels (from source): InpLowerTF; InpHigherTF; InpCCIFast; InpCCIMed; InpCCISlow; InpScanMode; InpRefreshSeconds; InpRowsPerPage; InpHideChartStuff; InpPanelX

