
def get_last_col(nums: list[int]) -> list[int]:
    first_col = [nums[0]]
    next_row = nums

    while True:
        tmp = []
        
        for i in range(1, len(next_row)):
            tmp.append(next_row[i] - next_row[i - 1])
        
        first_col.append(tmp[0])

        if not any(tmp):
            break
        else:
            next_row = tmp
    
    # print(first_col[::-1])
    return first_col[::-1]

def get_final_num(nums: list[int]) -> int:
    final_num = []

    for n in nums:
        if not final_num:
            final_num.append(0)
            continue
        else:
            final_num.append(n - final_num[-1])
    
    # print(final_num)
    return final_num[-1]

puzzle_test = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45\
"""

if __name__ == '__main__':
    with open('day9/one/puzzle.txt') as f:
        puzzle = f.read()

    # puzzle = puzzle_test
    puzzle = [[int(l) for l in line.split(' ')] for line in puzzle.split('\n')]
    
    final_nums = []

    for p in puzzle:
        # print(p)
        last_col = get_last_col(p)
        final_nums.append(get_final_num(last_col))
        # print(' ')
    
    print(sum(final_nums))

