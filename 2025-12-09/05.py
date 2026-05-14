import logging
from tools import read_lines

input_file = "my_input05.txt"
default_input_file = "input05.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

use_default_input_file = False

class Intervals:
    data = []
    def __init__(self, start, end):
        assert start <= end
        self.data = [[start, end]]

    def count(self):
        return sum([x[1]-x[0]+1 for x in self.data])

    def substract(self, start, end):
        """
        Substract the interval [start, end] from the set of integers
        represented in this instance of class Intervals.
        """
        data_new = []
        for [a,b] in self.data:
            # Is [a,b] contained in [start,end]?
            if a > start and b < end:
                logging.debug("contained")
                continue
            # Do [a,b] and [start, end] intersect at all?
            if b < start or a > end:
                # no.
                logging.debug("no intersection")
                data_new += [[a,b]]
                continue
            # Does [a, b] - [start, end] consist of a single interval?
            if (start <= a) and (end <= b):
                logging.debug("single interval in result (right)")
                data_new += [[end+1, b]]
                continue
            if (a <= start) and (b <= end):
                logging.debug("single interval in result (left)")
                data_new += [[a, start-1]]
                continue
            # Otherwise, [start, end] is contained in [a,b], so [a, b] - [start, end] is two disjoint intervals:
            logging.debug("two intervals in result")
            data_new += [[a, start-1], [end+1, b]]
        self.data = data_new

if __name__ == '__main__':
    try:
        lines = read_lines(default_input_file if use_default_input_file else input_file)
    except FileNotFoundError:
        lines = read_lines(default_input_file)
    logging.info(f"Input file: {len(lines)} lines")


    # part 1+2: fresh ID ranges
    i = 0
    fresh = []
    while True:
        line = lines[i]
        i+=1
        x, y = line.split("-")
        fresh += [[int(x), int(y)]]
        if lines[i] == "":
            break

    # part 2: number of distinct integers in fresh ID ranges
    integers_in_fresh_ranges = 0
    for j in range(len(fresh)):
        [x, y] = fresh[j]
        c = Intervals(x, y)
        for k in range(j):
            c.substract(fresh[k][0], fresh[k][1])
        integers_in_fresh_ranges += c.count()

    logging.info(f"Part 2: {integers_in_fresh_ranges} distinct integers in fresh ranges")

    # part 1
    i += 1
    num_fresh = 0
    while i < len(lines):
        k = int(lines[i])
        if len([a for a in fresh if a[0] <= k <= a[1]]) > 0:
            num_fresh += 1
        i += 1

    logging.info(f"Part 1: {num_fresh} fresh items")

