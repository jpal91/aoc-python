import os
import sys
import copy
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

class ExpandingGrid(Grid):

    def get_next(self, node: Cell, direction: int) -> tuple[Cell, tuple[int, int]]:
        y, x = node.coords

        match direction:
            case 0:
                return self[-1][x], (-self.rows, 0)
            case 1:
                return self[y][0], (0, self.cols)
            case 2:
                return self[0][x], (self.rows, 0)
            case 3:
                return self[y][-1], (0, -self.cols)


def bfs(node: Cell):
    queue = deque([(node, 0, (0, 0))])
    plots = set()
    visited = set()

    while queue:
        node, steps, offset = queue.popleft()

        if (node, steps, offset) in visited or steps >= max_steps:
            if steps == max_steps:
                node.value = 'O'
                plots.add((node, offset))
            continue
        visited.add((node, steps, offset))

        for i, n in enumerate(node.neighbors):
            if (n and n.value == '#') or n in visited:
                continue
            
            if n is None:
                next_node, os = grid.get_next(node, i)
                queue.append((next_node, steps + 1, (offset[0] + os[0], offset[1] + os[1])))
            else:
                queue.append((n, steps + 1, offset))
    
    return plots

if __name__ == '__main__':
    with open('day21/one/puzzle.txt') as f:
        puzzle = f.read()
    
    puzzle = puzzle_test

    grid: ExpandingGrid = ExpandingGrid.from_str(puzzle)
    max_steps = 5000

    for cell in grid:
        if cell.value == 'S':
            res = bfs(cell)
            break

    print(len(res))
    # print(grid)