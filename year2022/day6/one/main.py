from collections import deque

class Marker:

    def __init__(self, slice: list):
        self.set = set({*slice})
        self.queue = deque(slice)

    def __str__(self):
        return f"Marker({self.queue}, {self.set})"

    @property
    def is_unique(self) -> bool:
        return len(self.set) == 4

    def add(self, item: str):
        last = self.queue.popleft()
        if last in self.set and last not in self.queue:
            self.set.remove(last)

        self.queue.append(item)
        self.set.add(item)
        

def part1(input: str):
    markers = Marker(input[0:4])

    for i, let in enumerate(input[4:]):
        # print(markers, len(markers.set))
        if markers.is_unique:
            return i + 4
        markers.add(let)

def part2(input: str):
    markers = Marker(input[0:14])

    for i, let in enumerate(input[14:]):
        # print(markers, len(markers.set), i + 14)
        if len(markers.set) == 14:
            return i + 14
        markers.add(let)
    
    return i + 14

    

test_puzzle = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
test_puzzle2 = "bvwbjplbgvbhsrlpgdmjqwftvncz"
test_puzzle3 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"

if __name__ == '__main__':
    import os
    with open(os.path.expanduser("~/dev/aoc/pyaoc/year2022/inputs/day6.txt")) as f:
        puzzle = f.read()
    # puzzle = test_puzzle

    res = part2(puzzle)
    print(res)