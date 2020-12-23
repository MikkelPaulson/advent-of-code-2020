"""https://adventofcode.com/2020/day/23"""

import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Using your labeling, simulate 100 moves. What are the labels on the cups
    after cup 1?
    """

    cups = parse(stdin)

    play(cups, 100)

    stderr.write(f"End of game: {cups}\n")

    output = cups[cups.index(1) + 1:] + cups[:cups.index(1)]
    return sum(map(
        lambda cup: cup[1] * pow(10, cup[0]),
        enumerate(reversed(output))
    ))


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Determine which two cups will end up immediately clockwise of cup 1. What
    do you get if you multiply their labels together?
    """

    cups = parse(stdin)
    cups += range(len(cups) + 1, 1000001)

    play(cups, 10000000)

    next_cups = [cups[cups.index(1) + i] % len(cups) for i in [1, 2]]
    stderr.write(f"{next_cups[0]} * {next_cups[1]} = "
                 f"{next_cups[0] * next_cups[1]}\n")

    return next_cups[0] * next_cups[1]


def play(cups: list, rounds: int):
    """
    Play the game for a specified number of rounds. Modifies cups in place.
    """

    def play_round(edges: dict, current_cup: int) -> int:
        """
        Play a round of the cup game. Returns the new current cup.
        """

        max_cup = len(edges)

        cups_in_hand = [edges[current_cup]]
        while len(cups_in_hand) < 3:
            cups_in_hand.append(edges.pop(cups_in_hand[-1]))
        edges[current_cup] = edges.pop(cups_in_hand[-1])

        destination_cup = current_cup - 1 if current_cup != 1 else max_cup
        while destination_cup in cups_in_hand:
            destination_cup -= 1
            if destination_cup < 1:
                destination_cup = max_cup

        while cups_in_hand:
            edges[cups_in_hand[-1]] = edges[destination_cup]
            edges[destination_cup] = cups_in_hand.pop()

        return edges[current_cup]

    def cups_to_edges(cups: list) -> dict:
        edges = {cups[i]: cups[i + 1] for i in range(len(cups) - 1)}
        edges[cups[-1]] = cups[0]
        return edges

    def edges_to_cups(edges: dict) -> list:
        cups = [1]
        index = edges[1]
        while index != 1:
            cups.append(index)
            index = edges[index]
        return cups

    current_cup = cups[0]

    edges = cups_to_edges(cups)

    for _ in range(rounds):
        current_cup = play_round(edges, current_cup)

    cups[:] = edges_to_cups(edges)


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of ints representing the order of the cups.
    """

    return [int(c) for c in stdin.read().strip()]
