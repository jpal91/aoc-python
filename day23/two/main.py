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
            # self.val = sum([sum(e.coords) for e in self])
            y,x = 0, 0
            for n in self:
                r, c = n.coords
                y += r
                x += c
            
            y = y // len(self)
            x = x // len(self)

            self.val = (y, x)
        
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
            # exits.extend([(k, n) for n in v if n[1] != 2])
            # self.add(tuple(sorted((k, *adj_nodes), key=lambda x: x.coords)))
            self.add(self.Edge((k, *adj_nodes)))
        
        # for ent, ext in exits:
        #     ent_node = self.get(ent)
        #     ext_node = self.get(ext[0])
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    
    def __hash__(self):
        return hash(tuple(sorted(self)))

    # @lru_cache(None)
    def get(self, node: Cell):
        if node in self.edge_map:
            return self.edge_map[node]
        for n in self:
            if node in n:
                self.edge_map[node] = n
                return n
        return None
    
    # def add(self, edge):
    #     for n in edge:
    #         self.edge_map[n] = edge
    #     super().add(edge)
    
    # def remove(self, edge):
    #     for n in edge:
    #         del self.edge_map[n]
        
    #     super().remove(edge)
    



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

    path = set()
    count = 0
    

    
    # res = longest_path(first, 0, True)
    end = time.time()
    # print(res, count, end - start)
    # print(longest_path.cache_info())



    print(end - start)