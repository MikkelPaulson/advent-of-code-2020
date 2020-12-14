"""https://adventofcode.com/2020/day/14"""

import functools
import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    Execute the initialization program. What is the sum of all values left in
    memory after it completes?
    """

    memory = dict()
    program = parse(stdin)

    for (mask, commands) in program:
        for (index, value) in commands:
            memory[index] = value
            for (offset, bit) in mask.items():
                if bit == 1:
                    memory[index] |= 1 << offset
                elif bit == 0:
                    memory[index] &= ~(1 << offset)

    stderr.write(f"{memory}\n")
    return f"{sum(memory.values())}"


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    Execute the initialization program using an emulator for a version 2
    decoder chip. What is the sum of all values left in memory after it
    completes?
    """

    memory = dict()
    program = parse(stdin)

    def get_floating_options(floating_bits: list) -> list:
        """
        Get the possible results for a given set of floating bits. Returns a
        2-tuple of the bitmask to _set_ and the bitmask to _remove_.
        """

        if len(floating_bits) == 0:
            return [(0, ~0)]

        result = []
        for i in range(1 << (len(floating_bits))):
            set_mask = 0
            clear_mask = 0
            for (j, offset) in enumerate(floating_bits):
                if i & (1 << j):
                    set_mask |= 1 << offset
                else:
                    clear_mask |= 1 << offset
            result.append((set_mask, ~clear_mask))

        return result

    for (mask, commands) in program:
        floating_bits = [k for k, v in mask.items() if v is None]
        set_bits = functools.reduce(
            lambda acc, item: acc | 1 << item[0] if item[1] == 1 else acc,
            mask.items(),
            0
        )

        stderr.write(f"{mask}\n")
        stderr.write(f"{floating_bits}\n")
        stderr.write(f"{set_bits}\n")

        stderr.write(f"{get_floating_options(floating_bits)}\n")

        for (set_mask, clear_mask) in get_floating_options(floating_bits):
            stderr.write(f"{set_bits} | {set_mask} & {clear_mask}\n")
            for (index, value) in commands:
                memory[(index | set_bits | set_mask) & clear_mask] = value

    return str(sum(memory.values()))


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of tuples, each with a little-endian bit mask
    represented as a list and a list of commands to execute.
    """

    return list(map(
        lambda chunk: (
            {
                35 - k: v
                for k, v in enumerate([
                    int(char) if char != 'X' else None
                    for char in chunk[0]
                ])
            },
            [
                tuple(map(int, command.replace("mem[", "").split("] = ", 1)))
                for command in chunk[1].strip().split("\n")
            ]
        ),
        [
            (chunk.split("\n", 1))
            for chunk in stdin.read().strip().split("mask = ") if chunk != ""
        ]
    ))
