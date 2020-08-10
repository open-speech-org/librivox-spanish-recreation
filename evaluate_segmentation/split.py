"""
Usage:

python evaluate_segmentation/split.py tokenized_text transformed_audios fixed_annotations evaluate_segmentation/tokenized_text evaluate_segmentation/transformed_audios evaluate_segmentation/fixed_annotations 100
"""
import os
import shutil
import sys

import logging

import random

LOGGER = logging.getLogger(__name__)


def split_manually(
        tokenized_folder,
        wav_folder,
        annotations_folder,
        output_folder,
        wav_output_folder,
        output_annotations_folder,
        threshold,
        num_corpus=5,
        folder_prefix="sub_corpus_{}"
):
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
        wav_folder_name = os.path.join(wav_output_folder, folder_prefix.format(corpus))
        annotations_folder_name = os.path.join(output_annotations_folder, folder_prefix.format(corpus))
        LOGGER.info("Writing corpus %s" % folder_name)
        os.makedirs(folder_name, exist_ok=True)
        os.makedirs(wav_folder_name, exist_ok=True)
        os.makedirs(annotations_folder_name, exist_ok=True)
        random_smaller_recordings = random.choices(list(smaller_than_threshold_recordings.keys()), k=15)
        LOGGER.info("Smaller chosen: %s" % ",".join(random_smaller_recordings))
        for smaller_name in random_smaller_recordings:
            with open(os.path.join(folder_name, smaller_name), "w+") as current_file:
                current_file.writelines(smaller_than_threshold_recordings[smaller_name])

            wav_name = smaller_name.replace(".txt", ".wav")
            original_wav_file_path = os.path.join(wav_folder, wav_name)
            if os.path.exists(original_wav_file_path):
                shutil.copy2(original_wav_file_path, os.path.join(wav_folder_name, wav_name))
            else:
                LOGGER.error("%s does not exists" % original_wav_file_path)

            annotations_name = smaller_name.replace(".txt", ".TextGrid")
            original_annotations_file_path = os.path.join(annotations_folder, annotations_name)
            if os.path.exists(original_annotations_file_path):
                shutil.copy2(original_annotations_file_path, os.path.join(annotations_folder_name, annotations_name))
            else:
                LOGGER.error("%s does not exists" % original_wav_file_path)

        random_larger_recordings = random.choices(list(larger_than_threshold_recordings.keys()), k=5)
        LOGGER.info("Larger chosen: %s" % ",".join(larger_than_threshold_recordings))
        for larger_name in random_larger_recordings:
            with open(os.path.join(folder_name, larger_name), "w+") as current_file:
                current_file.writelines(larger_than_threshold_recordings[larger_name])

            wav_name = larger_name.replace(".txt", ".wav")
            original_wav_file_path = os.path.join(wav_folder, wav_name)
            if os.path.exists(original_wav_file_path):
                shutil.copy2(original_wav_file_path, os.path.join(wav_folder_name, wav_name))
            else:
                LOGGER.error("%s does not exists" % original_wav_file_path)

            annotations_name = larger_name.replace(".txt", ".TextGrid")
            original_annotations_file_path = os.path.join(annotations_folder, annotations_name)
            if os.path.exists(original_annotations_file_path):
                shutil.copy2(original_annotations_file_path, os.path.join(annotations_folder_name, annotations_name))
            else:
                LOGGER.error("%s does not exists" % original_wav_file_path)


if __name__ == "__main__":
    if len(sys.argv) != 8:
        LOGGER.error("Only 7 arg accepted")
        exit(1)
    console_log = logging.StreamHandler()
    LOGGER.addHandler(console_log)
    LOGGER.setLevel(logging.DEBUG)
    split_manually(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
