import re

VALUES = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

REGEX = re.compile(r'(?=(one|two|three|four|five|six|seven|eight|nine|[0-9])).*(one|two|three|four|five|six|seven|eight|nine|[0-9])')

def main(puzzle: str) -> int:
    puzzle = puzzle.split('\n')
    results = []

    for _, line in enumerate(puzzle):
        matches = REGEX.search(line)
        if not matches or not matches.groups():
            continue

        first, last = matches.groups()

        if first in VALUES:
            first = VALUES[first]
        if last in VALUES:
            last = VALUES[last]
        

        results.append(first + last)

    return sum([int(r) for r in results])

puzzle_alt = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

if __name__ == '__main__':
    with open('two/puzzle.txt') as f:
        puzzle = f.read()
    
    final_result = main(puzzle)
    print(final_result)