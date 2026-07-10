"""Save and load: schema-versioned JSON, validated at the boundary.

The save lives in $VESPER_HOME (default ~/.vesper). A corrupt or
foreign file raises SaveError with a message fit to show the player;
it never crashes the watch.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from engine.state import (
    ENDINGS,
    FINAL_WATCH,
    TENDABLES,
    GameState,
    JournalEntry,
)

SCHEMA = 1


class SaveError(Exception):
    """The save file exists but cannot be trusted."""


def save_dir() -> Path:
    override = os.environ.get("VESPER_HOME")
    if override:
        return Path(override)
    return Path.home() / ".vesper"


def save_path() -> Path:
    return save_dir() / "save.json"


def to_dict(state: GameState) -> dict:
    return {
        "schema": SCHEMA,
        "observer": state.observer,
        "watch": state.watch,
        "flags": sorted(state.flags),
        "journal": [[e.watch, e.text] for e in state.journal],
        "witnessed": sorted(state.witnessed),
        "tended": [[name, watch] for name, watch in state.tended],
        "generator_strikes": state.generator_strikes,
        "ending": state.ending,
    }


def from_dict(data: dict) -> GameState:
    if not isinstance(data, dict):
        raise SaveError("save file is not a record")
    if data.get("schema") != SCHEMA:
        raise SaveError(f"save schema {data.get('schema')!r} is not {SCHEMA}")
    try:
        observer = str(data["observer"])
        watch = int(data["watch"])
        flags = frozenset(str(f) for f in data["flags"])
        journal = tuple(
            JournalEntry(watch=int(w), text=str(t)) for w, t in data["journal"]
        )
        witnessed = frozenset(str(d) for d in data["witnessed"])
        tended = tuple((str(n), int(w)) for n, w in data["tended"])
        strikes = int(data["generator_strikes"])
        ending = data["ending"]
    except (KeyError, TypeError, ValueError) as exc:
        raise SaveError(f"save file is damaged: {exc}") from exc
    if not 1 <= watch <= FINAL_WATCH:
        raise SaveError(f"impossible watch number: {watch}")
    if {name for name, _ in tended} != set(TENDABLES):
        raise SaveError("save file lost track of the station")
    if ending is not None and ending not in ENDINGS:
        raise SaveError(f"unknown ending in save: {ending!r}")
    return GameState(
        observer=observer,
        watch=watch,
        flags=flags,
        journal=journal,
        witnessed=witnessed,
        tended=tended,
        generator_strikes=strikes,
        ending=str(ending) if ending is not None else None,
    )


def save(state: GameState) -> None:
    directory = save_dir()
    directory.mkdir(parents=True, exist_ok=True)
    tmp = save_path().with_suffix(".json.tmp")
    tmp.write_text(json.dumps(to_dict(state), indent=2), encoding="utf-8")
    tmp.replace(save_path())


def load() -> GameState | None:
    """Return the saved game, None if there is no save at all."""
    path = save_path()
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SaveError(f"save file is unreadable: {exc}") from exc
    return from_dict(data)


def delete() -> None:
    save_path().unlink(missing_ok=True)
