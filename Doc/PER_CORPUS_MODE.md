# Per-Corpus Graph Processing

## Overview

This feature allows you to build **separate graphs for each corpus sample** in your dataset and answer only the questions corresponding to each specific corpus sample. This is useful when you want to:

- Isolate graph construction per document
- Avoid cross-document interference in the knowledge graph
- Process each document independently with its own set of questions
- Analyze performance on a per-document basis

## Usage

### Basic Command

```bash
python main_per_corpus.py -opt Option/Method/<METHOD>.yaml -dataset_name your_dataset
```

For example, using RAPTOR:
```bash
python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name HotpotQA
```

### Data Format Requirements

Your dataset directory should contain two JSON files:

#### 1. Corpus.json
Each line should be a JSON object with the following fields:
- `title`: Title of the document
- `context`: The main text content of the document

Example:
```json
{"title": "Python Programming", "context": "Python is a high-level, interpreted programming language..."}
{"title": "Machine Learning", "context": "Machine learning is a subset of artificial intelligence..."}
```

#### 2. Question.json
Each line should be a JSON object with the following fields:
- `question`: The question text
- `answer`: The expected answer
- `doc_id` or `corpus_id`: Integer linking the question to a corpus document (0-indexed)

Example:
```json
{"question": "Who created Python?", "answer": "Guido van Rossum", "doc_id": 0}
{"question": "When was Python first released?", "answer": "1991", "doc_id": 0}
{"question": "What does machine learning enable?", "answer": "Systems to learn...", "doc_id": 1}
```

## How It Works

1. **Load Dataset**: Reads all corpus documents and questions from the dataset directory
2. **For Each Corpus Sample**:
   - Extract the corpus document
   - Get all questions associated with that document (via `doc_id` or `corpus_id`)
   - Initialize a new GraphRAG instance with a unique namespace
   - Build a graph specifically for this corpus document
   - Query all questions for this corpus
   - Save results for this corpus sample
3. **Combine Results**: Aggregate all per-corpus results into a combined output file
4. **Evaluate**: Run evaluation metrics on the combined results

## Output Structure

The script creates the following outputs in your experiment directory:

```
working_dir/
└── exp_name/
    ├── Configs/           # Configuration files used
    ├── Results/
    │   ├── corpus_0_results.json    # Results for first corpus
    │   ├── corpus_1_results.json    # Results for second corpus
    │   ├── ...
    │   └── all_results.json         # Combined results
    ├── Metrics/
    │   └── metrics.json             # Evaluation metrics
    └── [index_name]_corpus_[N]/     # Separate graph storage for each corpus
```

### Result Fields

Each result entry includes:
- All original question fields (`question`, `answer`, etc.)
- `output`: The model's generated answer
- `corpus_id`: ID of the source corpus document
- `corpus_title`: Title of the source corpus document

## Example

See the test dataset in `Data/TestDataset/` for a minimal working example:
- 3 corpus documents (Python, Machine Learning, Data Science)
- 6 questions (2 questions per corpus)

To test with this dataset:
```bash
python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name TestDataset
```

## Comparison with Standard Mode

| Aspect | Standard Mode (`main.py`) | Per-Corpus Mode (`main_per_corpus.py`) |
|--------|---------------------------|----------------------------------------|
| Graph Building | One graph for all corpus documents | Separate graph for each corpus document |
| Question Answering | All questions against single graph | Questions filtered by corpus |
| Graph Storage | Single namespace | Multiple namespaces (one per corpus) |
| Memory Usage | Higher (all docs in one graph) | Lower per iteration |
| Isolation | Cross-document connections possible | Each corpus is isolated |

## Tips

1. **Memory Management**: Each corpus is processed sequentially, so memory usage stays consistent
2. **Graph Persistence**: Each graph is saved with a unique identifier (`index_name_corpus_N`)
3. **Debugging**: Check individual corpus result files to identify issues with specific documents
4. **Performance**: Processing time scales linearly with the number of corpus samples

## Notes

- If a corpus has no associated questions, it will be skipped
- The linking field can be either `doc_id` or `corpus_id` in Question.json
- Original `main.py` behavior is unchanged - use it for standard all-at-once processing
