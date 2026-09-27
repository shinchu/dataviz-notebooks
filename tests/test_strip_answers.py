"""Tests for scripts/strip_answers.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from strip_answers import strip_file  # noqa: E402

FIXTURE = {
    "cells": [
        {"cell_type": "markdown", "metadata": {}, "source": ["# answer in markdown stays"]},
        {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
         "source": ["# your code goes here"]},
        {"cell_type": "code", "execution_count": 3, "metadata": {},
         "outputs": [{"name": "stdout", "output_type": "stream", "text": ["42\n"]}],
         "source": ["# answer\n", "\n", "print(42)"]},
        {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
         "source": ["x = 1  # answer later is not a marker"]},
    ],
    "metadata": {"kernelspec": {"name": "python3"}},
    "nbformat": 4,
    "nbformat_minor": 5,
}


def test_removes_only_answer_cells_and_is_idempotent(tmp_path: Path) -> None:
    """Answer cells (and their outputs) go; everything else is kept; a rerun is a no-op."""
    path = tmp_path / "nb.ipynb"
    path.write_text(json.dumps(FIXTURE, indent=1) + "\n", encoding="utf-8")

    assert strip_file(path) == 1
    nb = json.loads(path.read_text(encoding="utf-8"))
    assert [c["source"] for c in nb["cells"]] == [
        FIXTURE["cells"][0]["source"], FIXTURE["cells"][1]["source"], FIXTURE["cells"][3]["source"],
    ]
    assert "42" not in path.read_text(encoding="utf-8")
    assert nb["metadata"] == FIXTURE["metadata"] and nb["nbformat"] == 4

    before = path.read_text(encoding="utf-8")
    assert strip_file(path) == 0
    assert path.read_text(encoding="utf-8") == before
