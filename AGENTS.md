# AGENTS.md — The Creator (Evidence Court) — auto-loaded

> **AUTO-LOADED by Grok Build** when the session root is this folder.  
> Permanent project instructions. Do not invent a softer Court.

**Owner:** Monty  
**Mission SSOT (lab goal):** `mark_here/knowledge/lab/GOAL.md` + Court **`evidence_court/GOAL_LAW.md` (A31)** — one bot, any target/risk, **no retrain after final policy**, breach **0**, scalping **8–400/day**, **emergent senses drive the brain**.  
**Court procedure SSOT:** `grok_cli_evidence_court_v2.md` + **`GOAL_RELATIVE_COURT_LAW.md` (A33)**  
**Promoted laws:** `evidence_court/MASTER_ARCHITECTURE.md`  
**Best / production policy SSOT:** `evidence_court/BEST_POLICY.md`  
**Live docket:** `evidence_court/ISSUE_DOCKET.md` · checkpoint: `evidence_court/CONTINUATION_CHECKPOINT.md`

---

## PERMANENT — Law A31: Goal is the north star of every Court action

**Canonical:** `evidence_court/GOAL_LAW.md` + `.json`  
**Pin:** `pytest evidence_court/tests/test_goal_law.py -q`  
**Auto-load:** `.grok/rules/00_goal_law.md`

| THE LAW | Forbidden |
|---------|-----------|
| Every case/issue declares **goal_axes** (G-*) | Freestyle cases with no goal map |
| Docket ranked by **measured goal gaps** | Side quests while blockers open |
| After every verdict: re-measure → **regenerate** issues | Stopping Court because “docs look done” |
| Final boss = dual + A13 + no-retrain + senses-drive + multi-seed | Calling mission complete with open G-* blockers |

---

## PERMANENT — Law A32: Emergent senses (sight / feel / taste / hearing)

**Canonical:** `evidence_court/EMERGENT_SENSES_LAW.md` + `.json`  
**Docket:** `SENSES_CASE_DOCKET.md` (CASE-0031…0034)  
**Pin:** `pytest evidence_court/tests/test_emergent_senses_law.py -q`  
**Auto-load:** `.grok/rules/00_emergent_senses.md`

| THE LAW | Forbidden |
|---------|-----------|
| Senses on **every official MARK set** | Averaging all TFs as “force” |
| Relative to **edge/reasoning**, not indicator names | Folklore RSI-only “senses” |
| Outputs **pack into state and train the brain** | Probe-only / log-only senses on production path |
| Fail modes unit/Watch-testable | Ignoring flat B&B days as “no edge” |

**Fail modes (must kill):**  
Sight — flat on bread-and-butter pullback day.  
Feel — lone oscillator fire or freeze on load.  
Taste — all bars equal or marginal fires on high-target days.  
Hearing — thrash-reverse without tide change or stale story into regime shift.

---

## PERMANENT — Law A33: Goal-relative Court keeps going + retains evidence

**Canonical:** `evidence_court/GOAL_RELATIVE_COURT_LAW.md` + `.json`  
**Pin:** `pytest evidence_court/tests/test_goal_relative_court_law.py -q`  
**Auto-load:** `.grok/rules/00_goal_relative_court.md`

| THE LAW | Forbidden |
|---------|-----------|
| Continuous loop until final boss | “Wait for user to open next case” |
| **Generate new issues** from measurements on G-* axes | Clutter docket with non-blocking polish first |
| **Full Court** for production/brain/A13/dual/senses/promote | Summary Court smuggling behavior changes |
| Append **EVIDENCE_LEDGER** + scoreboard history | Rulings with no durable machine record |

**Retention paths:**  
`ledger/EVIDENCE_LEDGER.jsonl` · `ledger/SCOREBOARD_HISTORY.jsonl` · `ledger/COUNSEL_CACHE.jsonl` · `precedents/`

---

## PERMANENT — Law A14: Meta-policy must be trained (not “practice”)

**Canonical:** `evidence_court/META_POLICY_TRAIN_LAW.md`  
**Code:** `evidence_court/meta_rl/policy.py` · CLI `meta-train`  
**Pin tests:** `tests/test_meta_policy_train.py`, `tests/test_goal_risk_no_retrain.py`

| THE LAW | Forbidden |
|---------|-----------|
| Policy **must be meta-trained** before prove/forward | Untrained seed stub as production brain |
| Meta-learning is **permanent** architecture | Calling it optional “practice only” |
| Same trained weights adapt to targets via **goal/risk context** | Retrain weights every time Monty changes target/risk |
| Offline `meta_update` / `meta-train` improves the map | `train_step` during frozen inference / prove |

**No-retrain** = no weight updates **at inference** when target/risk changes.  
**Not** “never train.”

---

## PERMANENT — Law A13: Scalping cadence (**Monty overrules Judge**)

**Canonical:** `evidence_court/SCALPING_CADENCE_LAW.md` + `.json`  
**Pin test:** `pytest evidence_court/tests/test_scalping_cadence_law.py -q`  
**Auto-load:** `.grok/rules/00_scalping_cadence.md`

This bot is a **scalping bot**. It **MUST take between 8 and 400 trades every day**.

| THE LAW | Forbidden |
|---------|-----------|
| **MUST** land **[8, 400]** trades/day (inclusive) | Soft “may” / optional capacity language |
| Scalper under risk envelope; breach **0**; no retrain | Few-trades swing as production identity |
| Owner overrule stands above Judge preference | PROMOTE path that cannot hit min **8** |
| Cap **400** hard (no thrash past ceiling) | Treating 5-slot path as A13-compliant |

**How** the bot hits 8–400 still needs measured A10 work.  
**That it must** is already law — Judge does not get to soften or defer the mandate.

---

## PERMANENT — Law A30: Full-project checklist schedule (Monty)

**Canonical:** `evidence_court/FULL_PROJECT_CHECKLIST_LAW.md` + `.json`  
**Schedule:** `evidence_court/schedules/SCHEDULE.md`  
**Creator checklist:** `schedules/CREATOR_GOAL_CHECKLIST.md` (each row has **goal_axes**)  
**Mark checklist:** `schedules/MARK_GOAL_CHECKLIST.md` (after Creator done)  
**Pin:** `pytest evidence_court/tests/test_full_project_checklist_law.py -q`  
**Auto-load:** `.grok/rules/00_full_project_checklist.md`

| Phase | Who | What |
|------:|-----|------|
| **1** | **Creator** | Whole project → checklist of what must happen for GOAL |
| | | **Each item → full Court (A10+A15)** |
| **2** | **Mark** | Whole project **+ KAG** → his checklist |
| | | **Each item → full Court** (only after Phase 1 complete) |

Forbidden: skip Court on an item; start Mark before Creator complete.

---

## PERMANENT — Law A29: Real brain + L2L + serious train (Monty — no Judge delay)

**Canonical:** `evidence_court/BRAIN_L2L_LAW.md`  
**Code:** `meta_rl/brain.py` · `policy.py` · `goal_path` `brain_drives=True`  
**CLI:** `python -m evidence_court.meta_rl.cli meta-train --steps 8000`

| THE LAW | Forbidden |
|---------|-----------|
| **Trained multi-layer meta-brain** decides fire/size | Hard-rule soup as the decider |
| **Learn-to-learn** (transfer roles / renames) | Untrained stub / thin linear prior as “policy” |
| Sensors feed **state**; brain chooses | Shipping without serious curriculum |
| **London/NY ≥8 trades capacity** — no “no opportunity” excuse | Excusing flat London/NY as nature |
| No retrain when target/risk changes at prove | Full retrain every pair |

---

## PERMANENT — Law A28: Opportunity Watch Agent + senses docket (Monty)

**Canonical:** `evidence_court/OPPORTUNITY_WATCH_LAW.md` + `.json`  
**Code:** `evidence_court/meta_rl/opportunity_watch.py`  
**Docket:** `evidence_court/SENSES_CASE_DOCKET.md`  
**Pin:** `pytest evidence_court/tests/test_opportunity_watch_law.py -q`  
**Auto-load:** `.grok/rules/00_opportunity_watch.md`

**Always-on agent** watches for **missed** pullback / continuation when HTF is trending and LTF prints Mark **RSI(5)+BB(10,0.5,shift+2)** timing.  
On miss → **complaint** (`how_to_sense_next`). **Many complaints per case OK.**  
**London/NY** = most activity — highest weight. **Long-term performance.**

**Next cases (binding):**  
**CASE-0031 Sight** → **0032 Feel** → **0033 Taste** → **0034 Hearing** (maps C-001 / C-005)

---

## PERMANENT — Law A15: Counsel to the Court (Monty)

**Canonical:** `evidence_court/COUNSEL_TO_THE_COURT_LAW.md` + `.json`  
**Pin test:** `pytest evidence_court/tests/test_counsel_to_the_court_law.py -q`  
**Auto-load:** `.grok/rules/00_counsel.md` · short sheet `evidence_court/COUNSEL.md`

**Counsel** helps the **Judge deliberate**. Job: **sift the internet** for the **best possible policy** and file **one opinion** per case (no production code).  
Use `ledger/COUNSEL_CACHE.jsonl` so sifts accumulate (A33).

Judge **must** view **all three opinions + evidence** before ruling:

| # | Opinion | Source |
|---|---------|--------|
| 1 | **Creator** | Internet + new tests (A10) |
| 2 | **Mark** | Knowledge + new tests (A10) |
| 3 | **Counsel** | Internet sift → best policy recommendation + sources/evidence |

Sequence: openings → counters → **Counsel** → Critic → Optimist → Judge IRAC (must name all three).  
PROMOTE without three-opinion deliberation → **Forbidden**.

---

## PERMANENT — Law A10: Adversarial Rounds

**Canonical:** `evidence_court/ADVERSARIAL_ROUNDS_LAW.md` + `.json`  
**Pin test:** `pytest evidence_court/tests/test_adversarial_rounds_law.py -q`

Every Evidence Court case **must**:

1. **Creator opening** — strongest argument from the **internet** + **new test**.  
2. **Mark opening** — strongest argument from **his knowledge** + **new test**.  
3. **One counter each** — one counter-argument + one **newer** test (or waive).  
4. **No second counter.** Judge strikes further party replies.  
5. **Counsel opinion (A15)** — internet sift for best policy + evidence.  
6. Critic → Optimist → Judge IRAC (**three opinions** weighed).

| Forbidden as proof | Required as proof |
|--------------------|-------------------|
| Old suite greens, prior KAG alone, mentor rank | New test / newer test for **this** claim |
| Placeholder soft openings | Strongest real argument from each side’s source |

**Roles:** Creator codes after Judge order / PROMOTE only. Mark and Counsel do **not** write production code.  
**Also permanent:** Flea-jar, MARK_SETS_LAW, A13 scalping, A14 meta-train, A15 Counsel, A31–A33 goal process, no silent PROVEN overwrite.

---

## Also load

- `.grok/rules/00_adversarial_rounds.md`  
- `.grok/rules/00_counsel.md`  
- `.grok/rules/00_opportunity_watch.md`  
- `.grok/rules/00_full_project_checklist.md`  
- `.grok/rules/00_court_mission.md`  
- `.grok/rules/00_scalping_cadence.md`  
- `.grok/rules/00_goal_law.md`  
- `.grok/rules/00_emergent_senses.md`  
- `.grok/rules/00_goal_relative_court.md`  
- `mark_here/ESQUIRE.md` when Mark speaks  
- `evidence_court/COUNSEL.md` when Counsel speaks  
- `evidence_court/README.md` for commands  

If a session skips A10 openings/counters on Full Court, that session is **out of Court** — stop and reopen under the law.

---

## PERMANENT — Court before major decisions (Monty order)

**Every major decision** (edge rule, sizing rule, fill model, promote gate, senses→brain wiring, new module behavior) **must go through Evidence Court A10 + A15** before it is treated as production law.

**Forbidden:** inventing dials/path changes mid-session and calling them “done” without case file + new tests + measurement + **ledger event**.  
**Allowed without full case (Summary Court A33):** typo fixes, test pins for already-PROMOTED laws, inventory reads, running existing CLI evals.  
**If code landed without Court:** quarantine as experimental; open/reopen a case; prove or strip.

---

## PERMANENT — Goal → Issue docket → Court cycle (biggest first)

From `grok_cli_evidence_court_v2.md` §9 + **A33**:

1. If **/goal is not achieved** (measured scoreboard) → **Judge identifies issues** on **G-* axes**.  
2. Issues go on **`evidence_court/ISSUE_DOCKET.md`**, ranked **biggest → smallest**, each with `goal_axes`.  
3. Court tries **rank-1 first**, then smaller issues.  
4. After each verdict → re-check goal → **regenerate** docket (close non-blockers, spawn new residuals) → next case on new #1.  
5. **No freestyle cases** for lower-ranked issues while a larger blocker is open.  
6. **Keep going** — generate new goal-relevant issues until final boss.

That **is** the cycle until final boss + empty blocker docket.

---

## PERMANENT — Road for the trained policy (not a cliff)

**A14:** weights come from **meta-train**. Your job is to make the policy’s job **easy**.

> Build a **road** for it to drive on. Do **not** pave a road off a **cliff**.

| Road | Cliff |
|------|--------|
| Honest state + goal/risk context | Untrained stub as “the bot” |
| Trainable curriculum, champion load | Handcraft thrash that can’t be learned |
| Risk envelope as rails | Exit floors that scratch all R |
| Real edges at A13 density | Pad trades / full-size multi thrash |
| Senses → state → brain | Probe-only cosmetics |
| Court measures + ledger | Invented dials |

Canonical: `evidence_court/ROAD_FOR_THE_POLICY.md` · docket rank-1 **C-001 / CASE-0031**.
