# GOAL-RELATIVE COURT LAW — PERMANENT (Law A33)

**Status:** PERMANENT COURT LAW  
**Promoted:** 2026-08-07 as **Law A33** (Monty standing order)  
**Purpose:** Keep the **legal process running forever toward the goal**, generate **new issues relevant to achieving the goal**, retain denser evidence, and improve efficiency **without** weakening A10/A15 adversarial teeth.  
**Depends on:** A10, A15, A30, A31, A32  
**Machine pin:** `GOAL_RELATIVE_COURT_LAW.json` · test: `tests/test_goal_relative_court_law.py`

---

## 1. Foundation that never stops

The Evidence Court **is the operating system** of this project. It does not pause because docs look complete. It does not invent random side quests.

```text
scoreboard (measured)
    → goal_achieved? 
         YES → FINAL_BOT_SPEC / empty blocker docket
         NO  → Judge generates / refreshes issues from goal gaps (A31 axes)
              → rank biggest → smallest
              → Full Court (A10+A15) on rank-1 production blockers
              → verdict → ledger + scoreboard delta
              → loop
```

**This loop is permanent.** New measurements **must** be able to spawn new `ISSUE-*` / `C-*` / sense cases that are still **goal-relative**. Issues that no longer block any **G-*** axis are **closed** or demoted — they do not clutter the schedule.

---

## 2. Issue generation rules (binding)

After every case verdict and after every `forward100` / prove scoreboard:

1. Judge (or Court clerk under Judge order) lists **measured gaps** only.  
2. Each gap maps to ≥1 **A31 goal axis**.  
3. Rank by severity:  
   - **S0** breach / no-retrain violation / risk envelope broken  
   - **S1** dual conversion (clear % / hits / low_hr)  
   - **S2** A13 density  
   - **S3** senses not driving brain / Watch loop open  
   - **S4** L2L / train quality / multi-seed honesty  
   - **S5** polish / docs / non-blocking integrity  
4. **Only S0–S4** may open Full Court cases while any higher severity is open.  
5. Freestyle “interesting” ideas without an axis → **out of Court**.

### Required fields on every open issue / case

| Field | Required |
|-------|----------|
| `issue_id` / `item_id` | yes |
| `goal_axes` | yes (list of G-*) |
| `blocks_metric` | yes (e.g. hits, a13_frac, breach, sense_fail) |
| `severity` | S0–S5 |
| `evidence_pointers` | ledger event ids / artifact paths |
| `status` | open / in_court / closed / blocked |

---

## 3. Tiered Court (efficiency without soft teeth)

| Tier | When | Required |
|------|------|----------|
| **Full Court** | Changes production path, brain, A13, dual conversion, risk envelope, senses→brain, promote gates | Full A10 openings + counters + **A15 Counsel** + Critic + Optimist + Judge IRAC |
| **Summary Court** | Re-measure only, pin tests for already-PROMOTED laws, pure doc pins, Judge-ordered gap-fill measurement | Written claim, command, artifact SHA, Judge one-line ruling; **no** production behavior change without Full Court |

**Forbidden:** using Summary Court to smuggle production dials.

---

## 4. Evidence retention (must get denser over time)

### 4.1 Permanent Evidence Ledger (JSONL)

Path: `evidence_court/ledger/EVIDENCE_LEDGER.jsonl`  
**Append-only.** One JSON object per line for every material claim, test, metric, SHA, ruling.

Minimum schema:

```json
{
  "ts": "ISO-8601",
  "event_id": "EVT-YYYYMMDD-####",
  "case_id": "CASE-00xx|null",
  "issue_id": "C-00x|ISSUE-xxx",
  "goal_axes": ["G-CLEAR"],
  "kind": "claim|test|metric|ruling|scoreboard|counsel|artifact",
  "summary": "one line",
  "metric": {"name": "hits", "value": 11},
  "artifact_path": "evidence_court/artifacts/...",
  "artifact_sha256": "optional",
  "ruling": "PROMOTE|REJECT|ADMIT|INCONCLUSIVE|null",
  "refs": ["path/to/case.md"]
}
```

### 4.2 Precedent Cards

On case close, write `evidence_court/precedents/CASE-XXXX.card.md`:

- question  
- ruling  
- goal_axes  
- scoreboard delta  
- key evidence pointers (ledger event_ids)  
- **do_not_reargue_unless** (what new measurement would reopen)

Future sessions load cards + ledger **before** re-reading full case prose.

### 4.3 Living Scoreboard History

Path: `evidence_court/ledger/SCOREBOARD_HISTORY.jsonl`  
After every forward/prove:

```json
{
  "ts": "ISO-8601",
  "case_id": "CASE-0029",
  "hits": 11,
  "low_hr": 0.28,
  "a13_frac": 0.28,
  "breach": 0,
  "mean_tr": 7.27,
  "promote_ready": false,
  "seed": 42,
  "artifact_sha256": "..."
}
```

### 4.4 Counsel cache

Path: `evidence_court/ledger/COUNSEL_CACHE.jsonl`  
Store internet sift design-classes + sources so Counsel does not re-research from zero every case.

### 4.5 CONTINUATION_CHECKPOINT requirements (upgraded)

Must include: goal_achieved, top open docket (with goal_axes), last scoreboard row, pointers to ledger + latest cards, exact resume command.

---

## 5. How new issues are generated (examples — not exhaustive)

| Measured observation | Spawn issue axis | Example title |
|---------------------|------------------|---------------|
| Miss rate high on London PB/cont | G-SIGHT + G-A13 | Wire Watch misses into path |
| Fires on lone RSI | G-FEEL | Force-confirm feel gate in curriculum |
| High target hits≈0 | G-TASTE + G-CLEAR | Goal-pressure taste + high band train |
| Thrash after stop | G-HEAR | Day-story / tide-change hearing |
| a13_frac < 0.5 | G-A13 | Density without pad |
| hits flat multi-seed | G-CLEAR + G-LONG | Dual conversion multi-seed |
| Fingerprint changes on pair swap | G-NO_RETRAIN | Freeze train at prove |
| Two champion paths | G-ONEBOT | Single prove brain |

After PROMOTE, if metric still short of final boss, **spawn residual issue** at lower rank rather than declaring mission complete.

---

## 6. Relationship to A30 checklists

- Creator Phase 1 items **C-001…C-012** remain the primary queue.  
- A33 **requires** each C-* row to list `goal_axes`.  
- Sense cases 0031–0034 are **not optional side content** — they are the A32 path into **C-001 / C-005**.  
- Mark Phase 2 stays blocked until Phase 1 terminal.  
- When scoreboard improves, Judge may **insert** new residual issues between C-* items **if severity demands** (e.g. breach appears → S0 jumps to rank 1).

---

## 7. Efficiency rules for agents

1. Load: `GOAL_LAW` → scoreboard history tail → ISSUE_DOCKET → CONTINUATION_CHECKPOINT → relevant Precedent Cards.  
2. Do **not** re-litigate PROMOTED laws without new measurement.  
3. One Full Court case at a time on rank-1.  
4. Append ledger events in the same turn as verdicts.  
5. Keep generating goal-relative issues until final boss.

---

## Immutable

Append-only permanent. Supercede only by later PROMOTE + Monty approval.
