import re
from collections import defaultdict

def parse_stacks(input: str):
    input = input.split('\n')
    index_to_stack = {}

    for i, ch in enumerate(input.pop()):
        if ch.isnumeric():
            index_to_stack[i] = int(ch)
    
    stack_map = defaultdict(list)

    for line in reversed(input):
        for i, l in enumerate(line):
            if l.isalpha():
                stack = index_to_stack[i]
                stack_map[stack].append(l)
    
    return stack_map

def parse_instructs(input: str):
    input = input.strip().split('\n')
    regex = re.compile(r'move (\d+) from (\d+) to (\d+)')
    inst = []

    for line in input:
        matches = regex.match(line)
        inst.append((int(matches.group(1)), int(matches.group(2)), int(matches.group(3))))
    
    return inst


def parse(input: str):
    input = input.split('\n\n')
    stacks = parse_stacks(input[0])
    inst = parse_instructs(input[1])

    return stacks, inst

def solve(input: str, part1: bool):
    stacks, instructions = parse(input)

    for (count, start, to) in instructions:
        tmp = []

        while count > 0:
            tmp.append(stacks[start].pop())
            count -= 1
        
        if part1:
            stacks[to].extend(tmp)
        else:
            stacks[to].extend(tmp[::-1])
    
    res = ""

    for s in stacks.values():
        res += s[-1]
    
    return res


test_puzzle = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

if __name__ == '__main__':
    import os
    with open(os.path.expanduser("~/dev/aoc/pyaoc/year2022/inputs/day5.txt")) as f:
        puzzle = f.read()
    # puzzle = test_puzzle

    res = solve(puzzle, False)
    print(res)