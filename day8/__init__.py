"""https://adventofcode.com/2020/day/8"""


def part1(stdin, stdout, _stderr):
    """
    Run your copy of the boot code. Immediately before any instruction is
    executed a second time, what value is in the accumulator?
    """

    commands = parse(stdin)
    acc, _ = run(commands)
    stdout.write(f"{acc}\n")


def parse(stdin):
    """
    Parse an input program into an array of tuples.
    """

    return [
        tuple(line.split(" ")) for line in stdin.read().strip().split("\n")
    ]


def run(commands):
    """
    Execute an input program. Returns the acc value and a boolean indicating if
    the program exited cleanly or encountered a loop.
    """

    run_count = set()
    acc = 0
    line = 0

    while line not in run_count:
        run_count.add(line)

        if commands[line][0] == 'acc':
            acc += int(commands[line][1])

        if commands[line][0] == 'jmp':
            line += int(commands[line][1])
        else:
            line += 1

        if line >= len(commands):
            return acc, True

    return acc, False
