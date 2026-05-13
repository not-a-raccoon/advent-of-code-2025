import logging
from tools import read_lines

input_file = "my_input01.txt"
default_input_file = "input01.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

use_default_input_file = False

if __name__ == '__main__':
    # read input; "L"=left rotation, "R"=right rotation, start at position 50
    position = 50
    num_clicks = 0
    count = 0
    try:
        lines = read_lines(default_input_file if use_default_input_file else input_file)
    except FileNotFoundError:
        lines = read_lines(default_input_file)

    input_commands = [int(x.replace('L', '-').replace('R','')) for x in  lines]
    logging.info("Input file: {}".format(input_commands))
    for i in range(len(input_commands)):
        logging.info(f"Input #{i}: {input_commands[i]}")
        # part 2:
        logging.debug(f"position: {position}, input: {input_commands[i]}")
        num_clicks += abs(input_commands[i]) // 100
        logging.debug(f"adding {abs(input_commands[i]) // 100} clicks")
        if position != 0 and input_commands[i] < 0 and (position + ((input_commands[i]) % 100)-100) <= 0:
            num_clicks += 1
            logging.debug("extra click (negative)")
        elif input_commands[i] > 0 and (input_commands[i] % 100) + position >= 100:
            num_clicks += 1
            logging.debug("extra click (positive)")

        # part 1:
        position += input_commands[i]
        position %= 100
        if position % 100 == 0:
            count += 1

    logging.info("Count: {}".format(count))
    logging.info("Number of clicks: {}".format(num_clicks))


