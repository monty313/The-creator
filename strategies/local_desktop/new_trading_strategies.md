# Momentum and Mean-Reversion Entry Strategies

This document codifies four multi-timeframe entry strategies built for the MT5 Gravity Framework. They follow the core logic of using Higher Timeframes (HTF) to establish dominant directional gravity, while Lower Timeframes (LTF) trigger the entry through slingshot pullbacks or alignment.

## Core Architecture: Timeframe Sets
These strategies operate on chained timeframe groups. The first timeframe listed is the Execution (Lower) Timeframe. The subsequent timeframes act as the Directional (Higher) Timeframes. 

*Standard Confidence Sets:*
- 1m (LTF) / 15m (HTF) / 30m (HTF)
- 5m (LTF) / 30m (HTF) / 1h (HTF)
- 15m (LTF) / 1h (HTF) / 4h (HTF)
- 30m (LTF) / 4h (HTF) / 1d (HTF)

*Extra Confidence Sets (Adds one more HTF acting with identical logic to the other HTFs):*
- 1m / 15m / 30m / 1h
- 5m / 30m / 1h / 4h
- 15m / 1h / 4h / 1d
- 30m / 4h / 1d / 1w

*(Note: Buy rules are listed below. Sell rules are the exact mathematical inverse.)*

---

## Strategy 1: Dual CCI Shifted SMA Slingshot

**Logic:** The HTFs establish strong momentum gravity by pulling both fast and slow CCIs above their predictive SMAs. The LTF executes a "slingshot" entry when the fast CCI briefly dips below its SMA (building tension) while the slow CCI remains anchored above its SMA.

**Indicators:**
- CCI 30 (Fast)
- CCI 100 (Slow)
- Applied to both CCIs: SMA 2, Shift +2

**Buy Rules:**
- **HTF Condition:** Both CCI 30 and CCI 100 are ABOVE their respective applied SMAs.
- **LTF Trigger:** CCI 100 is ABOVE its applied SMA, AND CCI 30 is BELOW its applied SMA (pullback).

---

## Strategy 2: Dual Bollinger Band Trend Reversion

**Logic:** HTFs prove intense trend continuation by keeping price above a wide and a tight Bollinger Band. The LTF executes when price pulls back from extreme over-extension, dipping below the tight band but staying above the wide band.

**Indicators:**
- Bollinger Band 100, Deviation 0.5, Shift +2
- Bollinger Band 10, Deviation 0.5, Shift +2
- SMA 50

**Buy Rules:**
- **HTF Condition:** Price is ABOVE both the 100-period and 10-period Bollinger Bands.
- **LTF Trigger:** Price is ABOVE the 100-period Bollinger Band, but pulls back to close BELOW the 10-period Bollinger Band.
- **Re-entry Rule:** Re-enter long every time price bounces down and touches the 10-period Bollinger Band, AS LONG AS the 50 SMA remains above the 100-period Bollinger Band on the LTF.

---

## Strategy 3: Shifted Price Envelope Breakout

**Logic:** Uses forward-shifted Simple Moving Averages applied directly to the High and Low of price to create a predictive envelope. Buys require price to fully clear the top of the envelope across all timeframes.

**Indicators:**
- **HTF Envelope:** 
  - SMA 4, Shift +4, Applied to High
  - SMA 4, Shift +4, Applied to Low
- **LTF Envelope:**
  - SMA 4, Shift +2, Applied to High
  - SMA 4, Shift +2, Applied to Low

**Buy Rules:**
- **HTF Condition:** Price is ABOVE both the High-applied and Low-applied SMA 4 (Shift +4).
- **LTF Trigger:** Price is ABOVE both the High-applied and Low-applied SMA 4 (Shift +2).

---

## Strategy 4: RSI Bollinger Tension Snap

**Logic:** HTF establishes extreme bullish velocity by keeping both fast and slow RSIs above an applied Bollinger Band. The LTF executes when the slow RSI maintains trend (above the midline) but the fast RSI stretches into an extreme localized oversold state (below its lower band) to snap back upward.

**Indicators:**
- Fast RSI: RSI 2 with applied Bollinger Band (Period 20, Deviation 0.5, Shift +2)
- Slow RSI: RSI 20 with applied Bollinger Band (Period 20, Deviation 0.5, Shift +2)

**Buy Rules:**
- **HTF Condition:** Both RSI 2 and RSI 20 are ABOVE their respective applied Bollinger Bands.
- **LTF Trigger:** RSI 20 is ABOVE the middle level of its applied Bollinger Band, AND RSI 2 is BELOW the lower band of its applied Bollinger Band.
