# Strategy 5: MOMENTUM / RATE OF CHANGE (ROC)

**family profile key:** guide_s05_roc  
**slug:** s05_roc_momentum  
**kind:** note / educational guide  
**Source HTML:** strategies/Strategies to replicate in Algo Trading.docx.html  
**Source URL (saved from):** https://docs.google.com/document/u/0/d/1j7bEX0znMD0YhcpR3oijKIzX8qBj3-lX/mobilebasic  
**Class:** trend following  
**Not Court law.** Language-only inventory for lab adapters under 2HTF+1LTF · 4 sets · PB+cont.

---

## Guide language (extracted)

STRATEGY 5 
 MOMENTUM / RATE OF CHANGE (ROC) 
 Trade the speed of price — buy what is accelerating, avoid what is decelerating 

 Diagram 5 — Price line with ROC oscillator below. Long entry when ROC crosses above zero (momentum turns positive). Exit when ROC crosses back below zero. Peak momentum zone identified where ROC is highest. 
 The Concept 
 Momentum measures how fast price is moving, not just which direction. A price moving up at increasing speed has more buying energy than a price moving up slowly. The Rate of Change (ROC) calculates the percentage change in price over N bars — if price today is higher than it was 12 days ago, ROC is positive. When ROC crosses from negative to positive, recent momentum has flipped bullish. The ROC strategy trades the direction of that momentum flip. 

 Formula: ROC = (Current Close − Close N bars ago) ÷ Close N bars ago × 100. A 12-period ROC on daily bars measures momentum over approximately 2.5 weeks. 

 How to Use It 

 Entry Rules 

 Long entry: ROC (12-period on daily) crosses ABOVE zero from below. This means price today is higher than 12 days ago for the first time after a negative period. 

 Add a trend filter: only take long entries when price is above its 50-period MA. This prevents buying momentum bounces in a downtrend. 

 Stronger signal: ROC crosses zero AND is still accelerating (the ROC line is sloping steeply upward, not flattening). 

 Short entry: ROC crosses BELOW zero, price below 50-period MA. 

 Stop Loss and Exit 

 Exit long: ROC crosses back below zero (momentum has turned negative again). 

 Stop loss: below the most recent swing low at the time of entry. Do not use a percentage stop — use structure. 

 If ROC peaks and starts turning back toward zero while price is still near highs — consider reducing position or tightening stop. ROC divergence (price making new high, ROC making lower high) is an early warning. 

 Worked Example 
 A stock has been falling for 3 weeks with ROC deeply negative at −8%. Price stabilises. ROC begins rising. On day 22, ROC crosses above zero (now +0.5%) — long entry. Price is also above its 50-day MA (trend filter passed). Entry at ₹320. Swing low at ₹295 — stop at ₹293. ROC climbs to +12% over the next month. Price reaches ₹390. ROC then peaks and crosses back below zero — exit at ₹385. Gain: ₹65 on a ₹27 risk. 

 Common Mistakes 

 Trading ROC crossovers without a trend filter — in choppy markets, ROC oscillates through zero constantly, generating dozens of losing trades. 

 Using ROC alone without any price-action confirmation — a short-term momentum flip (12-period) against a strong longer-term trend usually resolves as a reversion, not a new trend. 

 Not accounting for the lookback period — a 3-period ROC is extremely noisy; a 25-period ROC is very slow. 12–14 periods is the practical sweet spot for daily charts.
