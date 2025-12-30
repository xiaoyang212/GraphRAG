#!/bin/bash
# Example script to run per-corpus graph processing with RAPTOR method

# Set your configuration
DATASET_NAME="TestDataset"  # Change this to your dataset name
METHOD="RAPTOR"              # Change this to your desired method
CONFIG_FILE="Option/Method/${METHOD}.yaml"

# Before running, make sure:
# 1. You have configured your LLM and embedding settings in Option/Config2.yaml
# 2. Your dataset is in Data/${DATASET_NAME}/ with Corpus.json and Question.json
# 3. Questions in Question.json have a 'doc_id' or 'corpus_id' field linking to corpus

echo "============================================"
echo "Running Per-Corpus GraphRAG Processing"
echo "Dataset: ${DATASET_NAME}"
echo "Method: ${METHOD}"
echo "============================================"

python main_per_corpus.py \
    -opt "${CONFIG_FILE}" \
    -dataset_name "${DATASET_NAME}"

echo ""
echo "============================================"
echo "Processing complete!"
echo "Check results in ./${METHOD}/Results/"
echo "============================================"
