import sys
import os

import logging

from nltk.tokenize import sent_tokenize

LOGGER = logging.getLogger(__name__)


def create_text_files(text_folder, output_folder):

    for text_file in os.listdir(text_folder):
        with open(os.path.join(text_folder, text_file)) as file:
            print("Processing", text_file)
            text = " ".join(file.readlines())
            text = text.replace("\n", " ")
            tokenized_text = sent_tokenize(text, language="spanish")
            new_lines = list()
            for index, sentence in enumerate(tokenized_text):
                new_lines.append(f"{index}:{sentence}\n")
            new_file_path = os.path.join(output_folder, text_file)
            output_file = open(new_file_path, "w+")
            output_file.writelines(new_lines)
            output_file.close()


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        LOGGER.error("Only 2 arg accepted")
        exit(1)
    create_text_files(sys.argv[1], sys.argv[2])
