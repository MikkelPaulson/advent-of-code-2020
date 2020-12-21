"""https://adventofcode.com/2020/day/2"""

import io
import os
import subprocess


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Each line gives the password policy and then the password. The password
    policy indicates the lowest and highest number of times a given letter must
    appear for the password to be valid. For example, 1-3 a means that the
    password must contain a at least 1 time and at most 3 times.

    How many passwords are valid according to their policies?
    """

    return gawk("part1.gawk", stdin, stderr)


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Each policy actually describes two positions in the password, where 1 means
    the first character, 2 means the second character, and so on. (Be careful;
    Toboggan Corporate Policies have no concept of "index zero"!) Exactly one
    of these positions must contain the given letter. Other occurrences of the
    letter are irrelevant for the purposes of policy enforcement.

    How many passwords are valid according to the new interpretation of the
    policies?
    """

    return gawk("part2.gawk", stdin, stderr)


def gawk(
        script: str,
        stdin: io.TextIOWrapper,
        stderr: io.TextIOWrapper
) -> int:
    """Execute a gawk command in the current directory."""

    command = f"gawk -f {os.path.dirname(os.path.realpath(__file__))}/{script}"

    stderr.write(f"{command}\n")
    result = subprocess.run(
        command,
        stdin=stdin,
        capture_output=True,
        check=True,
        shell=True
    )

    return int(result.stdout.decode().strip())
