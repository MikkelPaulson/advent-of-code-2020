"""https://adventofcode.com/2020/day/6"""


def part1(stdin, stdout, stderr):
    """
    For each group, count the number of questions to which anyone answered
    "yes". What is the sum of those counts?
    """

    groups = parse(stdin)
    totals = [
        len(set.union(*group)) for group in groups
    ]

    stderr.write(f"{totals}\n")
    stdout.write(f"{sum(totals)}\n")


def part2(stdin, stdout, stderr):
    """
    For each group, count the number of questions to which everyone answered
    "yes". What is the sum of those counts?
    """

    groups = parse(stdin)
    intersections = [
        len(set.intersection(*group)) for group in groups
    ]

    stderr.write(f"{intersections}\n")
    stdout.write(f"{sum(intersections)}\n")


def parse(stdin):
    """Parse a raw declaration form input."""

    return [
        [
            set(answer for answer in person)
            for person in group.split("\n")
        ]
        for group in stdin.read().strip().split("\n\n")
    ]
