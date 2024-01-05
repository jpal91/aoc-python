import sys
import runpy

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Not enough args")
        exit(1)
    
    day, part = sys.argv[1], sys.argv[2]
    runpy.run_path(f'pyaoc/day{day}/{"one" if part == "1" else "two"}/main.py', run_name='__main__')