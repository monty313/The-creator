# CASE-L2L-P1 — Senses reach the brain and change decisions

**case_id:** CASE-L2L-P1  
**status:** CLOSED — **ACCEPT** (Proposal 1 under `L2L_PROJECT__ONE_BOT_100_DAYS.md`)  
**opened:** 2026-08-09  
**instruction_doc:** `L2L_PROJECT__ONE_BOT_100_DAYS.md` §6 Proposal 1  
**docket_issue_id:** C-001 / C-005 sense-drive residual  
**goal_axes:** G-SIGHT, G-FEEL, G-TASTE, G-HEAR, G-L2L, G-TRAIN, G-NO_RETRAIN  

**question:** Can the four sense reports (sight/feel/taste/hearing) be encoded into a fixed numeric vector, packed into the Meta-RL state the brain trains and infers on, without expanding `META_RL_DIM` (frozen-weight load contract), and can a unit test prove that changing only a sense value changes the brain’s logits?

---

## ROUND STRUCTURE (A10 + A15)

Creator + Mark openings + NEW tests → counters → Counsel → Critic → Optimist → Judge IRAC  

**Roles:** Creator codes after ACCEPT only. Mark and Counsel do not write production code.

---

## Creator opening

### strongest_internet_argument

State representation learning for sequential decisions requires packing **task-relevant sensory features** into the observation the policy actually reads — not leaving multi-view signals as side-channel logs. Multi-view / multi-feature RL work shows agents need fused numeric channels so attention can weight them; probe-only senses fail the “drive the brain” test (A32).  

**claim:** Encode four Court senses → fixed 16-d pack → write into Mark agent_votes[0:16] so `META_RL_DIM` stays **176** and champion `.npz` still loads; brain `forward_raw` reacts when only sense slots change.

**new_test:** `test_creator_new_sense_value_change_changes_brain_logits`  
**also:** `test_creator_new_senses_pack_into_meta_rl_state_dim_preserved`

---

## Mark Here, Esq. — opening

### strongest_knowledge_argument

Mark’s soul/KAG and A32: Sight / Feel / Taste / Hearing are **relational** (force, load, edge quality, day story) — not indicator names. Fail modes (flat on B&B day; lone oscillator; all bars equal; thrash reverse) are only killable if the **brain sees** the sense pack at train and prove. Probe-only `_sense_l2l_once` that never enters `build_meta_rl_state` is costume physics.  

**claim:** Day path must call `probe_all_senses` and pass `sense_report=` into state packing; layout must name the sense slice.

**new_test:** `test_mark_new_senses_not_probe_only_in_layout`  
**also:** shipped goal_path packs `sense_report` on decision path (`meta["senses_packed"]=True`)

---

## Creator counter

**counter:** Expanding META_RL_DIM would break frozen champion load and smuggle a cliff (retrain every layout). Keep dim 176; overlay senses into existing agent_votes capacity (were zeros on production path).  

**newer_test:** `test_creator_new_senses_pack_into_meta_rl_state_dim_preserved` asserts `META_RL_DIM == 176`.

---

## Mark counter

**counter:** Overlay is not “handing the final trade.” Teacher path still Mark topology; senses are process channels. Old champion has weak/random weights on those columns until curriculum trains them — Proposal 1 is **wiring**, Proposals 2–6 make senses **alive** under reward.  

**newer_test:** waive further unit — wiring proven by Creator logits test; residual = train-time process reward (P2–P6).

---

## Counsel opinion (A15)

### internet_sift

State representation learning surveys emphasize compact task-relevant channels over raw multi-stream logs. Multi-view RL and multi-feature supervised RL for markets pack heterogeneous signals into a shared state for the policy net — not side probes. Attention-based RL needs features **in** the observation to weight them.

### policy_recommendation

1. ACCEPT Proposal 1 packing into fixed slots without dim break.  
2. Do **not** treat ACCEPT as final boss — retrain/curriculum for sense columns is P2–P7.  
3. Keep breach rails and A13 process separate (P9–P10).  
4. Pin unit: sense-only delta → logit delta.

### opinion

Creator’s dim-safe pack + Mark’s drive-not-probe demand align with policy science. Reject would freeze A32 as decoration.

### evidence

Units in `tests/test_l2l_proposal1_senses_drive_brain.py` (4/4). Layout in `state.meta_rl_layout()`.

### sources

- arXiv state representation learning survey (DeepMind-linked SRL framing)  
- Multi-view / multi-feature RL packing practice  
- Court A32 + L2L_PROJECT §2–3  

---

## Critic

- Overlay uses agent_votes region historically reserved for 92 agents — document the smuggle.  
- Untrained sense columns on production champion mean weak effect until meta-train.  
- 100-day north star not yet re-measured (Proposal 1 is wiring).

## Optimist

- Unblocks A32 production rule without cliff retrain of whole layout.  
- Honest road for L2L process supervision.  
- Unit proves non-decoration.

---

## Judge IRAC

### Issue

Does packing four senses into Meta-RL state (fixed 16-d, dim-preserving) so the brain’s logits react, without handing final trades or breaking freeze, satisfy L2L Proposal 1 Accept rules?

### Rule

L2L_PROJECT Accept: closer to north star path; no final answer; freezable weights; breach path; PB+cont remain; senses change decisions; unit proof.  
A10+A15 three opinions. A32 senses drive brain. A14 no retrain at inference. META_RL_DIM load contract.

### Application

- **Creator:** encode + pack + logits test **PASS**.  
- **Mark:** layout + not probe-only + day-path pack **PASS**.  
- **Counsel:** SRL multi-view pack recommendation; ACCEPT wiring, defer alive-reward to later proposals.  
- Dim 176 held → champion load contract held.  
- No hard if-rule trade; brain still decides.  
- PB/cont topologies still in edge path.  
- Residual: champion weights not yet meta-trained on sense columns → P2–P6.

### Conclusion

1. **ACCEPT** Proposal 1 (CASE-L2L-P1).  
2. Code: `encode_sense_report`, `build_meta_rl_state(sense_report=...)`, goal_path pack.  
3. **Not** final PROMOTE of mission; continue Proposal 2 (Sight alive).  
4. Ledger + scoreboard history append.  
5. Champion file not replaced solely by this case (wiring only).

---

## Measured proof

| Test | Result |
|------|--------|
| `test_l2l_proposal1_senses_drive_brain.py` | **4/4 PASS** |
| `test_senses.py` | green |
| META_RL_DIM | **176** |

---

## Implementation map

| Module | Change |
|--------|--------|
| `meta_rl/senses.py` | `SENSE_PACK_DIM`, `encode_sense_report` |
| `meta_rl/state.py` | sense overlay into agent_votes; `extract_sense_pack` |
| `meta_rl/goal_path.py` | pack senses on decision + teacher paths |
| `tests/test_l2l_proposal1_senses_drive_brain.py` | Creator/Mark new tests |

---

**Next Court case under L2L doc:** Proposal 2 — Sight becomes alive on structure.
