"""https://adventofcode.com/2020/day/5"""


def part1(stdin, stdout, stderr):
    """
    As a sanity check, look through your list of boarding passes. What is the
    highest seat ID on a boarding pass?
    """

    tickets = parse(stdin)
    stderr.write(f"{tickets}\n")

    max_ticket = max([
        row * 8 + seat
        for (row, seat) in tickets
    ])

    stdout.write(f"{max_ticket}\n")


def parse(stdin):
    """
    Parse "FBFBBFFRLR" to "0101100101", then to (44, 5)
    """

    return [
        (
            int(line[:7].replace("B", "1").replace("F", "0"), 2),
            int(line[7:10].replace("R", "1").replace("L", "0"), 2),
        )
        for line in stdin.readlines()
    ]
