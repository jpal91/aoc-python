import os
import sys
from collections import deque

sys.path.append(os.path.expanduser('~/dev/aoc'))
from utils.grid import Grid, Cell

puzzle_test = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

def bfs(node: Cell):
    queue = deque([(node, 0)])
    plots = set()
    visited = set()

    while queue:
        node, steps = queue.popleft()

        if (node, steps) in visited or steps >= max_steps:
            if steps == max_steps:
                node.value = 'O'
                plots.add(node)
            continue
        visited.add((node, steps))

        for n in node.act_neighbors:
            if n.value == '#' or n in visited:
                continue
            queue.append((n, steps + 1))
    
    return plots

if __name__ == '__main__':
    with open('day21/one/puzzle.txt') as f:
        puzzle = f.read()
    
    # puzzle = puzzle_test

    grid = Grid.from_str(puzzle)
    max_steps = 64

    for cell in grid:
        if cell.value == 'S':
            res = bfs(cell)
            break

    print(len(res))
    # print(grid)