# ADVERSARIAL ROUNDS LAW — PERMANENT (binding on Court roles)

**Status:** PERMANENT COURT LAW  
**Promoted:** 2026-08-07 as **Law A10** in `MASTER_ARCHITECTURE.md`  
**Human order:** Monty — make permanent  
**Not optional. Not a style preference. Not overridable by politeness, rank, or time pressure.**

Companion short sheet: `ADVERSARIAL_ROUNDS.md`  
**Counsel (A15 permanent):** `COUNSEL_TO_THE_COURT_LAW.md` — Judge must weigh **three opinions** (Creator, Mark, Counsel)  
Full procedure: `../grok_cli_evidence_court_v2.md` §1, §2 (2a–2b), §3, §4  
Mark: `../mark_here/ESQUIRE.md`

---

## Standing rule

Every Evidence Court case **must** run this structure:

| Round | Creator | Mark Here, Esq. |
|-------|---------|-----------------|
| **Opening** | Strongest argument from the **internet** | Strongest argument from **his knowledge** (soul / @physics / personal KAG) |
| **Proof** | **New test** for this case | **New test** for this case |
| **Counter (exactly one)** | One counter-argument + one **newer** test | One counter-argument + one **newer** test |

### Hard caps

1. **One opening per side** — strongest case, not a placeholder.  
2. **One new test per opening** — proves that opening. Old suite greens / prior KAG / rank ≠ proof.  
3. **One counter per side** — argument + **newer** test (distinct from that side’s opening test), or explicit **waive** on the record.  
4. **No second counter.** Judge strikes any third-round party reply.  
5. After counters (or waivers) → **Counsel opinion (A15)** → Critic → Optimist → Judge IRAC.  
6. Judge IRAC **must** deliberate on **all three opinions** + evidence: Creator, Mark, Counsel.

### “Newer test” means

Distinct assertion, fixture, bound window, seed set, case artifact path, or measurement order — **not** re-running the opening test.

---

## Judge enforcement (mandatory)

| Defect | Ruling posture |
|--------|----------------|
| Creator opens without strongest **internet** argument | INCONCLUSIVE — order redo of Creator opening |
| Mark opens without strongest **knowledge** argument | INCONCLUSIVE — order redo of Mark opening |
| Opening “proved” only by old tests / rank / pack cite | Insufficient — order **new** test |
| Second counter from either side | **STRIKE** the filing |
| PROMOTE without openings + new tests (and counters or waivers) | **Forbidden** |
| Missing Counsel opinion (post-A15) or IRAC ignoring Counsel | **INCONCLUSIVE** / **Forbidden PROMOTE** (see A15) |

---

## Required case fields (permanent schema)

New and open cases **must** include:

- `creator_opening` (incl. `strongest_internet_argument` + `new_test`)
- `mark_opening` (incl. `strongest_knowledge_argument` + `new_test`)
- `creator_counter` (`used` | `waived` + `newer_test` when used)
- `mark_counter` (`used` | `waived` + `newer_test` when used)
- `counsel_opinion` (**A15** — internet sift + policy recommendation + evidence/sources)

Historical PROMOTED cases (CASE-0001, CASE-0002, CASE-FORWARD-100) and pre-A15 experimental cases may lack `counsel_opinion` only as frozen history. **All cases opened after Law A15** require Counsel.

---

## Immutable

This law is **append-only permanent**.  
It may only be amended by a **new Court case** that PROMOTE-replaces it with a superceding Law id, with human (Monty) approval on the record.  
Silent weakening is a Court defect.

**Pinned by test:** `evidence_court/tests/test_adversarial_rounds_law.py`  
**Machine pin:** `evidence_court/ADVERSARIAL_ROUNDS_LAW.json`
