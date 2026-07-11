"""Command parsing and dispatch. Handlers are pure of terminal concerns:
they take (state, argument-string, io) and return (new_state, signal).

Signals: None (keep going), "sleep" (end the watch), "quit" (leave),
"ended" (an ending has been set; the shell plays it out).
"""

from __future__ import annotations

from content import (
    catalog,
    eyepiece,
    places,
    reports,
    rituals,
    shelf,
    watches,
    wire,
)
from engine import draw, state as st, term
from engine.io import IO
from engine.state import FINAL_WATCH, GameState

Result = tuple[GameState, str | None]

_ALIASES = {
    "S": "SCAN", "D": "DIFF", "E": "EYE", "L": "LISTEN", "W": "WALK",
    "T": "TEND", "J": "JOURNAL", "R": "REPORT", "ST": "STATUS",
    "H": "HELP", "?": "HELP",
}


def parse(line: str) -> tuple[str, str]:
    stripped = line.strip()
    if not stripped:
        return "", ""
    head, _, rest = stripped.partition(" ")
    cmd = head.upper()
    return _ALIASES.get(cmd, cmd), rest.strip()


def _spend(state: GameState, io: IO) -> GameState:
    """A deep-night act. Past the budget the night pushes back — in
    prose only; the final watch is exempt and endless."""
    if state.acts >= st.NIGHT_BUDGET and state.watch < FINAL_WATCH:
        io.say(watches.fatigue_line(state.acts), "dim")
    return st.spend_act(state)


def dispatch(state: GameState, line: str, io: IO) -> Result:
    cmd, rest = parse(line)
    if not cmd:
        return state, None
    handler = _COMMANDS.get(cmd)
    if handler is None:
        io.say(f"UNRECOGNISED: {cmd}", "os")
        io.say("the terminal has never pretended to understand more "
               "than it understands. HELP lists what it does.", "dim")
        return state, None
    return handler(state, rest, io)


# ── the boards ────────────────────────────────────────────────────────

def _help(state: GameState, rest: str, io: IO) -> Result:  # noqa: ARG001
    io.say("STATION BOARDS —", "os")
    entries = [
        ("SCAN", "survey the sector; draw the plot"),
        ("DIFF", "compare tonight's plot against the archive"),
        ("EYE <designation>", "put your own eye to a source"),
        ("LISTEN", "open the wire"),
        ("REPORT", "file the sector report to the Bureau"),
        ("JOURNAL WRITE|READ|COPY", "the book kept by hand"),
        ("SHELF [keeper]", "the old keepers' volumes"),
        ("WALK <place>", "dome, corridor, quarters, plant, generator"),
        ("TEND <thing>", "generator, clock, plant"),
        ("STATUS", "the station and the watch"),
        ("SLEEP", "end the watch"),
        ("QUIT", "leave the terminal (the watch is saved)"),
    ]
    if state.watch >= places.OUTSIDE_FROM_WATCH:
        entries.insert(9, ("SUIT / OUTSIDE", "exterior work. mind the checks"))
    if st.has_flag(state, "QUESTION_ASKED"):
        entries.insert(0, ("ANSWER", "the channel is held open"))
    for name, blurb in entries:
        io.say(f"  {name:<22} {blurb}", "os")
    io.say("(single letters serve: S D E L W T J R. the night is only "
           "so long; the deeper boards will tell you when it has grown "
           "late.)", "dim")
    return state, None


def _status(state: GameState, rest: str, io: IO) -> Result:  # noqa: ARG001
    io.say(f"VESPER STATION — EPOCH {reports.epoch(state):,} — "
           f"WATCH {state.watch} OF {FINAL_WATCH}", "os")
    io.say(watches.duties_line(state), "os")
    io.say(f"THE HOUR: {watches.hour_label(state.acts)}", "os")
    if state.watch >= 8:
        observer = ("REMY" if st.has_flag(state, "QUESTION_ASKED")
                    else f"{state.observer.upper()} (UNVERIFIED)")
        io.say(f"OBSERVER OF RECORD: {observer}", "os")
    io.art([
        "  " + draw.render_gauge("GENERATOR", rituals.generator_fraction(state)),
        "  " + draw.render_gauge("MOISTURE", rituals.plant_fraction(state)),
    ])
    if st.generator_warning_active(state):
        io.say("WARNING: GENERATOR CYCLE IRREGULAR. TEND IT.", "alert")
    io.say(f"CATALOGUE: {catalog.count_visible(state)} SOURCES ON THE "
           f"CURRENT PLOT. ANNOTATIONS IN YOUR HAND: {len(state.witnessed)}.",
           "os")
    io.say(f"JOURNAL: {len(state.journal)} ENTRIES.", "os")
    return state, None


def _scan(state: GameState, rest: str, io: IO) -> Result:  # noqa: ARG001
    already = st.has_flag(state, f"SCANNED_{state.watch}")
    io.say(f"SCANNING SECTOR — EPOCH {reports.epoch(state):,}", "os")
    io.pause(0.5)
    lines = draw.render_sky(
        catalog.visible_stars(state),
        width=catalog.SKY_WIDTH,
        height=catalog.SKY_HEIGHT,
        absent=catalog.absent_region(state),
    )
    io.art(["  " + line for line in lines])
    io.say(f"SOURCES RESOLVED: {catalog.count_visible(state)}", "os")
    if already:
        io.say("the sky does not change because you ask it twice. that "
               "used to be a comfort.", "dim")
        return state, None
    state = st.add_flag(state, f"SCANNED_{state.watch}")
    if catalog.front_active(state) and not st.has_flag(state, "SEEN_FRONT"):
        state = st.add_flag(state, "SEEN_FRONT")
        io.say("the east third of the plot has not gone dark. dark "
               "resolves; dark is a reading. the plot simply stops "
               "being a plot there, grain and grid and border, as if "
               "the instrument had been asked to chart the inside of "
               "the word 'no'.")
    elif catalog.new_removals(state):
        io.say("PLOT DISAGREES WITH ARCHIVE COUNT. RUN DIFF.", "alert")
    elif state.watch == 1:
        io.say("the plotter draws the sector line by line, the stylus "
               "whispering across the paper like something small "
               "walking on snow, and the sky you know assembles "
               "itself dot by dot under the red lamp. all present. "
               "you initial the count the way you have initialled "
               "ten thousand counts, and the initialling is the "
               "point: somebody looked.", "dim")
    return state, None


def _diff(state: GameState, rest: str, io: IO) -> Result:  # noqa: ARG001
    if not st.has_flag(state, f"SCANNED_{state.watch}"):
        io.say("DIFF: NO PLOT FOR THIS EPOCH. RUN SCAN FIRST.", "os")
        return state, None
    removals = catalog.new_removals(state)
    state = st.add_flag(state, f"DIFFED_{state.watch}")
    if not removals:
        io.say("DIFF: PLOT AGREES WITH ARCHIVE.", "os")
        if state.watch == 1:
            io.say("agreement, the dull gold standard of the trade. you "
                   "would not trade it for interesting. you have seen "
                   "what interesting does to a catalogue.", "dim")
        return state, None
    io.say("DIFF —", "os")
    io.say("  DESIGNATION        ARCHIVE                 YOUR RECORD", "os")
    for i, star in enumerate(removals):
        shown = term.glitch(f"{star.id:<12}", severity=0.18,
                            seed=state.watch * 31 + i)
        label = f" — {star.name}" if star.name else ""
        retained = catalog.is_retained(star, state)
        right = ("ANNOTATION RETAINED" if retained
                 else "ACCESSION IN YOUR HAND")
        io.say(f"  {shown}     NO SUCH SOURCE          {right}{label}", "os")
    io.say(f"REMOVALS THIS EPOCH: {len(removals)}. EXTINCTION EVENTS "
           f"LOGGED: 0.", "os")
    io.pause()
    if state.watch == 2:
        io.say("not dimmed. not occluded. removed — from the archive, "
               "from the ephemerides, from the index of the index. the "
               "record does not say the sources died. the record says "
               "you have been initialling empty sky for forty years, "
               "and the record is signed by everyone but you.")
    elif state.watch == 3:
        io.say("the Ember Gate tonight. a binary since before the "
               "catalogue was a catalogue — and the archive now holds "
               "one star and one apology of arithmetic, a companion "
               "orbiting a mass that is no longer permitted to have "
               "been. the numbers still balance. they balance around a "
               "held breath.")
    elif state.watch == 5:
        io.say("the Pilgrim is in the column tonight. your first "
               "accession. you were twenty-six; you measured its "
               "motion four nights running before you dared claim it, "
               "and Okonkwo signed the accession with both your names "
               "because, he said, a first star should be witnessed "
               "twice. the archive now witnesses it zero times. you "
               "make up the difference.")
    elif state.watch == 6:
        io.say("Weir's Star. they named it the day they buried her — "
               "the Bureau's one recorded act of sentiment, a woman's "
               "whole watch folded into a designation. the archive has "
               "tonight unfolded it. there is no Weir's Star; there "
               "was, accordingly, no Weir. the chair arm in the dome "
               "continues to hold two initials, cut deep, in a medium "
               "that has never heard of the archive.")
    elif state.watch == 8:
        io.say("the Lantern. the first place your eye goes. the first "
               "star every keeper showed to every visitor the station "
               "ever had, back when it had them — the one light in "
               "the sector that never needed the trick of looking "
               "away. the column holds it now between VS-0479 and "
               "VS-0512 as if it were a line item. you initial the "
               "diff, because the duty is the duty, and your pen "
               "presses hard enough to be read from the back of the "
               "page.")
    elif state.watch >= 7:
        io.say("you no longer check the archive against your journal. "
               "you check your journal against your memory, and you do "
               "it with the door of the dome bolted, quietly, like a "
               "man counting money in a bad town.")
    return state, None


def _eye(state: GameState, rest: str, io: IO) -> Result:
    if catalog.by_id(rest) is not None:
        state = _spend(state, io)
    return eyepiece.look(state, rest, io), None


def _listen(state: GameState, rest: str, io: IO) -> Result:  # noqa: ARG001
    state = _spend(state, io)
    return wire.listen(state, io), None


def _report(state: GameState, rest: str, io: IO) -> Result:  # noqa: ARG001
    return reports.file_report(state, io), None


def _journal(state: GameState, rest: str, io: IO) -> Result:
    verb, _, _ = rest.upper().partition(" ")
    if verb == "WRITE":
        return _journal_write(state, io), None
    if verb == "READ":
        return _journal_read(state, io), None
    if verb == "COPY":
        return _journal_copy(state, io), None
    if verb == "BURN":
        return _journal_burn(state, io)
    io.say("JOURNAL WRITE — take up the pen. JOURNAL READ — the kept "
           "pages. JOURNAL COPY — re-write what is fading.", "os")
    return state, None


def _journal_write(state: GameState, io: IO) -> GameState:
    io.say(watches.pen_prompt(state.watch), "dim")
    io.say("you take up the pen. (finish with a single '.' on its own "
           "line; an empty first line leaves the page blank.)", "dim")
    lines: list[str] = []
    while True:
        line = io.ask("✎ ")
        if line.strip() == ".":
            break
        if not line.strip() and not lines:
            break
        if not line.strip():
            continue
        lines.append(line.strip())
    text = " ".join(lines).strip()
    if not text:
        io.say("the page stays blank tonight. blank is also a record.",
               "dim")
        return state
    state = st.add_journal(state, text)
    state = _spend(state, io)
    io.say("ink, in a hand. the one archive with a single reader and no "
           "editor. you blot it and close the book.", "dim")
    return state


def _journal_read(state: GameState, io: IO) -> GameState:
    living = st.living_journal(state)
    if not living:
        io.say("the journal falls open at the elastic. nothing in your "
               "hand yet this tour of watches. the earlier keepers' "
               "volumes are shelved in the dome, spines sun-faded by a "
               "lamp pretending to be a sun.", "dim")
        return state
    faded_any = False
    for index, entry in living:
        fade = watches.journal_fade(state.watch, entry.watch)
        shown = draw.erase_words(entry.text, fade,
                                 seed=index * 31 + entry.watch)
        faded_any = faded_any or shown != entry.text
        io.art(["  " + line for line in
                draw.render_page([shown], title=f"WATCH {entry.watch}")])
    if faded_any and not st.has_flag(state, "NOTICED_FADE"):
        state = st.add_flag(state, "NOTICED_FADE")
        io.say("the ink has not faded. fading leaves brown ghosts, and "
               "you know them. these words are gone the way the "
               "sources are gone: with the paper unmarked, as if your "
               "hand had skipped them in the writing — as if you had "
               "always, carefully, written around holes the exact "
               "shape of what you meant.")
    return state


def _journal_copy(state: GameState, io: IO) -> GameState:
    candidates = []
    for index, entry in st.living_journal(state):
        fade = watches.journal_fade(state.watch, entry.watch)
        if fade <= 0:
            continue
        shown = draw.erase_words(entry.text, fade,
                                 seed=index * 31 + entry.watch)
        missing = sum(1 for tok in shown.split() if draw.GONE_CHAR in tok)
        if missing:
            candidates.append((fade, index, entry, missing))
    if not candidates:
        io.say("JOURNAL: NO PAGE NEEDS THE PEN.", "os")
        io.say("nothing has faded that you could mend tonight. ahead of "
               "the losses, for once. it will not last, and it counts "
               "anyway.", "dim")
        return state
    candidates.sort(key=lambda c: (-c[0], c[1]))
    _, index, entry, missing = candidates[0]
    fresh_text = draw.erase_words(entry.text, 0.01,
                                  seed=state.watch * 97 + index)
    state = st.supersede_journal(state, index)
    state = st.add_journal(state, fresh_text)
    state = _spend(state, io)
    io.say(f"you take the watch-{entry.watch} page and re-write it "
           "fresh, word by missing word, filling the holes from "
           "memory. most come back — your hand remembers the shapes "
           "even where the paper forgot them. one does not. you write "
           "around it, leaving a gap the shape of your faith that it "
           "was there.")
    io.say(f"RESTORED: {max(0, missing - 1)} OF {missing} WORDS. "
           "PAGE RE-ENTERED IN FRESH INK.", "os")
    io.say("re-copying the book. Remy's volume mentions the practice, "
           "you suddenly recall — 'a catalogue is not the paper. it is "
           "the act, renewed.' you had always read that as philosophy.",
           "dim")
    return state


def _journal_burn(state: GameState, io: IO) -> Result:
    if state.watch < FINAL_WATCH:
        io.say("there are nights the incinerator door has a look about "
               "it. not tonight. the book goes back in the drawer.",
               "dim")
        return state, None
    io.say("the incinerator door swings light on its hinge. forty years "
           "of keeping, one armful. this is the one act on the station "
           "the terminal has no board for and the archive no field.",
           "dim")
    answer = io.ask("burn ▸ type BURN to confirm, anything else to keep ▸ ")
    if answer.strip().upper() != "BURN":
        io.say("you put the book back. your hands are steadier for "
               "having weighed it.", "dim")
        return state, None
    state = st.add_flag(state, "BURNED")
    return st.set_ending(state, "QUIET"), "ended"


def _shelf(state: GameState, rest: str, io: IO) -> Result:
    if rest.strip().upper() in shelf.KEEPERS:
        state = _spend(state, io)
    return shelf.open_shelf(state, rest, io), None


def _walk(state: GameState, rest: str, io: IO) -> Result:
    place = rest.strip().upper()
    if place == "PLANT ROOM":
        place = "PLANT"
    if place in places.PLACES:
        state = _spend(state, io)
    return places.walk(state, rest, io), None


def _tend(state: GameState, rest: str, io: IO) -> Result:
    if rest.strip().upper() in rituals.THINGS:
        state = _spend(state, io)
    return rituals.tend(state, rest, io), None


def _suit(state: GameState, rest: str, io: IO) -> Result:
    return places.suit_check(state, rest, io), None


def _outside(state: GameState, rest: str, io: IO) -> Result:  # noqa: ARG001
    state = places.go_outside(state, io)
    return state, ("ended" if state.ending else None)


def _answer(state: GameState, rest: str, io: IO) -> Result:  # noqa: ARG001
    if not st.has_flag(state, "QUESTION_ASKED"):
        io.say("ANSWER: NO CHANNEL IS HELD OPEN.", "os")
        io.say("nothing has asked you anything. the sky owes you no "
               "questions, and you would do well to stop rehearsing "
               "answers.", "dim")
        return state, None
    io.say("the sending key is under your hand. the carrier is open "
           "and the east is listening the way the east does "
           "everything now: entirely.", "dim")
    io.say("type what you will send. an empty line sits back from the "
           "key.", "dim")
    words = io.ask("send ▸ ").strip()
    if not words:
        io.say("you take your hand off the key. the carrier stays open "
               "behind you all night, a door ajar in a house where "
               "you now know you are not alone.", "dim")
        return state, None
    state = st.set_final_words(state, words)
    return st.set_ending(state, "ANSWER"), "ended"


def _sleep(state: GameState, rest: str, io: IO) -> Result:  # noqa: ARG001
    return state, "sleep"


def _quit(state: GameState, rest: str, io: IO) -> Result:  # noqa: ARG001
    return state, "quit"


_COMMANDS = {
    "HELP": _help,
    "STATUS": _status,
    "SCAN": _scan,
    "DIFF": _diff,
    "EYE": _eye,
    "LISTEN": _listen,
    "REPORT": _report,
    "JOURNAL": _journal,
    "SHELF": _shelf,
    "WALK": _walk,
    "TEND": _tend,
    "SUIT": _suit,
    "OUTSIDE": _outside,
    "ANSWER": _answer,
    "SLEEP": _sleep,
    "QUIT": _quit,
}
