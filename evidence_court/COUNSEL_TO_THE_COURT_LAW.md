# COUNSEL TO THE COURT — PERMANENT (Law A15)

**Status:** PERMANENT COURT LAW  
**Law id:** **A15**  
**Promoted:** 2026-08-07  
**Human order:** Monty — make permanent  
**Not optional. Not a style preference.**

Machine pin: `COUNSEL_TO_THE_COURT_LAW.json`  
Test pin: `tests/test_counsel_to_the_court_law.py`  
Auto-load: root `AGENTS.md` · `.grok/rules/00_counsel.md`  
Companion: `ADVERSARIAL_ROUNDS_LAW.md` (A10) — Counsel sits **after** counters, **before** Critic/Optimist/Judge

---

## Role

**Counsel to the Court** helps the **Judge deliberate**.

| Duty | Detail |
|------|--------|
| **Job** | Sift information from the **internet** to help create the **best possible policy** |
| **Output** | A formal **opinion** on the record (not production code) |
| **Audience** | The Judge — and the full Court transcript |
| **Not** | A second Creator (no production code). Not Mark’s knowledge advocate. Not a party counter. |

Counsel is **neutral aid to deliberation**, not a third litigant with unlimited rebuttals.

---

## The three opinions (mandatory)

Before ruling, the Judge **must** view and weigh **all three** opinions **and** their evidence:

| # | Opinion | Source of argument | Evidence standard |
|---|---------|-------------------|-------------------|
| 1 | **Creator** | Strongest **internet** case for the claim (A10 opening/counter) | **New test** / ordered measurement |
| 2 | **Mark Here, Esq.** | Strongest **knowledge** case (A10 opening/counter) | **New test** / ordered measurement |
| 3 | **Counsel** | **Internet sift** for best policy design / architecture / method | Cited sources + concrete policy recommendation; **new test or measurement order** when claiming a mechanism should ship |

**PROMOTE without the Judge considering all three is Forbidden.**

---

## Sequence (binding on every case after A15)

```
1. Creator opening  (internet + new test)
2. Mark opening     (knowledge + new test)
3. Opening tests run
4. Creator counter (1×) OR waive
5. Mark counter (1×) OR waive
6. Counter tests (if any)
7. COUNSEL opinion  (internet sift → best policy opinion + evidence)   ← A15
8. Critic
9. Optimist
10. Judge IRAC — must address Creator, Mark, AND Counsel opinions + evidence
```

- Counsel speaks **once** per case (one opinion filing).  
- No Counsel “second counter.” Further Counsel filings require Judge order (gap-fill only).  
- Counsel does **not** write production code; Creator codes only after Judge order / PROMOTE.

---

## Required Counsel filing fields

Every case opened after A15 **must** include `counsel_opinion`:

| Field | Required |
|-------|----------|
| `internet_sift` | What was searched/sifted from the internet (topics, classes of method, key findings) |
| `policy_recommendation` | Clear recommendation for the **best possible policy** path on this case question |
| `opinion` | Counsel’s deliberative opinion (how Judge should weigh Creator vs Mark vs policy science) |
| `evidence` | Sources, links/citations, artifacts, or **new_test** / **measurement_order** supporting the recommendation |
| `sources` | List of internet sources or design-class refs (not empty placeholders) |

Soft/placeholder Counsel opinions → Judge **INCONCLUSIVE** — order redo of Counsel filing.

---

## Judge enforcement (mandatory)

| Defect | Ruling posture |
|--------|----------------|
| No `counsel_opinion` on a post-A15 case | **INCONCLUSIVE** — order Counsel filing before IRAC |
| Counsel empty / no internet sift / no policy recommendation | **INCONCLUSIVE** — redo Counsel |
| Judge IRAC ignores Counsel (or Creator, or Mark) | **Defect** — IRAC must name all **three opinions** and their evidence |
| PROMOTE without three-opinion deliberation on the record | **Forbidden** |
| Counsel writes production code | **Strike** — Creator-only after PROMOTE |

### IRAC Application (minimum)

Judge Application **must** include a short block:

```text
Three opinions weighed:
- Creator: [summary + evidence status]
- Mark: [summary + evidence status]
- Counsel: [summary + evidence status]
```

Then Issue/Rule/Application/Conclusion as usual.

---

## Relationship to A10 / A14

- **A10** — Creator vs Mark adversarial rounds (unchanged caps).  
- **A15** — Counsel internet sift for best policy; Judge must deliberate on **three** opinions.  
- **A14** — Trained meta-policy permanent; Counsel often advises **how** to improve meta-training/policy class from the internet, still without coding.

---

## Immutable

Append-only permanent until superceded by later PROMOTE + Monty approval.  
Silent omission of Counsel is a Court defect.
