"""https://adventofcode.com/2020/day/10"""


def part1(stdin, stderr):
    """
    Find a chain that uses all of your adapters to connect the charging outlet
    to your device's built-in adapter and count the joltage differences between
    the charging outlet, the adapters, and your device. What is the number of
    1-jolt differences multiplied by the number of 3-jolt differences?
    """

    gaps = parse(stdin)

    gap_1_count = 0
    gap_3_count = 0

    for gap in gaps:
        if gap == 1:
            gap_1_count += 1
        elif gap == 3:
            gap_3_count += 1

    result = gap_1_count * (gap_3_count + 1)
    stderr.write(f"{gap_1_count} * {gap_3_count + 1} = {result}\n")
    return str(result)


def part2(stdin, stderr):
    """
    What is the total number of distinct ways you can arrange the adapters to
    connect the charging outlet to your device?
    """

    gaps = parse(stdin)
    combinations = 1
    last_3 = -1

    chunk_possibilities = {
        1: 1,  # 33
        2: 1,  # 313
        3: 2,  # 3113, 323
        4: 4,  # 31113, 3213, 3123, 333
        5: 7,  # 311113, 32113, 31213, 31123, 3223, 3313, 3133
    }

    gaps.append(3)
    for index, gap in enumerate(gaps):
        stderr.write(f"{index} {gap}")
        if gap == 3:
            stderr.write(f" {index - last_3}")
            combinations *= chunk_possibilities[index - last_3]
            last_3 = index
        stderr.write("\n")

    return str(combinations)


def parse(stdin):
    """
    Calculate the gaps between a sorted sequence of integers, starting at 0.
    """

    adapters = [
        int(line) for line in stdin.read().strip().split("\n")
    ]

    adapters.sort()
    gaps = []
    prev = 0
    for adapter in adapters:
        gaps.append(adapter - prev)
        prev = adapter

    return gaps
