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
        bus: math.ceil(time / bus) * bus - time
        for bus in buses.values()
    }
    stderr.write(f"{departure_times}\n")

    next_bus = min(departure_times, key=departure_times.get)

    return f"{next_bus * departure_times[next_bus]}"


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> str:
    """
    What is the earliest timestamp such that all of the listed bus IDs depart
    at offsets matching their positions in the list?
    """

    _, buses_dict = parse(stdin)
    buses = [{"number": v, "offset": k} for k, v in buses_dict.items()]
    stderr.write(f"{buses}\n")

    def gcd(a, b):
        while b != 0:
            (a, b) = (b, a % b)
        return a

    def lcm(a, b):
        return a * b // gcd(a, b)

    result = 0
    increment = 1
    iterations = 0

    for bus in buses:
        stderr.write(f"Testing bus {bus}\n")
        while (result + bus["offset"]) % bus["number"] != 0:
            result += increment
            iterations += 1

        stderr.write(
            f"({result} + {bus['offset']}) % {bus['number']} == 0, "
            f"now incrementing by lcm({increment}, {bus['number']}) = "
            f"{lcm(increment, bus['number'])}\n"
        )

        increment = lcm(increment, bus["number"])

    stderr.write(f"Complete in {iterations} iterations\n")

    return str(result)


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of tuples: string direction and int distance.
    """

    data = stdin.read().strip().splitlines()

    return int(data[0]), {
        offset: int(bus)
        for offset, bus in enumerate(data[1].split(",")) if bus != 'x'
    }
