# Strategy 12: Z-SCORE STATISTICAL REVERSION

**family profile key:** guide_s12_zscore_mr  
**slug:** s12_zscore_reversion  
**kind:** note / educational guide  
**Source HTML:** strategies/Strategies to replicate in Algo Trading.docx.html  
**Source URL (saved from):** https://docs.google.com/document/u/0/d/1j7bEX0znMD0YhcpR3oijKIzX8qBj3-lX/mobilebasic  
**Class:** mean reversion  
**Not Court law.** Language-only inventory for lab adapters under 2HTF+1LTF · 4 sets · PB+cont.

---

## Guide language (extracted)

STRATEGY 12 
 Z-SCORE STATISTICAL REVERSION 
 The most mathematically rigorous reversion signal — how many standard deviations from the mean? 

 Diagram 12 — Price with rolling mean, and Z-Score oscillator below. Entry SHORT when Z crosses back below +2. Entry LONG when Z crosses back above -2. Exit at Z = 0. Stop at ±3 standard deviations. 
 The Concept 
 The Z-Score is a statistical measure of how many standard deviations a value is from its mean. Applied to price, it answers precisely: "Is price far from normal, and by exactly how much?" A Z-Score of +2 means price is 2 standard deviations above the rolling mean — statistically, this occurs less than 5% of the time in a normal distribution. A Z-Score above +2 (or below -2) signals a statistically rare extreme. 

 Formula: Z-Score = (Current Price − Rolling Mean) ÷ Rolling Standard Deviation. Typical lookback: 20 periods. Unlike RSI or Stochastic which are normalized to 0–100, Z-Score values are unbounded — in extreme trending markets, Z can reach 3, 4, or higher. 

 How to Use It 

 Entry Rules 

 Short entry: Z-Score rises above +2 (extreme overbought), then CROSSES BACK BELOW +2. Enter short on the close that crosses back below +2. 

 Long entry: Z-Score falls below -2 (extreme oversold), then CROSSES BACK ABOVE -2. Enter long on the close that crosses back above -2. 

 Trend filter: Require the 50-period MA to be flat or declining for short entries, flat or rising for long entries. Avoid trading reversions directly against a strong trend. 

 Z-Score divergence (advanced): Price makes a new extreme (new high) but Z-Score makes a lower high — momentum is weakening. This is the statistical equivalent of RSI divergence and a stronger signal. 

 Stop Loss and Exit 

 Stop loss: If Z-Score reaches ±3 in the wrong direction, exit. A Z above +3 means you are fighting an unusual momentum event — stand aside. 

 Primary exit: Z-Score returns to 0 (price is back at its rolling mean). This is the mathematical target. 

 Conservative exit: Z-Score reaches ±0.5 (close enough to mean to take profit early). 

 Worked Example 
 A stock's 20-day rolling mean is ₹450. Rolling standard deviation is ₹15. Current price = ₹482. Z-Score = (482 − 450) ÷ 15 = +2.13. Z has crossed above +2. Next day, price closes at ₹478. Z-Score = (478 − 450) ÷ 15 = +1.87 — crosses back below +2. Short entry at ₹478. Stop: Z reaches +3, i.e. price at 450 + (3×15) = ₹495. Stop at ₹496. Target: Z = 0, price = ₹450. Exit at ₹452. Profit: ₹26 on an ₹18 risk. 

 Common Mistakes 

 Assuming price is always normally distributed — in trending markets, Z-Score can stay above +2 for extended periods. Always use the trend filter. 

 Not recalculating the mean and standard deviation on a rolling basis — static levels become stale quickly. The lookback must roll forward with each new bar. 

 Confusing Z-Score with RSI — both use extreme thresholds, but Z-Score is unbounded while RSI caps at 0 and 100. Z-Score above +4 is possible in extreme moves; RSI cannot exceed 100.
