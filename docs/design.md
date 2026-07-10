# VESPER — design

A terminal game about being the last person still looking up.

## Premise

The universe is old. Most of the sky is ember-red or gone dark, and the
enclaves of what remains of humanity stopped answering centuries ago —
not violently, just the way a conversation trails off. One observatory
still keeps the sky catalogue, because the watch has always been kept.

You are the observer. You have a generator, a corridor, a dome, a plant
in a jar, a clock that must be wound, and a journal you keep by hand.

The scans begin returning removals: sources that are not dying but
un-having-been. The archive agrees they never existed. Your journal —
and your memory — still list them. The front of un-having moves closer
every epoch: through the dead enclaves' carrier bands, through your own
past, toward the dome.

It is never named, never shaped, never explained — not even by the
game. It manifests only as absence, contradiction, and, twice, address.

## Design pillars

1. **The character first.** Signals matter, but the game centers on the
   observer: rituals, body, memory, the reasons he stays. Machine text
   is uppercase and procedural; his interiority is lowercase prose.
2. **Record vs eye vs memory.** The three witnesses disagree, in both
   directions, and the disagreement escalates. Nothing is resolved.
3. **Diegetic everything.** Every graphic is something the station
   would draw: sky plots, diff tables, amplitude strips, gauges,
   journal pages. No photographs. No pictures of the thing.
4. **Rare, fair deaths.** Two, both preceded by explicit repeated
   warnings. Death is written as an ending, not a game-over screen.

## Structure: seven watches

Wake → rituals and chores → SCAN → DIFF → optionally EYE a designation
→ sometimes LISTEN → REPORT to the Bureau → JOURNAL → SLEEP.

Signature mechanic: **the journal quotes you back.** JOURNAL WRITE
takes the player's own free-typed entries; later watches replay them
with words missing (deterministic). Witnessing matters mechanically:
designations the player has EYEd persist one epoch longer in the
catalogue after removal ("OBSERVER ANNOTATION RETAINED").

### Commands

HELP STATUS SCAN DIFF EYE <id> LISTEN REPORT
JOURNAL [WRITE|READ|BURN] WALK <place> TEND <thing> SLEEP QUIT
Late game: SUIT, OUTSIDE (dangerous, warned).

Places: dome, corridor, quarters, plant room, generator room.
Tendables: generator, clock, plant.

### Graphics (engine/draw.py, pure and testable)

- Sky plot: sparse dot grid (`* ∙ ·` by magnitude) inside a border.
  Dots thin watch by watch. Late: a region renders as absent cells and
  the plot's own border develops a gap where the front crosses it.
- DIFF tables with glitch-corrupted rows for never-having-been sources.
- LISTEN amplitude strip (`▁▂▃▄▅▆▇`), mostly noise, briefly too regular.
- Journal pages, bordered, with `▒▒` where words have gone.
- Gauges for generator, plant moisture. Mundane, warm, steady.

### Deaths

- COLD — generator warnings (from watch 4) ignored two watches running.
- OUTSIDE — going out with incomplete suit checks after being told, or
  staying past the third warning.

### Endings (watch 7)

- KEEPER — file the final report; the catalogue's last entry is an
  observer. A sliver of grace is permitted here, no more.
- QUIET — burn the journal, or simply lie down without filing.
- ANSWER — reply when the wire addresses you by a name you do not
  remember being yours. Written as language decay; unexplained.
- COLD / OUTSIDE — the deaths, written as endings.

## Architecture

    vesper.py              entry (--fast, --new; VESPER_FAST=1)
    engine/term.py         ANSI, typewriter + Ctrl+C skip, beat, glitch
    engine/state.py        frozen GameState + pure update functions
    engine/draw.py         pure renderers (sky, strip, gauge, page)
    engine/persistence.py  schema-versioned JSON save, VESPER_HOME
    engine/commands.py     parser + dispatch, injected IO (testable)
    engine/shell.py        boot, sign-in, watch loop, autosave, endings
    content/*.py           all prose and data — the story lives here only
    tests/                 engine behavior + content integrity + e2e

Python stdlib only. Immutable state. Files small.

## Out of scope (YAGNI)

Photos/ASCII stills of anything alive, inventory, map movement, combat,
sound, curses UI, explanations.
