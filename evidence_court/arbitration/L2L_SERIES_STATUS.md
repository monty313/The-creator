# L2L series status (Court)

**Doc:** `L2L_PROJECT__ONE_BOT_100_DAYS.md`  
**Updated:** 2026-08-09 (P10 residual measured)

| # | Proposal | Ruling | Evidence |
|---|----------|--------|----------|
| 1 | Senses reach brain | **ACCEPT** | CASE-L2L-P1 · unit logits |
| 2 | Sight alive | **ACCEPT_NARROW** | process curriculum + units |
| 3 | Feel alive | **ACCEPT_NARROW** | load/collapse wait process |
| 4 | Taste alive | **ACCEPT_NARROW** | patience/noise process |
| 5 | Hearing alive | **ACCEPT_NARROW** | wait_subtype process |
| 6 | Step-by-step senses | **ACCEPT_NARROW** | multi-sense reward boost |
| 7 | L2L holdout | **ACCEPT_NARROW** | holdout curriculum steps |
| 8 | Lock weights | **ACCEPT** | freeze + fingerprint stable |
| 9 | Breach 0 | **ACCEPT** (measured windows) | dual breach_count=0 |
| 10 | 8–400 every day + clear | **REJECT full** | a13_every_day false |
| 10r | Density residual road | **ACCEPT_NARROW_LAB** | CASE-L2L-P10-residual |

**Final §7 gate:** **false**  
**Production champion:** still CASE-0037 `meta_policy_champion.npz` (`42:meta4275:…`)  
**Lab residual shadow:** `artifacts/meta_policy_l2l_p10_residual.npz` (`42:meta10835:…`)  
**Prior L2L washout shadow:** `artifacts/meta_policy_l2l_p2_p10.npz` (do not use)  
**Report:** `artifacts/l2l_p10_residual_report.json`  
**Case:** `cases/CASE-L2L-P10-residual.md`

### Residual dual (north-star random T×R)

| window | residual a13 | champ a13 | residual hits | floor hold |
|--------|-------------:|----------:|--------------:|:-----------|
| 30d | 0.33 | 0.27 | 3=3 | n/a |
| 100d | 0.42 | 0.41 | 7=7 | **false** vs BEST_POLICY 0.64/11/18 |

**Next:** C-004 conversion under density; raise a13_every_day; align dual SSOT with forward100 floor; multi-seed when dual climbs.
