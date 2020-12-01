"""
Advent of Code is an Advent calendar of small programming puzzles for a variety
of skill sets and skill levels that can be solved in any programming language
you like. People use them as a speed contest, interview prep, company training,
university coursework, practice problems, or to challenge each other.
"""

import sys


def main(argv, stdin, stdout, stderr):
    """Dispatcher. This will probably make someone's eyes bleed."""

    if len(argv) < 2 or not argv[1].isnumeric():
        print("Expected syntax: " + argv[0] + " [day]")
        sys.exit(1)

    day = int(sys.argv[1])

    if day < 1 or day > 1:
        print("Invalid day: " + str(day))
        sys.exit(1)

    module = __import__("day" + str(day))
    getattr(module, "main")(argv, stdin, stdout, stderr)


main(sys.argv, sys.stdin, sys.stdout, sys.stderr)
