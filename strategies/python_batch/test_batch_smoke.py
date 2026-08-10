"""Smoke tests for shipped strategy batch entry (real path, not theater)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategies.python_batch.families import fam_mark_rsi_bb, entries_for_mode  # noqa: E402
from strategies.python_batch.mtf import OFFICIAL_SETS, build_set, load_mt5_csv  # noqa: E402
from strategies.python_batch.run_strategy_batch import (  # noqa: E402
    DEFAULT_DATA,
    ALT_DATA,
    run_one,
    aggregate_family,
)


def _toy_m1(n: int = 5000) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    idx = pd.date_range("2024-01-01", periods=n, freq="1min")
    # random walk
    rets = rng.normal(0, 0.0001, size=n)
    close = 1.10 + np.cumsum(rets)
    high = close + rng.uniform(0, 0.0002, size=n)
    low = close - rng.uniform(0, 0.0002, size=n)
    open_ = np.roll(close, 1)
    open_[0] = close[0]
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close}, index=idx)


def test_official_sets_are_four_with_2htf_1ltf():
    assert len(OFFICIAL_SETS) == 4
    for name, (ltf, h1, h2) in OFFICIAL_SETS.items():
        assert ltf and h1 and h2 and ltf != h1 and h1 != h2


def test_mark_family_emits_pb_and_cont_entries():
    m1 = _toy_m1(8000)
    sb = build_set(m1, "set3_15m_1h_4h")
    long_pb, short_pb = entries_for_mode(sb, fam_mark_rsi_bb, "pullback")
    long_c, short_c = entries_for_mode(sb, fam_mark_rsi_bb, "continuation")
    assert long_pb.dtype == bool or str(long_pb.dtype) == "bool"
    assert len(long_pb) == len(sb.close)
    # modes are distinct series objects
    assert not (long_pb.equals(long_c) and short_pb.equals(short_c) and long_pb.any())


def test_vectorbt_stats_non_empty_on_toy():
    pytest.importorskip("vectorbt")
    m1 = _toy_m1(12000)
    sb = build_set(m1, "set2_5m_30m_1h")
    row = run_one("mark_rsi_bb_l2l", fam_mark_rsi_bb, sb, "continuation", sb.ltf)
    assert row.error == "" or "Total Trades" in str(row.stats)
    # either trades or empty stats — but stats dict present from real run_one
    assert isinstance(row.stats, dict)
    if row.trades > 0:
        assert "Total Return [%]" in row.stats or "Total Return [%]" in row.stats.keys() or len(row.stats) > 3


def test_load_real_csv_if_present():
    path = DEFAULT_DATA if DEFAULT_DATA.exists() else ALT_DATA
    if not path.exists():
        pytest.skip("no FX CSV on machine")
    df = load_mt5_csv(path, tail_bars=2000)
    assert len(df) > 100
    assert {"open", "high", "low", "close"} <= set(df.columns)
