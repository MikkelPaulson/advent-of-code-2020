"""https://adventofcode.com/2020/day/20"""

import collections
import functools
import io
import re


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    Assemble the tiles into an image. What do you get if you multiply together
    the IDs of the four corner tiles?
    """

    tiles = parse(stdin)
    stderr.write(f"tiles: {tiles}\n")

    tile_sides = calc_sides(tiles)
    stderr.write(f"tile_sides: {tile_sides}\n")

    vertices = get_vertices(tile_sides)
    stderr.write(f"vertices: {vertices}\n")

    corners = [vertex for vertex, edges in vertices.items() if len(edges) == 2]
    stderr.write(f"corners: {corners}\n")

    return str(functools.reduce(lambda a, b: a * b, corners))


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    How many # are not part of a sea monster?
    """

    tiles = parse(stdin)
    stderr.write(f"tiles: {tiles}\n")

    tile_sides = calc_sides(tiles)
    stderr.write(f"tile_sides: {tile_sides}\n")

    vertices = get_vertices(tile_sides)
    stderr.write(f"vertices: {vertices}\n")

    used_vertices = set()
    grid = [[fill_tile(vertices, list(), used_vertices, 0, 0)]]
    used_vertices.add(grid[0][0])
    side_length = 1
    while True:
        vertex = fill_tile(vertices, grid, used_vertices, side_length, 0)
        used_vertices.add(vertex)
        stderr.write(f"row 0, col {side_length}: {vertex}\n")
        side_length += 1
        grid[0].append(vertex)
        if len(vertices[vertex]) == 2:
            break

    for row in range(1, side_length):
        grid.append(list())
        for col in range(side_length):
            vertex = fill_tile(vertices, grid, used_vertices, col, row)
            used_vertices.add(vertex)
            grid[row].append(vertex)
            stderr.write(f"row {row}, col {col}: {vertex}\n")

    stderr.write(f"grid: {grid}\n")


def fill_tile(vertices: dict, grid: list, used_vertices: set, col: int, row: int) -> int:

    # top row
    if row == 0:

        # top left corner
        if col == 0:
            for vertex, edges in vertices.items():
                if len(edges) == 2:
                    return vertex

            raise Exception("No top left corner vertex found.")

        for vertex in vertices[grid[row][col - 1]]:
            if len(vertices[vertex]) < 4 and vertex not in used_vertices:
                return vertex

        raise Exception("No top vertex found.")

    side_length = len(grid[0])

    # bottom row
    if row == side_length - 1:

        # bottom left corner
        if col == 0:
            for vertex in vertices[grid[row - 1][col]]:
                if len(vertices[vertex]) == 2:
                    return vertex

            raise Exception("No bottom left corner vertex found.")

        for vertex in vertices[grid[row][col - 1]]:
            if len(vertices[vertex]) < 4 and vertex not in used_vertices:
                return vertex

        raise Exception("No bottom vertex found.")

    # left/right side
    if col in (0, side_length - 1):
        for vertex in vertices[grid[row - 1][col]]:
            if len(vertices[vertex]) < 4 and vertex not in used_vertices:
                return vertex

        raise Exception("No left/right vertex found.")

    # non-side tile: The tile above ours and the tile to the left of ours will
    # always have two tiles in common, ours and the one diagonally up and to
    # the left of ours. We can look up its ID, so adding it to the mix means
    # that its ID will appear three times among the vertices and ours twice.
    # Taking the second most common result in the bunch gives us the target
    # tile.
    _, (vertex, _) = collections.Counter(
        list(vertices[grid[row - 1][col]]) +
        list(vertices[grid[row][col - 1]]) +
        [grid[row - 1][col - 1]]
    ).most_common(2)

    return vertex


def get_vertices(tile_sides: dict) -> dict:
    """Find matching edges within a set of tiles."""

    edges = collections.defaultdict(list)

    for tile_id, tile in tile_sides.items():
        for edge in tile:
            edges[edge].append(tile_id)
            edges["".join(reversed(edge))].append(tile_id)

    vertices = collections.defaultdict(set)

    for edge in edges.values():
        if len(edge) == 2:
            vertices[edge[0]].add(edge[1])
            vertices[edge[1]].add(edge[0])

    return dict(vertices.items())


def calc_sides(tiles: dict) -> dict:
    """Compute the sides of each tile, returned in a N W S E order."""

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
