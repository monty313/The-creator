"""Download Dukascopy M1 BID candles into a local parquet cache.

Dukascopy URL layout (month is 0-indexed):
  https://datafeed.dukascopy.com/datafeed/{SYM}/{YYYY}/{MM0}/{DD}/BID_candles_min_1.bi5
Each .bi5 is LZMA-compressed 24-byte rows:
  int32 sec_of_day, int32 open, int32 close, int32 low, int32 high, float32 volume
Prices are ints scaled by the instrument point (1e5 FX majors, 1e3 XAU/JPY-quoted).

The endpoint rate-limits hard, so this uses curl with pacing + retries and caches
every day file under data/raw/ so reruns resume for free.

Usage: python3 fetch_dukascopy.py EURUSD 2026-01-05 2026-08-07
"""

from __future__ import annotations

import datetime as dt
import lzma
import struct
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

SCALE = {"EURUSD": 1e5, "GBPUSD": 1e5, "USDJPY": 1e3, "XAUUSD": 1e3, "USDCHF": 1e5,
         "AUDUSD": 1e5, "USDCAD": 1e5}
BASE = "https://datafeed.dukascopy.com/datafeed/{sym}/{y}/{m:02d}/{d:02d}/BID_candles_min_1.bi5"
ROW = struct.Struct(">iiiiif")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"


def fetch_day_raw(sym: str, day: dt.date, cache_dir: Path) -> bytes | None:
    cache = cache_dir / f"{sym}_{day.isoformat()}.bi5"
    if cache.exists():
        return cache.read_bytes() or None
    url = BASE.format(sym=sym, y=day.year, m=day.month - 1, d=day.day)
    for attempt in range(7):
        proc = subprocess.run(
            ["curl", "-s", "--http1.1", "-A", UA, "--max-time", "40",
             "-w", "%{http_code}", "-o", str(cache) + ".tmp", url],
            capture_output=True, text=True)
        code = proc.stdout.strip()
        tmp = Path(str(cache) + ".tmp")
        if code == "200" and tmp.exists() and tmp.stat().st_size > 0:
            body = tmp.read_bytes()
            if not body.lstrip().startswith(b"<html"):
                tmp.rename(cache)
                time.sleep(5.0)      # steady pacing beats burst-and-backoff here
                return body
        if code == "404":
            tmp.unlink(missing_ok=True)
            cache.write_bytes(b"")          # negative-cache holidays
            time.sleep(1.2)
            return None
        tmp.unlink(missing_ok=True)
        time.sleep(2.5 * (attempt + 1))     # 503/000/429 -> back off
    print(f"  [warn] gave up on {sym} {day}")
    return None


def decode(sym: str, day: dt.date, body: bytes) -> pd.DataFrame | None:
    try:
        raw = lzma.decompress(body)
    except lzma.LZMAError:
        return None
    scale = SCALE[sym]
    n = len(raw) // ROW.size
    base_ts = dt.datetime(day.year, day.month, day.day, tzinfo=dt.timezone.utc)
    recs = []
    for i in range(n):
        t, o, c, lo, hi, v = ROW.unpack_from(raw, i * ROW.size)
        recs.append((base_ts + dt.timedelta(seconds=t), o / scale, hi / scale,
                     lo / scale, c / scale, v))
    return pd.DataFrame(recs, columns=["time", "open", "high", "low", "close", "volume"])


def fetch_range(sym: str, start: dt.date, end: dt.date, out: Path) -> pd.DataFrame:
    cache_dir = out.parent / "raw"
    cache_dir.mkdir(parents=True, exist_ok=True)
    frames = []
    day = start
    done = 0
    while day <= end:
        if day.weekday() != 5:              # Saturday has no session
            body = fetch_day_raw(sym, day, cache_dir)
            if body:
                df = decode(sym, day, body)
                if df is not None and len(df):
                    frames.append(df)
            done += 1
            if done % 20 == 0:
                print(f"  {sym}: {done} days fetched, at {day}")
        day += dt.timedelta(days=1)
    full = pd.concat(frames, ignore_index=True)
    full = full.drop_duplicates("time").sort_values("time").set_index("time")
    full = full[~((full.volume == 0) & (full.high == full.low))]
    full.to_parquet(out)
    return full


if __name__ == "__main__":
    sym = sys.argv[1]
    start = dt.date.fromisoformat(sys.argv[2])
    end = dt.date.fromisoformat(sys.argv[3])
    out = Path(__file__).parent / "data" / f"{sym}_M1.parquet"
    out.parent.mkdir(exist_ok=True)
    df = fetch_range(sym, start, end, out)
    print(sym, len(df), "bars", df.index[0], "->", df.index[-1])
