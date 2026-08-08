"""Prep: parse MT5 M1 exports -> clean parquet + meta. Costs use recorded spread (points->price), zero-fill by hour-of-day median."""
import pandas as pd, numpy as np, json, os

SYMS = ['EURUSD','GBPUSD','XAUUSD','US500','US30']
POINT = {'EURUSD':1e-5,'GBPUSD':1e-5,'XAUUSD':0.01,'US500':0.01,'US30':0.01}
PIP   = {'EURUSD':1e-4,'GBPUSD':1e-4,'XAUUSD':0.1,'US500':1.0,'US30':1.0}
# round-trip commission+slippage in PIPs (spread handled separately per-bar):
# FX: FTMO-style $3/side/lot = 0.6 pip RT + 0.2 pip RT slippage
# XAU: $6RT/lot = 0.6 pip RT + 0.4 slippage ; indices: no commission, slippage only
COMM_SLIP_RT_PIPS = {'EURUSD':0.8,'GBPUSD':0.8,'XAUUSD':1.0,'US500':0.4,'US30':1.0}

os.makedirs('data/clean', exist_ok=True)
meta = {}
for sym in SYMS:
    df = pd.read_csv(f'data/{sym}_M1_export.csv', sep='\t')
    df.columns = [c.strip('<>').lower() for c in df.columns]
    t = pd.to_datetime(df['date']+' '+df['time'], format='%Y.%m.%d %H:%M:%S')
    df = pd.DataFrame({'t':t,'o':df['open'].astype('float64'),'h':df['high'].astype('float64'),
                       'l':df['low'].astype('float64'),'c':df['close'].astype('float64'),
                       'spread_pts':df['spread'].astype('float64')})
    df = df.drop_duplicates(subset='t').sort_values('t').reset_index(drop=True)
    # spread in price units; zero-fill by hour-of-day median of nonzero
    sp_price = df['spread_pts']*POINT[sym]
    hr = df['t'].dt.hour
    nz = sp_price>0
    hmed = sp_price[nz].groupby(hr[nz]).median()
    fill = hr.map(hmed).fillna(sp_price[nz].median() if nz.any() else 0.0)
    df['spread'] = np.where(nz, sp_price, fill)
    # usable M1 regime: earliest good day (>=300 bars) from which >=90% of weekdays to end are good (tolerates holes)
    dcount = df.groupby(df['t'].dt.normalize()).size()
    good = dcount[dcount>=300].index.sort_values()
    if len(good)==0: raise SystemExit(f'{sym}: no M1 days')
    end = df['t'].iloc[-1].normalize()
    m1_start = None
    for g in good:
        wd = np.busday_count(g.date(), (end+pd.Timedelta(days=1)).date())
        cov = (good>=g).sum()/max(wd,1)
        if cov >= 0.90:
            m1_start = g; break
    if m1_start is None: m1_start = good[-1]
    m1 = df[df['t']>=m1_start].reset_index(drop=True)
    m1.to_parquet(f'data/clean/{sym}_m1.parquet')
    # full file (any granularity) kept for HTF-only use (US30 pre-M1 era is H1)
    df.to_parquet(f'data/clean/{sym}_full.parquet')
    meta[sym] = {'point':POINT[sym],'pip':PIP[sym],'comm_slip_rt_pips':COMM_SLIP_RT_PIPS[sym],
                 'm1_start':str(m1_start),'m1_rows':len(m1),'full_rows':len(df),
                 'first':str(df['t'].iloc[0]),'last':str(df['t'].iloc[-1]),
                 'median_spread_pips':float((df['spread']/PIP[sym]).median()),
                 'p90_spread_pips':float((df['spread']/PIP[sym]).quantile(0.9))}
    print(sym, meta[sym])
json.dump(meta, open('data/clean/meta.json','w'), indent=1)
print('done')
