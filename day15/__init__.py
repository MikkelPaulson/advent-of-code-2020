"""https://adventofcode.com/2020/day/15"""

import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Given your starting numbers, what will be the 2020th number spoken?
    """

    return nth(stdin, stderr, 2020)


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Given your starting numbers, what will be the 30000000th number spoken?
    """

    return nth(stdin, stderr, 30000000)


def nth(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper, end: int) -> int:
    """
    Brute-force the nth number spoken given an input set of numbers.
    """

    debug_interval = end // 100
    numbers = parse(stdin)
    number = next(reversed(numbers.keys()))

    for turn in range(len(numbers), end):
        (prev, last) = numbers.get(number)

        if turn % debug_interval == 0:
            stderr.write(
                f"{turn}: {number} was previously spoken in turn {prev}"
            )

        if prev is None:
            number = 0
        else:
            number = last - prev

        if turn % debug_interval == 0:
            stderr.write(f", so I say \"{number}\"\n")

        if prev is None:
            number = 0
        else:
            number = last - prev

        numbers[number] = (numbers.get(number, (None, None))[1], turn)

    return number


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of ints.
    """

    return {
        int(v): (None, k)
        for k, v in enumerate(stdin.read().strip().split(","))
    }
