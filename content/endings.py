"""The five ways the watch ends. Each is an ending, not a game over.

House rule, held to the last line: the thing is never named, never
shaped, never explained. What can be written is what a man does in
front of it.
"""

from __future__ import annotations

from content import shelf
from engine import draw, state as st
from engine.io import IO
from engine.state import GameState


def run_profile(state: GameState) -> dict:
    """What kind of keeper this run was. Pure; endings read it."""
    return {
        "witnessed": len(state.witnessed),
        "journal": len(st.living_journal(state)),
        "volumes": sum(
            1 for k in shelf.KEEPERS if st.has_flag(state, f"READ_{k}")
        ),
        "went_outside": st.has_flag(state, "WENT_OUTSIDE"),
        "saw_the_other": st.has_flag(state, "SAW_THE_OTHER"),
        "heard_pulse_wrong": st.has_flag(state, "HEARD_PULSE_WRONG"),
    }


def _replay_pages(state: GameState, io: IO, fractions: list[float]) -> None:
    """The journal, one last time. fractions cycles over the entries."""
    living = st.living_journal(state)
    for n, (index, entry) in enumerate(living):
        fraction = fractions[min(n * len(fractions) // max(1, len(living)),
                                 len(fractions) - 1)]
        shown = draw.erase_words(entry.text, fraction,
                                 seed=index * 31 + entry.watch)
        io.art(["  " + line for line in
                draw.render_page([shown], title=f"WATCH {entry.watch}")])
        io.pause(0.4)


def play(state: GameState, io: IO) -> None:
    io.say("", "os")
    scene = _SCENES[state.ending]
    scene(state, io)
    profile = run_profile(state)
    io.say("", "os")
    io.say(f"ANNOTATIONS IN YOUR HAND: {profile['witnessed']}. "
           f"VOLUMES TAKEN DOWN: {profile['volumes']} OF "
           f"{len(shelf.KEEPERS)}.", "os")
    io.say(f"■ THE WATCH OF {state.observer.upper()} — {state.ending}", "os")


def _keeper(state: GameState, io: IO) -> None:
    io.say("you file the last report and then, because the watch is "
           "not over until the watch is over, you tidy the dome. "
           "chair square to the desk. eyepiece capped, the little "
           "brass lid seating with its familiar half-turn and click. "
           "the crank wiped of your handprints with the soft rag "
           "kept for nothing else, brass given back to brass. the "
           "red lamp you leave burning. some rooms should not have "
           "to be dark before their time.")
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
           "wrote. the pen scratches in the quiet — the loudest thing "
           "left in the sky — and the ink goes down wet and black "
           "and certain. four words. you know the four words. every "
           "keeper has known the four words, and now there is "
           "nothing left for them to be about except the hand that "
           "writes them.")
    io.say("STILL THERE. STILL HERE.", "alert")
    io.pause(0.8)
    io.say("the archive will not hold this. paper holds it. paper, and "
           "whatever it is that paper is a gesture toward — the thing "
           "a witness does, the unwitnessable act of having seen.")
    profile = run_profile(state)
    if profile["volumes"] >= len(shelf.KEEPERS):
        io.say("you shelve your journal beside the other four, squaring "
               "the spines. you read every one of them, this last tour. "
               "whatever the shelf is now — record, monument, kindling "
               "for nobody — it is complete, and completeness was "
               "always the whole of the craft.")
    if profile["witnessed"] >= 10:
        io.say(f"{profile['witnessed']} annotations stand in your hand "
               "against the archive's clean pages. every one of them "
               "was a night you looked when looking changed nothing "
               "and did it anyway. that arithmetic the east may keep.")
    if profile["journal"]:
        io.say("and the terminal, unasked, does the one kind thing of "
               "its long service. it prints your pages back. all of "
               "them. whole.")
        _replay_pages(state, io, [0.0])
        io.say("every word present. every word kept.", "alert")
    io.say("they can take the sky — that is proven now. they can take "
           "the record of the sky, and the towns, and the names, and "
           "whatever it was the names were pinned to. what they have "
           "not taken — what you begin to suspect cannot be taken, "
           "because it is not a thing but an act — is the choosing. "
           "which way to face. whether to attend or to look away. "
           "what to keep, and at what hour to set it down. of all "
           "your issued equipment, the stance was the one item never "
           "on any inventory, and so the one item nothing knows how "
           "to remove.")
    io.say("the east will arrive. it will arrive after the choosing "
           "has already happened. in the only ledger that was ever "
           "yours to keep, that is called too late.")
    io.say("the count was kept. all the way to the end of counting, "
           "the count was kept, and it was kept by you.")
    io.say("", "prose")
    io.say("EPOCH 71,208. CATALOGUE CLOSED IN GOOD ORDER.", "os")
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
    if st.has_flag(state, "BURNED"):
        io.say("of the pages, one line survives, caught unburned at the "
               "grate's lip, and you leave it there: ash holds no "
               "appointments.", "dim")
    elif st.living_journal(state):
        io.say("you leave the journal open on the desk, and look once "
               "at what the fading has decided to spare:", "dim")
        _replay_pages(state, io, [0.9])
    io.say("you lie down with your boots off, and the weight that "
           "leaves you is not the boots. the blanket's wool is rough "
           "under your chin exactly the way it has been rough for "
           "forty years, and the tick and the pulse keep the room "
           "the size of a room. somewhere east of everything, the "
           "count arrives at its last number, and it is not your "
           "number, because you have set yours down.")
    io.say("this is not surrender, whatever box the Bureau's forms "
           "would have wanted ticked. surrender requires an enemy, "
           "and the east was never that; it is barely even an it. "
           "this is the other thing, the thing old men do well or "
           "badly and almost never get to choose the hour of: the "
           "closing of a ledger by the one who kept it, in his own "
           "hand, at a line of his own choosing. you look back down "
           "the long column of your life and find you do not need it "
           "recounted, or believed, or held by anyone. it was had. "
           "that is the whole of what having ever was.")
    io.say("what comes is not sleep exactly, but it is gentle, the way "
           "snowfall is gentle: not out of kindness. out of "
           "thoroughness.")
    io.say("", "prose")
    io.say(f"EPOCH 71,208. NO REPORT ON FILE.", "os")
    io.say("NO OBSERVER OF RECORD. NO OBSERVER OF RECORD HAS EVER "
           "BEEN AT VESPER STATION.", "os")
    io.say("NO ACTION FOLLOWS.", "os")


def _answer(state: GameState, io: IO) -> None:
    io.say("you key the transmitter. forty years of receiving, and "
           "the sending key is stiff as a new boot — it takes real "
           "weight, the whole of two fingers, and closes with a "
           "click you feel in the bones of the hand like a latch "
           "going home. the carrier goes out of you — out of the "
           "station — east.")
    if state.final_words:
        sent = state.final_words
        io.say(f"“{sent},” you send, and the east takes the words the "
               "way dark water takes a stone: without argument, "
               "without ring or ripple, and you feel each one leave "
               "you like a pulled nail —")
        io.pause(0.8)
        for step, fraction in enumerate((0.3, 0.6, 0.9), start=1):
            io.say(f"“{draw.erase_words(sent, fraction, seed=step)},” "
                   "you send —", "dim")
    else:
        io.say(f"you send your name. the true one. “{state.observer},” "
               "you send, “keeper of the Vesper catalogue, fifth of "
               "that watch,” and the east takes the words the way dark "
               "water takes a stone: without argument, without ring or "
               "ripple, and you feel each one leave you like a pulled "
               "nail —")
        io.pause(0.8)
        io.say("you send your na▒e. the true one. you send your ▒▒me, "
               "keeper of the ▒esper catalogue, ▒▒▒th of that watch, "
               "and the ▒ast takes the wor▒s —", "dim")
        io.say("you send ▒▒▒▒ ▒ame. the ▒▒▒e one. ▒▒▒ send —", "dim")
    io.say("▒▒▒ ▒▒▒▒ —", "dim")
    if st.living_journal(state):
        io.say("and behind the words, unbidden, the pages go too, "
               "lifting off the paper line by line into the carrier:",
               "dim")
        _replay_pages(state, io, [0.3, 0.6, 0.9])
    io.pause(1.0)
    io.say("and where the words were there is not emptiness. there is "
           "room. you had not known the self was a wall until doors "
           "began appearing in it — a lifetime of keeping the count "
           "from behind one pair of eyes, and it turns out the eyes "
           "were the narrow part. what comes through the doors is "
           "not voices. it is the hearing itself, shared out, the "
           "way a harbour shares its water with the sea and is not "
           "thereby emptied. you are not being taken. you are being "
           "attended — by everything, at last, from every side, the "
           "one thing you spent forty years doing and never once "
           "received.")
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
           "him. your breath begins to show, then to settle — a fine "
           "frost gathering on the blanket's wool where it crosses "
           "your chest, your own small weather, the last weather "
           "there will ever be indoors.")
    io.say("you had warnings. you counted them at the time — that is "
           "the bitter arithmetic of it, you counted everything, and "
           "you let this number alone go by unattended.")
    io.say("the regrets, when they come, are not the great ones. that "
           "is the finding nobody files: at the end the large griefs "
           "stand off politely at the edge of the lamp, and it is "
           "the small ones that come and sit on the cot. you meant "
           "to re-pot the plant and said next watch. you hoarded the "
           "last real tea against an occasion and no occasion ever "
           "outranked an ordinary tuesday, and now the tin will "
           "outlive the tongue. you never told the plant its name "
           "out loud where it could hear you. these are the ones "
           "that hold your hand.")
    io.pause(0.8)
    io.say("near the end it is almost warm, which you know to be a "
           "lie, and you hold instead to the one true thing in reach: "
           "the dent in the pillow, ten thousand sleeps deep, a record "
           "in a medium no archive can amend. proof of you. proof of "
           "every keeper who was ever too tired to be a hero and lay "
           "down anyway and got up anyway, ten thousand times, until "
           "once.")
    io.say("", "prose")
    _unfiled_fragment(state, io)
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
    io.say("what you feel, standing in it, is not fear, and you would "
           "swear to that in any log under any oath. it is scale. "
           "you are one witness wide — one lamp of attention in a "
           "skull — and the thing before you is measured in "
           "nothings, and the feeling that rises is the indecent "
           "secret of every awe you ever felt under the old rich "
           "sky: the relief of being made small enough, at last, to "
           "stop carrying yourself.")
    io.say("it does not take you. that would be an event, and it has "
           "never once been an event. it permits, and goes on "
           "permitting, and somewhere behind you the bottle finishes "
           "its arithmetic, and of the two of them the bottle at "
           "least has the decency to be something.")
    io.say("the tether is found at full extension. the tether is not "
           "found. there is no tether of record.", "dim")
    io.say("", "prose")
    _unfiled_fragment(state, io)
    io.say("AIRLOCK: OUTER DOOR OPEN AT EPOCH CHANGE.", "os")
    io.say("EXTERIOR WORK LOG: NO ENTRY. NO EXTERIOR WORK HAS EVER "
           "BEEN LOGGED AT VESPER STATION.", "os")
    io.say("NO ACTION FOLLOWS.", "os")


def _unfiled_fragment(state: GameState, io: IO) -> None:
    """For the deaths: one page survives, half-eaten, unfiled."""
    living = st.living_journal(state)
    if not living:
        return
    index, entry = living[0]
    shown = draw.erase_words(entry.text, 0.5, seed=index * 31 + entry.watch)
    io.say("PAPER RECORD — UNFILED:", "os")
    io.art(["  " + line for line in
            draw.render_page([shown], title=f"WATCH {entry.watch}")])


_SCENES = {
    "KEEPER": _keeper,
    "QUIET": _quiet,
    "ANSWER": _answer,
    "COLD": _cold,
    "OUTSIDE": _outside,
}
