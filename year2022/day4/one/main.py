

class Section:

    def __init__(self, start: int, finish: int):
        self.start = start
        self.finish = finish
    
    def __contains__(self, other: "Section") -> bool:
        if other.start >= self.start and other.finish <= self.finish:
            return True
        return False
    
    def overlaps(self, other: "Section") -> bool:
        if self in other or other in self:
            return True
        
        if self.start <= other.start and self.finish >= other.start:
            return True
        elif self.start <= other.finish and self.finish >= other.finish:
            return True
        
        return False

def parse(input: str) -> list[tuple[Section, Section]]:
    res = []
    for line in input.strip().split("\n"):
        line = line.replace('-', ' ').replace(',', ' ').split(' ')
        nums = list(map(int, line))
        s1, s2 = Section(*nums[:2]), Section(*nums[2:])
        res.append((s1, s2))
    
    return res

def part1(input: str) -> int:
    sections = parse(input)
    count = 0

    for s in sections:
        s1, s2 = s

        if s2 in s1 or s1 in s2:
            count += 1
    
    return count

def part2(input: str) -> int:
    sections = parse(input)
    count = 0

    for s in sections:
        s1, s2 = s

        if s1.overlaps(s2):
            count += 1

    return count
    

test_puzzle = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

if __name__ == '__main__':
    import os
    with open(os.path.expanduser("~/dev/aoc/pyaoc/year2022/inputs/day4.txt")) as f:
        puzzle = f.read()
    # puzzle = test_puzzle

    res = part2(puzzle)
    print(res)