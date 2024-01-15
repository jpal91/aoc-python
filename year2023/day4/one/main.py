import re

CARD_REGEX = re.compile(r'Card\s+\d+: (.*)', re.DOTALL)
LISTS_REGEX = re.compile(r'\s+')

def get_lists(card: str) -> tuple[set[str], set[str]]:
    card = CARD_REGEX.match(card).group(1)
    lists = card.split('|')
    winning, have = LISTS_REGEX.split(lists[0].strip()), LISTS_REGEX.split(lists[1].strip())

    return set(winning), set(have)

def get_score(matches: int) -> int:
    if matches == 0:
        return 0
    elif matches == 1:
        return 1
    
    return get_score(matches - 1) * 2

puzzle_test = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

if __name__ == '__main__':
    with open('day4/one/puzzle.txt') as f:
        puzzle = f.readlines()
    
    puzzle_test = puzzle_test.split('\n')
    total = 0

    for p in puzzle:
        if not p:
            continue
        win, have = get_lists(p)

        sect = win.intersection(have)
        score = get_score(len(sect))

        total += score

    print(total)
