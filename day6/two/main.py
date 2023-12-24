
puzzle_test = """\
Time:      7  15   30
Distance:  9  40  200
"""

def farthest(held: int, max: int) -> int:
    return (max - held) * held

def binary_search(pos_range: range, max_time: int, max_dist: int, rev: bool) -> int:
    l, r = 0, pos_range[-1]

    while l <= r:
        mid = (r + l) // 2
        wins = farthest(mid, max_time) > max_dist

        if wins:
            if not rev:
                r = mid - 1
            else:
                l = mid + 1
        else:
            if not rev:
                l = mid + 1
            else:
                r = mid - 1
        
        if l == r:
            if not rev:
                return mid + 1
            else:
                return mid - 1

if __name__ == '__main__':
    with open('day6/one/puzzle.txt') as f:
        puzzle = f.read()

    t, d = puzzle.strip().split('\n')
    time = int("".join(map(str, t[5:].split())))
    dist = int("".join(map(str, d[9:].split())))

    bottom, top = 0, time

    half1 = range(0, time // 2)
    half2 = range(time // 2, time + 1)
    search1 = binary_search(half1, time, dist, False)
    search2 = binary_search(half2, time, dist, True)
    print(search1, search2)
    print(search2 - search1)
