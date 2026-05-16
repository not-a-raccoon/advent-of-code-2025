import logging
from tools import read_lines

input_file = "my_input07.txt"
default_input_file = "input07.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

use_default_input_file = False

part1_split_count = 0
part2_path_count = 1

def part1(grid, x, y):
    # Place a beam at (x,y), then propagate it
    global part1_split_count
    if grid[y][x] != ".":
        return
    grid[y][x] = "|"
    if y < len(grid)-1:
        if grid[y+1][x] == "^":
            # beam splitter
            part1(grid, x - 1, y + 1)
            part1(grid, x + 1, y + 1)
            part1_split_count += 1
        else:
            part1(grid, x, y + 1)

def part2(grid, start_x, start_y):
    rows = len(grid)
    cols = len(grid[0])
    # path_counts[y][x] = number of distinct beam paths passing through (x, y)
    path_counts = [[0] * cols for _ in range(rows)]
    path_counts[start_y][start_x] = 1

    # each cell is computed once using its parent's count
    for y in range(start_y, rows - 1):
        for x in range(cols):
            count = path_counts[y][x]
            if count == 0:
                continue
            if grid[y + 1][x] == "^":
                if x - 1 >= 0:
                    path_counts[y + 1][x - 1] += count
                if x + 1 < cols:
                    path_counts[y + 1][x + 1] += count
            else:
                path_counts[y + 1][x] += count

    return path_counts

def pretty_print(array):
    for line in array:
        print("".join(
            [x  for x in line]))

if __name__ == '__main__':
    try:
        lines = read_lines(default_input_file if use_default_input_file else input_file)
    except FileNotFoundError:
        lines = read_lines(default_input_file)
    grid_as_array = [list(x.replace("\n", "")) for x in lines]

    start_pos = [x for x in range(len(grid_as_array[0])) if grid_as_array[0][x] == "S"][0]

    # part 1
    part1(grid_as_array, start_pos, 1)

    # part 2
    path_counts = part2(grid_as_array, start_pos, 1)
    part2_path_count = sum(path_counts[-1])

    # pretty_print(grid_as_array)
    logging.info(f"Part 1: {part1_split_count} beam splits")
    logging.info(f"Part 2: {part2_path_count} beam paths")