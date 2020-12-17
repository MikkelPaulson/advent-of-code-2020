"""https://adventofcode.com/2020/day/15"""

import io
import itertools


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    Starting with your given initial configuration, simulate six cycles. How
    many cubes are left in the active state after the sixth cycle?
    """

    cubes, coord_min, coord_max = parse(stdin)

    for i in range(6):
        stderr.write(f"Cycle {i}:\n")
        stderr.write(f"cubes: {cubes}\n")
        stderr.write(f"min: {coord_min}\n")
        stderr.write(f"max: {coord_max}\n")
        cubes, coord_min, coord_max = cycle(cubes, coord_min, coord_max)

    stderr.write("Cycle 6:\n")
    stderr.write(f"cubes: {cubes}\n")
    stderr.write(f"min: {coord_min}\n")
    stderr.write(f"max: {coord_max}\n")
    return str(len(cubes))


def cycle(cubes, coord_min, coord_max) -> (set, tuple, tuple):
    """
    Run one cycle on a full data set, returning the new data set as well as the
    new min and max coordinates for future iterations.
    """

    def xyz_range(coord_min, coord_max=None):
        if coord_max is None:
            coord_max = coord_min

        return itertools.product(
            range(coord_min[0] - 1, coord_max[0] + 2),
            range(coord_min[1] - 1, coord_max[1] + 2),
            range(coord_min[2] - 1, coord_max[2] + 2),
        )

    def calc_state(cubes, coord) -> bool:
        neighbors = 0

        for neighbor in xyz_range(coord):
            if neighbor != coord and neighbor in cubes:
                neighbors += 1
                if neighbors > 3:
                    return False

        return neighbors == 3 or (coord in cubes and neighbors == 2)

    new_cubes = set()
    for coord in xyz_range(coord_min, coord_max):
        if calc_state(cubes, coord):
            new_cubes.add(coord)
            coord_min = tuple(map(min, zip(coord, coord_min)))
            coord_max = tuple(map(max, zip(coord, coord_max)))

    return new_cubes, coord_min, coord_max


def parse(stdin: io.TextIOWrapper) -> (set, tuple, tuple):
    """
    Parse the input into a set of x,y,z tuples representing the active cubes.
    """

    result = set()

    coord_min = (0, 0, 0)
    coord_max = (0, 0, 0)

    for y_pos, line in enumerate(stdin.read().strip().splitlines()):
        for x_pos, char in enumerate(line):
            if char == '#':
                coord = (x_pos, y_pos, 0)
                result.add(coord)
                coord_max = tuple(map(max, zip(coord, coord_max)))

    return result, coord_min, coord_max
