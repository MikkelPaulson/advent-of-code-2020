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


def play(cups: list, rounds: int):
    """
    Play the game for a specified number of rounds. Modifies cups in place.
    """

    def play_round(cups: list, current_cup: int) -> int:
        """
        Play a round of the cup game. Returns the new current cup.
        """

        i = cups.index(current_cup)
        cups_in_hand = cups[i+1:i+4]
        del cups[i+1:i+4]

        while len(cups_in_hand) < 3:
            cups_in_hand.append(cups.pop(0))

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

    current_cup = cups[0]
    for _ in range(rounds):
        current_cup = play_round(cups, current_cup)


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a list of ints representing the order of the cups.
    """

    return [int(c) for c in stdin.read().strip()]
