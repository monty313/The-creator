# Strategies — lab prove folder

**Not Court law. Not production hard-code.**

## For any future LLM

**Process SSOT (do everything we did, per strategy):**  
→ **[LLM_INSTRUCTIONS.md](LLM_INSTRUCTIONS.md)**

That file is the full pipeline: language → 1:1 inventory → baseline batch → accuracy (WR > 60.4%) → optional H2H → Monte Carlo → inject results into each strategy’s files. **Do not invent a shorter path.**

**14 strategies from “Strategies to replicate in Algo Trading” HTML:**  
→ language notes in [algo_guide_14/](algo_guide_14/) · prove report [ALGO_GUIDE_14_PROVE_REPORT.md](ALGO_GUIDE_14_PROVE_REPORT.md)  
→ re-prove: `python -m strategies.python_batch.run_prove_guide14`

Teaching geometry (not a promote list): [00_intuition.md](00_intuition.md)

---

## Results (current corpus)

| Artifact | What |
|----------|------|
| **[LLM_INSTRUCTIONS.md](LLM_INSTRUCTIONS.md)** | Full prove process for every new/existing strategy |
| **[TWEAKED_ACCURACY_REPORT.md](TWEAKED_ACCURACY_REPORT.md)** | Post-tweak: all families **WR > 60.4%** |
| **[TWEAKED_ACCURACY_RESULTS.json](TWEAKED_ACCURACY_RESULTS.json)** | Pre/post win rates + scores |
| **[tweaks/](tweaks/)** | Per-family what / why / scores + MC block |
| **[FAMILY_INVENTORY_1TO1.json](FAMILY_INVENTORY_1TO1.json)** | 1:1 families, `collapses: []` |
| **[STRATEGY_TEST_REPORT.md](STRATEGY_TEST_REPORT.md)** | Pre-tweak baseline batch |
| **[ranked/](ranked/)** | Baseline rank folders + all-sim inject |
| **[SAUCES_TEST_REPORT.md](SAUCES_TEST_REPORT.md)** | McFlurry + Dimension Jump baseline |
| **[CCI_VS_MCFLURRY_REPORT.md](CCI_VS_MCFLURRY_REPORT.md)** | CCI upgraded vs McFlurry |
| **[MONTE_CARLO_REPORT.md](MONTE_CARLO_REPORT.md)** | Bootstrap + shuffle MC |
| **[MONTE_CARLO_RESULTS.json](MONTE_CARLO_RESULTS.json)** | Full MC distributions |
| **[MONTE_CARLO_BY_FILE.md](MONTE_CARLO_BY_FILE.md)** | MC rank → tweak file |
| **[SIM_RESULTS_INJECT_REPORT.md](SIM_RESULTS_INJECT_REPORT.md)** | Inject coverage proof |

## Re-run (full pipeline)

```text
python -m strategies.python_batch.inventory_1to1
python -m strategies.python_batch.run_strategy_batch_1to1
python -m strategies.python_batch.run_sauces_test
python -m strategies.python_batch.run_tweak_batch
python -m strategies.python_batch.run_monte_carlo --sims 1000 --seed 42
python -m strategies.python_batch.inject_all_sim_results
python -m pytest strategies/python_batch/test_batch_1to1_smoke.py strategies/python_batch/test_tweak_winrate.py -q
```

Optional H2H: `python -m strategies.python_batch.run_cci_vs_mcflurry`

Contract: **2 HTF + 1 LTF**, four MARK sets, **pullback + continuation**, vectorbt.

## Language sources

See `language/` (cited). Note folders keep prose; each note is its own family in the 1:1 inventory. Sauces live in `sauces/`.
