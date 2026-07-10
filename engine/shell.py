"""The main loop: boot, sign-in, the watches, and the going down.

This is the only module that touches the real terminal (through term)
and the save file. Everything it orchestrates is testable without it.
"""

from __future__ import annotations

from content import boot as boot_content, endings, watches
from engine import commands, persistence, state as st, term
from engine.io import IO
from engine.state import FINAL_WATCH, GameState

_KIND_STYLE = {
    "os": ((term.Style.GREEN,), 0.003),
    "prose": ((), term.CHAR_DELAY),
    "dim": ((term.Style.DIM,), term.CHAR_DELAY),
    "alert": ((term.Style.AMBER, term.Style.BOLD), term.CHAR_DELAY),
}


class TerminalIO:
    def say(self, text: str, kind: str = "prose") -> None:
        styles, pace = _KIND_STYLE.get(kind, _KIND_STYLE["prose"])
        term.say(text, *styles, pace=pace)

    def ask(self, prompt: str) -> str:
        try:
            return input(term.paint(prompt, term.Style.GREEN))
        except EOFError:
            return "QUIT"
        except KeyboardInterrupt:
            print()
            self.say("(QUIT leaves the terminal; the watch is saved.)",
                     "dim")
            return ""

    def art(self, lines: list[str]) -> None:
        for line in lines:
            print(term.paint(line, term.Style.GREEN))

    def pause(self, seconds: float = 0.35) -> None:
        term.beat(seconds)


def advance_after_sleep(state: GameState, io: IO) -> GameState:
    """Everything that happens between SLEEP and the next waking."""
    state = st.record_sleep_strikes(state)
    if st.generator_is_fatal(state):
        return st.set_ending(state, "COLD")
    if state.watch >= FINAL_WATCH:
        if st.has_flag(state, f"REPORTED_{FINAL_WATCH}"):
            return st.set_ending(state, "KEEPER")
        return st.set_ending(state, "QUIET")
    watches.close(state, io)
    state = st.next_watch(state)
    return watches.wake(state, io)


def _start(io: IO, fresh: bool) -> GameState | None:
    if not fresh:
        try:
            saved = persistence.load()
        except persistence.SaveError as error:
            io.say(f"SAVE FILE REJECTED: {error}", "alert")
            io.say("the sign-in book, at least, does not corrupt. "
                   "beginning a new watch.", "dim")
            saved = None
        if saved is not None and saved.ending is None:
            boot_content.welcome_back(io, saved.observer, saved.watch)
            return watches.wake(saved, io)
    boot_content.boot(io)
    name = boot_content.sign_in(io)
    state = st.new_game(name)
    return watches.wake(state, io)


def run(argv: list[str]) -> int:
    if "--fast" in argv:
        term.set_fast(True)
    fresh = "--new" in argv
    io = TerminalIO()
    state = _start(io, fresh)
    if state is None:
        return 1

    while True:
        persistence.save(state)
        line = io.ask(f"\nW{state.watch} ▸ ")
        state, signal = commands.dispatch(state, line, io)
        if signal == "quit":
            persistence.save(state)
            io.say("the terminal dims to its standing glow. the watch "
                   "waits where you left it.", "dim")
            return 0
        if signal == "sleep":
            state = advance_after_sleep(state, io)
        if state.ending is not None:
            endings.play(state, io)
            persistence.delete()
            io.say("(a new watch begins with: python3 vesper.py)", "dim")
            return 0
