"""https://adventofcode.com/2020/day/20"""

import collections
import io
import re


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    Assemble the tiles into an image. What do you get if you multiply together
    the IDs of the four corner tiles?
    """

    tiles = parse(stdin)

    edges = collections.defaultdict(list)

    for tile_id, tile in tiles.items():
        for edge in tile:
            stderr.write(f"{tile_id}: {edge}\n")
            edges[edge].append(tile_id)
            edges["".join(reversed(edge))].append(tile_id)

    stderr.write(f"{tiles}\n")
    stderr.write(f"{edges}\n")

    singles = collections.Counter(
        [edge[0] for edge in edges.values() if len(edge) == 1]
    )

    stderr.write(f"{singles}\n")

    product = 1
    for corner, _ in singles.most_common(4):
        product *= corner

    return str(product)


def parse(stdin: io.TextIOWrapper) -> dict:
    """
    Parse the input into a dict of lists. The keys are the integer IDs and the
    values are 4-element lists containing the edges rendered as binary.
    """

    raw_tiles = [
        block.splitlines() for block in stdin.read().strip().split("\n\n")
    ]

    pattern = re.compile("Tile ([0-9]+):")

    return {
        int(pattern.match(raw_tile[0]).group(1)): [
            raw_tile[1],
            "".join([line[-1] for line in raw_tile[1:]]),
            "".join(reversed(raw_tile[-1])),
            "".join([line[0] for line in reversed(raw_tile[1:])]),
        ] for raw_tile in raw_tiles
    }
