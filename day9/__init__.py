"""https://adventofcode.com/2020/day/8"""


def part1(stdin, stdout, stderr, preamble_size=25):
    """
    The first step of attacking the weakness in the XMAS data is to find the
    first number in the list (after the preamble) which is not the sum of two
    of the 25 numbers before it. What is the first number that does not have
    this property?
    """

    def is_valid(value, preamble):
        for i, _ in enumerate(preamble):
            for j in range(i, len(preamble)):
                if preamble[i] + preamble[j] == value:
                    stderr.write(f"{preamble[i]} + {preamble[j]} = {value}\n")
                    return True
        return False

    data = parse(stdin)
    for i in range(preamble_size, len(data)):
        if not is_valid(data[i], data[i - preamble_size:i]):
            stdout.write(f"{data[i]}\n")
            return

    raise Exception("No invalid values found.")


def parse(stdin):
    """
    Parse an input data set into a list.
    """

    return [
        int(line) for line in stdin.read().strip().split("\n")
    ]
