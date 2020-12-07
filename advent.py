"""
Advent of Code is an Advent calendar of small programming puzzles for a variety
of skill sets and skill levels that can be solved in any programming language
you like. People use them as a speed contest, interview prep, company training,
university coursework, practice problems, or to challenge each other.

https://adventofcode.com/2020/
"""

import sys


def main(argv, stdin, stdout, stderr):
    """Dispatcher. This will probably make someone's eyes bleed."""

    if len(argv) != 2:
        stderr.write(f"Expected syntax: {argv[0]} [day].[part]\n")
        return 1

    try:
        [day, part] = [int(i) for i in argv[1].split('.', 2)]
    except ValueError:
        stderr.write(f"Expected syntax day.part, got {argv[1]}\n")
        return 1

    if day < 1 or day > 25:
        stderr.write(f"Invalid day: {day}\n")
        return 1
    if part < 1 or part > 2:
        stderr.write(f"Invalid part: {part}\n")
        return 1

    try:
        module = __import__(f"day{day}")
    except ModuleNotFoundError:
        stderr.write(f"Day {day} does not yet have a solution.\n")
        return 1

    def missing(_stdin, _stdout, stderr):
        stderr.write(f"Day {day} part {part} does not yet have a solution.\n")
        return 1

    if stdin.isatty():
        with open(f"day{day}/input.txt") as input_file:
            result = getattr(module, f"part{part}", missing)(
                input_file, stdout, stderr)
    else:
        result = getattr(module, f"part{part}", missing)(stdin, stdout, stderr)

    if result is None:
        result = 0

    return result


sys.exit(main(sys.argv, sys.stdin, sys.stdout, sys.stderr))
