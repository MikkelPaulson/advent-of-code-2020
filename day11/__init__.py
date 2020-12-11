"""https://adventofcode.com/2020/day/11"""

import io


def part1(stdin, stderr):
    """
    Simulate your seating area by applying the seating rules repeatedly until
    no seats change state. How many seats end up occupied?
    """

    seats = parse(stdin)
    new_seats = apply_round(seats)
    while seats != new_seats:
        seats = new_seats
        new_seats = apply_round(seats)
        stderr.write(f"{new_seats}\n")

    return str(len([seat for _, seat in seats.items() if seat == '#']))


def apply_round(layout: dict) -> dict:
    """
    - If a seat is empty (L) and there are no occupied seats adjacent to it,
      the seat becomes occupied.
    - If a seat is occupied (#) and four or more seats adjacent to it are also
      occupied, the seat becomes empty.
    - Otherwise, the seat's state does not change.
    """

    return {
        (row, col): get_adjacency(layout, row, col)
        for (row, col), _ in layout.items()
    }


def get_adjacency(layout: dict, row: int, col: int) -> str:
    """
    Get the number of occupied seats adjacent to the current seat.
    """

    seat = layout[(row, col)]
    if seat == '.':
        return '.'

    adjacent_seats = [
        (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
        (row, col - 1), (row, col + 1),
        (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),
    ]
    adjacent_count = 0

    for (adjacent_row, adjacent_col) in adjacent_seats:
        if layout.get((adjacent_row, adjacent_col)) == '#':
            adjacent_count += 1

    if adjacent_count == 0 and seat == 'L':
        return '#'
    if adjacent_count >= 4 and seat == '#':
        return 'L'

    return seat


def parse(stdin: io.TextIOWrapper) -> dict:
    """
    Parse the input into an array of arrays of characters.
    """

    return {
        (row, col): seat
        for row, line in enumerate(stdin.read().strip().splitlines())
        for col, seat in enumerate(line)
    }
