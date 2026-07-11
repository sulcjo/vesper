"""The shape of a watch: waking, duties, and the going down to sleep.

Also owns the journal-fade policy — how hard the past is being leaned
on, expressed as the fraction of a written entry that no longer reads.
"""

from __future__ import annotations

from content import reports
from engine import state as st
from engine.io import IO
from engine.state import FINAL_WATCH, GameState

_FADE_BASE = {6: 0.12, 7: 0.25, 8: 0.4, 9: 0.55}


def journal_fade(current_watch: int, entry_watch: int) -> float:
    """How much of an entry written on entry_watch is gone when read
    on current_watch. This watch's own ink is always safe."""
    if entry_watch >= current_watch:
        return 0.0
    base = _FADE_BASE.get(current_watch, 0.0)
    if base == 0.0:
        return 0.0
    age_penalty = 0.04 * max(0, current_watch - entry_watch - 1)
    return min(0.7, base + age_penalty)


def hour_label(acts: int) -> str:
    if acts < 3:
        return "EARLY"
    if acts < st.NIGHT_BUDGET:
        return "DEEP"
    return "LATE"


_FATIGUE = (
    "the deep hours. your eyes negotiate each line before agreeing to "
    "read it. an old man's night is a short coat — it does not cover "
    "everything you would like it to.",
    "you catch yourself standing in the middle of the room with no "
    "memory of the errand that brought you there. the errand waits, "
    "patient, somewhere behind your eyes. the cot argues its case.",
    "the station has gone very quiet around your tiredness, the way "
    "company falls silent around a man who should long since have "
    "gone to bed. whatever this is, it will weigh less in the "
    "morning. (SLEEP is wise.)",
)


def fatigue_line(acts: int) -> str:
    over = max(0, acts - st.NIGHT_BUDGET)
    return _FATIGUE[min(over, len(_FATIGUE) - 1)]


_PEN_PROMPTS = {
    1: "begin with the weather, Okonkwo told you once. there is no "
       "weather. he knew that. begin anyway.",
    2: "write what you counted. write what counted.",
    3: "the archive holds records. hold something the archive cannot.",
    4: "write the sound the generator makes when it doubts, exactly, "
       "so that someone could believe you.",
    5: "write who taught you. spell the names slowly.",
    6: "write the name you still have. write around the one you do "
       "not.",
    7: "write what you are for. one line will do. one line has always "
       "done.",
    8: "write what you would keep, if keeping were the only verb left.",
    9: "last page tonight, one way or another. write to whoever reads "
       "over the shoulder of no one.",
}


def pen_prompt(watch: int) -> str:
    return _PEN_PROMPTS.get(watch, _PEN_PROMPTS[9])


def duties_line(state: GameState) -> str:
    marks = []
    for duty, flag in (("SCAN", f"SCANNED_{state.watch}"),
                       ("DIFF", f"DIFFED_{state.watch}"),
                       ("REPORT", f"REPORTED_{state.watch}")):
        marks.append(f"{duty}[{'x' if st.has_flag(state, flag) else ' '}]")
    return "DUTIES THIS EPOCH: " + "  ".join(marks)


def wake(state: GameState, io: IO) -> GameState:
    io.say("", "os")
    io.say(f"VESPER STATION — EPOCH {reports.epoch(state):,} — "
           f"WATCH {state.watch} OF {FINAL_WATCH}", "os")
    io.say(duties_line(state), "os")
    if st.generator_warning_active(state):
        if state.generator_strikes == 0:
            io.say("NOTICE: GENERATOR CYCLE IRREGULAR. MAINTENANCE IS "
                   "INDICATED.", "alert")
        else:
            io.say("WARNING: GENERATOR CYCLE CRITICAL. WITHOUT "
                   "MAINTENANCE THIS WATCH, HEATING WILL FAIL.", "alert")
    io.say("", "os")
    _WAKES[state.watch](state, io)
    return state


def _wake_1(state: GameState, io: IO) -> None:
    io.say("you wake before the bell, as always. forty years will set a "
           "clock in the meat of you. the quarters hold their overnight "
           "cold — a cold with the texture of iron — and you dress "
           "inside the blanket's last warmth the way you have ten "
           "thousand times, boots last, laces by feel.")
    io.say("the kettle knocks against its element as it heats: three "
           "knocks, a pause, two more, the same stammer it has had "
           "since Weir's day. tea the colour of rust, mostly stems "
           "now. you drink half of it standing and carry the rest, "
           "and the two-minute walk to the dome goes as it always "
           "goes — free hand trailing the rail, steel burning cold "
           "through the fingerless glove — the little liturgy, in the "
           "same order since the morning you inherited it.")
    if st.has_flag(state, "LEGACY"):
        io.say("the sign-in book felt heavy under your pen this morning, "
               "heavier than the station's years explain, as if other "
               "watches had been kept here that the inventory has "
               "misplaced. you did not count the pages. you have "
               "learned which counts to leave alone.", "dim")
    io.say("the work is simple and it is yours: scan the sector, compare "
           "against the archive, file to a Bureau that has not written "
           "back in living memory. the watch has always been kept. that "
           "the sky has mostly stopped needing watching is, you would "
           "say, if anyone asked, entirely beside the point.")
    io.say("(HELP lists the boards. SLEEP ends the watch.)", "dim")


def _wake_2(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("you dreamed of counting. not of numbers — of the act, the "
           "pointing finger, the moving lips. you woke with your hand "
           "already shaping it under the blanket, index finger ticking "
           "off the dark, and lay still until it stopped.")
    io.say("the kettle takes longer than it used to, or you have "
           "started timing it — the element glowing its dull orange a "
           "long while before the water believes it. either way: tea, "
           "rail, dome. the sky is where you left it. you would "
           "notice. it is your whole profession to notice.")


def _wake_3(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("last night you took the journal out and read your own "
           "accessions against the archive, line by line, like a man "
           "checking his change. the archive is clean. the archive is "
           "perfectly clean, the way snow is clean over a field you "
           "know has a road in it.")
    io.say("your handwriting does not agree with the record. one of "
           "them is you. this ought to be a simple sentence, and you "
           "notice, buttering the last of the hard bread, that it no "
           "longer entirely is.")


def _wake_4(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("the generator woke you. not by stopping — by hesitating, "
           "one beat held too long, the way a sentence hesitates "
           "before bad news is put in it. you lay in the dark with "
           "your palm flat against the wall, reading the rotation "
           "through the plating the way a doctor reads a wrist, "
           "timing it against the clock's tick until both agreed to "
           "go on. the station is old. you are old. the arrangement "
           "has always been that you fail last.")


def _wake_5(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("you woke thinking of Okonkwo, your keeper before Weir's, "
           "the one who trained you. sixty days of him saying the same "
           "sentence at the same hour: the instrument is the station; "
           "the observer is the instrument's conscience. you thought he "
           "was being poetic. he was being technical. it took you a "
           "decade to hear the difference.")
    io.say("in his day there were still four beacons on the wire and a "
           "supply shuttle every hundred epochs. the shuttle stopped in "
           "his lifetime. he logged its non-arrival every hundredth "
           "epoch for the rest of his watch, without comment, a man "
           "holding a door for someone who has plainly gone home "
           "another way. you keep meaning to take that page down from "
           "the shelf. tonight, maybe, if the boards run quiet. "
           "(the SHELF holds the old keepers' volumes.)")


def _wake_6(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("you woke reaching for a name and it was not there. not a "
           "star's — a person's. the pier, the water, the sun on the "
           "water, the laugh — all present, filed, vivid. the name has "
           "the shape of a missing tooth: your tongue keeps going to "
           "it, and it keeps being a hole.")
    io.say("your mouth still knows it. that is the cruelty of it. the "
           "lips part, the tongue lifts, the whole word stands ready "
           "in the muscle the way a stair is ready in the legs — and "
           "nothing arrives. the body keeps what the mind is docked. "
           "for one long minute you sit there, shaped around a sound "
           "you cannot make, a bell holding the swing of a tongue it "
           "no longer has.")
    io.say("you sat on the edge of the cot and made yourself say the "
           "names you do have. your own. the plant's, which you have "
           "never told anyone. Weir. Okonkwo. Sever. Remy. the count "
           "came up short and you got dressed anyway, because the sky "
           "does not wait on grief, especially not now, when it is "
           "doing so much of its own vanishing.")


def _wake_7(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("in the dream the counting had a direction. you woke before "
           "you could hear which, with the blanket already off, and lay "
           "there doing the sums of an old man's night: how many "
           "watches you have kept, how many are left in you, and how "
           "it happens that the second number has started feeling like "
           "the sky's decision rather than your body's.")
    io.say("the station is quieter than its own inventory of noises. "
           "you have begun to catch the walls at it — holding still, "
           "the way a room holds still when it has just stopped "
           "talking about you.")
    io.say("twice tonight you came to from the outside: a keeper, seen "
           "as if from the doorway, an old man bent correct and "
           "punctual over a board. you could not swear you were "
           "behind his eyes at the time. the work was right, whoever "
           "did it. you initial his figures and do not raise the "
           "matter with him.", "dim")


def _wake_8(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("frost on the inside of the corridor now, fine as breath on "
           "glass. it comes away under your thumbnail in a little "
           "white curl and melts against the skin without wetting it, "
           "there and then simply not. the station is not colder. you "
           "checked the figures twice. it is as if the walls have "
           "started believing the east instead of the thermometer, "
           "and you cannot entirely blame them.")
    io.say("SUIT PROTOCOL UNSEALED. EXTERIOR WORK IS AVAILABLE THIS "
           "WATCH. (SUIT, then OUTSIDE.)", "os")
    io.say("the array wants sweeping — the feed-horns fur up with "
           "frost-glass and the couplings walk loose in the cold. it "
           "is real work and it is outside, forty years of habit "
           "against sixty metres of tether. you will decide at the "
           "door, like always. there has never before been an always "
           "with this in it.", "dim")


def _wake_9(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("you do not remember deciding to wake. you were asleep, and "
           "then you were standing in the dome already dressed, hand "
           "on the shutter crank, with the tea going cold on the rail "
           "behind you like an offering to whoever you were yesterday.")
    io.say("the east is in the room now. not visibly. the dome is "
           "sealed and the shutter is shut and the east is in the room "
           "the way winter is in a house, under the doors, in the "
           "nails. tonight the sector gets its last honest count. "
           "after that — the count is nearly right, the wire said. "
           "it is your arithmetic. finish it or do not.")
    io.say("FINAL EPOCH. ALL BOARDS REMAIN AVAILABLE.", "os")


_WAKES = {1: _wake_1, 2: _wake_2, 3: _wake_3, 4: _wake_4, 5: _wake_5,
          6: _wake_6, 7: _wake_7, 8: _wake_8, 9: _wake_9}


def close(state: GameState, io: IO) -> None:
    """The lying-down at the end of a survived watch (not the final)."""
    lines = {
        1: "you bank the lamps and lie down. the clock ticks. the "
           "generator answers it, half a beat behind, all night, like "
           "two old men agreeing about nothing in particular.",
        2: "sleep comes slow. you count to keep from counting — your "
           "own trick against your own habit — and lose, and count, "
           "and sleep.",
        3: "you put the journal under the pillow. you have not done "
           "that since your first year. the paper breathes when you "
           "turn over, a small dry voice saying kept, kept, kept.",
        4: "you sleep with your boots on. if the generator hesitates "
           "again you will hear it through the frame of the cot, and "
           "be up, and be useful. useful is the whole of the plan now "
           "and it has the great merit of fitting on one line.",
        5: "you fall asleep listening for the Pulse through the floor, "
           "which is not possible, and hearing it anyway, which is "
           "what listening is for. four seconds. four seconds. the "
           "house of the species, sleeping, but breathing.",
        6: "in the dark you go through the pier again: boards, water, "
           "sun, laugh. you set the missing name gently aside, the "
           "way you would sheet over a chair, and sleep in the room "
           "with it.",
        7: "you wind the clock before bed though it is not the hour "
           "for it, eleven turns, and lie down inside its tick as if "
           "drawing a chalk line around yourself. count that, you "
           "think at the ceiling, at the east, at nothing. it is an "
           "honest number and it is mine.",
        8: "the station ticks and settles around you, kept and "
           "keeping. whatever is standing open in the east, it can "
           "stand open one more night without you looking at it. "
           "this is either courage or its house-trained cousin. you "
           "sleep before you can rule.",
    }
    io.say(lines.get(state.watch, "you sleep."), "dim")
