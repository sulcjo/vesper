"""Pure character-cell renderers for the station's instruments.

Every function takes plain data and returns strings — no IO, no state,
no randomness. Determinism keeps them snapshot-testable and keeps the
horror authored rather than accidental.
"""

from __future__ import annotations

BLOCKS = " ▁▂▃▄▅▆▇█"
MAG_CHARS = {1: "*", 2: "+", 3: "·"}
GRAIN_CHAR = "."
GONE_CHAR = "▒"

Rect = tuple[int, int, int, int]  # x0, y0, x1, y1 inclusive


def _in_rect(x: int, y: int, rect: Rect | None) -> bool:
    if rect is None:
        return False
    x0, y0, x1, y1 = rect
    return x0 <= x <= x1 and y0 <= y <= y1


def _grain(x: int, y: int) -> bool:
    # Fixed speckle so the sky has texture; its absence is what shows.
    return (x * 7 + y * 11) % 23 == 0


def render_sky(
    stars: list[tuple[int, int, int]],
    width: int = 60,
    height: int = 12,
    absent: Rect | None = None,
) -> list[str]:
    """Render the sector plot. Cells inside `absent` render as nothing —
    no stars, no grain, and a gap in the plot's own border where the
    region touches it."""
    grid = [
        [GRAIN_CHAR if _grain(x, y) else " " for x in range(width)]
        for y in range(height)
    ]
    for x, y, mag in stars:
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = MAG_CHARS.get(mag, "·")
    if absent is not None:
        for y in range(height):
            for x in range(width):
                if _in_rect(x, y, absent):
                    grid[y][x] = " "

    def border_char(x: int, edge_y: int, char: str) -> str:
        # The front eats the frame too, where it touches.
        if absent is not None and _in_rect(x, edge_y, absent):
            return " "
        return char

    top = "┌" + "".join(border_char(x, 0, "─") for x in range(width)) + "┐"
    bottom = (
        "└" + "".join(border_char(x, height - 1, "─") for x in range(width)) + "┘"
    )
    lines = [top]
    for y, row in enumerate(grid):
        left = border_char(0, y, "│")
        right = border_char(width - 1, y, "│")
        lines.append(left + "".join(row) + right)
    lines.append(bottom)
    return lines


def render_strip(levels: list[int]) -> str:
    """Amplitude strip for the wire. Levels clamp to 0..8."""
    return "".join(BLOCKS[max(0, min(8, level))] for level in levels)


def render_gauge(label: str, fraction: float, width: int = 16) -> str:
    fraction = max(0.0, min(1.0, fraction))
    filled = round(fraction * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"{label:<10} [{bar}] {round(fraction * 100):>3d}%"


def render_page(lines: list[str], width: int = 56, title: str = "") -> list[str]:
    """A bordered journal page. Long lines wrap; missing words arrive
    already replaced by the caller — the page just holds them."""
    inner: list[str] = []
    for raw in lines:
        text = raw
        while len(text) > width:
            cut = text.rfind(" ", 0, width)
            if cut <= 0:
                cut = width
            inner.append(text[:cut])
            text = text[cut:].lstrip(" ")
        inner.append(text)
    head = f"╴{title}╶" if title else ""
    top = "┌" + head + "─" * max(0, width + 2 - len(head)) + "┐"
    page = [top]
    for line in inner:
        page.append("│ " + line.ljust(width) + " │")
    page.append("└" + "─" * (width + 2) + "┘")
    return page


def render_banner(lines: list[str], width: int = 60) -> list[str]:
    """A double-ruled station banner for the top of a watch."""
    top = "╔" + "═" * (width + 2) + "╗"
    bottom = "╚" + "═" * (width + 2) + "╝"
    out = [top]
    for line in lines:
        out.append("║ " + line[:width].ljust(width) + " ║")
    out.append(bottom)
    return out


def erase_words(text: str, fraction: float, seed: int) -> str:
    """Replace a deterministic fraction of words with GONE marks.
    Pure arithmetic selection — no RNG state, stable across runs."""
    if fraction <= 0:
        return text
    words = text.split(" ")
    eligible = [i for i, w in enumerate(words) if any(c.isalnum() for c in w)]
    if not eligible:
        return text
    count = max(1, round(len(eligible) * min(1.0, fraction)))
    ranked = sorted(
        range(len(eligible)),
        key=lambda k: (((k + 1) * (2 * seed + 1) * 2654435761) % 2**32, k),
    )
    chosen = {eligible[k] for k in ranked[:count]}
    out = []
    for i, word in enumerate(words):
        if i in chosen:
            out.append(GONE_CHAR * max(2, len(word) // 2 + 1))
        else:
            out.append(word)
    return " ".join(out)
