"""
    PRG550 Assignment Base Code

    Written by: 	Danny Abesdris
    Modified by: 	Michal Heidenreich
    Last update: 	February 18, 2025
"""

import random
import sys

MIN_ROWS = 10
MAX_ROWS = 36
MIN_COLUMNS = 20
MAX_COLUMNS = 36


def create_maze(rows, columns):
    rows, columns = validate_dimensions(rows, columns)
    blank, slab, wall, corner = ' ', '-', '|', '+'

    row_state, pin_location = initialize_maze(rows, columns)
    maze = generate_maze(rows, columns, row_state, pin_location, blank, slab, wall, corner)
    bottom_row = generate_bottom_row(maze, wall, blank, slab)

    return maze + bottom_row


def validate_dimensions(rows, columns):
    try:
        rows, columns = int(rows) - 1, int(columns) - 1
    except ValueError:
        error_message()

    if not (MIN_ROWS - 1 <= rows <= MAX_ROWS - 1 and MIN_COLUMNS - 1 <= columns <= MAX_COLUMNS - 1):
        error_message()

    return rows, columns


def initialize_maze(rows, columns):
    row_state = ['-'] * (columns // 2)
    pin_location = random.randint(1, (columns // 2) * (rows // 2 - 1))

    return row_state, pin_location


def generate_maze(rows, columns, row_state, pin_location, blank, slab, wall, corner):
    maze = f"{corner}{slab * (columns - 1)}{corner}\n"
    maze += f"@{blank * (columns - 1)}{wall}\n"

    for row in range(1, rows // 2):
        top_row, bottom_row, up_next = '', '', wall

        for column in range(columns // 2):
            if random.randint(0, 1) or column == 0:
                top_row += up_next + blank
                bottom_row += wall
                up_next, row_state[column] = wall, corner
            else:
                top_row += row_state[column] + slab
                bottom_row += blank
                up_next, row_state[column] = corner, slab
            bottom_row += '#' if (pin_location := pin_location - 1) == 0 else blank

        if columns % 2:
            top_row += top_row[-1]
            bottom_row += blank

        maze += f"{top_row}{up_next}\n{bottom_row}{wall}\n"

    if rows % 2:
        maze += f"{bottom_row.replace('#', ' ')}{wall}\n"

    return maze


def generate_bottom_row(maze, wall, blank, slab):
    last_row = maze.strip().split("\n")[-1]
    return last_row.translate(str.maketrans({wall: '+', blank: slab, '#': slab})) + "\n"


def error_message():
    print(
        f"Error: maze dimensions incorrect...\n"
        "Usage: python maze.py rows columns\n"
        f"       minimum rows >= {MIN_ROWS} maximum rows <= {MAX_ROWS}\n"
        f"       minimum columns >= {MIN_COLUMNS} maximum columns <= {MAX_COLUMNS}\n"
    )

    sys.exit(1)
