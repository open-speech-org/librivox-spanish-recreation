import csv
import sys
import os

import logging

LOGGER = logging.getLogger(__name__)


def create_text_files(input_file_name, folder):
    if not input_file_name.endswith(".csv"):
        LOGGER.error("Only CSV file accepted")

    new_lines = list()
    with open(input_file_name) as file:
        reader = csv.reader(file)
        new_lines.append(",".join(next(reader) + ["total_seconds"])+"\n")
        for r in reader:
            if r[5]:
                print("Creating file", r[0])
                output_file_name = f"{r[0]}_1.txt"
                output_file = open(os.path.join(folder, output_file_name), "w+")
                output_file.close()


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        LOGGER.error("Only 2 arg accepted")
        exit(1)
    create_text_files(sys.argv[1], sys.argv[2])
