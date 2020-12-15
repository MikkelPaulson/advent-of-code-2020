"""https://adventofcode.com/2020/day/15"""

import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    Given your starting numbers, what will be the 2020th number spoken?
    """

    numbers = parse(stdin)
    stderr.write(f"{numbers}\n")

    number = next(reversed(numbers.keys()))

    for turn in range(len(numbers), 2020):
        (prev, last) = numbers.get(number)

        stderr.write(f"{turn}: {number} was previously spoken in turn {prev}")

        if prev is None:
            number = 0
        else:
            number = last - prev

        stderr.write(f", so I say \"{number}\"\n")

        numbers[number] = (numbers.get(number, (None, None))[1], turn)

    return str(number)


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of ints.
    """

    return {
        int(v): (None, k)
        for k, v in enumerate(stdin.read().strip().split(","))
    }
