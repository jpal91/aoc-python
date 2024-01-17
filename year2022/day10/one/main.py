
from collections import deque
from enum import Enum
from typing import Any, Optional

class Instructions(Enum):
    ADDX = 1
    NOOP = 0

def parse(input: str) -> deque[tuple[Instructions, Optional[int]]]:
    queue = deque()

    for line in input.strip().splitlines():
        insts = line.split(' ')
        inst = Instructions.ADDX if insts[0] == 'addx' else Instructions.NOOP
        val = int(insts[1]) if len(insts) > 1 else 0

        queue.append((inst, val))
    
    return queue

def part1(input: str) -> int:
    queue = parse(input)
    signals = deque([0])
    cycle, x, wait_until = 1, 1, 1
    sig_strength = 0

    
    while queue:
        
        if cycle < wait_until:
            
            if cycle in [20, 60, 100, 140, 180, 220]:
                sig_strength += (cycle * x)

            cycle += 1
            continue
        
        x += signals.pop()
        inst, val = queue.popleft()

        if cycle in [20, 60, 100, 140, 180, 220]:
            sig_strength += (cycle * x)

        
        if inst == Instructions.ADDX:
            
            wait_until = cycle + 2
        else:
            wait_until = cycle

        signals.appendleft(val)
        cycle += 1        


    return sig_strength

def part2(input: str) -> int:
    queue = parse(input)
    signals = deque([0])
    cycle, x, wait_until = 1, 1, 1

    crt = [['.' for _ in range(40)] for _ in range(6)]
    r, c = 0, 0
    
    while queue:
        
        if cycle >= wait_until:
            x += signals.pop()
            inst, val = queue.popleft()
            
            if inst == Instructions.ADDX:
                
                wait_until = cycle + 2
            else:
                wait_until = cycle

            signals.appendleft(val)
             

        if (
            c == x or
            c == x - 1 or
            c == x + 1
        ):
            crt[r][c] = '#'
        
        c += 1

        if c >= 40:
            r += 1
            c = 0
        
        if r == 6:
            break
        
        cycle += 1
    
    return crt

test_puzzle = """\
noop
addx 3
addx -5
"""

test_puzzle2 = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

if __name__ == '__main__':
    with open('pyaoc/year2022/inputs/day10.txt') as f:
        puzzle = f.read()
    puzzle = test_puzzle2

    # res = part1(puzzle)
    
    res = part2(puzzle)
    [print("".join(r)) for r in res]
