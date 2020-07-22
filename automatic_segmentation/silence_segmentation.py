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



def create_automatic_segmentation(wav_folder, output_folder):

    for wav_file in os.listdir(wav_folder):
        frequency, signal = wavfile.read(os.path.join(wav_folder, wav_file))
        LOGGER.debug(f"Processing {wav_file}: frequency: {frequency}")
        segmentation = silence_segmentation.silence_segmentation(signal, frequency)



if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        LOGGER.error("Only 2 arg accepted")
        exit(1)
    create_automatic_segmentation(sys.argv[1], sys.argv[2])
