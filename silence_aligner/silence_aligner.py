"""
Usage:

python silence_aligner/silence_aligner.py original_text transformed_audios silence_aligner/silly_align F_08_1
python silence_aligner/silence_aligner.py original_text transformed_audios_cropped silence_aligner/cropped_align F_08_1
"""
import os
import re
import sys

import logging

import numpy as np
import textgrids

from scipy.io import wavfile

from openspeechlib.segmentation.silence_segmentation import (
    skip_adjacent_segmentator,
    silence_segmentation_for_energy_bins,
    transform_signal_into_energy_bins,
)
from openspeechlib.segmentation.dynamic_threshold import kmeans_first_and_last_second_minimum

# from scripts.tokenize_texts import sent_tokenize
def sent_tokenize(text):
    return [x for x in re.split("\.|,|;|:|\n|!|¿|¡|\?|-|—|\(|\)|«|»", text) if x.replace(" ", "")]

LOGGER = logging.getLogger(__name__)


CONSTANT_SIL = "sil"


def extract_segments_from_file(
        wav_file,
        threshold=0.05,
        calculate_threshold_dynamically=False,
        regularize_with=0
):
    window_width_size = 0.025
    windows_offset_size = 0.01
    frequency, signal = wavfile.read(wav_file)
    LOGGER.debug(f"Processing {wav_file}: frequency: {frequency}")
    if len(signal.shape) > 1:
        signal = signal[0]
    energy_bins = transform_signal_into_energy_bins(
        signal,
        frequency,
        window_width_size=window_width_size,
        windows_offset_size=windows_offset_size,
    )
    print(f"Desired threshold, {threshold}")
    if calculate_threshold_dynamically:
        calculated_threshold = kmeans_first_and_last_second_minimum(
            energy_bins,
            int(1/windows_offset_size),
            regularize_with=regularize_with
        )
        print(f"Calculated threshold, {calculated_threshold}")
    else:
        calculated_threshold = threshold
    return silence_segmentation_for_energy_bins(
        energy_bins,
        frequency,
        calculated_threshold,
        segmentator=skip_adjacent_segmentator,
    ), frequency


def evaluate_single_file(text_folder, wav_folder, results_folder, file_name):
    LOGGER.debug(f"Processing {file_name}")
    text = " ".join(open(os.path.join(text_folder, f"{file_name}.txt"), 'r').readlines())
    tokenized_text = sent_tokenize(text)
    tokenized_text = tokenized_text[1:]
    segments, audio_frequency = extract_segments_from_file(os.path.join(wav_folder, f"{file_name}.wav"))
    min_length = min(len(tokenized_text), len(segments))
    tg = textgrids.TextGrid()
    tg.xmin = 0
    tg.xmax = segments[-1][1] / audio_frequency
    tier = textgrids.Tier()
    tg[file_name] = tier
    previous_segment = 0
    for i in range(min_length):
        xmin, xmax = segments[i]
        tier.append(
            textgrids.Interval(
                tokenized_text[i],
                previous_segment / audio_frequency,
                xmin / audio_frequency
            )
        )
        previous_segment = xmax
    tg.write(os.path.join(results_folder, f"silence_aligned_{file_name}.TextGrid"))


def evaluate_folder(text_folder, wav_folder, results_folder):

    for file_name in os.listdir(text_folder):
        try:
            evaluate_single_file(text_folder, wav_folder, results_folder, file_name.replace(".txt", ""))
        except FileNotFoundError as e:
            LOGGER.error(e)


if __name__ == "__main__":
    console_log = logging.StreamHandler()
    LOGGER.addHandler(console_log)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.info(sys.argv)
    if len(sys.argv) == 5:
        LOGGER.info("Evaluating for single file")
        evaluate_single_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        exit(0)
    if len(sys.argv) != 4:
        LOGGER.error("Only 3 arg accepted")
        exit(1)

    evaluate_folder(sys.argv[1], sys.argv[2], sys.argv[3])
