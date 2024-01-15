from collections import defaultdict

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

def neighbors(coords: tuple[int, int]) -> list[tuple[int, int]]:
    row, col = coords
    new_coords = []

    for d in DELTAS:
        dy, dx = d
        new_r, new_c = row + dy, col + dx

        if (
            new_r < 0 or new_r >= grid.rows or
            new_c < 0 or new_c >= grid.cols
        ):
            continue

        new_coords.append((new_r, new_c))
    
    return new_coords

def dfs(coords: tuple[int, int]) -> str:
    r, c = coords

    if (r, c) in memo or c < 0 or c >= grid.cols or not grid[r][c].isnumeric():
        return ''
    
    memo.add((r, c))
    
    return dfs((r, c - 1)) + grid[r][c] + dfs((r, c + 1))


def get_adj(coords: tuple[int, int]) -> list[int]:
    row, col = coords

    adj_nums = []
    for n in neighbors((row, col)):
        r, c = n
        res = dfs((r, c))

        if res:
            adj_nums.append(res)
    
    if len(adj_nums) == 2:
        return adj_nums
    else:
        return []


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
    total = 0

    for r in range(grid.rows):
        for c in range(grid.cols):
            coord = grid[r][c]
            if not coord.isnumeric() and coord != '.':

                if res := get_adj((r, c)):
                    total += (int(res[0]) * int(res[1]))
                
    print(total)