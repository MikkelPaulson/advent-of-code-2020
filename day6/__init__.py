"""https://adventofcode.com/2020/day/6"""


def part1(stdin, stdout, stderr):
    """
    For each group, count the number of questions to which anyone answered
    "yes". What is the sum of those counts?
    """

    groups = parse(stdin)
    totals = [
        len(group) for group in groups
    ]

    stderr.write(f"{totals}\n")
    stdout.write(f"{sum(totals)}\n")


def parse(stdin):
    """Parse a raw declaration form input."""

    return [
        set(
            answer
            for person in group.split("\n")
            for answer in person
        )
        for group in stdin.read().strip().split("\n\n")
    ]
