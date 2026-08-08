"""GV-015 'Tunnel Rider' — BB(100,.5,+2) + BB(10,.5,+2) on all set TFs, SMA50 on LTF.
Buy: close above upper bands of BOTH BBs on ALL 3 TFs AND above LTF SMA50 (edge-triggered).
Re-entry: LTF price crosses up / touches upper BB10 while LTF SMA50 > LTF upper BB100 (and close>SMA50 so the exit rule doesn't instantly fire).
Exit: LTF close crosses SMA50 the other way (state-based). Shorts mirrored. No parameter grid — one fixed config.
"""
import pandas as pd, numpy as np, json, sys
from engine import resample, bb, map_flag, simulate

meta = json.load(open('data/clean/meta.json'))
LADDERS15 = [('5m','30m','1h'), ('15m','1h','4h'), ('30m','4h','1d')]
SYMS = sys.argv[1:] if len(sys.argv)>1 else ['EURUSD','GBPUSD','XAUUSD','US500']

def band_flags(f):
    u100,l100 = bb(f['c'],100,0.5,2); u10,l10 = bb(f['c'],10,0.5,2)
    valid = u100.notna()&u10.notna()
    up = (f['c']>u100)&(f['c']>u10)&valid
    dn = (f['c']<l100)&(f['c']<l10)&valid
    return up, dn, valid, u100, l100, u10, l10

def daily_stats(x, ntr=None):
    x = np.asarray(x,float)
    cum = np.cumsum(x); dd = float((cum-np.maximum.accumulate(cum)).min()) if len(x) else 0.0
    return {'days':len(x),'total':round(float(x.sum()),1),'mean':round(float(x.mean()),2) if len(x) else 0,
            'green_pct':round(100*float((x>0).mean()),1) if len(x) else 0,
            'worst':round(float(x.min()),1) if len(x) else 0,'best':round(float(x.max()),1) if len(x) else 0,
            'maxdd':round(dd,1),'m_over_w':(round(float(x.mean()/abs(x.min())),4) if len(x) and x.min()<0 else None),
            'tr_per_day':(round(float(ntr.mean()),2) if ntr is not None else None)}

out={}
for sym in SYMS:
    df = pd.read_parquet(f'data/clean/{sym}_m1.parquet')
    pip, comm = meta[sym]['pip'], meta[sym]['comm_slip_rt_pips']
    frames = {tf: resample(df, tf) for tf in {t for lad in LADDERS15 for t in lad}}
    dc = df.groupby(df['t'].dt.normalize()).size()
    day_index = dc[dc>=300].index.values.astype('datetime64[D]')
    for li, lad in enumerate(LADDERS15):
        L,M,H = lad
        fL, fM, fH = frames[L], frames[M], frames[H]
        upL, dnL, vL, u100L, l100L, u10L, l10L = band_flags(fL)
        upM, dnM, vM, *_ = band_flags(fM)
        upH, dnH, vH, *_ = band_flags(fH)
        sma50 = fL['c'].rolling(50).mean()
        lc = fL['close_time']
        gupM = map_flag(upM, vM, fM['close_time'], lc); gdnM = map_flag(dnM, vM, fM['close_time'], lc)
        gupH = map_flag(upH, vH, fH['close_time'], lc); gdnH = map_flag(dnH, vH, fH['close_time'], lc)
        c = fL['c']; lo = fL['l']; hi = fL['h']
        base_valid = vL & sma50.notna()
        # initial entries: full stack state, edge-triggered
        Gup = (upL & base_valid).values & gupM & gupH & (c>sma50).values
        Gdn = (dnL & base_valid).values & gdnM & gdnH & (c<sma50).values
        edge_up = Gup & ~np.concatenate([[False],Gup[:-1]])
        edge_dn = Gdn & ~np.concatenate([[False],Gdn[:-1]])
        # re-entries: touch or cross-up of LTF upper BB10, gated by SMA50 vs BB100 band and close vs SMA50
        touch_up = (c>u10L) & ((lo<=u10L) | (c.shift(1)<=u10L.shift(1)))
        re_up = (touch_up & (sma50>u100L) & (c>sma50) & base_valid).values
        touch_dn = (c<l10L) & ((hi>=l10L) | (c.shift(1)>=l10L.shift(1)))
        re_dn = (touch_dn & (sma50<l100L) & (c<sma50) & base_valid).values
        entL = np.nonzero(edge_up | re_up)[0]; entS = np.nonzero(edge_dn | re_dn)[0]
        # exits: state cross of SMA50
        exit_valid = base_valid.values
        exL_t = lc.values[( (c<sma50).values & exit_valid )]
        exS_t = lc.values[( (c>sma50).values & exit_valid )]
        lt = {'open_time':fL['open_time'].values,'o':fL['o'].values,'c':fL['c'].values,'spread':fL['spread'].values}
        trades = simulate(lt, entL, entS, exL_t, exS_t, pip, comm, want_trades=True)
        if not trades:
            out[f'{sym}_L{li}'] = {'ladder':lad,'n_trades':0}; continue
        tp = np.array([t[3] for t in trades]); gi = np.array([t[1] for t in trades])
        btp = np.array([t[5] for t in trades]); hold = np.array([t[6] for t in trades])
        sides = np.array([t[2] for t in trades])
        days_of_trades = lt['open_time'][gi].astype('datetime64[D]')
        # valid trading window starts at first entry candidate availability
        first_ok = lt['open_time'][np.nonzero(base_valid.values & (gupM|gdnM|True))[0][0]].astype('datetime64[D]')
        didx = day_index[day_index >= max(first_ok, day_index[0])]
        daily = np.zeros(len(didx)); ntr = np.zeros(len(didx))
        pos = np.searchsorted(didx, days_of_trades)
        okm = (pos>=0)&(pos<len(didx))
        np.add.at(daily, pos[okm], tp[okm]); np.add.at(ntr, pos[okm], 1)
        pre, last30 = daily[:-30], daily[-30:]
        w = tp[tp>0]; l = tp[tp<=0]
        res = {'ladder':lad, 'n_trades':int(len(tp)), 'wr':round(100*float((tp>0).mean()),1),
               'net_pips':round(float(tp.sum()),1),
               'avg_win':round(float(w.mean()),2) if len(w) else None,
               'avg_loss':round(float(l.mean()),2) if len(l) else None,
               'longs_net':round(float(tp[sides>0].sum()),1),'shorts_net':round(float(tp[sides<0].sum()),1),
               'med_btp':int(np.median(btp[btp>0])) if (btp>0).any() else None,
               'never_profit_pct':round(100*float((btp<0).mean()),1),
               'med_hold_bars':int(np.median(hold)),
               'full':daily_stats(daily,ntr),'pre':daily_stats(pre),'last30':daily_stats(last30)}
        if len(pre) and pre.min()<0:
            sc = 4.0/abs(pre.min())
            res['sizing'] = {'implied_mean_daily_pct_pre':round(float(pre.mean()*sc),3),
                             'implied_mean_daily_pct_last30':round(float(last30.mean()*sc),3)}
        out[f'{sym}_L{li}'] = res
        print(f"{sym} L{li} {lad}: n={res['n_trades']} WR={res['wr']}% net={res['net_pips']} "
              f"({res['full']['mean']}/day, grn {res['full']['green_pct']}%, worst {res['full']['worst']}) "
              f"last30={res['last30']['total']} L/S={res['longs_net']}/{res['shorts_net']}")
json.dump(out, open('results/gv15_report.json','w'), indent=1, default=str)
print('GV15 DONE')
