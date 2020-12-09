"""https://adventofcode.com/2020/day/3"""


def part1(stdin, stderr):
    """
    Starting at the top-left corner of your map and following a slope of right
    3 and down 1, how many trees would you encounter?
    """

    tree_count = 0
    y_pos = 0

    for line in stdin:
        if is_tree(3, 1, line, y_pos, stderr):
            tree_count += 1
        y_pos += 1

    return str(tree_count)


def part2(stdin, stderr):
    """
    Determine the number of trees you would encounter if, for each of the
    following slopes, you start at the top-left corner and traverse the map all
    the way to the bottom:

    * Right 1, down 1.
    * Right 3, down 1. (This is the slope you already checked.)
    * Right 5, down 1.
    * Right 7, down 1.
    * Right 1, down 2.

    What do you get if you multiply together the number of trees encountered on
    each of the listed slopes?
    """

    slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
    tree_counts = [0, 0, 0, 0, 0]
    y_pos = 0

    for line in stdin:
        for i in range(0, 5):
            if is_tree(slopes[i][0], slopes[i][1], line, y_pos, stderr):
                tree_counts[i] += 1
        y_pos += 1

    result = tree_counts[0]
    for element in tree_counts[1:]:
        result *= element

    return str(result)


def is_tree(x_step, y_step, line, y_pos, stderr):
    """
    Determine if a tree is present, given a line, line number, and x/y steps.
    """

    debug = f"{x_step},{y_step}  "

    if y_pos % y_step == 0:
        x_pos = (int(y_pos / y_step) * x_step) % len(line.strip())
        if line[x_pos] == "#":
            stderr.write(debug + ("%2d  " % x_pos)
                         + line[:x_pos] + "X" + line[x_pos + 1:])
            return True

        line = ("%2d  " % x_pos) + line[:x_pos] + "O" + line[x_pos + 1:]
    else:
        line = " -  " + line

    stderr.write(debug + line)
    return False
