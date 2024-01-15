import math
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
        # self.memory: dict[Module, int] = defaultdict(int)
        self.memory: list[Module] = []

    def toggle(self, mod: Module) -> bool:

        if all([m.pulse for m in self.memory]):
            self._pulse = Pulse.LOW
        else:
            self._pulse = Pulse.HIGH
        
        return bool(self.pulse)

class BroadCaster(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state_map: dict[int, tuple[Pulse]] = {}
        self.nodes: list[Module] = []
        self.last_state = None
    
    @property
    def state(self) -> int:
        # return list((c.pulse for c in self.nodes))
        return hash(tuple(c.pulse for c in self.nodes))
    
    @property
    def repeat_hash(self) -> bool:
        return self.last_state in self.state_map
    
    def set_state(self) -> None:
        state = tuple(c.pulse for c in self.nodes)
        state_hash = hash(state)
        
        if state_hash not in self.state_map:
            self.state_map[hash(state)] = state
            return None
        return state_hash
    
    def update_state(self, hash: int) -> None:
        state = self.state_map[hash]
        for n, s in zip(self.nodes, state):
            n._pulse = s

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

def press(targets: list[Module]):
    queue: deque[Module] = deque([broadcaster])
    report = []

    while queue:
        node = queue.popleft()

        if node in targets and node.pulse == Pulse.HIGH:
            report.append(node)

        for c in node.connections:
            if c.toggle(node) is None:
                continue

            queue.append(c)
    

    return report

def timeit(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return res
    return wrapper

if __name__ == '__main__':
    with open('day20/one/puzzle.txt') as f:
        puzzle = f.read().strip()


    broadcaster = None
    nodes: dict[str, tuple[Module | FlipFlop | Conjunction, list[str]]] = {}
    for p in puzzle.split('\n'):
        node, connections = p.split(' -> ')
        connections = [c.strip() for c in connections.split(',')]

        if node == 'broadcaster':
            broadcaster = BroadCaster(node)
            nodes[node] = (broadcaster, connections)
        elif node.startswith('%'):
            new_node = FlipFlop(node[1:])
            nodes[node[1:]] = (new_node, connections)
        else:
            new_node = Conjunction(node[1:])
            nodes[node[1:]] = (new_node, connections)

    for k, v in nodes.items():
        node, connections = v
        broadcaster.nodes.append(node)

        for c in connections:
            if c in nodes:
                output = nodes[c][0]
            else:
                output = Module(c)
                setattr(output, 'toggle', lambda *_: True)
            node.connections.append(output)

            if isinstance(output, Conjunction):
                output.memory.append(node)
    
    targets: list[Conjunction] = nodes['xn'][0].memory

    count = 0
    cycles = []

    while targets:
        count += 1
        report = press(targets)
        for r in report:
            cycles.append(count)
            targets.remove(r)
        
        if not targets:
            break
    
    print(math.lcm(*cycles))


