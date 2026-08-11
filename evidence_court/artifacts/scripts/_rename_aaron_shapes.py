"""Rename Aaron curriculum Load/Reclaim identifiers → pullback/continuation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

GLOBAL = [
    ("aaron_flr_from_senses", "aaron_force_state_from_senses"),
    ("reclaim_heavy", "continuation_heavy"),
    ("load_wait_steps", "pullback_wait_steps"),
    ("reclaim_fire_steps", "continuation_fire_steps"),
    ("load_wait", "pullback_wait"),
    ("reclaim_fire", "continuation_fire"),
    ("fire_on_load", "fire_on_pullback"),
    ("load_building_not_reclaim", "pullback_building_not_continuation"),
    ("slingshot_load_wait", "slingshot_pullback_wait"),
    ("not_reclaim_or_taste_block", "not_continuation_or_taste_block"),
    ("reclaim_with_force_fire", "continuation_with_force_fire"),
    ("reclaim_ok", "continuation_ok"),
    ("AARON_FLR_REASON", "AARON_FORCE_STATE"),
]

EXTRA = [
    (
        "Aaron FLR process curriculum",
        "Aaron Force + LTF state curriculum",
    ),
    (
        "Force (permission) → Load (wait tension) → Reclaim (fire with Force)",
        "Force (2 HTFs agree) → LTF state (pullback / continuation / calibrating)",
    ),
    (
        "Method-first rewards/penalties from Aaron_here/AARON.md §3.7–3.11.",
        "**Forbidden language:** Load / Reclaim. Method-first rewards from Aaron_here/AARON.md.",
    ),
    (
        "Map living sense pack → FLR process label",
        "Map living sense pack → Force+state process label",
    ),
    (
        "Force = multi-set consensus side.\n    Load = tension / slingshot without launch.\n"
        "    Reclaim = launch/release/continuation with Force + allow_fire.\n"
        "    Hold (Aaron t4) = mid-progress + Force still live + reclaim path → re-commit same side\n"
        "    (do **not** reverse / scratch a winner while Force holds).",
        "Force = multi-set consensus side (proxy for dual HTF agree).\n"
        "    Pullback = tension / slingshot without launch → WAIT.\n"
        "    Continuation = launch/release/continuation with Force → preferred FIRE.\n"
        "    Hold (scalper) = mid-progress + Force live + continuation → re-commit same side.",
    ),
    ("Load building, no launch → wait (Load ≠ fire)", "Pullback building, no launch → wait (pullback ≠ fire)"),
    ("without reclaim shape", "without continuation shape"),
    ("prefer reclaim fire", "prefer continuation fire"),
    ("Reclaim with Force → fire", "Continuation with Force → fire"),
    ("if reclaim would be valid", "if continuation would be valid"),
    ("until reclaim;", "until continuation;"),
    ("Synthetic FLR episode", "Synthetic Force+state episode"),
    ("Force + Load bottom", "Force + pullback bottom"),
    ("cont/reclaim", "continuation"),
    ("correct FLR *process*", "correct Force+state *process*"),
    (
        "Force-wait → Load-wait → Reclaim-fire → mixed.",
        "Force-wait → pullback-wait → continuation-fire → mixed.",
    ),
    (
        "Force → Load → Reclaim → **Hold while Force**\n"
        "    → exit when Force dies + dip-chase / thrash **penalties** (AARON.md §3.7–3.11).",
        "Force → pullback → continuation → hold while Force\n"
        "    → exit when Force dies + dip-chase / thrash penalties (AARON.md).",
    ),
    ("almost all reclaim_fire", "almost all continuation_fire"),
    (
        "Aaron curriculum stages 1–5 method-rich (hold is stage after reclaim)",
        "Aaron curriculum stages 1–5 method-rich (hold is stage after continuation)",
    ),
    (
        "# Force 12% · Load+dip 15% · Reclaim 28% · Hold 28% · Exit/penalty 10% · mixed 7%",
        "# Force 12% · pullback+dip 15% · continuation 28% · Hold 28% · Exit/penalty 10% · mixed 7%",
    ),
    ("Aaron FLR reason curriculum pins", "Aaron Force+state curriculum pins"),
    ("process shapes, not copy-only.", "process shapes (pullback/continuation), not copy-only."),
    ("def test_load_wait_not_fire", "def test_pullback_wait_not_fire"),
    ("def test_reclaim_heavy_curriculum_prefers_fire_shapes", "def test_continuation_heavy_curriculum_prefers_fire_shapes"),
]

FILES = [
    "evidence_court/meta_rl/aaron_reason_curriculum.py",
    "evidence_court/tests/test_aaron_reason_curriculum.py",
    "evidence_court/meta_rl/train_aaron_reason.py",
    "evidence_court/meta_rl/train_aaron_method_hold.py",
    "evidence_court/meta_rl/train_day12_until_pass.py",
]


def main() -> None:
    for fp in FILES:
        p = ROOT / fp
        if not p.exists():
            print("MISS", fp)
            continue
        t = p.read_text(encoding="utf-8")
        old = t
        for a, b in GLOBAL:
            t = t.replace(a, b)
        for a, b in EXTRA:
            t = t.replace(a, b)
        if "def aaron_force_state_from_senses" in t and "aaron_flr_from_senses = aaron_force_state_from_senses" not in t:
            if not t.endswith("\n"):
                t += "\n"
            t += "\n# Deprecated alias (old name)\naaron_flr_from_senses = aaron_force_state_from_senses\n"
        if t != old:
            p.write_text(t, encoding="utf-8")
            print("PATCHED", fp)
        else:
            print("NOCHANGE", fp)
        for w in ("load_wait", "reclaim_fire", "reclaim_heavy", "fire_on_load"):
            if w in t:
                print("  leftover", w)


if __name__ == "__main__":
    main()
