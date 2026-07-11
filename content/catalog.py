"""The sky catalogue: every source, its place on the plot, and the
watch on which it stops having existed.

Removal is not destruction. A removed source is not dark — it is
uncatalogued, unarchived, unremembered by everything except, for a
while, the observer. A designation the observer has put his eye to
persists on the plot one watch past its removal: the archive calls
this OBSERVER ANNOTATION RETAINED, and files no further objection.
"""

from __future__ import annotations

from dataclasses import dataclass

from engine.state import FINAL_WATCH, GameState

SKY_WIDTH = 60
SKY_HEIGHT = 12

# The front crosses the sector on the final watch and takes the eastern
# third of the plot with it — stars, grain, and the border alike.
FRONT_RECT = (40, 0, 59, 11)
FRONT_WATCH = FINAL_WATCH


@dataclass(frozen=True)
class Star:
    id: str
    x: int
    y: int
    mag: int
    gone: int | None = None  # watch on which it is removed; None = stays
    name: str = ""  # the real name, from the old sky
    folk: str = ""  # what the keepers call it
    note: str = ""  # one catalogue-margin line, shown by EYE


# The last sky is the real sky. Nearly everything bright died long
# ago; what remains of our neighbourhood is the red dwarfs — Proxima,
# Barnard's, Wolf 359, TRAPPIST-1 — burning their trillion-year
# candles, and the cooled remnants of the famous dead.
ALL: tuple[Star, ...] = (
    # ── the named ones ────────────────────────────────────────────────
    Star("VS-0001", 8, 6, 2, None, "Sol", "the first entry",
         "the home star. a black remnant now, past seeing except by "
         "memory of where to look, and the catalogue's oldest line. "
         "the margin holds four words in the first keeper's hand: "
         "STILL THERE. STILL HERE."),
    Star("VS-0088", 22, 3, 1, 8, "Sirius", "the Lantern",
         "the Dog Star — the brightest thing the old sky had, and its "
         "white remnant is the brightest ember the sector has left. "
         "every keeper has shown it to someone once. there is no one "
         "left to show it to, and it is still the first place your "
         "eye goes."),
    Star("VS-0141", 47, 8, 2, 6, "Ross 128", "Weir's Star",
         "the books list it as Ross 128. the Bureau let her name "
         "stand over it when she died in the dome chair mid-count — "
         "its one recorded act of sentiment. it was cheaper than an "
         "inquiry."),
    Star("VS-0202", 15, 9, 2, 5, "Barnard's Star", "the Pilgrim",
         "the fastest walker the old sky had — proper motion too "
         "quick for dignity, too steady for a ship. your first "
         "accession re-confirmation, forty years ago. you were proud "
         "of it. you are still proud of it."),
    Star("VS-0301", 33, 5, 2, 3, "Alpha Centauri", "the Ember Gate",
         "the double lamp: nearest neighbours of the home star, first "
         "port the species ever wanted and last it let go of. two "
         "white remnants about a common hearth. the catalogue lists "
         "an orbital period and, in older editions, a superstition."),
    Star("VS-0302", 35, 5, 3, None, "Proxima", "",
         "the little red sister. trillions of years in her yet — she "
         "will outlive the catalogue, the Bureau, and the count. she "
         "continues to orbit. the archive is no longer prepared to "
         "say what."),
    Star("VS-0350", 27, 6, 2, 7, "Tau Ceti", "the Furnaces",
         "the swarm at Tau Ceti — points resolved as one to the naked "
         "eye. the old books say they were lit, not born: the last "
         "great work, from when the species still built at that size. "
         "the archive files this under folklore. the archive was not "
         "there."),
    Star("VS-0527", 9, 0, 2, None, "Omega Centauri", "Candle Row",
         "the old globular, a million ancient suns kept in one jar. "
         "keepers rest their eyes on it between counts — a memory of "
         "what the whole sky was like, kept small, like a coal "
         "carried in a tin."),
    Star("VS-0256", 53, 3, 2, 4, "61 Cygni", "",
         "the first star whose distance a human being ever measured — "
         "Bessel, with a heliometer, when the species was young. the "
         "counting began there, in a sense. it is in the diff "
         "column tonight, which is a sentence you refuse to finish."),
    Star("VS-0468", 31, 8, 3, 8, "TRAPPIST-1", "",
         "seven small worlds around a coal. the books disagree about "
         "whether anyone ever woke there, and are gone now, so the "
         "disagreement is settled the way everything is settled."),
    Star("VS-0227", 45, 1, 2, 6, "Kapteyn's Star", "",
         "the old halo wanderer — born before the galaxy's disc, "
         "passing through the neighbourhood on business of its own. "
         "even the archive used to write it with a kind of respect."),
    # ── the numbered sky (the real neighbourhood, what's left of it) ──
    Star("VS-0117", 4, 2, 3, None, "Lacaille 9352"),
    Star("VS-0126", 11, 4, 3, None, "Ross 154"),
    Star("VS-0135", 18, 7, 3, None, "GJ 1061"),
    Star("VS-0158", 26, 10, 3, 6, "Teegarden's Star"),
    Star("VS-0163", 29, 2, 2, 7, "Luyten's Star"),
    Star("VS-0189", 38, 9, 3, 6, "Ross 248"),
    Star("VS-0214", 42, 4, 3, 5, "Wolf 1061"),
    Star("VS-0240", 50, 6, 3, 4, "Gliese 876"),
    Star("VS-0261", 57, 9, 3, 5, "YZ Ceti"),
    Star("VS-0288", 6, 11, 3, 3, "DX Cancri"),
    Star("VS-0299", 24, 0, 3, 4, "Wolf 359"),
    Star("VS-0326", 55, 0, 3, 2, "EZ Aquarii"),
    Star("VS-0417", 58, 11, 3, 2, "GJ 1002"),
    Star("VS-0433", 2, 8, 3, 7, "Groombridge 34"),
    Star("VS-0451", 13, 1, 3, 7, "Lacaille 8760"),
    Star("VS-0479", 40, 11, 3, 8, "Ross 614"),
    Star("VS-0490", 20, 5, 3, None, "Lalande 21185"),
    Star("VS-0503", 44, 7, 3, 8, "Struve 2398"),
    Star("VS-0512", 51, 10, 3, 8, "LHS 1140"),
)


def by_id(designation: str) -> Star | None:
    wanted = designation.strip().upper()
    for star in ALL:
        if star.id == wanted:
            return star
    # allow the real names and the keepers' folk names; he uses both
    lowered = designation.strip().lower()
    for star in ALL:
        if star.name and star.name.lower() == lowered:
            return star
        if star.folk and star.folk.lower() == lowered:
            return star
    return None


def is_retained(star: Star, state: GameState) -> bool:
    """Removed this very watch, but held on the plot by witness."""
    return (
        star.gone is not None
        and star.gone == state.watch
        and star.id in state.witnessed
    )


def is_visible(star: Star, state: GameState) -> bool:
    if front_active(state) and in_front(star):
        return False
    if star.gone is None:
        return state.watch < FRONT_WATCH or not in_front(star)
    return state.watch < star.gone or is_retained(star, state)


def in_front(star: Star) -> bool:
    x0, y0, x1, y1 = FRONT_RECT
    return x0 <= star.x <= x1 and y0 <= star.y <= y1


def front_active(state: GameState) -> bool:
    return state.watch >= FRONT_WATCH


def absent_region(state: GameState) -> tuple[int, int, int, int] | None:
    return FRONT_RECT if front_active(state) else None


def visible_stars(state: GameState) -> list[tuple[int, int, int]]:
    return [(s.x, s.y, s.mag) for s in ALL if is_visible(s, state)]


def new_removals(state: GameState) -> list[Star]:
    """Sources whose removal lands on this watch's scan."""
    return [s for s in ALL if s.gone == state.watch]


def removed_so_far(state: GameState) -> list[Star]:
    return [s for s in ALL if s.gone is not None and s.gone <= state.watch]


def count_visible(state: GameState) -> int:
    return len(visible_stars(state))
