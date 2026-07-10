"""Game state: a frozen dataclass plus pure update functions.

Nothing here performs IO. Every "mutation" returns a new GameState, so
handlers can be tested by comparing values in and values out. All story
knowledge (what removals mean, when warnings fire) lives in content/;
this module only knows the shape of the facts.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

TENDABLES = ("GENERATOR", "CLOCK", "PLANT")
FINAL_WATCH = 7
GENERATOR_WARNING_FROM_WATCH = 4
GENERATOR_WARNING_AGE = 2  # watches since last tending before it complains
GENERATOR_FATAL_STRIKES = 2  # ignored-warning sleeps before the cold wins

ENDINGS = ("KEEPER", "QUIET", "ANSWER", "COLD", "OUTSIDE")


@dataclass(frozen=True)
class JournalEntry:
    watch: int
    text: str


@dataclass(frozen=True)
class GameState:
    observer: str = "OBSERVER"
    watch: int = 1
    flags: frozenset[str] = frozenset()
    journal: tuple[JournalEntry, ...] = field(default_factory=tuple)
    witnessed: frozenset[str] = frozenset()
    tended: tuple[tuple[str, int], ...] = (
        ("GENERATOR", 1),
        ("CLOCK", 1),
        ("PLANT", 1),
    )
    generator_strikes: int = 0
    ending: str | None = None


def new_game(observer: str) -> GameState:
    name = observer.strip() or "the observer"
    return GameState(observer=name)


def has_flag(state: GameState, flag: str) -> bool:
    return flag in state.flags


def add_flag(state: GameState, *flags: str) -> GameState:
    return replace(state, flags=state.flags | frozenset(flags))


def add_journal(state: GameState, text: str) -> GameState:
    entry = JournalEntry(watch=state.watch, text=text)
    return replace(state, journal=state.journal + (entry,))


def witness(state: GameState, designation: str) -> GameState:
    return replace(state, witnessed=state.witnessed | {designation})


def last_tended(state: GameState, thing: str) -> int:
    for name, watch in state.tended:
        if name == thing:
            return watch
    raise ValueError(f"unknown tendable: {thing}")


def tend(state: GameState, thing: str) -> GameState:
    if thing not in TENDABLES:
        raise ValueError(f"unknown tendable: {thing}")
    new_tended = tuple(
        (name, state.watch if name == thing else watch)
        for name, watch in state.tended
    )
    updated = replace(state, tended=new_tended)
    if thing == "GENERATOR":
        updated = replace(updated, generator_strikes=0)
    return updated


def generator_warning_active(state: GameState) -> bool:
    if state.watch < GENERATOR_WARNING_FROM_WATCH:
        return False
    age = state.watch - last_tended(state, "GENERATOR")
    return age >= GENERATOR_WARNING_AGE


def record_sleep_strikes(state: GameState) -> GameState:
    """Apply the generator's ignored-warning count at end of watch."""
    if generator_warning_active(state):
        return replace(state, generator_strikes=state.generator_strikes + 1)
    return replace(state, generator_strikes=0)


def generator_is_fatal(state: GameState) -> bool:
    return state.generator_strikes >= GENERATOR_FATAL_STRIKES


def next_watch(state: GameState) -> GameState:
    return replace(state, watch=state.watch + 1)


def set_ending(state: GameState, ending: str) -> GameState:
    if ending not in ENDINGS:
        raise ValueError(f"unknown ending: {ending}")
    return replace(state, ending=ending)
