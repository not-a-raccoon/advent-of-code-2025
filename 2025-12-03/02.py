import logging
from tools import read_csv

input_file = "my_input02.txt"
default_input_file = "input02.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

use_default_input_file = False

def find_invalid_ids(from_id, to_id, divisors):
    found = 0
    sum_found_ids = 0
    found_part1 = 0
    sum_found_ids_part1 = 0
    for i in range(max(from_id, 10), to_id+1):
        for d in divisors[len(str(i))]:
            s = str(i)
            t = s[:len(s)//d]
            if s == d*t:
                found += 1
                sum_found_ids += i
                if d == 2:
                    # part 1
                    found_part1 += 1
                    sum_found_ids_part1 += i

                logging.debug(f"Found invalid id for divisor {d}: {i}")
                # count each invalid id only one:
                break
    return found_part1, sum_found_ids_part1, found, sum_found_ids




if __name__ == '__main__':
    try:
        lines = read_csv(default_input_file if use_default_input_file else input_file, ',')
    except FileNotFoundError:
        lines = read_csv(default_input_file, ',')
    lines = lines[0]
    logging.info(f"Input file: {len(lines)} ranges given")

    # for part 2:
    max_number = max([max({int(r.split("-")[0]), int(r.split("-")[1])}) for r in lines])
    logging.info(f"Max number: {max_number}")
    divisors = {j: [k for k in range(2, j+1) if j % k == 0] for j in range(1, len(str(max_number))+1)}
    logging.info(f"Divisors: {divisors}")

    found = 0
    sum_found_ids = 0
    found_part1 = 0
    sum_found_ids_part1 = 0
    for r in lines:
        range_from = int(r.split("-")[0])
        range_to = int(r.split("-")[1])
        logging.info(f"Range from {range_from} to {range_to}")
        f1, s1, f, s = find_invalid_ids(range_from, range_to, divisors)
        found_part1 += f1
        sum_found_ids_part1 += s1
        found += f
        sum_found_ids += s
    logging.info(f"Part 1: Found {found_part1} invalid ids, their sum is: {sum_found_ids_part1}")
    logging.info(f"Part 2: Found {found} invalid ids, their sum is: {sum_found_ids}")
