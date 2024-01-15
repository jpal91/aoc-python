import re

RED = 12
GREEN = 13
BLUE = 14

REGEX = re.compile(r'((\d+) (red|green|blue))')

def main(puzzle: str) -> int:
    ids = 0
    
    for i, line in enumerate(puzzle):
        matches = REGEX.findall(line)
        valid = True

        for m in matches:
            if m[2] == 'red' and int(m[1]) > RED:
                valid = False
            elif m[2] == 'green' and int(m[1]) > GREEN:
                valid = False
            elif m[2] == 'blue' and int(m[1]) > BLUE:
                valid = False
            
            if not valid:
                break
        
        if valid:
            ids += i + 1
    
    return ids


if __name__ == '__main__':
    with open('day2/one/puzzle.txt') as f:
        puzzle = f.readlines()
    
    result = main(puzzle)
    print(result)

    