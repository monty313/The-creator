"""Overlay Court principles onto REAL charts (TradingView captures + MT5/M1 data).

Uses cv2 only. Language: Force / Pullback / Resume (never load/reclaim).
TradingView CDP optional — falls back to artifacts/tv_xau_tf_*.png.
"""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ART = Path(__file__).resolve().parent
OUT = ART / "policy_principles_on_charts"
OUT.mkdir(parents=True, exist_ok=True)

# BGR
WHITE = (235, 235, 235)
GOLD = (40, 180, 220)
GREEN = (80, 200, 120)
RED = (80, 80, 220)
CYAN = (200, 200, 80)
ORANGE = (60, 140, 255)
PURPLE = (200, 120, 180)
MUTED = (160, 160, 170)
DARK = (0, 0, 0)

TV_SHOTS = {
    "1m": ART / "tv_xau_tf_1m.png",
    "15m": ART / "tv_xau_tf_15m.png",
    "30m": ART / "tv_xau_tf_30m.png",
    "day12": ART / "tv_day12_chart_view.png",
}

XAU_M1 = Path(
    r"C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\the-truth\data\raw\XAUUSD_M1_full.csv"
)


def put(img, text, xy, scale=0.55, color=WHITE, thick=1):
    cv2.putText(
        img, text, xy, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick, cv2.LINE_AA
    )


def banner_top(img, lines: Sequence[Tuple[str, tuple]], h_frac: float = 0.22):
    """Semi-transparent principle banner on top of real chart."""
    h, w = img.shape[:2]
    bh = max(90, int(h * h_frac))
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (w, bh), (12, 12, 16), -1)
    out = cv2.addWeighted(overlay, 0.72, img, 0.28, 0)
    y = 28
    for text, col in lines:
        put(out, text[:110], (16, y), 0.55 if y > 40 else 0.7, col, 2 if y < 40 else 1)
        y += 26
    return out


def banner_bottom(img, text: str, color=CYAN):
    h, w = img.shape[:2]
    overlay = img.copy()
    cv2.rectangle(overlay, (0, h - 48), (w, h), (12, 12, 16), -1)
    out = cv2.addWeighted(overlay, 0.7, img, 0.3, 0)
    put(out, text[:120], (16, h - 18), 0.5, color, 1)
    return out


def side_rail(img, title: str, bullets: Sequence[str], color=GOLD):
    """Right-side principle rail on real chart."""
    h, w = img.shape[:2]
    rw = min(340, max(260, w // 3))
    x0 = w - rw
    overlay = img.copy()
    cv2.rectangle(overlay, (x0, 0), (w, h), (18, 18, 24), -1)
    out = cv2.addWeighted(overlay, 0.78, img, 0.22, 0)
    put(out, title[:28], (x0 + 12, 36), 0.6, color, 2)
    y = 70
    for b in bullets:
        for i in range(0, len(b), 32):
            put(out, b[i : i + 32], (x0 + 12, y), 0.42, WHITE, 1)
            y += 20
        y += 8
        if y > h - 60:
            break
    put(out, "Policy eyes on REAL chart", (x0 + 12, h - 40), 0.4, MUTED, 1)
    put(out, "cv2 overlay | not edge engine", (x0 + 12, h - 18), 0.38, MUTED, 1)
    return out


def load_tv(path: Path) -> Optional[np.ndarray]:
    if not path.is_file():
        return None
    img = cv2.imread(str(path))
    return img


def annotate_force_pullback_resume(img: np.ndarray, tf_label: str) -> np.ndarray:
    """Principle 04 on a live/TV chart."""
    out = banner_top(
        img,
        [
            (f"PRINCIPLE: FORCE -> PULLBACK -> RESUME  |  TV chart  {tf_label}", GOLD),
            ("FORCE = HTF permission (tide). No Force = I wait.", GREEN),
            ("PULLBACK = LTF dip against tide. I still wait (no dip-chase).", ORANGE),
            ("RESUME = return with Force. Then I may fire.", CYAN),
        ],
    )
    out = banner_bottom(
        out,
        "I am the Policy. This is a REAL chart. Geometry over indicator names. Source: TradingView capture.",
    )
    # legend boxes lower-left
    h, w = out.shape[:2]
    x, y = 20, h - 160
    for lab, col in (
        ("FORCE", GREEN),
        ("PULLBACK", ORANGE),
        ("RESUME", CYAN),
    ):
        cv2.rectangle(out, (x, y), (x + 110, y + 36), col, 2)
        put(out, lab, (x + 12, y + 25), 0.5, col, 1)
        x += 125
    return out


def annotate_three_tf_roles(img: np.ndarray, role: str, tf: str) -> np.ndarray:
    """Mark set stack role on this TF chart."""
    role_u = role.upper()
    meaning = {
        "LTF": "TIMING — pullback / resume / continuation on this clock",
        "HTF1": "FORCE — mid confirmation of tide",
        "HTF2": "FORCE — higher confirmation of tide",
    }.get(role_u, "Mark set role")
    out = banner_top(
        img,
        [
            (f"MARK SET ROLE: {role_u} = {tf}  |  TradingView", GOLD),
            (meaning, CYAN),
            ("Never average all TFs into mush force. Each role is distinct.", WHITE),
            ("Set1 stack: LTF 1m | HTF1 15m | HTF2 30m", MUTED),
        ],
    )
    out = side_rail(
        out,
        "Policy principle",
        [
            "HTF gives permission",
            "LTF times the entry",
            "pullback_resume OK",
            "continuation OK",
            "no Force = WAIT",
            "A13: 8-400 trades/day",
            "breach must stay 0",
            "no retrain at prove",
        ],
        GOLD,
    )
    return out


def annotate_mission(img: np.ndarray) -> np.ndarray:
    out = banner_top(
        img,
        [
            ("MISSION A31 on REAL MARKET  |  TradingView / MT5 data path", GOLD),
            ("ONE bot. Target% and Risk% change STATE, not WEIGHTS.", GREEN),
            ("Breach 0 absolute. Scalper MUST land 8-400 trades/day (A13).", RED),
            ("Train offline. Freeze at prove. Measure dual. Court PROMOTE only.", ORANGE),
        ],
    )
    return banner_bottom(
        out, "Evidence: principles painted on live-style chart — Policy understanding"
    )


def annotate_mental_replay(img: np.ndarray) -> np.ndarray:
    out = banner_top(
        img,
        [
            ("MENTAL REPLAY on chart  |  BEFORE / DURING / AFTER x 3 TFs", GOLD),
            ("BEFORE: Force side + pullback/resume setup", GREEN),
            ("DURING: hold with Force or thrash on LTF noise?", ORANGE),
            ("AFTER: still Force? exit quality? outcome tags teach offline", CYAN),
        ],
        h_frac=0.2,
    )
    h, w = out.shape[:2]
    # 3 phase labels across chart mid
    for i, (lab, col) in enumerate(
        (("BEFORE", GREEN), ("DURING", ORANGE), ("AFTER", CYAN))
    ):
        x = int(w * (0.12 + i * 0.28))
        cv2.rectangle(out, (x, h // 2 - 20), (x + 140, h // 2 + 20), col, 2)
        put(out, lab, (x + 20, h // 2 + 8), 0.6, col, 2)
    return banner_bottom(
        out, "Offline journal only — I do not retrain from this at prove (A14)"
    )


def annotate_senses(img: np.ndarray) -> np.ndarray:
    out = banner_top(
        img,
        [
            ("SENSES A32 on market picture  |  pack into my brain", GOLD),
            ("SIGHT structure  |  FEEL pullback tension  |  TASTE edge+goal  |  HEAR regime", CYAN),
            ("Fail: flat on B&B day | freeze on tension | all bars equal | thrash reverse", RED),
        ],
    )
    return side_rail(
        out,
        "Not folklore RSI",
        [
            "Relative to edge",
            "Every official set",
            "Drive the brain",
            "Not probe-only",
        ],
        PURPLE,
    )


def load_m1_bars(path: Path, date: str = "2026-01-21", limit: int = 180) -> List[dict]:
    """Load MT5-style M1 CSV (flexible columns)."""
    if not path.is_file():
        return []
    rows: List[dict] = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        # sniff header
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(f, dialect=dialect)
        if not reader.fieldnames:
            return []
        fields = {n.lower().strip(): n for n in reader.fieldnames}

        def col(*names):
            for n in names:
                if n in fields:
                    return fields[n]
            for k, v in fields.items():
                for n in names:
                    if n in k:
                        return v
            return None

        c_date = col("date", "time", "datetime", "timestamp")
        c_o = col("open", "o")
        c_h = col("high", "h")
        c_l = col("low", "l")
        c_c = col("close", "c")
        if not all([c_o, c_h, c_l, c_c]):
            return []
        for r in reader:
            raw_t = str(r.get(c_date, "") or "")
            if date and date not in raw_t and not raw_t.startswith(date):
                # also allow YYYY.MM.DD
                d2 = date.replace("-", ".")
                if d2 not in raw_t:
                    continue
            try:
                rows.append(
                    {
                        "t": raw_t,
                        "open": float(r[c_o]),
                        "high": float(r[c_h]),
                        "low": float(r[c_l]),
                        "close": float(r[c_c]),
                    }
                )
            except (TypeError, ValueError, KeyError):
                continue
            if len(rows) >= limit:
                break
    return rows


def render_mt5_candles(
    bars: Sequence[dict],
    *,
    w: int = 1280,
    h: int = 720,
    title: str = "XAUUSD M1 (MT5 data path)",
) -> np.ndarray:
    """Paint OHLC candles from MT5/local CSV — real prices, cv2 canvas."""
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = (22, 22, 28)
    if len(bars) < 5:
        put(img, "No M1 bars — check XAUUSD CSV path", (40, 80), 0.7, RED, 2)
        return img

    put(img, title, (20, 36), 0.7, GOLD, 2)
    put(img, f"bars={len(bars)}  source=local MT5-style CSV  (not synthetic random)", (20, 64), 0.45, MUTED, 1)

    pad_l, pad_r, pad_t, pad_b = 60, 40, 90, 50
    chart_w = w - pad_l - pad_r
    chart_h = h - pad_t - pad_b
    highs = [b["high"] for b in bars]
    lows = [b["low"] for b in bars]
    lo, hi = min(lows), max(highs)
    span = max(hi - lo, 1e-9)

    def ypx(price: float) -> int:
        return int(pad_t + (hi - price) / span * chart_h)

    n = len(bars)
    bw = max(2, chart_w // n - 1)
    for i, b in enumerate(bars):
        x = pad_l + int(i * chart_w / n)
        y_o, y_c = ypx(b["open"]), ypx(b["close"])
        y_h, y_l = ypx(b["high"]), ypx(b["low"])
        up = b["close"] >= b["open"]
        col = GREEN if up else RED
        cv2.line(img, (x + bw // 2, y_h), (x + bw // 2, y_l), col, 1)
        y1, y2 = min(y_o, y_c), max(y_o, y_c)
        if y2 - y1 < 1:
            y2 = y1 + 1
        cv2.rectangle(img, (x, y1), (x + bw, y2), col, -1)

    # Force / Pullback / Resume legend on MT5 chart
    put(img, "Geometry to see here:", (20, h - 28), 0.5, WHITE, 1)
    put(img, "FORCE (tide)", (280, h - 28), 0.5, GREEN, 1)
    put(img, "PULLBACK (dip)", (430, h - 28), 0.5, ORANGE, 1)
    put(img, "RESUME (with tide)", (610, h - 28), 0.5, CYAN, 1)
    return img


def collage_three_tv(paths: dict) -> Optional[np.ndarray]:
    """Stack LTF/HTF1/HTF2 TV shots with role labels (Mark set1)."""
    imgs = []
    labels = [("LTF", "1m"), ("HTF1", "15m"), ("HTF2", "30m")]
    for role, tf in labels:
        p = paths.get(tf)
        im = load_tv(p) if p else None
        if im is None:
            return None
        im = cv2.resize(im, (900, 320))
        put(im, f"{role} = {tf}", (16, 36), 0.9, GOLD, 2)
        imgs.append(im)
    # title strip
    title = np.zeros((70, 900, 3), dtype=np.uint8)
    title[:] = (18, 18, 22)
    put(title, "MARK SET1 on TradingView: 1m + 15m + 30m  |  Force from HTFs, timing on LTF", (12, 44), 0.55, GOLD, 2)
    return np.vstack([title] + imgs)


def save(name: str, img: np.ndarray) -> Path:
    p = OUT / name
    cv2.imwrite(str(p), img)
    print("wrote", p, img.shape)
    return p


def main():
    written: List[Path] = []

    # --- TradingView real captures ---
    for tf, path in list(TV_SHOTS.items())[:3]:
        im = load_tv(path)
        if im is None:
            print("missing TV shot", path)
            continue
        role = {"1m": "LTF", "15m": "HTF1", "30m": "HTF2"}.get(tf, "TF")
        a = annotate_three_tf_roles(im, role, tf)
        written.append(save(f"tv_{tf}_role_{role.lower()}.png", a))
        b = annotate_force_pullback_resume(im, tf)
        written.append(save(f"tv_{tf}_force_pullback_resume.png", b))

    day12 = load_tv(TV_SHOTS["day12"])
    if day12 is not None:
        written.append(save("tv_day12_mission_a31.png", annotate_mission(day12)))
        written.append(
            save("tv_day12_mental_replay.png", annotate_mental_replay(day12))
        )
        written.append(save("tv_day12_senses_a32.png", annotate_senses(day12)))

    col = collage_three_tv(TV_SHOTS)
    if col is not None:
        written.append(save("tv_set1_collage_1m_15m_30m.png", col))

    # --- MT5 / local M1 path ---
    bars = load_m1_bars(XAU_M1, date="2026-01-21", limit=200)
    if not bars:
        # try any recent chunk: last rows of file without date filter
        bars = load_m1_bars(XAU_M1, date="", limit=200)
    mt5 = render_mt5_candles(
        bars,
        title="XAUUSD M1 from MT5 data path (local CSV)",
    )
    written.append(save("mt5_xau_m1_raw_candles.png", mt5))
    written.append(
        save(
            "mt5_xau_m1_force_pullback_resume.png",
            annotate_force_pullback_resume(mt5, "M1 MT5-data"),
        )
    )
    written.append(save("mt5_xau_m1_mission.png", annotate_mission(mt5)))
    written.append(save("mt5_xau_m1_senses.png", annotate_senses(mt5)))

    # index
    idx = np.zeros((520, 1000, 3), dtype=np.uint8)
    idx[:] = (18, 18, 22)
    put(idx, "INDEX — Principles on REAL charts (TV + MT5 data)", (20, 40), 0.7, GOLD, 2)
    put(idx, f"folder: {OUT.as_posix()}", (20, 70), 0.45, MUTED, 1)
    put(idx, "TradingView CDP was offline — used saved TV captures + MT5 CSV.", (20, 100), 0.45, ORANGE, 1)
    y = 140
    for p in written:
        put(idx, p.name, (20, y), 0.45, WHITE, 1)
        y += 22
    written.append(save("00_index.png", idx))
    print("DONE", len(written), "files ->", OUT)


if __name__ == "__main__":
    main()
