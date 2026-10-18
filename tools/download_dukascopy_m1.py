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


_UA = {"User-Agent": "Mozilla/5.0 (research; m1-candles)"}


def fetch_day(sym: str, day: dt.date, *, retries: int = 12) -> bytes:
    url = URL_TPL.format(sym=sym, y=day.year, m0=day.month - 1, d=day.day)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=_UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return b""
            # 429 / 5xx: back off patiently
            time.sleep(min(5.0 * (attempt + 1), 45.0))
            if attempt == retries - 1:
                raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            # connection reset / drop: server is throttling — wait it out
            time.sleep(min(5.0 * (attempt + 1), 45.0))
            if attempt == retries - 1:
                raise
    return b""


def decode_day(raw: bytes, sym: str, day: dt.date, tz: str = "eet") -> list[str]:
    """Decode one day file. ``tz='eet'`` converts UTC → MT5 broker time
    (Europe/Athens): Sunday 22:00 UTC becomes Monday 00:00/01:00 EET, matching
    the repo's original MT5 CSV convention (no thin Sunday 'days')."""
    if not raw:
        return []
    try:
        blob = lzma.decompress(raw)
    except lzma.LZMAError:
        return []
    zone = None
    if tz == "eet":
        from zoneinfo import ZoneInfo

        zone = ZoneInfo("Europe/Athens")
    point = POINT.get(sym, 100_000.0)
    base = dt.datetime(day.year, day.month, day.day, tzinfo=dt.timezone.utc)
    rows: list[str] = []
    for off in range(0, len(blob) - _REC.size + 1, _REC.size):
        t, o, c, lo, hi, vol = _REC.unpack_from(blob, off)
        if vol <= 0.0 or o <= 0:
            continue
        stamp = base + dt.timedelta(seconds=int(t))
        if zone is not None:
            stamp = stamp.astimezone(zone)
        rows.append(
            f"{stamp:%Y.%m.%d}\t{stamp:%H:%M:%S}\t"
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
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--delay", type=float, default=0.25, help="post-request sleep per worker (s)")
    ap.add_argument("--tz", choices=("utc", "eet"), default="eet", help="output timestamps (eet = MT5 broker time)")
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
        rows = decode_day(fetch_day(sym, d), sym, d, tz=args.tz)
        if args.delay > 0:
            time.sleep(args.delay)
        return rows

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
