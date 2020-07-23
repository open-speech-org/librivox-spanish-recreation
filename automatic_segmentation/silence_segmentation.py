"""
Usage:

python automatic_segmentation/silence_segmentation.py transformed_audios automatic_segmentation/segmentation
"""
import os
import sys

import logging

from scipy.io import wavfile
import textgrids
from openspeechlib.segmentation import silence_segmentation


LOGGER = logging.getLogger(__name__)


def write_text_grid_from_segmentation(segmentation, text_name, output_folder, xmin=0, xmax=0, audio_frequency=16000):
    tg = textgrids.TextGrid()
    tg.xmin = xmin
    tg.xmax = xmax
    tier = textgrids.Tier()
    tg[text_name] = tier
    for xmin, xmax in segmentation:
        tier.append(
            textgrids.Interval(
                "",
                xmin/audio_frequency,
                xmax/audio_frequency
            )
        )
    tg.write(os.path.join(output_folder, f"automatic_{text_name}.TextGrid"))


def evaluate_for_single_file(wav_folder, output_folder, wav_file):
    frequency, signal = wavfile.read(os.path.join(wav_folder, wav_file))
    LOGGER.debug(f"Processing {wav_file}: frequency: {frequency}")
    segmentation = silence_segmentation.silence_segmentation(signal, frequency, 0.15)
    write_text_grid_from_segmentation(
        segmentation,
        wav_file.replace(".wav", ""),
        output_folder,
        xmax=signal.shape[-1] / frequency,
        audio_frequency=frequency
    )


def create_automatic_segmentation(wav_folder, output_folder):

    for wav_file in os.listdir(wav_folder):
        evaluate_for_single_file(wav_folder, output_folder, wav_file)
        break


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 4:
        evaluate_for_single_file(sys.argv[1], sys.argv[2], sys.argv[3])
        exit(0)
    if len(sys.argv) != 3:
        LOGGER.error("Only 2 arg accepted")
        exit(1)
    create_automatic_segmentation(sys.argv[1], sys.argv[2])
