"""HTF momentum definitions: Court slope vs Monty CCI/RSI+BB conditions.

EXPERIMENTAL MEASURE ONLY — does not change production edge / champion.
Compare predictive hit-rate and a simple permission-trading proxy.

Slope (current Court primitive)
-------------------------------
  trend_dir on each HTF close series, lookback=5:
    a = close[i - 5], b = close[i]
    ret = (b - a) / abs(a)
    score = clip(ret * 50, -1, +1)
  Pair agree: same sign and |f| >= 0.12 on both HTFs of a set.
  Force = mean(f1, f2); if not agree, force *= 0.35 (edge path).
  Strong slope bull/bear for this study: agree and force sign clear
  (|force| >= 0.20 after mean, with agree).

Monty Condition 1 (CCI + BB) — both HTFs
----------------------------------------
  CCI periods 10, 30, 100.
  BB(10, 0.5) on each CCI series (mid = SMA of that CCI).
  Strong bull: all 3 CCI > their BB mid on HTF1 AND on HTF2.
  Strong bear: all 3 CCI < their BB mid on HTF1 AND on HTF2.

Monty Condition 2 (RSI + BB) — both HTFs
----------------------------------------
  RSI periods 5, 15.
  BB(10, 0.5) on each RSI series.
  Bull: both RSI > BB mid on HTF1 AND HTF2.
  Bear: both RSI < BB mid on HTF1 AND HTF2.

Strong trending market (Monty): Condition1 OR Condition2 active
(same side). Measured separately and as OR-union.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .edge import _ltf_timing_signal
from .indicators import (
    cci,
    resample_m1_to_tf,
    rsi,
    series_above_bb_mid,
    series_below_bb_mid,
    trend_dir_series,
)
from .price_io import SYMBOL_FILES, available_symbols, load_m1_trailing_calendar_days
from .sets import OFFICIAL_SETS

# BB on oscillators: user did not specify Mark LTF shift+2 → use 0 for HTF defs
BB_PERIOD = 10
BB_DEV = 0.5
BB_SHIFT = 0
SLOPE_LOOKBACK = 5
SLOPE_AGREE_MIN = 0.12
SLOPE_STRONG_MIN = 0.20
CCI_PERIODS = (10, 30, 100)
RSI_PERIODS = (5, 15)

DEFAULT_OUT = Path("evidence_court/artifacts/htf_momentum_compare_report.json")


@dataclass
class MomentumFlags:
    """Per-bar flags on an aligned sample (one set, two HTFs synced by time)."""
    slope_bull: bool = False
    slope_bear: bool = False
    cci_bull: bool = False
    cci_bear: bool = False
    rsi_bull: bool = False
    rsi_bear: bool = False

    @property
    def monty_bull(self) -> bool:
        """Strong bull: Condition1 OR Condition2."""
        return self.cci_bull or self.rsi_bull

    @property
    def monty_bear(self) -> bool:
        return self.cci_bear or self.rsi_bear


def _ohlc(bars: Sequence[dict]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    o = np.array([float(b["open"]) for b in bars], dtype=np.float64)
    h = np.array([float(b["high"]) for b in bars], dtype=np.float64)
    l = np.array([float(b["low"]) for b in bars], dtype=np.float64)
    c = np.array([float(b["close"]) for b in bars], dtype=np.float64)
    return o, h, l, c


def _bar_key(b: dict) -> str:
    return f"{b['date']}T{b.get('time', '00:00:00')}"


def slope_series_flags(
    closes: np.ndarray,
    *,
    lookback: int = SLOPE_LOOKBACK,
    agree_min: float = SLOPE_AGREE_MIN,
    strong_min: float = SLOPE_STRONG_MIN,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (score, strong_bull, strong_bear) series for one HTF (strong needs pair later)."""
    score = trend_dir_series(closes, lookback=lookback)
    # single-TF strength flags used only after pair combine
    strong_up = score >= strong_min
    strong_dn = score <= -strong_min
    return score, strong_up, strong_dn


def pair_slope_flags(
    f1: np.ndarray,
    f2: np.ndarray,
    *,
    agree_min: float = SLOPE_AGREE_MIN,
    strong_min: float = SLOPE_STRONG_MIN,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Align length min; return force, bull, bear with Court agree rule."""
    n = min(f1.size, f2.size)
    f1, f2 = f1[-n:], f2[-n:]
    force = 0.5 * (f1 + f2)
    agree = (f1 * f2 > 0) & (np.abs(f1) >= agree_min) & (np.abs(f2) >= agree_min)
    force = np.where(agree, force, force * 0.35)
    bull = agree & (force >= strong_min)
    bear = agree & (force <= -strong_min)
    return force, bull, bear


def single_tf_cci_bb_side(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Per bar: all CCI periods above/below their BB mid."""
    n = close.size
    above_all = np.ones(n, dtype=bool)
    below_all = np.ones(n, dtype=bool)
    for p in CCI_PERIODS:
        series = cci(high, low, close, period=p)
        ab = series_above_bb_mid(series, BB_PERIOD, BB_DEV, BB_SHIFT)
        be = series_below_bb_mid(series, BB_PERIOD, BB_DEV, BB_SHIFT)
        # need finite CCI
        finite = np.isfinite(series)
        above_all &= ab & finite
        below_all &= be & finite
    return above_all, below_all


def single_tf_rsi_bb_side(close: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    n = close.size
    above_all = np.ones(n, dtype=bool)
    below_all = np.ones(n, dtype=bool)
    for p in RSI_PERIODS:
        series = rsi(close, period=p)
        ab = series_above_bb_mid(series, BB_PERIOD, BB_DEV, BB_SHIFT)
        be = series_below_bb_mid(series, BB_PERIOD, BB_DEV, BB_SHIFT)
        finite = np.isfinite(series)
        above_all &= ab & finite
        below_all &= be & finite
    return above_all, below_all


def pair_bool_and(a1: np.ndarray, a2: np.ndarray) -> np.ndarray:
    n = min(a1.size, a2.size)
    return a1[-n:] & a2[-n:]


def compute_set_momentum_series(
    m1: Sequence[dict],
    ltf: str,
    htf1: str,
    htf2: str,
) -> Dict[str, Any]:
    """Build aligned momentum flags on the slower HTF clock (htf2), sample when both exist."""
    b1 = resample_m1_to_tf(m1, htf1)
    b2 = resample_m1_to_tf(m1, htf2)
    bl = resample_m1_to_tf(m1, ltf)
    if len(b1) < 120 or len(b2) < 120 or len(bl) < 120:
        return {"ok": False, "error": "short_history"}

    _, h1, l1, c1 = _ohlc(b1)
    _, h2, l2, c2 = _ohlc(b2)
    _, _, _, cl = _ohlc(bl)

    # Slope series
    s1 = trend_dir_series(c1, SLOPE_LOOKBACK)
    s2 = trend_dir_series(c2, SLOPE_LOOKBACK)

    # Align HTF1 onto HTF2 timestamps by last-known value (as-of join)
    keys1 = [_bar_key(b) for b in b1]
    keys2 = [_bar_key(b) for b in b2]
    # map date-only for daily mix: use sequential as-of by bar index ratio
    # Prefer key match on date for 1d; for intraday floor htf1 to htf2
    f1_on_2 = _asof_series(keys1, s1, keys2)
    f2 = s2
    force, slope_bull, slope_bear = pair_slope_flags(f1_on_2, f2)

    cci_b1, cci_s1 = single_tf_cci_bb_side(h1, l1, c1)
    cci_b2, cci_s2 = single_tf_cci_bb_side(h2, l2, c2)
    cci_bull = pair_bool_and(_asof_bool(keys1, cci_b1, keys2), cci_b2)
    cci_bear = pair_bool_and(_asof_bool(keys1, cci_s1, keys2), cci_s2)

    rsi_b1, rsi_s1 = single_tf_rsi_bb_side(c1)
    rsi_b2, rsi_s2 = single_tf_rsi_bb_side(c2)
    rsi_bull = pair_bool_and(_asof_bool(keys1, rsi_b1, keys2), rsi_b2)
    rsi_bear = pair_bool_and(_asof_bool(keys1, rsi_s1, keys2), rsi_s2)

    n = force.size
    # forward return on HTF2: next k bars
    fwd_1 = _forward_ret(c2[-n:], 1)
    fwd_3 = _forward_ret(c2[-n:], 3)
    fwd_5 = _forward_ret(c2[-n:], 5)

    # LTF timing labels aligned to HTF2 (as-of)
    keys_l = [_bar_key(b) for b in bl]
    # for each htf2 bar, use force sign for LTF signal quality proxy
    ltf_act = []
    for i in range(n):
        # find ltf end index <= this htf2 time
        idx = _asof_index(keys_l, keys2[-n + i] if n else keys2[i])
        if idx is None or idx < 25:
            ltf_act.append("wait")
            continue
        # use force at i
        frc = float(force[i])
        window = cl[max(0, idx - 80) : idx + 1]
        topo, act, _, _ = _ltf_timing_signal(window, frc)
        ltf_act.append(act if act in ("long", "short") else "wait")

    return {
        "ok": True,
        "n": n,
        "force": force,
        "slope_bull": slope_bull,
        "slope_bear": slope_bear,
        "cci_bull": cci_bull[-n:] if cci_bull.size >= n else cci_bull,
        "cci_bear": cci_bear[-n:] if cci_bear.size >= n else cci_bear,
        "rsi_bull": rsi_bull[-n:] if rsi_bull.size >= n else rsi_bull,
        "rsi_bear": rsi_bear[-n:] if rsi_bear.size >= n else rsi_bear,
        "monty_bull": None,  # filled below
        "monty_bear": None,
        "fwd_1": fwd_1,
        "fwd_3": fwd_3,
        "fwd_5": fwd_5,
        "ltf_act": ltf_act,
        "close_htf2": c2[-n:],
    }


def _asof_series(keys_src: List[str], values: np.ndarray, keys_dst: List[str]) -> np.ndarray:
    """Last-known value from src for each dst key (lexicographic time keys)."""
    out = np.zeros(len(keys_dst), dtype=np.float64)
    j = 0
    last = 0.0
    for i, kd in enumerate(keys_dst):
        while j < len(keys_src) and keys_src[j] <= kd:
            last = float(values[j])
            j += 1
        out[i] = last
    return out


def _asof_bool(keys_src: List[str], values: np.ndarray, keys_dst: List[str]) -> np.ndarray:
    out = np.zeros(len(keys_dst), dtype=bool)
    j = 0
    last = False
    for i, kd in enumerate(keys_dst):
        while j < len(keys_src) and keys_src[j] <= kd:
            last = bool(values[j])
            j += 1
        out[i] = last
    return out


def _asof_index(keys_src: List[str], key_dst: str) -> Optional[int]:
    # binary-ish linear last index <= key
    lo, hi = 0, len(keys_src) - 1
    ans = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if keys_src[mid] <= key_dst:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans


def _forward_ret(closes: np.ndarray, k: int) -> np.ndarray:
    c = np.asarray(closes, dtype=np.float64)
    n = c.size
    out = np.full(n, np.nan)
    for i in range(n - k):
        a = c[i]
        if a == 0:
            continue
        out[i] = (c[i + k] - a) / abs(a)
    return out


def _stats_for_mask(
    mask: np.ndarray,
    side: str,
    fwd: np.ndarray,
) -> Dict[str, float]:
    """Predictive: bull mask should have fwd>0; bear mask fwd<0."""
    m = np.asarray(mask, dtype=bool) & np.isfinite(fwd)
    n = int(m.sum())
    if n == 0:
        return {"n": 0, "hit_rate": float("nan"), "mean_fwd": float("nan"), "coverage": 0.0}
    r = fwd[m]
    if side == "bull":
        hits = r > 0
    else:
        hits = r < 0
    return {
        "n": n,
        "hit_rate": float(np.mean(hits)),
        "mean_fwd": float(np.mean(r)),
        "coverage": float(n / max(mask.size, 1)),
    }


def _trade_proxy(
    mask_bull: np.ndarray,
    mask_bear: np.ndarray,
    ltf_act: List[str],
    fwd: np.ndarray,
) -> Dict[str, float]:
    """When HTF strong + LTF same-side fire, score forward HTF return as proxy P&L sign."""
    wins = 0
    n = 0
    pnls: List[float] = []
    for i in range(min(len(ltf_act), fwd.size)):
        if not np.isfinite(fwd[i]):
            continue
        act = ltf_act[i]
        if act == "long" and bool(mask_bull[i]):
            n += 1
            pnls.append(float(fwd[i]))
            if fwd[i] > 0:
                wins += 1
        elif act == "short" and bool(mask_bear[i]):
            n += 1
            # short profits when fwd < 0
            pnls.append(float(-fwd[i]))
            if fwd[i] < 0:
                wins += 1
    if n == 0:
        return {"n_trades": 0, "win_rate": float("nan"), "mean_proxy_pnl": float("nan")}
    return {
        "n_trades": n,
        "win_rate": wins / n,
        "mean_proxy_pnl": float(np.mean(pnls)),
    }


def evaluate_pack(pack: Dict[str, Any]) -> Dict[str, Any]:
    if not pack.get("ok"):
        return pack
    n = int(pack["n"])
    slope_bull = np.asarray(pack["slope_bull"], dtype=bool)[-n:]
    slope_bear = np.asarray(pack["slope_bear"], dtype=bool)[-n:]
    cci_bull = np.asarray(pack["cci_bull"], dtype=bool)[-n:]
    cci_bear = np.asarray(pack["cci_bear"], dtype=bool)[-n:]
    rsi_bull = np.asarray(pack["rsi_bull"], dtype=bool)[-n:]
    rsi_bear = np.asarray(pack["rsi_bear"], dtype=bool)[-n:]
    monty_bull = cci_bull | rsi_bull
    monty_bear = cci_bear | rsi_bear
    fwd5 = np.asarray(pack["fwd_5"], dtype=np.float64)[-n:]
    fwd3 = np.asarray(pack["fwd_3"], dtype=np.float64)[-n:]
    ltf_act = list(pack["ltf_act"])[-n:]

    methods = {
        "slope": (slope_bull, slope_bear),
        "cci_bb_cond1": (cci_bull, cci_bear),
        "rsi_bb_cond2": (rsi_bull, rsi_bear),
        "monty_or_cond1_or_cond2": (monty_bull, monty_bear),
    }
    out: Dict[str, Any] = {"n_bars": n, "methods": {}}
    for name, (bu, be) in methods.items():
        pred = {
            "bull_fwd5": _stats_for_mask(bu, "bull", fwd5),
            "bear_fwd5": _stats_for_mask(be, "bear", fwd5),
            "bull_fwd3": _stats_for_mask(bu, "bull", fwd3),
            "bear_fwd3": _stats_for_mask(be, "bear", fwd3),
        }
        # combined directional hit when either side active
        both = bu | be
        side = np.where(bu, 1.0, np.where(be, -1.0, 0.0))
        m = both & np.isfinite(fwd5)
        if m.sum():
            # hit if sign(fwd) matches side
            hit = (np.sign(fwd5[m]) == side[m]) | ((fwd5[m] == 0) & (side[m] == 0))
            # zero fwd rare; require strict sign match for non-zero side
            hit = np.sign(fwd5[m]) * side[m] > 0
            comb_hr = float(np.mean(hit))
            comb_n = int(m.sum())
        else:
            comb_hr, comb_n = float("nan"), 0
        trade = _trade_proxy(bu, be, ltf_act, fwd5)
        out["methods"][name] = {
            "predictive": pred,
            "combined_active_hit_rate_fwd5": comb_hr,
            "combined_active_n": comb_n,
            "coverage_any": float(both.mean()),
            "trade_proxy_ltf_align_fwd5": trade,
        }
    return out


def run_compare(
    *,
    symbols: Optional[Sequence[str]] = None,
    n_days: int = 90,
    sets: Optional[Sequence[int]] = None,
    out_path: Path | str = DEFAULT_OUT,
) -> Dict[str, Any]:
    syms = list(symbols) if symbols else [s for s in ("XAUUSD", "EURUSD", "GBPUSD") if s in available_symbols()]
    set_ids = list(sets) if sets else [1, 2, 3, 4]
    report: Dict[str, Any] = {
        "law": "experimental_htf_momentum_compare",
        "slope_formula": {
            "name": "trend_dir",
            "lookback_bars": SLOPE_LOOKBACK,
            "a": "close[i - lookback]",
            "b": "close[i]",
            "ret": "(b - a) / abs(a)",
            "score": "clip(ret * 50, -1, +1)",
            "pair_agree": f"same sign and |f| >= {SLOPE_AGREE_MIN} on both HTFs",
            "strong": f"agree and |mean force| >= {SLOPE_STRONG_MIN}",
            "note": "This is what production edge uses for HTF force (agree + mean).",
        },
        "monty_cond1": {
            "cci_periods": list(CCI_PERIODS),
            "bb": {"period": BB_PERIOD, "dev": BB_DEV, "shift": BB_SHIFT},
            "bull": "all 3 CCI > BB mid on both HTFs",
            "bear": "all 3 CCI < BB mid on both HTFs",
        },
        "monty_cond2": {
            "rsi_periods": list(RSI_PERIODS),
            "bb": {"period": BB_PERIOD, "dev": BB_DEV, "shift": BB_SHIFT},
            "bull": "both RSI > BB mid on both HTFs",
            "bear": "both RSI < BB mid on both HTFs",
        },
        "strong_trend_monty": "cond1 OR cond2 (same side)",
        "symbols": syms,
        "n_days": n_days,
        "rows": [],
        "aggregate": {},
    }

    # aggregate accumulators
    agg: Dict[str, Dict[str, List[float]]] = {}

    for sym in syms:
        path = SYMBOL_FILES.get(sym)
        if path is None or not path.exists():
            continue
        m1 = load_m1_trailing_calendar_days(path, n_days=n_days + 15)
        if len(m1) < 500:
            continue
        for s in OFFICIAL_SETS:
            if s.set_id not in set_ids:
                continue
            h1, h2 = s.confirmation_tfs[0], s.confirmation_tfs[1]
            pack = compute_set_momentum_series(m1, s.entry_tf, h1, h2)
            if not pack.get("ok"):
                continue
            ev = evaluate_pack(pack)
            row = {
                "symbol": sym,
                "set_id": s.set_id,
                "set_name": s.name,
                "stack": list(s.tfs),
                "eval": ev,
            }
            report["rows"].append(row)
            for mname, mdat in ev.get("methods", {}).items():
                bucket = agg.setdefault(
                    mname,
                    {
                        "hit_rates": [],
                        "coverages": [],
                        "trade_win_rates": [],
                        "trade_ns": [],
                        "mean_proxy_pnls": [],
                        "combined_ns": [],
                    },
                )
                hr = mdat.get("combined_active_hit_rate_fwd5")
                if hr == hr:  # not nan
                    bucket["hit_rates"].append(float(hr))
                    bucket["combined_ns"].append(float(mdat.get("combined_active_n") or 0))
                bucket["coverages"].append(float(mdat.get("coverage_any") or 0))
                tr = mdat.get("trade_proxy_ltf_align_fwd5") or {}
                wr = tr.get("win_rate")
                if wr == wr:
                    bucket["trade_win_rates"].append(float(wr))
                    bucket["trade_ns"].append(float(tr.get("n_trades") or 0))
                mp = tr.get("mean_proxy_pnl")
                if mp == mp:
                    bucket["mean_proxy_pnls"].append(float(mp))

    summary = {}
    for mname, b in agg.items():
        def _wavg(vals: List[float], weights: List[float]) -> float:
            if not vals:
                return float("nan")
            if weights and len(weights) == len(vals) and sum(weights) > 0:
                return float(np.average(vals, weights=weights))
            return float(np.mean(vals))

        summary[mname] = {
            "mean_predictive_hit_rate_fwd5": _wavg(b["hit_rates"], b["combined_ns"]),
            "mean_coverage": float(np.mean(b["coverages"])) if b["coverages"] else float("nan"),
            "mean_trade_proxy_win_rate": _wavg(b["trade_win_rates"], b["trade_ns"]),
            "total_trade_proxy_n": int(sum(b["trade_ns"])),
            "mean_proxy_pnl": float(np.mean(b["mean_proxy_pnls"])) if b["mean_proxy_pnls"] else float("nan"),
            "n_set_symbol_rows": len(b["hit_rates"]),
        }
    report["aggregate"] = summary

    # rank methods by predictive hit then trade win
    ranked = sorted(
        summary.items(),
        key=lambda kv: (
            -1.0 if kv[1]["mean_predictive_hit_rate_fwd5"] != kv[1]["mean_predictive_hit_rate_fwd5"]
            else -float(kv[1]["mean_predictive_hit_rate_fwd5"]),
            -1.0 if kv[1]["mean_trade_proxy_win_rate"] != kv[1]["mean_trade_proxy_win_rate"]
            else -float(kv[1]["mean_trade_proxy_win_rate"]),
        ),
    )
    report["rank_by_predictive_then_trade"] = [
        {"method": k, **v} for k, v in ranked
    ]
    if ranked:
        report["winner_predictive"] = ranked[0][0]
        # separate trade winner
        tr = sorted(
            summary.items(),
            key=lambda kv: (
                -1.0 if kv[1]["mean_trade_proxy_win_rate"] != kv[1]["mean_trade_proxy_win_rate"]
                else -float(kv[1]["mean_trade_proxy_win_rate"]),
                -float(kv[1].get("total_trade_proxy_n") or 0),
            ),
        )
        report["winner_trade_proxy"] = tr[0][0] if tr else None

    outp = Path(out_path)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    report["out_path"] = str(outp)
    return report


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Compare HTF slope vs Monty CCI/RSI momentum")
    p.add_argument("--days", type=int, default=90)
    p.add_argument("--out", type=str, default=str(DEFAULT_OUT))
    p.add_argument("--symbols", type=str, default="XAUUSD,EURUSD,GBPUSD")
    args = p.parse_args(list(argv) if argv is not None else None)
    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    rep = run_compare(symbols=syms, n_days=int(args.days), out_path=args.out)
    print(json.dumps({
        "out": rep.get("out_path"),
        "aggregate": rep.get("aggregate"),
        "winner_predictive": rep.get("winner_predictive"),
        "winner_trade_proxy": rep.get("winner_trade_proxy"),
        "n_rows": len(rep.get("rows") or []),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
