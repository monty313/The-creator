"""Adapter profiles shared by 1:1 families (logic reuse OK; family ids stay unmerged)."""
from __future__ import annotations

from typing import Callable, Dict

from strategies.python_batch import families as fam
from strategies.python_batch.families_guide14 import GUIDE14_PROFILES
from strategies.python_batch.mtf import SetBars

# profile key → adapter function (bull, bear, modes)
PROFILES: Dict[str, Callable[[SetBars], tuple]] = {
    "mark_rsi_bb": fam.fam_mark_rsi_bb,
    "truth_s1_cci": fam.fam_s1_cci,
    "truth_s2_bb": fam.fam_s2_bb,
    "truth_s3_env": fam.fam_s3_env,
    "truth_s4_rsi_snap": fam.fam_s4_rsi_snap,
    "cci_gravity": fam.fam_cci_gravity,
    "bb_mtf": fam.fam_bb_mtf,
    "cool_bb": fam.fam_cool_bb,
    "sma_scalp": fam.fam_sma_scalp,
    "kinetic": fam.fam_kinetic,
    "jordan": fam.fam_jordan,
    "fasg": fam.fam_fasg,
    "snap8": fam.fam_snap8,
    "gv014": fam.fam_gv014,
    "gv015": fam.fam_gv015,
    "ati_sma": fam.fam_ati_sma,
    "orb": fam.fam_orb,
    "dual_thrust": fam.fam_dual_thrust,
    "supertrend": fam.fam_supertrend,
    "donchian": fam.fam_donchian,
    "bband_rsi": fam.fam_bband_rsi,
    "macd": fam.fam_macd,
    "ma_sample": fam.fam_ma_sample,
    "linreg": fam.fam_linreg,
    "ma_ribbon": fam.fam_ma_ribbon,
    "rl_proxy": fam.fam_rl_proxy,
    "momentum": fam.fam_mom_mtf,
    "challenge": fam.fam_challenge,
    "mcflurry": fam.fam_mcflurry,
    "dimension_jump": fam.fam_dimension_jump,
    # 14 strategies from Strategies-to-replicate guide
    **GUIDE14_PROFILES,
}


def resolve_adapter(profile: str) -> Callable[[SetBars], tuple]:
    if profile not in PROFILES:
        return PROFILES["mark_rsi_bb"]
    return PROFILES[profile]


def entries_for_profile(sb: SetBars, profile: str, mode: str):
    from strategies.python_batch.mtf import apply_htf_gate

    fn = resolve_adapter(profile)
    bull, bear, modes = fn(sb)
    pb_l, pb_s, cont_l, cont_s = modes
    return apply_htf_gate(bull, bear, pb_l, pb_s, cont_l, cont_s, mode)
