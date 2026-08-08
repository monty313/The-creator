# OPPORTUNITY WATCH LAW — PERMANENT (Monty)

**Law id:** **A28**  
**Status:** PERMANENT  
**Human order:** Monty — always-on watch agent; senses are next cases; long-term performance  
**Not optional.**

Machine pin: `OPPORTUNITY_WATCH_LAW.json`  
Code: `meta_rl/opportunity_watch.py`  
Test: `tests/test_opportunity_watch_law.py`  
Docket: `SENSES_CASE_DOCKET.md`  
Auto-load: `AGENTS.md` · `.grok/rules/00_opportunity_watch.md`

---

## Standing rule

1. **One agent is always on:** the **Opportunity Watch Agent**.  
2. It watches whether the bot **misses** valid **pullback** and **continuation** opportunities defined by:
   - **HTF trending** (official set confirmation TFs agree / force clear), and  
   - **LTF timing** on the **lowest timeframe of that set** with **RSI(5) + BB(10, dev=0.5, shift=+2)**  
     (`pullback_resume` or `continuation` per Mark edge law A7).  
3. If a miss is detected → file a **complaint** (sense failure): *how should the bot sense this next time?*  
4. **Multiple complaints** may appear in **one Court case**.  
5. Session priority: **London / New York** has the most activity — miss complaints in that band are **highest weight** for long-term performance.  
6. Goal of the watch: **long-term performance** (more good trades + conversion under risk), not one-day luck.

---

## What counts as an opportunity (canonical)

| Field | Rule |
|-------|------|
| Sets | All four official Mark sets |
| HTF | Confirmation TFs trending / `htf_agree` + actionable force |
| LTF | Entry TF of the set only |
| Timing | RSI5 + BB10(0.5, shift+2) → `pullback_resume` or `continuation` |
| Act | long or short with HTF |
| Session hint | London–NY overlap / active band is **prime activity** |

**Miss:** opportunity exists at decision time **and** bot did **not** take a matching fire (wait / skip / wrong side / no trade).

---

## Complaints (permanent schema)

Each complaint:

```text
complaint_id
asof_date / asof_time
symbol
set_id / set_name
topology          # pullback_resume | continuation
side              # long | short
session_band      # london_ny | other
sense_gap         # sight | feel | taste | hearing | (combo)
what_bot_did      # wait | skipped | wrong_side | none
how_to_sense_next # concrete sense fix hypothesis for Court
```

Complaints feed **sense cases** (Sight / Feel / Taste / Hearing).  
They are **evidence of incomplete opportunity**, not proof the market is impossible (flea-jar).

---

## Senses docket (next cases — binding order)

| Case | Sense | Question (simple) |
|------|-------|-------------------|
| **CASE-0031** | **Sight + Watch Agent** | Detect and log misses; bot *sees* HTF+LTF PB/cont |
| **CASE-0032** | **Feel** | Sense load vs launch so fewer load-missed fires |
| **CASE-0033** | **Taste** | Sense edge quality + goal/risk so fires convert |
| **CASE-0034** | **Hearing** | Sense London/NY + day story so density lands in active session |

Each case may carry **multiple complaints** from the Watch Agent.  
Court still A10 + A15. Measure long-term (100d dual / A13), not vanity unit greens alone.

---

## Agent rules

| Rule | Detail |
|------|--------|
| Always on | Runs on day-path / forward eval when enabled; not optional decoration |
| No production override alone | Watch does not silently force trades; it **complains** → Court/policy sense fix |
| No pad | Complaints are real Mark-edge opportunities only (A7/A12) |
| Permanent | Cannot remove without Monty + PROMOTE superceding law |

---

## Immutable

Append-only permanent until later PROMOTE + Monty approval.  
Silent disable of Opportunity Watch is a Court defect.
