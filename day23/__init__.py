"""https://adventofcode.com/2020/day/23"""

import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Using your labeling, simulate 100 moves. What are the labels on the cups
    after cup 1?
    """

    cups = parse(stdin)

    current_cup = cups[0]

    for round_num in range(100):
        stderr.write(
            f"move {round_num + 1}: " + " ".join(map(str, cups)).replace(
                str(current_cup), f"({current_cup})"
            ) + "\n"
        )
        current_cup = play_round(cups, current_cup)

    stderr.write(f"End of game: {cups}\n")

    output = cups[cups.index(1) + 1:] + cups[:cups.index(1)]
    return sum(map(
        lambda cup: cup[1] * pow(10, cup[0]),
        enumerate(reversed(output))
    ))


def play_round(cups: list, current_cup: int) -> int:
    """
    Play a round of the cup game. Returns the new current cup.
    """

    cups_in_hand = list()
    for _ in range(3):
        cups_in_hand.append(cups.pop(
            (cups.index(current_cup) + 1) % len(cups)))

    destination_cup = current_cup - 1
    while destination_cup > 0:
        try:
            destination_index = cups.index(destination_cup)
            break
        except ValueError:
            destination_cup -= 1
    else:
        destination_index = cups.index(max(cups))

    cups[destination_index + 1:destination_index + 1] = cups_in_hand

    return cups[(cups.index(current_cup) + 1) % len(cups)]


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of ints representing the order of the cups.
    """

    return [int(c) for c in stdin.read().strip()]
