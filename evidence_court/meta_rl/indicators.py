"""Multi-timeframe indicators — RSI / Bollinger with completed-bar only semantics.

Hint edge (Possible edge not tested.txt):
  RSI period 5 with applied BB period 10, deviation 0.5, shift +2
  on the **LTF (first TF) of each official Mark set** for pullback / continuation timing.
  HTF (last two) provide force / permission — not entry timing.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

# Official Mark TF minutes
TF_MINUTES: Dict[str, int] = {
    "1m": 1,
    "5m": 5,
    "15m": 15,
    "30m": 30,
    "1h": 60,
    "4h": 240,
    "1d": 1440,
}


def rsi(closes: np.ndarray, period: int = 5) -> np.ndarray:
    """Wilder-style RSI; length matches input; early values NaN."""
    c = np.asarray(closes, dtype=np.float64).reshape(-1)
    n = c.size
    out = np.full(n, np.nan, dtype=np.float64)
    if n < period + 1:
        return out
    delta = np.diff(c, prepend=c[0])
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)
    # seed SMA
    avg_gain = np.mean(gain[1 : period + 1])
    avg_loss = np.mean(loss[1 : period + 1])
    if avg_loss == 0:
        out[period] = 100.0
    else:
        rs = avg_gain / avg_loss
        out[period] = 100.0 - (100.0 / (1.0 + rs))
    for i in range(period + 1, n):
        avg_gain = (avg_gain * (period - 1) + gain[i]) / period
        avg_loss = (avg_loss * (period - 1) + loss[i]) / period
        if avg_loss == 0:
            out[i] = 100.0
        else:
            rs = avg_gain / max(avg_loss, 1e-12)
            out[i] = 100.0 - (100.0 / (1.0 + rs))
    return out


def bollinger(
    closes: np.ndarray,
    period: int = 10,
    dev: float = 0.5,
    shift: int = 2,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """BB mid/upper/lower. ``shift`` delays series so decision at t uses BB[t-shift].

    No look-ahead: shifted values are past completed computations only.
    """
    c = np.asarray(closes, dtype=np.float64).reshape(-1)
    n = c.size
    mid = np.full(n, np.nan)
    upper = np.full(n, np.nan)
    lower = np.full(n, np.nan)
    if n < period:
        return mid, upper, lower
    for i in range(period - 1, n):
        window = c[i - period + 1 : i + 1]
        m = float(np.mean(window))
        s = float(np.std(window, ddof=0))
        mid[i] = m
        upper[i] = m + dev * s
        lower[i] = m - dev * s
    if shift > 0:
        mid = _shift_forward_nan(mid, shift)
        upper = _shift_forward_nan(upper, shift)
        lower = _shift_forward_nan(lower, shift)
    return mid, upper, lower


def _shift_forward_nan(x: np.ndarray, shift: int) -> np.ndarray:
    """Value at index i becomes previous value from i-shift (pad head with nan)."""
    out = np.full_like(x, np.nan)
    if shift <= 0:
        return x.copy()
    out[shift:] = x[:-shift]
    return out


def sma(closes: np.ndarray, period: int) -> np.ndarray:
    c = np.asarray(closes, dtype=np.float64).reshape(-1)
    n = c.size
    out = np.full(n, np.nan)
    if n < period:
        return out
    cum = np.cumsum(c)
    out[period - 1] = cum[period - 1] / period
    for i in range(period, n):
        out[i] = (cum[i] - cum[i - period]) / period
    return out


def trend_dir(closes: np.ndarray, lookback: int = 5) -> float:
    """Signed force proxy in [-1,1] from completed closes slope.

    Exact formula (current Court HTF force primitive):
      a = close[-(lookback+1)]   # close lookback bars before last
      b = close[-1]              # latest completed close
      ret = (b - a) / abs(a)
      score = clip(ret * 50.0, -1.0, +1.0)

    Not an MA structure model — pure recent close-to-close return scaled.
    """
    c = np.asarray(closes, dtype=np.float64).reshape(-1)
    if c.size < lookback + 1:
        return 0.0
    a, b = float(c[-lookback - 1]), float(c[-1])
    if a == 0:
        return 0.0
    ret = (b - a) / abs(a)
    return float(np.clip(ret * 50.0, -1.0, 1.0))


def trend_dir_series(closes: np.ndarray, lookback: int = 5) -> np.ndarray:
    """Per-bar trend_dir at each index (uses completed window ending at i)."""
    c = np.asarray(closes, dtype=np.float64).reshape(-1)
    n = c.size
    out = np.zeros(n, dtype=np.float64)
    for i in range(lookback, n):
        a, b = float(c[i - lookback]), float(c[i])
        if a == 0:
            out[i] = 0.0
        else:
            out[i] = float(np.clip(((b - a) / abs(a)) * 50.0, -1.0, 1.0))
    return out


def cci(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    period: int = 20,
) -> np.ndarray:
    """Commodity Channel Index (Lambert): (TP - SMA(TP)) / (0.015 * MAD)."""
    h = np.asarray(high, dtype=np.float64).reshape(-1)
    l = np.asarray(low, dtype=np.float64).reshape(-1)
    c = np.asarray(close, dtype=np.float64).reshape(-1)
    n = c.size
    out = np.full(n, np.nan, dtype=np.float64)
    if n < period or h.size != n or l.size != n:
        return out
    tp = (h + l + c) / 3.0
    for i in range(period - 1, n):
        window = tp[i - period + 1 : i + 1]
        m = float(np.mean(window))
        mad = float(np.mean(np.abs(window - m)))
        if mad < 1e-12:
            out[i] = 0.0
        else:
            out[i] = (float(tp[i]) - m) / (0.015 * mad)
    return out


def series_above_bb_mid(
    series: np.ndarray,
    bb_period: int = 10,
    bb_dev: float = 0.5,
    shift: int = 0,
) -> np.ndarray:
    """True where series[i] > Bollinger mid (SMA of series). NaN → False."""
    mid, _up, _lo = bollinger(series, period=bb_period, dev=bb_dev, shift=shift)
    s = np.asarray(series, dtype=np.float64).reshape(-1)
    out = np.zeros(s.size, dtype=bool)
    for i in range(s.size):
        if np.isnan(s[i]) or np.isnan(mid[i]):
            out[i] = False
        else:
            out[i] = bool(s[i] > float(mid[i]))
    return out


def series_below_bb_mid(
    series: np.ndarray,
    bb_period: int = 10,
    bb_dev: float = 0.5,
    shift: int = 0,
) -> np.ndarray:
    """True where series[i] < Bollinger mid (SMA of series). NaN → False."""
    mid, _up, _lo = bollinger(series, period=bb_period, dev=bb_dev, shift=shift)
    s = np.asarray(series, dtype=np.float64).reshape(-1)
    out = np.zeros(s.size, dtype=bool)
    for i in range(s.size):
        if np.isnan(s[i]) or np.isnan(mid[i]):
            out[i] = False
        else:
            out[i] = bool(s[i] < float(mid[i]))
    return out


def resample_m1_to_tf(
    bars: Sequence[DictLike],
    tf: str,
) -> List[dict]:
    """Resample M1 OHLC dicts to higher TF. bars: date,time,open,high,low,close."""
    minutes = TF_MINUTES.get(tf)
    if minutes is None:
        raise ValueError(f"unknown tf {tf}")
    if minutes == 1:
        return [dict(b) for b in bars]

    buckets: Dict[str, dict] = {}
    order: List[str] = []
    for b in bars:
        key = _bucket_key(str(b["date"]), str(b.get("time", "00:00:00")), minutes)
        if key not in buckets:
            buckets[key] = {
                "date": b["date"],
                "time": b.get("time", "00:00:00"),
                "open": float(b["open"]),
                "high": float(b["high"]),
                "low": float(b["low"]),
                "close": float(b["close"]),
                "_key": key,
            }
            order.append(key)
        else:
            o = buckets[key]
            o["high"] = max(o["high"], float(b["high"]))
            o["low"] = min(o["low"], float(b["low"]))
            o["close"] = float(b["close"])
    return [{k: v for k, v in buckets[key].items() if k != "_key"} for key in order]


def _bucket_key(date: str, time: str, minutes: int) -> str:
    """Floor timestamp to TF bucket."""
    # date YYYY-MM-DD or YYYY.MM.DD; time HH:MM:SS
    d = date.replace(".", "-")
    parts = time.split(":")
    h = int(parts[0]) if parts else 0
    m = int(parts[1]) if len(parts) > 1 else 0
    total = h * 60 + m
    if minutes >= 1440:
        return d  # daily
    floored = (total // minutes) * minutes
    hh, mm = divmod(floored, 60)
    return f"{d}T{hh:02d}:{mm:02d}"


# typing without importing heavy
DictLike = dict
