# L2L PROJECT — ONE BOT, 100 DAYS

**Status:** Court instruction document for Grok CLI  
**Owner:** Monty  
**Date:** 2026-08-09  
**Repo:** monty313/The-creator  

---

## 1. Mission (North Star)

Build **one** frozen-weight scalping bot that can do all of the following on a 100-day forward test:

- Hit a **random** daily target drawn from [5, 90]
- Stay inside a **random** risk floor drawn from [1, 3]
- Keep **breach = 0** on every measured day
- Land **8–400 trades** every single day (Law A13)
- Fire **both pullbacks and continuations**
- Never retrain the weights after the final policy is locked (target and risk change only through the state)

This is the only scoreboard that matters.  
Every proposal below is judged only by how it moves the bot closer to (or away from) this 100-day result.

---

## 2. Learn-to-Learn Principle (non-negotiable)

The bot must **learn how to learn**.  
We never hand it the final answer.

- Do **not** give it ready-made “this is a pullback → fire” labels as the final decision.
- Do **not** hard-code the trade.
- Do **not** retrain weights at inference when the target or risk changes.

Instead we:

- Give the bot living senses (Sight, Feel, Taste, Hearing)
- Pack those senses into the state so they actually drive the MetaBrain
- Reward the **process** of good reasoning with the senses
- Let the frozen brain invent its own method on unseen days and new target/risk pairs

This is process supervision + learn-to-learn.  
If a proposal just copies answers or freezes a hard-rule path, the Court **rejects** it.

---

## 3. Court Rules — How to Accept or Reject Every Proposal

The Court (Creator + Mark + Counsel + Judge) must apply these rules to every proposal.

### Accept only when ALL of the following are true

1. The change moves the bot closer to the 100-day north-star scoreboard (or at least does not move it farther away).
2. The change does **not** give the bot the final answer. It only improves the process, the senses, or the state the brain sees.
3. After the change the weights can still be frozen. Target and risk still change only through context.
4. Breach stays 0 (or the proposal has a clear path to keep it 0).
5. Both pullbacks **and** continuations remain possible (no proposal may kill one of them).
6. The senses (or the new state channels) actually change decisions. They are not probe-only decorations.
7. A unit test or measured forward result proves the claim.

### Reject immediately when any of the following is true

- The proposal hands the bot a finished trade decision or a hard if-rule that replaces the brain.
- The proposal requires retraining weights at inference when target or risk changes.
- The proposal is only “logging” or “probe” work that never reaches the trained state or the MetaBrain.
- The proposal improves one edge type (pullback or continuation) while destroying the other.
- The proposal cannot show a measured path to the 100-day scoreboard.
- The proposal increases breach risk with no compensating control.

### Court process for each proposal

1. Creator opens with the strongest technical argument and a concrete test.
2. Mark opens with the strongest knowledge argument and a concrete test.
3. Each side may give **one** counter + newer test (or waive).
4. Counsel sifts for the best possible policy and gives one opinion.
5. Critic and Optimist speak once each.
6. Judge issues IRAC and rules **ACCEPT** or **REJECT**.
7. Accepted proposals are recorded in the Evidence Ledger and the scoreboard is re-measured.
8. Rejected proposals are closed with the reason and cannot be re-opened without new evidence.

---

## 4. What the Bot Must Honestly See (state ingredients)

These pieces must be present and honest in every state the brain sees:

- Honest target + risk + progress + room
- The 4 official Mark sets: force + LTF timing + pullback
- Regime / load vs launch
- Position heat
- Session
- Senses that actually change decisions

If any of these are missing, fake, or ignored by the brain, the Court treats the current policy as incomplete.

---

## 5. Core Skills the Bot Must Learn

1. See structure (force + timing)
2. Fire enough good edges — **both pullbacks and continuations**
3. Size for that target under that risk
4. Stop when room is gone
5. Still clear the day

Every accepted proposal must help at least one of these skills without harming the others.

---

## 6. Ordered Proposals (Court will vote Accept / Reject on each)

Work in this order. Do not skip ahead.

### Proposal 1 — Senses reach the brain and change decisions
**Goal axis:** G-SIGHT, G-FEEL, G-TASTE, G-HEAR, G-L2L  
**Work:**  
- Encode the four sense reports into a fixed numeric vector.  
- Pack that vector into the Meta-RL state the brain trains and infers on.  
- Prove with a unit test that changing only a sense value changes the brain’s action or logits.  

**Accept when:** senses are no longer probe-only decorations and the brain reacts to them.  
**Reject when:** senses are still only logged or the dim change breaks the frozen-weight contract.

### Proposal 2 — Sight becomes alive on structure (force + timing)
**Goal axis:** G-SIGHT  
**Work:** Reward good structure reading on the 4 Mark sets for both pullbacks and continuations. Never hand the final trade label.  
**Accept when:** bot no longer goes flat on ordinary bread-and-butter pullback or continuation days.  
**Reject when:** Sight is still a static probe or only works on pre-selected days.

### Proposal 3 — Feel becomes alive (load vs launch)
**Goal axis:** G-FEEL  
**Work:** Reward only when the feeling of tension / load leads to useful waiting or useful firing.  
**Accept when:** no lone-oscillator fires and no freezing when load is building.  
**Reject when:** Feel is still ignored by the brain or produces thrash.

### Proposal 4 — Taste becomes alive under goal/risk pressure
**Goal axis:** G-TASTE, G-CLEAR  
**Work:** Reward the bot’s own judgment of edge quality under the honest target, risk, progress and room.  
**Accept when:** high-target days only take high-quality edges (both pullback and continuation).  
**Reject when:** every bar is still treated as equal or marginal edges are fired on hard targets.

### Proposal 5 — Hearing becomes alive (regime / day-story / wait)
**Goal axis:** G-HEAR, G-A13  
**Work:** Reward useful regime, load-vs-launch, session and day-story reading.  
**Accept when:** no thrash-reverses without a real tide change and no stale stories after a regime shift.  
**Reject when:** Hearing is still a static label or wait is just silence.

### Proposal 6 — MetaBrain reasons step-by-step with the senses
**Goal axis:** G-L2L, G-CLEAR  
**Work:** Reward the intermediate reasoning steps that use the four senses + the honest state pieces. Never reward only the final P&L.  
**Accept when:** clear step-by-step reasoning appears before decisions and improves the 100-day path.  
**Reject when:** the brain is still only pattern-matching or copying teacher labels.

### Proposal 7 — Learn-to-learn on unseen days and new target/risk pairs
**Goal axis:** G-L2L, G-NO_RETRAIN  
**Work:** Curriculum that forces the bot to invent methods on days and target/risk pairs it has never seen.  
**Accept when:** the same frozen weights still produce useful behaviour on brand-new data.  
**Reject when:** performance collapses the moment the day or the target/risk pair is novel.

### Proposal 8 — Lock the weights (context-only adaptation)
**Goal axis:** G-NO_RETRAIN  
**Work:** Freeze the final policy. From this moment only the target and risk numbers in the state may change.  
**Accept when:** fingerprint is stable across any target×risk pair and no `meta_update` is called at inference.  
**Reject when:** any weight is still updated at prove or forward time.

### Proposal 9 — Breach stays 0 (stop when room is gone)
**Goal axis:** G-BREACH0  
**Work:** Reward the process that keeps position heat and daily risk inside the floor before any breach can occur.  
**Accept when:** every measured scoreboard (including the 100-day run) shows breach = 0.  
**Reject when:** breach appears on any held-out day.

### Proposal 10 — 8–400 trades every day and clear the random target
**Goal axis:** G-A13, G-CLEAR  
**Work:** Reward the process that naturally produces enough good pullbacks **and** continuations so the day clears. Never force a fixed trade count.  
**Accept when:** on a 100-day random-target×risk forward test the bot lands 8–400 trades every day, breach = 0, and clears a non-trivial fraction of the random targets.  
**Reject when:** trade count falls outside the band or clear rate is vacuous.

---

## 7. Final Promote Gate (only after all proposals are accepted)

The Court may issue a final **PROMOTE** only when:

- All ten proposals above have been accepted with measured evidence
- A multi-seed, multi-window 100-day forward test shows:
  - random targets drawn from [5, 90]
  - random risk floors drawn from [1, 3]
  - breach = 0 on every day
  - trade count ∈ [8, 400] every day
  - both pullbacks and continuations appear
  - weights never change after the lock
- Senses are proven to change decisions (unit test + measured ablation)
- The same frozen champion artifact is used for every target×risk pair

Until that gate is passed, the policy remains **not production-ready**.

---

## 8. How to use this document in Grok CLI

1. Drop this file into the workspace.
2. For every new idea or code change, treat it as a **proposal**.
3. Run the Court process (Creator / Mark / Counsel / Judge) against the Accept / Reject rules in Section 3.
4. Record the ruling and the new scoreboard numbers in the Evidence Ledger.
5. Never skip the order of the ten proposals unless the Judge re-orders by severity with a written reason.
6. The only success that counts is the 100-day random-target result with frozen weights.

---

**End of document.**  
This is the single instruction set the Court will follow until the one-bot 100-day mission is complete.
