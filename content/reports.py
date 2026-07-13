"""REPORT — filing to the Bureau, and what comes back.

The Bureau's receipts are the other half of the horror: the human
institution that outlived its humans. The receipts never threaten.
They just decline, with perfect courtesy, to contain anyone.
"""

from __future__ import annotations

from content import catalog
from engine import state as st
from engine.io import IO
from engine.state import GameState

EPOCH_BASE = 71_198  # the count was old before the station was


def epoch(state: GameState) -> int:
    return EPOCH_BASE + state.watch


def file_report(state: GameState, io: IO) -> GameState:
    flag = f"REPORTED_{state.watch}"
    if st.has_flag(state, flag):
        io.say("BUREAU: A REPORT FOR THIS EPOCH IS ALREADY ON FILE.", "os")
        io.say("you file one report a watch. more would look like worry.",
               "dim")
        return state

    removed = catalog.new_removals(state)
    visible = catalog.count_visible(state)
    observer = "REMY" if st.has_flag(state, "QUESTION_ASKED") else state.observer

    io.say(f"COMPOSING SECTOR REPORT — EPOCH {epoch(state):,}", "os")
    if st.has_flag(state, f"SCANNED_{state.watch}"):
        io.say(f"  SOURCES CONFIRMED THIS EPOCH: {visible}", "os")
        if removed:
            io.say(f"  DISCREPANCIES NOTED: {len(removed)} "
                   f"(SEE ATTACHED ANNOTATIONS)", "os")
        else:
            io.say("  DISCREPANCIES NOTED: NONE", "os")
    else:
        io.say("  SOURCES CONFIRMED THIS EPOCH: UNAVAILABLE — NO "
               "CURRENT SCAN", "os")
        io.say("  DISCREPANCY STATUS: NOT EVALUATED", "os")
        io.say("  REPORT STATUS: INCOMPLETE", "os")
        io.say("the form takes the emptiness without comment. forms "
               "always do. an unscanned sky is not a lie, exactly; "
               "it is a night the record will show you looked away.",
               "dim")
    io.say(f"  OBSERVER OF RECORD: {observer.upper()}", "os")
    io.say("TRANSMITTING TO BUREAU OF THE CATALOGUE ...", "os")
    io.pause(0.6)

    state = st.add_flag(state, flag)
    _receipt(state, io)
    return state


def _receipt(state: GameState, io: IO) -> None:
    watch = state.watch
    if watch <= 3:
        io.say("BUREAU RECEIPT: REPORT ACCEPTED INTO REVIEW QUEUE.", "os")
        io.say("BUREAU RECEIPT: QUEUE POSITION 4,112. ESTIMATED REVIEW: —",
               "os")
        io.say("NO ACTION FOLLOWS.", "os")
        if watch == 1:
            io.say("the receipt is the same receipt it has always been. "
                   "there is a comfort in a machine that has answered "
                   "four thousand reports with the same shrug. you are "
                   "in a long line of people it did not listen to.",
                   "dim")
        return
    if watch == 4:
        io.say("BUREAU RECEIPT: REPORT ACCEPTED INTO REVIEW QUEUE.", "os")
        io.say("BUREAU RECEIPT: QUEUE POSITION 3,977. ESTIMATED REVIEW: —",
               "os")
        io.say("NO ACTION FOLLOWS.", "os")
        io.say("position three thousand nine hundred seventy-seven. the "
               "queue has stood at 4,112 since before your watch began. "
               "nothing reviews. so the queue is not being worked from "
               "the front. it is being shortened from somewhere else — "
               "reports, and the stations that wrote them, leaving the "
               "line the way the sources leave the sky: without ever "
               "having stood in it.", "dim")
        return
    if watch == 5:
        io.say("BUREAU RECEIPT: REPORT ACCEPTED INTO REVIEW QUEUE.", "os")
        io.say(f"BUREAU RECEIPT: LOGGED AT EPOCH {epoch(state) - 1:,}.", "os")
        io.say("NO ACTION FOLLOWS.", "os")
        io.say("logged at the previous epoch. before you wrote it. you "
               "read the line four times. a clock error, you decide, "
               "carefully, the way a man steps over a hole he has "
               "decided not to see.", "dim")
        return
    if watch == 6:
        io.say("BUREAU RECEIPT: REPORT ACCEPTED.", "os")
        io.say("BUREAU RECEIPT: ADVISORY — NO OBSERVER OF RECORD AT "
               "VESPER STATION.", "os")
        io.say("NO ACTION FOLLOWS.", "os")
        io.say("no observer of record. you look at your hands on the "
               "keys. they go on being hands, for now, obedient, "
               "liver-spotted, real. you type an objection into the "
               "advisory field. the field accepts it and grows no "
               "larger.", "dim")
        return
    if watch == 7:
        io.say("BUREAU RECEIPT: RECEIVED.", "os")
        io.pause(0.5)
        io.say("the receipt arrives in the wrong characters. not "
               "garbled — set, formal, in the closed script that runs "
               "around the face of your clock, the one nobody living "
               "reads. the terminal renders it without complaint, as "
               "if it had been waiting all these years to be asked.")
        io.say("you copy the shapes into the paper log by hand, in case "
               "they matter, in case they are the review, arrived at "
               "last, in the language the Bureau kept for endings.",
               "dim")
        return
    if watch == 8:
        io.say("TRANSMISSION COMPLETE. AWAITING RECEIPT ...", "os")
        io.pause(0.9)
        io.say("nothing comes back. not a refusal — a refusal would be "
               "an answer. the carrier goes out into the east and does "
               "not even leave a hole.")
        io.say("you file the report again in the paper log, by hand, "
               "and find that your hand has stopped shaking by the "
               "second line. the work is the work. that is the whole of "
               "what is left, and, you are surprised to note, it is "
               "enough.", "dim")
        return
    # the final watch
    io.say("CHANNEL OPEN. DESTINATION UNVERIFIABLE.", "os")
    io.say("REPORT FILED.", "os")
    io.say("filed to whom, filed to what, the report does not ask and "
           "neither, any longer, do you. the catalogue is kept. that a "
           "thing is unwitnessed has never yet excused the witness.",
           "dim")
