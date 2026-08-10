# Public / internet strategy language — with sources

Language only. Sources are **upstream URLs** (plus license notes). No vendored strategy code is kept under `strategies/language/`.

## A. je-suis-tm / quant-trading

| Field | Citation |
|-------|----------|
| **Source** | https://github.com/je-suis-tm/quant-trading |
| **License (upstream)** | Apache-2.0 |

| Strategy language | Idea (plain words) |
|-------------------|--------------------|
| London Breakout | Session-aware FX open-range after Tokyo→London |
| Dual Thrust | Intraday range breakout from prior range |
| RSI Pattern Recognition | Classic RSI pattern family |
| Bollinger Bands Pattern Recognition | BB pattern family |
| Parabolic SAR | SAR trail/reverse idea |

## B. freqtrade / freqtrade-strategies

| Field | Citation |
|-------|----------|
| **Source** | https://github.com/freqtrade/freqtrade-strategies |
| **Platform** | https://github.com/freqtrade/freqtrade |
| **License (upstream)** | GPL-3.0 |

| Strategy language | Idea (plain words) |
|-------------------|--------------------|
| multi_tf | Multi-timeframe RSI via informative pairs |
| InformativeSample | Higher-TF context pattern |
| Bandtastic / BbandRsi / Low_BB | Bollinger-centric / RSI+BB mean reversion |
| MultiRSI | Multiple RSI lengths |
| Scalp / SmoothScalp / ReinforcedSmoothScalp / Quickie | High-turnover scalp density language |
| HourBasedStrategy | Hour-of-day session gates |
| Supertrend | Supertrend filter language |
| CustomStoplossWithPSAR / FixedRiskRewardLoss | Stop / R:R management sketches |
| hlhb | High-low / HLHB structure sample |

Upstream: educational examples; not production by default.

## C. vectorbt templates

| Field | Citation |
|-------|----------|
| **Source (project)** | https://github.com/polakowo/vectorbt |
| **Note** | Local template names harvested earlier; language only retained |

| Template language | Idea |
|-------------------|------|
| rsi_backtest | RSI entry/exit template |
| supertrend_backtest | Supertrend template |
| donchian_backtest | Donchian channel template |

## D. Not retained as strategy language

| Item | Note |
|------|------|
| Scam stubs / Loader bots | Not strategies |
| Exchange bots without readable edge prose | Skipped |
