"""The keepsake: a paper record of the watch, left behind for the
player when a run ends. Composed here, written to disk by persistence.

It holds what the player actually wrote and did — the true, unfaded
text. Whatever the game did to those words on screen, the keepsake
keeps them whole. That asymmetry is the point.
"""

from __future__ import annotations

from content import reports, shelf
from engine import state as st
from engine.state import GameState

_ENDING_LINES = {
    "KEEPER": "the watch was closed in good order.",
    "QUIET": "no final report is on file.",
    "ANSWER": "the count is right.",
    "COLD": "station temperature went out of range.",
    "OUTSIDE": "the outer door was open at epoch change.",
}

_RULE = "─" * 62


def compose(state: GameState) -> str:
    lines: list[str] = []
    lines.append(_RULE)
    lines.append("VESPER STATION — RECORD OF A WATCH")
    lines.append(f"observer of record: {state.observer}")
    lines.append(f"final epoch: {reports.epoch(state):,} "
                 f"(watch {state.watch})")
    lines.append(_ENDING_LINES.get(state.ending or "", "the record ends."))
    lines.append(_RULE)
    lines.append("")

    if state.journal:
        lines.append("the journal, in the keeper's own hand, complete —")
        lines.append("every page ever written, including the ones he "
                     "re-copied. paper keeps what it was given:")
        lines.append("")
        for entry in state.journal:
            lines.append(f"  watch {entry.watch}:")
            lines.append(f"    {entry.text}")
            lines.append("")
    else:
        lines.append("the journal was never written in. blank is also "
                     "a record.")
        lines.append("")

    if state.witnessed:
        lines.append(f"designations annotated by eye, {len(state.witnessed)} "
                     "in all:")
        lines.append("  " + ", ".join(sorted(state.witnessed)))
        lines.append("")

    volumes = [k.title() for k in shelf.KEEPERS
               if st.has_flag(state, f"READ_{k}")]
    if volumes:
        lines.append("volumes taken down from the shelf: "
                     + ", ".join(volumes) + ".")
        lines.append("")

    lines.append(_RULE)
    lines.append("whatever else happened, somebody looked.")
    lines.append(_RULE)
    return "\n".join(lines) + "\n"
