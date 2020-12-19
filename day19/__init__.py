"""https://adventofcode.com/2020/day/19"""

import io
import re


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    Before you can help with the homework, you need to understand it yourself.
    Evaluate the expression on each line of the homework; what is the sum of
    the resulting values?
    """

    def compile_rule(rules: dict, index: int) -> str:
        if isinstance(rules[index], str):
            return rules[index]

        pattern = "|".join([
            "".join(map(lambda i: compile_rule(rules, i), options))
            for options in rules[index]
        ])

        if len(rules[index]) > 1:
            pattern = f"({pattern})"

        print(f"{index}: {pattern}")

        rules[index] = pattern
        return pattern

    rules, messages = parse(stdin)
    stderr.write(f"{rules}\n")
    stderr.write(f"{messages}\n")
    stderr.write(f"{compile_rule(rules, 0)}\n")

    pattern = re.compile(compile_rule(rules, 0))
    return str(len(list(filter(
        lambda message: pattern.fullmatch(message) is not None,
        messages
    ))))


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a 2-tuple containing a dict of rules and a list of
    strings to match against. Each rule is either a string (indicating a
    literal) or a list of lists, each parent list representing an option and
    each child representing the sequence of sub-patterns to match.
    """

    def parse_rule(rule: str):
        if rule[0] == "\"":
            return rule[1]

        return [
            [
                int(ref)
                for ref in option.split()
            ]
            for option in rule.split(" | ")
        ]

    rules, messages = stdin.read().strip().split("\n\n")

    return (
        {
            int(field): parse_rule(value)
            for line in rules.splitlines()
            for field, value in [line.split(": ")]
        },
        messages.splitlines()
    )
