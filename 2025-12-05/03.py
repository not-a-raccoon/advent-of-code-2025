import logging
from tools import read_lines

input_file = "my_input03.txt"
default_input_file = "input03.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

use_default_input_file = False

def solve(s: str, N: int) -> int:
    assert (len(s) >= N) and (N >= 2)
    result = ""
    last_pos=0
    for k in range(N):
        idx = max(range(last_pos,len(s)-N+k+1), key=s.__getitem__)
        result += s[idx]
        last_pos = idx+1
    return int(result)

if __name__ == '__main__':
    try:
        lines = read_lines(default_input_file if use_default_input_file else input_file)
    except FileNotFoundError:
        lines = read_lines(default_input_file)
    logging.info(f"Input file: {len(lines)} lines")

    sum_part1 = 0
    sum_part2 = 0
    for l in lines:
        logging.debug(f"Input: {l}")
        a = solve(l, 2)
        sum_part1 += a
        logging.debug(f"Output for part 1: {a}")
        a = solve(l, 12)
        sum_part2 += a
        logging.debug(f"Output for part 2: {a}")

    logging.info(f"Part 1: {sum_part1}")
    logging.info(f"Part 2: {sum_part2}")