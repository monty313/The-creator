//+------------------------------------------------------------------+
//|                                            FTMO_Sentinel_EA.mq5  |
//|  The Creator — Evidence Court lab · EXPERIMENTAL (not Court law) |
//|                                                                  |
//|  Geometry (from strategies/ corpus, measured winners):           |
//|    Permission : dual-HTF CCI M-line force (+ Mark BB mass)       |
//|    Timing     : reclaim-only fire (load -> cross back through 0) |
//|                 Engine A = CCI gravity M-line (corpus MC rank 13,|
//|                 P(loss)=0%) · Engine B = McFlurry RSI eddy H001  |
//|    Shell      : session 07-21 · bar confirm · micro structure    |
//|                 · spread cap  (accuracy layer, 125/125 families) |
//|    Exits      : first-breath barriers (tight TP / wider SL,      |
//|                 no time-stop thrash)                             |
//|                                                                  |
//|  Day Governor (FTMO rails):                                      |
//|    * bank the day at +DailyGoal (default 2.5%) and stop          |
//|    * ratchet: once day >= trigger, a profit floor trails the     |
//|      day peak -> a green day can never close red                 |
//|    * soft halt -1.5% / hard flatten -2.0% (FTMO limit is -5%)    |
//|    * per-trade risk auto-capped so one loss can never cross      |
//|      the daily budget · loss-streak halving · house-money boost  |
//|    * total-DD fuse at -6% (FTMO limit -10%) -> permanent halt    |
//|    * challenge manager: stop at +10%, ticket-trades until the    |
//|      minimum trading days are registered                         |
//|                                                                  |
//|  MEASURED VERDICT (2026-08-12, see VALIDATION.md v3):            |
//|    * Governor safety VALIDATED on real M1: worst day -1.5%,      |
//|      zero FTMO breaches in every window/symbol/variant.          |
//|    * Engine D Keltner fade (DEFAULT): cross-symbol validated —   |
//|      positive on both time splits on real EURUSD (7mo) AND real  |
//|      GBPUSD M1, strength lot-sizing. European pairs only.        |
//|    * Engine C London ORB: EURUSD-only evidence (train +6.1%,     |
//|      test +14.4%, robust neighborhood) — failed GBPUSD/USDJPY.   |
//|      Attach only on EURUSD as a second leg (own magic number).   |
//|    * Corpus reclaim engines (A/B): FAILED validation, lab only.  |
//|    * Measured portfolio (fade EUR+GBP + ORB EUR): +49.9%/7mo,    |
//|      mean day +0.27%, 0 breaches, 66% of challenge starts pass   |
//|      (median 24 trading days). NOT "+2.5% every day", NOT "pass  |
//|      every time" — those remain physically unguaranteeable.      |
//|      Forward-test on demo before any funded attempt.             |
//+------------------------------------------------------------------+
#property copyright "The Creator lab"
#property version   "1.00"
#property strict

#include <Trade/Trade.mqh>

//=== Identity ======================================================
input group    "=== Identity ==="
input long     InpMagic              = 250812;        // Magic number
input string   InpComment            = "FTMO_SENTINEL";

//=== FTMO challenge frame ==========================================
input group    "=== FTMO challenge frame ==="
input double   InpInitialBalance     = 0.0;    // Challenge initial balance (0 = capture on first run)
input double   InpProfitTargetPct    = 10.0;   // Challenge profit target %
input int      InpMinTradingDays     = 4;      // Minimum trading days
input double   InpMaxTotalLossPct    = 6.0;    // OUR total-loss fuse % (FTMO allows 10)
input double   InpSoftDailyStopPct   = 1.5;    // No new trades once day <= -this %
input double   InpHardDailyStopPct   = 2.0;    // Flatten everything at -this % (FTMO allows 5)
input int      InpDayResetHour       = 0;      // Server hour matching FTMO midnight CE(S)T

//=== Day Governor (the 2.5%/day engine) ============================
input group    "=== Day Governor ==="
input double   InpDailyGoalPct       = 2.5;    // Bank the day and stop at +this %
input bool     InpBankAtGoal         = true;   // Flatten + stop when daily goal reached
input double   InpRatchetTriggerPct  = 0.8;    // Arm the green-day ratchet at +this %
input double   InpRatchetFloorPct    = 0.20;   // Minimum locked day profit % once armed
input double   InpRatchetTrailRatio  = 0.60;   // Floor trails this fraction of day peak
input double   InpLadderFraction     = 0.75;   // House-money ladder: risk += frac * day profit %
input double   InpMaxRiskPct         = 2.00;   // Risk per trade ceiling % (ladder cap)

//=== Risk ==========================================================
input group    "=== Risk ==="
input double   InpRiskPct            = 0.80;   // Base risk per trade (% of initial balance; fade validated at 0.8)
input double   InpMaxLots            = 10.0;   // Absolute lot cap
input int      InpMaxTradesPerDay    = 40;     // Trade cadence cap for the day
input int      InpMaxConsecLosses    = 3;      // Stop the day after this many consecutive losses
input bool     InpLossStreakHalving  = true;   // Halve risk after each consecutive loss
input int      InpCooldownMinutes    = 8;      // Minutes between entries (per symbol)
input int      InpMaxOpenPositions   = 1;      // Simultaneous positions (this symbol+magic)

//=== Sessions / calendar ===========================================
input group    "=== Sessions / calendar ==="
input bool     InpUseSessionFilter   = true;
input int      InpSessionStartHour   = 7;      // Server hour (London open zone)
input int      InpSessionEndHour     = 21;     // Server hour (NY close zone)
input bool     InpFridayFlatten      = true;
input int      InpFridayLastEntryHour= 19;     // No new trades Friday after this hour
input int      InpFridayFlattenHour  = 21;     // Flatten Friday at this hour
input string   InpNewsBlackout       = "";     // e.g. "14:25-14:35;15:55-16:05" server time, no entries

//=== Entry mode ====================================================
enum ENUM_ENTRY_MODE { MODE_LONDON_ORB=0, MODE_CORPUS_RECLAIM=1, MODE_KELTNER_FADE=2 };
input group    "=== Entry mode ==="
input ENUM_ENTRY_MODE InpEntryMode  = MODE_KELTNER_FADE;  // fade = cross-symbol validated (VALIDATION.md v3)

//=== Engine D: Keltner fade (cross-symbol validated) ===============
input group    "=== Engine D: Keltner fade ==="
input int      InpKfEmaPeriod       = 20;      // Channel mid = EMA(this)
input double   InpKfMult            = 2.0;     // Channel width = mult * ATR(14)
input double   InpKfTpAtr           = 1.5;     // TP = mult * ATR
input double   InpKfSlAtr           = 2.0;     // SL = mult * ATR
input bool     InpKfH4Filter        = true;    // Skip fades against a strong H4 trend
input bool     InpKfStrengthSizing  = true;    // Risk scales with stretch beyond the band

//=== Engine C: London opening-range breakout (validated) ===========
input group    "=== Engine C: London ORB ==="
input int      InpOrbRangeEndHour    = 7;      // Overnight range = day start .. this hour (server; align to 07 UTC)
input int      InpOrbEntryUntilHour  = 12;     // Breakouts accepted until this hour
input double   InpOrbTpMult          = 1.25;   // TP = mult * range height
input bool     InpOrbStopAtMid       = true;   // SL at range mid (measured better than far side)
input double   InpOrbMinHeightAtr    = 1.0;    // Range must exceed this * ATR(14)
input double   InpOrbMinSlAtr        = 0.2;    // Skip if SL distance below this * ATR
input double   InpOrbRiskPct         = 1.00;   // One-shot risk per trade % (per side per day)

//=== Engines (corpus reclaim mode — NOT validated, kept for lab) ===
input group    "=== Engine A: CCI gravity reclaim ==="
input bool     InpUseEngineCCI       = true;
input int      InpCciPeriod          = 20;
input double   InpCciForceThreshold  = 8.0;    // |M| floor on HTF1 (genuine force)
input int      InpLoadLookback       = 8;      // Bars of load before reclaim counts

input group    "=== Engine B: McFlurry RSI eddy (H001) ==="
input bool     InpUseEngineMcFlurry  = false;  // measured worse than Engine A (VALIDATION.md)
input int      InpMcfRsiPeriod       = 13;
input double   InpMcfForceThreshold  = 1.5;    // |M| floor on HTF1

input group    "=== Mark doctrine gates ==="
input bool     InpRequireMarkMass    = true;   // close vs BB(100,0.5,+2) mid on BOTH HTFs
input bool     InpUseMarkTiming      = false;  // extra: RSI(5) + BB-on-RSI release cross
input int      InpMarkRsiPeriod      = 5;
input int      InpMarkBbPeriod       = 10;
input double   InpMarkBbDev          = 0.5;
input int      InpMarkBbShift        = 2;
input double   InpConcurrenceBoost   = 1.25;   // Risk multiplier when both engines agree

//=== Timeframes ====================================================
input group    "=== Timeframes (2 HTF + trigger = chart TF) ==="
input ENUM_TIMEFRAMES InpHTF1        = PERIOD_H1;
input ENUM_TIMEFRAMES InpHTF2        = PERIOD_H4;

//=== Accuracy shell filters ========================================
input group    "=== Accuracy shell ==="
input bool     InpUseBarConfirm      = true;   // Entry bar close agrees with side
input bool     InpUseMicroStructure  = true;   // Higher-low (long) / lower-high (short)
input int      InpMaxSpreadPoints    = 15;

//=== Exits =========================================================
input group    "=== Exits: first-breath barriers ==="
enum ENUM_EXIT_MODE { EXIT_ATR_BARRIERS=0, EXIT_FIXED_FRACTION=1 };
input ENUM_EXIT_MODE InpExitMode     = EXIT_ATR_BARRIERS;
input int      InpAtrPeriod          = 14;
input double   InpTpAtrMult          = 0.70;   // TP = mult * ATR (first breath)
input double   InpSlAtrMult          = 2.80;   // SL = mult * ATR (thesis invalidation)
input double   InpTpFraction         = 0.00028;// EXIT_FIXED_FRACTION: TP as price fraction
input double   InpSlFraction         = 0.00115;// EXIT_FIXED_FRACTION: SL as price fraction

//=== Ticket-trade mode (min trading days after target) =============
input group    "=== Ticket trades ==="
input bool     InpTicketMode         = true;   // After target: micro-trade once/day until min days
input int      InpTicketHour         = 15;     // Fallback hour to place the ticket trade

//===================================================================
CTrade   g_trade;
int      g_hCciLtf=INVALID_HANDLE, g_hCciH1=INVALID_HANDLE, g_hCciH2=INVALID_HANDLE;
int      g_hRsiMcfLtf=INVALID_HANDLE, g_hRsiMcfH1=INVALID_HANDLE, g_hRsiMcfH2=INVALID_HANDLE;
int      g_hRsiMark=INVALID_HANDLE, g_hAtr=INVALID_HANDLE;
int      g_hEmaKf=INVALID_HANDLE, g_hAtrH4=INVALID_HANDLE;
datetime g_lastBarTime=0;
datetime g_lastEntryTime=0;
int      g_lossStreak=0;
double   g_baseline=0.0;          // challenge initial balance
long     g_dayIdx=-1;             // current governor day index
double   g_dayAnchor=0.0;         // max(balance,equity) at day reset
double   g_dayPeakPL=0.0;         // best equity excursion today (account ccy)
bool     g_dayHalted=false;       // soft/hard stop hit -> no more trades today
bool     g_dayBanked=false;       // goal/ratchet banked -> done, green
int      g_tradesToday=0;
int      g_consecLossesToday=0;
bool     g_orbFiredLong=false;    // one shot per side per day
bool     g_orbFiredShort=false;
bool     g_permHalt=false;
bool     g_challengeDone=false;
int      g_tradingDays=0;
long     g_lastCountedDay=-1;
bool     g_ticketPlacedToday=false;

//=== persistence keys =============================================
string GVKey(const string what)          { return StringFormat("FTMOSENT_%I64d_%s", InpMagic, what); }
string GVDayKey(const string what,long d){ return StringFormat("FTMOSENT_%I64d_%s_%I64d", InpMagic, what, d); }

double GVGet(const string key, double fallback)
  { return GlobalVariableCheck(key) ? GlobalVariableGet(key) : fallback; }
void   GVSet(const string key, double v) { GlobalVariableSet(key, v); }

//+------------------------------------------------------------------+
int OnInit()
{
   g_trade.SetExpertMagicNumber(InpMagic);
   g_trade.SetDeviationInPoints(20);

   g_hCciLtf = iCCI(_Symbol, PERIOD_CURRENT, InpCciPeriod, PRICE_TYPICAL);
   g_hCciH1  = iCCI(_Symbol, InpHTF1,        InpCciPeriod, PRICE_TYPICAL);
   g_hCciH2  = iCCI(_Symbol, InpHTF2,        InpCciPeriod, PRICE_TYPICAL);
   g_hRsiMcfLtf = iRSI(_Symbol, PERIOD_CURRENT, InpMcfRsiPeriod, PRICE_CLOSE);
   g_hRsiMcfH1  = iRSI(_Symbol, InpHTF1,        InpMcfRsiPeriod, PRICE_CLOSE);
   g_hRsiMcfH2  = iRSI(_Symbol, InpHTF2,        InpMcfRsiPeriod, PRICE_CLOSE);
   g_hRsiMark   = iRSI(_Symbol, PERIOD_CURRENT, InpMarkRsiPeriod, PRICE_CLOSE);
   g_hAtr       = iATR(_Symbol, PERIOD_CURRENT, InpAtrPeriod);
   g_hEmaKf     = iMA(_Symbol, PERIOD_CURRENT, InpKfEmaPeriod, 0, MODE_EMA, PRICE_CLOSE);
   g_hAtrH4     = iATR(_Symbol, PERIOD_H4, 14);

   if(g_hCciLtf==INVALID_HANDLE || g_hCciH1==INVALID_HANDLE || g_hCciH2==INVALID_HANDLE ||
      g_hRsiMcfLtf==INVALID_HANDLE || g_hRsiMcfH1==INVALID_HANDLE || g_hRsiMcfH2==INVALID_HANDLE ||
      g_hRsiMark==INVALID_HANDLE || g_hAtr==INVALID_HANDLE ||
      g_hEmaKf==INVALID_HANDLE || g_hAtrH4==INVALID_HANDLE)
     { Print("FTMO Sentinel: indicator handle failed"); return INIT_FAILED; }

   // challenge baseline: input > persisted > current balance
   g_baseline = InpInitialBalance > 0.0 ? InpInitialBalance
                                        : GVGet(GVKey("BASELINE"), AccountInfoDouble(ACCOUNT_BALANCE));
   GVSet(GVKey("BASELINE"), g_baseline);
   g_permHalt       = GVGet(GVKey("PERMHALT"), 0.0) > 0.5;
   g_challengeDone  = GVGet(GVKey("DONE"),     0.0) > 0.5;
   g_tradingDays    = (int)GVGet(GVKey("TDAYS"), 0.0);
   g_lastCountedDay = (long)GVGet(GVKey("LASTTDAY"), -1.0);

   PrintFormat("FTMO Sentinel up. baseline=%.2f permHalt=%d done=%d tradingDays=%d",
               g_baseline, g_permHalt, g_challengeDone, g_tradingDays);
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   IndicatorRelease(g_hCciLtf);  IndicatorRelease(g_hCciH1);  IndicatorRelease(g_hCciH2);
   IndicatorRelease(g_hRsiMcfLtf); IndicatorRelease(g_hRsiMcfH1); IndicatorRelease(g_hRsiMcfH2);
   IndicatorRelease(g_hRsiMark); IndicatorRelease(g_hAtr);
   IndicatorRelease(g_hEmaKf); IndicatorRelease(g_hAtrH4);
}

//=== position helpers =============================================
int OwnPositions()
{
   int n=0;
   for(int i=PositionsTotal()-1; i>=0; --i)
   {
      string sym = PositionGetSymbol(i);
      if(sym==_Symbol && PositionGetInteger(POSITION_MAGIC)==InpMagic) n++;
   }
   return n;
}

void CloseAllOwn(const string why)
{
   for(int i=PositionsTotal()-1; i>=0; --i)
   {
      string sym = PositionGetSymbol(i);
      if(sym!=_Symbol) continue;
      if(PositionGetInteger(POSITION_MAGIC)!=InpMagic) continue;
      ulong ticket = PositionGetInteger(POSITION_TICKET);
      if(!g_trade.PositionClose(ticket))
         PrintFormat("Sentinel close fail t=%I64u err=%d", ticket, GetLastError());
   }
   if(why!="") Print("Sentinel flatten: ", why);
}

//=== indicator math ===============================================
// CCI M-line: M = SMA7(SMA2(CCI)) - SMA21(SMA2(CCI)); m[0] = bar 'shift'
bool CciMLine(const int handle, const int shift, const int count, double &m[])
{
   int need = count + 21 + 2;                    // s2 chain + sma21 window
   double cci[];
   ArraySetAsSeries(cci, true);
   if(CopyBuffer(handle, 0, shift, need, cci) < need) return false;
   double s2[];
   int n2 = need - 1;
   ArrayResize(s2, n2);
   for(int i=0; i<n2; ++i) s2[i] = 0.5*(cci[i]+cci[i+1]);
   ArrayResize(m, count);
   for(int i=0; i<count; ++i)
   {
      double a7=0, a21=0;
      for(int k=0; k<7;  ++k) a7  += s2[i+k];
      for(int k=0; k<21; ++k) a21 += s2[i+k];
      m[i] = a7/7.0 - a21/21.0;
   }
   return true;
}

// McFlurry M-line: M = SMA7(RSI) - SMA21(RSI); m[0] = bar 'shift'
bool McfMLine(const int handle, const int shift, const int count, double &m[])
{
   int need = count + 21;
   double rsi[];
   ArraySetAsSeries(rsi, true);
   if(CopyBuffer(handle, 0, shift, need, rsi) < need) return false;
   ArrayResize(m, count);
   for(int i=0; i<count; ++i)
   {
      double a7=0, a21=0;
      for(int k=0; k<7;  ++k) a7  += rsi[i+k];
      for(int k=0; k<21; ++k) a21 += rsi[i+k];
      m[i] = a7/7.0 - a21/21.0;
   }
   return true;
}

// Mark mass: close[1] vs SMA100(close) mid shifted +2, on tf. +1 bull, -1 bear, 0 flat/error
int MarkMass(const ENUM_TIMEFRAMES tf)
{
   double close_[];
   ArraySetAsSeries(close_, true);
   if(CopyClose(_Symbol, tf, 0, 105, close_) < 105) return 0;
   double mid=0;
   for(int k=0; k<100; ++k) mid += close_[3+k];   // bar1 + shift(+2) -> window starts at 3
   mid /= 100.0;
   if(close_[1] > mid) return  1;
   if(close_[1] < mid) return -1;
   return 0;
}

// Mark timing: RSI(5) with BB(period,dev,shift) on the RSI series.
// ret +1 = release cross up upper band (BUY fire), -1 = cross down lower band, 0 = none
int MarkTiming()
{
   int per = InpMarkBbPeriod, sh = InpMarkBbShift;
   int need = per + sh + 3;
   double rsi[];
   ArraySetAsSeries(rsi, true);
   if(CopyBuffer(g_hRsiMark, 0, 0, need, rsi) < need) return 0;

   double up[2], lo[2];
   for(int b=1; b<=2; ++b)                        // bands at bar1 and bar2
   {
      double mean=0, var=0;
      for(int k=0; k<per; ++k) mean += rsi[b+sh+k];
      mean /= per;
      for(int k=0; k<per; ++k) { double d=rsi[b+sh+k]-mean; var += d*d; }
      double sd = MathSqrt(var/per);
      up[b-1] = mean + InpMarkBbDev*sd;
      lo[b-1] = mean - InpMarkBbDev*sd;
   }
   bool fireUp = (rsi[2] <= up[1]) && (rsi[1] > up[0]);
   bool fireDn = (rsi[2] >= lo[1]) && (rsi[1] < lo[0]);
   if(fireUp) return  1;
   if(fireDn) return -1;
   return 0;
}

//=== signal =======================================================
// dir: +1 long, -1 short, 0 none. conc set true when both engines fire together.
int Signal(bool &concurrence)
{
   concurrence = false;
   int lookback = MathMax(2, InpLoadLookback);
   int cnt = lookback + 2;

   int cciDir = 0;
   if(InpUseEngineCCI)
   {
      double mL[], mH1[], mH2[];
      if(CciMLine(g_hCciLtf, 1, cnt, mL) &&
         CciMLine(g_hCciH1,  1, 2,   mH1) &&
         CciMLine(g_hCciH2,  1, 2,   mH2))
      {
         double mn=mL[1], mx=mL[1];
         for(int i=1; i<=lookback && i<cnt; ++i) { mn=MathMin(mn,mL[i]); mx=MathMax(mx,mL[i]); }
         bool fireL = (mL[1] <= 0.0 && mL[0] > 0.0) && (mn < 0.0);   // load then reclaim up
         bool fireS = (mL[1] >= 0.0 && mL[0] < 0.0) && (mx > 0.0);   // load then reclaim down
         bool forceL = (mH1[0] > 0 && mH2[0] > 0 && mH1[0] >=  InpCciForceThreshold);
         bool forceS = (mH1[0] < 0 && mH2[0] < 0 && mH1[0] <= -InpCciForceThreshold);
         if(fireL && forceL) cciDir = 1;
         if(fireS && forceS) cciDir = -1;
      }
   }

   int mcfDir = 0;
   if(InpUseEngineMcFlurry)
   {
      double mL[], mH1[], mH2[];
      if(McfMLine(g_hRsiMcfLtf, 1, cnt, mL) &&
         McfMLine(g_hRsiMcfH1,  1, 2,   mH1) &&
         McfMLine(g_hRsiMcfH2,  1, 2,   mH2))
      {
         double mn=mL[1], mx=mL[1];
         for(int i=1; i<=lookback && i<cnt; ++i) { mn=MathMin(mn,mL[i]); mx=MathMax(mx,mL[i]); }
         bool fireL = (mL[1] <= 0.0 && mL[0] > 0.0) && (mn < 0.0);
         bool fireS = (mL[1] >= 0.0 && mL[0] < 0.0) && (mx > 0.0);
         bool forceL = (mH1[0] > 0 && mH2[0] > 0 && mH1[0] >=  InpMcfForceThreshold);
         bool forceS = (mH1[0] < 0 && mH2[0] < 0 && mH1[0] <= -InpMcfForceThreshold);
         if(fireL && forceL) mcfDir = 1;
         if(fireS && forceS) mcfDir = -1;
      }
   }

   int dir = 0;
   if(cciDir != 0 && mcfDir == cciDir) { dir = cciDir; concurrence = true; }
   else if(cciDir != 0)                 dir = cciDir;
   else if(mcfDir != 0)                 dir = mcfDir;
   if(dir == 0) return 0;

   // Mark mass gate (doctrine: both HTFs on the right side of BB mid)
   if(InpRequireMarkMass)
   {
      int m1 = MarkMass(InpHTF1), m2 = MarkMass(InpHTF2);
      if(!(m1 == dir && m2 == dir)) return 0;
   }
   // Optional Mark timing confluence
   if(InpUseMarkTiming && MarkTiming() != dir) return 0;

   // Accuracy shell: bar confirm + micro structure on the trigger TF
   MqlRates r[];
   ArraySetAsSeries(r, true);
   if(CopyRates(_Symbol, PERIOD_CURRENT, 0, 5, r) < 5) return 0;
   if(InpUseBarConfirm)
   {
      if(dir > 0 && !(r[1].close > r[1].open)) return 0;
      if(dir < 0 && !(r[1].close < r[1].open)) return 0;
   }
   if(InpUseMicroStructure)
   {
      if(dir > 0 && !(r[1].low  > r[3].low))  return 0;   // higher-low texture
      if(dir < 0 && !(r[1].high < r[3].high)) return 0;   // lower-high texture
   }
   return dir;
}

// London ORB: overnight range breakout on the closed trigger bar.
// Returns +1/-1 and fills slDist/tpDist (price distances); 0 = no fire.
int OrbSignal(double &slDist, double &tpDist)
{
   MqlDateTime now;
   TimeToStruct(TimeCurrent(), now);
   if(now.hour < InpOrbRangeEndHour || now.hour >= InpOrbEntryUntilHour) return 0;

   // bars of the current server day
   MqlDateTime ds = now;
   ds.hour = 0; ds.min = 0; ds.sec = 0;
   datetime dayStart = StructToTime(ds);
   datetime rangeEnd = dayStart + (long)InpOrbRangeEndHour*3600;
   MqlRates r[];
   ArraySetAsSeries(r, true);
   int copied = CopyRates(_Symbol, PERIOD_CURRENT, dayStart, TimeCurrent(), r);
   if(copied < 5) return 0;

   double rngHi = -DBL_MAX, rngLo = DBL_MAX;
   int nRange = 0;
   for(int i = copied-1; i >= 0; --i)          // oldest -> newest
   {
      if(r[i].time >= rangeEnd) break;
      rngHi = MathMax(rngHi, r[i].high);
      rngLo = MathMin(rngLo, r[i].low);
      nRange++;
   }
   if(nRange < 3 || rngHi <= rngLo) return 0;
   double height = rngHi - rngLo;

   double atrv[];
   ArraySetAsSeries(atrv, true);
   if(CopyBuffer(g_hAtr, 0, 1, 1, atrv) < 1 || atrv[0] <= 0) return 0;
   if(height < InpOrbMinHeightAtr*atrv[0]) return 0;   // degenerate range

   double mid = 0.5*(rngHi + rngLo);
   double c1 = r[1].close;                     // last closed bar
   int dir = 0;
   if(!g_orbFiredLong  && c1 > rngHi) dir = 1;
   if(!g_orbFiredShort && c1 < rngLo) dir = -1;
   if(dir == 0) return 0;

   slDist = InpOrbStopAtMid ? MathAbs(c1 - mid)
                            : (dir > 0 ? c1 - rngLo : rngHi - c1);
   tpDist = height*InpOrbTpMult;
   if(slDist < InpOrbMinSlAtr*atrv[0] || tpDist <= 0) return 0;
   return dir;
}

// Keltner fade: closed bar beyond EMA +/- mult*ATR, optional H4 trend veto.
// Returns +1/-1, fills barrier distances and the strength risk multiplier.
int KeltnerFadeSignal(double &slDist, double &tpDist, double &strengthMult)
{
   double ema[], atrv[];
   ArraySetAsSeries(ema, true);
   ArraySetAsSeries(atrv, true);
   if(CopyBuffer(g_hEmaKf, 0, 1, 1, ema) < 1) return 0;
   if(CopyBuffer(g_hAtr,   0, 1, 1, atrv) < 1 || atrv[0] <= 0) return 0;
   MqlRates r[];
   ArraySetAsSeries(r, true);
   if(CopyRates(_Symbol, PERIOD_CURRENT, 0, 3, r) < 3) return 0;

   double upper = ema[0] + InpKfMult*atrv[0];
   double lower = ema[0] - InpKfMult*atrv[0];
   int dir = 0;
   double stretch = 0.0;
   if(r[1].close < lower) { dir = 1;  stretch = (lower - r[1].close)/atrv[0]; }
   if(r[1].close > upper) { dir = -1; stretch = (r[1].close - upper)/atrv[0]; }
   if(dir == 0) return 0;

   if(InpKfH4Filter)
   {
      double c4[], a4[];
      ArraySetAsSeries(c4, true);
      ArraySetAsSeries(a4, true);
      if(CopyClose(_Symbol, PERIOD_H4, 1, 14, c4) < 14) return 0;
      if(CopyBuffer(g_hAtrH4, 0, 1, 1, a4) < 1 || a4[0] <= 0) return 0;
      double smaNow = 0, smaPrev = 0;
      for(int k=0; k<10; ++k) { smaNow += c4[k]; smaPrev += c4[k+3]; }
      double slope = (smaNow - smaPrev)/10.0;
      if(dir > 0 && slope < -0.5*a4[0]) return 0;   // no knife-catch in strong H4 downtrend
      if(dir < 0 && slope >  0.5*a4[0]) return 0;
   }

   slDist = atrv[0]*InpKfSlAtr;
   tpDist = atrv[0]*InpKfTpAtr;
   strengthMult = InpKfStrengthSizing ? MathMin(MathMax(1.0 + stretch, 0.5), 2.0) : 1.0;
   return dir;
}

//=== calendar / session ===========================================
bool InSession()
{
   if(!InpUseSessionFilter) return true;
   MqlDateTime dt; TimeToStruct(TimeCurrent(), dt);
   if(dt.hour < InpSessionStartHour || dt.hour >= InpSessionEndHour) return false;
   if(dt.day_of_week == 5 && dt.hour >= InpFridayLastEntryHour) return false;
   return dt.day_of_week >= 1 && dt.day_of_week <= 5;
}

bool InNewsBlackout()
{
   if(InpNewsBlackout == "") return false;
   MqlDateTime dt; TimeToStruct(TimeCurrent(), dt);
   int nowMin = dt.hour*60 + dt.min;
   string wins[];
   int n = StringSplit(InpNewsBlackout, ';', wins);
   for(int i=0; i<n; ++i)
   {
      string parts[];
      if(StringSplit(wins[i], '-', parts) != 2) continue;
      string a[], b[];
      if(StringSplit(parts[0], ':', a) != 2 || StringSplit(parts[1], ':', b) != 2) continue;
      int from = (int)StringToInteger(a[0])*60 + (int)StringToInteger(a[1]);
      int to   = (int)StringToInteger(b[0])*60 + (int)StringToInteger(b[1]);
      if(nowMin >= from && nowMin <= to) return true;
   }
   return false;
}

bool SpreadOk()
{
   long sp = SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
   return sp <= InpMaxSpreadPoints;
}

//=== risk sizing ==================================================
double CurrentRiskPct(const double basePct)
{
   double r = basePct;
   if(InpLossStreakHalving && g_lossStreak > 0)
      r /= MathPow(2.0, MathMin(g_lossStreak, 4));
   double dayPL = AccountInfoDouble(ACCOUNT_EQUITY) - g_dayAnchor;
   double dayPLPct = dayPL / g_baseline * 100.0;
   // house-money ladder: escalate risk only from profit already earned today
   if(dayPLPct > 0.0)
      r += InpLadderFraction * dayPLPct;
   r = MathMin(r, InpMaxRiskPct);
   // hard cap: one loss must never push the day through the soft stop
   double remainingPct = dayPLPct + InpSoftDailyStopPct;
   r = MathMin(r, MathMax(remainingPct, 0.0));
   return MathMax(r, 0.0);
}

double LotsForRisk(const double slDistance, const double riskPct)
{
   if(slDistance <= 0 || riskPct <= 0) return 0.0;
   double riskMoney = g_baseline * riskPct / 100.0;
   double tickSize  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   if(tickSize <= 0 || tickValue <= 0) return 0.0;
   double lossPerLot = slDistance / tickSize * tickValue;
   if(lossPerLot <= 0) return 0.0;
   double lots = riskMoney / lossPerLot;
   double step = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   double vmin = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double vmax = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   lots = MathFloor(lots/step)*step;
   lots = MathMin(lots, MathMin(vmax, InpMaxLots));
   if(lots < vmin) return 0.0;   // cannot size safely -> skip trade
   return lots;
}

//=== day governor =================================================
long DayIndexNow()
{
   return (long)((TimeCurrent() - (long)InpDayResetHour*3600) / 86400);
}

void RolloverIfNeeded()
{
   long d = DayIndexNow();
   if(d == g_dayIdx) return;
   // new governor day
   if(g_dayIdx >= 0 && OwnPositions() > 0)
      CloseAllOwn("day reset flatten");
   g_dayIdx = d;
   string ak = GVDayKey("ANCHOR", d);
   double eq = AccountInfoDouble(ACCOUNT_EQUITY);
   double bal= AccountInfoDouble(ACCOUNT_BALANCE);
   if(GlobalVariableCheck(ak)) g_dayAnchor = GlobalVariableGet(ak);   // another instance set it
   else { g_dayAnchor = MathMax(eq, bal); GVSet(ak, g_dayAnchor); }
   g_dayPeakPL = 0.0;
   g_dayHalted = GVGet(GVDayKey("HALT", d), 0.0) > 0.5;
   g_dayBanked = GVGet(GVDayKey("BANK", d), 0.0) > 0.5;
   g_tradesToday = (int)GVGet(GVDayKey("TRADES", d), 0.0);
   g_consecLossesToday = 0;
   g_lossStreak = 0;
   g_ticketPlacedToday = false;
   g_orbFiredLong = false;
   g_orbFiredShort = false;
   PrintFormat("Sentinel new day idx=%I64d anchor=%.2f", d, g_dayAnchor);
}

void SetDayHalt(const string why)
{
   g_dayHalted = true;
   GVSet(GVDayKey("HALT", g_dayIdx), 1.0);
   Print("Sentinel DAY HALT: ", why);
}

void SetDayBank(const string why)
{
   g_dayBanked = true;
   GVSet(GVDayKey("BANK", g_dayIdx), 1.0);
   Print("Sentinel DAY BANKED GREEN: ", why);
}

void SetPermHalt(const string why)
{
   g_permHalt = true;
   GVSet(GVKey("PERMHALT"), 1.0);
   Print("Sentinel PERMANENT HALT: ", why);
}

// returns true when trading is allowed to continue this tick
bool Governor()
{
   double eq  = AccountInfoDouble(ACCOUNT_EQUITY);
   double bal = AccountInfoDouble(ACCOUNT_BALANCE);

   // sync shared account-level flags (another symbol's instance may have set them)
   if(!g_permHalt      && GVGet(GVKey("PERMHALT"), 0.0) > 0.5)            g_permHalt = true;
   if(!g_dayHalted     && GVGet(GVDayKey("HALT", g_dayIdx), 0.0) > 0.5)   g_dayHalted = true;
   if(!g_dayBanked     && GVGet(GVDayKey("BANK", g_dayIdx), 0.0) > 0.5)   g_dayBanked = true;
   if(!g_challengeDone && GVGet(GVKey("DONE"), 0.0) > 0.5)                g_challengeDone = true;
   g_tradingDays = (int)MathMax(g_tradingDays, GVGet(GVKey("TDAYS"), 0.0));

   if(g_permHalt) { if(OwnPositions()>0) CloseAllOwn("perm halt"); return false; }

   // total-DD fuse (ours 6% vs FTMO 10%)
   if(eq <= g_baseline*(1.0 - InpMaxTotalLossPct/100.0))
   {
      CloseAllOwn("total-DD fuse");
      SetPermHalt(StringFormat("equity %.2f <= fuse", eq));
      return false;
   }

   // challenge target reached (balance-based, no open positions)
   if(!g_challengeDone && bal >= g_baseline*(1.0 + InpProfitTargetPct/100.0) && OwnPositions()==0)
   {
      g_challengeDone = true;
      GVSet(GVKey("DONE"), 1.0);
      Print("Sentinel: CHALLENGE TARGET REACHED");
   }
   if(g_challengeDone && g_tradingDays >= InpMinTradingDays)
   {
      if(OwnPositions()>0) CloseAllOwn("challenge complete");
      return false;                      // done: stop entirely
   }

   double dayPL = eq - g_dayAnchor;
   g_dayPeakPL  = MathMax(g_dayPeakPL, dayPL);

   // hard daily stop: flatten everything
   if(dayPL <= -g_baseline*InpHardDailyStopPct/100.0)
   {
      CloseAllOwn("hard daily stop");
      SetDayHalt(StringFormat("dayPL %.2f hard stop", dayPL));
      return false;
   }
   // soft daily stop: no new trades
   if(!g_dayHalted && dayPL <= -g_baseline*InpSoftDailyStopPct/100.0)
      SetDayHalt(StringFormat("dayPL %.2f soft stop", dayPL));

   // daily goal bank
   if(InpBankAtGoal && !g_dayBanked && dayPL >= g_baseline*InpDailyGoalPct/100.0)
   {
      CloseAllOwn("daily goal reached");
      SetDayBank(StringFormat("dayPL %.2f >= goal", dayPL));
   }
   // green-day ratchet
   if(!g_dayBanked && g_dayPeakPL >= g_baseline*InpRatchetTriggerPct/100.0)
   {
      double floorAmt = MathMax(g_baseline*InpRatchetFloorPct/100.0,
                                g_dayPeakPL*InpRatchetTrailRatio);
      if(dayPL <= floorAmt)
      {
         CloseAllOwn("ratchet floor");
         SetDayBank(StringFormat("locked %.2f of peak %.2f", dayPL, g_dayPeakPL));
      }
   }

   // Friday flatten
   if(InpFridayFlatten)
   {
      MqlDateTime dt; TimeToStruct(TimeCurrent(), dt);
      if(dt.day_of_week==5 && dt.hour >= InpFridayFlattenHour && OwnPositions()>0)
         CloseAllOwn("friday flatten");
   }

   return !(g_dayHalted || g_dayBanked);
}

//=== entries ======================================================
void CountTradingDay()
{
   if(g_lastCountedDay == g_dayIdx) return;
   g_lastCountedDay = g_dayIdx;
   g_tradingDays++;
   GVSet(GVKey("TDAYS"), g_tradingDays);
   GVSet(GVKey("LASTTDAY"), (double)g_lastCountedDay);
}

// barrier distances for the corpus-reclaim mode (ORB computes its own)
bool ReclaimBarriers(double &slDist, double &tpDist)
{
   if(InpExitMode == EXIT_ATR_BARRIERS)
   {
      double atr[];
      ArraySetAsSeries(atr, true);
      if(CopyBuffer(g_hAtr, 0, 1, 1, atr) < 1) return false;
      slDist = atr[0]*InpSlAtrMult;
      tpDist = atr[0]*InpTpAtrMult;
   }
   else
   {
      MqlTick tick;
      if(!SymbolInfoTick(_Symbol, tick)) return false;
      double mid = 0.5*(tick.bid + tick.ask);
      slDist = mid*InpSlFraction;
      tpDist = mid*InpTpFraction;
   }
   return slDist > 0 && tpDist > 0;
}

bool OpenPosition(const int dir, const double riskPct, const string tag,
                  const double slDist, const double tpDist)
{
   MqlTick tick;
   if(!SymbolInfoTick(_Symbol, tick)) return false;
   if(slDist <= 0 || tpDist <= 0) return false;

   double lots = LotsForRisk(slDist, riskPct);
   if(lots <= 0) return false;

   bool ok;
   if(dir > 0)
      ok = g_trade.Buy(lots, _Symbol, tick.ask, tick.ask - slDist, tick.ask + tpDist,
                       InpComment + "_" + tag);
   else
      ok = g_trade.Sell(lots, _Symbol, tick.bid, tick.bid + slDist, tick.bid - tpDist,
                        InpComment + "_" + tag);
   if(!ok)
   {
      PrintFormat("Sentinel order fail dir=%d err=%d ret=%d", dir, GetLastError(),
                  (int)g_trade.ResultRetcode());
      return false;
   }
   g_lastEntryTime = TimeCurrent();
   // account-level shared counter: read-modify-write so multi-symbol instances share the cap
   g_tradesToday = (int)GVGet(GVDayKey("TRADES", g_dayIdx), 0.0) + 1;
   GVSet(GVDayKey("TRADES", g_dayIdx), g_tradesToday);
   CountTradingDay();
   return true;
}

// ticket-trade: minimum-size trade to register a trading day after target hit
void MaybeTicketTrade()
{
   if(!InpTicketMode || !g_challengeDone) return;
   if(g_tradingDays >= InpMinTradingDays) return;
   if(g_ticketPlacedToday || g_lastCountedDay == g_dayIdx) return;
   if(!InSession() || !SpreadOk() || InNewsBlackout()) return;

   MqlDateTime dt; TimeToStruct(TimeCurrent(), dt);
   bool concurrence=false;
   int dir = Signal(concurrence);
   if(dir == 0 && dt.hour >= InpTicketHour) dir = 1;   // fallback: timed micro long
   if(dir == 0) return;

   MqlTick tick;
   if(!SymbolInfoTick(_Symbol, tick)) return;
   double atr[];
   ArraySetAsSeries(atr, true);
   if(CopyBuffer(g_hAtr, 0, 1, 1, atr) < 1) return;
   double vmin = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double sl = atr[0]*1.0, tp = atr[0]*1.0;
   bool ok = (dir > 0)
      ? g_trade.Buy (vmin, _Symbol, tick.ask, tick.ask-sl, tick.ask+tp, InpComment+"_TICKET")
      : g_trade.Sell(vmin, _Symbol, tick.bid, tick.bid+sl, tick.bid-tp, InpComment+"_TICKET");
   if(ok)
   {
      g_ticketPlacedToday = true;
      CountTradingDay();
      Print("Sentinel ticket trade placed (registering trading day)");
   }
}

//+------------------------------------------------------------------+
void OnTick()
{
   RolloverIfNeeded();

   bool mayTrade = Governor();

   // challenge-done ticket mode runs even when normal trading is off
   if(!mayTrade)
   {
      MaybeTicketTrade();
      return;
   }

   // new-bar gate on trigger TF
   datetime bt = iTime(_Symbol, PERIOD_CURRENT, 0);
   if(bt == g_lastBarTime) return;
   g_lastBarTime = bt;

   if(!InSession() || !SpreadOk() || InNewsBlackout()) return;
   if(OwnPositions() >= InpMaxOpenPositions) return;
   g_tradesToday = (int)GVGet(GVDayKey("TRADES", g_dayIdx), 0.0);   // shared across symbols
   if(g_tradesToday >= InpMaxTradesPerDay) return;
   if(g_consecLossesToday >= InpMaxConsecLosses)
   {
      SetDayHalt("max consecutive losses");
      return;
   }
   if(g_lastEntryTime > 0 && TimeCurrent() - g_lastEntryTime < InpCooldownMinutes*60) return;

   bool concurrence=false;
   int dir = 0;
   double slDist=0, tpDist=0, strengthMult=1.0;
   string tag = "";
   if(InpEntryMode == MODE_LONDON_ORB)
   {
      dir = OrbSignal(slDist, tpDist);
      tag = "ORB";
   }
   else if(InpEntryMode == MODE_KELTNER_FADE)
   {
      dir = KeltnerFadeSignal(slDist, tpDist, strengthMult);
      tag = "KFADE";
   }
   else
   {
      dir = Signal(concurrence);
      if(dir != 0 && !ReclaimBarriers(slDist, tpDist)) dir = 0;
      tag = concurrence ? "CONC" : (dir>0 ? "L" : "S");
   }
   if(dir == 0) return;

   double risk = CurrentRiskPct(InpEntryMode == MODE_LONDON_ORB ? InpOrbRiskPct
                                                                : InpRiskPct);
   risk *= strengthMult;                       // fade strength sizing (1.0 otherwise)
   if(concurrence) risk *= InpConcurrenceBoost;
   risk = MathMin(risk, InpMaxRiskPct);        // ceiling holds after ALL multipliers
   // re-apply the one-loss-cannot-break-the-day cap after any boost
   double dayPL = AccountInfoDouble(ACCOUNT_EQUITY) - g_dayAnchor;
   double remainingPct = (dayPL + g_baseline*InpSoftDailyStopPct/100.0)/g_baseline*100.0;
   risk = MathMin(risk, MathMax(remainingPct, 0.0));
   if(risk <= 0.02) return;

   if(OpenPosition(dir, risk, tag, slDist, tpDist))
   {
      if(InpEntryMode == MODE_LONDON_ORB)
      {
         if(dir > 0) g_orbFiredLong = true; else g_orbFiredShort = true;
      }
      PrintFormat("Sentinel entry mode=%d dir=%d risk=%.2f%% tradesToday=%d",
                  (int)InpEntryMode, dir, risk, g_tradesToday);
   }
}

//=== trade result tracking ========================================
void OnTradeTransaction(const MqlTradeTransaction &trans,
                        const MqlTradeRequest &request,
                        const MqlTradeResult &result)
{
   if(trans.type != TRADE_TRANSACTION_DEAL_ADD) return;
   if(!HistoryDealSelect(trans.deal)) return;
   if(HistoryDealGetInteger(trans.deal, DEAL_MAGIC) != InpMagic) return;
   if(HistoryDealGetString(trans.deal, DEAL_SYMBOL) != _Symbol) return;
   if((ENUM_DEAL_ENTRY)HistoryDealGetInteger(trans.deal, DEAL_ENTRY) != DEAL_ENTRY_OUT) return;

   double pnl = HistoryDealGetDouble(trans.deal, DEAL_PROFIT)
              + HistoryDealGetDouble(trans.deal, DEAL_SWAP)
              + HistoryDealGetDouble(trans.deal, DEAL_COMMISSION);
   if(pnl < 0) { g_lossStreak++; g_consecLossesToday++; }
   else if(pnl > 0) { g_lossStreak = 0; g_consecLossesToday = 0; }
}
//+------------------------------------------------------------------+
