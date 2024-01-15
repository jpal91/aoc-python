import re
import math
from collections import deque

AL_REGEX = re.compile(r'.+:\n?(.+)', re.DOTALL)

class Map(dict[range, range]):

    def __init__(self, map: str) -> None:
        super().__init__()
        _map = AL_REGEX.match(map).group(1).strip().split('\n')
        

        for m in _map:
            source, dest, delta = (int(v) for v in m.split(' ') if v)
            self[range(dest, dest + delta + 1)] = range(source, source + delta + 1)
        
        self._keys = [k for k in self.keys()]
    
    def __repr__(self) -> str:
        return f"Map({len(self.keys())})"
    
    def __contains__(self, __key: range | int) -> bool:
        if isinstance(__key, range):
            for k in self._keys():
                if __key.start in k or __key[-1] in k:
                    return True
            return False
        return any([__key in r for r in self.keys()])
    
    # def __getitem__(self, __key: int) -> int:
    #     for key in self.keys():
    #         if __key in key:
    #             idx = key.index(__key)
    #             return self.get(key)[idx]
    #     return __key

    def contains(self, __key: range) -> tuple[range, range]:
        for k in self._keys:
            if __key.start in k or __key[-1] in k:
                return (k, self[k])
        return ()

# class Alamanac(list[Map]):

#     def __init__(self, maps: list[str]) -> None:
#         super().__init__([Map(m) for m in maps])
    
#     def __contains__(self, __key: object) -> bool:
#         return any([__key in s for s in self])

#     def get_location(self, seed: int) -> int:
#         next_key = None

#         for map in self:
#             if not next_key:
#                 next_key = map[seed]
#             else:
#                 next_key = map[next_key]
        
#         return next_key
    
ALMANAC: list[Map] = None

def clamp(rang1: range, key_range: range, val_range: range) -> list[range]:
    ranges = []
    nr_start, nr_end = val_range.start, val_range[-1]

    if rang1.start < key_range.start:
        ranges.append(range(rang1.start, key_range.start))
    else:
        nr_start += (rang1.start - key_range.start)

    if key_range[-1] < rang1[-1]:
        ranges.append(range(key_range[-1], rang1[-1] + 1))
    else:
        nr_end -= (key_range[-1] - rang1[-1])
    
    ranges.append(range(nr_start, nr_end))
    return ranges

def bfs(rang: range):
    queue = deque([(rang, 0, [])])
    minimum = math.inf

    while queue:
        r, idx, path = queue.popleft()

        ranges = [r]
        # for map in ALMANAC[idx]:
        #     if key := map.contains(r):
        #         ranges = clamp(r, key, ALMANAC[idx][key])
        #         break
        cur_map = ALMANAC[idx]

        if kv := cur_map.contains(r):
            ranges = clamp(r, kv[0], kv[1])
        
        if idx == 6:
            small_range = min(ranges, key= lambda x: x.start)
            minimum = min(small_range.start, minimum)
            # if minimum == 0:
            #     for key in ALMANAC[idx].keys():
            #         if r.start in key:
            #             idxx = key.index(r.start)
            #             print(ALMANAC[idx][key][idxx])
            #             exit()
            # continue
            # for nr in ranges:
            #     if r.start in nr:
            #         nidx = nr.index(r.start)
            #         minimum = min(minimum, nr[nidx])
            #     else:
            #         minimum = min(minimum, r.start)
            continue
        
        for nr in ranges:
            queue.append((nr, idx + 1, [*path, r]))
    
    return minimum

puzzle_test = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

if __name__ == '__main__':
    with open('day5/one/puzzle.txt') as f:
        puzzle = f.read()
    
    puzzle = puzzle.split('\n\n')
    seeds = AL_REGEX.match(puzzle[0]).group(1).strip().split(' ')
    puzzle.pop(0)

    seeds = [range(int(seeds[r]), int(seeds[r]) + int(seeds[r + 1]) + 1) for r in range(0, len(seeds), 2)]
    # print(seeds)
    ALMANAC = [Map(p) for p in puzzle]

    # print(min([min(almanac.get_location(int(s[0])), almanac.get_location(int(s[-1]))) for s in seeds]))
    # print(almanac.get_location(515785082))
    # res = bfs(seeds[2])
    res = min([_res := bfs(s) for s in seeds])
    print(res)