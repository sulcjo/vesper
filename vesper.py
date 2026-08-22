#!/usr/bin/env python3
"""VESPER — a terminal game about being the last person still looking up.

Usage:
    python3 vesper.py           resume the saved watch, or begin
    python3 vesper.py --new     begin again from the sign-in book
    python3 vesper.py --fast    no typewriter pacing (also VESPER_FAST=1)
"""

from __future__ import annotations

import sys

from engine.shell import run


def _force_utf8_console() -> None:
    """Windows' legacy console (conhost, what a double-clicked .exe opens)
    often defaults stdio to a codepage that can't encode this game's
    em-dashes and box-drawing characters, raising UnicodeEncodeError deep
    into a later watch and killing the process with no visible traceback
    (the window closes with it). Force UTF-8 everywhere, tolerating
    anything the terminal still can't display rather than crashing on it.

    On Windows this also switches the console's own codepage to UTF-8
    (65001) so the characters actually render instead of just failing to
    crash — reconfiguring Python's side alone stops the exception but
    leaves the legacy codepage to mangle anything outside it."""
    if sys.platform == "win32":
        try:
            import subprocess
            subprocess.run(["chcp", "65001"], shell=True, capture_output=True)
        except OSError:
            pass
    for stream_name in ("stdout", "stderr", "stdin"):
        stream = getattr(sys, stream_name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    _force_utf8_console()
    return run(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
