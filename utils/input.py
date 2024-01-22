import sys
from pathlib import Path

def _get_input(day: int) -> str:
    dir_path = Path('~/dev/aoc/pyaoc/inputs').expanduser()
    input_path = dir_path / f'day{day}.txt'

    with open(input_path) as f:
        puzzle = f.read().strip()
    
    return puzzle


def get_input(year: int, day: int) -> str:
    dir_path = Path(f'~/dev/aoc/pyaoc/year20{year}/inputs').expanduser()
    input_path = dir_path / f'day{day}.txt'

    with open(input_path) as f:
        puzzle = f.read().strip()
    
    return puzzle