# Initialize
mkdir -p evaluate_segmentation/silence_baseline evaluate_segmentation/fixed_annotations evaluate_segmentation/transformed_audios evaluate_segmentation/tokenized_text

# Run split
python evaluate_segmentation/split.py tokenized_text transformed_audios fixed_annotations evaluate_segmentation/tokenized_text evaluate_segmentation/transformed_audios evaluate_segmentation/fixed_annotations 100

# Annotate using fixed threshold
THRESHOLD=0.05
mkdir -p evaluate_segmentation/silence_baseline/sub_corpus_{0..4}/segmentation_${THRESHOLD}

for i in {0..4}
do
  echo python automatic_segmentation/silence_segmentation.py evaluate_segmentation/transformed_audios/sub_corpus_${i} evaluate_segmentation/silence_baseline/sub_corpus_${i}/segmentation_${THRESHOLD} ${THRESHOLD}
  # python automatic_segmentation/silence_segmentation.py evaluate_segmentation/transformed_audios/sub_corpus_${i} evaluate_segmentation/silence_baseline/sub_corpus_${i}/segmentation_${THRESHOLD} ${THRESHOLD}
done

mkdir -p evaluate_segmentation/silence_baseline/sub_corpus_{0..4}/results_${THRESHOLD}

for i in {0..4}
do
  echo python silence_baseline/silence_baseline.py evaluate_segmentation/fixed_annotations/sub_corpus_${i} evaluate_segmentation/silence_baseline/sub_corpus_${i}/segmentation_${THRESHOLD} evaluate_segmentation/silence_baseline/sub_corpus_${i}/results_${THRESHOLD}
done


# Annotate using dynamic
THRESHOLD=dynamic

mkdir -p evaluate_segmentation/silence_baseline/sub_corpus_{0..4}/segmentation_${THRESHOLD}

for i in {0..4}
do
  echo python automatic_segmentation/silence_segmentation.py evaluate_segmentation/transformed_audios/sub_corpus_${i} evaluate_segmentation/silence_baseline/sub_corpus_${i}/segmentation_${THRESHOLD} ${THRESHOLD}
  # python automatic_segmentation/silence_segmentation.py evaluate_segmentation/transformed_audios/sub_corpus_${i} evaluate_segmentation/silence_baseline/sub_corpus_${i}/segmentation_${THRESHOLD} ${THRESHOLD}
done

mkdir -p evaluate_segmentation/silence_baseline/sub_corpus_{0..4}/results_${THRESHOLD}

for i in {0..4}
do
  echo python silence_baseline/silence_baseline.py evaluate_segmentation/fixed_annotations/sub_corpus_${i} evaluate_segmentation/silence_baseline/sub_corpus_${i}/segmentation_${THRESHOLD} evaluate_segmentation/silence_baseline/sub_corpus_${i}/results_${THRESHOLD}
done


# Clean
rm -rf evaluate_segmentation/silence_baseline/* evaluate_segmentation/fixed_annotations/* evaluate_segmentation/transformed_audios/* evaluate_segmentation/tokenized_text/*
