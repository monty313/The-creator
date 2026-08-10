# Strategy 14: WILLIAMS %R EXTREME REVERSION

**family profile key:** guide_s14_willr_mr  
**slug:** s14_williams_r_reversion  
**kind:** note / educational guide  
**Source HTML:** strategies/Strategies to replicate in Algo Trading.docx.html  
**Source URL (saved from):** https://docs.google.com/document/u/0/d/1j7bEX0znMD0YhcpR3oijKIzX8qBj3-lX/mobilebasic  
**Class:** mean reversion  
**Not Court law.** Language-only inventory for lab adapters under 2HTF+1LTF · 4 sets · PB+cont.

---

## Guide language (extracted)

STRATEGY 14 
 WILLIAMS %R EXTREME REVERSION 
 Similar to Stochastic but inverted — favored for its simplicity and sensitivity to short-term extremes 

 Diagram 14 — Williams %R (0 to -100 scale, inverted). Above -20 = overbought (short zone). Below -80 = oversold (long zone). Entry on exit from the zone. Key note: the scale is inverted — this confuses many traders. 
 The Concept 
 Williams %R, developed by Larry Williams, measures where price closed relative to the highest high over the lookback period. The critical difference from Stochastic: the scale runs from 0 to -100 (inverted). A reading of 0 means the close was at the highest high of the period — extremely overbought. A reading of -100 means the close was at the lowest low — extremely oversold. Above -20 is the overbought zone (trade short). Below -80 is the oversold zone (trade long). 

 Formula: %R = (Highest High − Close) ÷ (Highest High − Lowest Low) × -100. Typical lookback: 14 periods. Because the scale is inverted relative to RSI and Stochastic, it trips up many traders who come to it from those indicators. Always verify which end of the scale is overbought before placing a trade. 

 How to Use It 

 Entry Rules 

 Short entry: %R rises above -20 (enters overbought zone). Wait for %R to drop back BELOW -20 (exit the zone). Enter short on that bar's close. 

 Long entry: %R drops below -80 (enters oversold zone). Wait for %R to rise back ABOVE -80 (exit the zone). Enter long on that bar's close. 

 Momentum burst setup: %R rapidly moves from -80 to above -20 in 5 or fewer bars — this signals a powerful momentum burst. Trade the direction of the burst (trend follow), not the reversion. The speed of the move matters. 

 Larry Williams confirmation rule: Require price itself to confirm — after %R exits the overbought zone, the next candle should close lower than the previous close. After %R exits oversold, the next candle should close higher. 

 Setting: Standard is 14-period. For more sensitive signals use 10-period; for smoother signals use 20-period. 

 Stop Loss and Exit 

 Stop loss: Above the highest high of the lookback period (for shorts). This is the level that defines the "overbought" reading — if it breaks, the thesis is wrong. 

 Stop loss for longs: Below the lowest low of the lookback period. 

 Primary exit: %R returns to -50 (the midpoint — price closed at the midpoint of its recent range). 

 Extended exit: %R reaches the opposite zone (-80 for shorts, -20 for longs). 

 Worked Example 
 A stock has been rallying hard. Williams %R (14) rises to -8, entering the overbought zone above -20. Two days later, %R drops to -22, crossing back below -20. The candle also closes lower than the prior close (Larry Williams confirmation). Short entry at ₹345. 14-period highest high = ₹350 — stop at ₹352. %R target at -50 corresponds to ₹328 based on the current range. Price declines to ₹330 as %R reaches -55. Exit: ₹330. Profit: ₹15 on a ₹7 risk. 

 Common Mistakes 

 Getting the overbought/oversold direction backwards — above -20 is OVERBOUGHT (short). Below -80 is OVERSOLD (long). This is the single most common mistake with Williams %R because it is the opposite of every other oscillator. 

 Entering as soon as %R enters the extreme zone rather than waiting for it to exit — %R can stay above -20 for many bars during a strong trend. The exit from the zone is the signal. 

 Not combining with a trend filter — Williams %R generates frequent signals. In a trending environment, the majority of counter-trend signals will fail. Always know the bigger picture before fading an extreme. 

 When to Use Trend Following vs Mean Reversion 
 The single most important decision in applying these strategies is choosing which type fits the current market environment. Using a mean reversion strategy in a strong trend will result in a series of losses. Using a trend following strategy in a range-bound market will produce the same outcome. 

 Condition 
 Trend Following 
 Mean Reversion 

 ADX above 25 and rising 
 Favorable 
 Avoid 

 ADX below 20 (ranging) 
 Avoid 
 Favorable 

 New 52-week high / low 
 Favorable (breakout) 
 Caution — may continue 

 RSI at extremes in ranging market 
 Skip 
 Favorable 

 Price riding Bollinger upper band for 5+ bars 
 Favorable (strong trend) 
 Avoid fading 

 RSI divergence present 
 Watch for reversal 
 Favorable with confirmation 

 Major news / earnings session 
 Unpredictable — reduce size 
 Unpredictable — reduce size 

 © Trading Education Series  ·  Part 1: Trend Following        Page  of
