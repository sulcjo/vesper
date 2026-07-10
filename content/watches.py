"""The shape of a watch: waking, duties, and the going down to sleep.

Also owns the journal-fade policy — how hard the past is being leaned
on, expressed as the fraction of a written entry that no longer reads.
"""

from __future__ import annotations

from content import reports
from engine import state as st
from engine.io import IO
from engine.state import FINAL_WATCH, GameState

_FADE_BASE = {5: 0.15, 6: 0.35, 7: 0.55}


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


def _wake_1(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("you wake before the bell, as always. forty years will set a "
           "clock in the meat of you. kettle, dry tea, the two-minute "
           "walk from quarters to the dome with your hand trailing the "
           "cold rail the whole way — the little liturgy, done in the "
           "same order since the morning you inherited it.")
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
    io.say("the kettle takes longer than it used to, or you have started "
           "timing it. either way: tea, rail, dome. the sky is where "
           "you left it. you would notice. it is your whole profession "
           "to notice.")


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
           "one beat held too long, the way a sentence hesitates before "
           "bad news is put in it. you lay in the dark timing the "
           "rotation against the clock's tick until both agreed to go "
           "on. the station is old. you are old. the arrangement has "
           "always been that you fail last.")


def _wake_5(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("you woke reaching for a name and it was not there. not a "
           "star's — a person's. the pier, the water, the sun on the "
           "water, the laugh — all present, filed, vivid. the name has "
           "the shape of a missing tooth: your tongue keeps going to "
           "it, and it keeps being a hole.")
    io.say("you sat on the edge of the cot and made yourself say the "
           "names you do have. your own. the plant's, which you have "
           "never told anyone. Weir. Remy. the count came up short and "
           "you got dressed anyway, because the sky does not wait on "
           "grief, especially not now, when it is doing so much of its "
           "own vanishing.")


def _wake_6(state: GameState, io: IO) -> None:  # noqa: ARG001
    io.say("frost on the inside of the corridor now, fine as breath on "
           "glass. the station is not colder. you checked the figures "
           "twice. it is as if the walls have started believing the "
           "east instead of the thermometer, and you cannot entirely "
           "blame them.")
    io.say("SUIT PROTOCOL UNSEALED. EXTERIOR WORK IS AVAILABLE THIS "
           "WATCH. (SUIT, then OUTSIDE.)", "os")
    io.say("the array wants sweeping — the feed-horns fur up with "
           "frost-glass and the couplings walk loose in the cold. it "
           "is real work and it is outside, forty years of habit "
           "against sixty metres of tether. you will decide at the "
           "door, like always. there has never before been an always "
           "with this in it.", "dim")


def _wake_7(state: GameState, io: IO) -> None:  # noqa: ARG001
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
          6: _wake_6, 7: _wake_7}


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
        5: "in the dark you go through the pier again: boards, water, "
           "sun, laugh. you set the missing name gently aside, the "
           "way you would sheet over a chair, and sleep in the room "
           "with it.",
        6: "the station ticks and settles around you, kept and "
           "keeping. whatever is standing open in the east, it can "
           "stand open one more night without you looking at it. "
           "this is either courage or its house-trained cousin. you "
           "sleep before you can rule.",
    }
    io.say(lines.get(state.watch, "you sleep."), "dim")
