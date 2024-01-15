from typing import Any, Generator

DELTAS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


class Cell:

    def __init__(
        self, val: str | int | None = None, y: int = None, x: int = None
    ) -> None:
        self.value = val
        self._neighbors = [None] * 8
        self.y = y
        self.x = x

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value}, {self.y}, {self.x})"

    @property
    def coords(self) -> tuple[int, int]:
        return self.y, self.x

    @property
    def neighbors(self) -> list["Cell"]:
        return self._neighbors
    
    @property
    def act_neighbors(self) -> list["Cell"]:
        return [n for n in self._neighbors if n]

    @neighbors.setter
    def neighbors(self, n_list: list["Cell"]) -> None:
        self._neighbors = n_list


class Grid(list):
    def __init__(
        self,
        grid: list[list] = None,
        size: int = None,
        cell: Cell = Cell,
        n_size: int = 4,
    ) -> None:
        if not issubclass(cell, Cell):
            raise TypeError

        if grid:
            self.rows = len(grid)
            self.cols = len(grid[0])
            super().__init__(
                [
                    [
                        cell(grid[r][c], y=r, x=c)
                        if not isinstance(grid[r][c], Cell)
                        else grid[r][c]
                        for c in range(self.cols)
                    ]
                    for r in range(self.rows)
                ]
            )
        elif size:
            super().__init__(
                [[cell(y=r, x=c) for c in range(size)] for r in range(size)]
            )
            self.rows, self.cols = size, size

        self.y = 0
        self.x = 0

        for cell in self:
            cell.neighbors = [
                self[n[0]][n[1]] if n else None
                for n in self.neighbors(cell, n_size)
            ]
    
    def __str__(self):
        res = ""
        for i in range(self.rows):
            res += f'{self[i]}\n'
        return res

    def __next__(self):
        if self.y >= self.rows:
            self.y, self.x = 0, 0
            raise StopIteration

        value: Cell = self[self.y][self.x]

        self.x += 1
        if self.x >= self.cols:
            self.x = 0
            self.y += 1

        return value

    def __iter__(self):
        self.x, self.y = 0, 0
        return self
    
    def __contains__(self, key: Cell | tuple[int, int]) -> bool:
        if isinstance(key, Cell):
            return any([key in row for row in self])
        y, x = key
        return y >= 0 and y < self.rows and x >= 0 and x < self.cols

    def enum(self) -> Generator[tuple[int, int, Cell], None, None]:
        # y, x = -1, -1
        # for cell in self:
        #     x = (x + 1) % self.cols
        #     if x == 0:
        #         y += 1
        #     yield y, x, cell
        for y in range(self.rows):
            for x in range(self.cols):
                yield y, x, self[y][x]

    def neighbors(self, cell: Cell, n_size: int) -> list[tuple[int, int]]:
        row, col = cell.coords
        n_list = []
        deltas = DELTAS if n_size == 8 else DELTAS[0::2]

        for d in deltas:
            dy, dx = d
            new_row, new_col = dy + row, dx + col

            if new_row < 0 or new_row >= self.rows or new_col < 0 or new_col >= self.cols:
                n_list.append(None)
            else:
                n_list.append((new_row, new_col))

        return n_list

    @classmethod
    def from_str(cls, grid: str, type_hint: Any = str) -> "Grid":
        grid = [list(map(type_hint, col.split())) for col in grid.strip().split("\n")]
        return cls(grid)





if __name__ == "__main__":
    grid_list = [["A", "A", "A"], ["B", "B", "B"], ["C", "C", "C"]]
    grid_str = """\
    A A A
    B B B
    C C C
    """
    # grid = Grid(grid_list)
    # grid = Grid.from_str(grid_str)
    print(DELTAS[0::2])

    # for cell in grid:
    #     print(cell)
    # for y, x, cell in grid.enum():
    #     print(y, x, cell)
