"""WALK — the station, five rooms and a door that should stay shut.

The observer's interiority lives in these scenes. They change with the
watch: early is routine, middle is unease, late is a man deciding, room
by room, what he is prepared to lose.
"""

from __future__ import annotations

from engine import state as st
from engine.io import IO
from engine.state import GameState

PLACES = ("DOME", "CORRIDOR", "QUARTERS", "PLANT", "GENERATOR")


def _band(watch: int) -> str:
    if watch <= 2:
        return "early"
    if watch <= 5:
        return "mid"
    return "late"


def walk(state: GameState, place: str, io: IO) -> GameState:
    place = place.strip().upper()
    if place in ("PLANT ROOM",):
        place = "PLANT"
    if place not in PLACES:
        io.say(f"WALK: NO SUCH PLACE — {place or '(NOWHERE)'}", "os")
        io.say("dome, corridor, quarters, plant room, generator room. "
               "the whole of the indoors. it used to feel small.", "dim")
        return state
    _SCENES[place][_band(state.watch)](state, io)
    return state


# ── dome ──────────────────────────────────────────────────────────────

def _dome_early(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("the dome smells of cold brass and machine oil. the chair "
           "knows your shape; it should, it has had forty years to "
           "learn it. on the arm, half under your sleeve, are the "
           "initials E.W., cut with a pocket knife by a woman who is "
           "now a star's name and nothing else.")
    io.say("you rest your fingers on the letters, once, the way you "
           "touch a railing on a stair you trust.", "dim")


def _dome_mid(state: GameState, io: IO) -> None:
    io.say("the shutter is closed and the dome is a held breath. you "
           "can hear the grease cooling in the gears. through the vent, "
           "very far off, the generator keeps its pulse.")
    if state.watch >= 4:
        io.say("you notice you have started standing so that the "
               "eyepiece is between you and the east wall. the noticing "
               "is worse than the standing.", "dim")


def _dome_late(state: GameState, io: IO) -> None:
    io.say("the dome at the end of things. the chair, the tube, the "
           "brass circle of the shutter crank worn bright as a coin. "
           "every keeper who ever sat here is in the smoothness of "
           "that crank. you put your hand on it and all of them are "
           "briefly not gone.")
    if st.has_flag(state, "SAW_THE_OTHER"):
        io.say("you do not open the shutter. once was once.", "dim")


# ── corridor ──────────────────────────────────────────────────────────

def _corridor_early(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("forty paces of corridor, lit in sections that wake ahead of "
           "you and time out behind. walking it, you are always in one "
           "moving island of light. behind you, in the dark, is the "
           "rest of the human race. you have made this joke to yourself "
           "for forty years. it has stopped being a joke so gradually "
           "you cannot date the change.")


def _corridor_mid(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("tonight you stop halfway and stand still until the light "
           "over your head gives up and clicks off, just to prove that "
           "the dark that arrives is your own ordinary dark, with your "
           "own heart in it and the far hum of the generator. it is. "
           "you stand in it a moment longer anyway, on principle, "
           "though you could not say which principle.")


def _corridor_late(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("the lights wake ahead of you as they always have. you find "
           "you are grateful to them, individually, each one, the way "
           "you would be grateful to old dogs standing up one more "
           "time. everything that still works is a kept promise now, "
           "and the corridor is forty paces of kept promises.")


# ── quarters ──────────────────────────────────────────────────────────

def _quarters_early(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("cot, chest, kettle, clock. the dent in the pillow is the "
           "truest record on the station: proof of ten thousand sleeps, "
           "unfalsifiable, in a medium the archive cannot reach.")
    io.say("you make tea. the tin is down to dust and stems, and you "
           "make it anyway, because the kettle's rattle is one of the "
           "voices you still get to hear.", "dim")


def _quarters_mid(state: GameState, io: IO) -> None:
    io.say("in the chest, under the spare filters, there is a "
           "photograph. two people on a pier that no longer exists, "
           "over water that no longer exists, squinting into a sun that "
           "is a red coal now if it is anything. one of them is you.")
    if state.watch >= 5:
        io.say("you know the other face better than your own. you knew "
               "the name last watch. you put the photograph back face "
               "down, which is not the same as forgetting, whatever "
               "the archive would make of it.", "dim")
    else:
        io.say("you say the other name out loud, once, into the quiet, "
               "like putting a coin in a jar against the dark to come.",
               "dim")


def _quarters_late(state: GameState, io: IO) -> None:
    io.say("you take the photograph out and prop it against the clock, "
           "faces out, deliberately. if the east wants the pier and the "
           "water and the sun and the name, let it come through the "
           "tick of an honest clock to take them.")
    if state.journal:
        io.say("the journal lies where it always lies. you have kept it "
               "since your first watch. whatever else is decided this "
               "epoch, it was written by a hand, and the hand was "
               "yours.", "dim")


# ── plant room ────────────────────────────────────────────────────────

def _plant_early(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("the plant room is two lamps, a jar, and the only green in "
           "four light-decades. the manual calls it a psychological "
           "provision. the manual has never stood in here at 0300 with "
           "its face in the leaves, breathing.")


def _plant_mid(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("condensation runs the jar in slow beads. the plant does not "
           "know about the catalogue. things keep needing water; this "
           "is, as far as you can tell, the universe's one remaining "
           "opinion, and you have decided to share it.")


def _plant_late(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("you have moved the second chair in here — Weir's chair, by "
           "the inventory, though she never sat in it that you know of. "
           "you sit with the plant the way you would sit with a "
           "colleague on a hard night: no talk expected, both facing "
           "the lamp, as if it were weather.")


# ── generator room ────────────────────────────────────────────────────

def _generator_early(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("warm, loud, honest. the generator room is the one place on "
           "the station where the dark has to shout to be heard. you "
           "check the fuel figure against the ledger, an arithmetic "
           "you could do dead, and may.")


def _generator_mid(state: GameState, io: IO) -> None:
    if st.generator_warning_active(state):
        io.say("you can hear it from the doorway: a stumble in the "
               "rotation, a held breath where a beat should be. it is "
               "asking. machines this old only ask so many times.",
               "alert")
    else:
        io.say("the pulse is steady. you stand a while in the heat and "
               "the noise, taking it on like a man refuelling.")


def _generator_late(state: GameState, io: IO) -> None:
    if st.generator_warning_active(state):
        io.say("the stumble again, worse. out here the cold is not an "
               "event. it is the landlord, and the generator is the "
               "rent, and the rent is due.", "alert")
    else:
        io.say("steady. you rest your hand on the housing and feel the "
               "heartbeat of the last inhabited building in the sky, "
               "and privately, unprofessionally, you bless it.")


_SCENES = {
    "DOME": {"early": _dome_early, "mid": _dome_mid, "late": _dome_late},
    "CORRIDOR": {"early": _corridor_early, "mid": _corridor_mid,
                 "late": _corridor_late},
    "QUARTERS": {"early": _quarters_early, "mid": _quarters_mid,
                 "late": _quarters_late},
    "PLANT": {"early": _plant_early, "mid": _plant_mid, "late": _plant_late},
    "GENERATOR": {"early": _generator_early, "mid": _generator_mid,
                  "late": _generator_late},
}


# ── outside ───────────────────────────────────────────────────────────

SUIT_CHECKS = ("SEALS", "AIR", "TETHER")

_CHECK_SCENES = {
    "SEALS": "you work the ring seals with tallow the way the manual "
             "forbids and forty years recommend. the suit is older than "
             "some of the removals. it will hold because it has to.",
    "AIR": "the bottle gauge reads full and you weigh it in your hands "
           "anyway, because gauges are records and you have gone off "
           "records. it is heavy the way full things are heavy. good.",
    "TETHER": "you pay the tether out and back, feeling for frays. "
              "sixty metres of woven steel: the umbilical, the keepers "
              "call it, those keepers being you, to yourself.",
}


def suit_check(state: GameState, which: str, io: IO) -> GameState:
    which = which.strip().upper()
    if state.watch < 6:
        io.say("SUIT LOCKER: SEALED. NO EXTERIOR WORK IS SCHEDULED.", "os")
        io.say("there is no reason to go out. the cold is not curious "
               "about you. keep it that way.", "dim")
        return state
    if not which:
        done = [c for c in SUIT_CHECKS if st.has_flag(state, f"SUIT_{c}")]
        io.say("SUIT PROTOCOL — CHECKS: " + ", ".join(
            f"{c}[{'DONE' if c in done else 'PENDING'}]" for c in SUIT_CHECKS),
            "os")
        io.say("SUIT <CHECK> TO PERFORM. ALL THREE BEFORE THE DOOR.", "os")
        return state
    if which not in SUIT_CHECKS:
        io.say(f"SUIT: NO SUCH CHECK — {which}", "os")
        return state
    io.say(f"SUIT PROTOCOL — {which}", "os")
    io.say(_CHECK_SCENES[which])
    return st.add_flag(state, f"SUIT_{which}")


def go_outside(state: GameState, io: IO) -> GameState:
    if state.watch < 6:
        io.say("AIRLOCK: SEALED. NO EXTERIOR WORK IS SCHEDULED.", "os")
        io.say("you stand at the inner door a moment all the same, "
               "reading the frost patterns like a page.", "dim")
        return state
    missing = [c for c in SUIT_CHECKS if not st.has_flag(state, f"SUIT_{c}")]
    if missing:
        if not st.has_flag(state, "OUTSIDE_WARNED"):
            io.say("AIRLOCK: SUIT PROTOCOL INCOMPLETE — " +
                   ", ".join(missing), "alert")
            io.say("AIRLOCK: OVERRIDE IS AVAILABLE. OVERRIDE IS NOT "
                   "ADVISED. A SECOND ATTEMPT WILL BE TREATED AS "
                   "OVERRIDE.", "alert")
            io.say("the door would open. doors do not care. that has "
                   "always been the thing about doors.", "dim")
            return st.add_flag(state, "OUTSIDE_WARNED")
        io.say("AIRLOCK: OVERRIDE ACCEPTED.", "alert")
        state = st.add_flag(state, "OUTSIDE_OVERRIDE")
        return st.set_ending(state, "OUTSIDE")
    return _outside_scene(state, io)


def _outside_scene(state: GameState, io: IO) -> GameState:
    io.say("AIRLOCK: CYCLING. TETHER LIVE. BOTTLE LIVE.", "os")
    io.pause(0.6)
    io.say("outside is the sound of your own blood and nothing else "
           "whatsoever. the ground is grey glass to the horizon. above "
           "you the sky stands the way it has stood all your life — "
           "except in the east, where there is now a margin with "
           "nothing written in it.")
    io.say("you walk the line to the array, hand over hand along the "
           "tether, and do the work: two couplings re-seated, one "
           "feed-horn swept clear. the work takes eleven minutes. you "
           "have air for ninety.")
    stages = (
        "TETHER AT 40 METRES. RETURN OR STAY?",
        "TETHER AT 60 METRES — FULL EXTENSION. RETURN OR STAY?",
        "BOTTLE AT ONE THIRD. THE MARGIN IN THE EAST IS WIDER THAN "
        "IT WAS ELEVEN MINUTES AGO. RETURN OR STAY?",
    )
    prose = (
        "the work is done and you are still facing east. it does not "
        "pull. that is the terrible thing — it does not pull, it "
        "permits, the way an open gate permits, and you have been "
        "forty years behind a shut one.",
        "at full stretch the tether hums a note too low to hear, felt "
        "in the teeth. the east does not come closer. you do. those "
        "are different things and you can no longer explain the "
        "difference to yourself.",
    )
    for stage, line in zip(stages, prose + ("",)):
        io.say(stage, "alert")
        answer = io.ask("suit ▸ ").strip().upper()
        if answer not in ("STAY", "S"):
            io.say("you turn your back on the east, which costs more "
                   "than the walk out did, and go home hand over hand "
                   "with your own breath loud as weather. the inner "
                   "door seals behind you. the station is warm. the "
                   "station is loud. you had not known the generator "
                   "was a lullaby until now.")
            io.say("AIRLOCK: CYCLE COMPLETE. EXTERIOR WORK LOGGED.", "os")
            return st.add_flag(state, "WENT_OUTSIDE")
        if line:
            io.say(line)
    return st.set_ending(state, "OUTSIDE")
