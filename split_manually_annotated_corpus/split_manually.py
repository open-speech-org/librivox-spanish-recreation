"""
Usage:

python split_manually_annotated_corpus/split_manually.py tokenized_text split_manually_annotated_corpus/split 100
"""
import os
import sys

import logging

import random

LOGGER = logging.getLogger(__name__)


def split_manually(tokenized_folder, output_folder, threshold, num_corpus=5, folder_prefix="sub_corpus_{}"):
    larger_than_threshold_recordings = dict()
    smaller_than_threshold_recordings = dict()
    for annotation_file in os.listdir(tokenized_folder):
        with open(os.path.join(tokenized_folder, annotation_file)) as current_file:
            lines = current_file.readlines()
        if len(lines) > int(threshold):
            larger_than_threshold_recordings[annotation_file] = lines
        else:
            smaller_than_threshold_recordings[annotation_file] = lines

    print(len(larger_than_threshold_recordings))
    print(len(smaller_than_threshold_recordings))
    for corpus in range(num_corpus):
        folder_name = os.path.join(output_folder, folder_prefix.format(corpus))
        LOGGER.info("Writing corpus %s" % folder_name)
        os.makedirs(folder_name, exist_ok=True)
        random_smaller_recordings = random.choices(list(smaller_than_threshold_recordings.keys()), k=15)
        LOGGER.info("Smaller chosen: %s" % ",".join(random_smaller_recordings))
        for smaller_name in random_smaller_recordings:
            with open(os.path.join(folder_name, smaller_name), "w+") as current_file:
                current_file.writelines(smaller_than_threshold_recordings[smaller_name])
        random_larger_recordings = random.choices(list(larger_than_threshold_recordings.keys()), k=5)
        LOGGER.info("Larger chosen: %s" % ",".join(random_smaller_recordings))
        for larger_name in random_larger_recordings:
            with open(os.path.join(folder_name, larger_name), "w+") as current_file:
                current_file.writelines(larger_than_threshold_recordings[larger_name])




if __name__ == "__main__":
    if len(sys.argv) != 4:
        LOGGER.error("Only 3 arg accepted")
        exit(1)
    console_log = logging.StreamHandler()
    LOGGER.addHandler(console_log)
    LOGGER.setLevel(logging.DEBUG)
    split_manually(sys.argv[1], sys.argv[2], sys.argv[3])
