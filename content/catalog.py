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

from engine.state import GameState

SKY_WIDTH = 60
SKY_HEIGHT = 12

# The front crosses the sector on the final watch and takes the eastern
# third of the plot with it — stars, grain, and the border alike.
FRONT_RECT = (40, 0, 59, 11)
FRONT_WATCH = 7


@dataclass(frozen=True)
class Star:
    id: str
    x: int
    y: int
    mag: int
    gone: int | None = None  # watch on which it is removed; None = stays
    name: str = ""
    note: str = ""  # one catalogue-margin line, shown by EYE


ALL: tuple[Star, ...] = (
    # ── the named ones ────────────────────────────────────────────────
    Star("VS-0001", 8, 6, 2, None, "the first entry",
         "oldest line in the catalogue. the margin holds four words in "
         "the first keeper's hand: STILL THERE. STILL HERE."),
    Star("VS-0088", 22, 3, 1, 6, "the Lantern",
         "brightest source in the sector. every keeper has shown it to "
         "someone once. there is no one left to show it to, and it is "
         "still the first place your eye goes."),
    Star("VS-0141", 47, 8, 2, 5, "Weir's Star",
         "named for the keeper who died in the dome chair with the "
         "eyepiece still warm. the Bureau let the name stand. it was "
         "cheaper than an inquiry."),
    Star("VS-0202", 15, 9, 2, 4, "the Pilgrim",
         "proper motion too fast for a star, too steady for a ship. "
         "your first accession, forty years ago. you were proud of it. "
         "you are still proud of it."),
    Star("VS-0301", 33, 5, 2, 3, "the Ember Gate",
         "eastern component of the old binary. the catalogue lists an "
         "orbital period and, in older editions, a superstition."),
    Star("VS-0302", 35, 5, 3, None, "",
         "western companion of VS-0301. it continues to orbit. the "
         "archive is no longer prepared to say what."),
    # ── the numbered sky ──────────────────────────────────────────────
    Star("VS-0117", 4, 2, 3, None),
    Star("VS-0126", 11, 4, 3, None),
    Star("VS-0135", 18, 7, 3, None),
    Star("VS-0158", 26, 10, 3, 6),
    Star("VS-0163", 29, 2, 2, 6),
    Star("VS-0189", 38, 9, 3, 5),
    Star("VS-0214", 42, 4, 3, 5),
    Star("VS-0227", 45, 1, 2, 5),
    Star("VS-0240", 50, 6, 3, 4),
    Star("VS-0256", 53, 3, 2, 4),
    Star("VS-0261", 57, 9, 3, 4),
    Star("VS-0288", 6, 11, 3, 3),
    Star("VS-0299", 24, 0, 3, 3),
    Star("VS-0326", 55, 0, 3, 2),
    Star("VS-0417", 58, 11, 3, 2),
    Star("VS-0433", 2, 8, 3, 6),
    Star("VS-0451", 13, 1, 3, 6),
    Star("VS-0468", 31, 8, 3, 6),
    Star("VS-0479", 40, 11, 3, 6),
    Star("VS-0490", 20, 5, 3, None),
)


def by_id(designation: str) -> Star | None:
    wanted = designation.strip().upper()
    for star in ALL:
        if star.id == wanted:
            return star
    # allow the human names too; he would use them
    lowered = designation.strip().lower()
    for star in ALL:
        if star.name and star.name.lower() == lowered:
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
