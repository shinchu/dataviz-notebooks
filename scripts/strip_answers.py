"""Remove answer cells from Jupyter notebooks.

An answer cell is a code cell whose source starts with the ``# answer``
marker. Matching the 2025 workflow (commit be68ad1), each answer cell is
removed entirely, so neither its code nor its stored outputs survive.
All other cells and metadata are left untouched, and running the script
twice produces the same result.

Usage:
    python scripts/strip_answers.py week_1/intro-colab-python.ipynb [...]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ANSWER_MARKER = "# answer"
JSON_INDENT = 1  # Jupyter's on-disk indentation


def is_answer_cell(cell: dict[str, Any]) -> bool:
    """Return True if the cell is a code cell marked as an answer."""
    if cell.get("cell_type") != "code":
        return False
    source = cell.get("source", "")
    text = "".join(source) if isinstance(source, list) else source
    first_line = text.lstrip().split("\n", 1)[0].strip()
    return first_line.lower() == ANSWER_MARKER


def strip_notebook(nb: dict[str, Any]) -> int:
    """Remove answer cells from a notebook in place and return how many were removed."""
    cells = nb.get("cells", [])
    kept = [cell for cell in cells if not is_answer_cell(cell)]
    removed = len(cells) - len(kept)
    nb["cells"] = kept
    return removed


def strip_file(path: Path) -> int:
    """Strip answer cells from a notebook file, rewriting it only if something changed."""
    nb = json.loads(path.read_text(encoding="utf-8"))
    removed = strip_notebook(nb)
    if removed:
        path.write_text(
            json.dumps(nb, indent=JSON_INDENT, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return removed


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("notebooks", nargs="+", type=Path)
    args = parser.parse_args(argv)
    for path in args.notebooks:
        print(f"{path}: removed {strip_file(path)} answer cell(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
