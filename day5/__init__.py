"""https://adventofcode.com/2020/day/5"""


def part1(stdin, stderr):
    """
    As a sanity check, look through your list of boarding passes. What is the
    highest seat ID on a boarding pass?
    """

    tickets = parse(stdin)
    stderr.write(f"{tickets}\n")

    max_ticket = max(seat_ids(tickets))

    return str(max_ticket)


def part2(stdin, stderr):
    """
    It's a completely full flight, so your seat should be the only missing
    boarding pass in your list. However, there's a catch: some of the seats at
    the very front and back of the plane don't exist on this aircraft, so
    they'll be missing from your list as well.

    Your seat wasn't at the very front or back, though; the seats with IDs +1
    and -1 from yours will be in your list.

    What is the ID of your seat?
    """

    seats = sorted(seat_ids(parse(stdin)))

    for i in range(len(seats) - 1):
        stderr.write(
            f"{i}: {seats[i + 1]} - {seats[i]} = {seats[i + 1] - seats[i]}\n")

        if seats[i + 1] - seats[i] == 2:
            return str(seats[i] + 1)

    raise Exception("No matches found.")


def seat_ids(tickets):
    """Convert an array of (row, seat) tuples to seat IDs."""

    return [
        row * 8 + seat
        for (row, seat) in tickets
    ]


def parse(stdin):
    """Parse "FBFBBFFRLR" to "0101100101", then to (44, 5)."""

    return [
        (
            int(line[:7].replace("B", "1").replace("F", "0"), 2),
            int(line[7:10].replace("R", "1").replace("L", "0"), 2),
        )
        for line in stdin.readlines()
    ]
