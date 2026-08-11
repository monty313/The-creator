# Fair showdown: PROVEN vs Court CASE-0037

**Date:** 2026-08-09  
**Question:** Which policy is best when we use the **same score language**?

---

## Score (same for both)

| Word | Meaning |
|------|---------|
| **Clear** | Day PnL ≥ **target** AND **no breach** |
| **Breach** | Loss hits the risk floor |
| **Green** | Day PnL > 0 |

---

## Engines (cannot mix weights)

| Side | Brain | How scored |
|------|--------|------------|
| **PROVEN** | `PROVEN_SPRINT_row04_clear24_2026-07-20` | the-truth `prove_it` · XAU · ~90 curriculum days |
| **Court** | `meta_policy_champion.npz` (CASE-0037) | goal_path MetaBrain · last **60** days |

**Caveat:** same *definition* of clear/breach — **not** the same bar engine. Still the fairest head-to-head we can run without rewriting both stacks.

---

## Results

### Primary shared pair (both legal): **5% target / 3% risk**

| Policy | Clear | Breach | Days |
|--------|------:|-------:|-----:|
| PROVEN | **10%** | 0% | 90 |
| Court XAU-only | **32%** | 0% | 60 |
| Court multi (XAU+EUR+GBP) | **33%** | 0% | 60 |

**Winner: COURT_0037** (+~22 clear points vs PROVEN)

### Harder pair: **15% target / 2% risk**

| Policy | Clear | Breach | Days |
|--------|------:|-------:|-----:|
| PROVEN | **0%** | 0% | 90 |
| Court XAU-only | **18%** | 0% | 60 |

**Winner: COURT_0037**

### Mark yardstick: **3% target / 3.5% risk** (PROVEN only)

| Policy | Clear | Breach | Days |
|--------|------:|-------:|-----:|
| PROVEN | **24%** | 0% | 90 |
| Court | *cannot run* | — | Court band is target **[5–90]** and risk **[1–3]** |

PROVEN still owns **its** classic yardstick. Court is not allowed those numbers by GOAL_LAW.

---

## Overall best

### **Winner: Court CASE-0037 champion**  
(`evidence_court/artifacts/meta_policy_champion.npz`)

**Why**

- On every pair **both** bots can run (**5/3** and **15/2**), Court **clears more days**.  
- **Breach 0** on both sides.  
- Closest apples = **XAU-only Court vs PROVEN XAU** → Court **32% vs 10%** clear at 5/3.

**Why not “PROVEN is dead”**

- At Mark’s famous **3.0 / 3.5**, PROVEN still posts **~24% clear**.  
- Court **cannot** take that exam under current Court law.  
- Engines differ (fill model, features, day windows).

---

## Simple picture

```text
Same score: clear% + breach 0

  5/3   →  Court wins (32–33% vs PROVEN 10%)
  15/2  →  Court wins (18% vs PROVEN 0%)
  3/3.5 →  PROVEN only (~24%) — Court not legal

OVERALL (shared legal tests):  COURT_0037
Mark yardstick museum piece:   PROVEN still best AT 3/3.5
```

---

## Files

| File | What |
|------|------|
| `fair_policy_showdown.json` | Machine report |
| `meta_rl/fair_policy_showdown.py` | Re-run harness |

```bash
python -m evidence_court.meta_rl.fair_policy_showdown --court-days 60
```

---

## One line

**Under the same clear/breach definition, on pairs Court is allowed to trade, CASE-0037 beats PROVEN. PROVEN remains best only on the old 3.0/3.5 Mark yardstick Court cannot enter.**
