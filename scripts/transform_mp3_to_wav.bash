#!/bin/bash

MP3_FOLDER=$1
WAV_FOLDER=$2



for i in $MP3_FOLDER/*.mp3
do
  echo "Transforming $i"
  sox "$i" "$WAV_FOLDER/$(basename -s .mp3 "$i").wav"
done
