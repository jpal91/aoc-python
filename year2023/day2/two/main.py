import re

REGEX = re.compile(r'((\d+) (red|green|blue))')

def main(puzzle: str) -> int:
    # puzzle = puzzle.split('\n')
    powers = 0
    
    for line in puzzle:
        matches = REGEX.findall(line)
        red, blue, green = 0, 0, 0

        for m in matches:
            if m[2] == 'red':
                red = max(red, int(m[1]))
            elif m[2] == 'green':
                green = max(green, int(m[1]))
            elif m[2] == 'blue':
                blue = max(blue, int(m[1]))
        
        powers += (red * green * blue)
    
    return powers


puzzle_test = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

if __name__ == '__main__':
    with open('day2/one/puzzle.txt') as f:
        puzzle = f.readlines()
    
    result = main(puzzle)
    print(result)

    