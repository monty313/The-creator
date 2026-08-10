"""Smoke tests for 1:1 no-collapse inventory + vectorbt path."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategies.python_batch.inventory_1to1 import (  # noqa: E402
    build_inventory,
    inventory_counts,
    parse_mt_index,
    list_note_files,
)
from strategies.python_batch.mtf import build_set  # noqa: E402
from strategies.python_batch.profiles import entries_for_profile  # noqa: E402
from strategies.python_batch.run_strategy_batch_1to1 import run_one  # noqa: E402


def test_inventory_is_1to1_no_collapses():
    fams = build_inventory()
    c = inventory_counts(fams)
    assert c["total_collapse_entries"] == 0
    assert c["mt_names"] == c["mt_index_parsed"]
    assert c["note_files"] == c["note_files_listed"]
    assert c["total_families"] == c["mt_names"] + c["note_files"]
    assert c["mt_names"] >= 90  # ~95 MT names
    assert c["note_files"] >= 20
    # every family unique
    ids = [f.family_id for f in fams]
    assert len(ids) == len(set(ids))
    # no non-empty collapses
    assert all(f.collapses == [] for f in fams)


def test_mt_and_note_kinds_present():
    fams = build_inventory()
    assert any(f.kind == "mt" for f in fams)
    assert any(f.kind == "note" for f in fams)
    # MT names match index parse
    mt_titles = {f.title for f in fams if f.kind == "mt"}
    parsed = {n for n, _, _ in parse_mt_index()}
    assert mt_titles == parsed
    note_sources = {f.source for f in fams if f.kind == "note"}
    listed = {str(p) for p in list_note_files()}
    assert note_sources == listed


def _toy_m1(n: int = 10000) -> pd.DataFrame:
    rng = np.random.default_rng(7)
    idx = pd.date_range("2024-06-01", periods=n, freq="1min")
    close = 1.1 + np.cumsum(rng.normal(0, 1e-4, n))
    high = close + 1e-4
    low = close - 1e-4
    open_ = np.r_[close[0], close[:-1]]
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close}, index=idx)


def test_vectorbt_path_mt_and_note_families():
    pytest.importorskip("vectorbt")
    fams = build_inventory()
    mt = next(f for f in fams if f.kind == "mt")
    note = next(f for f in fams if f.kind == "note")
    sb = build_set(_toy_m1(), "set3_15m_1h_4h")
    for mode in ("pullback", "continuation"):
        le, se = entries_for_profile(sb, mt.adapter_profile, mode)
        assert len(le) == len(sb.close)
    row_mt = run_one(mt, sb, "continuation")
    row_note = run_one(note, sb, "pullback")
    assert isinstance(row_mt.stats, dict)
    assert isinstance(row_note.stats, dict)
    assert row_mt.family_id != row_note.family_id
