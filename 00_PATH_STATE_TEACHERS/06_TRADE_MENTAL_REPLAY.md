# Trade Mental Replay — Policy sees the full trade life

**Status:** lab wired (not production PROMOTE)  
**Code:** `evidence_court/meta_rl/trade_mental_replay.py`  
**Hook:** `run_goal_path_day(..., collect_mental_replay=True)`  
**Also on when:** `collect_path_state_teachers=True` (auto)

---

## Gap this closes

| Had | Gap | Now |
|-----|-----|-----|
| 176-d state at decision slots | No trade-lifecycle package | **BEFORE / DURING / AFTER** cards |
| Path teachers mostly **fire side** | No outcome story | **outcome_tag** + **teacher_hint** |
| Policy first-person only in arbitration docs | Not from real fills | **first_person** journal per trade |
| Mark HTF+LTF geometry | Not stored as 3-TF phase tape | **LTF + HTF1 + HTF2** per phase |

---

## The 3×3 mind (one official set)

```text
         LTF (timing)     HTF1 (force)     HTF2 (confirm)
BEFORE   pullback/resume  tide side        tide side
DURING   hold vs thrash   force hold?      still agree?
AFTER    exit quality     still Force?     still Force?
```

Sets (MARK_SETS_LAW):

| Set | LTF | HTF1 | HTF2 |
|----:|-----|------|------|
| 1 | 1m | 15m | 30m |
| 2 | 5m | 30m | 1h |
| 3 | 15m | 1h | 4h |
| 4 | 30m | 4h | 1d |

---

## How to turn it on

```python
fills, ledger, meta = run_goal_path_day(
    policy,
    date=day,
    m1_by_symbol=m1,
    target_percent=15.0,
    max_daily_risk_percent=2.0,
    symbols=["XAUUSD"],
    collect_mental_replay=True,          # journal cards
    # or collect_path_state_teachers=True  # journal + offline teachers
)
cards = meta["mental_replays"]           # compact dicts (no full state)
print(cards[0]["first_person"])
```

Save pack:

```python
from evidence_court.meta_rl.trade_mental_replay import save_mental_replay_pack
save_mental_replay_pack(cards, "evidence_court/artifacts/mental_replay_day.json")
```

Annotate a chart screenshot (cv2 — evidence only, not the edge engine):

```python
from evidence_court.meta_rl.trade_mental_replay import annotate_chart_png
annotate_chart_png("chart.png", cards[0], "chart_tmr.png")
```

---

## Offline teachers (A14 safe)

From BEFORE packed state + AFTER outcome:

| Source | When | Teacher |
|--------|------|---------|
| `path_state_mental_replay` | good/normal fire | side long/short |
| `path_state_mental_replay_clear` | clear progress | side |
| `path_state_mental_replay_hold` | green but thin + force still with | side (hold lesson) |
| `path_state_mental_replay_dead` | dead/thrash loss | **wait** |

Filter: `filter_path_state_teachers(..., allow_wait=True)` for dead lessons.

**Never** at prove/inference. Offline `meta_update` only.

---

## Policy first person (example)

```text
I fired long on XAUUSD set1(micro: 1m/15m/30m) as continuation.
BEFORE: LTF continuation rsi=55; HTF force=+0.40 agree=Y multi=agree_long.
DURING: LTF continuation rsi=54; HTF force=+0.38 agree=Y multi=agree_long.
AFTER:  LTF chop rsi=50; HTF force=+0.20 agree=Y multi=incomplete.
Result pnl=+0.250% → outcome=progress; I should learn: hold_more.
```

---

## Law notes

- No look-ahead past phase asof times (CASE-0004 completed HTF).
- Does not change production champion until Court PROMOTE.
- cv2 is for **HUD annotate / evidence**, not senses-drive.
