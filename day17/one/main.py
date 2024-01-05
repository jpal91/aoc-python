import sys
import os
import math
import curses
import heapq
from collections import deque

sys.path.append(os.path.expanduser('~/dev/aoc'))
from utils.grid import Grid, Cell

puzzle_test = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

def paint(screen, node, hl, moves, _moves = []):
    for y, x, cell in grid.enum():
        # if cell == node:
        #     screen.addstr(y, x, str(cell.value), curses.color_pair(1))
        # elif cell in _moves:
        #     screen.addstr(y, x, str(cell.value), curses.color_pair(2))
        # else:
            screen.addstr(y, x, str(cell.value))
    
    screen.addstr(13, 0, f'Heat Loss: {hl}')
    screen.addstr(14, 0, f'Moves: {moves}')
    screen.addstr(15, 0, str(_moves))
    hl = 0
    for cell in _moves:
        y, x = cell.coords
        if cell == node:
            screen.addstr(y, x, str(cell.value), curses.color_pair(1))
        else:
            screen.addstr(y, x, str(cell.value), curses.color_pair(2))
        hl += cell.value
        screen.addstr(13, 0, f'Heat Loss: {hl}')
        screen.refresh()
        screen.getch()
    screen.refresh()
    screen.getch()

def bfs(screen, cell: Cell, end: Cell) -> int:
    # queue = deque([(c, 1, 0, i) for i, c in enumerate(cell.neighbors) if c])
    queue = [(c.value, 0, c, i) for i, c in enumerate(cell.neighbors) if c and i == 1]
    heat_loss = math.inf
    visited = set()
    if screen:
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW)

    while queue:
        # node, moves, hl, direction = queue.popleft()
        hl, moves, node, direction = heapq.heappop(queue)
        

        if node == end:
            heat_loss = min(heat_loss, hl)
            if screen:
                paint(screen, node, hl, moves, )
            return hl
        
        if (node, moves) in visited:
            continue
        visited.add((node, moves))

        if moves == 3:
            left, right = (direction - 1) % 4, (direction + 1) % 4
            if (ln := node.neighbors[left]):
                heapq.heappush(queue, (hl + ln.value, 1, ln, left, ))
            if (rn := node.neighbors[right]):
                heapq.heappush(queue, (hl + rn.value, 1, rn, right, ))
            continue
        
        for i, n in enumerate(node.neighbors):
            if not n or i == (direction + 2) % 4:
                continue
            
            if i == direction:
                # queue.append((n, moves + 1, hl + n.value, i))
                heapq.heappush(queue, (hl + n.value, moves + 1, n, i, ))
            else:
                # queue.append((n, 1, hl + n.value, i))
                heapq.heappush(queue, (hl + n.value, 1, n, i, ))
        
        # if screen:
        #     paint(screen, node, hl, moves, visited)
        

    
    return heat_loss

        
def dfs(cell: Cell, moves: int, direction: int, hl: int, visited: dict, end: Cell) -> int:
    if cell in visited:
        return visited[cell]
    if cell == end:
        return hl + end.value

    # visited[cell] = hl + cell.value
    smallest_heat = math.inf
    for i, n in enumerate(cell.neighbors):
        if not n:
            continue
        if moves == 3 and i == direction:
            continue
        elif i == direction:
            smallest_heat = min(smallest_heat, dfs(n, moves + 1, i, hl, visited, end))
        else:
            smallest_heat = min(smallest_heat, dfs(n, 1, i, hl, visited, end))
    
    visited[cell] = smallest_heat
    return visited[cell]

if __name__ == '__main__':
    with open('day17/one/puzzle.txt') as f:
        puzzle = f.read()
    # puzzle = puzzle_test

    grid = Grid.from_str(puzzle, type_hint=int)
    first, last = grid[0][0], grid[grid.rows - 1][grid.cols - 1]
    
    viz = False
    if viz:
        res = curses.wrapper(bfs, first, last)
    else:
        res = bfs(None, first, last)
        # res = min([dfs(c, 1, i, c.value, {}, last) for i,c in enumerate(first.neighbors) if c])
    print(res)