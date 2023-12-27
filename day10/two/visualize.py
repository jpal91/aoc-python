from main import PuzzleGrid, Pipe

def visualize(grid: PuzzleGrid) -> str:
    res = ""
    vert_borders = ""

    for _, x, cell in grid.enum():
        if x == 0:
            res += '\n' + vert_borders + '\n'
            vert_borders = ""
        
        if isinstance(cell, Pipe) and cell.main_loop:
            res += f'\033[31m{cell.value}\033[0m '
        elif cell.escaped:
            res += f'\033[32m{cell.value}\033[0m '
        else:
            res += cell.value + ' '
        
        if (b := (cell, cell.neighbors[1])) in grid.borders:
            # if self.borders[b].is_exit:
            #     res += '\033[37;95m||\033[0m '
            if grid.borders[b].active:
                res += '\033[34m||\033[0m '
            else:
                res += '   '
        else:
            res += '   '
        
        if (b := (cell, cell.neighbors[2])) in grid.borders:
            # if self.borders[b].is_exit:
            #     vert_borders += '\033[37;95m=\033[0m    '
            if grid.borders[b].active:
                vert_borders += '\033[34m=\033[0m    '
            else:
                vert_borders += '     '
        else:
            vert_borders += '     '
    
    return res