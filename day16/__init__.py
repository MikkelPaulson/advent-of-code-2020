"""https://adventofcode.com/2020/day/15"""

import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    Given your starting numbers, what will be the 2020th number spoken?
    """

    fields, tickets = parse(stdin)
    all_groups = [j for i in fields.values() for j in i]
    all_groups.sort(key=lambda i: i[0])

    groups = list()
    group_min = None
    group_max = None

    for group in all_groups:
        if group_min is None:
            group_min, group_max = group
        elif group[0] > group_max + 1:  # this is a disparate group
            groups.append((group_min, group_max))
            group_min, group_max = group
        elif group[1] > group_max:
            group_max = group[1]

    groups.append((group_min, group_max))

    invalid_values = list()
    for ticket in tickets:
        for value in ticket:
            for (group_min, group_max) in groups:
                if value < group_min:
                    invalid_values.append(value)

                if value <= group_max:
                    break
            else:
                invalid_values.append(value)

    stderr.write(f"fields: {fields}\n")
    stderr.write(f"concatenated groups: {groups}\n")
    stderr.write(f"tickets: {tickets}\n")
    stderr.write(f"invalid values: {invalid_values}\n")
    return str(sum(invalid_values))


def parse(stdin: io.TextIOWrapper) -> tuple:
    """
    Parse the input into a tuple containing dict of ranges and an array of
    tickets. The first element of the dict is my ticket.
    """

    [raw_fields, my_ticket, other_tickets] = [
        v.strip() for v in stdin.read().split("\n\n")
    ]

    _, my_ticket = my_ticket.split("\n", 1)
    _, other_tickets = other_tickets.split("\n", 1)

    fields = dict()
    for line in raw_fields.splitlines():
        name, value = line.split(": ")
        fields[name] = [
            tuple(int(i) for i in group.split("-"))
            for group in value.split(" or ")
        ]

    # fields = {
    #     field: (value.split(" or "))
    #     for line in raw_fields.splitlines()
    #     for field, value in line.split(": ")
    # }

    tickets = [[int(field) for field in my_ticket.split(",")]] + [
        list(int(field) for field in ticket.split(","))
        for ticket in other_tickets.splitlines()
    ]

    return fields, tickets
