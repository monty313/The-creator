"""Download Dukascopy 1-minute BID candles → MT5-style tab CSV for price_io.

Writes the exact format ``evidence_court.meta_rl.price_io.load_m1_bars`` parses:
header line, then ``DATE<TAB>TIME<TAB>OPEN<TAB>HIGH<TAB>LOW<TAB>CLOSE<TAB>VOL``
with DATE as ``YYYY.MM.DD`` (loader converts dots to dashes).

Usage:
  python tools/download_dukascopy_m1.py --symbol XAUUSD \
      --start 2025-12-01 --end 2026-08-08 --out data/raw/XAUUSD_M1_full.csv

Dukascopy candle bi5 record (24 bytes, big-endian):
  int32 seconds-from-day-start · int32 open · int32 close · int32 low ·
  int32 high (all price * point multiplier) · float32 volume
Month in the URL is 0-indexed. Files are UTC days; weekend files are empty.
"""
from __future__ import annotations

import argparse
import datetime as dt
import lzma
import struct
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# price = stored int / POINT
POINT = {
    "XAUUSD": 1_000.0,
    "XAGUSD": 1_000.0,
    "EURUSD": 100_000.0,
    "GBPUSD": 100_000.0,
    "USDJPY": 1_000.0,
}

URL_TPL = (
    "https://datafeed.dukascopy.com/datafeed/{sym}/{y:04d}/{m0:02d}/{d:02d}/"
    "BID_candles_min_1.bi5"
)

_REC = struct.Struct(">5if")


def fetch_day(sym: str, day: dt.date, *, retries: int = 8) -> bytes:
    url = URL_TPL.format(sym=sym, y=day.year, m0=day.month - 1, d=day.day)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return b""
            if e.code == 429:
                time.sleep(min(4.0 * (attempt + 1), 30.0))
                continue
            if attempt == retries - 1:
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == retries - 1:
                raise
        time.sleep(2.0 * (attempt + 1))
    return b""


def decode_day(raw: bytes, sym: str, day: dt.date) -> list[str]:
    if not raw:
        return []
    try:
        blob = lzma.decompress(raw)
    except lzma.LZMAError:
        return []
    point = POINT.get(sym, 100_000.0)
    date_s = day.strftime("%Y.%m.%d")
    rows: list[str] = []
    for off in range(0, len(blob) - _REC.size + 1, _REC.size):
        t, o, c, lo, hi, vol = _REC.unpack_from(blob, off)
        if vol <= 0.0 or o <= 0:
            continue
        hh, rem = divmod(t, 3600)
        mm, ss = divmod(rem, 60)
        rows.append(
            f"{date_s}\t{hh:02d}:{mm:02d}:{ss:02d}\t"
            f"{o / point:.5f}\t{hi / point:.5f}\t{lo / point:.5f}\t{c / point:.5f}\t"
            f"{vol:.2f}"
        )
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--symbol", default="XAUUSD")
    ap.add_argument("--start", required=True, help="YYYY-MM-DD (UTC)")
    ap.add_argument("--end", required=True, help="YYYY-MM-DD inclusive (UTC)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args(argv)

    sym = args.symbol.upper()
    start = dt.date.fromisoformat(args.start)
    end = dt.date.fromisoformat(args.end)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    days: list[dt.date] = []
    day = start
    while day <= end:
        days.append(day)
        day += dt.timedelta(days=1)

    from concurrent.futures import ThreadPoolExecutor

    def one(d: dt.date) -> list[str]:
        return decode_day(fetch_day(sym, d), sym, d)

    n_days = 0
    n_bars = 0
    with out.open("w", encoding="utf-8") as f:
        f.write("<DATE>\t<TIME>\t<OPEN>\t<HIGH>\t<LOW>\t<CLOSE>\t<TICKVOL>\n")
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            for i, rows in enumerate(ex.map(one, days)):
                if rows:
                    f.write("\n".join(rows) + "\n")
                    n_days += 1
                    n_bars += len(rows)
                if (i + 1) % 50 == 0:
                    print(
                        f"  ...{days[i]} scanned={i + 1}/{len(days)} "
                        f"days_with_data={n_days} bars={n_bars}",
                        flush=True,
                    )

    print(f"DONE {sym}: days_with_data={n_days} bars={n_bars} -> {out}")
    return 0 if n_bars > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
