import os
import sys
import math
import heapq
from collections import deque

sys.path.append(os.path.expanduser('~/dev/aoc'))
from pyaoc.utils.grid import Grid, Cell
from pyaoc.utils.timeit import timeit

class StepCell(Cell):

    def __init__(self, value, *args, **kwargs):
        super().__init__(ord(value), *args, **kwargs)
    
@timeit
def part1(start: Cell, end: Cell) -> int:
    queue: deque[tuple[Cell, int, list]] = deque([ (start, 0) ])
    shortest = math.inf
    visited = set()

    while queue:
        node, steps = queue.popleft()

        if node.coords == end.coords:
            shortest = min(shortest, steps)
            continue

        if node.coords in visited or steps > shortest:
            continue

        # path.append(node.coords)
        visited.add(node.coords)

        for n in node.act_neighbors:
            if n.value > node.value + 1 or n.coords in visited:
                continue

            queue.append((n, steps + 1))

    return shortest

@timeit
def part2(start: Cell):
    queue: deque[tuple[Cell, int]] = deque([ (start, 0) ])
    visited = set()
    shortest = math.inf

    while queue:
        node, steps = queue.popleft()

        if node.value == ord('a'):
            shortest = min(shortest, steps)
            continue
        
        if node.coords in visited or steps > shortest:
            continue

        visited.add(node.coords)

        for n in node.act_neighbors:
            if n.value < node.value - 1 or n in visited:
                continue

            queue.append((n, steps + 1))
    
    return shortest


test_puzzle = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

if __name__ == '__main__':
    with open('pyaoc/year2022/inputs/day12.txt') as f:
        puzzle = f.read()
    # puzzle = test_puzzle
    grid = Grid.from_str(puzzle, cell=StepCell)

    for y, x, cell in grid.enum():
        if cell.value == ord('S'):
            cell.value = ord('a')
            start = cell
        if cell.value == ord('E'):
            cell.value = ord('z')
            end = cell

    res = part1(start, end)
    print(res)

    res = part2(end)
    print(res)