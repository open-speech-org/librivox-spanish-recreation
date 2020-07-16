# LibriVox Spanish Recreation

This repository contains information related to the Speech Corpus [LibriVox Spanish](https://catalog.ldc.upenn.edu/LDC2020S01) created by [CIEMPIESS](http://www.ciempiess.org/about), including a mapping between the manually annotated resources and its original source in [LibriVox](https://librivox.org/), also some manual annotations using point symbols

## Process

### Corpus information

First we extract all information from files/Speaker_Info.xls in the LibriVox Spanish corpus into 
[corpus_info/corpus_info.csv](corpus_info/corpus_info.csv)

Then we created a copy of corpus_info as [corpus_info/corpus_info_formatted.csv](corpus_info/corpus_info_formatted.csv) 
which includes an additional column for  total_seconds using [scripts/transform_time_column.py](scripts/transform_time_column.py) 

After we sort that file using the newly created column  total_seconds and store the content into the file 
[corpus_info/corpus_info_formatted_sorted.csv](corpus_info/corpus_info_formatted_sorted.csv) using the [scripts/sort_by_time_column.py](scripts/sort_by_time_column.py)

Manually we add new columns for useful information as chapter_name, librivox_book_url, audio_url, text_url and speaker_url

### Data preparation

#### Texts

We manually downloaded the text using the reference in the column text_url from [corpus_info/corpus_info_formatted_sorted.csv](corpus_info/corpus_info_formatted_sorted.csv)

Also we performed a first manual cleaning, putting the title in the first line and delimiting using a period.

All those files are stored in [original_text](original_text)

We tried an automatic tokenization using nltk in the scripts [scripts/download_nltk_data.py](scripts/download_nltk_data.py) 
and [scripts/tokenize_texts_nltk.py](scripts/tokenize_texts_nltk.py), however the tokenization didn't uses special characters 
as `? ; !` and others leaving a too broad segmentation. For that reason we implement our custom splitter defined in [scripts/tokenize_texts.py](scripts/tokenize_texts.py)
which uses the following expression to tokenize the texts `[x for x in re.split("\.|,|;|:|\n|!|¿|¡|\?|-|—\(|\)", text) if x.replace(" ", "")]`

All tokenized text are stored in [tokenized_text](tokenized_text) folder and each file has a format `number: text`. This
number will be used as a sentence identifier in the following annotation process.


#### Audios

We use [scripts/download_localized_audios.py](scripts/download_localized_audios.py) to download the files from the audio_url
column in [corpus_info/corpus_info_formatted_sorted.csv](corpus_info/corpus_info_formatted_sorted.csv)

And we transform all audios using [sox](http://sox.sourceforge.net/) and [scripts/transform_mp3_to_wav.bash](scripts/transform_mp3_to_wav.bash)



## Troubleshooting

Before execute any code make sure you have python 3.6+ installed and a virtual environment

```bash
python -m venv librivox_spanish_recreation_env
source librivox_spanish_recreation_env
pip install requirements.txt
```

To install sox, check your software package manager. If using ubuntu

```bash
sudo apt install sox
sudo apt install libsox-fmt-mp3
```
