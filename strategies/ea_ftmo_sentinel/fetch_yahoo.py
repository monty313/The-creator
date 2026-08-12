"""Fetch 60 days of M5 bars from Yahoo Finance chart API (secondary data source).

Yahoo FX quotes are indicative mid prices — good enough for a preliminary
cross-check while the authoritative Dukascopy M1 download completes.

Usage: python3 fetch_yahoo.py EURUSD  -> data/EURUSD_Y_M1.parquet (M5 bars)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def fetch(sym: str) -> pd.DataFrame:
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}=X"
           f"?interval=5m&range=60d")
    out = subprocess.run(["curl", "-s", "--max-time", "60", "-A", UA, url],
                         capture_output=True, text=True)
    data = json.loads(out.stdout)
    res = data["chart"]["result"][0]
    ts = res["timestamp"]
    q = res["indicators"]["quote"][0]
    df = pd.DataFrame({
        "time": pd.to_datetime(ts, unit="s"),      # epoch UTC
        "open": q["open"], "high": q["high"], "low": q["low"],
        "close": q["close"], "volume": [v or 0 for v in q["volume"]],
    }).dropna(subset=["open", "high", "low", "close"])
    df = df.drop_duplicates("time").sort_values("time").set_index("time")
    return df


if __name__ == "__main__":
    sym = sys.argv[1]
    df = fetch(sym)
    out = Path(__file__).parent / "data" / f"{sym}_Y_M1.parquet"
    out.parent.mkdir(exist_ok=True)
    df.to_parquet(out)
    print(sym, len(df), "M5 bars", df.index[0], "->", df.index[-1])
