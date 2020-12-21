"""https://adventofcode.com/2020/day/17"""

import io
import itertools


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Starting with your given initial configuration, simulate six cycles. How
    many cubes are left in the active state after the sixth cycle?
    """

    cubes = cycles(parse(stdin), 6, 3, stderr)
    return len(cubes)


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Starting with your given initial configuration, simulate six cycles in a
    4-dimensional space. How many cubes are left in the active state after the
    sixth cycle?
    """

    cubes = cycles(parse(stdin), 6, 4, stderr)
    return len(cubes)


def cycles(cubes: set, cycle_count: int, dimensions: int,
           stderr: io.TextIOWrapper) -> set:
    """
    Apply a given number of cycles to the data set.
    """

    def map_dimensions(cubes: set, dimensions: int) -> (set, tuple, tuple):
        """
        Parse the flat x,y plane into a set of x,y,z,... tuples representing
        the active cubes for an arbitrary number of dimensions.
        """

        result = set()

        coord_min = (0,) * dimensions
        coord_max = (0,) * dimensions
        padding = (0,) * (dimensions - 2)

        for coord in cubes:
            new_coord = coord + padding
            result.add(new_coord)
            coord_min = tuple(map(min, zip(new_coord, coord_min)))
            coord_max = tuple(map(max, zip(new_coord, coord_max)))

        return result, coord_min, coord_max

    cubes, coord_min, coord_max = map_dimensions(cubes, dimensions)

    for i in range(cycle_count):
        stderr.write(f"Cycle {i}:\n")
        stderr.write(f"cubes: {cubes}\n")
        stderr.write(f"min: {coord_min}\n")
        stderr.write(f"max: {coord_max}\n")
        cubes, coord_min, coord_max = cycle(cubes, coord_min, coord_max)

    stderr.write("Cycle 6:\n")
    stderr.write(f"cubes: {cubes}\n")
    stderr.write(f"min: {coord_min}\n")
    stderr.write(f"max: {coord_max}\n")

    return cubes


def cycle(cubes: set, coord_min: tuple, coord_max: tuple) -> \
        (set, tuple, tuple):
    """
    Run one cycle on a full data set, returning the new data set as well as the
    new min and max coordinates for future iterations.
    """

    def xyz_range(coord_min, coord_max=None):
        if coord_max is None:
            coord_max = coord_min

        ranges = list(
            range(coord_min[i] - 1, coord_max[i] + 2)
            for i, _ in enumerate(coord_min)
        )

        return itertools.product(*ranges)

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


def parse(stdin: io.TextIOWrapper) -> set:
    """
    Parse the input into a set of x,y,z,... tuples representing the active
    cubes for an arbitrary number of dimensions.
    """

    return set(
        (x, y)
        for y, line in enumerate(stdin.read().strip().splitlines())
        for x, char in enumerate(line)
        if char == '#'
    )
