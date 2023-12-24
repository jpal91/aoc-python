import re

puzzle_test = """\
Time:      7  15   30
Distance:  9  40  200
"""

def farthest(held: int, max: int) -> int:
    return (max - held) * held

if __name__ == '__main__':
    with open('day6/one/puzzle.txt') as f:
        puzzle = f.read()

    t, d = puzzle.strip().split('\n')
    times = map(int, t[5:].split())
    dists = map(int, d[9:].split())

    beats = 1
    for time, dist in zip(times, dists):
        best = len(list(filter(lambda x: x[1] > dist, [ (t, farthest(t, time)) for t in range(time + 1) ])))
        beats *= best
        print(best)
    print(beats)