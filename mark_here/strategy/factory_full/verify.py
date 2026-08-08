"""Verification: (1) causality poison test, (2) independent spot-check of entries, (3) manual cost audit, (4) long/short split."""
import pandas as pd, numpy as np, json
from engine import resample, build_signals, exit_events, simulate, CONFIGS

meta = json.load(open('data/clean/meta.json'))
sym, strat, lad = 'XAUUSD', 'GV014', ('5m','30m','1h')
df = pd.read_parquet(f'data/clean/{sym}_m1.parquet')
frames = {tf: resample(df, tf) for tf in ['5m','30m','1h']}
sig_up, sig_dn, sv, _ = build_signals(strat, frames, *lad)

# --- 1) POISON TEST: corrupt the last 60 days of M1; earlier signals must be identical
cut = df['t'].iloc[-1] - pd.Timedelta(days=60)
dfp = df.copy()
mask = dfp['t'] > cut
rng = np.random.default_rng(7)
for col in ['o','h','l','c']:
    dfp.loc[mask, col] = dfp.loc[mask, col].values * (1 + 0.02*rng.standard_normal(mask.sum()))
framesp = {tf: resample(dfp, tf) for tf in ['5m','30m','1h']}
sig_up_p, sig_dn_p, _, _ = build_signals(strat, framesp, *lad)
fL = frames['5m']
safe = fL['close_time'] <= cut  # bars fully before poison zone
same = (sig_up[safe.values] == sig_up_p[safe.values]).all() and (sig_dn[safe.values] == sig_dn_p[safe.values]).all()
print('POISON TEST (no lookahead):', 'PASS' if same else 'FAIL')

# exits causality too
exL, exS = exit_events(frames['30m'], 4, 1)
exLp, exSp = exit_events(framesp['30m'], 4, 1)
exL_safe = exL[exL <= np.datetime64(cut)]
print('POISON TEST exits:', 'PASS' if (exL_safe == exLp[:len(exL_safe)]).all() else 'FAIL')

# --- 2) INDEPENDENT SPOT-CHECK of 2 long entries (recompute BB conditions directly)
idx = np.nonzero(sig_up)[0]
pick = [idx[len(idx)//3], idx[2*len(idx)//3]]
f5, f30, f1h = frames['5m'], frames['30m'], frames['1h']
def bb_direct(s, n, dev):
    m = s.rolling(n).mean(); sd = s.rolling(n).std(ddof=0)
    return m+dev*sd, m-dev*sd
u20_5, _ = bb_direct(f5['c'],20,1.0); u200_5,_ = bb_direct(f5['c'],200,1.0)
u20_30,_ = bb_direct(f30['c'],20,1.0); u200_30,_ = bb_direct(f30['c'],200,1.0)
u20_1h,_ = bb_direct(f1h['c'],20,1.0); u200_1h,_ = bb_direct(f1h['c'],200,1.0)
for i in pick:
    ct = f5['close_time'].iloc[i]
    j30 = np.searchsorted(f30['close_time'].values, ct, side='right')-1
    j1h = np.searchsorted(f1h['close_time'].values, ct, side='right')-1
    c5, c5p = f5['c'].iloc[i], f5['c'].iloc[i-1]
    cond_trig = (c5 < u20_5.iloc[i]) and (c5p >= u20_5.iloc[i-1])
    cond_30 = (f30['c'].iloc[j30] > u200_30.iloc[j30]) and (f30['c'].iloc[j30] > u20_30.iloc[j30])
    cond_1h = (f1h['c'].iloc[j1h] > u200_1h.iloc[j1h]) and (f1h['c'].iloc[j1h] > u20_1h.iloc[j1h])
    print(f'entry bar {i} @ {ct}: LTF cross-under={cond_trig}, 30m gravity={cond_30} (bar closed {f30["close_time"].iloc[j30]}), 1h gravity={cond_1h} (bar closed {f1h["close_time"].iloc[j1h]})',
          '=> VALID' if (cond_trig and cond_30 and cond_1h) else '=> MISMATCH')

# --- 3) COST AUDIT: recompute one trade's pips by hand
lt = {'open_time': f5['open_time'].values,'o': f5['o'].values,'c': f5['c'].values,'spread': f5['spread'].values}
exL_t, exS_t = exit_events(f30, 4, 1)
trades = simulate(lt, np.nonzero(sig_up)[0], np.nonzero(sig_dn)[0], exL_t, exS_t, meta[sym]['pip'], meta[sym]['comm_slip_rt_pips'])
fi, gi, side, pips, cen = trades[len(trades)//2]
entry = lt['o'][fi] + (lt['spread'][fi] if side>0 else 0)
exitp = lt['o'][gi] + (0 if side>0 else lt['spread'][gi])
manual = ((exitp-entry) if side>0 else (entry-exitp))/meta[sym]['pip'] - meta[sym]['comm_slip_rt_pips']
print(f'COST AUDIT trade fi={fi} side={side}: engine={pips:.2f} manual={manual:.2f}', 'PASS' if abs(pips-manual)<1e-9 else 'FAIL')
print(f'  entry ask={entry:.2f} (bid {lt["o"][fi]:.2f} + spread {lt["spread"][fi]:.3f}), exit bid={exitp:.2f}, comm+slip={meta[sym]["comm_slip_rt_pips"]} pips RT')

# --- 4) LONG/SHORT split for XAU GV014 top units
for ladname, ladt, cfg in [('L1',('5m','30m','1h'),('MID',4,1)), ('L3',('30m','4h','1d'),('MID',3,1))]:
    fr = {tf: resample(df, tf) for tf in set(ladt)}
    su, sd, _, _ = build_signals('GV014', fr, *ladt)
    fL2 = fr[ladt[0]]
    lt2 = {'open_time': fL2['open_time'].values,'o': fL2['o'].values,'c': fL2['c'].values,'spread': fL2['spread'].values}
    eL, eS = exit_events(fr[ladt[1]], cfg[1], cfg[2])
    trs = simulate(lt2, np.nonzero(su)[0], np.nonzero(sd)[0], eL, eS, meta[sym]['pip'], meta[sym]['comm_slip_rt_pips'])
    tp = np.array([t[3] for t in trs]); sides = np.array([t[2] for t in trs])
    print(f'XAU GV014 {ladname}: longs n={int((sides>0).sum())} pips={tp[sides>0].sum():.0f} | shorts n={int((sides<0).sum())} pips={tp[sides<0].sum():.0f}')
