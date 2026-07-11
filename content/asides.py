"""Asides: the small human verbs HELP never mentions, and the varied
voices the terminal uses when asked things it cannot do twice.

None of these cost the night. They are rests, not acts — the game's
way of rewarding a player who treats the keeper as a person.
"""

from __future__ import annotations

from engine import state as st
from engine.io import IO
from engine.state import GameState

ASIDE_VERBS = ("TEA", "SIT", "HUM", "SING", "HELLO", "HI", "PRAY",
               "WAIT", "THANKS", "THANK", "XYZZY")


def _pick(state: GameState, variants: tuple[str, ...], salt: int = 0) -> str:
    index = (state.watch * 3 + state.acts + salt) % len(variants)
    return variants[index]


# ── the terminal's voices for the unaskable ──────────────────────────

_UNKNOWN = (
    "the terminal has never pretended to understand more than it "
    "understands. HELP lists what it does.",
    "the cursor blinks at it, twice, and lets it go. the boards are "
    "listed under HELP.",
    "whatever that was, the station has no circuit for it. neither, "
    "on reflection, do you.",
    "you read it back off the screen and are not sure you meant it "
    "either. HELP, if the night is getting long.",
)


def unknown_line(state: GameState, cmd: str) -> str:
    return _pick(state, _UNKNOWN, salt=len(cmd))


_LISTEN_AGAIN = (
    "the wire gives tonight what it gave. more listening will not "
    "make the sky say it twice.",
    "hiss, and under the hiss, nothing new. you close the band gently, "
    "like a door on a sleeping room.",
)


def listen_again(state: GameState, io: IO) -> GameState:
    io.say("WIRE: OPEN.", "os")
    if state.watch >= 9 and st.has_flag(state, "QUESTION_ASKED"):
        io.say("WIRE: CHANNEL HELD OPEN. IT IS STILL WAITING.", "alert")
        return state
    io.say(_pick(state, _LISTEN_AGAIN), "dim")
    return state


_TEND_AGAIN = (
    "you tended it this watch already. even kindness has a dosage.",
    "it is seen to. hovering is not maintenance, whatever it feels "
    "like tonight.",
)


def tend_again(state: GameState, thing: str, io: IO) -> GameState:
    io.say(f"{thing}: NOMINAL. SERVICED THIS WATCH.", "os")
    io.say(_pick(state, _TEND_AGAIN, salt=len(thing)), "dim")
    return state


_WALK_AGAIN = (
    "you were here an hour ago. the room holds its shape, which is "
    "the whole of what you came to check.",
    "nothing has moved. in most houses that goes without saying. you "
    "no longer live in most houses.",
    "the second visit is shorter. rooms, like people, say the "
    "important thing first.",
)


def walk_again(state: GameState, place: str, io: IO) -> GameState:
    io.say(_pick(state, _WALK_AGAIN, salt=len(place)), "dim")
    return state


# ── the unlisted verbs ────────────────────────────────────────────────

def aside(state: GameState, verb: str, io: IO) -> GameState:
    handler = _ASIDES[verb]
    return handler(state, io)


def _tea(state: GameState, io: IO) -> GameState:
    flag = f"TEA_{state.watch}"
    if st.has_flag(state, flag):
        io.say("the tin is only so deep, and the night is only so "
               "long. one cup a watch. rules are what a man has "
               "instead of company.", "dim")
        return state
    io.say("you put the kettle on for the pleasure of the argument it "
           "makes — the knocking, the sulk, the sudden agreement of "
           "the boil. tea the colour of rust, drunk with both hands "
           "around the cup. for the length of it, the station is just "
           "a kitchen, very far north of everything.")
    return st.add_flag(state, flag)


def _sit(state: GameState, io: IO) -> GameState:
    if state.watch >= 7:
        io.say("you sit and do nothing, which by this point in the "
               "tour is a discipline and not a lapse. the chair takes "
               "your weight the way it has taken every keeper's. the "
               "station goes on around you, tick and pulse and hum, "
               "a body breathing with you in it.")
    else:
        io.say("you sit. the chair creaks its one syllable. for a few "
               "minutes you let the station do the watching — it has "
               "the instruments for it, after all, and you built "
               "nothing tonight by standing.")
    return state


def _hum(state: GameState, io: IO) -> GameState:
    io.say("you hum a few bars of something whose name went wherever "
           "names go — a tune your hands remember from a kitchen, or "
           "a pier, or a grammar-book language. the dome gives it "
           "back a half-second late and a shade deeper, and for that "
           "half-second there are two of you, and the other one has "
           "a better voice.")
    return state


def _hello(state: GameState, io: IO) -> GameState:
    io.say("ACKNOWLEDGED.", "os")
    io.say("the terminal answers the way it answers everything — "
           "promptly, and without warmth, and after forty years you "
           "would not have the warmth if it offered. constancy is "
           "the better gift.", "dim")
    return state


def _pray(state: GameState, io: IO) -> GameState:
    io.say("you are not a praying man. Remy was, the volume says — "
           "he prayed at the top of every watch, to whom it does not "
           "record. you stand a moment with your hands still and your "
           "head down, in the general direction of whatever Remy "
           "found on the other end, and if it is listening, it knows "
           "a kept watch when it sees one.")
    return state


def _wait(state: GameState, io: IO) -> GameState:
    io.pause(1.2)
    io.say("you wait. the clock spends its seconds one at a time, "
           "openly, the only honest banker left. nothing happens, "
           "which — you remind yourself — is the good outcome, the "
           "one the whole station is built to notice the end of.")
    return state


def _xyzzy(state: GameState, io: IO) -> GameState:
    io.say("NOTHING HAPPENS.", "os")
    io.say("an old, old word — older than the station, the manual "
           "says nothing about it, and yet every terminal you have "
           "ever met has known to say that. some rituals outlive "
           "their magic. you, of all people, respect that.", "dim")
    return state


_ASIDES = {
    "TEA": _tea,
    "SIT": _sit,
    "HUM": _hum,
    "SING": _hum,
    "HELLO": _hello,
    "HI": _hello,
    "PRAY": _pray,
    "WAIT": _wait,
    "THANKS": _hello,
    "THANK": _hello,
    "XYZZY": _xyzzy,
}
