#!/usr/bin/env python3
"""Build a single-file distributable: dist/vesper.pyz

Bundles vesper.py, engine/ and content/ into a compressed zipapp that
runs anywhere Python 3.10+ does:

    python3 tools/build_pyz.py
    python3 dist/vesper.pyz
"""

from __future__ import annotations

import shutil
import tempfile
import zipapp
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ("vesper.py", "engine", "content")


def build() -> Path:
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    target = dist / "vesper.pyz"
    with tempfile.TemporaryDirectory() as staging_dir:
        staging = Path(staging_dir)
        for name in INCLUDE:
            source = ROOT / name
            if source.is_dir():
                shutil.copytree(
                    source, staging / name,
                    ignore=shutil.ignore_patterns("__pycache__"),
                )
            else:
                shutil.copy2(source, staging / name)
        zipapp.create_archive(
            staging, target, main="vesper:main",
            interpreter="/usr/bin/env python3", compressed=True,
        )
    return target


if __name__ == "__main__":
    print(build())
