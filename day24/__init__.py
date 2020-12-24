"""https://adventofcode.com/2020/day/24"""

import functools
import io


def part1(stdin: io.TextIOWrapper, _stderr: io.TextIOWrapper) -> int:
    """
    Go through the renovation crew's list and determine which tiles they need
    to flip. After all of the instructions have been followed, how many tiles
    are left with the black side up?
    """
    return len(parse_and_evaluate(stdin))


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    How many tiles will be black after 100 days?
    """

    def get_min_coord(a_coord: tuple, b_coord: tuple) -> tuple:
        return tuple(map(min, zip(a_coord, b_coord)))

    def get_max_coord(a_coord: tuple, b_coord: tuple) -> tuple:
        return tuple(map(max, zip(a_coord, b_coord)))

    def tile_generation(tiles: set, min_coord: tuple, max_coord: tuple) -> \
            (set, tuple, tuple):
        next_generation = set()
        for x_pos in range(min_coord[0] - 1, max_coord[0] + 2):
            for y_pos in range(min_coord[1] - 1, max_coord[1] + 2):
                adjacent = count_adjacent(tiles, (x_pos, y_pos))

                if adjacent == 2 or (adjacent == 1 and
                                     (x_pos, y_pos) in tiles):
                    next_generation.add((x_pos, y_pos))
                    min_coord = get_min_coord(min_coord, (x_pos, y_pos))
                    max_coord = get_max_coord(max_coord, (x_pos, y_pos))

        return next_generation, min_coord, max_coord

    def count_adjacent(tiles: set, coord: tuple) -> int:
        count = 0
        for direction in TILE_DIRECTIONS:
            if locate_tile([direction], coord) in tiles:
                count += 1
        return count

    tiles = parse_and_evaluate(stdin)

    min_coord = functools.reduce(get_min_coord, tiles, (0, 0))
    max_coord = functools.reduce(get_max_coord, tiles, (0, 0))

    for generation in range(0, 100):
        stderr.write(f"Day {generation}: {len(tiles)}\n")
        tiles, min_coord, max_coord = \
            tile_generation(tiles, min_coord, max_coord)

    return len(tiles)


#   NW  NE
# W   @   E
# SW  SE
#
# SE, NE, W should bring us back to the starting point, so:
TILE_DIRECTIONS = {
    "e": (1, 0),
    "se": (0, -1),
    "sw": (-1, -1),
    "w": (-1, 0),
    "nw": (0, 1),
    "ne": (1, 1),
}


def locate_tile(directions: list, start: tuple = (0, 0)) -> tuple:
    """
    Given a set of directions, determine the coordinates of a tile.
    """
    mapped_directions = [
        TILE_DIRECTIONS[direction]
        for direction in directions
    ]
    return functools.reduce(
        lambda a, b: tuple(map(sum, zip(a, b))),
        mapped_directions,
        start
    )


def parse_and_evaluate(stdin: io.TextIOWrapper) -> set:
    """
    Parse the input stream and reduce it to a set of coordinates representing
    the black tiles.
    """

    def parse(stdin: io.TextIOWrapper) -> list:
        """
        Parse the input into a list of lists of strings, each string being a
        direction: "e", "se", "sw", "w", "nw", and "ne". Each list refers to a
        single tile to flip.
        """

        def parse_line(line: str) -> list:
            result = list()
            i = 0
            while i < len(line):
                if line[i] in ["n", "s"]:
                    result.append(line[i:i + 2])
                    i += 2
                else:
                    result.append(line[i])
                    i += 1

            return result

        return [parse_line(line) for line in stdin.read().strip().splitlines()]

    flips = [locate_tile(directions) for directions in parse(stdin)]

    tiles = set()
    for flip in flips:
        if flip in tiles:
            tiles.remove(flip)
        else:
            tiles.add(flip)

    return tiles
