# Improvements — before and after

**What we got from path-state teachers.**  
Numbers from CASE-0037.  
Simple words.

---

## Short version

We taught the bot on **real wait-misses**.

**Result:**

- Many more days with enough trades (A13)  
- Fewer silent days (zero trades)  
- Target wins stayed the same (not worse, not better)  
- Risk still safe (breach 0)  

So: **density got better.**  
**Clearing the target still needs more work.**

---

## When this happened

| Item | Value |
|------|--------|
| Court case | **CASE-0037** |
| Date | 2026-08-08 |
| Ruling | **PROMOTE_NARROW** |
| New champion steps | meta **4275** |
| Teachers used | **400** packed states |
| London / NY share | **362 / 400** |
| Train days harvested | about **30** |

---

## Before vs after (main table)

Same test style: seed **42**, **100** days, dual measure.

| Metric | BEFORE (old floor) | AFTER (path-state champ) | Change | Plain English |
|--------|-------------------:|-------------------------:|--------|---------------|
| **a13_frac** | 0.28 | **0.64** | **+0.36** | Share of days with 8–400 trades **more than doubled** |
| **n_zero** | 39 | **18** | **−21** | Silent days cut almost in half |
| **mean_tr** | 7.38 | **39.4** | **+32** | Average trades per day much higher |
| **hits** | 11 | **11** | 0 | Same number of target-win days |
| **low_hr** | 0.28 | **0.28** | held | Prefer floor held (good) |
| **max_pnl** | 70 | 70 | 0 | Best day pnl same |
| **breach** | 0 | **0** | held | Still no risk blow-up |
| **promote_ready** | false | false | — | Not final boss yet |

---

## Trade-day buckets (easy picture)

How many of the 100 days fell into each bucket:

### BEFORE

| Bucket | Days | Meaning |
|--------|-----:|---------|
| **0 trades** | 39 | Silent — too quiet |
| **1–7 trades** | 33 | Some activity, under A13 min 8 |
| **8–400 trades** | 28 | OK scalping band |
| **>400** | 0 | No thrash past cap |

### AFTER (path-state champion)

| Bucket | Days | Meaning |
|--------|-----:|---------|
| **0 trades** | **18** | Still some silent days (better) |
| **1–7 trades** | **18** | Still some thin days (better) |
| **8–400 trades** | **64** | Most days now in the scalping band |
| **>400** | 0 | Cap still respected |

### Picture in words

```text
BEFORE:  lots of quiet days · few dense days
AFTER:   quieter days cut · dense days dominate
```

---

## What improved the most

### #1 Density (biggest win)

**a13_frac 0.28 → 0.64**

Meaning:

- Before: only about **28%** of days hit 8–400 trades.  
- After: about **64%** of days hit that band.

That is the main success of path-state teachers.

### #2 Fewer silent days

**n_zero 39 → 18**

Meaning:

- Before: **39** days with zero trades.  
- After: **18** zero-trade days.

Still not zero silent days.  
But much better.

### #3 More average activity

**mean_tr 7.38 → 39.4**

The bot is active more often on the path.  
Not the same as “always smart.”  
But it is learning to fire on real wait-miss states.

---

## What did NOT improve (honest)

| Thing | Result | Why it matters |
|-------|--------|----------------|
| **hits (target clears)** | Still **11 / 100** | Bot still rarely fully hits the day target |
| **promote_ready** | Still **false** | Not ready as final mission win |
| **Every-day A13** | Not done | 18 zero + 18 partial days left |
| **High-target band** | Still weak | Harder goals still need work |

So we did **not** solve “make money / clear target every day.”  
We solved a big part of **“stop sitting out good Mark setups.”**

---

## Compare to failed experiments (why this won)

We tried other densify ideas first. They looked busy but failed Court.

| Approach | a13-ish | Silent days | Prefer floor | Verdict |
|----------|---------|-------------|--------------|---------|
| **F-024** synthetic densify | Up some | Got **worse** | Broke low_hr | **REJECT** |
| **F-025** real labels + fake rebuilt state | Up some | Got **worse** | Prefer break risk | **REJECT** |
| **Path-state teachers (0037)** | **0.28 → 0.64** | **39 → 18** | **Held** | **PROMOTE_NARROW** |

### Plain English

| Approach | Simple verdict |
|----------|----------------|
| Fake states | Bot thrashes; quiet days get worse |
| Rebuilt states | Teaches the wrong eyes |
| **Real wait states** | Bot learns real misses; density up; safety held |

---

## What the champion learned (skill, not buzzwords)

### Learned well

- When I **waited** on a **real** Mark pullback / continuation…  
- …and the **same kind of eyes** show up again…  
- …**fire Mark’s side** more often.  
- Care more about **London / New York** moments.

### Not learned enough yet

- Hold / size so the day **hits target** more often.  
- Trade well on **every** remaining quiet day.  
- Full high-trend mastery on **all four** official sets as one clean skill.

---

## Files that prove the improvement

| File | Role |
|------|------|
| `evidence_court/cases/CASE-0037-path-state-teachers.md` | Court case + numbers |
| `evidence_court/BEST_POLICY.md` | Production floor SSOT |
| `evidence_court/artifacts/forward100_report_case0037.json` | Full dual report |
| `evidence_court/artifacts/forward100_case0037_summary.json` | Short summary |
| `evidence_court/artifacts/meta_policy_champion.npz` | Current champ weights |
| `evidence_court/artifacts/meta_policy_champion_pre0037.npz` | Backup before promote |
| `evidence_court/artifacts/path_state_teachers_case0037.json` | Teacher pack used |

---

## Grade card (easy)

| Area | Grade | Notes |
|------|:-----:|-------|
| A13 density | **A−** | Big jump; not perfect every day |
| Silent days | **B+** | Cut hard; 18 left |
| Target hits | **C** | Flat at 11 |
| Risk / no retrain | **A** | breach 0; freeze held |
| Overall as “what taught the champ most” | **A** | Best proven lever so far |

---

## What to improve next (same good class)

Do **more of this class**, not the rejected class.

| Next idea | Same good class? |
|-----------|------------------|
| More path-state harvest on remaining zero / 1–7 days | **Yes** |
| Teachers with better size / hold toward target | **Yes** (careful measure) |
| High-trend pullback→resume teachers on all 4 sets | **Yes** (align with mastery gym) |
| Synthetic densify only | **No** |
| Rebuilt fake states | **No** |
| Live force-pad | **No** |

---

## One page memory aid

```text
BEFORE: quiet bot, few A13 days
PROCESS: save real wait + Mark answer → offline train
AFTER:  more A13 days, fewer silent days
SAME:   hits 11, breach 0
NEXT:   more path teachers + conversion (hits)
```

---

**You are done with this folder’s three core docs.**

- How it works → `01_HOW_IT_WORKS.md`  
- How to use it → `02_HOW_TO_USE_IT.md`  
- Improvements → this file  

Start page: `README.md`
