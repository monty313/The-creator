"""Lab HTF force blend: slope + Monty CCI/RSI + doctrine source flags."""
from __future__ import annotations

import numpy as np

from evidence_court.meta_rl.htf_force import (
    IDX_HTF_CCI_ON,
    IDX_HTF_RSI_ON,
    IDX_HTF_SLOPE_ON,
    combine_htf_force,
    compute_htf_force_from_bars,
)
from evidence_court.meta_rl.regimes import (
    RegimeId,
    encode_regime_doctrine,
)


def test_combine_monty_slope_agree_boosts_permission():
    r = combine_htf_force(
        slope_force=0.4,
        slope_agree=True,
        monty_side=1,
        cci_side=1,
        rsi_side=0,
        mode="blend",
    )
    assert r.htf_agree
    assert r.force > 0
    assert r.slope_on == 1.0
    assert r.cci_on == 1.0
    assert r.rsi_on == 0.0
    assert r.reason == "monty_slope_agree"


def test_combine_monty_slope_conflict_kills_agree():
    r = combine_htf_force(
        slope_force=0.4,
        slope_agree=True,
        monty_side=-1,
        cci_side=-1,
        rsi_side=0,
        mode="blend",
    )
    assert not r.htf_agree
    assert r.reason == "monty_slope_conflict"


def test_combine_monty_only_permission():
    r = combine_htf_force(
        slope_force=0.05,
        slope_agree=False,
        monty_side=1,
        cci_side=0,
        rsi_side=1,
        mode="blend",
    )
    assert r.htf_agree
    assert abs(r.force - 0.65) < 1e-9
    assert r.rsi_on == 1.0
    assert r.reason == "monty_only"


def test_slope_only_mode_ignores_monty_for_force():
    r = combine_htf_force(
        slope_force=0.3,
        slope_agree=True,
        monty_side=1,
        cci_side=1,
        rsi_side=1,
        mode="slope",
    )
    assert r.mode == "slope"
    assert r.htf_agree
    assert abs(r.force - 0.3) < 1e-9


def test_doctrine_packs_source_flags_at_12_13_14():
    vec = encode_regime_doctrine(
        RegimeId.TREND_BULL,
        force=0.5,
        efficiency=0.6,
        slope_on=1.0,
        cci_on=1.0,
        rsi_on=0.0,
    )
    assert vec.shape[0] == 16
    assert float(vec[IDX_HTF_SLOPE_ON]) == 1.0
    assert float(vec[IDX_HTF_CCI_ON]) == 1.0
    assert float(vec[IDX_HTF_RSI_ON]) == 0.0
    # zeros default
    z = encode_regime_doctrine(RegimeId.INCOMPLETE)
    assert float(z[12]) == 0.0 and float(z[13]) == 0.0 and float(z[14]) == 0.0


def _synthetic_bars(n: int = 120, drift: float = 0.02) -> list:
    bars = []
    px = 100.0
    for i in range(n):
        px = px * (1.0 + drift * 0.01)
        bars.append(
            {
                "date": f"2026-01-{(i // 20) + 1:02d}",
                "time": f"{(i % 20):02d}:00:00",
                "open": px,
                "high": px * 1.001,
                "low": px * 0.999,
                "close": px,
            }
        )
    return bars


def test_compute_htf_force_blend_runs_on_bars():
    h1 = _synthetic_bars(150, drift=0.05)
    h2 = _synthetic_bars(150, drift=0.04)
    r0 = compute_htf_force_from_bars(h1, h2, monty_htf_blend=False)
    assert r0.mode == "slope"
    r1 = compute_htf_force_from_bars(h1, h2, monty_htf_blend=True)
    assert r1.mode == "blend"
    # uptrend synthetic → force should not be strongly negative
    assert r1.force >= -0.2
