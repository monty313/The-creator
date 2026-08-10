# Strategy 7: EMA RIBBON — MULTIPLE MA TREND SURFING

**family profile key:** guide_s07_ema_ribbon  
**slug:** s07_ema_ribbon  
**kind:** note / educational guide  
**Source HTML:** strategies/Strategies to replicate in Algo Trading.docx.html  
**Source URL (saved from):** https://docs.google.com/document/u/0/d/1j7bEX0znMD0YhcpR3oijKIzX8qBj3-lX/mobilebasic  
**Class:** trend following  
**Not Court law.** Language-only inventory for lab adapters under 2HTF+1LTF · 4 sets · PB+cont.

---

## Guide language (extracted)

STRATEGY 7 
 EMA RIBBON — MULTIPLE MA TREND SURFING 
 A stack of EMAs that shows trend health at a glance — fanned = trend, bunched = avoid 

 Diagram 7 — Left: EMAs bunched together (choppy, no trade). Right: EMAs fanned and stacked in order (8 > 13 > 21 > 34 > 55), all sloping up — strong trend confirmed. Entry on pullback to the ribbon. 
 The Concept 
 The EMA Ribbon uses a sequence of exponential moving averages (typically 8, 13, 21, 34, and 55 periods — Fibonacci-based) plotted simultaneously. When all EMAs are stacked in order (fastest on top for uptrends) and fanned apart, the trend is confirmed and accelerating. When the EMAs are bunched together or tangled, the market is directionless. The ribbon provides an immediate visual read of trend health that a single MA cannot. 

 How to Use It 

 Entry Rules 

 Bullish setup: 8 EMA > 13 EMA > 21 EMA > 34 EMA > 55 EMA, all sloping upward, and price above all of them. 

 Entry timing: wait for price to pull back and touch the upper ribbon (the 8 or 13 EMA). Enter when price bounces off the ribbon — this is "surfing the ribbon." 

 Aggressive entry: enter immediately when the ribbon fans out and stacks in order for the first time after a period of being bunched. 

 Bearish setup: 8 EMA < 13 EMA < 21 EMA < 34 EMA < 55 EMA, all sloping downward, price below all of them. Short on bounces into the ribbon from below. 

 Stop Loss and Exit 

 Stop loss: a daily CLOSE below the 55 EMA (the slowest EMA, the bottom of the ribbon). This is the structural support of the trend. 

 Exit signal: the ribbon begins to bunch up again (the 8 EMA starts converging toward the 21 EMA). This means trend momentum is fading. 

 Strong trend management: add to the position on each successful pullback to the ribbon as long as the stack order is maintained. 

 Worked Example 
 A growth stock has been rallying. The EMAs fan into perfect bullish order: 8 EMA = ₹520, 13 EMA = ₹512, 21 EMA = ₹502, 34 EMA = ₹490, 55 EMA = ₹478. Price pulls back to ₹515, touching the 8 EMA. Bullish candle appears — entry at ₹517. Stop at a daily close below ₹478 (55 EMA). Over the next 3 weeks price reaches ₹590. The ribbon begins to bunch — 8 EMA converges toward 21 EMA. Exit at ₹582. Gain: ₹65 per share on a ₹39 initial risk. 

 Common Mistakes 

 Entering when the ribbon is bunched — a messy, tangled ribbon means no trend. Wait for the ribbon to fan out clearly. 

 Using random MA periods instead of a sequence — the Fibonacci sequence (8, 13, 21, 34, 55) matters because these intervals are naturally spaced and observed by many market participants. 

 Setting the stop too tight inside the ribbon instead of below the 55 EMA — price regularly touches the 8 EMA during pullbacks. That is normal. Only a close below the 55 EMA is structurally significant. 

 What Is Mean Reversion? 
 Mean reversion is the tendency of prices to return to their historical average after an extreme move. When a stock or index moves significantly above or below its recent average — whether measured by a moving average, a statistical band, or an oscillator — there is a statistical tendency for that deviation to correct. Mean reversion traders sell into unusual strength and buy into unusual weakness, betting on the return to equilibrium. 

 Mean reversion is the structural opposite of trend following. A trend follower buys a new 20-day high expecting the move to continue. A mean reversion trader sells a new 20-day high expecting the move to exhaust and reverse. Both can be profitable — the key is knowing which market environment favors which approach. 

 💡 
 Mean reversion works best in range-bound, low-trend markets (ADX below 25). In a strong trending market, "oversold" can get much more oversold. Always check the broader trend context before fading an extreme. 

 ⚠️ 
 The most dangerous mistake in mean reversion: treating every extreme as a reversion opportunity. Some extremes are the START of a new trend. The strategies in this section include specific filters to distinguish the two — use them.
