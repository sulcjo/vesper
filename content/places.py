"""WALK — the station, five rooms and a door that should stay shut.

The observer's interiority lives in these scenes, one per room per
watch: early is routine, the middle is unease, the late watches are a
man deciding, room by room, what he is prepared to lose. The station's
history — its masons, its keepers, its dead suppliers — is told here
and nowhere else, in passing, the way a man who lives alone tells
things to a room.
"""

from __future__ import annotations

from collections.abc import Callable

from engine import state as st
from engine.io import IO
from engine.state import GameState

PLACES = ("DOME", "CORRIDOR", "QUARTERS", "PLANT", "GENERATOR")

OUTSIDE_FROM_WATCH = 8

Scene = str | tuple[str, ...] | Callable[[GameState, IO], None]


def walk(state: GameState, place: str, io: IO) -> GameState:
    place = place.strip().upper()
    if place in ("PLANT ROOM",):
        place = "PLANT"
    if place not in PLACES:
        io.say(f"WALK: NO SUCH PLACE — {place or '(NOWHERE)'}", "os")
        io.say("dome, corridor, quarters, plant room, generator room. "
               "the whole of the indoors. it used to feel small.", "dim")
        return state
    scene = _SCENES[place][state.watch]
    if callable(scene):
        scene(state, io)
    else:
        paragraphs = (scene,) if isinstance(scene, str) else scene
        for text in paragraphs:
            io.say(text)
    if place == "GENERATOR" and st.generator_warning_active(state):
        io.say("under everything, the stumble. a held breath where a "
               "beat should be. it is asking. machines this old only "
               "ask so many times.", "alert")
    return state


# ── dome — the instrument, and the line of keepers ────────────────────

def _dome_9(state: GameState, io: IO) -> None:
    io.say("the dome at the end of things. the chair, the tube, the "
           "brass circle of the shutter crank worn bright as a coin. "
           "every keeper who ever sat here is in the smoothness of "
           "that crank. you put your hand on it and all of them are "
           "briefly not gone.")
    if st.has_flag(state, "SAW_THE_OTHER"):
        io.say("you do not open the shutter. once was once.", "dim")


_DOME: dict[int, Scene] = {
    1: ("the dome smells of cold brass and machine oil, with something "
        "older underneath — dust warmed and re-warmed by lamplight "
        "until it has a kind of toast to it, the smell of every "
        "observatory there has ever been. one red work-lamp burns by "
        "the desk to spare your night eyes. somewhere up in the dark "
        "of the slit gears tick as the metal cools, a small patient "
        "sound, like the building counting to itself.",
        "the chair knows your shape; it should, it has had forty "
        "years to learn it. on the arm, half under your sleeve, are "
        "two initials, E. and W., cut with a pocket knife — not by "
        "Weir; her volume says she only sat still and let it "
        "happen, which for Weir was a kind of vow. the E. has no "
        "surname anywhere in the record. you rest your fingers in "
        "the grooves of the letters, once, the way you touch a "
        "railing on a stair you trust."),
    2: "the shutter is closed and the dome is a held breath. you can "
       "hear the grease cooling in the gears. through the vent, very "
       "far off, the generator keeps its pulse. a dome is a good "
       "instrument for listening to a station: everything arrives "
       "here eventually, sound and cold and news, all of it a little "
       "late, like the light.",
    3: "along the west wall, the shelf: four volumes, keeper-bound in "
       "generator-room leather, REMY to WEIR, the whole of the "
       "station's memory that was written on purpose. your own "
       "half-filled book will stand fifth. you run a thumb down the "
       "spines, dust to dust to dust to less dust. (the SHELF board "
       "will open them.)",
    4: "you notice you have started standing so that the eyepiece is "
       "between you and the east wall. an instrument between you and "
       "a direction, as if a direction could be interrupted. the "
       "noticing is worse than the standing.",
    5: "the mirror was ground at Shackleton, by hand, over eleven "
       "years, and carried up the scarp on a sledge by masons who "
       "reckoned the labour holy — the last light of the sky deserved "
       "one good eye to land in, they said. their mark is stamped in "
       "the cell: three dots over a curve, a face looking up. the "
       "town is gone, then unhappened. the mark holds its edge.",
    6: "Weir died in the chair with the eyepiece warm and her count "
       "half a column done, and the pad is still in the map drawer — "
       "you have never moved it. sixty-one sources ticked, the "
       "sixty-second line begun: a 'V', then nothing, the pencil "
       "trailing off the paper in a hair-fine stroke. the Bureau "
       "ruled the death orderly. the pencil line is the only part "
       "you have ever disagreed with.",
    7: "you catch yourself talking to the dome tonight, low, the way "
       "Okonkwo used to — telling it the count, the weather that "
       "there is no weather, the small news of the tea tin. the dome "
       "holds still the way rooms hold still for old men. you thank "
       "it. an observer's conscience must live somewhere; some nights "
       "it is easier to keep it in the woodwork than in the chest.",
    8: ("the crank, the chair, the cold circle of brass. you sit a "
        "while in the dark with your hand on the shutter gear and are, "
        "briefly, all of them at once: Remy's stubbornness, Sever's "
        "hands, Okonkwo's patience, Weir's unfinished V. everything "
        "that still works is a kept promise, and the dome is the "
        "oldest promise on the station.",
        "and you have known, for forty years, what the promise is "
        "underneath — you are not a fool and were never permitted to "
        "be one. the count is the plank a drowning species nailed "
        "between itself and the water: keep a record and the dark is "
        "not bottomless; be remembered and you have not entirely "
        "died. knowing this has never once made you let go. a man "
        "may see his plank clearly and love it. a man may drown "
        "well-attended, which the water cannot offer, and it turns "
        "out that was the bargain all along."),
    9: _dome_9,
}


# ── corridor — the station's bones ────────────────────────────────────

_CORRIDOR: dict[int, Scene] = {
    1: "forty paces of corridor, lit in sections that wake ahead of "
       "you with a click and a slow amber flutter, and time out "
       "behind with no sound at all. your boots ring differently "
       "over the fuel lines — you could walk it deaf and know where "
       "you were. walking it, you are always in one moving island "
       "of light. behind you, in the dark, is the rest of the human "
       "race. you have made this joke to yourself for forty years. "
       "it has stopped being a joke so gradually you cannot date "
       "the change.",
    2: "over the dome-end lintel, cut deep and filled with brass: "
       "XL PACES. Sever's work — the second keeper measured "
       "everything, doorways, ration tins, his own stride, and wrote "
       "the numbers into the station like a man sewing his name into "
       "his clothes before a journey. you touch the cold figures in "
       "passing. forty paces. still forty. some numbers hold.",
    3: "the walls are cut blocks, not prefab: glass-desert stone, "
       "quarried and dressed by the Shackleton masons in the same "
       "decade as the mirror. here and there a block carries a "
       "mason's mark — the little upturned face — and one, at knee "
       "height near the plant room, carries a child's handprint "
       "pressed into the sealant, small as a leaf. nobody logged "
       "whose. the station keeps it anyway.",
    4: "tonight you stop halfway and stand still until the light over "
       "your head gives up and clicks off, just to prove that the "
       "dark that arrives is your own ordinary dark, with your own "
       "heart in it and the far hum of the generator. it is. you "
       "stand in it a moment longer anyway, on principle, though you "
       "could not say which principle.",
    5: "there is a draft by the airlock frame that the station's "
       "drawings say cannot exist. Sever met the same draft, per his "
       "volume, and taped a thread to the frame to watch it move. "
       "you tape a thread to the frame. it hangs dead straight for "
       "an hour and then, once, lifts — toward the door. drafts go "
       "around obstacles. this one went toward.",
    6: "the third light section hesitates now before it wakes, an old "
       "man's pause between intending and standing. you have started "
       "saying good evening to it. it is the only thing on the "
       "station whose failing is honest — mechanical, datable, "
       "ordinary — and you find you are grateful to it for that, "
       "absurdly, the way you are grateful to weather in old books.",
    7: "your breath shows in the corridor tonight — but only along "
       "the east wall, a ribbon of fog that walks with you at "
       "shoulder height for ten paces and is gone. the west wall "
       "gives nothing. the thermometer, consulted twice, remains "
       "loyal. you log the ribbon under 'condensation, anomalous', "
       "and are proud, in a grey way, of the steadiness of the "
       "entry's handwriting.",
    8: "the lights wake ahead of you as they always have. you find "
       "you are grateful to them, individually, each one, the way "
       "you would be grateful to old dogs standing up one more time. "
       "everything that still works is a kept promise now, and the "
       "corridor is forty paces of kept promises.",
    9: "you walk it once tonight with the lights ordered off — hand "
       "on the rail, forty paces, boots finding the floor's known "
       "unevennesses like a tongue finding teeth. not a test of the "
       "corridor. a test of the walker. at the dome door you stand "
       "in the dark you crossed and inform the east, silently, that "
       "you know the way in your own house.",
}


# ── quarters — the man ────────────────────────────────────────────────

def _quarters_9(state: GameState, io: IO) -> None:
    io.say("cot made square. boots side by side. the photograph "
           "propped where it can see the room. everything a keeper "
           "owns, ready for inspection by nobody.")
    if state.journal:
        io.say("the journal lies where it always lies. whatever else "
               "is decided this epoch, it was written by a hand, and "
               "the hand was yours.", "dim")


_QUARTERS: dict[int, Scene] = {
    1: ("cot, chest, kettle, clock. the room smells of wool and "
        "paraffin and the ghost of ten thousand cups of tea, and it "
        "is exactly as large as a life needs to be, which surprised "
        "you once and does not now. the dent in the pillow is the "
        "truest record on the station: proof of ten thousand sleeps, "
        "unfalsifiable, in a medium the archive cannot reach.",
        "you sit on the cot a moment and let the springs say what "
        "they say. the tea tin on the shelf is down to dust and "
        "stems. you will make it anyway, later, because the kettle's "
        "rattle is one of the voices you still get to hear."),
    2: "the sign-in book lives on the shelf by the door, fat with "
       "years, its spine rebroken and relaid twice. five hands run "
       "through it: Remy's upright strokes, Sever's draughtsman "
       "block, Okonkwo's long forward lean like a man walking into "
       "wind, Weir's small exact letters, and then yours, page after "
       "page after page, changing so slowly across forty years that "
       "only by jumping decades can you catch yourself aging.",
    3: "in the chest, under the spare filters, there is a photograph. "
       "two people on a pier that no longer exists, over water that "
       "no longer exists, squinting into a sun that is a red coal "
       "now if it is anything. one of them is you. you say the other "
       "name out loud, once, into the quiet, like putting a coin in "
       "a jar against the dark to come.",
    4: "you do the tea arithmetic tonight, spoon against tin, the "
       "way Okonkwo taught you to do all supply sums: without hope "
       "as a variable. the last shuttle flew before Weir's watch. "
       "what is in the tin is what there is. eleven measures, you "
       "make it, and you are sixty days from nothing — which is to "
       "say, richer than the sky, which is out of nearly everything.",
    5: "you mend the elbow of your station coat with Weir's sewing "
       "kit — her name inked inside the lid in those small exact "
       "letters, needles kept bright in a fold of waxed cloth. thread "
       "the needle on the second try, old eyes, steady hands. a "
       "stitch is a very small kept promise, you think, pulling it "
       "tight. the coat has outlived four keepers. it is not going "
       "to fail on your watch either.",
    6: "you know the other face in the photograph better than your "
       "own. you knew the name last watch. you put the photograph "
       "back face down, which is not the same as forgetting, "
       "whatever the archive would make of it.",
    7: "before bed you print your own name on a slip of paper and "
       "fold it into your breast pocket, and are immediately, "
       "hotly, ashamed — a grown keeper, a man of records, carrying "
       "himself around like a label on a jar. you do not take it "
       "out of the pocket. shame is cheap. the name is not.",
    8: "you take the photograph out and prop it against the clock, "
       "faces out, deliberately. if the east wants the pier and the "
       "water and the sun and the name, let it come through the "
       "tick of an honest clock to take them.",
    9: _quarters_9,
}


# ── plant room — the life ─────────────────────────────────────────────

_PLANT: dict[int, Scene] = {
    1: "the plant room is two lamps, a jar, and the only green in "
       "four light-years. the lamps hum at a pitch just above the "
       "generator's, and the air in here is different air — thick, "
       "wet, faintly sweet, the condensation crawling the inside of "
       "the jar in beads that gather and let go, gather and let go. "
       "the manual calls it a psychological provision. the manual "
       "has never stood in here at 0300 with its face in the "
       "leaves, breathing.",
    2: "it is orchard stock, the plant — a cutting of a cutting of a "
       "tree that stood in the Shackleton concourse when Shackleton stood, come "
       "up the scarp on the last shuttle in a tin of wet cloth, "
       "logged by Okonkwo as 'provision, morale, one (1)'. the town "
       "that grew it has been unhappened. the cutting has not. you "
       "are careful never to say this out loud in here.",
    3: "condensation runs the jar in slow beads. the plant does not "
       "know about the catalogue. things keep needing water; this "
       "is, as far as you can tell, the universe's one remaining "
       "opinion, and you have decided to share it.",
    4: "pencil marks climb the jar's shoulder where four keepers "
       "have measured the reach of it, dated in four hands. you "
       "hold your flat palm at the newest leaf and add a mark, "
       "dated, in your own hand under the other four. growth, "
       "logged.",
    5: "you have moved the second chair in here — Weir's chair, by "
       "the inventory, though she never sat in it that you know of. "
       "you sit with the plant the way you would sit with a "
       "colleague on a hard night: no talk expected, both facing "
       "the lamp, as if it were weather.",
    6: "the plant has begun leaning into the lamp harder than the "
       "lamp deserves, all its leaves turned like a room of faces. "
       "you rotate the jar a quarter-turn, as always, to keep it "
       "growing even. by morning it has leaned back. not toward "
       "the east — you checked, compass in hand, feeling foolish. "
       "toward the light. good, you tell it, low. hold your heading.",
    7: "cold outside the door tonight, and the green smell stronger "
       "for it, the way bread smells more in a cold kitchen. you "
       "stand in it and breathe. four light-years of ember and "
       "static in every direction, and this one small wet room "
       "still smells like the middle of a summer that happened to "
       "someone.",
    8: "you carry the jar to quarters for the night, against the "
       "frost, walking the corridor slow as a server at some old "
       "rite, lamp trailing its cord behind you like a vestment. "
       "the leaves tick against your coat. if the last green thing "
       "in the sky spends its nights an arm's reach from the last "
       "keeper of the catalogue, that is not sentiment. that is "
       "consolidation of assets.",
    9: "you set the jar back under its lamp and top the water to the "
       "line. whatever this watch decides, the plant is not invited "
       "to the deciding; its work is leaves, and it is on schedule. "
       "you leave both lamps burning when you go. expense approved, "
       "keeper's authority, no signature required.",
}


# ── generator room — the heat ─────────────────────────────────────────

_GENERATOR: dict[int, Scene] = {
    1: "the heat meets you at the door like a hand on the chest. "
       "warm, loud, honest — the generator room is the one place on "
       "the station where the dark has to shout to be heard, and it "
       "loses. fuel oil sits in the air thick enough to taste, and "
       "the deckplates carry the rotation up through your boots and "
       "into your teeth, a rhythm your body has kept time with for "
       "so long that silence, when you leave, always arrives like a "
       "stumble. you check the fuel figure against the ledger, an "
       "arithmetic you could do dead, and may.",
    2: "the fuel is the desert, strictly speaking: Sever's "
       "synthesiser cracks the grey glass outside into something "
       "the burners will take, a trick he reverse-engineered from a "
       "mining manual and two failures that scorched his eyebrows "
       "off — his own volume says so, in draughtsman's block, with "
       "a diagram. the station eats the ground it stands on, slowly, "
       "politely. it has maybe a thousand years of ground.",
    3: "the pulse is steady. you stand a while in the heat and the "
       "noise, taking it on like a man refuelling.",
    4: "this is the station's third heart. the first two stand in "
       "the undercroft, stripped for parts, museum-still, tagged in "
       "Sever's hand: RETIRED WITH HONOURS 41,220 and the second "
       "one just RETIRED, because by then, his volume says, he had "
       "learned not to spend ceremony twice. you go down some "
       "watches and stand between them. every kept thing on this "
       "station is standing on the shoulders of a dead version of "
       "itself. so are you. so is the species. the trick, on the "
       "evidence, is to keep the current one turning.",
    5: "you repaint the red line on the pressure gauge tonight, the "
       "little liturgy of maintenance: brush, steady hand, the old "
       "line fainted to pink under forty years of heat. Okonkwo "
       "held that a keeper's real instrument was the station "
       "entire, and that paint was calibration. you get the line "
       "true on the first pass. you rinse the brush, cap the tin, "
       "and enter the time in the ledger.",
    6: "steady tonight. you put your palm flat on the housing and "
       "count the rotation against your own pulse, two rhythms "
       "neither young, both regular, and stand there a while in "
       "the warm noise like one old animal leaning on another.",
    7: "you bring your blanket down and sleep the first hour of the "
       "night in the generator room chair, against all standing "
       "orders, beside the third heart's noise. the cold is a "
       "landlord and the noise is the rent being paid, audibly, "
       "all night. it is the best hour of sleep you have had in "
       "twenty epochs. standing orders were written by people with "
       "neighbours.",
    8: "out here the cold is not an event. it is the landlord, and "
       "the generator is the rent, and the rent is due every hour "
       "of every watch forever. you check the feed, the filters, "
       "the figure in the ledger. paid up. paid up. paid up.",
    9: "steady. you rest your hand on the housing and feel the "
       "heartbeat of the last inhabited building in the sky, and "
       "privately, unprofessionally, you bless it.",
}


_SCENES: dict[str, dict[int, Scene]] = {
    "DOME": _DOME,
    "CORRIDOR": _CORRIDOR,
    "QUARTERS": _QUARTERS,
    "PLANT": _PLANT,
    "GENERATOR": _GENERATOR,
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
    if state.watch < OUTSIDE_FROM_WATCH:
        io.say("SUIT LOCKER: SEALED. NO EXTERIOR WORK IS SCHEDULED.", "os")
        io.say("there is no reason to go out. the cold is not curious "
               "about you. keep it that way.", "dim")
        return state
    if not which:
        done = [c for c in SUIT_CHECKS
                if st.has_flag(state, f"SUIT_{c}_{state.watch}")]
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
    return st.add_flag(state, f"SUIT_{which}_{state.watch}")


def go_outside(state: GameState, io: IO) -> GameState:
    if state.watch < OUTSIDE_FROM_WATCH:
        io.say("AIRLOCK: SEALED. NO EXTERIOR WORK IS SCHEDULED.", "os")
        io.say("you stand at the inner door a moment all the same, "
               "reading the frost patterns like a page.", "dim")
        return state
    missing = [c for c in SUIT_CHECKS
               if not st.has_flag(state, f"SUIT_{c}_{state.watch}")]
    if missing:
        if not st.has_flag(state, f"OUTSIDE_WARNED_{state.watch}"):
            io.say("AIRLOCK: SUIT PROTOCOL INCOMPLETE — " +
                   ", ".join(missing), "alert")
            io.say("AIRLOCK: OVERRIDE IS AVAILABLE. OVERRIDE IS NOT "
                   "ADVISED. A SECOND ATTEMPT THIS WATCH WILL BE "
                   "TREATED AS OVERRIDE.", "alert")
            io.say("the door would open. doors do not care. that has "
                   "always been the thing about doors.", "dim")
            return st.add_flag(state, f"OUTSIDE_WARNED_{state.watch}")
        io.say("AIRLOCK: OVERRIDE ACCEPTED.", "alert")
        state = st.add_flag(state, "OUTSIDE_OVERRIDE")
        return st.set_ending(state, "OUTSIDE")
    if st.has_flag(state, f"EXTERIOR_DONE_{state.watch}"):
        io.say("AIRLOCK: CYCLING. TETHER LIVE. BOTTLE LIVE.", "os")
        io.say("the array is swept; the couplings hold; your own boot "
               "prints from the last trip lie in the regolith, crisp "
               "as the hour you made them, and will outlast the "
               "catalogue. you stand at the top of the line a while, "
               "hand on the tether, not walking it, and go back in.")
        io.say("AIRLOCK: CYCLE COMPLETE. NO WORK LOGGED.", "os")
        return state
    return _outside_scene(state, io)


def _outside_scene(state: GameState, io: IO) -> GameState:
    io.say("AIRLOCK: CYCLING. TETHER LIVE. BOTTLE LIVE.", "os")
    io.pause(0.6)
    io.say("outside is the sound of your own blood and nothing else "
           "whatsoever — that, and what the boots bring up: the "
           "regolith's dry crunch arriving through your soles and "
           "shinbones, felt more than heard, each step a small "
           "report filed by the body. the ground is grey glass to "
           "the horizon, the Sea of Cold living up to both its "
           "names. above you the sky stands the way it has stood "
           "all your life — except in the east, where there is now "
           "a margin with nothing written in it.")
    io.say("and low over the southern rim, where it has hung since "
           "before there were eyes on this world to hang for: the "
           "Earth. dark, of course — a coin of deeper dark on the "
           "dark, home to whatever still keeps the Pulse wound. no "
           "keeper has ever caught it showing a light. every keeper "
           "has looked. you look now, on protocol, the oldest "
           "protocol there is.", "dim")
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
            return st.add_flag(state, "WENT_OUTSIDE",
                               f"EXTERIOR_DONE_{state.watch}")
        if line:
            io.say(line)
    return st.set_ending(state, "OUTSIDE")
