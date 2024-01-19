import re
import math

class Monkey:

    def __init__(self, items: list[int], op: tuple, test_tf: tuple, part1: bool = True):
        self.items = items
        self.op = op
        self.test_tf = test_tf
        self.inspections = 0
        self.part1 = part1

    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.items:
            raise StopIteration
        
        item = self.items.pop()

        if self.part1:
            new = self.operation(item) // 3
        else:
            new = self.operation(item)
        test, true, false = self.test_tf

        self.inspections += 1

        if not new % test:
            return (true, new)
        
        return (false, new)

    def operation(self, item: int) -> int:
        op_type, op_act = self.op

        if not op_act:
            op_act = item

        if op_type == 0:
            return item + op_act
        else:
            return item * op_act
    
    def add(self, item: int):
        self.items.append(item)
        
def parse(input: str, part1) -> dict[int, Monkey]:
    regex = re.compile(r'Monkey (\d):\n\s+Starting items: (.+)?\n\s+Operation: new = old (.+)?\n\s+Test: divisible by (\d+)\n\s+If true: throw to monkey (\d)\n\s+If false: throw to monkey (\d)', re.DOTALL)
    monkeys = {}

    for m in input.strip().split('\n\n'):
        m_match = regex.match(m)
        g = m_match.groups()
        
        no = int(g[0])
        items = list(map(int, g[1].split(', ')))
        test, true, false = tuple(map(int, g[3:]))

        op_type = 0 if g[2].startswith('+') else 1
        op_act = int(g[2][2:]) if g[2][-1].isnumeric() else None

        monkeys[no] = Monkey(items, (op_type, op_act), (test, true, false), part1)
    

    return monkeys


def part1(input: str) -> int:
    monkeys = parse(input, True)

    for _ in range(20):
        for monkey in monkeys.values():
            for (new, val) in monkey:
                monkeys[new].add(val)
        
    active = math.prod(sorted([m.inspections for m in monkeys.values()])[-2:])

    return active

def part2(input: str) -> int:
    monkeys = parse(input, False)
    [print(k, m.items) for k, m in monkeys.items()]
    for _ in range(10):
        for monkey in monkeys.values():
            for (new, val) in monkey:
                # if val > 1000000:
                #     val = val // 100000
                monkeys[new].add(val)
        [print(k, m.items) for k, m in monkeys.items()]
        print('')
        
    active = math.prod(sorted([m.inspections for m in monkeys.values()])[-2:])

    return active



test_puzzle = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

if __name__ == '__main__':
    with open('pyaoc/year2022/inputs/day11.txt') as f:
        puzzle = f.read()
    puzzle = test_puzzle

    res = part1(puzzle)
    print(res)

    res = part2(puzzle)
    print(res)
