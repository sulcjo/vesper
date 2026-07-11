"""Boot and sign-in: the station stands up, the observer sits down."""

from __future__ import annotations

from engine.io import IO

BOOT_LINES = (
    "VESPER STATION — SKY CATALOGUE AUTHORITY",
    "TERMINAL 1 OF 1",
    "",
    "POWER ................ GENERATOR (LOCAL)",
    "ARCHIVE .............. MOUNTED (READ DEGRADED)",
    "CATALOGUE ............ MOUNTED",
    "WIRE ................. LIVE",
    "BUREAU LINK .......... OPEN (LAST INBOUND: 214 EPOCHS)",
    "DOME ................. SEALED",
    "",
)


def boot(io: IO) -> None:
    for line in BOOT_LINES:
        io.say(line, "os")
    io.pause(0.4)


_ENDING_PHRASES = {
    "KEEPER": "watch closed in good order",
    "QUIET": "no report on file",
    "ANSWER": "the count is right",
    "COLD": "temperature out of range",
    "OUTSIDE": "no entry",
}


def sign_in(io: IO, ledger: list[dict] | None = None) -> str:
    io.say("the sign-in book is paper. it predates the terminal, and "
           "every keeper has signed it at the top of every watch, in "
           "ink, because the first duty of the watch is to say who is "
           "keeping it.", "dim")
    ledger = ledger or []
    if ledger:
        io.say("SIGN-IN BOOK — LAST PAGES:", "os")
        for run in ledger[-5:]:
            phrase = _ENDING_PHRASES.get(run["ending"], "no entry")
            io.say(f"  {run['name'].upper():<14} — {phrase}", "os")
    name = io.ask("sign-in ▸ ").strip()
    io.say("", "os")
    shown = (name or "the observer").upper()
    if any(run["name"].strip().upper() == shown for run in ledger):
        io.say("the name is already in the book, some pages up, in "
               "your handwriting. the hand that signed that line was "
               "steadier than yours is tonight. you have never signed "
               "this book before.", "dim")
    io.say(f"OBSERVER OF RECORD: {shown}", "os")
    io.say("THE WATCH IS YOURS.", "os")
    return name


def welcome_back(io: IO, observer: str, watch: int) -> None:
    io.say(f"SAVED WATCH FOUND — OBSERVER {observer.upper()}, "
           f"WATCH {watch}.", "os")
    io.say("the sign-in book lies open where you left it. the ink of "
           "your last entry has dried to the colour of everything "
           "else.", "dim")
