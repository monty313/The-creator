# Strategy 3: DONCHIAN CHANNEL — TURTLE TRADING

**family profile key:** guide_s03_donchian_turtle  
**slug:** s03_donchian_turtle  
**kind:** note / educational guide  
**Source HTML:** strategies/Strategies to replicate in Algo Trading.docx.html  
**Source URL (saved from):** https://docs.google.com/document/u/0/d/1j7bEX0znMD0YhcpR3oijKIzX8qBj3-lX/mobilebasic  
**Class:** trend following  
**Not Court law.** Language-only inventory for lab adapters under 2HTF+1LTF · 4 sets · PB+cont.

---

## Guide language (extracted)

STRATEGY 3 
 DONCHIAN CHANNEL — TURTLE TRADING 
 The systematic trend system that made millionaires in the 1980s, still effective today 

 Diagram 3 — Donchian Channel: the green upper band is the 20-period high, the red lower band is the 20-period low. Entry when price breaks above the upper band. Exit when price breaks below the 10-period low (shown in orange). 
 The Concept 
 The Donchian Channel, popularised by the legendary Turtle Traders experiment of the 1980s, tracks the highest high and lowest low over a defined lookback period. When price makes a new N-period high, it signals that buyers have overcome every seller from the past N periods — a structurally bullish signal. The system uses two channel lengths: a longer one for entries, and a shorter one for exits, so the trade has room to breathe. 

 How to Use It 

 Entry Rules 

 Draw the 20-period Donchian Channel (20-period high as upper band, 20-period low as lower band). 

 Long entry: Price closes above the upper band (20-period high). This is a new 20-bar high. 

 Short entry: Price closes below the lower band (20-period low). This is a new 20-bar low. 

 Skip the trade if the previous breakout in the same direction was profitable — Turtle System 1 rule. This filters overextended trends. 

 Position size: risk 1–2% of account per trade using ATR-based sizing. 

 Stop Loss and Exit 

 Initial stop loss: 2× ATR below the entry price (long trades). This accounts for normal volatility without premature exit. 

 Exit trigger: Price closes below the 10-period low (for long trades). This is a faster exit channel than the entry. 

 The 10-period exit is deliberately tighter than the 20-period entry — it prevents giving back excessive profit if the trend reverses. 

 Trail the stop: never widen the stop. Only move it in the direction of the trade, never against. 

 Worked Example 
 Crude oil has been ranging. The 20-day high is $82.00. Price closes at $82.40 — long entry triggered. ATR = $1.50. Initial stop = $82.40 − (2 × $1.50) = $79.40. 10-day low = $80.00 at entry. Over the next 4 weeks oil rallies to $91.00 and the 10-day low has risen to $87.50. Price then drops through $87.50 — exit at $87.50. Profit: $87.50 − $82.40 = $5.10 per barrel on a $3.00 initial risk. 

 Common Mistakes 

 Using the same channel for both entry and exit — the asymmetric system (20-period entry, 10-period exit) is deliberate. Both the same defeats the purpose. 

 Ignoring position sizing — the Turtle system uses ATR-based sizing specifically because risk is variable. Fixed lot sizing destroys the edge. 

 Exiting too early on the first pullback inside the 10-period low zone — wait for an actual close below it.
