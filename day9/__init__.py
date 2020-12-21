"""https://adventofcode.com/2020/day/9"""

import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    The first step of attacking the weakness in the XMAS data is to find the
    first number in the list (after the preamble) which is not the sum of two
    of the 25 numbers before it. What is the first number that does not have
    this property?
    """

    data = parse(stdin)
    return get_invalid(data, stderr, 25)


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    The final step in breaking the XMAS encryption relies on the invalid number
    you just found: you must find a contiguous set of at least two numbers in
    your list which sum to the invalid number from step 1.
    """

    data = parse(stdin)

    target = get_invalid(data, stderr, 25)
    window_start = 0
    window_end = 2
    window_sum = sum(data[window_start:window_end])

    while window_end < len(data):
        stderr.write(f"{data[window_start:window_end]}")

        if window_sum < target or window_end - window_start <= 2:
            stderr.write(f" < {target}\n")
            window_sum += data[window_end]
            window_end += 1
        elif window_sum > target:
            stderr.write(f" > {target}\n")
            window_sum -= data[window_start]
            window_start += 1
        else:
            stderr.write(f" = {target}\n")
            return (min(data[window_start:window_end]) +
                    max(data[window_start:window_end]))

    raise Exception("No matches found.")


def parse(stdin):
    """
    Parse an input data set into a list.
    """

    return [
        int(line) for line in stdin.read().strip().split("\n")
    ]


def get_invalid(data, stderr, preamble_size=25):
    def is_valid(value, preamble):
        for i, _ in enumerate(preamble):
            for j in range(i, len(preamble)):
                if preamble[i] + preamble[j] == value:
                    stderr.write(f"{preamble[i]} + {preamble[j]} = {value}\n")
                    return True
        return False

    for i in range(preamble_size, len(data)):
        if not is_valid(data[i], data[i - preamble_size:i]):
            return data[i]

    raise Exception("No invalid values found.")
