import csv
import sys

import logging

LOGGER = logging.getLogger(__name__)


def parse_time(input_file):
    pass


if __name__ == "__main__":
    if len(sys.argv != 2):
        LOGGER.error("Only 1 arg accepted")
        exit(1)
