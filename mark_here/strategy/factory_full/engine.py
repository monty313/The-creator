"""Gravity Factory engine — gapped-ladder MTF backtester.
Causality: signals on CLOSED bars only; higher-TF flags effective at bar close time; fills at next LTF bar open.
Costs: per-bar recorded spread (price units) paid on entry+exit sides as bid/ask; commission+slippage RT in pips.
"""
import pandas as pd, numpy as np, json

FLOORS = {'1m':'1min','5m':'5min','15m':'15min','30m':'30min','1h':'1h','4h':'4h'}
LADDERS = [('1m','15m','30m'), ('5m','30m','1h'), ('15m','1h','4h'), ('30m','4h','1d'), ('1h','1d','1w')]
EXIT_TFS = ['LTF','MID']
EXIT_PERIODS = [1,2,3,4]
EXIT_SHIFTS = [1,-1,-2,-3,-4,-5]
CONFIGS = [(etf,p,s) for etf in EXIT_TFS for p in EXIT_PERIODS for s in EXIT_SHIFTS]  # 48

def resample(df, tf):
    t = df['t']
    if tf=='1d':
        key = t.dt.normalize(); dur = pd.Timedelta(days=1)
    elif tf=='1w':
        key = (t - pd.to_timedelta(t.dt.weekday, unit='D')).dt.normalize(); dur = pd.Timedelta(days=7)
    else:
        key = t.dt.floor(FLOORS[tf]); dur = pd.Timedelta(FLOORS[tf])
    g = df.groupby(key)
    out = pd.DataFrame({'o':g['o'].first(),'h':g['h'].max(),'l':g['l'].min(),
                        'c':g['c'].last(),'spread':g['spread'].mean()})
    out = out.sort_index()
    out['open_time'] = out.index
    out['close_time'] = out.index + dur
    return out.reset_index(drop=True)

def rsi(s, n):
    d = s.diff()
    up = d.clip(lower=0.0); dn = (-d).clip(lower=0.0)
    ru = up.ewm(alpha=1.0/n, min_periods=n).mean()
    rd = dn.ewm(alpha=1.0/n, min_periods=n).mean()
    denom = ru + rd
    out = 100.0 * ru / denom
    return out.where(denom > 0, 50.0)

def bb(s, n, dev, shift):
    m = s.rolling(n).mean(); sd = s.rolling(n).std(ddof=0)
    return (m+dev*sd).shift(shift), (m-dev*sd).shift(shift)

def flags_gv13(f):
    r2 = rsi(f['c'],2); r20 = rsi(f['c'],20)
    u2,d2 = bb(r2,20,0.5,2); u20,d20 = bb(r20,20,0.5,2)
    valid = r2.notna()&r20.notna()&u2.notna()&u20.notna()
    return {'grav_up':((r2>u2)&(r20>u20)&valid), 'grav_dn':((r2<d2)&(r20<d20)&valid),
            'trig_up':((r20>u20)&(r2<=u2)&valid), 'trig_dn':((r20<d20)&(r2>=d2)&valid),
            'valid':valid, 'dbg':{'r2':r2,'r20':r20,'u2':u2,'u20':u20,'d2':d2,'d20':d20}}

def flags_gv14(f):
    c = f['c']
    u200,d200 = bb(c,200,1.0,0); u20,d20 = bb(c,20,1.0,0)
    valid = u200.notna()&u20.notna()
    trig_up = (c<u20)&(c.shift(1)>=u20.shift(1))&valid&valid.shift(1).fillna(False)
    trig_dn = (c>d20)&(c.shift(1)<=d20.shift(1))&valid&valid.shift(1).fillna(False)
    return {'grav_up':((c>u200)&(c>u20)&valid), 'grav_dn':((c<d200)&(c<d20)&valid),
            'trig_up':trig_up, 'trig_dn':trig_dn, 'valid':valid,
            'dbg':{'u200':u200,'d200':d200,'u20':u20,'d20':d20}}

FLAGS = {'GV013':flags_gv13, 'GV014':flags_gv14}

def map_flag(flag, valid, htf_close, ltf_close):
    """value of flag from last higher-TF bar whose close_time <= ltf_close; False if none/invalid."""
    idx = np.searchsorted(htf_close.values, ltf_close.values, side='right') - 1
    ok = idx >= 0
    idx0 = np.where(ok, idx, 0)
    fv = flag.values[idx0] & valid.values[idx0] & ok
    return fv

def build_signals(strat, frames, L, M, H):
    fL, fM, fH = frames[L], frames[M], frames[H]
    flL, flM, flH = FLAGS[strat](fL), FLAGS[strat](fM), FLAGS[strat](fH)
    lc = fL['close_time']
    gupM = map_flag(flM['grav_up'], flM['valid'], fM['close_time'], lc)
    gdnM = map_flag(flM['grav_dn'], flM['valid'], fM['close_time'], lc)
    gupH = map_flag(flH['grav_up'], flH['valid'], fH['close_time'], lc)
    gdnH = map_flag(flH['grav_dn'], flH['valid'], fH['close_time'], lc)
    sig_up = flL['trig_up'].values & gupM & gupH
    sig_dn = flL['trig_dn'].values & gdnM & gdnH
    if strat=='GV013':  # state-based trigger -> edge
        sig_up = sig_up & ~np.concatenate([[False], sig_up[:-1]])
        sig_dn = sig_dn & ~np.concatenate([[False], sig_dn[:-1]])
    # validity of the whole stack mapped to LTF (for tradable_start)
    vM = map_flag(flM['valid'], flM['valid'], fM['close_time'], lc)
    vH = map_flag(flH['valid'], flH['valid'], fH['close_time'], lc)
    stack_valid = flL['valid'].values & vM & vH
    return sig_up, sig_dn, stack_valid, (flL, flM, flH)

def exit_events(fT, p, s):
    c = fT['c']; sma = c.rolling(p).mean()
    if s > 0:
        ref_c, ref_s = c, sma.shift(s)
    else:
        ref_c, ref_s = c.shift(-s), sma
    valid = ref_c.notna() & ref_s.notna()
    exL = (ref_c < ref_s) & valid
    exS = (ref_c > ref_s) & valid
    ct = fT['close_time'].values
    return ct[exL.values], ct[exS.values]

def simulate(lt, entL_idx, entS_idx, exL_times, exS_times, pip, comm, want_trades=False):
    """lt: dict arrays open_time,o,c,spread (LTF). ent*_idx: decision bar indices (fill at +1)."""
    ot = lt['open_time']; o = lt['o']; c = lt['c']; sp = lt['spread']; n = len(ot)
    cands = [(i+1, +1) for i in entL_idx if i+1 < n] + [(i+1, -1) for i in entS_idx if i+1 < n]
    cands.sort()
    trades = []
    pos_end = -1
    for fi, side in cands:
        if fi <= pos_end: continue
        ft = ot[fi]
        ext = exL_times if side>0 else exS_times
        j = np.searchsorted(ext, ft, side='right')
        censored = False
        if j >= len(ext):
            gi = n-1; censored = True
        else:
            gi = int(np.searchsorted(ot, ext[j], side='left'))
            if gi >= n: gi = n-1; censored = True
        if gi <= fi: gi = min(fi+1, n-1)
        if side > 0:
            entry = o[fi] + sp[fi]
            exitp = c[gi] if censored else o[gi]
            pips = (exitp - entry)/pip - comm
        else:
            entry = o[fi]
            exitp = (c[gi] + sp[gi]) if censored else (o[gi] + sp[gi])
            pips = (entry - exitp)/pip - comm
        trades.append((fi, gi, side, pips, censored))
        pos_end = gi
    if not want_trades:
        return trades
    # bars-to-profit per trade (net of all RT costs), using LTF closes
    enriched = []
    for fi, gi, side, pips, censored in trades:
        seg = c[fi:gi+1]
        if side > 0:
            fl = (seg - (o[fi]+sp[fi]))/pip - comm
        else:
            fl = (o[fi] - (seg + sp[fi:gi+1]))/pip - comm
        pos = np.nonzero(fl > 0)[0]
        btp = int(pos[0])+1 if len(pos) else -1
        enriched.append((fi, gi, side, pips, censored, btp, gi-fi))
    return enriched

def run_unit(strat, ladder, frames, pip, comm, day_index):
    """Returns daily_net (48,D), daily_ntr (48,D), tradable_start, cand counts."""
    L, M, H = ladder
    sig_up, sig_dn, stack_valid, _ = build_signals(strat, frames, L, M, H)
    fL = frames[L]
    lt = {'open_time': fL['open_time'].values, 'o': fL['o'].values,
          'c': fL['c'].values, 'spread': fL['spread'].values}
    entL = np.nonzero(sig_up)[0]; entS = np.nonzero(sig_dn)[0]
    vidx = np.nonzero(stack_valid)[0]
    tstart = fL['open_time'].values[vidx[0]] if len(vidx) else None
    days = lt['open_time'].astype('datetime64[D]')
    D = len(day_index)
    dpos = np.searchsorted(day_index, days)
    net = np.zeros((len(CONFIGS), D)); ntr = np.zeros((len(CONFIGS), D), dtype=np.int32)
    for k,(etf,p,s) in enumerate(CONFIGS):
        fT = frames[L] if etf=='LTF' else frames[M]
        exL_t, exS_t = exit_events(fT, p, s)
        for fi, gi, side, pips, cen in simulate(lt, entL, entS, exL_t, exS_t, pip, comm):
            d = dpos[gi]
            if 0 <= d < D:
                net[k, d] += pips; ntr[k, d] += 1
    return net, ntr, tstart, len(entL), len(entS)
