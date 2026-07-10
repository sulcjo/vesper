"""The five ways the watch ends. Each is an ending, not a game over.

House rule, held to the last line: the thing is never named, never
shaped, never explained. What can be written is what a man does in
front of it.
"""

from __future__ import annotations

from engine import state as st
from engine.io import IO
from engine.state import GameState


def play(state: GameState, io: IO) -> None:
    io.say("", "os")
    scene = _SCENES[state.ending]
    scene(state, io)
    io.say("", "os")
    io.say(f"■ THE WATCH OF {state.observer.upper()} — {state.ending}", "os")


def _keeper(state: GameState, io: IO) -> None:
    io.say("you file the last report and then, because the watch is not "
           "over until the watch is over, you tidy the dome. chair "
           "square to the desk. eyepiece capped. the crank wiped of "
           "your handprints, brass given back to brass.")
    io.pause(0.6)
    io.say("the east comes on the way morning used to, when there were "
           "mornings: not arriving anywhere, simply being the case, "
           "more and more. the plot empties. the grain goes. the border "
           "of the chart unwrites itself left to right like a sentence "
           "read backwards.")
    if st.has_flag(state, "WENT_OUTSIDE"):
        io.say("you think of the gate standing open at sixty metres, and "
               "of turning your back on it, and you find you would turn "
               "again. it was never that the east was forbidden. it was "
               "that the count was yours.")
    io.say("you take up the journal and write the sector's final entry "
           "by hand, in ink, in the margin, where the first keeper "
           "wrote. four words. you know the four words. every keeper "
           "has known the four words, and now there is nothing left "
           "for them to be about except the hand that writes them.")
    io.say("STILL THERE. STILL HERE.", "alert")
    io.pause(0.8)
    io.say("the archive will not hold this. paper holds it. paper, and "
           "whatever it is that paper is a gesture toward — the thing "
           "a witness does, the unwitnessable act of having seen.")
    io.say("the count was kept. all the way to the end of counting, "
           "the count was kept, and it was kept by you.")
    io.say("", "prose")
    io.say("EPOCH 71,206. CATALOGUE CLOSED IN GOOD ORDER.", "os")
    io.say("OBSERVER OF RECORD: PRESENT.", "os")


def _quiet(state: GameState, io: IO) -> None:
    if st.has_flag(state, "BURNED"):
        io.say("the journal burns the way old paper burns, eagerly, as "
               "if it had been waiting to be let off. forty years of "
               "accessions, margins, tea-rings, the pier, the water, "
               "the name you had and the hole where the other one "
               "was — smoke, heat, a bright hinge of flame, gone.")
        io.say("you expected grief. what arrives instead is the feeling "
               "at the end of a long shift, boots off, weight down. "
               "nothing is lost that is not first kept. you have "
               "resigned the keeping. that is all. it turns out to be "
               "possible, like most terrible things.")
    else:
        io.say("you do not file the last report. the composing screen "
               "waits, patient as furniture, and you look at it for a "
               "while the way you would look at a field you are done "
               "mowing, and you switch the board off.")
        io.say("you make the rounds without hurrying: the plant watered, "
               "the clock wound, the generator's flank warm under your "
               "palm. not duties now. courtesies. the difference is "
               "enormous and invisible, like everything tonight.")
    io.pause(0.6)
    io.say("you lie down with your boots off. the tick and the pulse "
           "keep the room the size of a room. somewhere east of "
           "everything, the count arrives at its last number, and it "
           "is not your number, because you have set yours down.")
    io.say("what comes is not sleep exactly, but it is gentle, the way "
           "snowfall is gentle: not out of kindness. out of "
           "thoroughness.")
    io.say("", "prose")
    io.say(f"EPOCH 71,206. NO REPORT ON FILE.", "os")
    io.say("NO OBSERVER OF RECORD. NO OBSERVER OF RECORD HAS EVER "
           "BEEN AT VESPER STATION.", "os")
    io.say("NO ACTION FOLLOWS.", "os")


def _answer(state: GameState, io: IO) -> None:
    io.say("you key the transmitter. forty years of receiving, and the "
           "sending key is stiff as a new boot. you press it and the "
           "carrier goes out of you — out of the station — east.")
    io.say(f"you send your name. the true one. “{state.observer},” "
           "you send, “keeper of the Vesper catalogue, fifth of "
           "that watch,” and the east takes the words the way dark "
           "water takes a stone: without argument, without ring or "
           "ripple, and you feel each one leave you like a pulled "
           "nail —")
    io.pause(0.8)
    io.say("you send your na▒e. the true one. you send your ▒▒me, "
           "keeper of the ▒esper catalogue, ▒▒▒th of that watch, and "
           "the ▒ast takes the wor▒s —", "dim")
    io.say("you send ▒▒▒▒ ▒ame. the ▒▒▒e one. ▒▒▒ send —", "dim")
    io.say("▒▒▒ ▒▒▒▒ —", "dim")
    io.pause(1.0)
    io.say("the carrier holds. the carrier holds. the carrier holds "
           "something, and the count, at long last, is right.")
    io.say("", "prose")
    io.say("WIRE: TRAFFIC LOGGED.", "os")
    io.say("OBSERVER OF RECORD: REMY.", "os")
    io.say("OBSERVERS OF RECORD: ALL OF THEM. THE COUNT IS RIGHT.", "os")


def _cold(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("the generator stops at the bottom of the night, between "
           "one tick of the clock and a next tick that does not come "
           "from anywhere. you are awake at once. you were a keeper; "
           "your body knows the sound of a kept thing ending.")
    io.say("the cold is not dramatic. it is procedural. it comes "
           "through the walls in the order the manual would predict, "
           "corridor first, then quarters, closing the station down "
           "section by section like a man turning off lights behind "
           "him.")
    io.say("you had warnings. you counted them at the time — that is "
           "the bitter arithmetic of it, you counted everything, and "
           "you let this number alone go by unattended.")
    io.pause(0.8)
    io.say("near the end it is almost warm, which you know to be a "
           "lie, and you hold instead to the one true thing in reach: "
           "the dent in the pillow, ten thousand sleeps deep, a record "
           "in a medium no archive can amend. proof of you. proof of "
           "every keeper who was ever too tired to be a hero and lay "
           "down anyway and got up anyway, ten thousand times, until "
           "once.")
    io.say("", "prose")
    io.say("EPOCH 71,20▒. STATION TEMPERATURE OUT OF RANGE.", "os")
    io.say("NO OBSERVER OF RECORD. NO ACTION FOLLOWS.", "os")


def _outside(state: GameState, io: IO) -> None:
    if st.has_flag(state, "OUTSIDE_OVERRIDE"):
        io.say("the door does what doors do. you are through it in the "
               "old suit with the unchecked seals, and the cold takes "
               "the measure of the shortcuts you took, seam by seam, "
               "with a bookkeeper's patience.")
    else:
        io.say("you stay. the third time of asking, and you stay, and "
               "the staying settles over you like a verdict read in "
               "your own voice.")
    io.say("you face the east with your bottle thinning and the tether "
           "humming its one low note, and the margin where the sky "
           "was opens the way an ear opens to a sound — nothing "
           "moving, nothing coming, only a listening getting larger.")
    io.pause(0.8)
    io.say("it does not take you. that would be an event, and it has "
           "never once been an event. it permits, and goes on "
           "permitting, and somewhere behind you the bottle finishes "
           "its arithmetic, and of the two of them the bottle at "
           "least has the decency to be something.")
    io.say("the tether is found at full extension. the tether is not "
           "found. there is no tether of record.", "dim")
    io.say("", "prose")
    io.say("AIRLOCK: OUTER DOOR OPEN AT EPOCH CHANGE.", "os")
    io.say("EXTERIOR WORK LOG: NO ENTRY. NO EXTERIOR WORK HAS EVER "
           "BEEN LOGGED AT VESPER STATION.", "os")
    io.say("NO ACTION FOLLOWS.", "os")


_SCENES = {
    "KEEPER": _keeper,
    "QUIET": _quiet,
    "ANSWER": _answer,
    "COLD": _cold,
    "OUTSIDE": _outside,
}
