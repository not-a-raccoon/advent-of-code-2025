import logging
from tools import read_lines
import galois, numpy as np
import itertools
import sympy as sp
from scipy.optimize import milp, LinearConstraint, Bounds


input_file = "my_input10.txt"
default_input_file = "input10.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

use_default_input_file = False

def parse_input(lines):
    result = []
    for s in lines:
        b = None
        c = None
        A = []
        for t in s.split():
            if t[0] == "[":
                #  result vector
                b = [int(x) for x in t[1:-1].replace("#","1").replace(".","0")]
            elif t[0] == "(":
                # coefficient column, b should already be defined when we encounter one of these
                assert b is not None
                v = [0]*len(b)
                tt = t[1:-1].split(",")
                for i in range(len(tt)):
                    v[int(tt[i])] = 1
                A += [v]
            elif t[0] == "{":
                c = [int(x) for x in t[1:-1].split(",")]
        result += [[A, b, c]]
    return result

def part1(L):
    # The inputs in parentheses define a matrix A, the input in square brackets
    # defines a vector v, both over GF(2). The system of equations could be underdefined,
    # so there could be more than one possible solution. We need to find the solution vector
    # with the lowest number of nonzero elements to solve the puzzle.
    # To do this, we row-reduce the matrix, pick a particular solution, and then iterate
    # over the matrix's null space to enumerate all solutions.
    maxdim = 0
    GF2 = galois.GF(2)
    sum_of_lowest_number_of_ones = 0
    for i in range(len(L)):
        A, b, _ = L[i]
        AA = GF2(np.transpose(A))
        logging.info(f"*** Problem #{i} ***")

        aug = GF2(np.column_stack([np.transpose(A), np.transpose(b)]))
        R = aug.row_reduce()
        N, M = AA.shape
        logging.debug(f"A has shape: {N}x{M}")
        logging.debug(f"A|b:\r\n{aug}")

        # particular solution:
        x_particular = GF2.Zeros(M)
        row = 0
        for col in range(M):
            if row < N and R[row, col] == 1:
                x_particular[col] = R[row, -1]
                row += 1
        logging.debug(f"Particular solution: {x_particular}")

        # null space basis:
        null_basis = AA.null_space()

        logging.debug(f"\nNull-space has dimension: {len(null_basis)}")

        # All solutions, check for lowest number of "1"s:
        solutions = []
        lowest_number_of_ones = None

        k = len(null_basis)
        best_solution = None
        for bits in itertools.product([0, 1], repeat=k):
            x = x_particular.copy()
            for bit, vec in zip(bits, null_basis):
                if bit:
                    x += vec
            number_of_ones = np.count_nonzero(x)
            if (not lowest_number_of_ones) or number_of_ones < lowest_number_of_ones:
                lowest_number_of_ones = number_of_ones
                best_solution = x
        assert lowest_number_of_ones
        logging.info(f"Lowest number of ones: {lowest_number_of_ones}, best solution: {best_solution}")
        sum_of_lowest_number_of_ones += lowest_number_of_ones

    logging.info(f"Sum of lowest number of ones: {sum_of_lowest_number_of_ones}")


def to_integer_vector(v):
    """
    Scale a rational SymPy vector to an integer vector.
    """
    denoms = [r.q for r in v]
    scale = sp.lcm(denoms)

    return sp.Matrix([int(scale * r) for r in v])


def part2(L):
    sum_of_lowest_number_of_moves = 0
    for i in range(len(L)):
        logging.info(f"*** Problem #{i} ***")
        A, _, b = L[i]
        A_T = np.array(A, dtype=float).T # shape: (number of counters, number of buttons)
        n_buttons = len(A)

        # Minimize sum of x (all coefficients = 1)
        c = np.ones(n_buttons)
        constraints = LinearConstraint(A_T, lb=b, ub=b)
        integrality = np.ones(n_buttons)  # all variables should be integers
        bounds = Bounds(lb=0)  # x_i >= 0

        res = milp(c, constraints=constraints, integrality=integrality, bounds=bounds)
        x = int(round(res.fun))

        best_manhattan_norm = int(round(res.fun))

        logging.info(f"Shortest solution has norm: {best_manhattan_norm}")

        sum_of_lowest_number_of_moves += best_manhattan_norm

    logging.info(f"Sum of lowest number of ones: {sum_of_lowest_number_of_moves}")

    return sum_of_lowest_number_of_moves


if __name__ == '__main__':
    try:
        lines = read_lines(default_input_file if use_default_input_file else input_file)
    except FileNotFoundError:
        lines = read_lines(default_input_file)

    L = parse_input(lines)

    logging.info("*** PART 1 ***")
    part1(L)
    logging.info("*** PART 2 ***")
    part2(L)