"""https://adventofcode.com/2020/day/19"""

import io
import re


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    How many messages completely match rule 0?
    """

    rules, messages = parse(stdin)
    stderr.write(f"{compile_rule(rules, 0)}\n")

    pattern = re.compile(compile_rule(rules, 0))
    return len(list(filter(
        lambda message: pattern.fullmatch(message) is not None,
        messages
    )))


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    After updating rules 8 and 11, how many messages completely match rule 0?
    """

    rules, messages = parse(stdin)
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    stderr.write(f"{compile_rule(rules, 0)}\n")

    pattern = re.compile(compile_rule(rules, 0))
    return len(list(filter(
        lambda message: pattern.fullmatch(message) is not None,
        messages
    )))


def compile_rule(rules: dict, index: int) -> str:
    """
    Compule a rule based on all referenced rules. Hard-coded to avoid the
    circular reference in the new rules 8 and 11.
    """

    if isinstance(rules[index], str):
        return rules[index]

    if index == 8 and len(rules[8]) > 1:
        rules[index] = f"({compile_rule(rules, 42)})+"
        return rules[index]
    if index == 11 and len(rules[11]) > 1:
        rules[index] = "(" + "|".join([
            f"({compile_rule(rules, 42)})" + "{" + str(i) + "}"
            f"({compile_rule(rules, 31)})" + "{" + str(i) + "}"
            for i in range(1, 10)
        ]) + ")"

        return rules[index]

    pattern = "|".join([
        "".join(map(lambda i: compile_rule(rules, i), options))
        for options in rules[index]
    ])

    if len(rules[index]) > 1:
        pattern = f"({pattern})"

    rules[index] = pattern
    return pattern


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
