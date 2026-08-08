"""Time-stop exit family: base shifted-SMA exit + 'kill if not net-green within N LTF candles'.
Motivated by candles-to-profit data: winners green in 1-3 candles, ~25% of trades never green.
Grid: 48 base exit configs x TS in {None,2,3,5,8,13} = 288 per unit. GV-014 only, WF protocol unchanged."""
import pandas as pd, numpy as np, json, time
from engine import LADDERS, CONFIGS, resample, build_signals, exit_events

import sys
meta = json.load(open('data/clean/meta.json'))
SYMS = sys.argv[1:] if len(sys.argv)>1 else ['EURUSD','GBPUSD','XAUUSD','US500']
TS_GRID = [None,2,3,5,8,13]
TUNE, TEST, MIN_TR, MIN_TR_FB = 252, 63, 25, 10

def simulate_ts(lt, entL, entS, exL_t, exS_t, pip, comm, ts_n):
    ot=lt['open_time']; o=lt['o']; c=lt['c']; sp=lt['spread']; n=len(ot)
    cands = [(i+1,+1) for i in entL if i+1<n] + [(i+1,-1) for i in entS if i+1<n]
    cands.sort()
    out=[]; pos_end=-1
    for fi, side in cands:
        if fi <= pos_end: continue
        ft = ot[fi]
        ext = exL_t if side>0 else exS_t
        j = np.searchsorted(ext, ft, side='right')
        if j >= len(ext): gi=n-1; cen=True
        else:
            gi=int(np.searchsorted(ot, ext[j], side='left')); cen=False
            if gi>=n: gi=n-1; cen=True
        if gi<=fi: gi=min(fi+1,n-1)
        if ts_n is not None:
            we = min(fi+ts_n, gi)   # check closes fi..we-1
            seg = c[fi:we]
            if side>0: fl = (seg-(o[fi]+sp[fi]))/pip - comm
            else:      fl = (o[fi]-(seg+sp[fi:we]))/pip - comm
            if not (fl>0).any() and fi+ts_n < gi:
                gi = min(fi+ts_n, n-1); cen=False
        if side>0:
            entry=o[fi]+sp[fi]; exitp = c[gi] if cen else o[gi]
            pips=(exitp-entry)/pip - comm
        else:
            entry=o[fi]; exitp=(c[gi]+sp[gi]) if cen else (o[gi]+sp[gi])
            pips=(entry-exitp)/pip - comm
        out.append((fi,gi,side,pips)); pos_end=gi
    return out

def pick(net, ntr, cols):
    tn=net[:,cols].sum(1); tt=ntr[:,cols].sum(1)
    for mt in (MIN_TR, MIN_TR_FB):
        ok=tt>=mt
        if ok.any(): return int(np.argmax(np.where(ok,tn,-1e18)))
    return None

ALLCFG=[(cfg, ts) for cfg in CONFIGS for ts in TS_GRID]
log=open('results/ts.log','a',buffering=1)
res={}
for sym in SYMS:
    df=pd.read_parquet(f'data/clean/{sym}_m1.parquet')
    frames={tf:resample(df,tf) for tf in ['1m','5m','15m','30m','1h','4h','1d','1w']}
    days=np.load(f'results/{sym}_days.npy')
    pip=meta[sym]['pip']; comm=meta[sym]['comm_slip_rt_pips']
    for li,lad in enumerate(LADDERS):
        t0=time.time()
        su,sd,sv,_=build_signals('GV014',frames,*lad)
        fL=frames[lad[0]]
        lt={'open_time':fL['open_time'].values,'o':fL['o'].values,'c':fL['c'].values,'spread':fL['spread'].values}
        entL,entS=np.nonzero(su)[0],np.nonzero(sd)[0]
        vidx=np.nonzero(sv)[0]
        if not len(vidx): continue
        d0=np.searchsorted(days, lt['open_time'][vidx[0]].astype('datetime64[D]'))
        D=len(days); dpos=np.searchsorted(days, lt['open_time'].astype('datetime64[D]'))
        net=np.zeros((len(ALLCFG),D)); ntr=np.zeros((len(ALLCFG),D),dtype=np.int32)
        exit_cache={}
        for k,((etf,p,s),ts) in enumerate(ALLCFG):
            if (etf,p,s) not in exit_cache:
                fT=frames[lad[0]] if etf=='LTF' else frames[lad[1]]
                exit_cache[(etf,p,s)]=exit_events(fT,p,s)
            eL,eS=exit_cache[(etf,p,s)]
            for fi,gi,side,pips in simulate_ts(lt,entL,entS,eL,eS,pip,comm,ts):
                d=dpos[gi]
                if 0<=d<D: net[k,d]+=pips; ntr[k,d]+=1
        oos_lo=D-30; pre=np.arange(d0,oos_lo); oos=np.arange(oos_lo,D)
        if len(pre)<TUNE+TEST:
            log.write(f'{sym} L{li}: skip\n'); continue
        wf=[]; start=0
        while start+TUNE+TEST<=len(pre):
            kk=pick(net,ntr,pre[start:start+TUNE])
            wf.append(net[kk,pre[start+TUNE:start+TUNE+TEST]] if kk is not None else np.zeros(TEST))
            start+=TEST
        x=np.concatenate(wf); kf=pick(net,ntr,pre)
        o=net[kf,oos] if kf is not None else np.zeros(30)
        res[f'{sym}_L{li}']={'ladder':lad,'wf_total':round(float(x.sum()),1),'wf_day':round(float(x.mean()),2),
            'green':round(100*float((x>0).mean()),1),'worst':round(float(x.min()),1),
            'm_over_w':round(float(x.mean()/abs(x.min())),4) if x.min()<0 else None,
            'oos30':round(float(o.sum()),1),'final_cfg':str(ALLCFG[kf]) if kf is not None else None,
            'tr_day':round(float(ntr[kf,pre].mean()),2) if kf is not None else 0}
        log.write(f"{sym} L{li} {lad}: WF {res[f'{sym}_L{li}']['wf_total']} ({res[f'{sym}_L{li}']['wf_day']}/d) OOS30 {res[f'{sym}_L{li}']['oos30']} cfg {res[f'{sym}_L{li}']['final_cfg']} {time.time()-t0:.0f}s\n")
import os
old = json.load(open('results/ts_report.json')) if os.path.exists('results/ts_report.json') else {}
old.update(res)
json.dump(old,open('results/ts_report.json','w'),indent=1)
log.write(f'TS DONE {SYMS}\n')
print('TS DONE', SYMS)
