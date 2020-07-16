import csv
import os
import sys

import logging

import requests

LOGGER = logging.getLogger(__name__)


def download_localized_audios(input_file_name, output_folder):
    if not input_file_name.endswith(".csv"):
        LOGGER.error("Only CSV file accepted")

    with open(input_file_name) as file:
        reader = csv.reader(file)
        # Skip header
        next(reader)
        for r in reader:
            file_name = os.path.join(output_folder, f"{r[0]}_1.mp3")
            if not os.path.exists(file_name):
                print("Downloading file", file_name)
                if r[6]:
                    with requests.get(r[6], stream=True) as response:
                        response.raise_for_status()
                        with open(file_name, "wb") as new_file:
                            for chunk in response.iter_content(chunk_size=8192):
                                new_file.write(chunk)
            else:
                print("Skipping file", file_name)


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        LOGGER.error("Only 3 arg accepted")
        exit(1)
    download_localized_audios(sys.argv[1], sys.argv[2])
