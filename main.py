"""news-image-20261119 entrypoint (Python 3.13, standard library only).

Copies the repository's entry.png to /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png outside the grader container).
Deterministic: the same bytes on every run; no network access.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT.mkdir(parents=True, exist_ok=True)

shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
