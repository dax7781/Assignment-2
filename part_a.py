#!/usr/bin/env python3
"""PRG550 Assignment 02 – Part A (Unicode Maze ASCII Generator)."""

import sys
import importlib.util
import os

MIN_ROWS = 10
MAX_ROWS = 36
MIN_COLUMNS = 20
MAX_COLUMNS = 36


def index_label(n):
    """Return 0-9 then A-Z label."""
    if n < 10:
        return str(n)
    return chr(ord('A') + n - 10)


def top_labels(width):
    return "".join(index_label(i % 36) for i in range(width))


def load_generator(path):
    """Import a2.py dynamically."""
    spec = importlib.util.spec_from_file_location("a2", path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    raise SystemExit("Error: could not import a2.py")


def validate_dims(rows, cols):
    if not (MIN_ROWS <= rows <= MAX_ROWS) or not (MIN_COLUMNS <= cols <= MAX_COLUMNS):
        print("Error: maze dimensions incorrect...")
        print("Usage: python3 part_a.py rows columns")
        print(f"       minimum rows >= {MIN_ROWS} maximum rows <= {MAX_ROWS}")
        print(f"       minimum columns >= {MIN_COLUMNS} maximum columns <= {MAX_COLUMNS}")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 part_a.py <rows> <cols>")
        sys.exit(1)

    try:
        rows = int(sys.argv[1])
        cols = int(sys.argv[2])
    except ValueError:
        print("Rows and columns must be integers.")
        sys.exit(1)

    validate_dims(rows, cols)

    a2_path = os.path.join(os.path.dirname(__file__), "a2.py")
    maze_module = load_generator(a2_path)

    if not hasattr(maze_module, "create_maze"):
        raise SystemExit("Error: a2.py does not define create_maze(rows, cols)")

    maze_lines = maze_module.create_maze(rows, cols)
    if isinstance(maze_lines, str):
        maze_lines = maze_lines.splitlines()

    header = "   " + top_labels(len(maze_lines[0]))
    print(header)

    for i, line in enumerate(maze_lines):
        print(index_label(i % 36).rjust(2) + " " + line)


if __name__ == "__main__":
    main()
