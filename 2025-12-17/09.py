import logging
from tools import read_lines
from shapely.geometry import Polygon

input_file = "my_input09.txt"
default_input_file = "input09.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

use_default_input_file = False

def rectangle_area(x1, y1, x2, y2):
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

def rectangle_coordinates(x1, y1, x2, y2):
    # given two edges of a rectangle, calculate the other two:
    return [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]

if __name__ == '__main__':
    try:
        lines = read_lines(default_input_file if use_default_input_file else input_file)
    except FileNotFoundError:
        lines = read_lines(default_input_file)

    input_data = [[int(x) for x in y.split(",")] for y in lines]

    # part 1
    # calculate all rectangle ares:
    rectangle_areas = {}
    max_rectangle_area = 0
    for i in range(len(input_data)):
        for j in range(i+1,len(input_data)):
            rectangle_areas[i,j] = rectangle_area(*input_data[i],*input_data[j])
            if rectangle_areas[i,j] > max_rectangle_area:
                max_rectangle_area = rectangle_areas[i,j]

    logging.info(f"Part 1: largest rectangle area: {max_rectangle_area}")

    # part 2
    # the polygon of red&green tiles:
    p = Polygon(input_data)
    # loop through the rectangles in descending order (ordered by their size):
    i = 0
    for key, value in sorted(rectangle_areas.items(), key=lambda item: item[1], reverse=True):
        # test if this rectangle consists only of red/green tiles:
        i += 1
        if i % 100 == 0:
            logging.info(f"Part 2: testing rectangle #{i}")
        q = Polygon(rectangle_coordinates(*input_data[key[0]], *input_data[key[1]]))
        if p.contains(q):
            logging.info(f"Part 2: largest rectangle area that consists entirely of red/green tiles: {value}")
            break