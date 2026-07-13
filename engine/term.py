"""Terminal presentation: color, pacing, and signal corruption.

Everything that touches a real TTY lives here so the rest of the engine
stays pure and testable. Pacing can be disabled globally (--fast, tests).
"""

from __future__ import annotations

import os
import random
import shutil
import sys
import textwrap
import time

WRAP_WIDTH_MAX = 78
CHAR_DELAY = 0.011
BEAT_DELAY = 0.35
CORRUPTION = "▒█░#&%@"

_fast = False


def set_fast(value: bool) -> None:
    global _fast
    _fast = value


def is_fast() -> bool:
    return _fast or os.environ.get("VESPER_FAST") == "1"


def _color_enabled() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty() and os.environ.get("TERM") != "dumb"


class Style:
    RESET = "\033[0m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    AMBER = "\033[33m"
    RED = "\033[31m"
    CYAN = "\033[36m"


def _truecolor_enabled() -> bool:
    if not _color_enabled():
        return False
    return os.environ.get("COLORTERM", "") in ("truecolor", "24bit")


# The station's monitor: aged phosphor. One palette, five duties.
_PHOSPHOR = {
    "os": (87, 217, 119),      # spring green — the machine speaking
    "prose": (184, 230, 192),  # pale phosphor — the man
    "dim": (96, 130, 104),     # moss — marginalia
    "alert": (255, 176, 0),    # amber — warnings
    "art": (111, 207, 143),    # mid green — instruments
}

_FALLBACK = {
    "os": (Style.GREEN,),
    "prose": (),
    "dim": (Style.DIM,),
    "alert": (Style.AMBER, Style.BOLD),
    "art": (Style.GREEN,),
}


def _cooled(rgb: tuple[int, int, int], watch: int) -> tuple[int, int, int]:
    """From watch 7 the whole monitor runs a little colder and dimmer,
    a few percent per watch — beneath notice, above perception."""
    if watch < 7:
        return rgb
    factor = 1.0 - 0.05 * (watch - 6)
    r, g, b = rgb
    return (int(r * factor), int(g * factor), min(255, int(b * 1.04)))


def kind_styles(kind: str, watch: int = 1) -> tuple[str, ...]:
    """Escape prefix(es) for a semantic line kind."""
    if _truecolor_enabled():
        r, g, b = _cooled(_PHOSPHOR.get(kind, _PHOSPHOR["prose"]), watch)
        color = f"\033[38;2;{r};{g};{b}m"
        if kind == "alert":
            return (color, Style.BOLD)
        return (color,)
    return _FALLBACK.get(kind, ())


def clear_screen() -> None:
    """Wipe to a fresh page. Only on a live terminal — piped output
    (tests, playtest scripts) must stay an honest transcript."""
    if _color_enabled() and not is_fast():
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def paint(text: str, *styles: str) -> str:
    if not styles or not _color_enabled():
        return text
    return "".join(styles) + text + Style.RESET


def width() -> int:
    return min(shutil.get_terminal_size((80, 24)).columns, WRAP_WIDTH_MAX)


def wrap(text: str, reserve: int = 0) -> list[str]:
    limit = max(20, width() - reserve)
    lines: list[str] = []
    for raw in text.split("\n"):
        if not raw.strip():
            lines.append("")
            continue
        indent = " " * (len(raw) - len(raw.lstrip(" ")))
        lines.extend(
            textwrap.wrap(
                raw,
                limit,
                initial_indent="",
                subsequent_indent=indent,
                drop_whitespace=True,
            )
            or [""]
        )
    return lines


def say(text: str, *styles: str, pace: float = CHAR_DELAY,
        indent: int = 0) -> None:
    """Print wrapped text with a typewriter cadence. Ctrl+C skips the effect."""
    pad = " " * indent
    for line in wrap(text, reserve=indent):
        line = pad + line if line else line
        painted = paint(line, *styles)
        if is_fast() or pace <= 0:
            print(painted)
            continue
        try:
            _type_line(line, styles, pace)
        except KeyboardInterrupt:
            # Finish the whole message instantly rather than eating it.
            set_fast(True)
            print(paint(line, *styles))
    sys.stdout.flush()


def _type_line(line: str, styles: tuple[str, ...], pace: float) -> None:
    prefix = "".join(styles) if styles and _color_enabled() else ""
    suffix = Style.RESET if prefix else ""
    sys.stdout.write(prefix)
    for char in line:
        sys.stdout.write(char)
        sys.stdout.flush()
        if not char.isspace():
            time.sleep(pace)
    sys.stdout.write(suffix + "\n")


def beat(seconds: float = BEAT_DELAY) -> None:
    """A held silence. The cheapest special effect there is."""
    if not is_fast():
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            set_fast(True)


def rule(char: str = "─") -> None:
    say(char * width(), Style.DIM, pace=0)


def glitch(text: str, severity: float = 0.08, seed: int | None = None) -> str:
    """Corrupt a fraction of characters. Deterministic when seeded (tests)."""
    rng = random.Random(seed)
    out = []
    for char in text:
        if char.strip() and rng.random() < severity:
            out.append(rng.choice(CORRUPTION))
        else:
            out.append(char)
    return "".join(out)
