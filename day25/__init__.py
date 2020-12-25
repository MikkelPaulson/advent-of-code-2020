"""https://adventofcode.com/2020/day/25"""

import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    What encryption key is the handshake trying to establish?
    """

    public_keys = parse(stdin)
    loop_size = [None, None]
    subject_number = 7
    result = 1

    iterations = 0
    while None in loop_size:
        iterations += 1
        result = (result * subject_number) % 20201227
        stderr.write(f"{iterations}: {result} ({loop_size})\n")
        if result in public_keys:
            loop_size[public_keys.index(result)] = iterations
            stderr.write(f"==> {public_keys.index(result)}\n")

    stderr.write("Negotiating encryption key:\n")
    subject_number = public_keys[0]
    result = 1
    for i in range(loop_size[1]):
        stderr.write(f"{i}: {result}\n")
        result = (result * subject_number) % 20201227

    return result


def parse(stdin: io.TextIOWrapper) -> [int]:
    """
    Parse the input into a list of ints, representing the public keys of the
    card and the door.
    """

    return tuple(int(line) for line in stdin.read().strip().splitlines())
