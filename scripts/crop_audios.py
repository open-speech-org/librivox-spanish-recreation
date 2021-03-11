"""
python scripts/crop_audios.py transformed_audios fixed_annotations transformed_audios_cropped
"""
import logging

import os
import sys

from scipy.io import wavfile
import textgrids

LOGGER = logging.getLogger(__name__)


def create_text_files(wav_folder, transcription_folder, output_folder):
    for wav_file in os.listdir(wav_folder):
        try:
            file_name = wav_file.replace(".wav", "")
            LOGGER.info(f"Processing {file_name}")
            frequency, signal = wavfile.read(os.path.join(wav_folder, f"{file_name}.wav"))
            text_grid = textgrids.TextGrid(os.path.join(transcription_folder, f"{file_name}.TextGrid"))
            intervals = text_grid[file_name]
            initial_second = -1
            end_second = signal.shape[-1] / frequency
            for interval in intervals:
                if interval.text == "1":
                    initial_second = interval.xmin
                if interval.text == "" and initial_second > -1:
                    end_second = interval.xmax
                    break
            cropped_signal = signal[int(initial_second * frequency):int(end_second * frequency)]
            output_path = os.path.join(output_folder, f"cropped_{file_name}.wav")
            LOGGER.info(f"Saving cropped file in {output_path}")
            wavfile.write(output_path, frequency, cropped_signal)

        except FileNotFoundError:
            LOGGER.error(f"File not found {file_name}")

if __name__ == "__main__":
    console_log = logging.StreamHandler()
    LOGGER.addHandler(console_log)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.info(sys.argv)
    if len(sys.argv) != 4:
        LOGGER.error("Only 3 arg accepted")
        exit(1)
    create_text_files(sys.argv[1], sys.argv[2], sys.argv[3])
