"""1:1 inventory: every MT index name + every strategy note file (no collapses)."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

STRATEGIES = Path(__file__).resolve().parents[1]
MT_INDEX = STRATEGIES / "language" / "01_METATRADER_INDEX.md"

NOTE_DIRS = [
    STRATEGIES / "local_desktop",
    STRATEGIES / "army_library_strategy_copy",
    STRATEGIES / "army_snap8",
    STRATEGIES / "mark_doctrine_refs",
    STRATEGIES / "the_truth_main_extra",
    STRATEGIES / "algo_guide_14",
]

SKIP_NOTE_NAMES = {
    "SOURCE.md",
    "README.md",
    "README_FACTORY.txt",
}


@dataclass
class FamilySpec:
    family_id: str
    kind: str  # "mt" | "note"
    title: str
    source: str
    adapter_profile: str
    fidelity: str
    collapses: list  # always empty for this goal


def _slug(s: str) -> str:
    s = s.strip()
    s = re.sub(r"[^\w\-]+", "_", s, flags=re.UNICODE)
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:120] if s else "unnamed"


def parse_mt_index(path: Path = MT_INDEX) -> List[tuple[str, str, str]]:
    """Return list of (name, platform, summary) from MT index table."""
    rows: List[tuple[str, str, str]] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if line.startswith("| Name") or line.startswith("|---") or line.startswith("|------"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 3:
            continue
        name, plat, summary = parts[0], parts[1], parts[2]
        if not name or name.lower() == "name":
            continue
        # skip pure separator
        if set(name) <= {"-", " "}:
            continue
        rows.append((name, plat, summary))
    return rows


def list_note_files() -> List[Path]:
    out: List[Path] = []
    for d in NOTE_DIRS:
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*")):
            if not p.is_file():
                continue
            if p.name in SKIP_NOTE_NAMES:
                continue
            if p.suffix.lower() not in {".md", ".txt"}:
                continue
            # skip nested SOURCE already handled
            if p.name.upper() == "SOURCE.MD":
                continue
            out.append(p)
    return out


def pick_profile(name: str, summary: str = "", path_hint: str = "") -> tuple[str, str]:
    """Map sparse language → adapter profile key + fidelity label."""
    blob = f"{name} {summary} {path_hint}".lower()

    # --- Algo guide 14 (Strategies to replicate in Algo Trading) ---
    _guide = {
        "s01_ma_crossover": "guide_s01_ma_cross",
        "s02_breakout_trading": "guide_s02_breakout",
        "s03_donchian_turtle": "guide_s03_donchian_turtle",
        "s04_adx_directional": "guide_s04_adx_di",
        "s05_roc_momentum": "guide_s05_roc",
        "s06_parabolic_sar": "guide_s06_psar",
        "s07_ema_ribbon": "guide_s07_ema_ribbon",
        "s08_bb_mean_reversion": "guide_s08_bb_mr",
        "s09_rsi_reversion": "guide_s09_rsi_mr",
        "s10_vwap_reversion": "guide_s10_vwap_mr",
        "s11_keltner_reversion": "guide_s11_keltner_mr",
        "s12_zscore_reversion": "guide_s12_zscore_mr",
        "s13_stochastic_reversion": "guide_s13_stoch_mr",
        "s14_williams_r_reversion": "guide_s14_willr_mr",
    }
    for slug, prof in _guide.items():
        if slug in blob or slug in path_hint.lower():
            return prof, "high"
    if "algo_guide_14" in blob or "algo_guide_14" in path_hint.lower():
        # fallback if slug rename — still own family, map carefully
        return "guide_s01_ma_cross", "medium"

    if "rsi_bb_l2l" in blob or ("rsi" in blob and "bb" in blob and "skill" in blob):
        return "mark_rsi_bb", "high"
    if "rsi + bb" in blob or "rsi+bb" in blob:
        return "mark_rsi_bb", "high"
    if re.search(r"strategy_s1|cci.?slingshot|dual cci", blob):
        return "truth_s1_cci", "high"
    if re.search(r"strategy_s2|bb_trend_reversion|trend reversion", blob):
        return "truth_s2_bb", "high"
    if re.search(r"strategy_s3|envelope_breakout|envelope", blob):
        return "truth_s3_env", "high"
    if re.search(r"strategy_s4|rsi_tension|tension snap", blob):
        return "truth_s4_rsi_snap", "high"
    if "snap-8" in blob or "snap8" in blob or "nested alignment" in blob:
        return "snap8", "high"
    if "gv-014" in blob or "gv014" in blob or "gravity snap" in blob:
        return "gv014", "medium"
    if "gv-015" in blob or "gv015" in blob or "tunnel" in blob:
        return "gv015", "medium"
    if "adr-0004" in blob:
        return "truth_s1_cci", "medium"  # multi-strategy ADR — still own family

    # MT / name heuristics
    if "cci_gravity" in blob or "strikegate" in blob:
        return "cci_gravity", "medium"
    if "zeroline" in blob or "zero_line" in blob or "zero line" in blob:
        return "cci_gravity", "medium"
    if "bb_mtf" in blob or "strategy4" in blob or "cci_mtf_bb" in blob:
        return "bb_mtf", "medium"
    if "coolbollinger" in blob or "coolboolinger" in blob or "cool bollinger" in blob:
        return "cool_bb", "medium"
    if "sma_scalper" in blob or "sma_fan" in blob or "tritf_sma" in blob:
        return "sma_scalp", "medium"
    if "kinetic" in blob:
        return "kinetic", "medium"
    if "jordan" in blob or "unity play" in blob or "momentum_matrix" in blob or "play 4" in blob:
        return "jordan", "medium"
    if "fasg" in blob or "trendday" in blob:
        return "fasg", "medium"
    if "shifted" in blob and "sma" in blob:
        return "ati_sma", "medium"
    if "gold_orb" in blob or "orb" in blob and "gold" in blob:
        return "orb", "medium"
    if "london" in blob and "breakout" in blob:
        return "orb", "medium"
    if "dual thrust" in blob or "dual_thrust" in blob:
        return "dual_thrust", "medium"
    if "supertrend" in blob:
        return "supertrend", "medium"
    if "donchian" in blob:
        return "donchian", "medium"
    if "bband" in blob or "bandtastic" in blob or "multi rsi" in blob:
        return "bband_rsi", "medium"
    if "macd" in blob:
        return "macd", "medium"
    if "moving average" in blob and "sample" in blob:
        return "ma_sample", "medium"
    if "linear" in blob and "reg" in blob:
        return "linreg", "medium"
    if "ribbon" in blob:
        return "ma_ribbon", "medium"
    if any(
        k in blob
        for k in (
            "dqn",
            "onlinelearner",
            "neural",
            "perceptron",
            "q-learning",
            "qlearning",
            "metalearning",
            "rl_",
            " mql5 rl",
            "randomforest",
            "autotradingbot",
            "pdf_multistrategy",
            "votingforest",
        )
    ):
        return "rl_proxy", "low"
    if "challenge" in blob or "s11_runner" in blob or "decisiontree" in blob or "ftmo_dt" in blob:
        return "challenge", "medium"
    if "momentum" in blob or "ftmo ultra" in blob or "simple scalper" in blob or "us30_expansion" in blob:
        return "momentum", "medium"
    if "rsi_bb_extreme" in blob or ("rsi" in blob and "bb" in blob):
        return "mark_rsi_bb", "medium"
    if "agent teacher" in blob:
        return "bb_mtf", "medium"
    if "ati_ftmo" in blob:
        return "challenge", "medium"
    if "cci" in blob:
        return "cci_gravity", "medium"
    if "section-" in blob or "new_trading_strategies" in blob:
        return "mark_rsi_bb", "medium"
    if "errorrate" in blob or "autogk" in blob or "slope_screener" in blob:
        return "ma_sample", "low"
    if "hurst" in blob:
        return "momentum", "low"
    if "swarm" in blob:
        return "cci_gravity", "low"
    if "crossent" in blob or "kmeans" in blob:
        return "linreg", "low"
    if "some bs" in blob or "some bullshit" in blob or "to opimize" in blob:
        return "rl_proxy", "low"

    # default scaffold
    return "mark_rsi_bb", "low"


def build_inventory() -> List[FamilySpec]:
    families: List[FamilySpec] = []
    seen: set[str] = set()

    for name, plat, summary in parse_mt_index():
        fid = f"mt__{_slug(name)}"
        # uniqueness
        base = fid
        n = 2
        while fid in seen:
            fid = f"{base}_{n}"
            n += 1
        seen.add(fid)
        profile, fidelity = pick_profile(name, summary)
        families.append(
            FamilySpec(
                family_id=fid,
                kind="mt",
                title=name,
                source=f"strategies/language/01_METATRADER_INDEX.md :: {name} ({plat})",
                adapter_profile=profile,
                fidelity=fidelity,
                collapses=[],
            )
        )

    for path in list_note_files():
        rel = path.relative_to(STRATEGIES).as_posix()
        fid = f"note__{_slug(rel)}"
        base = fid
        n = 2
        while fid in seen:
            fid = f"{base}_{n}"
            n += 1
        seen.add(fid)
        profile, fidelity = pick_profile(path.stem, path_hint=rel)
        families.append(
            FamilySpec(
                family_id=fid,
                kind="note",
                title=path.name,
                source=str(path),
                adapter_profile=profile,
                fidelity=fidelity,
                collapses=[],
            )
        )

    return families


def inventory_counts(families: List[FamilySpec] | None = None) -> dict:
    fams = families if families is not None else build_inventory()
    mt = sum(1 for f in fams if f.kind == "mt")
    notes = sum(1 for f in fams if f.kind == "note")
    collapses = sum(len(f.collapses) for f in fams)
    return {
        "mt_names": mt,
        "note_files": notes,
        "total_families": len(fams),
        "total_collapse_entries": collapses,
        "mt_index_parsed": len(parse_mt_index()),
        "note_files_listed": len(list_note_files()),
    }


def to_jsonable(families: List[FamilySpec]) -> list:
    return [asdict(f) for f in families]


if __name__ == "__main__":
    fams = build_inventory()
    c = inventory_counts(fams)
    print(c)
    assert c["total_collapse_entries"] == 0
    assert c["mt_names"] == c["mt_index_parsed"]
    assert c["note_files"] == c["note_files_listed"]
    assert c["total_families"] == c["mt_names"] + c["note_files"]
    print("OK", c["total_families"], "families 1:1")
