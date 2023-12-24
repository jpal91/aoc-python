import re

AL_REGEX = re.compile(r'.+:\n?(.+)', re.DOTALL)

class Map(dict[range, range]):

    def __init__(self, map: str) -> None:
        super().__init__()
        _map = AL_REGEX.match(map).group(1).strip().split('\n')

        for m in _map:
            source, dest, delta = (int(v) for v in m.split(' ') if v)
            self[range(dest, dest + delta + 1)] = range(source, source + delta + 1)
    
    def __contains__(self, __key: object) -> bool:
        return any([__key in r for r in self.keys()])
    
    def __getitem__(self, __key: int) -> int:
        for key in self.keys():
            if __key in key:
                idx = key.index(__key)
                return self.get(key)[idx]
        return __key

class Alamanac(list[Map]):

    def __init__(self, maps: list[str]) -> None:
        super().__init__([Map(m) for m in maps])
    
    def __contains__(self, __key: object) -> bool:
        return any([__key in s for s in self])

    def get_location(self, seed: int) -> int:
        next_key = None

        for map in self:
            if not next_key:
                next_key = map[seed]
            else:
                next_key = map[next_key]
            # print(next_key)
        
        return next_key

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

    almanac = Alamanac(puzzle)

    # print(min([almanac.get_location(int(s)) for s in seeds]))
    print(almanac.get_location(457535844))
    # print(min([almanac.get_location(s) for s in range(720333403, 1105567597)]))