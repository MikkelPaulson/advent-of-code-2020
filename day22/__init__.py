"""https://adventofcode.com/2020/day/22"""

import functools
import io


def part1(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Play the small crab in a game of Combat using the two decks you just dealt.
    What is the winning player's score?
    """

    def play_round(hands: tuple):
        cards = (hands[0].pop(0), hands[1].pop(0))

        if cards[0] > cards[1]:
            hands[0].append(cards[0])
            hands[0].append(cards[1])
        else:
            hands[1].append(cards[1])
            hands[1].append(cards[0])

    hands = parse(stdin)

    while hands[0] and hands[1]:
        stderr.write(f"{hands}\n")
        play_round(hands)

    stderr.write(f"{hands}\n")

    return score(hands[0] if hands[0] else hands[1])


def part2(stdin: io.TextIOWrapper, stderr: io.TextIOWrapper) -> int:
    """
    Defend your honor as Raft Captain by playing the small crab in a game of
    Recursive Combat using the same two decks as before. What is the winning
    player's score?
    """

    def play(hands: tuple, stderr: io.TextIOWrapper) -> int:
        rounds = set()

        while hands[0] and hands[1]:
            key = (score(hands[0]), score(hands[1]))
            if key in rounds:
                return 0

            rounds.add(key)
            stderr.write(f"{hands}\n")

            cards = (hands[0].pop(0), hands[1].pop(0))

            if cards[0] <= len(hands[0]) and cards[1] <= len(hands[1]):
                stderr.write("Recursing...\n")
                winner = play((
                    hands[0][:cards[0]],
                    hands[1][:cards[1]],
                ), stderr)
                stderr.write(f"Player {winner + 1} wins the sub-game.\n")
            elif cards[0] > cards[1]:
                winner = 0
            else:
                winner = 1

            stderr.write(f"Player {winner + 1} wins the round.\n")
            hands[winner].append(cards[winner])
            hands[winner].append(cards[1 - winner])

        return 0 if hands[0] else 1

    hands = parse(stdin)
    winner = play(hands, stderr)

    stderr.write(f"{hands}\n")

    return score(hands[winner])


def score(hand: list) -> int:
    """Calculate the score of a winning hand."""

    return functools.reduce(
        lambda score, card: score + card[1] * (len(hand) - card[0]),
        enumerate(hand),
        0
    )


def parse(stdin: io.TextIOWrapper) -> list:
    """
    Parse the input into a tuple of lists representing the two players' hands.
    """

    player1, player2 = stdin.read().strip().split("\n\n", 1)

    return (
        [int(i) for i in player1.splitlines()[1:]],
        [int(i) for i in player2.splitlines()[1:]],
    )
