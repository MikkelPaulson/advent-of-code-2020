"""https://adventofcode.com/2020/day/8"""


def part1(stdin, stdout, stderr):
    """
    Run your copy of the boot code. Immediately before any instruction is
    executed a second time, what value is in the accumulator?
    """

    commands = parse(stdin)

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

        stderr.write(f"{line} {acc} {commands[line][0]} {commands[line][1]}\n")

    stdout.write(f"{acc}\n")


def parse(stdin):
    """
    Parse a rule sets into a dict of arrays. Each element is a bag type, each
    value represents all bags that that type can contain.
    """

    return [
        tuple(line.split(" ")) for line in stdin.read().strip().split("\n")
    ]
