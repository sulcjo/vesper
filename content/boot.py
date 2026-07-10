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


def sign_in(io: IO) -> str:
    io.say("the sign-in book is paper. it predates the terminal, and "
           "every keeper has signed it at the top of every watch, in "
           "ink, because the first duty of the watch is to say who is "
           "keeping it.", "dim")
    name = io.ask("sign-in ▸ ").strip()
    io.say("", "os")
    io.say(f"OBSERVER OF RECORD: {(name or 'the observer').upper()}", "os")
    io.say("THE WATCH IS YOURS.", "os")
    return name


def welcome_back(io: IO, observer: str, watch: int) -> None:
    io.say(f"SAVED WATCH FOUND — OBSERVER {observer.upper()}, "
           f"WATCH {watch}.", "os")
    io.say("the sign-in book lies open where you left it. the ink of "
           "your last entry has dried to the colour of everything "
           "else.", "dim")
