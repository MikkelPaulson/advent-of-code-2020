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

    def evaluate(expression: list) -> int:
        for i, element in enumerate(expression):
            if isinstance(element, list):
                expression[i] = evaluate(element)

        while len(expression) > 1:
            lhs, oper, rhs = expression[0:3]

            if oper == '+':
                result = lhs + rhs
            elif oper == '*':
                result = lhs * rhs
            else:
                raise Exception(f"Invalid operator: {oper}")

            expression[0:3] = [result]

        return expression[0]

    total = 0
    expressions = parse(stdin)
    for expression in expressions:
        stderr.write(f"{expression} = ")
        result = evaluate(expression)
        stderr.write(f"{result}\n")
        total += result

    return str(total)


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of strings representing the expressions.
    """

    def parse_expression(expression: str) -> list:
        """Parse an expression to return the integer result."""

        def parse_expression_part(expression: str) -> (list, str):
            """Parse an expression, consuming part and returning the rest."""

            result = list()

            while expression != "":
                if expression.startswith("("):
                    part, expression = parse_expression_part(expression[1:])
                    result.append(part)
                else:
                    match = SPLIT_PATTERN.match(expression)
                    result.append(int(match.group(1)))
                    expression = match.group(2)

                if expression != "":
                    oper, expression = expression[0], expression[1:]
                    if oper == ")":
                        return result, expression
                    result.append(oper)

            return result, ""

        result, _ = parse_expression_part(expression.replace(" ", ""))
        return result

    return [
        parse_expression(line)
        for line in stdin.read().strip().splitlines()
    ]
