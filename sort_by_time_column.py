import csv
import sys

import logging

LOGGER = logging.getLogger(__name__)


def sort_by_time(input_file_name):
    if not input_file_name.endswith(".csv"):
        LOGGER.error("Only CSV file accepted")

    new_lines = list()
    with open(input_file_name) as file:
        reader = csv.reader(file)
        new_lines.append(",".join(next(reader) + ["total_seconds"])+"\n")
        lines = list(reader)
        sorted_lines = sorted(lines, key=lambda x: int(x[7]))
        new_lines.extend("\n".join(map(lambda x: ",".join(x), sorted_lines)))
    output_file_name = f"{'.'.join(input_file_name.split('.')[:-1])}_sorted.csv"
    output_file = open(output_file_name, "w+")
    output_file.writelines(new_lines)
    output_file.close()


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 2:
        LOGGER.error("Only 1 arg accepted")
        exit(1)
    sort_by_time(sys.argv[1])
