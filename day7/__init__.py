"""https://adventofcode.com/2020/day/7"""

import collections
import re


def part1(stdin, stdout, stderr):
    """
    You have a shiny gold bag. If you wanted to carry it in at least one
    other bag, how many different bag colors would be valid for the
    outermost bag?
    """

    containers = parse(stdin)
    stderr.write(f"{containers}\n")
    contents = flip(containers)
    stderr.write(f"{contents}\n")

    count = 0
    options = {"shiny gold"}
    while count < len(options):
        stderr.write(f"{count}\n")
        count = len(options)
        options.update(
            *(contents[x] for x in options)
        )

    stderr.write(f"{options}\n")
    stdout.write(f"{count - 1}\n")


def flip(containers):
    """
    Invert the input so that instead of representing the containers, we
    represent the bags that can be contained in each container.
    """

    contents = collections.defaultdict(set)
    for container in containers:
        for content in containers[container]:
            contents[content].add(container)

    return contents


def parse(stdin):
    """
    Parse a rule sets into a dict of arrays. Each element is a bag type, each
    value represents all bags that that type can contain.
    """

    return dict(
        parse_rule(line)
        for line in stdin.read().strip().split("\n")
    )


def parse_rule(line):
    """
    Parse a single rule line to a key/value pair.

    Input: "vibrant lavender bags contain 1 shiny coral bag, 4 dotted purple
            bags."
    Output: "vibrant lavender", ["shiny coral", "dotted purple"]

    Input: "shiny indigo bags contain no other bags."
    Output: "shiny indigo", []
    """

    container, content_raw = line.split(" bags contain ")
    if content_raw == 'no other bags.':
        contents = set()
    else:
        contents = set(
            re.sub(r"[0-9]+ ([a-z ]+) bags?\.?", r"\1", bag_raw)
            for bag_raw in content_raw.split(", ")
        )

    return container, contents
