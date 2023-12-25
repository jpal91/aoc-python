import re
from functools import lru_cache

puzzle_test1 = """\
RLR

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)\
"""

puzzle_test2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)\
"""

class LeftRightLoop(list[str]):

    def __init__(self, lr: list[str]):
        super().__init__(lr)
        self.current = 0
        self.n = len(self)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        value = self[self.current]
        self.current = (self.current + 1) % self.n
        return value

if __name__ == '__main__':
    with open('day8/one/puzzle.txt') as f:
        puzzle = f.read()
    
    puzzle = re.match(r'(.*)\n\n(.*)', puzzle, re.DOTALL)
    
    LR = LeftRightLoop([0 if item == 'L' else 1 for item in puzzle.group(1)])
    NODE_MAP = {
        k : v.split(', ') for k,v in
        re.findall(r'(\w\w\w) = \((\w\w\w, \w\w\w)\)\n', puzzle.group(2))
    }

    next_node = 'AAA'
    count = 0
    
    for lr in LR:
        next_node = NODE_MAP[next_node][lr]
        count += 1

        if next_node == 'ZZZ':
            break
    
    print(count)
