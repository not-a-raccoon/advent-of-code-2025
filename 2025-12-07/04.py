import logging
from tools import read_lines

input_file = "my_input04.txt"
default_input_file = "input04.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

use_default_input_file = False

def part1(grid):
    accessible_fields = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "@":
                occupied_neighbours =  0
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        if not(dx == 0 and dy == 0) and (i+dy) in range(len(grid)) and (j+dx) in range(len(grid[i])):
                            if grid[i+dy][j+dx] == "@":
                                occupied_neighbours += 1
                if occupied_neighbours < 4:
                    accessible_fields += [[i,j]]
    return accessible_fields, len(accessible_fields)

def part2(grid):
    iterations = 0
    accessible_fields_part2 = 0
    while True:
        iterations += 1
        accessible_fields, n = part1(grid)
        accessible_fields_part2 += n
        if n == 0:
            logging.info(f"Breaking after {iterations} iterations")
            break
        logging.info(f"Removing {n} rolls of paper.")
        for [y,x] in accessible_fields:
            grid[y] = (grid[y][:x] if x>0 else '') + '.' + (grid[y][x+1:] if x<len(grid[y])-1 else '')

    return accessible_fields_part2






if __name__ == '__main__':
    try:
        grid = read_lines(default_input_file if use_default_input_file else input_file)
    except FileNotFoundError:
        grid = read_lines(default_input_file)
    logging.info(f"Input file: {len(grid)} rows, {len(grid[0])} columns")
    _, a = part1(grid)
    logging.info(f"Part 1: Accessible fields: {a}")
    b = part2(grid)
    logging.info(f"Part 2: Accessible fields: {b}")


