"""https://adventofcode.com/2020/day/14"""

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
                else:
                    memory[index] &= ~(1 << offset)

    stderr.write(f"{memory}\n")
    return f"{sum(memory.values())}"


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
                ]) if v is not None
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
