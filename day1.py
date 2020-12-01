"""
Before you leave, the Elves in accounting just need you to fix your
expense report (your puzzle input); apparently, something isn't quite
adding up.

Specifically, they need you to find the two entries that sum to 2020
and then multiply those two numbers together.

For example, suppose your expense report contained the following:

    1721
    979
    366
    299
    675
    1456

In this list, the two entries that sum to 2020 are 1721 and 299.
Multiplying them together produces 1721 * 299 = 514579, so the correct
answer is 514579.

Of course, your expense report is much larger. Find the two entries
that sum to 2020; what do you get if you multiply them together?
"""

import array


def main(argv, stdin, stdout, stderr):
    """Module entry point."""
    if len(argv) >= 3 and argv[2] == '2':
        part2(stdin, stdout, stderr)
    else:
        part1(stdin, stdout, stderr)


def part1(stdin, stdout, stderr):
    """Find two numbers that sum to 2020, then multiply them."""

    numbers = array.array('i')

    for line in stdin:
        number = int(line.strip())
        pair = 2020 - number

        try:
            numbers.index(pair)
            stderr.write(str(number) + " + " + str(pair) + "\n")
            stdout.write(str(number * pair) + "\n")
            return
        except ValueError:
            numbers.append(number)

    raise Exception("No matches found.")


def part2(stdin, stdout, stderr):
    """Find three numbers that sum to 2020, then multiple them."""

    numbers = array.array('i')

    for line in stdin:
        numbers.append(int(line.strip()))

    for i in range(len(numbers) - 2):
        for j in range(i + 1, len(numbers) - 1):
            for k in range(j + 1, len(numbers)):
                if numbers[i] + numbers[j] + numbers[k] == 2020:
                    stderr.write(
                        str(numbers[i]) + " + " + str(numbers[j]) + " + "
                        + str(numbers[k]) + "\n")
                    stdout.write(
                        str(numbers[i] * numbers[j] * numbers[k]) + "\n")
                    return

    raise Exception("No matches found.")
