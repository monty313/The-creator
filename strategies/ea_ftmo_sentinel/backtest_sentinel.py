"""Bar-accurate backtest of FTMO_Sentinel_EA.mq5 on real Dukascopy M1 data.

Mirrors the EA:
  * signals on CLOSED M5 bars, entry at next M5 bar open (+spread for longs)
  * Engine A: CCI M-line reclaim + dual-HTF force (H1/H4, |M_H1| >= 8)
  * Engine B: McFlurry RSI M-line reclaim + force (|M_H1| >= 1.5)
  * optional Mark mass gate: close vs SMA100(+2) on both HTFs
  * shell: session 07-21 UTC, bar confirm, micro structure, cooldown, 1 position
  * exits: ATR barriers (TP 0.7*ATR14, SL 2.8*ATR14), adjudicated on M1 bars;
    if one M1 bar touches both barriers the trade counts as a LOSS (conservative)
  * Day Governor: base risk 0.8% + house-money ladder 0.75 (cap 2%), loss-streak
    halving, 3-consecutive-loss day stop, soft -1.5% / hard -2.0%, goal bank
    +2.5%, ratchet 0.8%/0.2%/60%, day flatten at UTC midnight, max 40 trades/day

Honest by construction: no look-ahead, spread+commission charged, conservative
same-bar rule, results split by month to expose window luck.

Usage:  python3 backtest_sentinel.py EURUSD [variant ...]
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

# --- repo indicator conventions (strategies/python_batch/indicators.py) ----
def sma(s, n):  return s.rolling(n, min_periods=n).mean()

def rsi(close, n=14):
    d = close.diff()
    up = d.clip(lower=0.0)
    dn = (-d).clip(lower=0.0)
    ma_up = up.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()
    ma_dn = dn.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()
    rs = ma_up / ma_dn.replace(0.0, np.nan)
    return 100.0 - (100.0 / (1.0 + rs))

def atr(high, low, close, n=14):
    prev = close.shift(1)
    tr = pd.concat([(high - low), (high - prev).abs(), (low - prev).abs()], axis=1).max(axis=1)
    return tr.rolling(n, min_periods=n).mean()

def cci(high, low, close, n=20):
    tp = (high + low + close) / 3.0
    ma = tp.rolling(n, min_periods=n).mean()
    md = (tp - ma).abs().rolling(n, min_periods=n).mean()
    return (tp - ma) / (0.015 * md.replace(0.0, np.nan))

def cci_mline(h, l, c, n=20):
    x = sma(cci(h, l, c, n), 2)
    return sma(x, 7) - sma(x, 21)

def rsi_mline(c, n=13):
    r = rsi(c, n)
    return sma(r, 7) - sma(r, 21)


@dataclass
class Config:
    name: str = "default"
    use_engine_cci: bool = True
    use_engine_mcf: bool = True
    require_concurrence: bool = False
    require_mark_mass: bool = True
    cci_force: float = 8.0
    mcf_force: float = 1.5
    load_lookback: int = 8
    use_bar_confirm: bool = True
    use_micro_structure: bool = True
    session: tuple = (7, 21)
    tp_atr: float = 0.70
    sl_atr: float = 2.80
    atr_period: int = 14
    spread: float = 0.00007      # 0.7 pip all-in cost (FTMO raw + commission)
    base_risk: float = 0.80
    max_risk: float = 2.00
    ladder: float = 0.75
    soft_stop: float = 1.5
    hard_stop: float = 2.0
    goal: float = 2.5
    ratchet_trigger: float = 0.8
    ratchet_floor: float = 0.20
    ratchet_trail: float = 0.60
    max_trades_day: int = 40
    max_consec_losses: int = 3
    cooldown_min: int = 8
    conc_boost: float = 1.25


def resample(m1: pd.DataFrame, rule: str) -> pd.DataFrame:
    o = m1.resample(rule, label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
    return o.dropna(subset=["open"])


def map_htf(htf_series: pd.Series, target_index) -> pd.Series:
    """Value of the last COMPLETED HTF bar at each target timestamp (no peeking)."""
    return htf_series.shift(1).reindex(target_index, method="ffill")


def build_signals(m1: pd.DataFrame, cfg: Config):
    m5 = resample(m1, "5min")
    h1 = resample(m1, "1h")
    h4 = resample(m1, "4h")

    idx = m5.index
    diag = {}

    def reclaim(m: pd.Series, lookback: int):
        prev = m.shift(1)
        mn = m.shift(1).rolling(lookback, min_periods=1).min()
        mx = m.shift(1).rolling(lookback, min_periods=1).max()
        fire_l = (prev <= 0) & (m > 0) & (mn < 0)
        fire_s = (prev >= 0) & (m < 0) & (mx > 0)
        return fire_l.fillna(False), fire_s.fillna(False)

    # Engine A: CCI gravity
    a_l = pd.Series(False, idx); a_s = pd.Series(False, idx)
    if cfg.use_engine_cci:
        mL = cci_mline(m5.high, m5.low, m5.close)
        fl, fs = reclaim(mL, cfg.load_lookback)
        m1f = map_htf(cci_mline(h1.high, h1.low, h1.close), idx)
        m2f = map_htf(cci_mline(h4.high, h4.low, h4.close), idx)
        a_l = fl & (m1f > 0) & (m2f > 0) & (m1f >= cfg.cci_force)
        a_s = fs & (m1f < 0) & (m2f < 0) & (m1f <= -cfg.cci_force)
        diag["A_fire"] = int(fl.sum() + fs.sum())
        diag["A_after_force"] = int(a_l.sum() + a_s.sum())

    # Engine B: McFlurry
    b_l = pd.Series(False, idx); b_s = pd.Series(False, idx)
    if cfg.use_engine_mcf:
        mL = rsi_mline(m5.close)
        fl, fs = reclaim(mL, cfg.load_lookback)
        m1f = map_htf(rsi_mline(h1.close), idx)
        m2f = map_htf(rsi_mline(h4.close), idx)
        b_l = fl & (m1f > 0) & (m2f > 0) & (m1f >= cfg.mcf_force)
        b_s = fs & (m1f < 0) & (m2f < 0) & (m1f <= -cfg.mcf_force)
        diag["B_fire"] = int(fl.sum() + fs.sum())
        diag["B_after_force"] = int(b_l.sum() + b_s.sum())

    conc_l, conc_s = a_l & b_l, a_s & b_s
    if cfg.require_concurrence:
        sig_l, sig_s = conc_l, conc_s
    else:
        sig_l, sig_s = a_l | b_l, a_s | b_s
    diag["union_or_conc"] = int(sig_l.sum() + sig_s.sum())

    # Mark mass gate (SMA100 shift+2 as BB(100,.5,+2) midline)
    if cfg.require_mark_mass:
        mid1 = map_htf(sma(h1.close, 100).shift(2), idx)
        mid2 = map_htf(sma(h4.close, 100).shift(2), idx)
        c1 = map_htf(h1.close, idx)
        c2 = map_htf(h4.close, idx)
        sig_l = sig_l & (c1 > mid1) & (c2 > mid2)
        sig_s = sig_s & (c1 < mid1) & (c2 < mid2)
        diag["after_mass"] = int(sig_l.sum() + sig_s.sum())

    if cfg.use_bar_confirm:
        sig_l = sig_l & (m5.close > m5.open)
        sig_s = sig_s & (m5.close < m5.open)
    if cfg.use_micro_structure:
        sig_l = sig_l & (m5.low > m5.low.shift(2))
        sig_s = sig_s & (m5.high < m5.high.shift(2))
    diag["after_shell"] = int(sig_l.sum() + sig_s.sum())

    a14 = atr(m5.high, m5.low, m5.close, cfg.atr_period)
    return m5, sig_l, sig_s, conc_l | conc_s, a14, diag


def run_backtest(m1: pd.DataFrame, cfg: Config):
    m5, sig_l, sig_s, conc, a14, diag = build_signals(m1, cfg)

    m1_times = m1.index.values
    m1_high = m1.high.values
    m1_low = m1.low.values
    m1_close = m1.close.values

    trades = []
    daily = {}          # date -> dict(pl, trades, banked, halted, min_float)

    day = None
    day_pl = day_peak = 0.0
    day_trades = day_consec = 0
    day_banked = day_halted = False
    streak = 0
    last_entry_ts = None
    pos_until = None    # skip M5 bars while a trade is being walked on M1

    sigL = sig_l.values; sigS = sig_s.values; concv = conc.values
    atrv = a14.values
    m5_open = m5.open.values; m5_index = m5.index

    def day_rec():
        return daily.setdefault(day, {"pl": 0.0, "trades": 0, "banked": False,
                                      "halted": False, "min_float": 0.0})

    for i in range(1, len(m5_index)):
        ts = m5_index[i]
        d = ts.date()
        if d != day:
            day = d
            day_pl = day_peak = 0.0
            day_trades = day_consec = 0
            day_banked = day_halted = False
            streak = 0
        if pos_until is not None and ts < pos_until:
            continue
        pos_until = None

        if day_banked or day_halted:
            continue
        hour = ts.hour
        if not (cfg.session[0] <= hour < cfg.session[1]):
            continue
        if ts.weekday() == 4 and hour >= 19:      # Friday last-entry
            continue
        if day_trades >= cfg.max_trades_day or day_consec >= cfg.max_consec_losses:
            day_halted = True
            day_rec()["halted"] = True
            continue
        if last_entry_ts is not None and (ts - last_entry_ts).total_seconds() < cfg.cooldown_min * 60:
            continue

        # signal decided on closed bar i-1, entry at bar i open
        j = i - 1
        long_ = bool(sigL[j]); short_ = bool(sigS[j])
        if not (long_ or short_):
            continue
        av = atrv[j]
        if not np.isfinite(av) or av <= 0:
            continue

        risk = cfg.base_risk
        if streak > 0:
            risk /= 2 ** min(streak, 4)
        if day_pl > 0:
            risk += cfg.ladder * day_pl
        risk = min(risk, cfg.max_risk)
        if concv[j]:
            risk *= cfg.conc_boost
        risk = min(risk, max(day_pl + cfg.soft_stop, 0.0))
        if risk <= 0.02:
            continue

        direction = 1 if long_ else -1
        entry_bid = m5_open[i]
        entry = entry_bid + cfg.spread if direction > 0 else entry_bid
        tp_dist, sl_dist = av * cfg.tp_atr, av * cfg.sl_atr
        if direction > 0:
            tp_level, sl_level = entry + tp_dist, entry - sl_dist
        else:
            tp_level, sl_level = entry - tp_dist - cfg.spread, entry + sl_dist - cfg.spread
            # short exits buy back at ask = bid + spread; fold spread into levels

        # ---- walk M1 bars from entry time ------------------------------
        k0 = np.searchsorted(m1_times, np.datetime64(ts))
        pnl = None
        exit_ts = None
        rec = day_rec()
        for k in range(k0, len(m1_times)):
            bar_ts = pd.Timestamp(m1_times[k])
            if bar_ts.date() != day:                       # day rollover flatten
                px = m1_close[k - 1] if k > k0 else entry
                move = (px - entry) if direction > 0 else (entry - px - cfg.spread)
                pnl = risk * move / sl_dist
                exit_ts = pd.Timestamp(m1_times[k - 1]) if k > k0 else bar_ts
                break
            hi, lo, cl = m1_high[k], m1_low[k], m1_close[k]
            if direction > 0:
                hit_sl = lo <= sl_level
                hit_tp = hi >= tp_level
            else:
                hit_sl = hi >= sl_level
                hit_tp = lo <= tp_level
            if hit_sl:                                     # conservative: SL first
                pnl = -risk
                exit_ts = bar_ts
                break
            if hit_tp:
                pnl = risk * tp_dist / sl_dist
                exit_ts = bar_ts
                break
            # governor watchdog on floating equity (per-M1-close ~ per tick)
            move = (cl - entry) if direction > 0 else (entry - cl - cfg.spread)
            floating = risk * move / sl_dist
            f_day = day_pl + floating
            rec["min_float"] = min(rec["min_float"], f_day)
            if f_day <= -cfg.hard_stop:
                pnl = floating
                exit_ts = bar_ts
                day_halted = True
                rec["halted"] = True
                break
            if f_day >= cfg.goal:
                pnl = floating
                exit_ts = bar_ts
                day_banked = True
                rec["banked"] = True
                break
            if max(day_peak, f_day) >= cfg.ratchet_trigger:
                floor_ = max(cfg.ratchet_floor, max(day_peak, f_day) * cfg.ratchet_trail)
                if f_day <= floor_:
                    pnl = floating
                    exit_ts = bar_ts
                    day_banked = True
                    rec["banked"] = True
                    break
        if pnl is None:                                    # data ended mid-trade
            continue

        day_pl += pnl
        day_peak = max(day_peak, day_pl)
        day_trades += 1
        last_entry_ts = ts
        rec["pl"] = day_pl
        rec["trades"] = day_trades
        if pnl < 0:
            streak += 1
            day_consec += 1
        elif pnl > 0:
            streak = 0
            day_consec = 0
        trades.append({"time": ts, "dir": direction, "risk": risk,
                       "pnl": pnl, "win": pnl > 0, "conc": bool(concv[j]),
                       "exit": exit_ts})
        pos_until = exit_ts + pd.Timedelta(minutes=1)

        # post-close governor checks (mirror EA order)
        if day_pl <= -cfg.soft_stop:
            day_halted = True
            rec["halted"] = True
        if day_pl >= cfg.goal:
            day_banked = True
            rec["banked"] = True
        elif day_peak >= cfg.ratchet_trigger:
            floor_ = max(cfg.ratchet_floor, day_peak * cfg.ratchet_trail)
            if day_pl <= floor_:
                day_banked = True
                rec["banked"] = True

    return trades, daily, diag


def challenge_walkforward(daily: dict, goal=10.0, fuse=-6.0, min_days=4, cap=45):
    dates = sorted(daily)
    outcomes = []
    for s in range(len(dates)):
        cum = 0.0
        tdays = 0
        res = None
        for k, d in enumerate(dates[s:s + cap]):
            rec = daily[d]
            if rec["min_float"] <= -5.0:
                res = ("FAIL_DAILY", k + 1); break
            cum += rec["pl"]
            if rec["trades"] > 0:
                tdays += 1
            if cum <= -10.0:
                res = ("FAIL_TOTAL", k + 1); break
            if cum <= fuse:
                res = ("HALT_FUSE", k + 1); break
            if cum >= goal and tdays >= min_days:
                res = ("PASS", k + 1); break
        outcomes.append(res or ("TIMEOUT", min(cap, len(dates) - s)))
    return outcomes


def report(sym: str, cfg: Config, trades: list, daily: dict, diag: dict) -> str:
    L = [f"### {sym} · variant `{cfg.name}`", ""]
    L.append(f"signal funnel: {diag}")
    n = len(trades)
    days = sorted(daily)
    ndays = len(days)
    if n == 0:
        L.append("**NO TRADES** — gates never opened on this window.")
        return "\n".join(L)
    wins = sum(1 for t in trades if t["win"])
    pls = [daily[d]["pl"] for d in days]
    tdays = [d for d in days if daily[d]["trades"] > 0]
    red = [p for d, p in zip(days, pls) if p < -1e-9 and daily[d]["trades"] > 0]
    green_goal = sum(1 for p in pls if p >= cfg.goal - 1e-9)
    banked = sum(1 for d in days if daily[d]["banked"])
    total = sum(pls)
    minf = min(daily[d]["min_float"] for d in days)
    L.append(f"- trades: **{n}** ({n / max(len(tdays),1):.1f}/trading day, "
             f"{len(tdays)}/{ndays} days traded) · WR **{wins/n:.1%}** · "
             f"concurrence fires: {sum(1 for t in trades if t['conc'])}")
    L.append(f"- total P&L: **{total:+.2f}%** of initial over {ndays} days "
             f"({total/max(ndays,1)*21:.1f}%/month-ish) · mean day {np.mean(pls):+.3f}% "
             f"· median day {np.median(pls):+.3f}%")
    L.append(f"- P(day >= +{cfg.goal}%): **{green_goal/max(len(tdays),1):.1%}** of traded days "
             f"· banked-green days: {banked}")
    L.append(f"- red traded days: **{len(red)}** (worst close {min(pls):+.2f}%) · "
             f"worst intraday float {minf:+.2f}% · FTMO -5% breaches: "
             f"**{sum(1 for d in days if daily[d]['min_float'] <= -5.0)}**")
    oc = challenge_walkforward(daily)
    from collections import Counter
    c = Counter(r for r, _ in oc)
    passes = [k for r, k in oc if r == "PASS"]
    L.append(f"- challenge walk-forward ({len(oc)} starts): "
             + ", ".join(f"{k} {v/len(oc):.0%}" for k, v in sorted(c.items()))
             + (f" · median days-to-pass {int(np.median(passes))}" if passes else ""))
    # month split (window-luck exposure)
    bym = {}
    for d in days:
        bym.setdefault(str(d)[:7], []).append(daily[d]["pl"])
    L.append("- by month: " + " · ".join(f"{m} {sum(v):+.1f}%" for m, v in sorted(bym.items())))
    return "\n".join(L)


VARIANTS = {
    "default":    Config(name="default"),
    "no_mass":    Config(name="no_mass", require_mark_mass=False),
    "conc_only":  Config(name="conc_only", require_concurrence=True, require_mark_mass=False),
    "cci_only":   Config(name="cci_only", use_engine_mcf=False, require_mark_mass=False),
    "mcf_only":   Config(name="mcf_only", use_engine_cci=False, require_mark_mass=False),
}


def main():
    sym = sys.argv[1] if len(sys.argv) > 1 else "EURUSD"
    names = sys.argv[2:] or list(VARIANTS)
    path = Path(__file__).parent / "data" / f"{sym}_M1.parquet"
    m1 = pd.read_parquet(path)
    if m1.index.tz is not None:
        m1.index = m1.index.tz_convert("UTC").tz_localize(None)   # plain UTC timestamps
    print(f"{sym}: {len(m1)} M1 bars {m1.index[0]} -> {m1.index[-1]}\n")
    spread = {"EURUSD": 0.00007, "GBPUSD": 0.00010, "XAUUSD": 0.20}.get(sym, 0.00010)
    blocks = []
    for nm in names:
        cfg = replace(VARIANTS[nm], spread=spread)
        trades, daily, diag = run_backtest(m1, cfg)
        block = report(sym, cfg, trades, daily, diag)
        print(block, "\n")
        blocks.append(block)
    out = Path(__file__).parent / f"BACKTEST_{sym}.md"
    out.write_text(f"# Sentinel backtest — {sym} (Dukascopy M1, bar-accurate)\n\n"
                   + "\n\n".join(blocks) + "\n")
    print(f"[written] {out}")


if __name__ == "__main__":
    main()
