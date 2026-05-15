import logging
from tools import read_lines
import math

input_file = "my_input06.txt"
default_input_file = "input06.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

use_default_input_file = False

def part1(grid):
    m = len(grid)
    result = 0
    for k in range(len(grid[0])):
        operator = grid[m-1][k]
        if operator == "+":
            column_total = sum([int(x[k]) for x in grid[:m-1]])
        elif operator == "*":
            column_total = math.prod([int(x[k]) for x in grid[:m-1]])
        else:
            raise NotImplementedError
        result += column_total
    return result

def part2(grid, operators, operator_positions):
    m = len(grid)
    result = 0
    for k in range(len(operators)):
        operator = operators[k]
        operator_position = operator_positions[k]
        next_operator_position = operator_positions[k+1]-1 if k < len(operator_positions) - 1 else len(grid[0])
        operands = []
        for j in range(operator_position, next_operator_position):
            operands.append(int("".join([grid[m][j] for m in range(len(grid)-1)])))
        logging.info(f"Operands: {operands}")
        logging.info(f"Operator position: {operator_position}")
        logging.info(f"Operator: {operator}")

        if operator == "+":
            column_total = sum(operands)
        elif operator == "*":
            column_total = math.prod(operands)
        else:
            raise NotImplementedError
        result += column_total
    return result

if __name__ == '__main__':
    try:
        lines = read_lines(default_input_file if use_default_input_file else input_file, do_strip=False)
    except FileNotFoundError:
        lines = read_lines(default_input_file, do_strip=False)

    # part 1
    grid_for_part1 = [[y.strip() for y in x.split()] for x in lines ]
    logging.info(f"Input file: {len(grid_for_part1)} rows, {len(grid_for_part1[0])} columns")
    logging.info(f"Part 1: {part1(grid_for_part1)}")

    # part 2
    operator_positions = [i for i in range(len(lines[-1])) if lines[-1][i] != " " and lines[-1][i] != "\n"]
    operators = [lines[-1][i] for i in operator_positions]
    logging.info(f"Operator positions: {operator_positions}")
    grid_as_array = [list(x.replace("\n", "")) for x in lines]
    # Empty columns are to the left of the operators.
    for k in operator_positions:
        if k == 0:
            continue
        for j in range(len(lines)-1):
            # mark this cell as column separator
            grid_as_array[j][k-1] = '#'
    logging.info(f"Part 2: {part2(grid_as_array, operators, operator_positions)}")
