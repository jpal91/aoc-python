from collections import deque

PIPES = {
    # Pipe : (North, East, South, West)
    # Read as: Can enter cell from...
    '|': (True, False, True, False),
    '-': (False, True, False, True),
    'J': (False, True, True, False),
    'L': (False, False, True, True),
    'F': (True, False, False, True),
    '7': (True, True, False, False)
}
DELTAS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

GRID: list[list[str]] = None
MAX_ROWS: int = None
MAX_COLS: int = None

def valid_move(new_coords: tuple[int, int], idx: int) -> bool:
    """Checks based on the new coordinates, and the direction moved
    from (idx -> DELTA[index] - corresponds to direction moved NEWS),
    if the move is valid based on the pipe type of the new cell
    """
    new_r, new_c = new_coords
    pipe = GRID[new_r][new_c]

    if pipe in PIPES:
        return PIPES[pipe][idx]
    else:
        return False


def neighbors(coords: tuple[int, int]) -> int:
    """Gets adjacent cells and checks if they are valid to move to"""
    row, col = coords
    n_list = []

    for i, d in enumerate(DELTAS):
        dy, dx = d
        r, c = row + dy, col + dx
        
        if (
            r < 0 or r >= MAX_ROWS or
            c < 0 or c >= MAX_COLS or
            not valid_move((r, c), i)
        ):
            continue

        n_list.append((r, c))
    
    return n_list

def bfs(start: tuple[int, int]) -> tuple[int, int]:
    """Breadth First Search starting at Start Point in Grid"""
    max_steps = 0
    # (row, col, steps taken, cells visited)
    queue = deque([(*start, 0, set())])

    while queue:
        r, c, steps, visited = queue.popleft()

        if (r, c) in visited:
            continue

        visited.add((r, c))
        max_steps = max(max_steps, steps)

        for n in neighbors((r, c)):
            queue.append((*n, steps + 1, visited))
    
    return max_steps

puzzle_test1 = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...\
"""

puzzle_test2 = """\
.....
.S-7.
.|.|.
.L-J.
.....\
"""

if __name__ == '__main__':
    with open('day10/one/puzzle.txt') as f:
        puzzle = f.read()

    # puzzle = puzzle_test2
    GRID = [[*row] for row in puzzle.split('\n')]
    MAX_ROWS = len(GRID)
    MAX_COLS = len(GRID[0])

    for r in range(MAX_ROWS):
        for c in range(MAX_COLS):
            if GRID[r][c] == 'S':
                res = bfs((r, c))
                print(res)
    
