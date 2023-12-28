import sys
import os
from pprint import pprint

sys.path.append(os.path.expanduser('~/dev/aoc'))
from grid.grid import Grid, Cell

puzzle_test1 = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
"""

puzzle_test2 = """
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

class EqCell(Cell):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __eq__(self, other):
        return self.value == other.value

class MirrorGrid(Grid):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def rotated(self) -> list[list[Cell]]:
        grid = []
        for c in range(self.cols - 1, -1, -1):
            node = self[0][c]
            col = [node]

            while (bottom := node.neighbors[2]):
                node = bottom
                col.append(node)
            
            grid.append(col)
        
        return grid

def split_and_flip(grid: MirrorGrid, idx: int) -> list[list[Cell]]:
    top, bottom = grid[:idx], grid[idx:]
    return top, bottom

def mirror_rows(grid: MirrorGrid, vert:bool) -> int:
    n = grid.rows if hasattr(grid, 'rows') else len(grid)
    for r in range(0, n - 1):
        if grid[r] != grid[r + 1]:
            continue
        nt, nb = len(grid[:r + 1]), len(grid[r + 1:])
        t, b = r, r + 1
        valid = True

        while t - 1 >= 0 and b + 1 < n:
            t -= 1
            b += 1

            if grid[t] != grid[b]:
                valid = False
                break
        
        if valid:
            return nb if vert else nt
    
    return 0
    
    # top, bottom = grid[:4], grid[3:]
    # [print(t) for t in top]
    # print('')
    # [print(b) for b in bottom]


if __name__ == '__main__':
    with open('day13/one/puzzle.txt') as f:
        puzzle = f.read().split('\n\n')

    # puzzle = (puzzle_test1 + puzzle_test2).split('\n\n')

    total = 0
    for p in puzzle:
        grid: MirrorGrid = MirrorGrid.from_str(p, cell=EqCell)
        vert = 0
        if horz := mirror_rows(grid, False):
            total += (horz * 100)
        elif vert := mirror_rows(grid.rotated(), True):
            total += vert
        
        # print(grid[0], horz, vert)
    print(total)