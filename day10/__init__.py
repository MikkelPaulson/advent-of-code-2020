"""https://adventofcode.com/2020/day/10"""


def part1(stdin, stderr):
    """
    Find a chain that uses all of your adapters to connect the charging outlet
    to your device's built-in adapter and count the joltage differences between
    the charging outlet, the adapters, and your device. What is the number of
    1-jolt differences multiplied by the number of 3-jolt differences?
    """

    adapters = parse(stdin)
    adapters.sort()

    gap_1_count = 0
    gap_3_count = 0
    prev = 0

    for adapter in adapters:
        stderr.write(f"{adapter} - {prev} = {adapter - prev}\n")
        if adapter - prev == 1:
            gap_1_count += 1
        elif adapter - prev == 3:
            gap_3_count += 1
        prev = adapter

    stderr.write(f"{prev + 3} - {prev} = 3\n")

    result = gap_1_count * (gap_3_count + 1)
    stderr.write(f"{gap_1_count} * {gap_3_count + 1} = {result}\n")
    return str(result)


def parse(stdin):
    """
    Parse an input data set into a list of integers.
    """

    return [
        int(line) for line in stdin.read().strip().split("\n")
    ]
