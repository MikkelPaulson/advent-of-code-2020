"""https://adventofcode.com/2020/day/2"""

import os
import subprocess


def part1(stdin, stdout, stderr):
    """
    Each line gives the password policy and then the password. The password
    policy indicates the lowest and highest number of times a given letter must
    appear for the password to be valid. For example, 1-3 a means that the
    password must contain a at least 1 time and at most 3 times.

    How many passwords are valid according to their policies?
    """

    gawk("part1.gawk", stdin, stdout, stderr)


def part2(stdin, stdout, stderr):
    """
    Each policy actually describes two positions in the password, where 1 means
    the first character, 2 means the second character, and so on. (Be careful;
    Toboggan Corporate Policies have no concept of "index zero"!) Exactly one
    of these positions must contain the given letter. Other occurrences of the
    letter are irrelevant for the purposes of policy enforcement.

    How many passwords are valid according to the new interpretation of the
    policies?
    """

    gawk("part2.gawk", stdin, stdout, stderr)


def gawk(script, stdin, stdout, stderr):
    """Execute a gawk command in the current directory."""

    subprocess.run("gawk -f " + os.path.dirname(os.path.realpath(__file__))
                   + "/" + script,
                   stdin=stdin,
                   stdout=stdout,
                   stderr=stderr,
                   check=True,
                   shell=True)
