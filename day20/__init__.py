"""https://adventofcode.com/2020/day/20"""

import collections
import io
import re


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Assemble the tiles into an image. What do you get if you multiply together
    the IDs of the four corner tiles?
    """

    tiles = parse(stdin)
    stderr.write(f"tiles: {tiles}\n")

    grid = compute_grid(tiles)
    stderr.write(f"grid: {grid}\n")

    return grid[0][0] * grid[0][-1] * grid[-1][0] * grid[-1][-1]


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    How many # are not part of a sea monster?
    """

    tiles = parse(stdin)
    stderr.write(f"tiles: {tiles}\n")

    grid = compute_grid(tiles)
    stderr.write(f"grid: {grid}\n")

    image = assemble_image(tiles, grid)
    paint_sea_monsters(image)

    stderr.write("\n".join(image) + "\n")

    return len([
        char
        for line in image
        for char in line if char == '#'
    ])


def assemble_image(tiles: dict, grid: list) -> list:
    """Assemble the set of tiles into a finished image."""

    def rotate_tile(tile: list) -> list:
        return [
            "".join([
                tile[col][len(tile) - row - 1]
                for col, _ in enumerate(tile)
            ])
            for row, _ in enumerate(tile[0])
        ]

    def align_tiles(tiles: dict, grid: list) -> list:
        def align_first_tile(tiles: tuple, grid: list) -> list:
            """Initialize the first tile."""
            tile = tiles[grid[0][0]].copy()
            tile_sides = calc_sides(tile)

            tile_sides_set = set(tile_sides)
            adjacent_sides = list()
            for adjacent_tile in [tiles[grid[0][1]], tiles[grid[1][0]]]:

                adjacent_tile_sides = set(calc_sides(adjacent_tile))

                if tile_sides_set.isdisjoint(adjacent_tile_sides):
                    adjacent_tile.reverse()
                    adjacent_sides.append((
                        set(calc_sides(adjacent_tile))
                        & tile_sides_set
                    ).pop())
                else:
                    adjacent_sides.append((
                        adjacent_tile_sides
                        & tile_sides_set
                    ).pop())

            # turns out everything was backwards, flip it
            if (tile_sides.index(adjacent_sides[0]) !=
                    (tile_sides.index(adjacent_sides[1]) + 1) % 4):
                tile.reverse()
                tile_sides = calc_sides(tile)
                adjacent_sides = ["".join(reversed(side))
                                  for side in adjacent_sides]

            # Re-align the tile with the right-adjacent side on the right (W)
            return align_tile(tile, adjacent_sides[0], 1)

        def align_tile(tile: list, side: str, position: int) -> list:
            """Align a tile so that the side at position == side."""
            tile = tile.copy()
            tile_sides = calc_sides(tile)
            side = "".join(reversed(side))

            if side not in tile_sides:
                tile.reverse()
                tile_sides = calc_sides(tile)

            if side not in tile_sides:
                raise Exception(f"{side} not found in {tile}")

            while tile_sides[position] != side:
                tile = rotate_tile(tile)
                tile_sides = calc_sides(tile)

            return tile

        aligned_tiles = list()
        for row, tile_ids in enumerate(grid):
            aligned_tiles.append(list())
            for col, tile_id in enumerate(tile_ids):
                if row == 0 and col == 0:
                    aligned_tiles[row].append(align_first_tile(tiles, grid))
                elif row == 0:
                    aligned_tiles[row].append(align_tile(
                        tiles[tile_id],
                        calc_sides(aligned_tiles[row][col - 1])[1],
                        3
                    ))
                else:
                    aligned_tiles[row].append(align_tile(
                        tiles[tile_id],
                        calc_sides(aligned_tiles[row - 1][col])[2],
                        0
                    ))

        return aligned_tiles

    def join_tiles(grid: list) -> list:
        return [
            "".join([
                tile[line_num][1:-1]
                for tile in tile_row
            ])
            for tile_row in grid
            for line_num in range(1, len(tile_row[0]) - 1)
        ]

    aligned_tiles = align_tiles(tiles, grid)

    image = join_tiles(aligned_tiles)
    if count_sea_monsters(image) > 0:
        return image

    for _ in range(3):
        image = rotate_tile(image)
        if count_sea_monsters(image) > 0:
            return image

    image.reverse()
    if count_sea_monsters(image) > 0:
        return image

    for _ in range(3):
        image = rotate_tile(image)
        if count_sea_monsters(image) > 0:
            return image

    raise Exception("No sea monsters found in any orientation.")


#   01234567890123456789
# 0 ..................#.
# 1 #....##....##....###
# 2 .#..#..#..#..#..#...
SEA_MONSTER = set([(1, 0), (2, 1), (2, 4), (1, 5), (1, 6),
                   (2, 7), (2, 10), (1, 11), (1, 12), (2, 13),
                   (2, 16), (1, 17), (1, 18), (0, 18), (1, 19)])
SEA_MONSTER_WIDTH = 20
SEA_MONSTER_HEIGHT = 3


def count_sea_monsters(image: list) -> int:
    """Count the number of sea monsters identified in the image."""
    count = 0
    for row in range(len(image) - SEA_MONSTER_HEIGHT):
        for col in range(len(image[0]) - SEA_MONSTER_WIDTH):
            for row_offset, col_offset in SEA_MONSTER:
                if image[row + row_offset][col + col_offset] != "#":
                    break
            else:
                count += 1
    return count


def paint_sea_monsters(image: list):
    """Paint the sea monsters with Os instead of #s."""
    for row in range(len(image) - SEA_MONSTER_HEIGHT):
        for col in range(len(image[0]) - SEA_MONSTER_WIDTH):
            for row_offset, col_offset in SEA_MONSTER:
                if image[row + row_offset][col + col_offset] != "#":
                    break
            else:
                for row_offset, col_offset in SEA_MONSTER:
                    image[row + row_offset] = (
                        image[row + row_offset][:col + col_offset] +
                        "O" +
                        image[row + row_offset][col + col_offset + 1:]
                    )


def compute_grid(tiles: dict) -> list:
    """Compute the grid arrangement based on a set of tiles."""

    def match_edges(tiles: dict) -> dict:
        sides = collections.defaultdict(list)

        for tile_id, tile in tiles.items():
            for side in calc_sides(tile):
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


def calc_sides(tile: list) -> list:
    """Compute the sides of each tile, returned in a N W S E order."""

    return [
        tile[0],
        "".join([line[-1] for line in tile]),
        "".join(reversed(tile[-1])),
        "".join([line[0] for line in reversed(tile)]),
    ]


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
