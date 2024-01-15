from collections import deque
from enum import Enum
import curses
import time
import heapq

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
        self.color = 0
        self.longest = 0

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
def bfs(start: TrailCell, cur_steps: int, visited: set, screen=None) -> int:
    queue = deque([(start, cur_steps, [])])
    # queue = [(0, start, [])]
    ends = []
    longest = 0
    vis = set()

    if screen:
        for y in range(59):
            for x in range(min(250, grid.cols)):
                screen.addstr(y, x, grid[y][x].value)
        screen.refresh()

    while queue:
        node, steps, path = queue.popleft()
        # steps, node, path = heapq.heappop(queue)

        if node.value in ['<', 'v', '>', 'X'] and node != start:
            # longest = max(longest, steps)
            # visited.add(node)
            ends.append((node, steps))
            continue

        if node.coords in path:
            continue
        vis.add(node.coords)

        for n in node.neighbors:
            if not n or n.value == '#' or n.coords in path or n in visited:
                continue
            # if n.value in ['<', 'v', '>', 'X'] and n != start:
            # # longest = max(longest, steps)
            #     visited.add(n)
            #     ends.add((n, steps + 1))
            #     continue

            queue.append((n, steps + 1, [*path, node.coords]))
        
        if screen:
            y, x = node.coords
            if y >= 58 or x >= 250:
                continue
            if (y,x) in vis:
                node.color += 1
            screen.addstr(*node.coords, node.value, curses.color_pair(node.color % 5 or 5))
            screen.addstr(59, 0, f'{node.coords}')
            screen.refresh()
    
    return list(ends)

def bfs_sections(start: TrailCell, end: TrailCell) -> int:
    queue = deque([(start, 0)])
    longest = 0
    count = 0
    visited = set()
    # print(grid.rows, grid.cols)
    graph = {}
    
    while queue:
        next_start, cur_steps = queue.popleft()
        
        if next_start == end:
            longest = max(longest, cur_steps)
            continue
        print(next_start.coords)
        ends = bfs(next_start, 0, visited)
        # visited.add(next_start)
        print(ends)
        # queue.extend(ends)
        if ends:
            queue.extend(ends)
            graph[next_start] = ends
        # count += 1
        # if count >3: break
    
    # print(longest)
    return dfs(start, 0, graph, end)

def dfs(node: TrailCell, steps, graph, last):
    if not node or node not in graph:
        return 0
    if node == last:
        return steps
    
    longest = steps
    for n, s in graph[node]:
        if res := dfs(n, steps + s, graph, last):
            longest = max(longest, res)
    
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
    # screen.getch()
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
    # puzzle = get_input(23)
    grid = Grid.from_str(puzzle, cell=TrailCell)

    for cell in grid.first_row:
        if cell.value == '.':
            first = cell
            break
    
    for cell in grid.last_row:
        if cell.value == '.':
            cell.value = 'X'
            last = cell
            break
    
    total = sum([cell.value == '.' for cell in grid])
    
    # run_grid(first, total)
    # res = bfs(first, last)
    res = bfs_sections(first, last)
    print(res)