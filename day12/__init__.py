"""https://adventofcode.com/2020/day/12"""

import io


def part1(stdin, stderr):
    """
    Figure out where the navigation instructions lead. What is the Manhattan
    distance between that location and the ship's starting position?
    """

    directions = parse(stdin)
    x_pos = 0
    y_pos = 0
    heading = 90
    for (action, distance) in directions:
        stderr.write(f"{action}{distance} ")

        if action == 'F':
            action = {0: 'N', 90: 'E', 180: 'S', 270: 'W'}[heading]

        if action == 'N':
            y_pos += distance
        elif action == 'S':
            y_pos -= distance
        elif action == 'E':
            x_pos += distance
        elif action == 'W':
            x_pos -= distance
        elif action == 'L':
            heading = (heading - distance + 360) % 360
        elif action == 'R':
            heading = (heading + distance) % 360

        stderr.write(f"{x_pos},{y_pos}@{heading}\n")

    return str(abs(x_pos) + abs(y_pos))


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of tuples: string direction and int distance.
    """

    return [
        (line[0], int(line[1:]))
        for line in stdin.read().strip().splitlines()
    ]
