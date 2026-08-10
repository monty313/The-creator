# Strategy 6: PARABOLIC SAR TRAILING SYSTEM

**family profile key:** guide_s06_psar  
**slug:** s06_parabolic_sar  
**kind:** note / educational guide  
**Source HTML:** strategies/Strategies to replicate in Algo Trading.docx.html  
**Source URL (saved from):** https://docs.google.com/document/u/0/d/1j7bEX0znMD0YhcpR3oijKIzX8qBj3-lX/mobilebasic  
**Class:** trend following  
**Not Court law.** Language-only inventory for lab adapters under 2HTF+1LTF · 4 sets · PB+cont.

---

## Guide language (extracted)

STRATEGY 6 
 PARABOLIC SAR TRAILING SYSTEM 
 Automatic trailing stop that accelerates as the trend matures — never gives back all the profit 

 Diagram 6 — Green SAR dots below price = uptrend (long position held). Red SAR dots above price = downtrend (short or flat). The flip point is the simultaneous exit and reversal signal. 
 The Concept 
 The Parabolic SAR (Stop and Reverse) places a trailing stop that moves closer to price over time as the trend matures, using an Acceleration Factor (AF). The stop starts far from price and accelerates toward it each time the price makes a new extreme in the trend direction. When price touches the SAR dot, the trade exits and a new trade in the opposite direction is immediately initiated. The system is always in the market — either long or short. 

 Key parameter: AF starts at 0.02, increments by 0.02 each time a new high (for longs) is made, up to a maximum of 0.20. A higher AF maximum makes the system tighter and more sensitive; a lower maximum gives more room. 

 How to Use It 

 Entry Rules 

 Long entry: SAR dot flips from ABOVE price to BELOW price. The SAR has shifted from tracking a downtrend to tracking an uptrend. 

 Short entry: SAR dot flips from BELOW price to ABOVE price. 

 Best used in combination with a trend filter (e.g. ADX above 25, or price above the 200 MA). In ranging markets, SAR flips constantly and generates losses. 

 Daily charts are the most reliable timeframe. On intraday charts, SAR whipsaws frequently in sideways sessions. 

 Stop Loss and Exit 

 The SAR dot IS the stop loss. No separate stop is needed — the system defines it automatically. 

 For the first few bars after entry, the SAR dot may be far from price — this is the widest risk point. Size position accordingly. 

 Exit: price touches or closes through the SAR dot on the other side. The dot flips, signalling a new trade in the opposite direction. 

 Partial use: many traders use SAR as a trailing stop only (not as an entry signal) for existing trend positions. 

 Worked Example 
 EUR/USD breaks out of a range. SAR flips below price at 1.0850. AF starts at 0.02. Over 10 days the pair rallies to 1.1020, making new highs on days 2, 4, 7, and 9. AF has stepped up to 0.10. SAR dot is now at 1.0940 and accelerating. On day 11, EUR/USD pulls back to 1.0935 — SAR at 1.0938. Price touches the dot. Exit at 1.0938. Total gain: 88 pips. The SAR dot flips above price — system goes short simultaneously. 

 Common Mistakes 

 Using Parabolic SAR in sideways markets — it is designed for trending conditions only. In a range, it flips almost every other bar. 

 Ignoring position sizing at entry — the initial SAR dot may be 3–4 ATRs away from price. Trading full size with a distant stop risks a large loss on the first reversal. 

 Treating every SAR flip as a trade signal — use a trend filter. Only trade SAR flips that align with the dominant trend direction.
