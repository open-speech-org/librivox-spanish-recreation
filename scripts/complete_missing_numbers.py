"""
Usage:

python complete_missing_numbers.py annotations fixed_annotations
"""

import os
import sys

import logging

import textgrids

LOGGER = logging.getLogger(__name__)


def complete_missing_numbers(text_folder, output_folder):

    for text_file in sorted(os.listdir(text_folder)):
        current_annotation = textgrids.TextGrid(os.path.join(text_folder, text_file))
        transcription_name = text_file.replace(".TextGrid", "")
        intervals = current_annotation[transcription_name]
        LOGGER.info(f"Analyzing {text_file}")
        LOGGER.info(f"-------------------")
        current_index = None
        last_manually_annotated_index = None
        first_index_found = False
        for interval in intervals:
            try:
                last_manually_annotated_index = int(interval.text)
                LOGGER.info(f"Manually annotated_index found: {last_manually_annotated_index}")
                if current_index and last_manually_annotated_index != current_index + 1:
                    LOGGER.error(f"Consistency problem at {last_manually_annotated_index}")
                current_index = last_manually_annotated_index
                first_index_found = True
            except ValueError:
                LOGGER.debug(f"Value error with {interval.text}")
                if isinstance(current_index, int):
                    LOGGER.debug(f"Current index {current_index} {type(current_index)}")
                    current_index = current_index + 1
            if first_index_found:
                LOGGER.debug(f"Writing {current_index}")
                interval.text = textgrids.Transcript(str(current_index))

        current_annotation.write(os.path.join(output_folder, text_file))


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        LOGGER.error("Only 2 arg accepted")
        exit(1)
    log = logging.FileHandler("automatic_filling.log")
    log.setLevel(logging.INFO)
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)
    LOGGER.addHandler(log)
    LOGGER.addHandler(console_log)
    LOGGER.setLevel(logging.DEBUG)
    complete_missing_numbers(sys.argv[1], sys.argv[2])
