from collections import deque
from dataclasses import dataclass

from grid import Grid, Cell

PIPES = {
    # Pipe : (North, East, South, West)
    # Read as: Can enter cell from...
    "|": (True, False, True, False),
    "-": (False, True, False, True),
    "J": (False, True, True, False),
    "L": (False, False, True, True),
    "F": (True, False, False, True),
    "7": (True, True, False, False),
    "S": (True, True, True, True)
}

@dataclass
class Border:
    cell_a: Cell
    cell_b: Cell
    active: bool = True
    is_exit: bool = False

    @property
    def vertical(self) -> bool:
        return self.cell_a.y == self.cell_b.y
    
    def adj_borders(self) -> list[tuple[int, int]]:
        cells = [self.cell_a, self.cell_b]

        if self.vertical:
            res = [
                (cells[0].neighbors[0], cells[1].neighbors[0]),
                (cells[1], cells[1].neighbors[0]),
                (cells[0], cells[0].neighbors[0]),
                (cells[0].neighbors[2], cells[1].neighbors[2]),
                (cells[1], cells[1].neighbors[2]),
                (cells[0], cells[0].neighbors[2])
            ]
        else:
            res = [
                (cells[0], cells[0].neighbors[1]),
                (cells[0].neighbors[1], cells[1].neighbors[1]),
                (cells[1], cells[1].neighbors[1]),
                (cells[1], cells[1].neighbors[3]),
                (cells[1].neighbors[3], cells[0].neighbors[3]),
                (cells[0], cells[0].neighbors[3])
            ]
        
        return res

class Main(Cell):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.escaped = False
        self.main_loop = False

class Pipe(Main):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def can_enter(self, idx: int) -> bool:
        return PIPES[self.value][idx]
    
    def can_exit(self, idx: int) -> bool:
        if self.value in ['S', '-', '|']:
            return self.can_enter(idx)
        return not PIPES[self.value][idx]

class PuzzleGrid(Grid):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.borders: dict[tuple[Cell, Cell], Border] = {}
        self.add_borders()
    
    def add_borders(self) -> None:
        for y, x, cell in self.enum():
            for n in cell.act_neighbors:
                is_exit = (
                    (y == 0 and n.y == 0) or (y == self.rows - 1 and n.y == self.rows - 1) or
                    (x == 0 and n.x == 0) or (x == self.cols - 1 and n.x == self.cols - 1)
                )
                border = Border(cell, n, is_exit=is_exit)
                if (a := (cell, n)) not in self.borders:
                    self.borders[a] = border
                if (b := (n, cell)) not in self.borders:
                    self.borders[b] = border
    
    def get_border(self, cell_a: Cell | tuple[int, int], cell_b: Cell | tuple[int, int]) -> Border | None:
        if isinstance(cell_a, tuple) and cell_a in self:
            y, x = cell_a
            cell_a = self[y][x]
        if isinstance(cell_b, tuple) and cell_b in self:
            y, x = cell_b
            cell_b = self[y][x] 
        
        if (a := (cell_a, cell_b)) in self.borders:
            return self.borders[a]
        if (b := (cell_b, cell_a)) in self.borders:
            return self.borders[b]
        
        return None
    
    def remove_border(self, cell_a: Cell, cell_b: Cell) -> None:
        if border := self.get_border(cell_a, cell_b):
            border.active = False
            pass
    
    def get_adj_borders(self, border: Border) -> bool:
        borders = []

        for a, b in border.adj_borders():
            if valid := self.get_border(a, b):
                borders.append(valid)
        
        return borders



GRID: PuzzleGrid = None

puzzle_test1 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

puzzle_test2 = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

puzzle_test3 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

def fill_grid(cell: Cell):
    queue = deque([(cell, -1, None)])
    visited = set()

    while queue:
        cell, direction, last = queue.popleft()

        if not isinstance(cell, Pipe):
            continue
        if direction != -1 and not cell.can_enter(direction):
            continue
        
        if last:
            GRID.remove_border(cell, last)
        if cell in visited:
            continue
        
        visited.add(cell)
        cell.main_loop = True

        for i, n in enumerate(cell.neighbors):
            if not n or not isinstance(n, Pipe) or not cell.can_exit(i) or n in visited:
                continue
            queue.append((n, i, cell))

def can_escape(border: Border) -> tuple[bool, set]:
    queue = deque([border])
    visited = set()

    while queue:
        border = queue.popleft()

        if border.is_exit and border.active:
            return True, visited
        if not border.active or id(border) in visited:
            continue
        
        visited.add(id(border))

        for b in GRID.get_adj_borders(border):
            queue.append(b)
    
    return False, visited

def main():
    for cell in GRID:
        if cell.value == 'S':
            fill_grid(cell)
            break
    
    trapped = 0
    safe_set, trap_set = set(), set()

    for cell in GRID:
        if cell.main_loop:
            continue

        n = cell.act_neighbors[0]
        border = GRID.get_border(cell, n)
        
        if id(border) in safe_set:
            continue
        elif id(border) in trap_set:
            trapped += 1
            continue
        
        escaped, ss = can_escape(border)
        if escaped:
            safe_set.update(ss)
        else:
            trapped += 1
            trap_set.update(ss)
    
    print(trapped)

if __name__ == "__main__":
    with open("day10/one/puzzle.txt") as f:
        puzzle = f.read()

    # puzzle = puzzle_test3
    pipe_types = PIPES.keys()
    GRID = PuzzleGrid([
        [
            Main(col, y=y, x=x) if (col not in pipe_types and col != 'S') else Pipe(col, y=y, x=x)
            for x, col in enumerate(row)
        ]
        for y, row in enumerate(puzzle.strip().split("\n"))
    ])
    main()