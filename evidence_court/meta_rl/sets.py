"""MARK SETS LAW pin — additive copy for Court package; must match mark_here law."""
from __future__ import annotations

from typing import List, Sequence, Tuple

from .types import OfficialSet, SubSet

# LTF first; HTF last two — immutable without MARK_SETS_LAW.md rewrite
MARK_SETS_LAW: Tuple[Tuple[int, str, str, Tuple[str, str]], ...] = (
    (1, "micro", "1m", ("15m", "30m")),
    (2, "intraday", "5m", ("30m", "1h")),
    (3, "swing", "15m", ("1h", "4h")),
    (4, "macro", "30m", ("4h", "1d")),
)

OFFICIAL_SETS: Tuple[OfficialSet, ...] = tuple(
    OfficialSet(sid, name, ltf, htfs) for sid, name, ltf, htfs in MARK_SETS_LAW
)

SUB_SETS: Tuple[SubSet, ...] = (
    SubSet("A", "1m", "5m"),
    SubSet("B", "5m", "15m"),
    SubSet("C", "15m", "30m"),
    SubSet("D", "1h", "4h"),
    SubSet("E", "4h", "1d"),
)


def mark_sets_law_table() -> List[dict]:
    return [
        {
            "set_id": s.set_id,
            "name": s.name,
            "ltf_entry": s.entry_tf,
            "htf_confirm": list(s.confirmation_tfs),
            "stack": list(s.tfs),
        }
        for s in OFFICIAL_SETS
    ]


def assert_mark_sets_law(
    stacks: Sequence[Tuple[str, str, str]] | None = None,
) -> None:
    expected = [
        ("1m", "15m", "30m"),
        ("5m", "30m", "1h"),
        ("15m", "1h", "4h"),
        ("30m", "4h", "1d"),
    ]
    if stacks is None:
        stacks = [s.tfs for s in OFFICIAL_SETS]
    got = [tuple(x) for x in stacks]
    if len(got) != 4:
        raise AssertionError(f"MARK SETS LAW requires 4 sets, got {len(got)}")
    for i, (e, g) in enumerate(zip(expected, got), start=1):
        if e != g:
            raise AssertionError(
                f"MARK SETS LAW broken on set {i}: expected {e}, got {g}"
            )


assert_mark_sets_law()
