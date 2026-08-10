# Strategy 11: KELTNER CHANNEL REVERSION

**family profile key:** guide_s11_keltner_mr  
**slug:** s11_keltner_reversion  
**kind:** note / educational guide  
**Source HTML:** strategies/Strategies to replicate in Algo Trading.docx.html  
**Source URL (saved from):** https://docs.google.com/document/u/0/d/1j7bEX0znMD0YhcpR3oijKIzX8qBj3-lX/mobilebasic  
**Class:** mean reversion  
**Not Court law.** Language-only inventory for lab adapters under 2HTF+1LTF · 4 sets · PB+cont.

---

## Guide language (extracted)

STRATEGY 11 
 KELTNER CHANNEL REVERSION 
 ATR-based bands that stay calmer than Bollinger during volatile spikes — fewer false signals 

 Diagram 11 — Keltner Channel (EMA ± 2×ATR). Short: price spikes above upper band, closes back inside. Long: price drops below lower band, closes back inside. Target: middle EMA. Comparison box shows difference vs Bollinger Bands. 
 The Concept 
 Keltner Channels work on the same principle as Bollinger Bands — define a "normal" trading range and trade reversions when price exits it. The key difference is the band calculation method. Bollinger Bands use standard deviation (which expands dramatically during volatile price spikes, widening the bands just as you want to trade the reversion). Keltner Channels use ATR (Average True Range), which is smoother and slower to respond — the bands stay more stable during spike conditions, giving cleaner reversion signals. 

 Construction: Middle band = 20-period EMA. Upper band = EMA + (2 × ATR). Lower band = EMA − (2 × ATR). Some traders use 1.5× or 2.5× ATR depending on preferred sensitivity. 

 How to Use It 

 Entry Rules 

 Short setup: Price closes above the upper Keltner band. Wait for the next candle to close back inside (below the upper band). Enter short on that close. 

 Long setup: Price closes below the lower Keltner band. Wait for the next candle to close back inside (above the lower band). Enter long on that close. 

 Combine with RSI: Require RSI above 70 for the short setup, RSI below 30 for the long setup. This dual confirmation filters out noise. 

 Keltner + Bollinger combination: When Bollinger Bands are INSIDE the Keltner Channel, the market is in a squeeze — a major move is coming. Do not trade reversion in this condition. Wait for the breakout direction, then trade that trend. 

 Stop Loss and Exit 

 Stop loss: Above the upper band for short trades. Below the lower band for long trades. 

 Primary target: The middle EMA (the center of the channel). 

 Extended target: The opposite Keltner band, provided the market is clearly in a range. 

 If price fails to close back inside within 3 bars after the signal — abandon the trade. The momentum is too strong for a reversion. 

 Worked Example 
 A commodity is ranging. Keltner upper band = $88.00. Price spikes to $89.20 on news, then closes the candle at $87.40 — back inside the channel. RSI at the close is 74 (above 70, confirming overbought). Short entry: $87.40. Stop: $89.50 (above upper band). Middle EMA target: $82.00. Price reverts over 4 days to $82.20. Exit: $82.20. Profit: $5.20 on a $2.10 risk. 

 Common Mistakes 

 Confusing Keltner and Bollinger Bands setup — both use a middle average and outer bands, but Keltner's ATR-based width makes it distinctly different during volatile periods. Know which one you have loaded. 

 Using the same multiplier for all instruments — a 2×ATR band is appropriate for some instruments but too tight or too wide for others. Calibrate to the instrument's typical daily range. 

 Ignoring the Keltner/Bollinger squeeze — this is the single most important Keltner signal and the one that tells you NOT to trade reversion. Missing it leads to fighting a breakout.
