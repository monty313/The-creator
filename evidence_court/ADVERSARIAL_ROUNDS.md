# Adversarial rounds — Creator vs Mark

**Status: PERMANENT COURT LAW (A10)** — not optional.  
**Full permanent law:** `ADVERSARIAL_ROUNDS_LAW.md` · pin `ADVERSARIAL_ROUNDS_LAW.json`  
**Master:** `MASTER_ARCHITECTURE.md` → Law A10  
**Canonical detail:** `../docs/grok_cli_evidence_court_v2.md` §1 roles, §2 items 2a–2b, §3 case schema, §4 mandatory loop.  
**Mark presentation:** `../mark_here/ESQUIRE.md`  
**Auto-load:** `../AGENTS.md` · `../.grok/rules/00_adversarial_rounds.md`  
**Test:** `tests/test_adversarial_rounds_law.py`

---

## The addition (plain language)

| Side | Opening | Proof | Then (max once) |
|------|---------|-------|-----------------|
| **Creator** | Strongest argument from the **internet** | **New test** for this case | One **counter-argument** + one **newer test** |
| **Mark Here, Esq.** | Strongest argument from **his knowledge** | **New test** for this case | One **counter-argument** + one **newer test** |

- Soft / placeholder openings → Judge orders redo before tests run.  
- Old suite greens / prior KAG / rank → **not** proof.  
- **No second counter** from either side. After counters (or waivers) → **Counsel (A15)** → Critic → Optimist → Judge IRAC.  
- Judge **must** weigh **three opinions**: Creator, Mark, **Counsel** (+ all evidence).

**Counsel (permanent A15):** sifts the **internet** for the **best possible policy**; files one `counsel_opinion`; does not write production code.  
→ `COUNSEL_TO_THE_COURT_LAW.md` · short sheet `COUNSEL.md`

---

## Sequence

```
1. Creator opening  (internet strongest + new test design)
2. Mark opening     (knowledge strongest + new test design)
3. Judge pre-register pass/fail for both opening tests
4. Run opening tests → both read results
5. Creator counter  (1× argument + newer test)  OR waive
6. Mark counter     (1× argument + newer test)  OR waive
7. Run counter tests (if any)
8. Counsel opinion  (internet sift → best policy + evidence/sources)  [A15]
9. Critic + Optimist on full record
10. Judge rules after weighing Creator + Mark + Counsel: INCONCLUSIVE | ADMIT_EXPERIMENT | REJECT | PROMOTE
```

“Newer test” = distinct assertion / fixture / bound / seed set / artifact path — not a re-run of the opening test.

---

## Case file fields

Use `creator_opening`, `mark_opening`, `creator_counter`, `mark_counter`, and **`counsel_opinion`** (A15) as in the Court protocol schema.  
Do not expand into unlimited rebuttal sections.
