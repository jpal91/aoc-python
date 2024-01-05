import os
import sys
from collections import defaultdict, deque

sys.path.append(os.path.expanduser('~/dev/aoc'))
from utils.grid import Grid, Cell

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

# def move_node(cell: Cell, b_map: dict, rows: int) -> bool:
#     node = cell
#     if not node.neighbors[0]:
#         node.value = 'O'
#         b_map[(rows + 1) - node.y] += 1
#         return True

#     while True:
#         next_node = node.neighbors[0]
#         if not next_node or next_node.value != '.':
#             if next_node and next_node.value == 'O':
#                 res = move_node(next_node, b_map, rows)
#                 if res:
#             node.value = 'O'
#             cell.value = '.'
#             b_map[(rows + 1) - node.y] += 1
#             return True
#         node = next_node

def main(puzzle: str):
    grid = Grid.from_str(puzzle)
    b_map = defaultdict(int)
    completed = set()

    for y in range(grid.rows):
        for x in range(grid.cols):
            cell = grid[y][x]
            # if y == 0:
            #     if cell.value == 'O':
            #         b_map[grid.rows + 1] += 1
            #     continue

            if cell.value in ['#', '.']:
                continue

            queue = deque([cell])
            

            while queue:
                root = queue.popleft()
                node = root

                if node in completed:
                    continue

                
                while True:
                    next_node = node.neighbors[0]
                    if next_node and next_node.value == '.':
                        node = next_node
                        continue
                    elif next_node and next_node.value == 'O' and next_node not in completed:
                        queue.extend([next_node, root])
                        break
                    else:
                        if node != root:
                            root.value = '.'
                        node.value = 'O'
                        b_map[(grid.rows) - node.y] += 1
                        completed.add(node)
                        break


        
    return grid, b_map

if __name__ == '__main__':
    with open('day14/one/puzzle.txt') as f:
        puzzle = f.read()
    # puzzle = puzzle_test1

    grid, b_map = main(puzzle)
    
    print(sum([k * v for k, v in b_map.items()]))