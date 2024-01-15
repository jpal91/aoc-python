

with open('day15/one/puzzle.txt') as f:
    puzzle = f.read().strip().split(',')

puzzle_test = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

# puzzle = puzzle_test.strip().split(',')
boxes: dict[int, list] = { num : [] for num in range(256) }
box_map = {}

def get_box(label: str) -> int:
    box = 0
    for let in label:
        box = ((ord(let) + box) * 17) % 256
    
    return box

def parse_step(step: str) -> tuple[str, str, int | None]:
    add = False if step[-1] == '-' else True
    label = step[:-2] if add else step[:-1]

    return step, label, add

for string in puzzle:
    step, label, add = parse_step(string)

    if not add:
        if label in box_map:
            box_num, old_step = box_map[label]
            boxes[box_num].remove(old_step)
            del box_map[label]
    elif add and label in box_map:
        box_num, old_step = box_map[label]
        idx = boxes[box_num].index(old_step)
        boxes[box_num][idx] = step
        box_map[label] = (box_num, step)
    else:
        box_num = get_box(label)
        boxes[box_num].append(step)
        box_map[label] = (box_num, step)

# print(boxes)
total = 0

for k, v in boxes.items():
    if not v:
        continue
    total += sum([(k + 1)* (i + 1) * int(val[-1]) for i, val in enumerate(v)])

print(total)


