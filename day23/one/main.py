from collections import deque
from enum import Enum
import curses
import time

from utils.grid import Grid, Cell, viz #viz_grid
from utils.input import get_input

puzzle_test = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

class TrailCell(Cell):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = None

        if (idx := ">v<".find(self.value)) != -1:
            self.slope = idx + 1
        else:
            self.slope = None
    
    @property
    def act_neighbors(self) -> list["TrailCell"]:
        if self.slope:
            return [self._neighbors[self.slope]]
        return super().act_neighbors
        

# @viz
def bfs(start: TrailCell, end: TrailCell, screen=None) -> int:
    queue = deque([(start, 0, [])])
    visited = set()
    longest = 0

    while queue:
        node, steps, moves = queue.popleft()

        if node == end:
            longest = max(longest, steps)
            continue

        # if (node, steps) in visited:
        #     continue
        # visited.add(node)
        if node.coords in moves:
            continue
        

        for n in node.act_neighbors:
            if n in moves or n.value == '#':
                continue
            queue.append((n, steps + 1, [*moves, node.coords]))
        
        if screen:
            viz_grid(screen, node, grid)
    
    return longest

def viz_grid(screen, maxyx, coords):
    min_y, min_x, max_y, max_x = maxyx
    screen.addstr(59, 0, f'{max_y, max_x, min_y, min_x, coords}')
    # for y, x, cell in grid.enum():
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            try:
                cell = grid[y][x]
            except:
                screen.addstr(59, 0, f'{y, x}')
            # if y >= max_y or x >= max_x or y <= min_y or x <= min_x:
            #     continue
            if cell.color:
                screen.addstr(y, x, cell.value, curses.color_pair(cell.color % 5 or 5))
            else:
                screen.addstr(y, x, cell.value)
    
    screen.refresh()
    screen.getch()
    # time.sleep(0.2)

@viz
def run_grid(start: TrailCell, total: int, screen = None):
    
    queue = deque([(start, 1)])
    visited = set()
    colors = 1

    if screen:
        sy,sx = screen.getmaxyx()
        y_offset, x_offset = sy // 2 - 1, sx // 2 - 1

    while queue:
        node, color = queue.popleft()

        node.color = color
        colors = max(colors, color)
        visited.add(node.coords)

        for n in node.act_neighbors:
            if n.value == '#' or n.color:
                continue
            if n.slope:
                queue.append((n, color + 1))
            else:
                queue.append((n, color))
        
    if screen:
        y, x = node.coords
        min_y, min_x = max(y - y_offset, 0), max(x - x_offset, 0)
        max_y, max_x = min(y + y_offset, sy - 2, grid.rows), min(x + x_offset, sx - 1, grid.cols)
        viz_grid(screen, (min_y, min_x, max_y, max_x), (y, x))
    
    print(colors, len(visited), total)
    return None


if __name__ == '__main__':
    
    puzzle = puzzle_test
    puzzle = get_input(23)
    grid = Grid.from_str(puzzle, cell=TrailCell)

    for cell in grid.first_row:
        if cell.value == '.':
            first = cell
            break
    
    for cell in grid.last_row:
        if cell.value == '.':
            last = cell
            break
    
    total = sum([cell.value == '.' for cell in grid])
    
    run_grid(first, total)
    # res = bfs(first, last)
    # print(res)