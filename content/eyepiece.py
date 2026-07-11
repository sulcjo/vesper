"""EYE — the optical telescope. The one witness that is not a record.

The catalogue can be edited. The archive can agree to anything. The
eyepiece is a tube, a mirror, and an old man's eye, and for a while
that is enough to keep a star.
"""

from __future__ import annotations

from content import catalog
from engine import state as st
from engine.io import IO
from engine.state import GameState

_MAG_LOOK = {
    1: "the eyecup is cold against the orbit of your eye, and then "
       "there is no eyecup, no dome, no you — just the light, filling "
       "the field. after so much ember-red, a bright source feels "
       "almost rude. you let it hurt a little.",
    2: "you settle into the chair, find the focus by touch — the "
       "knurled wheel, a quarter-turn past the sticking point — and "
       "there it is. steady, small, certain. the kind of light the "
       "catalogue was invented for.",
    3: "faint. your own breath fogs the eyepiece and you wait out the "
       "clearing, and even then you have to look slightly away to "
       "see it at all — the old trick, letting the edge of the eye "
       "do the believing.",
}


def look(state: GameState, raw: str, io: IO) -> GameState:
    star = catalog.by_id(raw)
    if star is None:
        io.say(f"EYE: NO SUCH DESIGNATION — {raw.strip().upper() or '(NONE)'}", "os")
        io.say("you check the spelling twice. some nights you would swear "
               "you knew every name up there. tonight you let it go.", "dim")
        return state

    if catalog.front_active(state) and catalog.in_front(star):
        return _front_scene(state, star, io)

    state = st.witness(state, star.id)

    if star.gone is None or state.watch < star.gone:
        return _present_scene(state, star, io)
    if star.gone == state.watch:
        return _removed_today_scene(state, star, io)
    return _removed_past_scene(state, star, io)


def _title(star: catalog.Star) -> str:
    if star.name and star.folk:
        return f"{star.id} — {star.name}, {star.folk}"
    if star.name:
        return f"{star.id} — {star.name}"
    return star.id


def _present_scene(state: GameState, star: catalog.Star, io: IO) -> GameState:
    io.say(f"EYE: TRACKING {_title(star).upper()}", "os")
    io.pause()
    io.say(_MAG_LOOK[star.mag])
    if star.note:
        io.say(star.note, "dim")
    if star.id == "VS-0302" and state.watch >= 3:
        io.say("Proxima. you time her drift against the crosshair, out "
               "of habit. the period is unchanged: she swings around "
               "the place where Alpha Centauri was, keeping faith with "
               "masses the archive no longer lists. trillions of years "
               "left in her, the little red sister — she will outlive "
               "the count itself. the arithmetic still works. that is "
               "the part you don't like.")
    if star.id == "VS-0001":
        io.say("STILL THERE. STILL HERE.", "dim")
    io.say("ANNOTATION LOGGED. OBSERVER OF RECORD CONFIRMS SOURCE.", "os")
    return state


_RETAINED_AGAIN = (
    "there it is: small, stubborn, and — as of tonight — unofficial. "
    "you hold it in the crosshair a while, the way you would hold a "
    "door for someone slow.",
    "still burning, still denied. you log it against the archive's "
    "clean refusal and feel, absurdly, like a man vouching for a "
    "friend at a border post.",
    "present. uncatalogued. yours, then. the eye takes its careful "
    "minute and the pen does the rest.",
)


def _removed_today_scene(state: GameState, star: catalog.Star, io: IO) -> GameState:
    io.say(f"EYE: TRACKING {_title(star).upper()}", "os")
    io.say("ARCHIVE: NO SUCH SOURCE. NO SUCH SOURCE HAS BEEN CATALOGUED.", "os")
    io.pause()
    if not st.has_flag(state, "SEEN_RETENTION"):
        state = st.add_flag(state, "SEEN_RETENTION")
        io.say("and yet. you put your eye to the tube and there it is, "
               "exactly where forty years of your own handwriting says "
               "it should be. the archive is wrong. you are looking at "
               "the proof. the proof is very small and very far away, "
               "and no one else will ever check.")
        io.say("ANNOTATION LOGGED. RETENTION GRANTED — ONE EPOCH.", "os")
        io.say("one epoch. the system's little mercy. as if it were "
               "embarrassed.", "dim")
        return state
    index = (state.watch + len(star.id)) % len(_RETAINED_AGAIN)
    io.say(_RETAINED_AGAIN[index])
    io.say("ANNOTATION LOGGED. RETENTION GRANTED — ONE EPOCH.", "os")
    return state


def _removed_past_scene(state: GameState, star: catalog.Star, io: IO) -> GameState:
    io.say(f"EYE: SLEWING TO ARCHIVE COORDINATES — {star.id}", "os")
    io.say("ARCHIVE: COORDINATES CORRESPOND TO NO CATALOGUED SOURCE.", "os")
    io.pause()

    if star.id == "VS-0088" and state.watch >= 9:
        # the Lantern, the last look.
        io.say("the field where the Lantern stood is not empty. empty you "
               "know. empty is most of the sky and all of the corridor. "
               "this is other. the eye slides off it the way a word, said "
               "too many times, stops agreeing to mean.")
        io.say("ANNOTATOR: SUBJECT — [no noun]", "os")
        io.say("ANNOTATOR: MAGNITUDE — [declined]", "os")
        io.say("you sit back from the eyepiece. you do not look again. "
               "some instruments you only get to break once.")
        return st.add_flag(state, "SAW_THE_OTHER")

    if star.id == "VS-0350":
        io.say("the Furnaces' field, empty. whatever they were — born "
               "or built, stars or the species' one cathedral — the "
               "question has been settled in the oldest way: by "
               "removing the subject. even the folklore file is gone "
               "from the archive. you recite what you remember of it "
               "into the annotation field, deliberately, an old man "
               "smuggling a legend across a border.")
        io.say("ANNOTATION LOGGED. ARCHIVE OBJECTS TO ANNOTATION.", "os")
        return state
    if st.has_flag(state, "SEEN_EMPTY_FIELD"):
        variants = (
            "empty, in the way you have learned to read empty: "
            "closed over, seamless, nothing owed.",
            "the field again, and again nothing — not even the kind "
            "of nothing that remembers being something.",
            "you give the coordinates their minute of attention "
            "anyway. attendance is not contingent on attendance "
            "being returned.",
        )
        io.say(variants[(state.watch + len(star.id)) % len(variants)])
    else:
        state = st.add_flag(state, "SEEN_EMPTY_FIELD")
        io.say("nothing in the field. not a dimness where it burned "
               "down, not a gap the right shape. the sky has closed "
               "over the place like water over a stone that was never "
               "thrown.")
    if star.name:
        spoken = f"{star.folk or star.name}" if star.folk else star.name
        io.say(f"you say the name anyway, quietly, giving it one more "
               f"witness: {spoken}.", "dim")
    io.say("ANNOTATION LOGGED. ARCHIVE OBJECTS TO ANNOTATION.", "os")
    return state


def _front_scene(state: GameState, star: catalog.Star, io: IO) -> GameState:
    io.say(f"EYE: SLEWING TO ARCHIVE COORDINATES — {star.id}", "os")
    io.say("EYE: CANNOT ACQUIRE FOCUS. NO FOCAL PLANE.", "os")
    io.pause()
    io.say("you look into the east of the sector and there is nothing to "
           "fail to see. dark is something — dark is distance and dust and "
           "your own tired blood ticking in the retina. this is not dark. "
           "the tube might as well be capped, except the cap would be "
           "something too.")
    io.say("you close the shutter. your hands do it without being asked.")
    return st.add_flag(state, "EYED_THE_FRONT")
