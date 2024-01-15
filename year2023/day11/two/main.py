import os
import sys
from itertools import combinations

sys.path.append(os.path.expanduser('~/dev/aoc'))
from utils.grid import Grid

puzzle_test1 = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

MULT: int = None

def get_distances(combos: list[tuple[int, int], tuple[int, int]]) -> list[tuple[int, int], tuple[int, int], int]:
    combos_w_dist = []
    for g1, g2 in combos:
        y1, x1, y2, x2 = *g1, *g2
        dist = abs(y2 - y1) + abs(x2 - x1)
        combos_w_dist.append((g1, g2, dist))
    
    return combos_w_dist

def expand_universe(galaxies: list[tuple[int, int]], xr: list[int], xc: list[int]) -> list[tuple[int, int]]:
    new_galaxies = []
    
    for g in galaxies:
        xpanded_r, xpanded_c = iter(xr), iter(xc)
        nr, nc = next(xpanded_r), next(xpanded_c)
        y, x = g
        ny, nx = y, x

        while (nr and y > nr) or (nc and x > nc):
            if nr and y > nr:
                ny += MULT - 1
                try:
                    nr = next(xpanded_r)
                except:
                    nr = None
            
            if nc and x > nc:
                nx += MULT - 1
                try:
                    nc = next(xpanded_c)
                except:
                    nc = None
        
        new_galaxies.append((ny, nx))
    
    return new_galaxies


def get_expanded_rc(grid: Grid) -> tuple[list[int], list[int]]:
    rows = []
    for r in range(grid.rows):
        node = grid[r][0]
        valid = node.value != '#'

        while node.neighbors[1]:
            node = node.neighbors[1]
            if node.value == '#':
                valid = False
                break
        
        if valid:
            rows.append(r)
    
    cols = []
    for c in range(grid.cols):
        node = grid[0][c]
        valid = node.value != '#'

        while node.neighbors[2]:
            node = node.neighbors[2]
            if node.value == '#':
                valid = False
                break
        
        if valid:
            cols.append(c)
    
    return rows, cols

def get_galaxies(grid: Grid) -> list[tuple[int, int]]:
    galaxies = []
    for cell in grid:
        if cell.value == '#':
            galaxies.append(cell.coords)
    return galaxies

def main(puzzle: str) -> int:
    grid = Grid.from_str(puzzle)
    galaxies = get_galaxies(grid)
    xr, xc = get_expanded_rc(grid)
    
    xp_galaxies = expand_universe(galaxies, xr, xc)
    combos = combinations(xp_galaxies, 2)
    combos_w_dist = get_distances(combos)
    
    print(sum([pair[2] for pair in combos_w_dist]))

if __name__ == '__main__':
    with open('day11/one/puzzle.txt') as f:
        puzzle = f.read()
    # puzzle = puzzle_test1
    MULT = 1000000

    main(puzzle)