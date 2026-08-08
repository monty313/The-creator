# Court transcript — Creator v. @mark_here (facts only)

**Standard:** Rhetoric does not pass. Only runnable tests and reproducible artifacts pass.  
**Mark has the KAG.** Creator owns production code after PROMOTE.

---

## CASE-0001 — Meta-RL state (prior)

| Role | Position | Evidence status |
|------|----------|-----------------|
| Creator | Additive Mark-168 + goal/risk-8; frozen policy | PROVED by `test_goal_risk_no_retrain`, `test_risk_envelope` |
| Mark | Preserve sets law; fix target saturation | PROVED by sets pin + legacy saturation test |
| Critic | No retrain / risk envelope | PROVED |
| Judge | **PROMOTE** | execution_record + IRAC on file |

---

## CASE-0002 — Multi-TF pullback/continuation edge (this session)

### Table opening

**Creator claim:** The untested edge in `Possible edge not tested.txt` is implemented as HTF force (official set confirmations) + LTF RSI(5)+BB(10,0.5,shift+2) timing for pullback_resume and continuation; multi-symbol concurrent book; 1:100 risk-legal lots; no look-ahead.

**Mark Here, Esq. counter (KAG):**
1. LTF must not redefine side without HTF permission.
2. Must scan all four Mark sets — never set2-only eyes.
3. Multi-symbol risk must aggregate on one daily ledger.
4. Leverage in lot math must be 1:100 (flea-jar), not folklore range.
5. These require **NEW tests**, not recycled CASE-0001 greens.

### Live evidence (commands + results)

```text
python -m pytest evidence_court/tests -q
→ 37 passed

python -m evidence_court.meta_rl.cli forward100 --days 100
→ promote_ready=true
→ n_days=100 breach_count=0 no_retrain=true
→ multi_symbol=true symbols=[XAUUSD,EURUSD,GBPUSD]
→ leverage=100.0
→ total_pullback_signals=18 total_continuation_signals=162
→ symbols_with_trades=[EURUSD,GBPUSD,XAUUSD]
→ no_lookahead=true force_side_used=false
→ l2l_day_path_ok=true senses_day_path_ok=true goal_consistency_ok=true
→ total_hits=2 (target 5% hit_rate=0.111) max_day_pnl≈14.21%
```

**Mark NEW tests** (`test_mark_kag_case0002_new.py`) — all passed:
- `test_NEW_mark_htf_incomplete_blocks_lone_ltf_fire`
- `test_NEW_mark_all_four_sets_scanned_never_set2_only`
- `test_NEW_mark_multi_symbol_aggregate_risk_envelope`
- `test_NEW_mark_risk_legal_lot_uses_leverage_100`
- `test_NEW_mark_state_dirs_drive_policy_not_rhetoric`

### Critic audit (measured)

| Check | Result |
|-------|--------|
| Look-ahead | Decision M1/TF as-of prior day; fill open→close/stop |
| force_side oracle | Absent (`force_side_used=false`) |
| Daily risk breach | 0 / 100 days |
| 1:100 leverage | metadata.leverage=100; lot unit tests |
| Pullbacks AND continuations | pb=18, cont=162 |
| Multi-symbol concurrent | 3 symbols traded under one ledger |
| No retrain | train_steps=0; fingerprint stable |

### Optimist note

Coverage path is live (pb+cont). High targets (70–90) still low hit_rate under 1–3% risk — **measured**, not declared impossible (flea-jar: incomplete opportunity vs ceiling).

### Judge IRAC — CASE-0002

- **Issue:** May Creator integrate multi-TF RSI5+BB pullback/continuation edge with multi-symbol 1:100 risk-legal sizing?
- **Rule:** PROMOTE only with NEW Mark tests, prior-only indicators, Mark sets law, flea-jar checklist, breach=0, day-path L2L/senses.
- **Application:** All measured gates hold. Mark’s NEW tests green. Forward100 promote_ready true.
- **Conclusion:** **PROMOTE**
- **Next:** CASE-FORWARD-100 remains PROMOTE under upgraded multi-symbol multi-TF path; live MT5 deploy still requires separate human step.

### Judge IRAC — CASE-FORWARD-100 (re-measured)

- **ruling:** **PROMOTE** (forward_sim_shadow)  
- **Artifact SHA256:** `23f1bc438b061317ac41948a05f88706d8ecdbd0729cdf31aba524a8eb909754`

---

## What did *not* pass (not claimed)

- Live MT5 order placement  
- “90% daily is easy” — hit_rate at 90% measured **0** on this window under 1–3% risk  
- Trained neural champion `.pt` — frozen Court policy stub only  
