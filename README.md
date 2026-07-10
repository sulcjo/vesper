# VESPER

*A terminal game about being the last person still looking up.*

The universe is old. The sky is mostly embers, the enclaves stopped
answering centuries ago, and one observatory still keeps the sky
catalogue — because the watch has always been kept. You are the
observer. Seven watches remain.

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
`VESPER_HOME`). A watch takes a few minutes; a full game under an hour.
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
