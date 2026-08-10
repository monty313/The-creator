"""Shared multi-timeframe bar builder for official MARK sets (2 HTF + 1 LTF)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd

from . import indicators as ind

# Official MARK sets: LTF, HTF1, HTF2 (order: LTF first for clarity)
OFFICIAL_SETS: Dict[str, Tuple[str, str, str]] = {
    "set1_1m_15m_30m": ("1m", "15m", "30m"),
    "set2_5m_30m_1h": ("5m", "30m", "1h"),
    "set3_15m_1h_4h": ("15m", "1h", "4h"),
    "set4_30m_4h_1d": ("30m", "4h", "1d"),
}

TF_RULES = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "30m": "30min",
    "1h": "1h",
    "4h": "4h",
    "1d": "1D",
}


@dataclass
class SetBars:
    name: str
    ltf: str
    htf1: str
    htf2: str
    # All series indexed on LTF timestamps (HTF ffilled)
    open: pd.Series
    high: pd.Series
    low: pd.Series
    close: pd.Series
    h1_open: pd.Series
    h1_high: pd.Series
    h1_low: pd.Series
    h1_close: pd.Series
    h2_open: pd.Series
    h2_high: pd.Series
    h2_low: pd.Series
    h2_close: pd.Series


def load_mt5_csv(path: str | Path, tail_bars: int | None = 90_000) -> pd.DataFrame:
    """Load MT5-export M1 CSV (<DATE> <TIME> OHLC...)."""
    path = Path(path)
    # Prefer explicit MetaTrader headers; fall back to first 6 columns.
    try:
        df = pd.read_csv(
            path,
            sep="\t",
            usecols=["<DATE>", "<TIME>", "<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>"],
        )
        df = df.rename(
            columns={
                "<DATE>": "date",
                "<TIME>": "time",
                "<OPEN>": "open",
                "<HIGH>": "high",
                "<LOW>": "low",
                "<CLOSE>": "close",
            }
        )
    except ValueError:
        df = pd.read_csv(path, sep="\t", header=0)
        df.columns = [str(c).strip().strip("<>").lower() for c in df.columns]
        need = ["date", "time", "open", "high", "low", "close"]
        missing = [c for c in need if c not in df.columns]
        if missing:
            raise ValueError(f"Unrecognized columns in {path}: {list(df.columns)}") from None
        df = df[need]

    # Tail early for speed on multi-million-row exports
    if tail_bars and len(df) > tail_bars:
        df = df.iloc[-tail_bars:].copy()

    ts = pd.to_datetime(
        df["date"].astype(str).str.strip() + " " + df["time"].astype(str).str.strip(),
        format="%Y.%m.%d %H:%M:%S",
        errors="coerce",
    )
    out = pd.DataFrame(
        {
            "open": pd.to_numeric(df["open"], errors="coerce").to_numpy(),
            "high": pd.to_numeric(df["high"], errors="coerce").to_numpy(),
            "low": pd.to_numeric(df["low"], errors="coerce").to_numpy(),
            "close": pd.to_numeric(df["close"], errors="coerce").to_numpy(),
        },
        index=pd.DatetimeIndex(ts),
    )
    out = out[out.index.notna()].dropna().sort_index()
    out = out[~out.index.duplicated(keep="last")]
    if out.empty:
        raise ValueError(f"No OHLCV rows loaded from {path}")
    return out


def resample_ohlc(m1: pd.DataFrame, tf: str) -> pd.DataFrame:
    rule = TF_RULES[tf]
    o = m1["open"].resample(rule).first()
    h = m1["high"].resample(rule).max()
    l = m1["low"].resample(rule).min()
    c = m1["close"].resample(rule).last()
    df = pd.DataFrame({"open": o, "high": h, "low": l, "close": c}).dropna()
    return df


def align_htf_to_ltf(ltf_index: pd.DatetimeIndex, htf: pd.DataFrame) -> pd.DataFrame:
    """Forward-fill completed HTF bars onto LTF index (no lookahead beyond ffill of closed bars).

    Uses shift(1) on HTF so LTF only sees last *completed* HTF bar.
    """
    h = htf.shift(1)
    return h.reindex(ltf_index, method="ffill")


def build_set(m1: pd.DataFrame, set_name: str) -> SetBars:
    ltf_n, h1_n, h2_n = OFFICIAL_SETS[set_name]
    ltf = resample_ohlc(m1, ltf_n) if ltf_n != "1m" else m1.copy()
    h1 = resample_ohlc(m1, h1_n)
    h2 = resample_ohlc(m1, h2_n)
    h1a = align_htf_to_ltf(ltf.index, h1)
    h2a = align_htf_to_ltf(ltf.index, h2)
    # drop warmup NaNs
    mask = h1a["close"].notna() & h2a["close"].notna() & ltf["close"].notna()
    ltf = ltf.loc[mask]
    h1a = h1a.loc[mask]
    h2a = h2a.loc[mask]
    return SetBars(
        name=set_name,
        ltf=ltf_n,
        htf1=h1_n,
        htf2=h2_n,
        open=ltf["open"],
        high=ltf["high"],
        low=ltf["low"],
        close=ltf["close"],
        h1_open=h1a["open"],
        h1_high=h1a["high"],
        h1_low=h1a["low"],
        h1_close=h1a["close"],
        h2_open=h2a["open"],
        h2_high=h2a["high"],
        h2_low=h2a["low"],
        h2_close=h2a["close"],
    )


def build_all_sets(m1: pd.DataFrame) -> Dict[str, SetBars]:
    return {name: build_set(m1, name) for name in OFFICIAL_SETS}


def htf_force_bb_mass(sb: SetBars, n: int = 100, dev: float = 0.5, shift: int = 2):
    """Mark-style HTF mass: both HTFs close vs BB mid on price."""
    _, m1, _ = ind.bollinger(sb.h1_close, n=n, dev=dev, shift=shift)
    _, m2, _ = ind.bollinger(sb.h2_close, n=n, dev=dev, shift=shift)
    bull = (sb.h1_close > m1) & (sb.h2_close > m2)
    bear = (sb.h1_close < m1) & (sb.h2_close < m2)
    return bull.fillna(False), bear.fillna(False)


def htf_force_sma(sb: SetBars, n: int = 50):
    m1 = ind.sma(sb.h1_close, n)
    m2 = ind.sma(sb.h2_close, n)
    bull = (sb.h1_close > m1) & (sb.h2_close > m2)
    bear = (sb.h1_close < m1) & (sb.h2_close < m2)
    return bull.fillna(False), bear.fillna(False)


def htf_force_cci(sb: SetBars, n: int = 20):
    c1 = ind.cci(sb.h1_high, sb.h1_low, sb.h1_close, n)
    c2 = ind.cci(sb.h2_high, sb.h2_low, sb.h2_close, n)
    bull = (c1 > 0) & (c2 > 0)
    bear = (c1 < 0) & (c2 < 0)
    return bull.fillna(False), bear.fillna(False)


def ltf_mark_rsi_bb_modes(sb: SetBars):
    """RSI(5) + BB(10,0.5,shift+2) on RSI series → pullback load & continuation fire.

    Note: doctrine sometimes says shift+5; project CASE-0015 uses shift+2. We use +2.
    Pullback = loaded extreme (RSI outside far band with tide).
    Continuation = cross of release band with tide.
    """
    r = ind.rsi(sb.close, 5)
    lo, mid, hi = ind.bollinger(r, n=10, dev=0.5, shift=2)
    # pullback load (extreme)
    pb_long = (r < lo).fillna(False)
    pb_short = (r > hi).fillna(False)
    # continuation release
    cont_long = ind.cross_up(r, hi).fillna(False)
    cont_short = ind.cross_dn(r, lo).fillna(False)
    return pb_long, pb_short, cont_long, cont_short


def apply_htf_gate(
    bull: pd.Series,
    bear: pd.Series,
    pb_long: pd.Series,
    pb_short: pd.Series,
    cont_long: pd.Series,
    cont_short: pd.Series,
    mode: str,
) -> tuple[pd.Series, pd.Series]:
    """mode in {pullback, continuation} → long_entry, short_entry under HTF force."""
    if mode == "pullback":
        long_e = bull & pb_long
        short_e = bear & pb_short
    else:
        long_e = bull & cont_long
        short_e = bear & cont_short
    return long_e.fillna(False), short_e.fillna(False)


def default_exits(close: pd.Series, long_e: pd.Series, short_e: pd.Series, hold: int = 12):
    """Time-based exit + opposite signal exit (keeps vectorbt simple)."""
    long_x = long_e.shift(hold).fillna(False) | short_e
    short_x = short_e.shift(hold).fillna(False) | long_e
    return long_x.astype(bool), short_x.astype(bool)
