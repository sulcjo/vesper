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

SCHEMA = 2
ACCEPTED_SCHEMAS = (1, 2)  # 1 lacks acts/final_words/superseded
LEDGER_SCHEMA = 1


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
        "journal": [[e.watch, e.text, e.superseded] for e in state.journal],
        "witnessed": sorted(state.witnessed),
        "tended": [[name, watch] for name, watch in state.tended],
        "generator_strikes": state.generator_strikes,
        "acts": state.acts,
        "final_words": state.final_words,
        "ending": state.ending,
    }


def from_dict(data: dict) -> GameState:
    if not isinstance(data, dict):
        raise SaveError("save file is not a record")
    if data.get("schema") not in ACCEPTED_SCHEMAS:
        raise SaveError(f"save schema {data.get('schema')!r} is not {SCHEMA}")
    try:
        observer = str(data["observer"])
        watch = int(data["watch"])
        flags = frozenset(str(f) for f in data["flags"])
        journal = tuple(
            JournalEntry(watch=int(row[0]), text=str(row[1]),
                         superseded=bool(row[2]) if len(row) > 2 else False)
            for row in data["journal"]
        )
        witnessed = frozenset(str(d) for d in data["witnessed"])
        tended = tuple((str(n), int(w)) for n, w in data["tended"])
        strikes = int(data["generator_strikes"])
        acts = int(data.get("acts", 0))
        final_words = str(data.get("final_words", ""))
        ending = data["ending"]
    except (KeyError, TypeError, ValueError, IndexError) as exc:
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
        acts=acts,
        final_words=final_words,
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


# ── the ledger: every watch this terminal has ever seen end ──────────

def ledger_path() -> Path:
    return save_dir() / "ledger.json"


def load_ledger() -> list[dict]:
    """Past runs, oldest first. A missing or damaged ledger is simply
    an empty book — the legacy feature must never break a fresh game."""
    path = ledger_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema") != LEDGER_SCHEMA:
            return []
        runs = []
        for run in data.get("runs", []):
            runs.append({
                "name": str(run["name"]),
                "ending": str(run["ending"]),
                "watch": int(run["watch"]),
            })
        return runs
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        return []


def append_ledger(name: str, ending: str, watch: int) -> None:
    runs = load_ledger()
    runs.append({"name": name, "ending": ending, "watch": watch})
    directory = save_dir()
    directory.mkdir(parents=True, exist_ok=True)
    tmp = ledger_path().with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps({"schema": LEDGER_SCHEMA, "runs": runs}, indent=2),
        encoding="utf-8",
    )
    tmp.replace(ledger_path())
