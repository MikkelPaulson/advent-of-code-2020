"""https://adventofcode.com/2020/day/12"""

import io
import math


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
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

    return abs(x_pos) + abs(y_pos)


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Figure out where the navigation instructions actually lead. What is the
    Manhattan distance between that location and the ship's starting position?
    """

    directions = parse(stdin)
    x_pos = 0
    y_pos = 0
    x_waypoint = 10
    y_waypoint = 1

    for (action, distance) in directions:
        stderr.write(f"{action}{distance} ")

        if action == 'N':
            y_waypoint += distance
        elif action == 'S':
            y_waypoint -= distance
        elif action == 'E':
            x_waypoint += distance
        elif action == 'W':
            x_waypoint -= distance
        elif action == 'R':
            action = 'L'
            distance *= -1

        if action == 'L':
            (x_waypoint, y_waypoint) = (
                round(x_waypoint * math.cos(distance * math.pi/180)
                      - y_waypoint * math.sin(distance * math.pi/180)),

                round(x_waypoint * math.sin(distance * math.pi/180)
                      + y_waypoint * math.cos(distance * math.pi/180)),
            )

        if action == 'F':
            x_pos += x_waypoint * distance
            y_pos += y_waypoint * distance

        stderr.write(f"{x_pos},{y_pos} waypoint {x_waypoint},{y_waypoint}\n")

    return abs(x_pos) + abs(y_pos)


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of tuples: string direction and int distance.
    """

    return [
        (line[0], int(line[1:]))
        for line in stdin.read().strip().splitlines()
    ]
