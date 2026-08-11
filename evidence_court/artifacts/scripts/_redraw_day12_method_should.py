"""Day 12 ONLY (2026-01-21): redraw how the method SHOULD have played out.

Method (no load/reclaim words):
  FORCE on → WAIT pullback → FIRE on RESUME → HOLD idea → NO thrash re-fire

Uses real M1 prices for that calendar day only.
"""
from __future__ import annotations

from pathlib import Path

# artifacts/ is parent of scripts/
ARTIFACTS = Path(__file__).resolve().parent.parent
from typing import Dict, List, Sequence, Tuple

import cv2
import numpy as np

from evidence_court.meta_rl.price_io import SYMBOL_FILES, load_m1_trailing_calendar_days

DAY = "2026-01-21"
OUT = ARTIFACTS / "day12" / "method_should"
OUT.mkdir(parents=True, exist_ok=True)

# BGR
BG = (18, 18, 22)
WHITE = (235, 235, 235)
MUTED = (150, 150, 160)
GOLD = (40, 180, 220)
GREEN = (80, 200, 120)
RED = (80, 80, 220)
ORANGE = (40, 160, 255)
CYAN = (200, 200, 80)
BLUE = (220, 140, 60)
GRAY = (120, 120, 130)
YELLOW = (0, 200, 255)


def tsec(t: str) -> int:
    p = str(t).split(":")
    return int(p[0]) * 3600 + int(p[1]) * 60 + int(float(p[2]) if len(p) > 2 else 0)


def load_day_m1() -> List[dict]:
    path = Path(SYMBOL_FILES["XAUUSD"])
    bars = load_m1_trailing_calendar_days(path, n_days=400)
    day = [b for b in bars if str(b.get("date", "")) == DAY]
    # session window for the markup story ~07:00–12:00 UTC (matches prior exhibit)
    day = [b for b in day if "07:00:00" <= str(b.get("time", "00:00:00")) <= "12:00:00"]
    if len(day) < 50:
        # fall back full day
        day = [b for b in bars if str(b.get("date", "")) == DAY]
    return day


def resample_5m(m1: Sequence[dict]) -> List[dict]:
    """Simple 5m OHLC for cleaner day chart."""
    buckets: Dict[str, List[dict]] = {}
    for b in m1:
        t = str(b.get("time", "00:00:00"))
        hh, mm, *_ = t.split(":")
        m5 = (int(mm) // 5) * 5
        key = f"{hh}:{m5:02d}:00"
        buckets.setdefault(key, []).append(b)
    out = []
    for key in sorted(buckets.keys(), key=tsec):
        chunk = buckets[key]
        out.append(
            {
                "time": key,
                "open": float(chunk[0]["open"]),
                "high": max(float(x["high"]) for x in chunk),
                "low": min(float(x["low"]) for x in chunk),
                "close": float(chunk[-1]["close"]),
            }
        )
    return out


# Method script for day 12 ONLY — what SHOULD have happened
# Times/prices aligned to Court exhibit (same day path prices)
SHOULD_ZONES = [
    {
        "name": "FORCE",
        "t0": "07:00:00",
        "t1": "08:15:00",
        "color": BLUE,
        "label": "1 FORCE ON — permission LONG only. NO fire yet (wait for resume).",
    },
    {
        "name": "RESUME1",
        "t0": "08:15:00",
        "t1": "08:30:00",
        "color": GREEN,
        "label": "2 RESUME / LAUNCH — ONLY legal fire #1. Hold this idea.",
    },
    {
        "name": "NO_THRASH",
        "t0": "08:30:00",
        "t1": "08:45:00",
        "color": RED,
        "label": "3 DO NOT RE-FIRE (bot thrash zone) — method = FLAT / manage only.",
    },
    {
        "name": "PULLBACK_WAIT",
        "t0": "08:45:00",
        "t1": "09:15:00",
        "color": YELLOW,
        "label": "4 PULLBACK vs Force — WAIT. No dip-chase.",
    },
    {
        "name": "RESUME2",
        "t0": "09:15:00",
        "t1": "09:45:00",
        "color": CYAN,
        "label": "5 RESUME #2 — second legal fire only. Then hold / size under rails.",
    },
    {
        "name": "DONE_WAIT",
        "t0": "09:45:00",
        "t1": "12:00:00",
        "color": GRAY,
        "label": "6 NO MORE ENTRIES — wait next real cycle or size-down / flat. No metronome.",
    },
]

# Method-legal trades only (should-have book)
SHOULD_TRADES = [
    {
        "name": "FIRE #1 RESUME",
        "entry_t": "08:15:00",
        "exit_t": "08:30:00",
        "entry_px": 4871.58,
        "exit_px": 4883.92,
        "pnl": 1.086,
        "note": "HOLD winner — do not open thrash leg after",
        "color": GREEN,
    },
    {
        "name": "FIRE #2 RESUME",
        "entry_t": "09:15:00",
        "exit_t": "09:45:00",  # longer hold than bot's 15m spray
        "entry_px": 4837.19,
        "exit_px": 4855.0,  # hold through early resume leg, not micro re-entries
        "pnl": 0.85,
        "note": "One pullback-resume cycle — then STOP new fires",
        "color": CYAN,
    },
]

# Ghost (forbidden) — what bot did wrong, drawn dashed / red X
FORBIDDEN = [
    {
        "name": "THRASH (forbidden)",
        "entry_t": "08:30:00",
        "exit_t": "08:45:00",
        "entry_px": 4883.92,
        "exit_px": 4861.63,
        "pnl": -1.934,
    },
    {
        "name": "early densify (forbidden)",
        "t0": "07:00:00",
        "t1": "08:10:00",
        "note": "Bot fired many longs here — method = WAIT for resume",
    },
    {
        "name": "micro PB spray (forbidden)",
        "t0": "09:45:00",
        "t1": "11:00:00",
        "note": "Bot re-fired every few minutes — method = no more entries",
    },
]


def put(img, text, xy, scale=0.5, color=WHITE, thick=1):
    cv2.putText(
        img, text[:120], xy, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick, cv2.LINE_AA
    )


def draw_chart(bars: List[dict], w: int = 1400, h: int = 860) -> np.ndarray:
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = BG

    put(img, f"DAY 12 ONLY  |  {DAY}  XAUUSD  |  HOW THE METHOD SHOULD HAVE PLAYED", (20, 32), 0.7, GOLD, 2)
    put(
        img,
        "Method: FORCE on → WAIT pullback → FIRE on RESUME only → HOLD idea → NO thrash re-fire",
        (20, 58),
        0.5,
        CYAN,
        1,
    )
    put(
        img,
        "Green arrows = legal method trades only  |  Red dashed = forbidden (what bot did)",
        (20, 82),
        0.45,
        MUTED,
        1,
    )

    pad_l, pad_r, pad_t, pad_b = 70, 320, 110, 90
    cw, ch = w - pad_l - pad_r, h - pad_t - pad_b
    lo = min(float(b["low"]) for b in bars)
    hi = max(float(b["high"]) for b in bars)
    span = max(hi - lo, 1e-6)
    t0 = tsec(bars[0]["time"])
    t1 = tsec(bars[-1]["time"])
    tr = max(t1 - t0, 1)

    def x_of(t: str) -> int:
        return pad_l + int((tsec(t) - t0) / tr * cw)

    def y_of(p: float) -> int:
        return pad_t + int((hi - p) / span * ch)

    # zone backgrounds
    for z in SHOULD_ZONES:
        x0, x1 = x_of(z["t0"]), x_of(z["t1"])
        if x1 <= x0:
            x1 = x0 + 4
        overlay = img.copy()
        col = z["color"]
        cv2.rectangle(overlay, (x0, pad_t), (x1, pad_t + ch), col, -1)
        img = cv2.addWeighted(overlay, 0.18, img, 0.82, 0)
        # zone tag at top of pane
        put(img, z["name"], (x0 + 4, pad_t + 18), 0.4, col, 1)

    # candles
    n = len(bars)
    bw = max(2, cw // max(n, 1) - 1)
    for i, b in enumerate(bars):
        x = pad_l + int(i * cw / n)
        yo, yc = y_of(b["open"]), y_of(b["close"])
        yh, yl = y_of(b["high"]), y_of(b["low"])
        up = b["close"] >= b["open"]
        col = (90, 190, 120) if up else (90, 90, 200)
        cv2.line(img, (x + bw // 2, yh), (x + bw // 2, yl), col, 1)
        y1, y2 = min(yo, yc), max(yo, yc)
        if y2 <= y1:
            y2 = y1 + 1
        cv2.rectangle(img, (x, y1), (x + bw, y2), col, -1)

    # method legal trades
    for trd in SHOULD_TRADES:
        x0, x1 = x_of(trd["entry_t"]), x_of(trd["exit_t"])
        y0, y1 = y_of(trd["entry_px"]), y_of(trd["exit_px"])
        col = trd["color"]
        cv2.arrowedLine(img, (x0, y0), (x1, y1), col, 3, tipLength=0.08)
        cv2.circle(img, (x0, y0), 7, col, -1)
        cv2.circle(img, (x1, y1), 7, col, 2)
        put(
            img,
            f"{trd['name']}  +{trd['pnl']:.2f}%",
            (x0 + 8, y0 - 12),
            0.5,
            col,
            2,
        )
        put(img, trd["note"], (x0 + 8, y0 + 18), 0.38, MUTED, 1)

    # forbidden thrash leg
    thr = FORBIDDEN[0]
    x0, x1 = x_of(thr["entry_t"]), x_of(thr["exit_t"])
    y0, y1 = y_of(thr["entry_px"]), y_of(thr["exit_px"])
    # dashed feel via segments
    steps = 12
    for i in range(steps):
        if i % 2:
            continue
        a = i / steps
        b = (i + 1) / steps
        xa = int(x0 + (x1 - x0) * a)
        xb = int(x0 + (x1 - x0) * b)
        ya = int(y0 + (y1 - y0) * a)
        yb = int(y0 + (y1 - y0) * b)
        cv2.line(img, (xa, ya), (xb, yb), RED, 2)
    # X marks
    for px, py in ((x0, y0), (x1, y1)):
        cv2.line(img, (px - 8, py - 8), (px + 8, py + 8), RED, 2)
        cv2.line(img, (px - 8, py + 8), (px + 8, py - 8), RED, 2)
    put(img, "FORBIDDEN THRASH  -1.93%  (method = do not take)", (x1 - 20, y1 + 24), 0.45, RED, 1)

    # forbidden densify brackets
    for fb in FORBIDDEN[1:]:
        if "t0" not in fb:
            continue
        x0, x1 = x_of(fb["t0"]), x_of(fb["t1"])
        y = pad_t + ch - 24
        cv2.rectangle(img, (x0, y - 8), (x1, y + 8), RED, 1)
        put(img, fb["name"], (x0 + 4, y - 14), 0.35, RED, 1)

    # right rail story
    rx = w - pad_r + 12
    put(img, "SHOULD book", (rx, pad_t + 20), 0.55, GOLD, 2)
    put(img, "2 fires only", (rx, pad_t + 48), 0.5, GREEN, 1)
    put(img, f"~+{1.086 + 0.85:.1f}% method legs", (rx, pad_t + 72), 0.45, GREEN, 1)
    put(img, "(illustrative R)", (rx, pad_t + 94), 0.35, MUTED, 1)
    put(img, "NOT taken:", (rx, pad_t + 130), 0.5, RED, 1)
    put(img, "thrash -1.93%", (rx, pad_t + 154), 0.45, RED, 1)
    put(img, "early densify", (rx, pad_t + 178), 0.45, RED, 1)
    put(img, "micro PB spray", (rx, pad_t + 202), 0.45, RED, 1)
    put(img, "Sequence", (rx, pad_t + 250), 0.5, GOLD, 1)
    lines = [
        "1 Force on → wait",
        "2 Resume → fire #1",
        "3 Hold — no re-fire",
        "4 Pullback → wait",
        "5 Resume → fire #2",
        "6 Flat / wait cycle",
    ]
    y = pad_t + 280
    for ln in lines:
        put(img, ln, (rx, y), 0.4, WHITE, 1)
        y += 22

    # time axis labels
    for b in bars[:: max(1, len(bars) // 8)]:
        x = x_of(b["time"])
        put(img, b["time"][:5], (x - 10, pad_t + ch + 28), 0.35, MUTED, 1)

    put(
        img,
        "DAY 12 ONLY — method path (should). Not production champion behavior.",
        (20, h - 24),
        0.45,
        MUTED,
        1,
    )
    put(
        img,
        "Real M1→5m candles 2026-01-21  |  legal fires = 2  |  thrash crossed out",
        (20, h - 48),
        0.45,
        WHITE,
        1,
    )
    return img


def draw_compare_strip(w: int = 1400, h: int = 280) -> np.ndarray:
    """Side story: bot vs method — day 12 only."""
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = BG
    put(img, "DAY 12 ONLY — BOT vs METHOD (clear)", (20, 36), 0.7, GOLD, 2)

    # left bot
    cv2.rectangle(img, (30, 60), (680, 250), (40, 30, 50), 2)
    put(img, "WHAT BOT DID", (50, 90), 0.6, RED, 2)
    for i, ln in enumerate(
        [
            "Many longs 07:00→ all day (densify)",
            "Took LAUNCH +1.09% then THRASH -1.93%",
            "Sprayed pullback tags every few minutes",
            "Hold ~10–15m then re-enter same side",
            "Net ~+3% — missed 15% clear",
        ]
    ):
        put(img, "• " + ln, (50, 125 + i * 22), 0.45, WHITE, 1)

    # right method
    cv2.rectangle(img, (720, 60), (1370, 250), (30, 50, 35), 2)
    put(img, "WHAT METHOD SAYS", (740, 90), 0.6, GREEN, 2)
    for i, ln in enumerate(
        [
            "Wait until first real RESUME (~08:15)",
            "Fire #1 — HOLD — do not thrash after",
            "Wait full pullback (yellow) — no chase",
            "Fire #2 on resume only — then stop",
            "Two clean legs, not 50–90 thrash tickets",
        ]
    ):
        put(img, "• " + ln, (740, 125 + i * 22), 0.45, WHITE, 1)
    return img


def main() -> None:
    print("Loading", DAY, "only…")
    m1 = load_day_m1()
    if not m1:
        raise SystemExit(f"No bars for {DAY}")
    print("m1 bars", len(m1), "from", m1[0].get("time"), "to", m1[-1].get("time"))
    bars = resample_5m(m1)
    print("5m bars", len(bars))

    chart = draw_chart(bars)
    p1 = OUT / "day12_ONLY_method_should_play.png"
    cv2.imwrite(str(p1), chart)
    print("wrote", p1)

    strip = draw_compare_strip()
    p2 = OUT / "day12_ONLY_bot_vs_method.png"
    cv2.imwrite(str(p2), strip)
    print("wrote", p2)

    # stack
    # resize strip to chart width
    strip2 = cv2.resize(strip, (chart.shape[1], 280))
    stacked = np.vstack([chart, strip2])
    p3 = OUT / "day12_ONLY_method_full.png"
    cv2.imwrite(str(p3), stacked)
    print("wrote", p3)


if __name__ == "__main__":
    main()
