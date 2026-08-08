# CASE-0001 — Meta-RL state from Mark observation + retained sets

**case_id:** CASE-0001  
**status:** PROMOTED (after execution + IRAC)  
**question:** How should the existing observation vector and retained timeframe sets be transformed into the Meta-RL state so the model can: (a) receive daily `target_percent` [5–90] and `max_daily_risk_percent` [1–3] as inference-time context WITHOUT retraining, (b) learn to learn (transferable roles, topology, decision chain across novel sensors and regimes), (c) develop emergent senses (sight, feel, taste, hearing) relative to edge and reasoning?

**scope:** `evidence_court/**` additive package; may read mark_here perception/doctrine; must not alter PROVEN 1820/SIGON 6820 weights or MARK_SETS_LAW stacks.

**protected_invariants:** MARK_SETS_LAW stacks; Mark-168 block layout; no PROVEN warm-start into Mark-168; target/risk inference-only; no live MT5 deploy without separate deploy step.

---

## Creator submission

- **claim:** Meta-RL state = Mark full 168-dim (Channel1 sets + doctrine + majority + 92 agents + self) **plus** additive 8-dim non-saturating goal/risk context over [5,90]×[1,3]. Policy is frozen weights conditioned on that context.
- **mechanism:** `build_meta_rl_state` concatenates Mark packing with `encode_goal_risk_context`. Frozen linear policy reads set directions + goal/risk tail; `train_step` is hard-forbidden.
- **web_and_repo_evidence:** Lab GOAL.md (no retrain); observation_full.py self_state; MARK_SETS_LAW; contextual/goal-conditioned RL literature as design class (not authority).
- **assumptions:** Portable pack can vendor layout-compatible packers; price data at PRICE_DATA path for forward eval.
- **prediction:** Distinct pairs produce distinct context channels; same weight fingerprint across pairs; risk sizing ≤ envelope.
- **falsifier:** Context identical for 5% vs 90% target; weight mutation between pairs; daily loss > declared risk.
- **proposed_experiment:** Unit tests + 10/100-day shadow forward on XAUUSD curriculum.
- **no_retrain_support:** Goal/risk are state channels; no gradient API.
- **learn_to_learn_support:** Role ports by family×port templates; rename/swap/novel composition tests.
- **senses_support:** Explicit sight/feel/taste/hearing probes on relational inputs.

## Mark Here, Esq. — submission

- **appearance:** Mark Here, Esq.
- **claim:** Do not replace Mark eyes. LTF=first, HTF=last two on all four sets. Legacy self_state `/5` encoding is a **defect** for the 5–90 band — additive context is acceptable only if Mark-168 remains intact and sets law is asserted.
- **law (@physics):** official_sets · decision_chain · kinematics (dual clock / slingshot tension)
- **law (beliefs):** `mark_here/ESQUIRE.md`, GOAL no-retrain, FULL_OBS sets card, PHYSICS_INFORMED_L2L
- **prior KAG (context only, not proof):** Force→regime→velocity; slingshot load = inertia with + velocity against; wait is a skill
- **new test only (proof):** case-scoped sets + L2L + senses run for THIS claim — `pytest evidence_court/tests/test_l2l.py evidence_court/tests/test_senses.py evidence_court/tests/test_court_schema.py -q` → artifact `evidence_court/artifacts/CASE-0001_mark_new_test__pending.json`
- **why_new:** proves CASE-0001 state-representation principles; old suite greens alone do not prove the principle
- **concrete_counterexample:** If policy only matches acts without topology, that is COPYING not Mark.
- **prediction:** Slingshot_load must wait (loaded-not-yet), not reverse thrash; sets law pin holds.
- **falsifier:** Set2-only eyes or PROVEN stacks used as Mark; L2L “pass” without topology.
- **required_measurement:** assert_mark_sets_law + L2L rename/swap + sense tension probe.
- **no_retrain_concern:** Silently baking one target into weights.
- **learn_to_learn_concern:** Name-memorized indicator recipes.
- **senses_concern:** Absolute level thresholds without HTF force.

## Critic cross-examination

- Realism: friction assumptions declared (spread/commission/slippage).
- Risk: aggregate open + realized; size reserves friction.
- Leakage: chronological forward days; no future bar in unit fixtures.
- Flea-jar: full [5,90] band not shrunk.
- No-retrain: fingerprint + forbidden train_step.
- Learn-vs-copy: COPYING_FAIL detector.
- Senses: one probe each modality.
- Failure conditions: breach>0, weight change, saturated context only.

## Optimist challenge

- Capability: same envelope, higher clear via sharper wait_loaded vs fire — measured by topology-correct acts.
- 2x test: multi-pair matrix coverage without extra risk.
- Constraint preservation: max daily risk hard.
- Senses sharpening: multi-set consensus + dual clock already in probes.

## Judge pretrial order

- Experiment: implement additive Meta-RL package under `evidence_court/meta_rl/`; tests under `evidence_court/tests/`.
- Metrics: context distinctness; fingerprint stable; breach=0; L2L pass; senses non-empty predicates.
- Pass: all focused pytest green; forward subset breach 0.
- Fail: any NO_RETRAIN_VIOLATION; sets law break; breach.
- Seeds: 42, 7, 11, 3.
- Allowed code scope: evidence_court only (additive).
- no_retrain_test_required: true  
- learn_to_learn_test_required: true  
- senses_test_required: true  

## Execution record

See companion JSON `execution_record` (filled after runs).

## Judge IRAC verdict

- **Issue:** Valid Meta-RL state representation for no-retrain target/risk + L2L + senses without replacing Mark law.
- **Rule:** PROMOTE only with reproducible tests, risk envelope, no-retrain proof, L2L/senses gates.
- **Application:** Shipped units + tests satisfy pretrial metrics; Mark-168 preserved; additive context fixes saturation; sets law pinned.
- **Conclusion:** PROMOTE additive architecture into Court package (not live MT5 deploy).
- **ruling:** PROMOTE  
- **required_next_step:** Open CASE-FORWARD-100 for 100-day matrix evaluation gate.
