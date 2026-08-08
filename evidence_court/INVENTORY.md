# Repository inventory — Evidence Court session 1

**Date:** 2026-08-07  
**Scope:** Locate existing Mark obs, sets, risk/sim, tests, protected invariants.  
**Rule:** No production model code written in this inventory step.

| path | purpose | owner/module | current test command | change risk |
|------|---------|--------------|----------------------|-------------|
| `mark_here/knowledge/lab/lineages/adaptive_rl_brain_7_31_26/perception/observation.py` | Channel1 32-dim sets packer | adaptive_rl_brain | none in portable pack | HIGH — layout pin |
| `mark_here/.../perception/observation_full.py` | Mark full 168-dim obs | adaptive_rl_brain | none in portable pack | HIGH — dim/layout |
| `mark_here/.../perception/sets.py` | MARK_SETS_LAW official stacks | adaptive_rl_brain | assert on import | CRITICAL — law |
| `mark_here/FULL_OBS_AND_TIMEFRAME_SETS.md` + `.json` | Doctrine card for 168-dim + sets | portable root | n/a (docs) | HIGH — semantics |
| `mark_here/knowledge/lab/configs/timeframes.yaml` | sets_mark vs proven_legacy | lab configs | n/a | HIGH — wrong lock = silent wrong eyes |
| `mark_here/knowledge/lab/configs/features.yaml` | sets_lock, self_state, slots flag | lab configs | n/a | HIGH — PROVEN vs Mark |
| `mark_here/knowledge/lab/configs/signal_slots.yaml` | 92 agent registry | lab configs | n/a | MED |
| `mark_here/knowledge/lab/GOAL.md` | no-retrain target/risk mission | lab doctrine | prove_it style | CRITICAL — goal |
| `mark_here/knowledge/lab/lineages/.../MARK_SETS_LAW.md` | immutable TF stacks | Mark/Monty | rewrite only with human | CRITICAL |
| `mark_here/knowledge/lab/lineages/.../MARK_DOCTRINE_FIVE_LAWS.md` | force→regime→velocity chain | Mark doctrine | n/a | HIGH |
| `mark_here/PRICE_DATA.md` + `PRICE_DATA_PATHS.json` | CSV discovery map | portable | n/a | LOW |
| `mark_here/WHO_I_AM.md` | Personhood: same Mark soul + personal KAG only | Mark identity | n/a | CRITICAL — identity |
| `mark_here/ESQUIRE.md` | Mark Here, Esq.: @physics + beliefs; evidence-in-tests duty | Mark advocacy | n/a | CRITICAL — Court voice |
| `mark_here/knowledge/soul/` | Personality, Fable, moral doctrine | Mark soul | n/a | CRITICAL — who he is |
| `mark_here/knowledge/kag/` | Mark-only knowledge/experiences (not other roles) | Mark personal KAG | n/a | HIGH — memory continuity |
| `mark_here/knowledge/kag/army/PHYSICS_*.md` | Physics law anchors for Mark’s advocacy | @physics | n/a | HIGH — law cites |
| `evidence_court/FLEA_JAR_COURT_LAW.md` | Full flea-jar law for all roles + Judge gate | Court / Judge | n/a | CRITICAL — impossibility gate |
| `C:/Users/user/Fable5_Foundation/.../data/raw/*.csv` | M1 OHLCV (XAU/EUR/GBP/US30) | lab price | n/a | external data |
| `mark_here/strategy/factory_full/*.py` | GV/ML strategy sim (not Meta-RL) | strategy factory | verify.py / wf.py | MED — separate stack |
| Lab `types.py` (not in portable pack) | Direction, SetConfluence, OfficialSet | lab perception | n/a | missing in pack |
| PROVEN ~1820 / SIGON ~6820 | other obs systems | features.yaml | n/a | **PROTECTED** — never mix weights |
| Evidence Court (`evidence_court/`) | this workspace | Court | pytest evidence_court/tests | NEW |

## Protected invariants

1. **MARK_SETS_LAW stacks** must remain `1m,15m,30m · 5m,30m,1h · 15m,1h,4h · 30m,4h,1d`.
2. **Mark full obs 168-dim layout** blocks (32+16+12+92+16) must not be silently reordered.
3. **No warm-start PROVEN → Mark-168** or reverse without retrain case.
4. **Target/risk are inference inputs** — no retrain when pair changes.
5. **Portable pack** does not embed price CSVs or full training entry; use PRICE_DATA map.

## Gaps for CASE-0001

- Portable pack lacks `types.py` and runnable Meta-RL policy/prove entry.
- Existing `pack_self_state` encodes `target_pct/5` (saturates ≥5%) — insufficient for [5,90] band.
- No Court case files, L2L/senses gates, or 100-day matrix eval in this repo root.

## Smallest first case

**CASE-0001:** How to transform existing Mark observation + retained timeframe sets into Meta-RL state for (a) inference-time target/risk, (b) learn-to-learn, (c) emergent senses — without unadjudicated production model code first.
