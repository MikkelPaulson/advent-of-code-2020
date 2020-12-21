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
    stderr.write(f"tiles: {tiles}\n")

    tile_edges = calc_edges(tiles)
    stderr.write(f"tile_edges: {tile_edges}\n")

    edges = match_edges(tile_edges)
    stderr.write(f"edges: {edges}\n")

    product = 1
    for corner in find_corners(edges):
        product *= corner

    return str(product)


def find_corners(edges: dict) -> list:
    """Find the IDs of the four corner tiles based on a dict of edge pairs."""
    return [k for k, v in collections.Counter(
        [edge[0] for edge in edges.values() if len(edge) == 1]
    ).most_common(4)]


def match_edges(tile_edges: dict) -> dict:
    """Find matching edges within a set of tiles."""

    edges = collections.defaultdict(list)

    for tile_id, tile in tile_edges.items():
        for edge in tile:
            edges[edge].append(tile_id)
            edges["".join(reversed(edge))].append(tile_id)

    return dict(edges.items())


def calc_edges(tiles: dict) -> dict:
    """Compute the edges of each tile, returned in a N W S E order."""

    return {
        tile_id: [
            tile[0],
            "".join([line[-1] for line in tile]),
            "".join(reversed(tile[-1])),
            "".join([line[0] for line in reversed(tile)]),
        ] for tile_id, tile in tiles.items()
    }


def parse(stdin: io.TextIOWrapper) -> dict:
    """
    Parse the input into a dict of lists. The keys are the integer IDs and the
    values are lists of strings, each representing a line of the tile.
    """

    tiles = [
        block.splitlines() for block in stdin.read().strip().split("\n\n")
    ]

    pattern = re.compile("Tile ([0-9]+):")

    return {
        int(pattern.match(tile[0]).group(1)): tile[1:]
        for tile in tiles
    }
