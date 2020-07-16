import csv
import sys

import logging

LOGGER = logging.getLogger(__name__)


def parse_time(input_file_name):
    if not input_file_name.endswith(".csv"):
        LOGGER.error("Only CSV file accepted")

    new_lines = list()
    with open(input_file_name) as file:
        reader = csv.reader(file)
        new_lines.append(",".join(next(reader) + ["total_seconds"])+"\n")
        for r in reader:
            only_digits = r[1].replace("h", "").replace("m", "").replace("s", "").split(":")
            new_lines.append(
                ",".join(
                    r + [
                        str(
                            int(only_digits[0]) * 3600 +
                            int(only_digits[1]) * 60 +
                            int(only_digits[2]))
                    ]
                ) + "\n"
            )

    output_file_name = f"{'.'.join(input_file_name.split('.')[:-1])}_formatted.csv"
    output_file = open(output_file_name, "w+")
    output_file.writelines(new_lines)
    output_file.close()


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 2:
        LOGGER.error("Only 1 arg accepted")
        exit(1)
    parse_time(sys.argv[1])
