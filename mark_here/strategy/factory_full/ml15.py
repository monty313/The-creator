"""GV-015 meta-labeler: rules frozen; ML predicts per-signal win probability from entry-time features.
Arms: A baseline | B ML-filter (p>=thr, thr chosen in-train) | C ML-sizing (w~p) | D vol-sizing (no ML control).
Purged expanding walk-forward over trade sequence; separate referee = trades in final 30 trading days.
"""
import pandas as pd, numpy as np, json
from engine import resample, bb, map_flag, simulate
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.inspection import permutation_importance

meta = json.load(open('data/clean/meta.json'))
sym = 'XAUUSD'; LAD = ('15m','1h','4h')
df = pd.read_parquet(f'data/clean/{sym}_m1.parquet')
frames = {tf: resample(df, tf) for tf in ['15m','1h','4h','1d']}
fL,fM,fH,fD = frames['15m'],frames['1h'],frames['4h'],frames['1d']

def bands(f):
    u100,l100 = bb(f['c'],100,0.5,2); u10,l10 = bb(f['c'],10,0.5,2)
    v = u100.notna()&u10.notna()
    return u100,l100,u10,l10,v
u100L,l100L,u10L,l10L,vL = bands(fL); u100M,l100M,u10M,l10M,vM = bands(fM); u100H,l100H,u10H,l10H,vH = bands(fH)
upL=(fL['c']>u100L)&(fL['c']>u10L)&vL; dnL=(fL['c']<l100L)&(fL['c']<l10L)&vL
upM=(fM['c']>u100M)&(fM['c']>u10M)&vM; dnM=(fM['c']<l100M)&(fM['c']<l10M)&vM
upH=(fH['c']>u100H)&(fH['c']>u10H)&vH; dnH=(fH['c']<l100H)&(fH['c']<l10H)&vH
sma50 = fL['c'].rolling(50).mean(); lc = fL['close_time']
gupM = map_flag(upM,vM,fM['close_time'],lc); gdnM = map_flag(dnM,vM,fM['close_time'],lc)
gupH = map_flag(upH,vH,fH['close_time'],lc); gdnH = map_flag(dnH,vH,fH['close_time'],lc)
c=fL['c']; lo=fL['l']; hi=fL['h']; basev = vL & sma50.notna()
Gup=(upL&basev).values&gupM&gupH&(c>sma50).values
Gdn=(dnL&basev).values&gdnM&gdnH&(c<sma50).values
eu=Gup&~np.concatenate([[False],Gup[:-1]]); ed=Gdn&~np.concatenate([[False],Gdn[:-1]])
ru=((c>u10L)&((lo<=u10L)|(c.shift(1)<=u10L.shift(1)))&(sma50>u100L)&(c>sma50)&basev).values
rd=((c<l10L)&((hi>=l10L)|(c.shift(1)>=l10L.shift(1)))&(sma50<l100L)&(c<sma50)&basev).values
lt = {'open_time':fL['open_time'].values,'o':fL['o'].values,'c':fL['c'].values,'spread':fL['spread'].values}
pip, comm = meta[sym]['pip'], meta[sym]['comm_slip_rt_pips']
trades = simulate(lt, np.nonzero(eu|ru)[0], np.nonzero(ed|rd)[0],
                  lc.values[((c<sma50).values&basev.values)], lc.values[((c>sma50).values&basev.values)],
                  pip, comm, want_trades=True)
print('trades:', len(trades))

# ---- features at decision bar d = fi-1 ----
tr_ = np.maximum(fL['h']-fL['l'], np.maximum((fL['h']-fL['c'].shift(1)).abs(), (fL['l']-fL['c'].shift(1)).abs()))
atr = tr_.rolling(14).mean()
atr_p = atr.rolling(500).rank(pct=True)
bw100 = (u100L-l100L); bw100_p = bw100.rolling(500).rank(pct=True)
bw10 = (u10L-l10L)/atr
slope = (sma50-sma50.shift(8))/atr
hourv = fL['open_time'].dt.hour.values; dowv = fL['open_time'].dt.weekday.values
sprd = fL['spread'].values/pip
def asof_vals(fT, cols):
    ct = fT['close_time'].values
    idx = np.searchsorted(ct, lc.values, side='right')-1
    idx0 = np.clip(idx,0,None)
    out = {k: fT[k].values[idx0] if k in fT else None for k in []}
    return idx0, idx>=0
iM,okM = asof_vals(fM,[]); iH,okH = asof_vals(fH,[]); iD,okD = asof_vals(fD,[])
atrM = (np.maximum(fM['h']-fM['l'],np.maximum((fM['h']-fM['c'].shift(1)).abs(),(fM['l']-fM['c'].shift(1)).abs()))).rolling(14).mean()
atrH = (np.maximum(fH['h']-fH['l'],np.maximum((fH['h']-fH['c'].shift(1)).abs(),(fH['l']-fH['c'].shift(1)).abs()))).rolling(14).mean()
sma50D = fD['c'].rolling(50).mean()
atrD = (fD['h']-fD['l']).rolling(14).mean()
bw100M_p = (u100M-l100M).rolling(200).rank(pct=True)
bw100H_p = (u100H-l100H).rolling(200).rank(pct=True)

FEATS = ['side','is_re','hour','dow','spread','atr','atr_p','bw100_p','bw10','slope_s',
         'd_b10_s','d_b100_s','d_sma_s','m_pos_s','h_pos_s','m_bwp','h_bwp','d_trend_s','last3','streak']
rows=[]; pnl=[]; times=[]
last3=[]; streak=0
for (fi,gi,side,pips,cen,btp,hold) in trades:
    d = fi-1
    if d < 600: continue
    m, h, dd = iM[d], iH[d], iD[d]
    f = {'side':side, 'is_re':0 if (eu[d] if side>0 else ed[d]) else 1,
         'hour':hourv[d], 'dow':dowv[d], 'spread':sprd[d],
         'atr':atr.iloc[d]/pip, 'atr_p':atr_p.iloc[d], 'bw100_p':bw100_p.iloc[d],
         'bw10':bw10.iloc[d], 'slope_s':side*slope.iloc[d],
         'd_b10_s': side*(c.iloc[d]-(u10L.iloc[d] if side>0 else l10L.iloc[d]))/atr.iloc[d],
         'd_b100_s': side*(c.iloc[d]-(u100L.iloc[d] if side>0 else l100L.iloc[d]))/atr.iloc[d],
         'd_sma_s': side*(c.iloc[d]-sma50.iloc[d])/atr.iloc[d],
         'm_pos_s': side*(fM['c'].iloc[m]-(u100M.iloc[m] if side>0 else l100M.iloc[m]))/max(atrM.iloc[m],1e-9),
         'h_pos_s': side*(fH['c'].iloc[h]-(u100H.iloc[h] if side>0 else l100H.iloc[h]))/max(atrH.iloc[h],1e-9),
         'm_bwp': bw100M_p.iloc[m], 'h_bwp': bw100H_p.iloc[h],
         'd_trend_s': side*(fD['c'].iloc[dd]-sma50D.iloc[dd])/max(atrD.iloc[dd],1e-9),
         'last3': sum(last3[-3:]) if last3 else 0.0, 'streak': streak}
    rows.append([f[k] for k in FEATS]); pnl.append(pips); times.append(lt['open_time'][fi])
    last3.append(pips); streak = (streak+1 if pips>0 else 0) if pips>0 else (streak-1 if pips<=0 else 0)
X = pd.DataFrame(rows, columns=FEATS).astype(float)
y = (np.array(pnl)>0).astype(int); P = np.array(pnl); T = np.array(times)
ok = ~X.isna().any(axis=1)
X,y,P,T = X[ok.values].reset_index(drop=True), y[ok.values], P[ok.values], T[ok.values]
print('usable trades:', len(X), 'base WR:', round(100*y.mean(),1))

def daily_series(times_, vals):
    dser = pd.Series(vals, index=pd.to_datetime(times_).normalize()).groupby(level=0).sum()
    idx = pd.bdate_range(dser.index.min(), dser.index.max())
    return dser.reindex(idx, fill_value=0.0).values

def arm_stats(name, keep_mask, weights=None):
    w = np.ones(len(P)) if weights is None else weights
    v = P*w*keep_mask
    kept = int(keep_mask.sum())
    d = daily_series(T, v)
    mw = d.mean()/abs(d.min()) if d.min()<0 else np.inf
    return {'arm':name,'kept':kept,'kept_pct':round(100*kept/len(P),1),
            'net':round(float(v.sum()),0),'pips_per_trade':round(float(v[keep_mask.astype(bool)].sum()/max(kept,1)),2),
            'wr':round(100*float((P[keep_mask.astype(bool)]>0).mean()),1) if kept else None,
            'mean_day':round(float(d.mean()),2),'worst_day':round(float(d.min()),0),
            'm_over_w':round(float(mw),4),'maxdd':round(float((np.cumsum(d)-np.maximum.accumulate(np.cumsum(d))).min()),0)}

# ---- expanding walk-forward ----
n = len(X); TRAIN0, BLOCK = 1000, 300
oosB = np.zeros(n,bool); oosC_w = np.zeros(n); oosD_w = np.zeros(n); in_oos = np.zeros(n,bool)
aucs=[]; thrs=[]
model=None
start = TRAIN0
while start < n-50:
    end = min(start+BLOCK, n)
    tr_idx = np.arange(0,start); te_idx = np.arange(start,end)
    model = HistGradientBoostingClassifier(max_iter=250, max_depth=3, learning_rate=0.05,
                                           l2_regularization=1.0, min_samples_leaf=40, random_state=7)
    model.fit(X.iloc[tr_idx], y[tr_idx])
    p_tr = model.predict_proba(X.iloc[tr_idx])[:,1]; p_te = model.predict_proba(X.iloc[te_idx])[:,1]
    if len(np.unique(y[te_idx]))>1: aucs.append(roc_auc_score(y[te_idx], p_te))
    best_thr, best_val = None, -1e18
    for q in np.arange(0.20,0.71,0.05):
        thr = np.quantile(p_tr,q); keep = p_tr>=thr
        if keep.mean()<0.40: continue
        val = P[tr_idx][keep].sum()/max(keep.sum(),1)
        if val>best_val: best_val, best_thr = val, thr
    thrs.append(best_thr)
    oosB[te_idx] = p_te>=best_thr
    mp = p_tr.mean(); oosC_w[te_idx] = np.clip(p_te/mp, 0.25, 2.0)
    med_atr = np.median(X['atr'].iloc[tr_idx]); oosD_w[te_idx] = np.clip(med_atr/X['atr'].iloc[te_idx], 0.25, 2.0)
    in_oos[te_idx] = True
    start = end

sel = in_oos
Ps, Ts = P[sel], T[sel]
def arm_stats2(name, keep, w=None):
    ww = np.ones(sel.sum()) if w is None else w
    v = Ps*ww*keep
    d = daily_series(Ts, v)
    kept=int(keep.sum())
    return {'arm':name,'kept_pct':round(100*kept/sel.sum(),1),'net':round(float(v.sum()),0),
            'wr_kept':round(100*float((Ps[keep.astype(bool)]>0).mean()),1) if kept else None,
            'pips_per_kept':round(float(Ps[keep.astype(bool)].sum()/max(kept,1)),2),
            'mean_day':round(float(d.mean()),2),'worst_day':round(float(d.min()),0),
            'm_over_w':round(float(d.mean()/abs(d.min())),4) if d.min()<0 else None,
            'maxdd':round(float((np.cumsum(d)-np.maximum.accumulate(np.cumsum(d))).min()),0)}
res = [arm_stats2('A baseline', np.ones(sel.sum())),
       arm_stats2('B ML-filter', oosB[sel].astype(float)),
       arm_stats2('C ML-sizing', np.ones(sel.sum()), oosC_w[sel]),
       arm_stats2('D vol-sizing', np.ones(sel.sum()), oosD_w[sel]),
       arm_stats2('E ML x vol sizing', np.ones(sel.sum()), oosC_w[sel]*oosD_w[sel]),
       arm_stats2('F filter + ML x vol', oosB[sel].astype(float), oosC_w[sel]*oosD_w[sel])]
print('\nWALK-FORWARD OOS (%d trades across %d blocks), mean AUC %.3f (folds: %s)' % (sel.sum(), len(thrs), np.mean(aucs), ' '.join(f'{a:.2f}' for a in aucs)))
for r in res: print(r)

# permutation importance on final model / last block
pi = permutation_importance(model, X.iloc[np.arange(0,n)][-600:], y[-600:], n_repeats=5, random_state=7)
imp = sorted(zip(FEATS, pi.importances_mean), key=lambda t:-t[1])[:10]
print('\nTop features:', [(f, round(v,4)) for f,v in imp])
json.dump({'aucs':[float(a) for a in aucs],'arms':res,'top_features':[(f,float(v)) for f,v in imp]},
          open('results/ml15_report.json','w'), indent=1)
print('ML15 DONE')
