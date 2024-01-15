import sys
import os
from pprint import pprint

sys.path.append(os.path.expanduser('~/dev/aoc'))
from utils.grid import Grid, Cell

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
    class Row(list):
        def __init__(self, row: list[Cell], idx: int):
            super().__init__(row)
            self._hash = hash("".join([cell.value for cell in row] + [idx]))
        
        def __hash__(self):
            return self._hash

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_list = [MirrorGrid.Row(self[r], str(r)) for r in range(self.rows)]
        self.row_map = {}
    
    def diff_rows(self, rows_a: list[Row], rows_b: list[Row]) -> int:
        diffs = 0

        for r1, r2 in zip(rows_a, rows_b[::-1]):
            if (key := (hash(r1), hash(r2))) in self.row_map:
                diffs += self.row_map[key]
            else:
                self.row_map[key] = len([c1 for c1, c2 in zip(r1, r2) if c1 != c2])
                diffs += self.row_map[key]
        return diffs
    
    @classmethod
    def rotated(cls, grid: str) -> list[list[Cell]]:
        grid: MirrorGrid = MirrorGrid.from_str(grid)
        _grid = []
        for c in range(grid.cols - 1, -1, -1):
            node: Cell = grid[0][c]
            col = [node.copy()]

            while (bottom := node.neighbors[2]):
                node = bottom
                col.append(node.copy())
            
            _grid.append(col)
        
        return cls(_grid)

def mirror_rows(grid: MirrorGrid | list[list[Cell]]) -> bool:
    n = grid.rows if hasattr(grid, 'rows') else len(grid)
    for r in range(0, n - 1):
        if grid[r] != grid[r + 1]:
            continue

        t, b = r, r + 1
        valid = True

        while t - 1 >= 0 and b + 1 < n:
            t -= 1
            b += 1

            if grid[t] != grid[b]:
                valid = False
                break
        
        if valid:
            return True
    
    return False

def diff(r1: list[Cell], r2: list[Cell]) -> list[Cell]:
    if r1 == r2:
        return []
    return [c1 for c1, c2 in zip(r1, r2) if c1 != c2]
    
    
# def fix_smudge(grid: MirrorGrid | list[list[Cell]], vert:bool) -> int:
#     n = grid.rows if hasattr(grid, 'rows') else len(grid)
#     for r in range(0, n - 1):
#         g_diff = None
#         if grid[r] != grid[r + 1]:
#             g_diff = len(diff(grid[r], grid[r + 1]))
#             if not g_diff:
#                 continue
#         nt, nb = len(grid[:r + 1]), len(grid[r + 1:])
#         t, b = r, r + 1
#         valid = True
#         fixed = False

#         if (t == 0 or b == n - 1) and g_diff == 1:
#             fixed = True

#         while t - 1 >= 0 and b + 1 < n:
#             t -= 1
#             b += 1

#             if not (d := diff(grid[t], grid[b])):
#                 continue
#             elif len(d) == 1:
#                 # idx = grid[t].index(d[0])
#                 # grid[t][idx].value = '#' if grid[t][idx].value == '.' else '.'
#                 fixed = True
#             elif fixed and len(d) >= 1:
#                 valid = False
        
#         if valid and fixed:
#             return nb if vert else nt
    
#     return 0

def fix_smudge(grid: MirrorGrid | list[list[Cell]], vert:bool) -> int:
    
    for r in range(0, grid.rows - 1):
        
        nt, nb = len(grid[:r + 1]), len(grid[r + 1:])
        t, b = r, r + 1
        valid = True
        fixed = False

        while t >= 0 and b < grid.rows:
            gt, gb = grid.row_list[t:r + 1], grid.row_list[r + 1:b + 1]
            if grid.diff_rows(gt, gb) == 1:
                fixed = True
                break

            t -= 1
            b += 1

        
        if valid and fixed:
            return nb if vert else nt
    
    return 0

if __name__ == '__main__':
    with open('day13/one/puzzle.txt') as f:
        puzzle = f.read().split('\n\n')

    # puzzle = (puzzle_test1 + puzzle_test2).split('\n\n')
    # puzzle = puzzle_test1
    # grid: MirrorGrid = MirrorGrid.from_str(puzzle, cell=EqCell)

    total = 0
    # total += fix_smudge(grid.rotated(), True)
    for p in puzzle:
        grid: MirrorGrid = MirrorGrid.from_str(p, cell=EqCell)
        vert = 0
        if horz := fix_smudge(grid, False):
            total += (horz * 100)
        elif vert := fix_smudge(MirrorGrid.rotated(p), True):
            total += vert
        
        print(horz, vert)
    print(total)
    # print([Cell('#')] - [Cell('#'), Cell('.')])