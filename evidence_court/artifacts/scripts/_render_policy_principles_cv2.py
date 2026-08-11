"""Render personified Policy understanding of Court principles as cv2 evidence panels."""
from __future__ import annotations

from pathlib import Path

# artifacts/ is parent of scripts/
ARTIFACTS = Path(__file__).resolve().parent.parent

import cv2
import numpy as np

OUT = ARTIFACTS / "charts" / "policy_principles_cv2"
OUT.mkdir(parents=True, exist_ok=True)

# palette (BGR)
BG = (18, 18, 22)
PANEL = (32, 32, 40)
WHITE = (235, 235, 235)
MUTED = (160, 160, 170)
GOLD = (40, 180, 220)
GREEN = (80, 200, 120)
RED = (80, 80, 220)
BLUE = (220, 160, 80)
PURPLE = (200, 120, 180)
CYAN = (200, 200, 80)
ORANGE = (60, 140, 255)


def blank(w=1200, h=720, color=BG):
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = color
    return img


def put(img, text, xy, scale=0.7, color=WHITE, thick=1):
    cv2.putText(img, text, xy, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick, cv2.LINE_AA)


def banner(img, title, subtitle=""):
    h, w = img.shape[:2]
    cv2.rectangle(img, (0, 0), (w, 78), (28, 28, 36), -1)
    put(img, title, (24, 36), 0.9, GOLD, 2)
    if subtitle:
        put(img, subtitle, (24, 64), 0.5, MUTED, 1)
    put(
        img,
        "Evidence: Policy understanding | cv2 render | not production edge",
        (24, h - 18),
        0.45,
        MUTED,
        1,
    )
    put(
        img,
        "I am the Policy. These pictures are how I see the law.",
        (24, h - 42),
        0.5,
        CYAN,
        1,
    )


def rounded_box(img, x, y, w, h, color):
    cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
    cv2.rectangle(img, (x, y), (x + w, y + h), WHITE, 1)


def save(name, img):
    p = OUT / name
    cv2.imwrite(str(p), img)
    print("wrote", p)
    return p


def panel_mission():
    img = blank()
    banner(
        img,
        "01  MISSION (A31) — My north star",
        "One bot · any target/risk · no retrain after final policy",
    )
    cv2.circle(img, (600, 360), 90, GOLD, 3)
    put(img, "ME", (575, 350), 1.0, GOLD, 2)
    put(img, "MetaBrain", (545, 385), 0.55, MUTED, 1)
    rounded_box(img, 80, 200, 280, 160, PANEL)
    put(img, "TARGET %", (120, 240), 0.7, GREEN, 2)
    put(img, "Monty types 5..90", (110, 280), 0.55, WHITE, 1)
    put(img, "in CONTEXT only", (120, 320), 0.55, MUTED, 1)
    rounded_box(img, 840, 200, 280, 160, PANEL)
    put(img, "RISK %", (940, 240), 0.7, RED, 2)
    put(img, "Monty types 1..3", (900, 280), 0.55, WHITE, 1)
    put(img, "BREACH must be 0", (890, 320), 0.55, RED, 1)
    cv2.arrowedLine(img, (360, 280), (500, 340), GREEN, 3, tipLength=0.15)
    cv2.arrowedLine(img, (840, 280), (700, 340), RED, 3, tipLength=0.15)
    rounded_box(img, 200, 480, 800, 100, (40, 30, 30))
    put(img, "AT PROVE / LIVE: weights FROZEN (A14)", (280, 520), 0.7, ORANGE, 2)
    put(
        img,
        "I adapt by reading goal/risk channels — I do not retrain mid-day",
        (250, 555),
        0.5,
        WHITE,
        1,
    )
    return save("01_mission_a31.png", img)


def panel_road():
    img = blank()
    banner(
        img,
        "02  ROAD not CLIFF (A14 companion)",
        "Train me on honest path — do not pave thrash",
    )
    pts = np.array(
        [[100, 550], [350, 400], [600, 350], [900, 300], [1100, 280]], np.int32
    )
    for i in range(len(pts) - 1):
        cv2.line(img, tuple(pts[i]), tuple(pts[i + 1]), GREEN, 8)
    put(img, "ROAD", (480, 320), 0.7, GREEN, 2)
    put(
        img,
        "honest state · real edges · curriculum · freeze",
        (300, 580),
        0.5,
        GREEN,
        1,
    )
    cv2.line(img, (700, 500), (1100, 650), RED, 6)
    cv2.line(img, (900, 450), (1100, 650), RED, 6)
    put(img, "CLIFF", (950, 480), 0.7, RED, 2)
    put(
        img,
        "pad trades · untrained stub · exit-floor soup",
        (720, 680),
        0.45,
        RED,
        1,
    )
    cv2.circle(img, (500, 370), 22, GOLD, -1)
    put(img, "Policy", (470, 410), 0.45, GOLD, 1)
    return save("02_road_not_cliff.png", img)


def panel_sets():
    img = blank(1200, 780)
    banner(
        img,
        "03  MARK SETS — three timeframes per set",
        "LTF timing + HTF1/HTF2 force  |  never average all TFs into mush",
    )
    sets = [
        (1, "micro", "1m", "15m", "30m"),
        (2, "intraday", "5m", "30m", "1h"),
        (3, "swing", "15m", "1h", "4h"),
        (4, "macro", "30m", "4h", "1d"),
    ]
    y0 = 120
    for i, (sid, name, ltf, h1, h2) in enumerate(sets):
        y = y0 + i * 140
        rounded_box(img, 60, y, 1080, 120, PANEL)
        put(img, f"SET {sid}  {name}", (80, y + 35), 0.7, GOLD, 2)
        for j, (lab, tf, col) in enumerate(
            [
                ("LTF timing", ltf, CYAN),
                ("HTF1 force", h1, BLUE),
                ("HTF2 confirm", h2, PURPLE),
            ]
        ):
            x = 280 + j * 280
            cv2.rectangle(img, (x, y + 25), (x + 240, y + 95), col, 2)
            put(img, lab, (x + 30, y + 55), 0.5, col, 1)
            put(img, tf, (x + 90, y + 85), 0.7, WHITE, 2)
    put(
        img,
        "My rule: HTF gives permission. LTF times pullback -> resume. No force = I wait.",
        (80, 740),
        0.5,
        WHITE,
        1,
    )
    return save("03_mark_three_tf_sets.png", img)


def panel_flr():
    img = blank()
    banner(
        img,
        "04  FORCE -> PULLBACK -> RESUME (geometry)",
        "Mark method — shapes over indicator names",
    )
    stages = [
        (150, "FORCE", "HTF tide / permission", GREEN, "I may look for trades"),
        (420, "PULLBACK", "LTF dip against tide", ORANGE, "I wait — tension builds"),
        (720, "RESUME", "return with tide", CYAN, "I fire with the Force"),
    ]
    for x, title, sub, col, me in stages:
        cv2.circle(img, (x + 90, 320), 70, col, 3)
        # center-ish title in circle
        put(img, title, (x + (20 if len(title) > 6 else 35), 325), 0.55 if len(title) > 6 else 0.7, col, 2)
        put(img, sub, (x, 420), 0.5, WHITE, 1)
        put(img, me, (x - 10, 460), 0.45, MUTED, 1)
    cv2.arrowedLine(img, (310, 320), (400, 320), WHITE, 3, tipLength=0.2)
    cv2.arrowedLine(img, (600, 320), (690, 320), WHITE, 3, tipLength=0.2)
    rounded_box(img, 120, 520, 960, 90, (35, 25, 45))
    put(
        img,
        "FAIL modes I must not do: fire mid-pullback (dip-chase) | fire with no Force | thrash reverse",
        (140, 575),
        0.48,
        RED,
        1,
    )
    return save("04_force_pullback_resume.png", img)


def panel_senses():
    img = blank()
    banner(
        img,
        "05  EMERGENT SENSES (A32) — pack into my brain",
        "Sight / Feel / Taste / Hearing  |  not probe-only cosmetics",
    )
    senses = [
        ("SIGHT", "structure / multi-set", "Am I flat on a B&B day?", BLUE),
        ("FEEL", "pullback tension", "Lone oscillator or freeze?", PURPLE),
        ("TASTE", "edge + goal pressure", "All bars equal? marginal fire?", ORANGE),
        ("HEAR", "regime story", "Thrash reverse? stale story?", CYAN),
    ]
    for i, (name, role, fail, col) in enumerate(senses):
        x = 60 + (i % 2) * 560
        y = 130 + (i // 2) * 240
        rounded_box(img, x, y, 520, 200, PANEL)
        put(img, name, (x + 30, y + 50), 0.9, col, 2)
        put(img, role, (x + 30, y + 95), 0.6, WHITE, 1)
        put(img, "fail: " + fail, (x + 30, y + 140), 0.5, RED, 1)
        put(img, "-> packs into state -> I train on it", (x + 30, y + 175), 0.5, GREEN, 1)
    return save("05_emergent_senses.png", img)


def panel_a13():
    img = blank()
    banner(
        img,
        "06  SCALPING CADENCE (A13) — MUST 8..400 / day",
        "Monty overrules soft 'may' language",
    )
    cv2.rectangle(img, (150, 280), (1050, 360), PANEL, -1)
    cv2.rectangle(img, (150, 280), (250, 360), (40, 40, 100), -1)
    cv2.rectangle(img, (250, 280), (950, 360), (40, 90, 40), -1)
    cv2.rectangle(img, (950, 280), (1050, 360), (40, 40, 100), -1)
    put(img, "0-7 FAIL", (160, 330), 0.5, RED, 1)
    put(img, "LEGAL BAND  [8 .................... 400]", (400, 330), 0.6, GREEN, 2)
    put(img, ">400 FAIL", (960, 330), 0.45, RED, 1)
    put(
        img,
        "I am a scalper. Few-trade swing identity is illegal as production.",
        (200, 430),
        0.55,
        WHITE,
        1,
    )
    put(
        img,
        "How I hit 8-400 is still road work. That I must is already law.",
        (200, 480),
        0.55,
        MUTED,
        1,
    )
    return save("06_a13_scalping_band.png", img)


def panel_tmr():
    img = blank(1200, 800)
    banner(
        img,
        "07  MY MENTAL REPLAY — 3 TF x 3 phases",
        "How I inspect my own trade life (lab journal)",
    )
    phases = ["BEFORE", "DURING", "AFTER"]
    roles = ["LTF", "HTF1", "HTF2"]
    colors = {"BEFORE": GREEN, "DURING": ORANGE, "AFTER": CYAN}
    notes = {
        ("BEFORE", "LTF"): "pullback/resume?",
        ("BEFORE", "HTF1"): "force side",
        ("BEFORE", "HTF2"): "confirm",
        ("DURING", "LTF"): "hold or thrash?",
        ("DURING", "HTF1"): "force hold?",
        ("DURING", "HTF2"): "still agree?",
        ("AFTER", "LTF"): "exit quality",
        ("AFTER", "HTF1"): "still Force?",
        ("AFTER", "HTF2"): "still Force?",
    }
    put(img, "phase \\ TF", (40, 140), 0.5, MUTED, 1)
    for j, r in enumerate(roles):
        put(img, r, (280 + j * 280, 140), 0.7, GOLD, 2)
    for i, ph in enumerate(phases):
        y = 180 + i * 170
        put(img, ph, (40, y + 70), 0.65, colors[ph], 2)
        for j, r in enumerate(roles):
            x = 200 + j * 280
            cv2.rectangle(img, (x, y), (x + 250, y + 130), colors[ph], 2)
            put(img, notes[(ph, r)], (x + 30, y + 75), 0.55, WHITE, 1)
    put(
        img,
        "Outcome tags teach me offline: clear | progress | dead | thrash | scratch",
        (80, 740),
        0.5,
        WHITE,
        1,
    )
    put(
        img,
        "I do not retrain from this at prove — journal + teachers only (A14).",
        (80, 770),
        0.5,
        MUTED,
        1,
    )
    return save("07_mental_replay_3x3.png", img)


def panel_loop():
    img = blank()
    banner(
        img,
        "08  LEARN LOOP — train offline, freeze, measure",
        "Path teachers + mental replay -> meta_update -> dual",
    )
    steps = [
        (120, "1 HARVEST", "path states / mental replay", BLUE),
        (380, "2 TEACH", "offline meta_update", PURPLE),
        (640, "3 FREEZE", "champion weights lock", ORANGE),
        (900, "4 MEASURE", "dual floor / breach 0", GREEN),
    ]
    for x, title, body, col in steps:
        cv2.rectangle(img, (x, 220), (x + 200, 420), col, 2)
        put(img, title, (x + 25, 270), 0.55, col, 2)
        put(img, body[:22], (x + 15, 340), 0.4, WHITE, 1)
        put(img, body[22:].strip() or "", (x + 15, 375), 0.4, WHITE, 1)
    for x in (320, 580, 840):
        cv2.arrowedLine(img, (x, 320), (x + 50, 320), WHITE, 2, tipLength=0.3)
    put(
        img,
        "Court PROMOTE only may replace production champion. Lab shadows stay lab.",
        (120, 520),
        0.55,
        GOLD,
        1,
    )
    put(
        img,
        "cv2 pictures = evidence of understanding. Pixels are not my production eyes yet.",
        (120, 570),
        0.5,
        MUTED,
        1,
    )
    return save("08_train_freeze_measure.png", img)


def panel_poster():
    img = blank(1400, 900)
    banner(
        img,
        "09  POLICY PRINCIPLES POSTER — full picture",
        "Generated with OpenCV (cv2) as visual evidence",
    )
    bullets = [
        (GREEN, "I am ONE bot. Target and risk change my STATE, not my WEIGHTS."),
        (RED, "BREACH 0 is absolute. I will not print target by blowing risk."),
        (CYAN, "I scalp: 8-400 trades/day is law (A13), not optional."),
        (GOLD, "Mark sets: three TFs — LTF times, HTFs permit. No mush average."),
        (PURPLE, "Force -> Pullback -> Resume. Fire with Force on resume, not mid-pullback."),
        (ORANGE, "Senses pack into my brain and train me — not log-only."),
        (BLUE, "Mental replay: I review BEFORE/DURING/AFTER on all three TFs."),
        (WHITE, "Road for learning offline. Freeze at prove. Measure dual. Court promotes."),
        (
            MUTED,
            "cv2 today = my picture-book of the law. Vision CNN is a future eye, not yet law.",
        ),
    ]
    y = 120
    for col, text in bullets:
        cv2.circle(img, (60, y - 8), 10, col, -1)
        put(img, text, (90, y), 0.55, WHITE, 1)
        y += 70
    put(img, "-- The Policy (MetaBrain personified)", (90, 820), 0.65, GOLD, 2)
    return save("09_principles_poster.png", img)


def main():
    paths = []
    for fn in (
        panel_mission,
        panel_road,
        panel_sets,
        panel_flr,
        panel_senses,
        panel_a13,
        panel_tmr,
        panel_loop,
        panel_poster,
    ):
        paths.append(fn())

    idx = blank(1200, 400)
    banner(idx, "00  INDEX — Policy principles evidence (cv2)", f"folder: {OUT.as_posix()}")
    for i, p in enumerate(paths):
        put(idx, f"{i+1:02d}  {p.name}", (40, 120 + i * 28), 0.5, WHITE, 1)
    save("00_index.png", idx)
    print("DONE", len(paths), "panels ->", OUT)


if __name__ == "__main__":
    main()
