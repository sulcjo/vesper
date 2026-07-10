"""The IO seam between engine/content and the real terminal.

Content modules narrate through this protocol and never import term
directly, so tests can run every scene against a scripted IO and the
shell can decide how each kind of line looks and sounds.

Kinds:
    os     — station OS output. uppercase, quick, green.
    prose  — the observer's interiority. typewriter pace.
    dim    — marginal, faded things.
    alert  — warnings. amber.
    art    — preformatted lines (plots, pages, strips): never wrapped,
             never paced, printed exactly as given.
"""

from __future__ import annotations

from typing import Protocol


class IO(Protocol):
    def say(self, text: str, kind: str = "prose") -> None: ...

    def ask(self, prompt: str) -> str: ...

    def art(self, lines: list[str]) -> None: ...

    def pause(self, seconds: float = 0.35) -> None: ...


class ScriptedIO:
    """Test double: feeds canned answers, records everything said."""

    def __init__(self, answers: list[str] | None = None) -> None:
        self.answers = list(answers or [])
        self.said: list[tuple[str, str]] = []
        self.prompts: list[str] = []

    def say(self, text: str, kind: str = "prose") -> None:
        self.said.append((kind, text))

    def ask(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if self.answers:
            return self.answers.pop(0)
        return ""

    def art(self, lines: list[str]) -> None:
        for line in lines:
            self.said.append(("art", line))

    def pause(self, seconds: float = 0.35) -> None:  # noqa: ARG002
        return

    def transcript(self) -> str:
        return "\n".join(text for _, text in self.said)
