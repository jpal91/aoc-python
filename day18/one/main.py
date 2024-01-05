import os
import sys
import re
from collections import deque

sys.path.append(os.path.expanduser('~/dev/aoc'))
from utils.grid import Grid, Cell

puzzle_test = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

REGEX = re.compile(r'(\w) (\d+) \(([#\w\d]+)\)')

class ColorCell(Cell):

    def __init__(self, color: str, dug: bool, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.color = color
        self.dug = dug
    
    

class ColorGrid(Grid):

    def fill_and_count(self) -> int:
        for cell in self:
            if cell.dug:
                start = cell
                break
        y, x = start.coords
        queue = deque([self[y + 1][x + 1]])

        while queue:
            node: ColorCell = queue.popleft()

            if node.dug:
                continue
            node.dug = True
            node.value = '#'
            self.dig_count += 1

            for n in node.act_neighbors:
                if n.dug:
                    continue
                queue.append(n)
        
        return self.dig_count


    @classmethod
    def from_dig_plan(cls, dig_plan: list[str]) -> "ColorGrid":
        grid_list: list[ColorCell] = []
        y, x = 0, 0
        max_y, max_x, min_y, min_x = 0, 0, 0, 0
        dig_count = 0

        for p in dig_plan:
            parsed = REGEX.match(p)
            direction, n, color = parsed.group(1), int(parsed.group(2)), parsed.group(3)

            match direction:
                case 'R':
                    grid_list.extend([ColorCell(color, True, '#', y=y, x=x + i) for i in range(1, n + 1)])
                    x += n
                    max_x = max(max_x, x)
                case 'D':
                    grid_list.extend([ColorCell(color, True, '#', y=y + i, x=x)for i in range(1, n + 1)])
                    y += n
                    max_y = max(max_y, y)
                case 'U':
                    grid_list.extend([ColorCell(color, True, '#', y=y - i, x=x) for i in range(1, n + 1)])
                    y -= n
                    min_y = min(min_y, y)
                case 'L':
                    grid_list.extend([ColorCell(color, True, '#', y=y, x=x - i) for i in range(1, n + 1)])
                    x -= n
                    min_x = min(min_x, x)
            
            dig_count += n

        grid = [[ColorCell(None, False, '.', y=r, x=c) for c in range(abs(max_x - min_x)  + 1)] for r in range(abs(max_y - min_y) + 1)]

        for g in grid_list:
            y, x = g.coords
            new_y, new_x = abs(min_y - y), abs(min_x - x)
            g.y, g.x = new_y, new_x
            grid[new_y][new_x] = g

        grid = cls(grid)
        grid.dig_count = dig_count

        return grid
        

if __name__ == '__main__':
    with open('day18/one/puzzle.txt') as f:
        puzzle = f.read().strip().split('\n')

    # puzzle = puzzle_test.strip().split('\n')

    grid = ColorGrid.from_dig_plan(puzzle)

    res = grid.fill_and_count()
    print(res)
    
    