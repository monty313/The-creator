"""Smoke: tweaked pipeline produces win_rate field via real measure path."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategies.python_batch.mtf import build_set  # noqa: E402
from strategies.python_batch.run_tweak_batch import (  # noqa: E402
    WIN_BAR,
    pick_tier,
)


def _toy(n=12000):
    rng = np.random.default_rng(0)
    idx = pd.date_range("2024-03-01", periods=n, freq="1min")
    close = 1.1 + np.cumsum(rng.normal(0, 1e-4, n))
    high = close + 2e-4
    low = close - 2e-4
    open_ = np.r_[close[0], close[:-1]]
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close}, index=idx)


def test_pick_tier_returns_win_rate_and_trades():
    pytest.importorskip("vectorbt")
    m1 = _toy()
    sets = {
        "set2_5m_30m_1h": build_set(m1, "set2_5m_30m_1h"),
        "set3_15m_1h_4h": build_set(m1, "set3_15m_1h_4h"),
    }
    # only two sets for speed — still real pick_tier path
    from strategies.python_batch.mtf import OFFICIAL_SETS

    # monkey-run with partial sets dict
    tier, rows, agg = pick_tier("smoke_mt", "cci_gravity", sets)
    assert "win_rate" in agg
    assert "trades" in agg
    assert isinstance(agg["win_rate"], float)
    assert tier is not None
    assert len(rows) == len(sets) * 2  # PB + cont


def test_results_json_all_above_bar_if_present():
    p = ROOT / "strategies" / "TWEAKED_ACCURACY_RESULTS.json"
    if not p.exists():
        pytest.skip("batch results not generated yet")
    import json

    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["fail_count"] == 0
    assert data["min_win_rate"] > WIN_BAR
    assert data["family_count"] >= 123
    for r in data["results"]:
        assert r["win_rate"] > WIN_BAR
        assert r["trades"] >= data["min_trades"]
        assert r["passed"] is True
