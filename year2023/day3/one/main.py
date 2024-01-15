from collections import deque, defaultdict

class Grid(list[str]):

    def __init__(self, puzzle: str) -> None:
        super().__init__(puzzle.split('\n'))
        if not self[-1]:
            self.pop()
        self.rows = len(self)
        self.cols = len(self[0])

grid: Grid = None
memo = set()
num_map = defaultdict(str)

DELTAS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

def neighbors(coords: tuple[int, int], horz: bool) -> list[tuple[int, int]]:
    row, col = coords
    new_coords = []

    for d in DELTAS:
        dy, dx = d
        new_r, new_c = row + dy, col + dx

        if horz and new_r != row:
            continue

        if (
            new_r < 0 or new_r >= grid.rows or
            new_c < 0 or new_c >= grid.cols
        ):
            continue

        new_coords.append((new_r, new_c))
    
    return new_coords

def bfs(coords: tuple[int, int]):
    row, col = coords
    queue = deque([(row, col)])

    while queue:
        r, c = queue.popleft()

        if (r, c) in memo:
            continue
        else:
            memo.add((r, c))
        
        if numeric := grid[r][c].isnumeric():
            num_map[(r, c)] = grid[r][c]

        for n in neighbors((r, c), numeric):
            row, col = n
            if n in memo or grid[row][col] == '.':
                continue

            if grid[row][col].isnumeric():
                queue.append((row, col))
            else:
                queue.append((row, col))

def get_nums(num_list: list[tuple[str, str, str]]) -> int:
    total = 0
    row, col, val = num_list.pop()
    num = val

    while num_list:
        r, c, v = num_list.pop()

        if row == r and c == col - 1:
            num = v + num
        else:
            total += int(num)
            num = v
        
        row, col, val = r, c, v
    
    total += int(num)
    
    return total

puzzle_test = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

if __name__ == '__main__':
    with open('day3/one/puzzle.txt') as f:
        puzzle = f.read()
    
    grid = Grid(puzzle)

    for r in range(grid.rows):
        for c in range(grid.cols):
            coord = grid[r][c]
            if not coord.isnumeric() and coord != '.':
                bfs((r, c))
                
    sorted_vals = sorted([(r, c, v) for (r, c), v in num_map.items()], key= lambda x: (x[0], x[1]))
    result = get_nums(sorted_vals)
    print(result)