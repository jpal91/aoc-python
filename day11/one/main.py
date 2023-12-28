import sys
import os
import math
import curses
import time
from typing import Any
from collections import deque
from pprint import pprint


sys.path.append(os.path.expanduser('~/dev/aoc'))
from grid.grid import Grid, Cell

class Galaxies(dict):

    def __init__(self) -> None:
        super().__init__()
    
    def __getitem__(self, __key: tuple[tuple[int, int], tuple[int, int]]) -> Any:
        try:
            item = super().__getitem__(__key)
        except:
            pass
        else:
            return item

        try:
            item = super().__getitem__(__key[::-1])
        except:
            pass
        else:
            return item
        
        self[__key] = math.inf
        return self[__key]
    
    def __setitem__(self, __key: Any, __value: Any) -> None:
        if __key in self:
            return super().__setitem__(__key, __value)
        elif __key[::-1] in self:
            return super().__setitem__(__key[::-1], __value)
        return super().__setitem__(__key, __value)
    
    @property
    def maximum(self) -> int:
        if not self.keys():
            return math.inf
        return max([val for val in self.values()])
    
    def get_galaxy(self, galaxy: tuple[int, int]) -> list[tuple[tuple[int, int], tuple[int, int], int]]:
        return [(*k, v) for k, v in self.items() if galaxy in k]
    
    def get_galaxies(self) -> list[tuple[tuple[int, int], tuple[int, int], int]]:
        return [(*k, v) for k, v in self.items()]



class ExpandingUniverse(Grid):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.galaxies = Galaxies()
        self.get_galaxies = self.galaxies.get_galaxies
        self.visualize = None
        self.screen = None
    
    def find_shortest(self) -> list[tuple[tuple[int, int], tuple[int, int], int]]:
        links = []
        # self.screen = curses.initscr()
        # curses.start_color()
        # curses.noecho()
        # curses.cbreak()
        # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        # curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        # curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
        try:
                    
            for cell in self:
                if cell.value == '#':
                    self._find_shortest(cell)

                    # self.__find_shortest(cell, set(), 0, cell)
                    # self._find_shortest(cell)
                    # break
        finally:
            # curses.echo()
            # curses.nocbreak()
            # curses.endwin()
            pass
        
        return links
    
    def paint(self, coords, steps, last):
        offset = 1
        for y, x, cell in self.enum():
            if y == 0:
                offset = 1
            if cell.coords in last:
                self.screen.addstr(y, x + 1, cell.value, curses.color_pair(3))
            elif cell.visited:
                self.screen.addstr(y, x + 1, cell.value, curses.color_pair(2))
            else:
                self.screen.addstr(y, x + 1, cell.value, curses.color_pair(1))
            offset += 1
            self.screen.refresh()
        
        self.screen.addstr(12, 0, str(steps))
        self.screen.addstr(13, 0, str(coords))
        self.screen.addstr(14, 0, str(last))
        self.screen.refresh()
        self.screen.getch()
        
        # time.sleep(0.1)

    
    def _find_shortest(self, cell: Cell) -> list[tuple[tuple[int, int], tuple[int, int], int]]:
        queue = deque([(cell, 0)])
        root = cell.coords
        visited = set()
        maximum = self.galaxies.maximum
        
        while queue:
            node, steps = queue.popleft()

            if node.value == '#' and node.coords != root:
                # current = self.galaxies[(root, node.coords)]
                # if len(path) > current:
                #     continue
                self.galaxies[(root, node.coords)] = min(self.galaxies[(root, node.coords)], steps)
            
            if node in visited:
                continue

            visited.add(node)
            node.visited = True
            

            for n in node.act_neighbors:
                if n in visited:
                    continue
                # queue.append((n, steps + 1, visited))
                queue.append((n, steps + 1))
            
            # self.paint(node.coords, steps, path)

            # if node.coords == (10, 10):
            #     self.screen.addstr(12, 0, str(steps))
            #     self.screen.refresh()
            #     self.screen.getch()
            
            
        
        return self.galaxies.get_galaxy(root)
    
    def __find_shortest(self, node: Cell, visited: set, steps: int, root: Cell) -> None:
        if node.value == '#' and node != root:
            self.galaxies[(root.coords, node.coords)] = min(self.galaxies[(root.coords, node.coords)], steps)
            return
        # if node in visited:
        #     return
        
        visited.add(node)

        for n in node.act_neighbors:
            if n in visited:
                continue
            self.__find_shortest(n, visited, steps + 1, root)
        
        return

    
    def get_visual(self) -> str:
        for v in self.visualize:
            y, x = v.coords
            self[y][x].value = 'X'
        
        return str(self)
    
    @classmethod
    def from_str(cls, _grid: str, type_hint: Any = str) -> "ExpandingUniverse":
        grid: list[list[str]] = [list(map(type_hint, [*col])) for col in _grid.strip().split("\n")]
        rows, cols = len(grid), len(grid[0])
        trows = rows
        tmp_grid = grid[::]
        
        add_row_after = []
        for r in range(rows):
            idx = 0

            while idx < cols and (node := grid[r][idx]) != '#':
                idx += 1
            
            if node != '#':
                add_row_after.append(r)
        
        for i, a in enumerate(add_row_after):
            tmp_grid.insert(a + i, ['.'] * cols)
            trows += 1
        
        add_col_after = []
        for c in range(cols):
            r = 0
            valid = True

            while r < rows:
                if grid[r][c] == '#':
                    valid = False
                    break
                r += 1
            
            if valid:
                add_col_after.append(c)
        # print(add_col_after)
        for i, a in enumerate(add_col_after):
            for r in range(trows):
                tmp_grid[r].insert(a + i, '.')
        
        return cls(tmp_grid)

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
        
if __name__ == '__main__':

    with open('day11/one/puzzle.txt') as f:
        puzzle = f.read()
    # puzzle = puzzle_test1

    grid = ExpandingUniverse.from_str(puzzle)

    grid.find_shortest()
    shortest = grid.get_galaxies()
    # viz = grid.get_visual()
    # print(viz)
    
    # print(len(shortest[7]))
    # print(sum([sum([s[2] for s in g]) for g in shortest]))
    # pprint(shortest)
    print(sum([s[2] for s in shortest]))
    # print(grid.rows, grid.cols)
    # print(grid)
