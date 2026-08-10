# Strategy 9: RSI OVERSOLD / OVERBOUGHT REVERSION

**family profile key:** guide_s09_rsi_mr  
**slug:** s09_rsi_reversion  
**kind:** note / educational guide  
**Source HTML:** strategies/Strategies to replicate in Algo Trading.docx.html  
**Source URL (saved from):** https://docs.google.com/document/u/0/d/1j7bEX0znMD0YhcpR3oijKIzX8qBj3-lX/mobilebasic  
**Class:** mean reversion  
**Not Court law.** Language-only inventory for lab adapters under 2HTF+1LTF · 4 sets · PB+cont.

---

## Guide language (extracted)

STRATEGY 9 
 RSI OVERSOLD / OVERBOUGHT REVERSION 
 The most used oscillator — but the entry is on the EXIT from the extreme zone, not the entry into it 

 Diagram 9 — RSI panel below price. Long entry when RSI crosses back above 30 (exits oversold). Short entry when RSI crosses back below 70 (exits overbought). SL at recent swing extreme. 
 The Concept 
 The RSI (Relative Strength Index) measures the speed and magnitude of recent price changes, scaled from 0 to 100. Above 70 signals overbought conditions — the stock has risen too fast relative to recent history. Below 30 signals oversold — it has fallen too fast. The mean reversion trade uses these extremes as setup zones, entering when the RSI exits the zone and momentum is shifting back. 

 How to Use It 

 Entry Rules 

 Long entry: RSI falls below 30 (enters oversold zone), then CROSSES BACK ABOVE 30. Entry on the bar that crosses back above 30. 

 Short entry: RSI rises above 70 (enters overbought zone), then CROSSES BACK BELOW 70. Entry on the bar that crosses back below 70. 

 Stronger signal — RSI divergence: Price makes a new low but RSI makes a HIGHER low (bullish divergence). This shows selling momentum is weakening even as price falls. Much higher probability than a simple 30/70 cross. 

 Trend filter: Do NOT trade RSI reversions against the dominant trend. In a strong downtrend (price below 200 MA), skip long entries at RSI 30 — wait for price to be in a neutral or bullish context first. 

 Two-period RSI variation: RSI(2) uses a 2-period lookback, generating more frequent signals. Oversold below 10, overbought above 90. More active, requires tighter risk management. 

 Stop Loss and Exit 

 Stop loss: Below the most recent swing low (for longs). This is the price level that invalidates the reversion thesis. 

 Exit: RSI reaches 50 (the midpoint) for a conservative exit, or RSI reaches 70 (the opposite extreme) for a full reversion hold. 

 For short trades: stop above the most recent swing high. Exit at RSI 50 or RSI 30. 

 Time stop: If RSI fails to return toward 50 within 8–10 bars, consider exiting — the reversion has stalled. 

 Worked Example 
 A commodity ETF has been selling off. RSI drops to 22 — deeply oversold. Three days later, RSI crosses back above 30 (now at 31). Long entry at the close: ₹185. Recent swing low = ₹178 — stop at ₹176. RSI target: 50 (midline). Price rises over the next 8 days. RSI reaches 52. Price has risen to ₹198. Exit: ₹198. Profit: ₹13 on a ₹9 risk. 

 Common Mistakes 

 Entering the moment RSI touches 30 or 70 — in a strong trend, RSI can stay pinned in extreme territory for many bars. Wait for the cross BACK through the threshold. 

 Ignoring RSI divergence — a simple RSI 30 touch without divergence is far weaker than one where price also makes a lower low while RSI makes a higher low. 

 Using RSI(14) for intraday trading on 1-min charts — RSI is noisy on very short timeframes. Use 15-min or higher for mean reversion work.
