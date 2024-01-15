import os

test_puzzle = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

def parse_rucksack(sack: str) -> list[tuple[set[str], set[str]]]:
    res = []

    for s in sack.strip().split("\n"):
        n = len(s)
        pt1 = set({*s[:n // 2]})
        pt2 = set({*s[n // 2:]})
        res.append((pt1, pt2))
    
    return res

def part1(s: str):
    rucksacks: list[tuple[set, set]] = parse_rucksack(s)
    priority = 0

    for sack in rucksacks:
        pt1, pt2 = sack
        pt1.intersection_update(pt2)

        same = pt1.pop()

        if same.isupper():
            val = (ord(same) - 64) + 26
        else:
            val = ord(same) - 96
        
        priority += val
    
    return priority

def part2(s: str):
    rucksacks = parse_rucksack(s)
    priority = 0

    for i in range(0, len(rucksacks), 3):
        group = set({ *rucksacks[i][0], *rucksacks[i][1] })

        for j in range(i + 1, i + 3):
            group.intersection_update({ *rucksacks[j][0], *rucksacks[j][1] })

        same = group.pop()

        if same.isupper():
            val = (ord(same) - 64) + 26
        else:
            val = ord(same) - 96
        
        priority += val
    
    return priority
        
        

if __name__ == '__main__':

    with open(os.path.expanduser("~/dev/aoc/pyaoc/inputs/day3.txt")) as f:
        puzzle = f.read()
    # puzzle = test_puzzle

    res = part2(puzzle)
    print(res)


