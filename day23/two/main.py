from collections import defaultdict, deque
from pprint import pprint
import sys
import time
sys.path.append('/home/jpal/dev/aoc/pyaoc')
import curses
import heapq
from functools import lru_cache, cached_property
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

class Edges(set):

    class Edge(list):
        
        def __init__(self, nodes):
            super().__init__(sorted(nodes, key=lambda x: x.coords))

            y,x = 0, 0
            for n in self:
                r, c = n.coords
                y += r
                x += c
            
            y = y // len(self)
            x = x // len(self)

            self.val = (y, x)
            self.exits = []

        def __repr__(self):
            return f'Edge{self.val}'
        
        def __eq__(self, other):
            # return all([o in self for o in other])
            return other.val == self.val

        def __lt__(self, other):
            return self.val < other.val
        
        def __hash__(self):
            # return hash(tuple(self))
            return hash(self.val)

    def __init__(self, graph: dict):
        super().__init__()
        self.edge_map = {}
        exits = []

        for k, v in graph.items():
            adj_nodes = (n[0] for n in v if n[1] == 2)
            exits.extend([(k, n) for n in v if n[1] != 2])
            # self.add(tuple(sorted((k, *adj_nodes), key=lambda x: x.coords)))
            self.add(self.Edge((k, *adj_nodes)))
        
        for ent, ext in exits:
            ent_node = self.get(ent)
            ext_node = self.get(ext[0])
            ent_node.exits.append((ext_node, ext[1]))
    

    def get(self, node: Cell):
        if node in self.edge_map:
            return self.edge_map[node]
        for n in self:
            if node in n:
                self.edge_map[node] = n
                return n
        return None
    
    



def dfs(cell: Cell, steps: int, connects: list, visited: set, start: Cell):
    if cell.value in ['v', '>', '<', 'S', 'X'] and cell != start:
        return [(cell, steps)]
    if cell.value == '#':
        return []
    
    n_list = []
    visited.add(cell)

    for n in cell.act_neighbors:
        if n in visited:
            continue
        
        if res := dfs(n, steps + 1, connects, visited, start):
            n_list.extend(res)
        

    return [*connects, *n_list]

@lru_cache(10000)
def longest_path(node: Cell, steps_taken: int, exiting: bool) -> int:

    if node == last:
        return steps_taken
    
    if (edge := edges.get(node)) in path:
        return 0

    if exiting:
        path.add(edge)
    

    longest = 0
    for next_node, steps in graph[node]:
        
        if (exiting and steps == 2) or (not exiting and steps > 2):
            continue

        res = longest_path(next_node, steps + steps_taken, not exiting)
        
        longest = max(longest, res)

    if exiting:
        path.remove(edge)

    return longest

@lru_cache(10000)
def longest_path2(edge: Edges.Edge, steps_taken: int, prev) -> int:

    if edge == last:
        return steps_taken - 2

    if edge in path:
        return 0

    
    path.add(edge)
    longest = 0
    for next_edge, steps in edge.exits:

        res = longest_path2(next_edge, steps + steps_taken + 2, edge)

        longest = max(longest, res)

    path.remove(edge)


    return longest



if __name__ == '__main__':
    
    puzzle = puzzle_test
    puzzle = get_input(23)
    grid = Grid.from_str(puzzle, cell=Cell)
    nodes = list[Cell]
    graph: dict[Cell, list[tuple[Cell, int]]] = {}

    for y, x, cell in grid.enum():
        if (
            (one := (y == 0 and cell.value == '.')) or
            (two := (y == grid.rows - 1 and cell.value == '.')) or
            cell.value in ['v', '<', '>']
        ):
            if one:
                first = cell
                cell.value = 'S'
            if two:
                last = cell
                cell.value = 'X'
            graph[cell] = dfs(cell, 0, [], set(), cell)

            if two:
                [graph[c].append((last, s)) for c,s in graph[cell]]
    start = time.time()
    edges = Edges(graph)

    memo = {}
    path = set()
    count = 0
    
    first = edges.get(first)
    last = edges.get(last)

    res = None #longest_path2(first, 0, None)
    end = time.time()
    print(res, end - start)