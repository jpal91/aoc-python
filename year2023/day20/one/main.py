
from enum import Enum, IntEnum
from collections import defaultdict, deque

class Pulse(IntEnum):
    __str__ = Enum.__str__
    HIGH = 1
    LOW = 0

    @staticmethod
    def flip(pulse: int) -> int:
        if pulse == Pulse.HIGH:
            return Pulse.LOW
        else:
            return Pulse.HIGH

class Module:

    def __init__(self, name: str):
        self.name = name
        self._pulse = Pulse.LOW
        self.connections: list[Module] = []
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.pulse})'
    
    @property
    def pulse(self) -> int:
        return self._pulse
    
    toggle = lambda *_: None


class FlipFlop(Module):

    def toggle(self, mod: Module) -> bool:
        if mod.pulse == Pulse.HIGH:
            return None
        self._pulse = Pulse.flip(self.pulse)
        return bool(self.pulse)

class Conjunction(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.memory: dict[Module, int] = defaultdict(int)

    def toggle(self, mod: Module) -> bool:
        self.memory[mod] = mod.pulse

        if all([m for m in self.memory.values()]):
            self._pulse = Pulse.LOW
        else:
            self._pulse = Pulse.HIGH
        
        return bool(self.pulse)

puzzle_test = r"""
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

puzzle_test2 = r"""
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

def press():
    # queue: deque[tuple[Module, Module]] = deque([(c, broadcaster) for c in broadcaster.connections])
    # low, high = len(broadcaster.connections) + 1, 0
    # visited = set()
    queue: deque[Module] = deque([broadcaster])
    low, high = 1, 0

    while queue:
        node = queue.popleft()

        for c in node.connections:
            if node.pulse == Pulse.LOW:
                low += 1
            else:
                high += 1

            if c.toggle(node) is None:
                continue

            queue.append(c)
    
    return low, high

if __name__ == '__main__':
    with open('day20/one/puzzle.txt') as f:
        puzzle = f.read().strip()

    # puzzle = puzzle_test2.strip()

    broadcaster = None
    nodes: dict[str, tuple[Module, list[str]]] = {}
    for p in puzzle.split('\n'):
        node, connections = p.split(' -> ')
        connections = [c.strip() for c in connections.split(',')]

        if node == 'broadcaster':
            broadcaster = Module(node)
            nodes[node] = (broadcaster, connections)
        elif node.startswith('%'):
            new_node = FlipFlop(node[1:])
            nodes[node[1:]] = (new_node, connections)
        else:
            new_node = Conjunction(node[1:])
            nodes[node[1:]] = (new_node, connections)

    for k, v in nodes.items():
        node, connections = v

        for c in connections:
            output = nodes[c][0] if c in nodes else Module('output')
            node.connections.append(output)

            if isinstance(output, Conjunction):
                output.memory[node] = Pulse.LOW
    
    lo, hi = 0, 0
    for _ in range(1000):
        l, h = press()
        lo += l
        hi += h

    print(lo * hi)