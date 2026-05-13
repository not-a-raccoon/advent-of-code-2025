import csv
import logging


def read_csv(file_path, delimiter=','):
    """
    Read a csv file and return a list of lines.
    :param file_path:
    :param delimiter:
    :return:
    """
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            return list(reader)
    except FileNotFoundError:
        logging.error('File not found')

def read_lines(file_path):
    """
    Read a text file and return a list of lines.
    :param file_path:
    :return:
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        logging.error('File not found')
        raise