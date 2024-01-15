
cv = []

with open('day15/one/puzzle.txt') as f:
    puzzle = f.read().strip().split(',')

puzzle_test = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

puzzle = puzzle_test.strip().split(',')

for string in puzzle:
    _cv = 0
    for let in string[:2]:
        _cv = ((ord(let) + _cv) * 17) % 256
    # cv += _cv
    cv.append(_cv)

print(cv)