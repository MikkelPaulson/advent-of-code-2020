"""https://adventofcode.com/2020/day/1"""

import array


def part1(stdin, stdout, stderr):
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
            stdout.write(f"{number * pair}\n")
            return
        except ValueError:
            numbers.append(number)

    raise Exception("No matches found.")


def part2(stdin, stdout, stderr):
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
                stdout.write(f"{numbers[i] * numbers[j] * numbers[k]}\n")
                return
            except ValueError:
                pass

    raise Exception("No matches found.")
