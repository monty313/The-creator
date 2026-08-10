# Strategy 8: BOLLINGER BAND MEAN REVERSION

**family profile key:** guide_s08_bb_mr  
**slug:** s08_bb_mean_reversion  
**kind:** note / educational guide  
**Source HTML:** strategies/Strategies to replicate in Algo Trading.docx.html  
**Source URL (saved from):** https://docs.google.com/document/u/0/d/1j7bEX0znMD0YhcpR3oijKIzX8qBj3-lX/mobilebasic  
**Class:** mean reversion  
**Not Court law.** Language-only inventory for lab adapters under 2HTF+1LTF · 4 sets · PB+cont.

---

## Guide language (extracted)

STRATEGY 8 
 BOLLINGER BAND MEAN REVERSION 
 Price touching the outer band signals statistical excess — the close back inside is the trigger 

 Diagram 8 — Short entry: price touches upper band, then closes back inside (confirmation). Long entry: price touches lower band, then closes back inside. SL outside the band. Target: middle band (20 MA). 
 The Concept 
 Bollinger Bands place an upper and lower band at 2 standard deviations above and below a 20-period moving average. Statistically, approximately 95% of price closes occur inside the bands. When price touches the outer band, it has moved to a statistically extreme zone. The mean reversion trade bets that price will return to the middle band (the 20 MA). 

 Critical distinction: touching the band is not the entry signal. Price can ride the outer band for several bars during a strong trend. The entry triggers only when price closes BACK INSIDE the band — confirming the rejection of the extreme level. 

 How to Use It 

 Entry Rules 

 Short setup: Price touches or closes above the upper band. Wait for the NEXT candle to close back inside the band. That close is the short entry. 

 Long setup: Price touches or closes below the lower band. Wait for the NEXT candle to close back inside the lower band. That close is the long entry. 

 Add a trend filter: Only take counter-trend trades (short at upper band in a downtrend; long at lower band in an uptrend). Or use the ADX to confirm the market is ranging (ADX below 25) before trading reversions. 

 Squeeze bonus: When the bands contract to their narrowest point in 20+ bars (the "Bollinger Squeeze"), an explosive move is imminent. The direction of the break is the trend trade — not a reversion. Do not fade squeezes. 

 Stop Loss and Exit 

 Stop loss: Place just outside the band that was touched. For a short from the upper band, stop above the upper band. For a long from the lower band, stop below the lower band. 

 Primary target: The middle band (20-period MA). This is the statistical "fair value" the bands are built around. 

 Extended target: The opposite band — use only in strongly ranging markets with clear support/resistance. 

 Exit early if: Price fails to reach the middle band within 5–7 bars and starts retreating — the reversion has lost momentum. 

 Worked Example 
 A stock is ranging. The upper Bollinger Band sits at ₹540. Price spikes to ₹543 — touching the upper band — but closes the candle at ₹532, back inside the band. Short entry at ₹532. Upper band = ₹540, stop at ₹542. Middle band (20 MA) = ₹498. Target: ₹498. Over the next 5 days price drifts down to ₹500. Exit: ₹500. Profit: ₹32 on a ₹10 risk (3.2:1 RR). 

 Common Mistakes 

 Shorting every touch of the upper band — in a strong uptrend, price can walk along the upper band for many bars. Always require the close back inside. 

 Using the opposite band as the target in a trending market — in a downtrend, price may not reach the upper band before reversing again. 

 Ignoring the band width — very wide bands after a spike mean the standard deviation is elevated. The statistical edge weakens in high-volatility regimes.
