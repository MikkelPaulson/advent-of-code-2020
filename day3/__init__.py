def main(argv, stdin, stdout, stderr):
    """Module entry point."""
    if len(argv) >= 3 and argv[2] == '2':
        part2(stdin, stdout, stderr)
    else:
        part1(stdin, stdout, stderr)


def part1(stdin, stdout, stderr):
    """
    Starting at the top-left corner of your map and following a slope of right
    3 and down 1, how many trees would you encounter?
    """

    x_coordinate = 0

    x_offset = 3
    tree_count = 0

    for line in stdin:
        if line[x_coordinate] == "#":
            line = line[:x_coordinate] + "X" + line[x_coordinate + 1:]
            tree_count += 1
        else:
            line = line[:x_coordinate] + "O" + line[x_coordinate + 1:]

        stderr.write(line)

        x_coordinate = (x_coordinate + x_offset) % len(line.strip())

    stdout.write(f"{tree_count}\n")



def part2(stdin, stdout, stderr):
    pass
