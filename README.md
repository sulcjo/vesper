# VESPER

*A terminal game about being the last person still looking up.*

This is our universe, very late. The bright stars died as the
physics always said they would; what remains of the real sky is the
red dwarfs — Proxima, Barnard's Star, Wolf 359 — burning their
trillion-year candles among the cooled remnants of the famous dead.
On the north rim of Mare Frigoris, the Sea of Cold, on Luna, one
observatory still keeps the sky catalogue — the far end of the
longest unbroken record our species ever kept, hand to hand back to
the clay of Babylon. You are the observer, fifth keeper of the
Vesper catalogue. Nine watches remain.

The scans have begun returning removals: sources that are not dying,
but un-having-been. The archive agrees they never existed. Your
journal, written by hand, still lists them.

## Run

Python 3.10+ — standard library only. No install.

```
python3 vesper.py           # resume the saved watch, or begin
python3 vesper.py --new     # start over from the sign-in book
python3 vesper.py --fast    # no typewriter pacing (or VESPER_FAST=1)
```

Progress autosaves after every command (to `~/.vesper/`, override with
`VESPER_HOME`). A watch takes a few minutes; a full game runs about an
hour, more if you read the old keepers' volumes — and you should.

The night is only so long: duties are always free, but the deeper
things — walking the rooms, the eyepiece, the wire, the shelf, the
pen — tire an old man. Choose. Single letters work for the common
boards (`S D E L W T J R`). What you write in the journal matters
more than you may at first suppose, and what fades can be fought:
`JOURNAL COPY`.

The station remembers finished watches. That is all that will be
said about that.
Type `HELP` at the prompt for the station's boards. `Ctrl+C` skips the
typewriter effect for the current passage.

Play with the sound of a fan or a heater somewhere in the room, if you
can arrange it.

## A note on dying

You can die. Rarely, fairly, and only after the station has told you
plainly what it needs. It will not happen by ambush. Everything else —
what to watch, what to answer, what to keep — is yours to decide, and
the game will not grade you. There are several endings. None of them
explains anything, which is a promise, not an apology.

## Development

```
python3 -m pytest tests/
```

Engine (`engine/`) is pure and tested; every line of story lives in
`content/`. See `docs/design.md`.

## Single-file build

```
python3 tools/build_pyz.py   # writes dist/vesper.pyz
python3 dist/vesper.pyz      # runs anywhere Python 3.10+ lives
```
