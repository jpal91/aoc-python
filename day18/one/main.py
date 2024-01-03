import os
import sys

sys.path.append(os.path.expanduser('~/dev/aoc'))
from grid.grid import Grid, Cell

grid = Grid(size = 2)
grid.add_row()
grid.add_col()
# for cell in grid:
#     print(cell.coords)
print(grid[0][-1].neighbors)
# print(grid)