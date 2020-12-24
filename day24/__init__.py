"""https://adventofcode.com/2020/day/24"""

import functools
import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Go through the renovation crew's list and determine which tiles they need
    to flip. After all of the instructions have been followed, how many tiles
    are left with the black side up?
    """

    flips = [locate_tile(directions) for directions in parse(stdin)]
    stderr.write(f"{flips}\n")

    tiles = set()
    for flip in flips:
        if flip in tiles:
            tiles.remove(flip)
        else:
            tiles.add(flip)

    stderr.write(f"{tiles}\n")

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


def locate_tile(directions: list) -> tuple:
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
        (0, 0)
    )


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
