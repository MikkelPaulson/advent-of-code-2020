"""https://adventofcode.com/2020/day/11"""

import io


def part1(stdin, stderr):
    """
    Simulate your seating area by applying the seating rules repeatedly until
    no seats change state. How many seats end up occupied?
    """

    def get_adjacency(layout: dict, row: int, col: int) -> str:
        """
        Calculate the final state of a seat given the current layout according
        to adjacency rules.
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

    def apply_round(layout: dict) -> dict:
        """
        - If a seat is empty (L) and there are no occupied seats adjacent to
          it, the seat becomes occupied.
        - If a seat is occupied (#) and four or more seats adjacent to it are
          also occupied, the seat becomes empty.
        - Otherwise, the seat's state does not change.
        """

        return {
            (row, col): get_adjacency(layout, row, col)
            for (row, col), _ in layout.items()
        }

    seats = parse(stdin)
    new_seats = apply_round(seats)
    while seats != new_seats:
        seats = new_seats
        new_seats = apply_round(seats)
        stderr.write(f"{new_seats}\n")

    return str(len([seat for _, seat in seats.items() if seat == '#']))


def part2(stdin, stderr):
    """
    Given the new visibility method and the rule change for occupied seats
    becoming empty, once equilibrium is reached, how many seats end up
    occupied?
    """

    def get_los(layout: dict, row: int, col: int) -> dict:
        """
        Calculate the final state of a seat given the current layout according
        to line of sight rules.
        """

        seat = layout[(row, col)]
        if seat == '.':
            return '.'

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        los_count = 0

        for (dir_row, dir_col) in directions:
            test_row = row + dir_row
            test_col = col + dir_col
            while (test_row, test_col) in layout:
                if layout[(test_row, test_col)] == '#':
                    los_count += 1
                    break

                if layout[(test_row, test_col)] == 'L':
                    break

                test_row = test_row + dir_row
                test_col = test_col + dir_col

            if seat == '#' and los_count >= 5:
                return 'L'
            if seat == 'L' and los_count > 0:
                return 'L'

        if seat == 'L' and los_count == 0:
            return '#'

        return seat

    def apply_round(layout: dict) -> dict:
        """
        Now, instead of considering just the eight immediately adjacent seats,
        consider the first seat in each of those eight directions. For example,
        the empty seat below would see eight occupied seats:

        Also, people seem to be more tolerant than you expected: it now takes
        five or more visible occupied seats for an occupied seat to become
        empty (rather than four or more from the previous rules). The other
        rules still apply: empty seats that see no occupied seats become
        occupied, seats matching no rule don't change, and floor never changes.
        """

        return {
            (row, col): get_los(layout, row, col)
            for (row, col), _ in layout.items()
        }

    seats = parse(stdin)
    new_seats = apply_round(seats)
    while seats != new_seats:
        seats = new_seats
        new_seats = apply_round(seats)
        stderr.write(f"{new_seats}\n")

    return str(len([seat for _, seat in seats.items() if seat == '#']))


def parse(stdin: io.TextIOWrapper) -> dict:
    """
    Parse the input into an array of arrays of characters.
    """

    return {
        (row, col): seat
        for row, line in enumerate(stdin.read().strip().splitlines())
        for col, seat in enumerate(line)
    }
