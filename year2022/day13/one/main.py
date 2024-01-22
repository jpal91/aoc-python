import sys
import os
from itertools import zip_longest

sys.path.append(os.path.expanduser('~/dev/aoc'))
from pyaoc.utils.input import get_input
from pyaoc.utils.timeit import timeit

def _part1(left: int | list, right: int | list):

    match (isinstance(left, int), isinstance(right, int)):
        case (False, True):
            return _part1(left, [right])
        case (True, False):
            return _part1([left], right)
        case (False, False):
            for l, r in zip_longest(left, right):
                if l is None:
                    return True
                if r is None:
                    return False
                if l == r:
                    continue
                return _part1(l, r)

        case (True, True):
            return left < right

@timeit
def part1(input: str) -> int:
    indices = []
    sums = 0

    for pair in input.split('\n\n'):
        tmp = []
        for line in pair.splitlines():
            l = eval(line)
            tmp.append(l)
        indices.append(tuple(tmp))
    
    for i, pair in enumerate(indices):
        left, right = pair
        if _part1(left, right):
            sums += i + 1
        
    return sums


test_puzzle = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

if __name__ == '__main__':
    puzzle = get_input(22, 13)
    # puzzle = test_puzzle

    res = part1(puzzle)
    print(res)