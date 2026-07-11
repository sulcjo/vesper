"""LISTEN — the wire. The station's ear on what remains of everyone.

The wire is used sparingly and that is by design: most watches it
offers nothing but the old hiss, and the observer knows better than to
make a habit of hoping. The escalation runs: a dead enclave's beacon,
the beacon unhappening, the station's own voice coming back wrong, and
then — twice — address.
"""

from __future__ import annotations

from engine import draw, state as st
from engine.io import IO
from engine.state import GameState


def _noise(seed: int, n: int, lo: int = 0, hi: int = 3) -> list[int]:
    span = hi - lo + 1
    return [
        lo + (((i + 3) * (2 * seed + 1) * 2654435761) >> 11) % span
        for i in range(n)
    ]


def _strip(io: IO, levels: list[int]) -> None:
    io.art(["  " + draw.render_strip(levels)])


def listen(state: GameState, io: IO) -> GameState:
    io.say("WIRE: OPEN. ALL REGISTERED BANDS.", "os")
    io.pause()
    scene = _SCENES.get(state.watch, _scene_hiss)
    return scene(state, io)


def _scene_hiss(state: GameState, io: IO) -> GameState:
    _strip(io, _noise(state.watch, 48))
    io.say("hiss. the same hiss the first keeper heard, the exhaled "
           "breath of everything that ever burned. you listen the way "
           "other people used to sit by the sea.")
    io.say("WIRE: CARRIER ONLY. NO TRAFFIC.", "os")
    return state


def _scene_first_night(state: GameState, io: IO) -> GameState:
    _strip(io, _noise(1, 48))
    io.say("the hiss. the oldest sound there is — the exhaled breath "
           "of everything that ever burned, thinned across the dark "
           "until it is texture more than voice. Okonkwo called "
           "listening to it 'taking the sea air'. there has never "
           "been a sea within four light-years of this chair.")
    io.say("you sit with it a while anyway, the way he taught you on "
           "your first watch: gain low, eyes shut, until the ear "
           "stops hunting for words in it and lets it be weather. "
           "it has never once had words in it. hold on to that, he "
           "said. the night you hear words, come tell me.")
    io.say("WIRE: CARRIER ONLY. NO TRAFFIC.", "os")
    return st.add_flag(state, "TOOK_THE_SEA_AIR")


def _scene_hollow_fading(state: GameState, io: IO) -> GameState:
    _strip(io, _noise(3, 20) + [4, 1, 4, 1, 3, 0, 4, 1] + _noise(7, 20))
    io.say("BAND 9 — REGISTERED BEACON: SHACKLETON ENCLAVE, LUNA "
           "SOUTH.", "os")
    io.pause()
    io.say("the loop again, fainter. bezpečný přístav. vplouvejte "
           "pomalu. pozor na — and there the sentence steps on a "
           "missing board. one word gone from the middle, clean, no "
           "scratch of damaged tape, the surrounding syllables "
           "closing over the gap as if they had always been "
           "neighbours. the word for shoals. you knew it last watch. "
           "you learned it from a grammar book, forty years ago, and "
           "the grammar book is on your shelf, and you already know "
           "without standing up what its page will and will not "
           "hold.")
    io.say("you have heard tape rot. tape rot mumbles. this is not "
           "a mumble. this is an edit, and you note in the log, in "
           "your steadiest hand, that you cannot remember what the "
           "word used to be, and that you have heard the loop nine "
           "hundred times.", "dim")
    io.say("WIRE: TRAFFIC LOGGED. LOOP INTEGRITY 44% AND FALLING.", "os")
    return st.add_flag(state, "HEARD_THE_EDIT")


def _scene_hollow_hill(state: GameState, io: IO) -> GameState:
    _strip(io, _noise(2, 16) + [5, 2, 5, 2, 4, 1, 5, 2] * 2 + _noise(5, 16))
    io.say("BAND 9 — REGISTERED BEACON: SHACKLETON ENCLAVE, LUNA "
           "SOUTH.", "os")
    io.pause()
    io.say("the Shackleton loop. a woman's voice, nine hundred years "
           "dead, reading the harbour litany in one of old Earth's "
           "small languages — one you had to learn from a grammar "
           "book, the vowels worn smooth as river stones by nine "
           "centuries of playback. bezpečný přístav, she says. "
           "vplouvejte pomalu. pozor na mělčiny. safe harbour, more "
           "or less. come in slowly. mind the shoals.")
    io.say("and behind her voice, if you close your eyes and lean "
           "into the gain, the room she sat in: the creak of a "
           "chair, a door shutting somewhere down a hall, and — "
           "under everything — rain against a window. there was "
           "never rain at Shackleton. they piped the sound of old "
           "Earth storms into the concourse, the books say, for the "
           "comfort of it. a recording inside a recording: weather "
           "from a world already done raining.", "dim")
    io.say("nobody has come in slowly for centuries. the tape survived "
           "the enclave. you have long since stopped deciding whether "
           "that is terrible or kind.")
    io.say("WIRE: TRAFFIC LOGGED. LOOP INTEGRITY 61% AND FALLING.", "os")
    return st.add_flag(state, "HEARD_HOLLOW")


def _scene_unregistered(state: GameState, io: IO) -> GameState:
    flat = [1] * 10
    gap = [0, 0, 0]
    _strip(io, flat + gap + flat + gap + [1] * 22)
    io.say("BAND 9 —", "os")
    io.say("WIRE: NO REGISTERED BEACON ON THIS BAND.", "os")
    io.say("ARCHIVE: NO BEACON HAS EVER BEEN REGISTERED ON THIS BAND.", "os")
    io.pause()
    if st.has_flag(state, "HEARD_HOLLOW"):
        io.say("you sat here two watches ago and listened to her read "
               "the harbour litany. you could hum the cadence of it "
               "now. the archive holds no tape, no enclave, no woman — "
               "Shackleton it lists as a hole at the pole of the Moon, "
               "surveyed once, never settled. the hiss where her voice "
               "was has edges, like a room with the furniture taken "
               "out but the dents still in the carpet.")
    else:
        io.say("the hiss on band nine is wrong in a way you cannot put "
               "your finger on — structured, like silence poured into a "
               "mould of something. you find you do not want to know the "
               "shape, and you note that wanting in the log, because "
               "noting things is the whole of what you are for.")
    io.say("WIRE: BAND CLOSED AT OBSERVER REQUEST.", "os")
    return st.add_flag(state, "HEARD_UNHAPPENING")


def _scene_echo(state: GameState, io: IO) -> GameState:
    half = _noise(11, 22)
    _strip(io, half + [2, 2] + list(reversed(half)))
    io.say("WIRE: OWN CARRIER DETECTED — BEARING EAST.", "os")
    io.say("WIRE: PROPAGATION DELAY 3.1 SECONDS. NO REFLECTOR AT RANGE.", "os")
    io.pause()
    io.say("the station's own signature, coming back out of the east "
           "three seconds late. there is nothing out there to bounce off. "
           "you check the delay four times. the fourth time it is 2.9.")
    io.say("something is learning the shape of your voice, or the sky "
           "has grown a wall, and you honestly could not say which "
           "thought you prefer. you switch off the repeater. the echo "
           "continues for a further two seconds. then it stops, which is "
           "worse, because stopping means noticing.")
    io.say("WIRE: REPEATER OFFLINE. LOG AMENDED.", "os")
    return st.add_flag(state, "HEARD_ECHO")


def _scene_pulse(state: GameState, io: IO) -> GameState:
    _strip(io, [0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0] * 4)
    io.say("BAND 1 — REGISTERED: THE MERIDIAN PULSE. GREENWICH, "
           "EARTH.", "os")
    io.pause()
    io.say("the Meridian Pulse. one soft knock every four seconds, "
           "from the old zero line on the home world — the clock the "
           "species set its every other clock by, still counting "
           "epochs for a civilisation that has mostly stopped opening "
           "its mail. it is the oldest continuous signal in the sky. "
           "Okonkwo used to call it the pilot light.")
    io.say("nobody living has raised Earth itself. but the clock is "
           "wound, or winds itself, under the hill at Greenwich where "
           "the counting of hours was once a trade, and out of "
           "everything on the wire it is the one sound that has never "
           "once been strange. you let a dozen knocks go by, the way "
           "you would stand in a doorway listening to a house sleep.")
    io.say("WIRE: PULSE COUNT AGREES WITH STATION COUNT. ALL CLOCKS "
           "CONCUR.", "os")
    return st.add_flag(state, "HEARD_PULSE")


def _scene_pulse_wrong(state: GameState, io: IO) -> GameState:
    _strip(io, [0, 0, 4, 0, 0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 4, 0] * 2
           + [4, 4] + [0] * 6)
    io.say("BAND 1 — REGISTERED: THE MERIDIAN PULSE.", "os")
    io.pause()
    io.say("the knock is there, and then the knock is early, and then "
           "it is two knocks close together like a heart missing its "
           "footing. Earth's own clock. you time it against the wound "
           "clock for an hour. there is no drift. there is arithmetic "
           "— the intervals are shortening by a fixed ratio, patient "
           "as interest.")
    if st.has_flag(state, "HEARD_PULSE"):
        io.say("the pilot light is not going out. it is being turned "
               "down, by the hand of nothing, on a schedule. a clock "
               "cannot dread. you have the dread on, as it were, its "
               "behalf; that is what an observer is for.")
    io.say("WIRE: PULSE COUNT NO LONGER AGREES WITH STATION COUNT.", "os")
    io.say("WIRE: THE PULSE COUNT IS DECREASING.", "alert")
    return st.add_flag(state, "HEARD_PULSE_WRONG")


def _latest_journal_line(state: GameState) -> str | None:
    if not state.journal:
        return None
    return state.journal[-1].text


def _scene_first_address(state: GameState, io: IO) -> GameState:
    half = [0, 2, 0, 3, 0, 2] * 3
    _strip(io, half + [6] + list(reversed(half)))
    io.say("WIRE: TRAFFIC. BAND UNNUMBERED.", "os")
    io.pause()
    line = _latest_journal_line(state)
    if line:
        spoken = draw.erase_words(line, 0.3, seed=state.watch)
        io.say("a voice. not the hiss arranging itself into a voice — a "
               "voice, level, unhurried, without breath where breath "
               "should be, and with no room behind it: no chair, no "
               "walls, no distance, sound arriving the way print "
               "arrives on a page. it says:")
        io.say(f"    {spoken}", "alert")
        io.say("your own words. the ones you wrote by hand, in the "
               "journal, which has no wire to it and no eyes on it and "
               "has never left the drawer.")
    else:
        io.say("a voice. not the hiss arranging itself into a voice — a "
               "voice, level, unhurried, without breath where breath "
               "should be. it reads back your last sector report, "
               "verbatim, in the flat tone of a man counting stairs in "
               "the dark.")
        io.say("    NO CHANGE. NO ACTION FOLLOWS.", "alert")
    io.say("then the carrier folds shut. the hiss comes back like water "
           "closing. you sit for a long time with your hand on the gain, "
           "not turning it up.")
    io.say("WIRE: TRAFFIC COULD NOT BE LOGGED. NO SOURCE OF RECORD.", "os")
    return st.add_flag(state, "ADDRESSED_ONCE")


def _scene_second_address(state: GameState, io: IO) -> GameState:
    _strip(io, [0] * 18 + [7] + [0] * 18)
    io.say("WIRE: TRAFFIC. ALL BANDS AT ONCE.", "os")
    io.pause()
    io.say("the voice does not bother with the hiss tonight. it is "
           "simply present, the way the cold is present, on every band, "
           "under every band, in the bones of the set. it says:")
    io.say("    REMY.", "alert")
    io.say("    REMY. THE COUNT IS NEARLY RIGHT.", "alert")
    io.pause(0.8)
    io.say("Remy was the first keeper. Remy is four words of marginalia "
           "and a grave you have never found. you are not Remy. you know "
           "your own name; you wrote it in the sign-in book tonight, the "
           "way you have ten thousand times.")
    io.say(f"you check the sign-in book. it says REMY, in your "
           f"handwriting, all the way down every page, and you cannot "
           f"now entirely hear the name “{state.observer}” in "
           f"your own head without it sounding like something you were "
           f"holding for a stranger.", "dim")
    io.say("the carrier stays open. it is waiting. the set has never "
           "once waited in forty years.")
    io.say("WIRE: CHANNEL HELD OPEN. THE COMMAND 'ANSWER' IS RECOGNISED.",
           "os")
    return st.add_flag(state, "QUESTION_ASKED")


_SCENES = {
    1: _scene_first_night,
    3: _scene_hollow_fading,
    2: _scene_hollow_hill,
    4: _scene_unregistered,
    5: _scene_pulse,
    6: _scene_echo,
    7: _scene_pulse_wrong,
    8: _scene_first_address,
    9: _scene_second_address,
}
