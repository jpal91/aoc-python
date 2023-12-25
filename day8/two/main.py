import re
import math

puzzle_test1 = """\
RLR

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)\
"""

puzzle_test2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)\
"""

puzzle_test3 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)\
"""

class LeftRightLoop(list[str]):
    """List that iterates over the Left/Right instructions"""

    def __init__(self, lr: list[str]):
        super().__init__(lr)
        self.current = 0
        self.n = len(self)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        # Returns next value and restarts at the end
        # ie LR -> LRLRLRLRLR...

        value = self[self.current]
        self.current = (self.current + 1) % self.n
        return value

class IterNode:
    """Iterates over the path based on the root node and the map"""

    def __init__(self, node: str, node_map: dict[str, list[str]]):
        self.root = node
        self.node = node
        self.node_map = node_map
        self.lr = 0
        self.steps = -1
        self.stop = False
    
    def __next__(self) -> str:
        value = self.node
        self.node = self.node_map[self.node][self.lr]
        return value
    
    def get_next(self, lr: int) -> bool:
        """Gets next node until it reaches a node ending in Z"""
        
        # Will return True once it's reached the end, waiting
        # for other IterNodes to complete
        if self.stop:
            return True
        self.lr = lr
        n = next(self)
        self.steps += 1

        if n.endswith('Z'):
            self.stop = True
            return True
        else:
            return False

class PathGroup(list[IterNode]):
    """Class to control starting group of IterNodes (ones beginning with A)"""
    
    def __init__(self, node_map: dict[str, list[str]], lr: LeftRightLoop):
        super().__init__(
            [IterNode(k, node_map) for k in node_map.keys() if k.endswith('A')]
        )
        self.lr = lr
    

    def __next__(self) -> bool:
        # Next will be called on each node until they reach the end (Z)
        # Their individual steps will be used to determine the Lowest Common Multiple
        next_lr = next(self.lr)
        return all([n.get_next(next_lr) for n in self])
    
    def print_paths(self) -> None:
        for node in self:
            print(node.root, node.steps)
    
    def get_lcm(self) -> list[int]:
        """Returns LCM of each node to determine when all will collide at Z"""
        return math.lcm(*[node.steps for node in self])
        

if __name__ == '__main__':
    with open('day8/one/puzzle.txt') as f:
        puzzle = f.read()
    
    puzzle = re.match(r'(.*)\n\n(.*)', puzzle, re.DOTALL)
    
    LR = LeftRightLoop([0 if item == 'L' else 1 for item in puzzle.group(1)])
    NODE_MAP = {
        k : v.split(', ') for k,v in
        re.findall(r'(\w\w\w) = \((\w\w\w, \w\w\w)\)\n?', puzzle.group(2))
    }

    pg = PathGroup(NODE_MAP, LR)

    while not next(pg):
        continue

    print(pg.get_lcm())
