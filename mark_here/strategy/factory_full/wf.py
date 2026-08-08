"""Walk-forward selection + untouched 30-trading-day OOS + final-config trade stats (incl. bars-to-profit)."""
import pandas as pd, numpy as np, json
from engine import LADDERS, CONFIGS, resample, build_signals, exit_events, simulate

SYMS = ['EURUSD','GBPUSD','XAUUSD','US500']
meta = json.load(open('data/clean/meta.json'))
TUNE, TEST, MIN_TR, MIN_TR_FALLBACK = 252, 63, 25, 10

def pick(net, ntr, cols):
    """argmax net over configs with min trades on given day-columns."""
    tn = net[:, cols].sum(1); tt = ntr[:, cols].sum(1)
    for mt in (MIN_TR, MIN_TR_FALLBACK):
        ok = tt >= mt
        if ok.any():
            k = int(np.argmax(np.where(ok, tn, -1e18)))
            return k, int(tt[k]), float(tn[k])
    return None, 0, 0.0

def daily_stats(x, ntr=None):
    x = np.asarray(x, dtype=float)
    if len(x)==0: return None
    cum = np.cumsum(x); dd = float((cum - np.maximum.accumulate(cum)).min())
    act = x[x!=0]
    return {'days':int(len(x)),'total':round(float(x.sum()),1),'mean':round(float(x.mean()),2),
            'green_pct':round(100*float((x>0).mean()),1),'zero_pct':round(100*float((x==0).mean()),1),
            'worst':round(float(x.min()),1),'best':round(float(x.max()),1),'maxdd':round(dd,1),
            'tr_per_day':(round(float(ntr.mean()),2) if ntr is not None else None),
            'mean_over_absworst':(round(float(x.mean()/abs(x.min())),4) if x.min()<0 else None)}

out = {}
frames_cache = {}
for sym in SYMS:
    df = pd.read_parquet(f'data/clean/{sym}_m1.parquet')
    frames_cache[sym] = {tf: resample(df, tf) for tf in ['1m','5m','15m','30m','1h','4h','1d','1w']}

for strat in ['GV013','GV014']:
    for li, lad in enumerate(LADDERS):
        key = f'{strat}_L{li}'
        out[key] = {'ladder':lad, 'symbols':{}}
        for sym in SYMS:
            z = np.load(f'results/{strat}_L{li}_{sym}.npz', allow_pickle=True)
            net, ntr = z['net'], z['ntr']
            days = np.load(f'results/{sym}_days.npy')
            tstart = z['tstart']
            # tradable day range
            if np.isnat(tstart): continue
            d0 = np.searchsorted(days, tstart.astype('datetime64[D]'))
            oos_lo = len(days) - 30
            pre = np.arange(d0, oos_lo)
            oos = np.arange(oos_lo, len(days))
            if len(pre) < TUNE + TEST:
                out[key]['symbols'][sym] = {'skip': f'insufficient history ({len(pre)} pre days)'}
                continue
            # rolling folds
            wf_net, wf_ntr, folds = [], [], []
            start = 0
            while start + TUNE + TEST <= len(pre):
                tune_cols = pre[start:start+TUNE]; test_cols = pre[start+TUNE:start+TUNE+TEST]
                k, tt, tn = pick(net, ntr, tune_cols)
                if k is None:
                    wf_net.append(np.zeros(len(test_cols))); wf_ntr.append(np.zeros(len(test_cols)))
                    folds.append({'cfg':None})
                else:
                    wf_net.append(net[k, test_cols]); wf_ntr.append(ntr[k, test_cols])
                    folds.append({'cfg':CONFIGS[k], 'tune_net':round(tn,1), 'tune_tr':tt,
                                  'test_net':round(float(net[k,test_cols].sum()),1)})
                start += TEST
            wf_x = np.concatenate(wf_net); wf_n = np.concatenate(wf_ntr)
            # final config on ALL pre days -> untouched OOS 30
            kf, ttf, tnf = pick(net, ntr, pre)
            res = {'pre_days':len(pre), 'folds':folds,
                   'wf': daily_stats(wf_x, wf_n),
                   'final_cfg': (CONFIGS[kf] if kf is not None else None),
                   'final_pre_net': round(tnf,1), 'final_pre_tr': ttf}
            if kf is not None:
                res['oos30'] = daily_stats(net[kf, oos], ntr[kf, oos])
                res['oos30_dates'] = [str(days[oos][0]), str(days[oos][-1])]
                # trade-level stats for final config over pre+oos
                L, M, H = lad
                fr = frames_cache[sym]
                sig_up, sig_dn, _, _ = build_signals(strat, fr, L, M, H)
                fL = fr[L]
                lt = {'open_time': fL['open_time'].values, 'o': fL['o'].values,
                      'c': fL['c'].values, 'spread': fL['spread'].values}
                etf, p, s = CONFIGS[kf]
                fT = fr[L] if etf=='LTF' else fr[M]
                exL_t, exS_t = exit_events(fT, p, s)
                trades = simulate(lt, np.nonzero(sig_up)[0], np.nonzero(sig_dn)[0],
                                  exL_t, exS_t, meta[sym]['pip'], meta[sym]['comm_slip_rt_pips'], want_trades=True)
                tp = np.array([t[3] for t in trades]); btp = np.array([t[5] for t in trades])
                hold = np.array([t[6] for t in trades]); cen = np.array([t[4] for t in trades])
                w = tp[tp>0]; l = tp[tp<=0]
                res['trades'] = {'n':len(tp), 'wr':round(100*float((tp>0).mean()),1),
                    'avg_win':round(float(w.mean()),2) if len(w) else None,
                    'avg_loss':round(float(l.mean()),2) if len(l) else None,
                    'med_btp_bars':int(np.median(btp[btp>0])) if (btp>0).any() else None,
                    'p75_btp_bars':int(np.percentile(btp[btp>0],75)) if (btp>0).any() else None,
                    'never_profit_pct':round(100*float((btp<0).mean()),1),
                    'med_hold_bars':int(np.median(hold)), 'censored':int(cen.sum()),
                    'total_pips':round(float(tp.sum()),1)}
                # sizing overlay: leverage so worst PRE day = -4% -> implied mean daily %
                pre_x = net[kf, pre]
                if pre_x.min() < 0:
                    scale = 4.0/abs(pre_x.min())
                    res['sizing'] = {'scale_pct_per_pip':round(scale,5),
                        'implied_mean_daily_pct_pre':round(float(pre_x.mean()*scale),3),
                        'implied_mean_daily_pct_oos30':round(float(net[kf,oos].mean()*scale),3),
                        'oos30_worst_pct':round(float(net[kf,oos].min()*scale),2)}
            out[key]['symbols'][sym] = res

json.dump(out, open('results/wf_report.json','w'), indent=1, default=str)
# compact leaderboard
rows = []
for key, v in out.items():
    for sym, r in v['symbols'].items():
        if 'wf' in r and r['wf']:
            rows.append((key, sym, r['wf']['total'], r['wf']['mean'], r['wf']['green_pct'],
                         r['wf']['worst'], r.get('oos30',{}).get('total') if r.get('oos30') else None,
                         str(r.get('final_cfg')), r.get('trades',{}).get('n')))
rows.sort(key=lambda r: -(r[2] or 0))
print(f"{'unit':10s} {'sym':7s} {'WFnet':>9s} {'WF/day':>7s} {'grn%':>5s} {'worst':>8s} {'OOS30':>8s} {'n_tr':>6s}  final_cfg")
for r in rows:
    print(f"{r[0]:10s} {r[1]:7s} {r[2]:9.0f} {r[3]:7.2f} {r[4]:5.1f} {r[5]:8.1f} {(r[6] if r[6] is not None else float('nan')):8.1f} {(r[8] or 0):6d}  {r[7]}")
print('WF DONE')
