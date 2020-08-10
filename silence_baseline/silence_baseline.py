"""
Usage:

python silence_baseline/silence_baseline.py fixed_annotations automatic_segmentation/segmentation silence_baseline/results F_08_1.TextGrid
"""
import os
import sys

import logging

import numpy as np
import textgrids


LOGGER = logging.getLogger(__name__)


CONSTANT_SIL = "sil"


def evaluate_single_file(manual_folder, automatic_folder, results_folder, file_name):
    LOGGER.debug(f"Processing {file_name}")
    manual_file = textgrids.TextGrid(os.path.join(manual_folder, file_name))
    automatic_file = textgrids.TextGrid(os.path.join(automatic_folder, f"automatic_{file_name}"))
    base_name = file_name.replace(".TextGrid", "")
    manual_intervals = manual_file[base_name]
    automatic_intervals = automatic_file[base_name]

    silences_out = 0
    silence_only_in_automatic = 0
    silence_in_both = 0
    total_automatic_silences = 0
    total_spoken_segments = 0
    manual_iterator = iter(manual_intervals)
    current_manual_interval = next(manual_iterator)
    for automatic_interval in automatic_intervals:
        if not automatic_interval.text:
            continue

        if automatic_interval.text.strip() == CONSTANT_SIL:
            if automatic_interval.xmin > current_manual_interval.xmax:
                current_manual_interval = next(manual_iterator)

            total_automatic_silences += 1
            if automatic_interval.xmin < current_manual_interval.xmax < automatic_interval.xmax:
                silence_in_both += 1
                current_manual_interval = next(manual_iterator)
                if current_manual_interval.text.strip():
                    total_spoken_segments += 1
            else:
                if not current_manual_interval.text.strip():
                    silences_out += 1
                else:
                    silence_only_in_automatic += 1
            if current_manual_interval.xmax < automatic_interval.xmax:
                current_manual_interval = next(manual_iterator)
                if current_manual_interval.text.strip():
                    total_spoken_segments += 1
    results = f"""Results
silences_out = {silences_out}
silence_only_in_automatic = {silence_only_in_automatic}  # False Positives
silence_in_both = {silence_in_both}  # True Positives
excluded_silences = {total_spoken_segments - silence_in_both}  # False negatives
total_automatic_silences = {total_automatic_silences}
total_spoken_segments = {total_spoken_segments}
(silence_in_both / total_spoken_segments) * 100 = {(silence_in_both / (total_spoken_segments or 1)) * 100 }
"""
    results_file = open(os.path.join(results_folder, f"{base_name}.results"), "w+")
    results_file.write(results)
    results_file.close()

    return silences_out, silence_only_in_automatic, silence_in_both, total_automatic_silences, total_spoken_segments


def evaluate_folder(manual_folder, automatic_folder, results_folder):
    total_silences_out = 0
    total_silence_only_in_automatic = 0
    total_silence_in_both = 0
    total_total_automatic_silences = 0
    total_total_spoken_segments = 0
    precisions = list()
    for file_name in os.listdir(manual_folder):
        try:
            silences_out, silence_only_in_automatic, silence_in_both, total_automatic_silences, total_spoken_segments = evaluate_single_file(manual_folder, automatic_folder, results_folder, file_name)
            if sum((silences_out, silence_only_in_automatic, silence_in_both, total_automatic_silences, total_spoken_segments)) > 0:
                total_silences_out += silences_out
                total_silence_only_in_automatic += silence_only_in_automatic
                total_silence_in_both += silence_in_both
                total_total_automatic_silences += total_automatic_silences
                total_total_spoken_segments += total_spoken_segments
                precisions.append((silence_in_both / (total_spoken_segments or 1)) * 100)
        except FileNotFoundError as e:
            LOGGER.error(e)
    results = f"""Results
silences_out = {total_silences_out}
silence_only_in_automatic = {total_silence_only_in_automatic}
silence_in_both = {total_silence_in_both}
total_automatic_silences = {total_total_automatic_silences}
total_spoken_segments = {total_total_spoken_segments}
(silence_in_both / total_spoken_segments) * 100 = {(total_silence_in_both / total_total_spoken_segments) * 100} 
    """
    results_file = open(os.path.join(results_folder, f"global.results"), "w+")
    results_file.write(results)
    results_file.close()

    np.savetxt(os.path.join(results_folder, "precisions.txt"), np.asarray(precisions), delimiter=",")



if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 5:
        evaluate_single_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        exit(0)
    if len(sys.argv) != 4:
        LOGGER.error("Only 3 arg accepted")
        exit(1)
    console_log = logging.StreamHandler()
    LOGGER.addHandler(console_log)
    LOGGER.setLevel(logging.DEBUG)
    evaluate_folder(sys.argv[1], sys.argv[2], sys.argv[3])
