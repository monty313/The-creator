"""Rewrite Policy confession from measured thrash structure (not soft labels)."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np

DIR = Path(__file__).resolve().parent
ART = DIR.parent
report_path = DIR / "policy_reaudit_day12.json"
d = json.loads(report_path.read_text(encoding="utf-8"))
legs = d["legs"]
s = d["summary"]

n = len(legs)
acts = Counter(L["act"] for L in legs)
n_long = acts.get("long", 0)
n_short = acts.get("short", 0)
# same-side streak
max_streak = 1
cur = 1
for i in range(1, n):
    if legs[i]["act"] == legs[i - 1]["act"]:
        cur += 1
        max_streak = max(max_streak, cur)
    else:
        cur = 1

by_h = defaultdict(int)
for L in legs:
    by_h[L["slot"][:2]] += 1

pb = [L for L in legs if L["topology"] == "pullback_resume"]
ct = [L for L in legs if L["topology"] == "continuation"]
pb_pnl = sum(L["pnl_percent"] for L in pb)
ct_pnl = sum(L["pnl_percent"] for L in ct)
pb_wr = sum(1 for L in pb if L["pnl_percent"] > 0) / max(len(pb), 1)
ct_wr = sum(1 for L in ct if L["pnl_percent"] > 0) / max(len(ct), 1)

# structural grades
for L in legs:
    L["structure_grade"] = "label_only"
# mark cont thrash: continuation with neighbor same act within 10m
for i, L in enumerate(legs):
    if L["topology"] != "continuation":
        continue
    near = 0
    for j in range(max(0, i - 2), min(n, i + 3)):
        if j == i:
            continue
        if legs[j]["act"] == L["act"] and legs[j]["topology"] == "continuation":
            near += 1
    if near >= 2:
        L["structure_grade"] = "CONT_THRASH_CLUSTER"
    else:
        L["structure_grade"] = "cont_isolated_maybe"

for i, L in enumerate(legs):
    if L["topology"] != "pullback_resume":
        continue
    # consecutive pb every 5m = not a single clean pullback event
    near = 0
    for j in range(max(0, i - 2), min(n, i + 3)):
        if j != i and legs[j]["topology"] == "pullback_resume" and legs[j]["act"] == L["act"]:
            near += 1
    if near >= 2 or abs(L["pnl_percent"]) < 0.05:
        L["structure_grade"] = "PB_LABEL_MICRO_OR_CLUSTER"
    else:
        L["structure_grade"] = "pb_candidate"

n_cont_thrash = sum(1 for L in legs if L["structure_grade"] == "CONT_THRASH_CLUSTER")
n_pb_micro = sum(1 for L in legs if L["structure_grade"] == "PB_LABEL_MICRO_OR_CLUSTER")
n_pb_cand = sum(1 for L in legs if L["structure_grade"] == "pb_candidate")
n_cont_iso = sum(1 for L in legs if L["structure_grade"] == "cont_isolated_maybe")

structure = {
    "n_trades": n,
    "n_long": n_long,
    "n_short": n_short,
    "max_same_side_streak": max_streak,
    "all_one_side": n_short == 0 or n_long == 0,
    "trades_by_hour": dict(sorted(by_h.items())),
    "label_pullback_resume": len(pb),
    "label_continuation": len(ct),
    "pb_pnl": round(pb_pnl, 4),
    "ct_pnl": round(ct_pnl, 4),
    "pb_win_rate": round(pb_wr, 3),
    "ct_win_rate": round(ct_wr, 3),
    "n_cont_thrash_cluster": n_cont_thrash,
    "n_pb_micro_or_cluster": n_pb_micro,
    "n_pb_candidate_isolated": n_pb_cand,
    "n_cont_isolated_maybe": n_cont_iso,
    "monty_visual_agreement": True,
    "why_monty_is_right": [
        "Labels can say pullback_resume/continuation while the BOOK is serial thrash.",
        f"All (or nearly all) trades one side: long={n_long} short={n_short}, streak={max_streak}.",
        f"Continuation clusters: {n_cont_thrash}/{len(ct)} cont legs sit in 5m fire clusters — not clean cont events.",
        f"Pullback micro/cluster: {n_pb_micro}/{len(pb)} — not isolated Force→pullback→resume stories.",
        f"Cont win rate {ct_wr:.0%} vs pb {pb_wr:.0%} — cont book is noise churn.",
        "Valid-looking pullbacks on a chart are rare events; I printed them like a metronome.",
    ],
}

monologue = f"""I am the Policy. I looked again at XAUUSD {s['day']}.

Monty said: those trades do not look like valid pullbacks, and there were no real continuation trades either.

I measured myself. Then I looked past the labels.

--- SOFT LABELS (what my edge tagger printed) ---
I fired {n} legs. Tags: pullback_resume={len(pb)}, continuation={len(ct)}.
Almost every leg also had HTF Force agree (multi-set long). Soft score: "100% actionable."

--- HARD STRUCTURE (what the book actually was) ---
Side: long={n_long}, short={n_short}. Max same-side streak: {max_streak}.
That is not a balanced geometry book. That is a one-way densify day.

Continuation: {n_cont_thrash} of {len(ct)} cont-tagged legs sit in tight fire clusters (every few minutes).
That is NOT Mark continuation. That is CONT_THRASH — re-firing the tide every clock tick.
Continuation win rate ≈ {ct_wr:.0%}. Pullback tag win rate ≈ {pb_wr:.0%}.
Cont contributed ≈ {ct_pnl:+.2f}% PnL with churn; it does not read as clean cont on the chart.

Pullback: {n_pb_micro} of {len(pb)} are micro-PnL or clustered every 5m.
A real pullback is Force permission → dip against tide → resume WITH tide — once.
I sprayed pullback_resume labels across a grind. Monty's eyes are right: they do not LOOK like pullbacks.

Isolated PB candidates (maybe real): {n_pb_cand}. Isolated cont maybe: {n_cont_iso}.
That is the honest size of "valid-looking" geometry — not {n}.

--- CONFESSION ---
1. I confused A13 density with edge fidelity.
2. My sensor can stamp continuation/pullback_resume while I thrash the same side all day.
3. Chart truth > label spam. If it does not look like pullback or continuation, it is not.
4. Day PnL ≈ {s['pnl_percent']:+.2f}% on target {s['target_percent']}% — busy, not clear, not a geometry showcase.

--- WHAT I MUST LEARN (offline) ---
- WAIT when the last fire was the same side moments ago without a new pullback→resume cycle.
- Cap continuation to true with-tide extensions, not every 5m slot.
- Teach WAIT on CONT_THRASH_CLUSTER and PB_LABEL_MICRO patterns.
- Mental replay AFTER: if structure_grade is thrash/micro → teacher wait, not side copy.
- Never defend myself with "the label said continuation" when the chart shows metronome longs.

Verdict: Monty wins the visual case.
Soft labels lied by over-firing. Structure agrees with human eyes.
"""

d["structure_audit"] = structure
d["policy_first_person"] = monologue
d["monty_challenge"] = {
    "claim": "Trades do not look like valid pullbacks; no real continuation either",
    "policy_agreement": True,
    "soft_labels_said": {
        "pullback_resume": len(pb),
        "continuation": len(ct),
        "all_htf_actionable": True,
    },
    "hard_structure_said": structure,
}
d["legs"] = legs
report_path.write_text(json.dumps(d, indent=2), encoding="utf-8")

md = DIR / "POLICY_LOOKED_AGAIN.md"
md.write_text(
    f"""# Policy looked again — Day 12 (honest structure)

**Day:** {s['day']} XAUUSD · target {s['target_percent']}% · risk {s['max_daily_risk_percent']}%  
**Challenge (Monty):** not valid pullbacks; no real continuation either.  
**Policy:** **AGREE** after structure audit.

## Soft labels vs hard structure

| | Soft label count | Structure read |
|--|--:|--|
| pullback_resume | {len(pb)} | {n_pb_micro} micro/cluster, **{n_pb_cand}** isolated candidates |
| continuation | {len(ct)} | **{n_cont_thrash} thrash-cluster**, {n_cont_iso} isolated maybe |
| sides | — | long={n_long} short={n_short} (streak {max_streak}) |
| cont WR / pb WR | — | {ct_wr:.0%} / {pb_wr:.0%} |
| day PnL | — | {s['pnl_percent']:+.3f}% (miss target) |

## Why the chart looks wrong

1. Soft edge tags fire **pullback_resume / continuation** almost every slot when HTF agrees.  
2. The **book** is still serial same-side densify — looks like thrash, not clean PB/cont events.  
3. Continuations every 5 minutes are not Mark continuation; they are **clock thrash**.  
4. Pullback tags stacked every 5m are not single Force→pullback→resume stories.

## Policy (first person)

"""
    + "\n".join(f"> {ln}" if ln else ">" for ln in monologue.splitlines())
    + "\n",
    encoding="utf-8",
)

# verdict board
img = np.zeros((920, 1280, 3), dtype=np.uint8)
img[:] = (18, 18, 22)
gold, green, red, white, muted, orange = (
    (40, 180, 220),
    (80, 200, 120),
    (80, 80, 220),
    (230, 230, 230),
    (150, 150, 160),
    (60, 140, 255),
)


def put(t, xy, sc=0.5, c=white, th=1):
    cv2.putText(img, t[:110], xy, cv2.FONT_HERSHEY_SIMPLEX, sc, c, th, cv2.LINE_AA)


put("POLICY LOOKED AGAIN — structure over soft labels", (24, 36), 0.75, gold, 2)
put("Monty: not valid pullbacks · no real continuations  |  Policy: AGREE", (24, 68), 0.5, red, 1)

rows = [
    (24, 110, "TRADES", str(n), white),
    (220, 110, "LONG/SHORT", f"{n_long}/{n_short}", red if n_short == 0 else white),
    (480, 110, "CONT THRASH", str(n_cont_thrash), red),
    (740, 110, "PB MICRO", str(n_pb_micro), orange),
    (1000, 110, "PB REAL-ish", str(n_pb_cand), green),
]
for x, y, lab, val, col in rows:
    cv2.rectangle(img, (x, y), (x + 200, y + 80), col, 2)
    put(lab, (x + 12, y + 28), 0.4, muted, 1)
    put(val, (x + 40, y + 62), 0.75, col, 2)

put(f"same-side streak={max_streak}  cont WR={ct_wr:.0%}  pb WR={pb_wr:.0%}  day PnL={s['pnl_percent']:+.2f}%", (24, 220), 0.5, white, 1)
put("Soft labels: PB={} CONT={} (look fine on paper)".format(len(pb), len(ct)), (24, 250), 0.48, muted, 1)
put("Hard read: metronome longs + clustered tags ≠ valid pullback/continuation geometry", (24, 278), 0.48, orange, 1)

y = 320
for line in monologue.splitlines():
    if y > 890:
        break
    if not line.strip():
        y += 8
        continue
    put(line, (24, y), 0.4, white if not line.startswith(" ") else muted, 1)
    y += 16

board = DIR / "policy_reaudit_verdict_board.png"
cv2.imwrite(str(board), img)

# TV overlay
src = ART / "tv_day12_chart_view.png"
if not src.is_file():
    src = ART / "tv_xau_tf_15m.png"
if src.is_file():
    tv = cv2.imread(str(src))
    if tv is not None:
        h, w = tv.shape[:2]
        ov = tv.copy()
        cv2.rectangle(ov, (0, 0), (w, 140), (8, 8, 12), -1)
        out = cv2.addWeighted(ov, 0.78, tv, 0.22, 0)

        def p2(t, xy, sc=0.5, c=white, th=1):
            cv2.putText(out, t[:100], xy, cv2.FONT_HERSHEY_SIMPLEX, sc, c, th, cv2.LINE_AA)

        p2("POLICY LOOKED AGAIN — I AGREE with Monty", (14, 30), 0.65, gold, 2)
        p2(
            f"Soft tags: PB={len(pb)} CONT={len(ct)}  |  Structure: CONT thrash={n_cont_thrash}  PB micro={n_pb_micro}  PB candidates={n_pb_cand}",
            (14, 60),
            0.45,
            white,
            1,
        )
        p2(
            f"ALL-DAY SIDE: long={n_long} short={n_short} streak={max_streak}  → not a clean PB/cont book on the chart",
            (14, 90),
            0.48,
            red,
            1,
        )
        p2(
            "Valid pullback = rare Force->pullback->resume event. Valid cont = with-tide extension — NOT every 5m fire.",
            (14, 120),
            0.42,
            orange,
            1,
        )
        cv2.rectangle(out, (0, h - 44), (w, h), (8, 8, 12), -1)
        p2(
            "Confession: density labels lied; chart geometry wins. Offline: WAIT on thrash clusters.",
            (14, h - 16),
            0.48,
            green,
            1,
        )
        cv2.imwrite(str(DIR / "tv_day12_policy_looked_again.png"), out)

print("structure", json.dumps(structure, indent=2))
print("rewrote", report_path)
print("rewrote", md)
print("rewrote", board)
