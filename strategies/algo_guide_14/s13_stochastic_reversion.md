# Strategy 13: STOCHASTIC OSCILLATOR REVERSION

**family profile key:** guide_s13_stoch_mr  
**slug:** s13_stochastic_reversion  
**kind:** note / educational guide  
**Source HTML:** strategies/Strategies to replicate in Algo Trading.docx.html  
**Source URL (saved from):** https://docs.google.com/document/u/0/d/1j7bEX0znMD0YhcpR3oijKIzX8qBj3-lX/mobilebasic  
**Class:** mean reversion  
**Not Court law.** Language-only inventory for lab adapters under 2HTF+1LTF · 4 sets · PB+cont.

---

## Guide language (extracted)

STRATEGY 13 
 STOCHASTIC OSCILLATOR REVERSION 
 Measures where price closed within its recent range — %K and %D crossovers in extreme zones trigger entries 

 Diagram 13 — Stochastic %K (yellow) and %D (blue dashed) with overbought zone above 80 and oversold below 20. Short when %K crosses below %D while both are above 80. Long when %K crosses above %D while both are below 20. 
 The Concept 
 The Stochastic Oscillator measures where price closed relative to its high-low range over the past N periods, scaled from 0 to 100. A reading of 100 means price closed at the highest point of its recent range. A reading of 0 means it closed at the lowest point. Values above 80 suggest the market is closing consistently near its highs — overbought. Values below 20 suggest closing consistently near the lows — oversold. 

 The oscillator produces two lines: %K (the raw calculation, faster) and %D (a 3-period smoothed average of %K, slower). The entry signal is a crossover of %K through %D while both lines are inside the extreme zone — not merely touching the threshold. 

 How to Use It 

 Entry Rules 

 Short entry: Both %K and %D are above 80. %K crosses BELOW %D while in the overbought zone. Enter short on the close of the crossover bar. 

 Long entry: Both %K and %D are below 20. %K crosses ABOVE %D while in the oversold zone. Enter long on the close of the crossover bar. 

 Stronger setup — "hook" from deep extreme: %K dips below 10 (or above 90 for shorts) before reversing. The deeper the extreme before the crossover, the stronger the reversion signal. 

 Trend filter: Use the Stochastic on a higher timeframe for context. Only take long entries at oversold on the lower timeframe if the higher timeframe Stochastic is also rising (not pinned in overbought). 

 Settings: Standard is (14, 3, 3) — 14-period %K, 3-period smoothing for %D, 3-period further smoothing. Faster settings like (5, 3, 3) give more signals but noisier. 

 Stop Loss and Exit 

 Stop loss: Below the recent swing low (for longs). The recent low is the level at which the oversold reading formed — if that breaks, the reversion has failed. 

 Exit: Stochastic reaches 50 (midline) for conservative exit; Stochastic reaches the opposite extreme zone (80 for longs, 20 for shorts) for a full reversion hold. 

 Time-based: If %K has not crossed back toward 50 within 5–8 bars of the signal, the oscillator may be curling back — exit and reassess. 

 Worked Example 
 A currency pair has been declining. Stochastic drops to 12 (%K) and 15 (%D) — both below 20. %K then crosses above %D (now 13 vs 12). Long entry on the crossover close at 1.0720. Swing low at 1.0698 — stop at 1.0693. Target: Stochastic reaches 80 (full reversion) or 1.0820 based on prior resistance. Over 6 days the pair recovers to 1.0815 as Stochastic reaches 77. Exit: 1.0815. Profit: 95 pips on a 27-pip risk. 

 Common Mistakes 

 Entering at the 80/20 threshold touch rather than waiting for the %K/%D crossover — price can remain overbought or oversold for many bars. The crossover is the momentum shift confirmation. 

 Using Stochastic on trending instruments without a trend filter — it generates continuous "oversold" readings in a downtrend. Every one of those appears like a long opportunity and most will fail. 

 Confusing Slow Stochastic with Fast Stochastic — Fast Stochastic is noisier and whipsaws more. Most traders prefer Slow Stochastic (already smoothed). Check your platform settings.
