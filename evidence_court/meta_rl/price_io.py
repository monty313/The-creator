"""Price I/O: M1 MT5 CSV load with optional date window (multi-symbol)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

_WINDOWS_RAW = Path(r"C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\the-truth\data\raw")
_REPO_RAW = Path(__file__).resolve().parents[2] / "data" / "raw"


def _resolve_raw_dir() -> Path:
    """Data dir resolution: env var > local Windows path > repo-relative data/raw."""
    env = os.environ.get("CREATOR_DATA_DIR", "").strip()
    if env:
        return Path(env)
    if _WINDOWS_RAW.exists():
        return _WINDOWS_RAW
    return _REPO_RAW


_RAW = _resolve_raw_dir()

SYMBOL_FILES: Dict[str, Path] = {
    "XAUUSD": _RAW / "XAUUSD_M1_full.csv",
    "EURUSD": _RAW / "EURUSD_M1_curriculum.csv",
    "GBPUSD": _RAW / "GBPUSD_M1_curriculum.csv",
    "US30": _RAW / "US30_M1_curriculum.csv",
}

# Fallback if full missing
if not SYMBOL_FILES["XAUUSD"].exists():
    _alt = _RAW / "XAUUSD_curriculum_2026.csv"
    if _alt.exists():
        SYMBOL_FILES["XAUUSD"] = _alt

_M1_CACHE: Dict[str, Tuple[float, List[dict]]] = {}


def load_m1_bars(
    path: Path,
    *,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[dict]:
    """Load M1 bars; optional inclusive date filter YYYY-MM-DD."""
    path = Path(path)
    key = f"{path.resolve()}|{start_date}|{end_date}"
    mtime = path.stat().st_mtime if path.exists() else 0.0
    # cache full file only when no filter
    cache_key = str(path.resolve()) if start_date is None and end_date is None else key
    if start_date is None and end_date is None:
        cached = _M1_CACHE.get(cache_key)
        if cached and cached[0] == mtime:
            return cached[1]

    if not path.exists():
        return []

    rows: List[dict] = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        header = f.readline()
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 6:
                continue
            try:
                date_s = parts[0].replace(".", "-")
                time_s = parts[1]
                o, h, l, c = float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])
            except (ValueError, IndexError):
                continue
            if start_date and date_s < start_date:
                continue
            if end_date and date_s > end_date:
                continue
            rows.append(
                {
                    "date": date_s,
                    "time": time_s,
                    "open": o,
                    "high": h,
                    "low": l,
                    "close": c,
                }
            )

    if start_date is None and end_date is None:
        _M1_CACHE[cache_key] = (mtime, rows)
    return rows


def bars_to_daily(m1: Sequence[dict]) -> List[dict]:
    by_day: Dict[str, List[dict]] = {}
    for r in m1:
        by_day.setdefault(r["date"], []).append(r)
    days: List[dict] = []
    for d in sorted(by_day.keys()):
        bars = by_day[d]
        days.append(
            {
                "date": d,
                "open": bars[0]["open"],
                "high": max(b["high"] for b in bars),
                "low": min(b["low"] for b in bars),
                "close": bars[-1]["close"],
                "n_bars": len(bars),
            }
        )
    return days


def m1_through_date(m1: Sequence[dict], date: str, *, max_bars: int = 20000) -> List[dict]:
    """Completed history through end of ``date`` (inclusive), capped for speed."""
    out = [b for b in m1 if b["date"] <= date]
    if len(out) > max_bars:
        return list(out[-max_bars:])
    return out


def available_symbols() -> List[str]:
    return [s for s, p in SYMBOL_FILES.items() if p.exists()]


def load_m1_trailing_calendar_days(path: Path, n_days: int = 200) -> List[dict]:
    """Single-pass load keeping only the last ``n_days`` calendar dates of M1 bars.

    Avoids holding entire multi-year CSVs in memory for multi-symbol runs.
    """
    path = Path(path)
    if not path.exists() or n_days <= 0:
        return []

    # date -> list of bars (only retain recent dates)
    from collections import OrderedDict

    by_date: "OrderedDict[str, List[dict]]" = OrderedDict()
    with path.open("r", encoding="utf-8", errors="replace") as f:
        _ = f.readline()
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 6:
                continue
            try:
                date_s = parts[0].replace(".", "-")
                time_s = parts[1]
                o, h, l, c = float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])
            except (ValueError, IndexError):
                continue
            if date_s not in by_date:
                by_date[date_s] = []
                # drop oldest calendar days beyond window
                while len(by_date) > n_days:
                    by_date.popitem(last=False)
            by_date[date_s].append(
                {
                    "date": date_s,
                    "time": time_s,
                    "open": o,
                    "high": h,
                    "low": l,
                    "close": c,
                }
            )
    rows: List[dict] = []
    for d in by_date:
        rows.extend(by_date[d])
    return rows
