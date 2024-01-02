import sys
import os
from collections import deque

sys.path.append(os.path.expanduser('~/dev/aoc'))
from grid.grid import Grid, Cell

puzzle_test = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

class Mirror(Cell):

    def __init__(self, mirror: str, *args, **kwargs) -> None:
        super().__init__(mirror, *args, **kwargs)
        self.shift = [1, 0, 3, 2] if mirror == '/' else [3, 2, 1, 0]
        self.energized = False

    def get_next(self, direction: int) -> list[int]:
        idx = self.shift[direction]
        return [(self.neighbors[idx], idx)]

class Splitter(Cell):

    def __init__(self, splitter: str, *args, **kwargs) -> None:
        super().__init__(splitter, *args, **kwargs)
        self.ends = [0, 2] if splitter == '|' else [1, 3]
        self.energized = False
    
    def get_next(self, direction: int) -> list[int]:
        if direction in self.ends:
            return [(self.neighbors[direction], direction)]
        else:
            return [(self.neighbors[idx], idx) for idx in self.ends]

def fill_grid(grid: Grid) -> int:
    queue = deque([(grid[0][0], 1)])
    energized = 0
    visited = set()

    while queue:
        n = queue.popleft()
        
        if not n[0] or n in visited:
            continue

        visited.add(n)

        cell, direction = n

        if cell.coords == (7, 4):
            pass

        if not cell.energized:
            cell.energized = True
            energized += 1

        if type(cell) == Cell:
            queue.append((cell.neighbors[direction], direction))
            continue

        for c in cell.get_next(direction):           
            queue.append(c)

    return energized

if __name__ == '__main__':

    with open('day16/one/puzzle.txt') as f:
        puzzle = [[*p] for p in f.read().strip().split('\n')]

    # puzzle = [[*p] for p in puzzle_test.strip().split('\n')]
    for r in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if (cell := puzzle[r][x]) == '.':
                new_cell = Cell('.', r, x)
                setattr(new_cell, 'energized', False)
                puzzle[r][x] = new_cell
            elif cell in ['/', '\\']:
                puzzle[r][x] = Mirror(cell, r, x)
            else:
                puzzle[r][x] = Splitter(cell, r, x)
    
    grid = Grid(puzzle)
    # print(grid[6][4].get_next(0))
    res = fill_grid(grid)
    
    print(res)