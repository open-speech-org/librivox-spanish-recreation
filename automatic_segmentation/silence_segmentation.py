"""
Usage:

python automatic_segmentation/silence_segmentation.py transformed_audios automatic_segmentation/segmentation
"""
import os
import sys

import logging

import numpy as np
from scipy.io import wavfile
import textgrids
from openspeechlib.segmentation.silence_segmentation import (
    skip_adjacent_segmentator,
    silence_segmentation_for_energy_bins,
    transform_signal_into_energy_bins,
)
from openspeechlib.segmentation.dynamic_threshold import kmeans_first_and_last_second_minimum


LOGGER = logging.getLogger(__name__)


def write_text_grid_from_segmentation(segmentation, text_name, output_folder, xmin=0, xmax=0, audio_frequency=16000):
    tg = textgrids.TextGrid()
    tg.xmin = xmin
    tg.xmax = xmax
    tier = textgrids.Tier()
    tg[text_name] = tier
    previous_segment = 0
    print(f"tokens: {len(segmentation)}")
    for xmin, xmax in segmentation:
        tier.append(
            textgrids.Interval(
                "",
                previous_segment / audio_frequency,
                xmin / audio_frequency
            )
        )
        tier.append(
            textgrids.Interval(
                "sil",
                xmin/audio_frequency,
                xmax/audio_frequency
            )
        )
        previous_segment = xmax
    tg.write(os.path.join(output_folder, f"automatic_{text_name}.TextGrid"))


def evaluate_for_single_file(
        wav_folder,
        output_folder,
        wav_file,
        threshold,
        calculate_threshold_dynamically,
        regularize_with=0
):
    window_width_size = 0.025
    windows_offset_size = 0.01
    frequency, signal = wavfile.read(os.path.join(wav_folder, wav_file))
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
        threshold = kmeans_first_and_last_second_minimum(
            energy_bins,
            int(1/windows_offset_size),
            regularize_with=regularize_with
        )
        print(f"Calculated threshold, {threshold}")
    segmentation = silence_segmentation_for_energy_bins(
        energy_bins,
        frequency,
        threshold,
        segmentator=skip_adjacent_segmentator,
    )
    write_text_grid_from_segmentation(
        segmentation,
        wav_file.replace(".wav", ""),
        output_folder,
        xmax=signal.shape[-1] / frequency,
        audio_frequency=frequency
    )
    return segmentation, threshold


def create_automatic_segmentation(wav_folder, output_folder, threshold_param=0.15):
    calculate_threshold_dynamically = False
    thresholds = list()
    if threshold_param == "dynamic":
        LOGGER.info("dynamic using as parameter for threshold")
        threshold = 0.15
        calculate_threshold_dynamically = True
    else:
        try:
            threshold = float(threshold_param)
        except:
            LOGGER.error("Cannot transform threshold into value %s" % threshold_param)
            LOGGER.error("Using default 0.15")
            threshold = 0.15

    for wav_file in os.listdir(wav_folder):
        try:
            segmentation, threshold = evaluate_for_single_file(
                wav_folder,
                output_folder,
                wav_file,
                threshold,
                calculate_threshold_dynamically
            )
            thresholds.append(threshold)

        except ValueError as e:
            LOGGER.error(e)
    if calculate_threshold_dynamically:
        np.savetxt(os.path.join(output_folder, "thresholds.txt"), np.asarray(thresholds), delimiter=",")


if __name__ == "__main__":
    if len(sys.argv) == 5:
        evaluate_for_single_file(sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[3], True,)
        exit(0)
    if len(sys.argv) != 4:
        LOGGER.error("Only 3 arg accepted")
        exit(1)
    console_log = logging.StreamHandler()
    LOGGER.addHandler(console_log)
    LOGGER.setLevel(logging.DEBUG)
    create_automatic_segmentation(sys.argv[1], sys.argv[2], sys.argv[3])
