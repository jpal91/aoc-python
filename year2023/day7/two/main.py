from collections import Counter

puzzle_test = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483\
"""

CARDS = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"][::-1]


def get_hand(h: list[str]) -> tuple[str, str, int]:
    hand, bid = h
    score = 0

    hand_count = Counter(hand)
    mc = hand_count.most_common()

    if "J" in hand_count and mc[0][1] != 5:
        _, bid, score = get_hand(
            [
                hand.replace(
                    "J", mc[0][0] if mc[0][0] != "J" else mc[1][0], hand_count["J"]
                ),
                bid,
            ]
        )
        return hand, bid, score

    if mc[0][1] == 5:
        score += 60
    elif mc[0][1] == 4:
        score += 50
    elif mc[0][1] == 3:
        score += 30
        if mc[1][1] == 2:
            score += 10
    elif mc[0][1] == 2:
        score += 10
        if mc[1][1] == 2:
            score += 10

    return hand, bid, score


def sort_hand(hands: list[tuple[str, str, int]]) -> list:
    return sorted(
        hands,
        key=lambda x: (x[2], *(CARDS.index(c) for c in x[0])),
    )


def parse(p: str) -> list:
    p = p.split("\n")
    return [line.split() for line in p]


if __name__ == "__main__":
    with open("day7/one/puzzle.txt") as f:
        puzzle = parse(f.read())

    # puzzle = parse(puzzle_test)

    hands = [get_hand(p) for p in puzzle]
    sorted_hand = sort_hand(hands)
    # print(hands)

    total = 0

    for i, hand in enumerate(sorted_hand):
        total += int(hand[1]) * (i + 1)

    print(total)
