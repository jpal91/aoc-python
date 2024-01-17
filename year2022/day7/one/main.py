
class Directory:

    def __init__(self, parent = None):
        self.files = []
        self.dirs = {}
        self.parent = parent
    
    @property
    def file_size(self):
        return sum([f[0] for f in self.files])
    

def parse(input: str) -> Directory:
    root = Directory()
    active_dir = root

    for line in input.splitlines()[1:]:
        if line.startswith('$ cd'):
            if line.endswith('..'):
                active_dir = active_dir.parent
            else:
                name = line[5:]
                active_dir = active_dir.dirs[name]
        elif line.startswith('dir'):
            name = line[4:]
            new_dir = Directory(parent=active_dir)
            active_dir.dirs[name] = new_dir
        elif line[0].isnumeric():
            l = line.split(' ')
            active_dir.files.append((int(l[0]), l[1]))
    
    return root

def find_size(act_dir: Directory, dirs: list, part2: bool):
    if not act_dir.dirs:
        if (fs := act_dir.file_size) < 100000 or part2:
            dirs.append(fs)
        return fs
    
    dir_size = act_dir.file_size
    for d in act_dir.dirs.values():
        dir_size += find_size(d, dirs, part2)
    
    if dir_size < 100000 or part2:
        dirs.append(dir_size)
    
    return dir_size

test_puzzle = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

if __name__ == '__main__':
    with open('pyaoc/year2022/inputs/day7.txt') as f:
        puzzle = f.read()

    # puzzle = test_puzzle
    dirs = []
    root = parse(puzzle)

    # find_size(root, dirs, False)
    # print(sum(dirs))

    # dirs.clear()

    find_size(root, dirs, True)
    dirs.sort()

    total = dirs[-1]
    needed = 30000000 - (70000000 - total)

    for d in dirs:
        if d >= needed:
            print(d)
            break
