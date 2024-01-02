import os
import sys
from collections import defaultdict, deque
import curses

sys.path.append(os.path.expanduser('~/dev/aoc'))
from grid.grid import Grid, Cell

puzzle_test1 = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

def paint(screen, grid, root, move):
    for y in range(grid.rows):
        for x in range(grid.cols):
            if (cell := grid[y][x]) == root:
                screen.addstr(y, x, str(cell.value), curses.color_pair(2))
            elif cell == move:
                screen.addstr(y, x, str(cell.value), curses.color_pair(1))
            else:
                screen.addstr(y, x, str(cell.value))
    screen.refresh()
    screen.getch()

def main(puzzle: str):
    grid = Grid.from_str(puzzle)
    
    completed = set()
    b_map_val = 0
    # curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
    # curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)

    for i in [0, 3, 2, 1]:
        b_map = defaultdict(int)
        # completed = set()
        if i == 2:
            pass
        
        for y in range(grid.rows):
            for x in range(grid.cols):
                cell = grid[y][x]
                if cell.value in ['#', '.']:
                    continue

                queue = deque([cell])
                
                if cell.coords == (6, 2):
                    pass

                while queue:
                    root = queue.popleft()
                    node = root

                    if node.coords in completed:
                        continue
                    
                    
                    while True:
                        next_node = node.neighbors[i]
                        if next_node and next_node.value == '.':
                            node = next_node
                            continue
                        elif next_node and next_node.value == 'O' and next_node.coords not in completed:
                            queue.extend([next_node, root])
                            break

                        if node != root:
                            root.value = '.'
                        node.value = 'O'
                        b_map[(grid.rows) - node.y] += 1
                        completed.add(node.coords)
                        completed.add(root.coords)
                        # paint(screen, grid, root, node)
                        break
        if i == 0:
            pass
        if i == 1:
            b_map_val += sum([k * v for k, v in b_map.items()])
        completed.clear()

        
    return grid, b_map_val

if __name__ == '__main__':
    with open('day14/two/puzzle.txt') as f:
        puzzle = f.read()
    # puzzle = puzzle_test1

    # curses.init_pair(0, curses.COLOR_GREEN, curses.COLOR_WHITE)
    # curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    # grid, b_map = curses.wrapper(main, puzzle)
    b_vals = []
    grid = puzzle
    count = 0
    grid_map = set()
    while True:
        if hash(grid) in grid_map:
            print(b_map)
            break
        # if hash(grid) in grid_map:
        #     _grid, b_map = grid_map[hash(grid)]
        #     print(b_map)
        # else:
        #     _grid, b_map = main(grid)
        #     grid_map[hash(grid)] = (_grid, b_map)
        #     grid = str(_grid)
        _grid, b_map = main(grid)
        grid_map.add(hash(grid))
        grid = str(_grid)
            
        b_vals.append(b_map)
        # mid = len(b_vals) // 2
        # if len(b_vals) > 1 and b_vals[:mid + 1] == b_vals[mid:]:
        #     break
        count += 1
        print(count, end='\r')

    
    # print(sum([k * v for k, v in b_map.items()]))
    # print(grid, '\n\n', b_vals)
    print(b_vals, len(b_vals))
    # with open('day14/two/puzzle2.txt', 'w') as f:
    #     f.write(str(grid))
    # for i, b in enumerate(b_vals):
    #     b_vals[i - 1] = b - b_vals[i - 1]
    # print(b_vals)