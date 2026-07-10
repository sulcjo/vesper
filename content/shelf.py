"""SHELF — the old keepers' volumes, the station's deliberate memory.

Four keepers came before: Remy, who began the watch; Sever, who built
what keeps it; Okonkwo, who taught what it is for; Weir, who died in
the chair. Their journals are the game's world told sideways — the
history of the sky's long evening, in the hands of the people who
counted it.
"""

from __future__ import annotations

from engine import state as st
from engine.io import IO
from engine.state import GameState

KEEPERS = ("REMY", "SEVER", "OKONKWO", "WEIR")


def open_shelf(state: GameState, which: str, io: IO) -> GameState:
    which = which.strip().upper()
    if not which:
        io.say("THE SHELF — KEEPERS' VOLUMES, IN ORDER OF WATCH:", "os")
        io.say("  REMY       first keeper. began the catalogue.", "os")
        io.say("  SEVER      second. built the synthesiser; measured "
               "everything.", "os")
        io.say("  OKONKWO    third. the last to speak with the "
               "enclaves.", "os")
        io.say("  WEIR       fourth. died in the dome chair, "
               "mid-count.", "os")
        io.say("SHELF <NAME> TO TAKE A VOLUME DOWN.", "os")
        io.say("your own stands unfinished in the drawer, which is "
               "where a living keeper's belongs.", "dim")
        return state
    if which not in KEEPERS:
        io.say(f"SHELF: NO SUCH VOLUME — {which}", "os")
        io.say("five keepers, four volumes, one drawer. the shelf has "
               "never needed to be longer, which is its own kind of "
               "record.", "dim")
        return state
    _VOLUMES[which](state, io)
    return st.add_flag(state, f"READ_{which}")


def _remy(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("VOLUME I — REMY. THE HAND IS UPRIGHT, THE INK GONE "
           "BROWN.", "os")
    io.say("the first pages are administration: the Bureau's founding "
           "writ, the station's consecration — his word — and the "
           "reason, set down once and never repeated: 'the enclaves "
           "have turned their lamps inward. someone must sit where "
           "the lamps face out. the sky is old and owed an audience "
           "at its going.'")
    io.say("later, this, undated: 'a man asked me at the founding "
           "what the watch was FOR, what use a count nobody reads. "
           "i said: when a thing cannot be saved, it can still be "
           "attended. he did not take the post. i did.'")
    io.say("and on the last written page, alone: 'the old books say "
           "the far rim of the sky was richer once, before the "
           "oldest catalogues. the old books disagree with each "
           "other by too much. i have decided not to have an "
           "opinion. opinions are for the Bureau. i will keep the "
           "count.'", "dim")
    io.say("the margin of the flyleaf holds the four words, first of "
           "all their sayings: STILL THERE. STILL HERE.", "dim")


def _sever(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("VOLUME II — SEVER. DRAUGHTSMAN'S BLOCK CAPITALS, "
           "DIAGRAMS ON EVERY THIRD PAGE.", "os")
    io.say("Sever inherited a station dying of its own boilers and "
           "rebuilt it from the ground it stands on: the synthesiser, "
           "the corridor lights, the undercroft, the second heart "
           "and then the third. his entries are bills of work. "
           "'EPOCH 41,220. RETIRED THE FIRST HEART WITH HONOURS. A "
           "MACHINE THAT HAS KEPT MEN ALIVE IS OWED A NOUN.'")
    io.say("once, only once, the block capitals fail into ordinary "
           "hand, small: 'measured the corridor again tonight. forty "
           "paces. i measure it because it stays. everything i left "
           "below the scarp has not. a man needs one number that "
           "stays.'")
    io.say("the last diagram in the volume is the tether anchor at "
           "the array, triple-checked, annotated in red: 'RATED FOR "
           "TEN TIMES A KEEPER. THE DOOR IS HONEST. BE CERTAIN THE "
           "KEEPER IS.'", "dim")


def _okonkwo(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("VOLUME III — OKONKWO. A LONG FORWARD HAND, LIKE A MAN "
           "WALKING INTO WIND.", "os")
    io.say("his watch was the leaving-time. four beacons on the wire "
           "when it began; the Hollow Hill loop alone at the end, "
           "and the towns below the scarp gone quiet one by one — "
           "'not fallen,' he writes, 'furled. they have voted, "
           "hearth by hearth, that the past is more comfortable "
           "than the future, and they are living in it. i do not "
           "blame them. i log them. those are different duties.'")
    io.say("'the shuttle did not come at epoch 63,300. nor 63,400. "
           "i will hold the door. a kept schedule is a lamp in a "
           "window: it is not for the keeper. it is for whoever is "
           "still out there deciding whether to come home.'")
    io.say("and near the end, to his successor, to you: 'the "
           "instrument is the station; the observer is the "
           "instrument's conscience. when the count grows strange — "
           "it will, boy, everything old grows strange — remember "
           "that a conscience is not asked to explain. it is asked "
           "to be present.'", "dim")


def _weir(state: GameState, io: IO) -> None:
    io.say("VOLUME IV — WEIR. SMALL EXACT LETTERS, NO WASTED "
           "STROKES.", "os")
    io.say("Weir's volume is the cleanest science on the shelf: "
           "seeing conditions, instrument drift, a decade-long study "
           "of the ember spectra done with tools two centuries past "
           "calibration. she trusted nothing she had not measured "
           "twice, including herself. 'the eye ages. i have begun "
           "logging my own error alongside the instrument's. both "
           "grow. the count must outlive our vanities.'")
    io.say("one entry breaks the ruled lines — it is written across "
           "them, diagonal, the only disorder in four hundred pages: "
           "'E. carved our letters into the chair arm today. i let "
           "her. the inventory can object when the inventory has "
           "sat forty years in the cold with someone worth carving "
           "letters with.'")
    if state.watch >= 6:
        io.say("you never found out who E. was to her, whose other "
               "initial shares the chair arm with hers. the volume "
               "does not say. tonight, with your own names going, "
               "that reticence reads less like privacy and more like "
               "prophecy: she kept the letters where paper could "
               "not lose them.", "dim")
    io.say("the final page is not in her hand. it is the Bureau's "
           "form, RELIEF OF WATCH, filled in by you, forty years "
           "ago, your signature young and careful. cause: ORDERLY. "
           "effects shipped: NONE. remarks: THE COUNT WAS CURRENT "
           "TO THE HOUR OF DEATH.", "dim")


_VOLUMES = {
    "REMY": _remy,
    "SEVER": _sever,
    "OKONKWO": _okonkwo,
    "WEIR": _weir,
}
