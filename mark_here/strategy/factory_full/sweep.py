"""Full sweep: 2 strategies x 5 gapped ladders x symbols x 48 exit configs -> daily P&L matrices."""
import pandas as pd, numpy as np, json, os, time, sys
from engine import LADDERS, CONFIGS, resample, run_unit

SYMS = ['EURUSD','GBPUSD','XAUUSD','US500']  # US30 excluded: modern M1 = 3 days only
meta = json.load(open('data/clean/meta.json'))
os.makedirs('results', exist_ok=True)

TFS_NEEDED = sorted({tf for lad in LADDERS for tf in lad}, key=lambda x: ['1m','5m','15m','30m','1h','4h','1d','1w'].index(x))

log = open('results/sweep.log','a', buffering=1)
def P(*a):
    print(*a); log.write(' '.join(map(str,a))+'\n')

for sym in SYMS:
    t0 = time.time()
    df = pd.read_parquet(f'data/clean/{sym}_m1.parquet')
    frames = {tf: resample(df, tf) for tf in TFS_NEEDED}
    # trading-day index: days with >=300 M1 bars
    dc = df.groupby(df['t'].dt.normalize()).size()
    day_index = dc[dc>=300].index.values.astype('datetime64[D]')
    np.save(f'results/{sym}_days.npy', day_index)
    pip = meta[sym]['pip']; comm = meta[sym]['comm_slip_rt_pips']
    P(f'{sym}: m1={len(df)} days={len(day_index)} frames_built={time.time()-t0:.0f}s')
    for strat in ['GV013','GV014']:
        for li, lad in enumerate(LADDERS):
            t1 = time.time()
            net, ntr, tstart, nL, nS = run_unit(strat, lad, frames, pip, comm, day_index)
            np.savez_compressed(f'results/{strat}_L{li}_{sym}.npz',
                                net=net, ntr=ntr, tstart=np.datetime64(tstart) if tstart is not None else np.datetime64('NaT'),
                                ladder=np.array(lad), configs=np.array(CONFIGS, dtype=object))
            P(f'{sym} {strat} L{li} {lad}: candL={nL} candS={nS} best={net.sum(1).max():.0f} worstcfg={net.sum(1).min():.0f} pips, {time.time()-t1:.0f}s')
P('SWEEP DONE')
