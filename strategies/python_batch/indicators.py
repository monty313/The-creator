"""Pure indicator helpers for strategy family adapters (no trading law)."""
from __future__ import annotations

import numpy as np
import pandas as pd


def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n, min_periods=n).mean()


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    d = close.diff()
    up = d.clip(lower=0.0)
    dn = (-d).clip(lower=0.0)
    ma_up = up.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()
    ma_dn = dn.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()
    rs = ma_up / ma_dn.replace(0.0, np.nan)
    return 100.0 - (100.0 / (1.0 + rs))


def atr(high: pd.Series, low: pd.Series, close: pd.Series, n: int = 14) -> pd.Series:
    prev = close.shift(1)
    tr = pd.concat(
        [(high - low), (high - prev).abs(), (low - prev).abs()],
        axis=1,
    ).max(axis=1)
    return tr.rolling(n, min_periods=n).mean()


def bollinger(
    s: pd.Series, n: int = 20, dev: float = 2.0, shift: int = 0
) -> tuple[pd.Series, pd.Series, pd.Series]:
    mid = sma(s, n)
    std = s.rolling(n, min_periods=n).std()
    upper = mid + dev * std
    lower = mid - dev * std
    if shift:
        mid = mid.shift(shift)
        upper = upper.shift(shift)
        lower = lower.shift(shift)
    return lower, mid, upper


def cci(high: pd.Series, low: pd.Series, close: pd.Series, n: int = 20) -> pd.Series:
    tp = (high + low + close) / 3.0
    ma = tp.rolling(n, min_periods=n).mean()
    # vectorized mean absolute deviation approx via rolling
    md = (tp - ma).abs().rolling(n, min_periods=n).mean()
    return (tp - ma) / (0.015 * md.replace(0.0, np.nan))


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    ef = ema(close, fast)
    es = ema(close, slow)
    line = ef - es
    sig = ema(line, signal)
    hist = line - sig
    return line, sig, hist


def donchian(high: pd.Series, low: pd.Series, n: int = 20):
    return low.rolling(n, min_periods=n).min(), high.rolling(n, min_periods=n).max()


def supertrend(
    high: pd.Series, low: pd.Series, close: pd.Series, n: int = 10, mult: float = 3.0
) -> pd.Series:
    """Direction series: +1 bull, -1 bear (simplified ATR channel)."""
    a = atr(high, low, close, n)
    hl2 = (high + low) / 2.0
    upper = hl2 + mult * a
    lower = hl2 - mult * a
    st = pd.Series(index=close.index, dtype=float)
    direction = pd.Series(1.0, index=close.index)
    for i in range(1, len(close)):
        if close.iloc[i] > upper.iloc[i - 1]:
            direction.iloc[i] = 1.0
        elif close.iloc[i] < lower.iloc[i - 1]:
            direction.iloc[i] = -1.0
        else:
            direction.iloc[i] = direction.iloc[i - 1]
        if direction.iloc[i] > 0:
            st.iloc[i] = max(lower.iloc[i], st.iloc[i - 1] if direction.iloc[i - 1] > 0 else lower.iloc[i])
        else:
            st.iloc[i] = min(upper.iloc[i], st.iloc[i - 1] if direction.iloc[i - 1] < 0 else upper.iloc[i])
    return direction


def shifted_sma(s: pd.Series, n: int, shift: int) -> pd.Series:
    return sma(s, n).shift(shift)


def cross_up(a: pd.Series, b: pd.Series) -> pd.Series:
    return (a > b) & (a.shift(1) <= b.shift(1))


def cross_dn(a: pd.Series, b: pd.Series) -> pd.Series:
    return (a < b) & (a.shift(1) >= b.shift(1))


def roc(close: pd.Series, n: int = 12) -> pd.Series:
    prev = close.shift(n)
    return (close - prev) / prev.replace(0.0, np.nan) * 100.0


def true_range(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    prev = close.shift(1)
    return pd.concat(
        [(high - low), (high - prev).abs(), (low - prev).abs()],
        axis=1,
    ).max(axis=1)


def adx_di(
    high: pd.Series, low: pd.Series, close: pd.Series, n: int = 14
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Return (+DI, -DI, ADX) Wilder-style approximation via EWM."""
    up = high.diff()
    dn = -low.diff()
    plus_dm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=high.index)
    minus_dm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=high.index)
    tr = true_range(high, low, close)
    alpha = 1.0 / n
    atr_w = tr.ewm(alpha=alpha, adjust=False, min_periods=n).mean()
    plus_di = 100.0 * plus_dm.ewm(alpha=alpha, adjust=False, min_periods=n).mean() / atr_w.replace(0.0, np.nan)
    minus_di = 100.0 * minus_dm.ewm(alpha=alpha, adjust=False, min_periods=n).mean() / atr_w.replace(0.0, np.nan)
    dx = (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0.0, np.nan) * 100.0
    adx = dx.ewm(alpha=alpha, adjust=False, min_periods=n).mean()
    return plus_di, minus_di, adx


def parabolic_sar(
    high: pd.Series, low: pd.Series, close: pd.Series, af_step: float = 0.02, af_max: float = 0.2
) -> tuple[pd.Series, pd.Series]:
    """Return (sar, direction) with direction +1 bull / -1 bear."""
    n = len(close)
    sar = np.zeros(n, dtype=float)
    direction = np.ones(n, dtype=float)
    if n == 0:
        return pd.Series(dtype=float), pd.Series(dtype=float)
    bull = True
    af = af_step
    ep = high.iloc[0]
    sar[0] = low.iloc[0]
    for i in range(1, n):
        prev_sar = sar[i - 1]
        if bull:
            sar[i] = prev_sar + af * (ep - prev_sar)
            sar[i] = min(sar[i], low.iloc[i - 1], low.iloc[i - 2] if i >= 2 else low.iloc[i - 1])
            if low.iloc[i] < sar[i]:
                bull = False
                sar[i] = ep
                ep = low.iloc[i]
                af = af_step
                direction[i] = -1.0
            else:
                direction[i] = 1.0
                if high.iloc[i] > ep:
                    ep = high.iloc[i]
                    af = min(af + af_step, af_max)
        else:
            sar[i] = prev_sar + af * (ep - prev_sar)
            sar[i] = max(sar[i], high.iloc[i - 1], high.iloc[i - 2] if i >= 2 else high.iloc[i - 1])
            if high.iloc[i] > sar[i]:
                bull = True
                sar[i] = ep
                ep = high.iloc[i]
                af = af_step
                direction[i] = 1.0
            else:
                direction[i] = -1.0
                if low.iloc[i] < ep:
                    ep = low.iloc[i]
                    af = min(af + af_step, af_max)
    return pd.Series(sar, index=close.index), pd.Series(direction, index=close.index)


def keltner(
    high: pd.Series, low: pd.Series, close: pd.Series, n: int = 20, mult: float = 1.5
) -> tuple[pd.Series, pd.Series, pd.Series]:
    mid = ema(close, n)
    a = atr(high, low, close, n)
    return mid - mult * a, mid, mid + mult * a


def zscore(close: pd.Series, n: int = 20) -> pd.Series:
    m = close.rolling(n, min_periods=n).mean()
    s = close.rolling(n, min_periods=n).std()
    return (close - m) / s.replace(0.0, np.nan)


def stochastic(
    high: pd.Series, low: pd.Series, close: pd.Series, k: int = 14, d: int = 3
) -> tuple[pd.Series, pd.Series]:
    ll = low.rolling(k, min_periods=k).min()
    hh = high.rolling(k, min_periods=k).max()
    stoch_k = 100.0 * (close - ll) / (hh - ll).replace(0.0, np.nan)
    stoch_d = stoch_k.rolling(d, min_periods=d).mean()
    return stoch_k, stoch_d


def williams_r(high: pd.Series, low: pd.Series, close: pd.Series, n: int = 14) -> pd.Series:
    hh = high.rolling(n, min_periods=n).max()
    ll = low.rolling(n, min_periods=n).min()
    return -100.0 * (hh - close) / (hh - ll).replace(0.0, np.nan)


def vwap_proxy(high: pd.Series, low: pd.Series, close: pd.Series, n: int = 48) -> pd.Series:
    """Rolling typical-price VWAP proxy (equal weight volume when volume unavailable)."""
    tp = (high + low + close) / 3.0
    return tp.rolling(n, min_periods=n).mean()
