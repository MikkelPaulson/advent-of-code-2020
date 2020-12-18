"""https://adventofcode.com/2020/day/18"""

import io
import re

SPLIT_PATTERN = re.compile(r"^([0-9]+)(.*)$")


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    Before you can help with the homework, you need to understand it yourself.
    Evaluate the expression on each line of the homework; what is the sum of
    the resulting values?
    """

    total = 0
    expressions = parse(stdin)
    for expression in expressions:
        result = evaluate(expression)
        stderr.write(f"{expression} = {result}\n")
        total += result

    return str(total)


def evaluate(expression: str) -> int:
    """Parse an expression to return the integer result."""

    def evaluate_part(expression: str) -> (int, str):
        """Parse an expression, consuming part and returning the rest."""

        result = 0
        oper = "+"

        while expression != "":
            if expression.startswith("("):
                lhs, expression = evaluate_part(expression[1:])
            else:
                match = SPLIT_PATTERN.match(expression)
                lhs = int(match.group(1))
                expression = match.group(2)

            if oper == "+":
                result += lhs
            elif oper == "*":
                result *= lhs
            else:
                raise Exception(f"Unexpected operator: {oper}")

            if expression != "":
                oper, expression = expression[0], expression[1:]
                if oper == ")":
                    return result, expression

        return result, ""

    result, _ = evaluate_part(expression.replace(" ", ""))
    return result


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of strings representing the expressions.
    """

    return stdin.read().strip().splitlines()
