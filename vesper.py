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


def main() -> int:
    return run(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
