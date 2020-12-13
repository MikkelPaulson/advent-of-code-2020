"""https://adventofcode.com/2020/day/13"""

import io
import math


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    What is the ID of the earliest bus you can take to the airport multiplied
    by the number of minutes you'll need to wait for that bus?
    """

    time, buses = parse(stdin)

    stderr.write(f"{time}\n")
    stderr.write(f"{buses}\n")

    departure_times = {
        bus: math.ceil(time / bus) * bus - time for bus in buses
    }
    stderr.write(f"{departure_times}\n")

    next_bus = min(departure_times, key=departure_times.get)

    return f"{next_bus * departure_times[next_bus]}"


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of tuples: string direction and int distance.
    """

    data = stdin.read().strip().splitlines()

    return int(data[0]), [
        int(bus) for bus in data[1].split(",") if bus != 'x'
    ]
