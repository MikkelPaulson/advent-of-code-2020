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

    grid = compute_grid(tiles)
    stderr.write(f"grid: {grid}\n")

    return str(grid[0][0] * grid[0][-1] * grid[-1][0] * grid[-1][-1])


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    How many # are not part of a sea monster?
    """

    tiles = parse(stdin)
    stderr.write(f"tiles: {tiles}\n")

    grid = compute_grid(tiles)
    stderr.write(f"grid: {grid}\n")

    stderr.write(
        f"corners: {grid[0][0]}, {grid[0][-1]}, "
        f"{grid[-1][0]}, {grid[-1][-1]}\n"
    )


def compute_grid(tiles: dict) -> list:
    """Compute the grid arrangement based on a set of tiles."""

    def match_edges(tiles: dict) -> dict:
        sides = collections.defaultdict(list)

        for tile_id, tile in calc_sides(tiles).items():
            for side in tile:
                sides[side].append(tile_id)
                sides["".join(reversed(side))].append(tile_id)

        edges = collections.defaultdict(set)

        for side in sides.values():
            if len(side) == 2:
                edges[side[0]].add(side[1])
                edges[side[1]].add(side[0])

        return dict(edges.items())

    def arrange_vertices(edges: dict) -> list:
        def find_corner(edges: dict) -> int:
            for vertex_id, vertex_edges in edges.items():
                if len(vertex_edges) == 2:
                    return vertex_id

            raise Exception("No corner vertex found.")

        def get_common_vertices(edges: tuple) -> set:
            result = set()
            counter = collections.Counter([
                vertex
                for vertices in edges
                for vertex in vertices
            ])
            for vertex, count in counter.most_common():
                if count == 1:
                    return result

                result.add(vertex)

            return result

        grid = [[find_corner(edges)]]
        line_length = None
        used_vertices = {grid[0][0]}
        col, row = 0, 0
        while len(used_vertices) < len(edges):
            col += 1
            if col == line_length:
                col = 0
                row += 1
                grid.append(list())

            try:
                common_vertices = get_common_vertices((
                    edges[grid[row - 1][col]],
                    edges[grid[row][col - 1]],
                ))

                for vertex in common_vertices:
                    if vertex not in used_vertices:
                        used_vertices.add(vertex)
                        grid[row].append(vertex)
                        break
                else:
                    raise Exception("No common vertex found.")

            except IndexError:
                if col == 0:
                    common_vertices = edges[grid[row - 1][col]]
                else:
                    common_vertices = edges[grid[row][col - 1]]

                for vertex in common_vertices:
                    if vertex not in used_vertices and len(edges[vertex]) < 4:
                        if line_length is None and len(edges[vertex]) == 2:
                            line_length = col + 1

                        used_vertices.add(vertex)
                        grid[row].append(vertex)
                        break
                else:
                    raise Exception("No edge vertex found.")

        return grid

    return arrange_vertices(match_edges(tiles))


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
