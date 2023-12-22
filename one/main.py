

def main(puzzle: str) -> int:
    lines = puzzle.split('\n')
    result = 0

    for line in lines:
        number = ''
        for letter in line:
            if letter.isnumeric():
                number += letter
        
        if number:
            result += int(number[0] + number[-1])
    
    return result

if __name__ == '__main__':
    with open('one/puzzle.txt') as f:
        puzzle = f.read()
    
    final_result = main(puzzle)
    print(final_result)