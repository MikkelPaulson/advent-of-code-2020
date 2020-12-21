"""https://adventofcode.com/2020/day/1"""

import array
import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """Find two numbers that sum to 2020, then multiply them."""

    numbers = array.array('i')

    iterations = 0
    for line in stdin:
        iterations += 1
        number = int(line.strip())
        pair = 2020 - number

        try:
            numbers.index(pair)
            stderr.write(f"{number} + {pair} in {iterations} iterations\n")
            return number * pair
        except ValueError:
            numbers.append(number)

    raise Exception("No matches found.")


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """Find three numbers that sum to 2020, then multiply them."""

    numbers = array.array('i')

    for line in stdin:
        numbers.append(int(line.strip()))

    iterations = 0
    for i in range(len(numbers) - 2):
        for j in range(i + 1, len(numbers) - 1):
            iterations += 1
            try:
                k = numbers.index(2020 - numbers[i] - numbers[j])
                stderr.write(f"{numbers[i]} + {numbers[j]} + {numbers[k]} in "
                             + f"{iterations} iterations\n")
                return numbers[i] * numbers[j] * numbers[k]
            except ValueError:
                pass

    raise Exception("No matches found.")
