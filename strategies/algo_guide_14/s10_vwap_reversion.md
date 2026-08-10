# Strategy 10: VWAP REVERSION (Intraday)

**family profile key:** guide_s10_vwap_mr  
**slug:** s10_vwap_reversion  
**kind:** note / educational guide  
**Source HTML:** strategies/Strategies to replicate in Algo Trading.docx.html  
**Source URL (saved from):** https://docs.google.com/document/u/0/d/1j7bEX0znMD0YhcpR3oijKIzX8qBj3-lX/mobilebasic  
**Class:** mean reversion  
**Not Court law.** Language-only inventory for lab adapters under 2HTF+1LTF · 4 sets · PB+cont.

---

## Guide language (extracted)

STRATEGY 10 
 VWAP REVERSION (Intraday) 
 The institutional anchor — professional money clusters around VWAP, price regularly snaps back to it 

 Diagram 10 — Intraday price chart with VWAP (yellow) and ±1σ bands. Short when price is far above VWAP+1σ with a rejection candle. Long when price is far below VWAP-1σ with a bounce candle. Target: VWAP itself. 
 The Concept 
 VWAP (Volume Weighted Average Price) is the average price at which every share has traded throughout the day, weighted by volume. Institutional investors — pension funds, mutual funds, algorithms — use VWAP as a benchmark. Large buy orders get executed near VWAP because executing above it is considered inefficient. This creates a natural gravitational pull: when price deviates significantly from VWAP, institutional order flow tends to bring it back. 

 VWAP resets to zero at the start of each trading day. It is fundamentally an intraday tool — do not use the daily VWAP for swing or position trades. On a standard candlestick chart, VWAP appears as a single line; on a VWAP band chart, 1σ and 2σ bands also appear, showing statistically significant deviation zones. 

 How to Use It 

 Entry Rules 

 Short setup: Price is trading significantly above VWAP (ideally above the +1σ band). A bearish rejection candle appears — a shooting star, bearish engulfing, or a candle closing below its open after touching the high. Enter short on the close of that candle. 

 Long setup: Price is trading significantly below VWAP (ideally below the -1σ band). A bullish reversal candle appears — a hammer, bullish engulfing, or a candle closing above its open after touching the low. Enter long on the close. 

 Time context: VWAP trades are strongest in the first 1–2 hours of the session and after lunch. Avoid the final 30 minutes — price often distorts due to institutional end-of-day rebalancing. 

 Volume confirmation: The reversal candle should show above-average volume. A quiet, low-volume rejection near VWAP lacks conviction. 

 Stop Loss and Exit 

 Stop loss: Above the session high (for shorts), below the session low (for longs), OR a fixed ATR-based stop above/below the entry candle. 

 Primary target: VWAP itself. This is where institutional benchmark execution concentrates. 

 Extended target: The opposite σ band (e.g. entering at +1σ, target -1σ) — only in range-bound sessions. 

 Time-based exit: Close the trade before the final 15 minutes of the session regardless of profit/loss — end-of-day flows are unpredictable. 

 Worked Example 
 At 10:15 AM, NIFTY futures open sharply higher and trade at 22,450 — 120 points above the VWAP of 22,330. The +1σ band sits at 22,400. A shooting star candle prints at 22,455. Short entry at 22,450. Stop above the session high of 22,480. Target: VWAP at 22,330. By 11:45 AM NIFTY drifts back to 22,335. Exit: 22,335. Profit: 115 points on a 30-point risk. 

 Common Mistakes 

 Trading VWAP reversion in a strong trending session — on a trend day, price diverges from VWAP all day and never comes back. Identify trend days early (price opens above VWAP and stays there with no return within the first hour) and switch to trend-following approaches. 

 Ignoring the session open time — VWAP at 9:32 AM is statistically meaningless because only a few minutes of data have accumulated. Wait until at least 9:45–10:00 AM for VWAP to be meaningful. 

 Using VWAP as a swing trade indicator — it resets daily. It has no relevance beyond the current session.
