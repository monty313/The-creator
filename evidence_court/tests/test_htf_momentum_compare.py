"""Unit pins for HTF slope formula + Monty CCI/RSI BB momentum helpers."""
from __future__ import annotations

import numpy as np

from evidence_court.meta_rl.htf_momentum_compare import (
    pair_slope_flags,
    single_tf_cci_bb_side,
    single_tf_rsi_bb_side,
)
from evidence_court.meta_rl.indicators import cci, trend_dir, trend_dir_series


def test_slope_formula_exact_numbers():
    """trend_dir: ret=(b-a)/|a|, score=clip(ret*50,-1,1)."""
    # 5-bar lookback: a=index -6 from end? lookback=5 → a = c[-(5+1)] = c[-6]
    closes = np.array([100.0, 100, 100, 100, 100, 100, 102.0], dtype=np.float64)
    # size 7: a=closes[1]=100? indices 0..6; lookback 5 → a=c[6-5]=c[1]=100, wait
    # implementation: a = c[-lookback-1], b = c[-1]
    # -6 and -1 → a=c[0] if len=7? len=7 indices 0..6; -6 → index 1
    # c[-6] with len 7 is index 1 = 100, b=102
    # Actually: range lookback+1 = 6, need at least 6 elements for lookback 5
    closes = np.array([100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 102.0])
    # a = closes[-6] = closes[1] = 100, b = 102, ret = 0.02, score = 1.0 (clipped)
    score = trend_dir(closes, lookback=5)
    assert abs(score - 1.0) < 1e-9

    # small move: +0.1% → ret=0.001 → *50 = 0.05
    closes2 = np.array([100.0] * 6 + [100.1])
    s2 = trend_dir(closes2, lookback=5)
    assert abs(s2 - 0.05) < 1e-9


def test_trend_dir_series_matches_last_point():
    rng = np.random.default_rng(0)
    c = 100 + np.cumsum(rng.normal(0, 0.2, size=80))
    series = trend_dir_series(c, lookback=5)
    assert abs(series[-1] - trend_dir(c, lookback=5)) < 1e-9


def test_pair_slope_agree_and_strong():
    f1 = np.array([0.3, 0.3, -0.3, 0.05])
    f2 = np.array([0.3, -0.3, -0.3, 0.3])
    force, bull, bear = pair_slope_flags(f1, f2)
    assert bull[0]  # agree up strong
    assert not bull[1]  # disagree
    assert bear[2]
    assert not bull[3] and not bear[3]  # weak


def test_cci_finite_and_rsi_bb_side_shapes():
    n = 200
    rng = np.random.default_rng(1)
    close = 100 + np.cumsum(rng.normal(0, 0.5, size=n))
    high = close + 0.3
    low = close - 0.3
    c = cci(high, low, close, period=20)
    assert np.isfinite(c[50:]).all()
    ab, be = single_tf_cci_bb_side(high, low, close)
    assert ab.shape == (n,)
    assert be.shape == (n,)
    # cannot be both above and below all three
    assert not np.any(ab & be)
    rab, rbe = single_tf_rsi_bb_side(close)
    assert rab.shape == (n,)
    assert not np.any(rab & rbe)
