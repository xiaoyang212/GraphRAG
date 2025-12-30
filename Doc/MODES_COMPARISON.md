# Comparison: Standard vs Per-Corpus Processing Modes

## Quick Reference

| Feature | Standard Mode (`main.py`) | Per-Corpus Mode (`main_per_corpus.py`) |
|---------|---------------------------|----------------------------------------|
| **Command** | `python main.py -opt <config> -dataset_name <name>` | `python main_per_corpus.py -opt <config> -dataset_name <name>` |
| **Graph Building** | One unified graph for all corpus documents | Separate isolated graph per corpus document |
| **Question Filtering** | All questions queried against the same graph | Questions filtered by corpus_id/doc_id |
| **Memory Usage** | Higher (entire corpus in one graph) | Lower per iteration (one corpus at a time) |
| **Processing Time** | Faster overall (one graph build) | Slower (multiple graph builds) |
| **Graph Isolation** | Cross-document connections possible | Complete isolation per document |
| **Use Case** | General RAG, multi-hop questions across docs | Document-specific QA, preventing cross-contamination |
| **Output Files** | Single `results.json` | Per-corpus results + combined `all_results.json` |
| **Graph Storage** | Single namespace (e.g., `tree_graph_balanced/`) | Multiple namespaces (e.g., `tree_graph_balanced_corpus_0/`) |

## When to Use Each Mode

### Use Standard Mode (`main.py`) when:
- ✅ Your questions may span multiple documents
- ✅ You want to find connections across documents
- ✅ You have limited time for processing
- ✅ Your dataset is relatively small
- ✅ You want to leverage the full corpus knowledge

### Use Per-Corpus Mode (`main_per_corpus.py`) when:
- ✅ Each question relates to a specific document
- ✅ You want to avoid cross-document interference
- ✅ You need to evaluate per-document performance
- ✅ You want isolated graph construction
- ✅ Your questions have clear document associations
- ✅ You're doing document-level analysis or debugging

## Example Scenarios

### Scenario 1: Wikipedia Articles with Document-Specific Questions
**Dataset**: 100 Wikipedia articles, each with 5 questions about that article only

**Recommended**: Per-Corpus Mode
- Each article gets its own graph
- Questions are isolated to their source article
- Easy to identify which articles perform poorly
- No knowledge leakage between articles

### Scenario 2: Multi-Document Question Answering
**Dataset**: Collection of news articles with questions requiring synthesis across multiple articles

**Recommended**: Standard Mode
- Build one graph connecting all articles
- Enable multi-hop reasoning across documents
- Find relationships between different news stories
- Support complex comparative questions

### Scenario 3: Document Collection with Mixed Question Types
**Dataset**: Technical documentation with both document-specific and cross-document questions

**Approach**: Run both modes
1. Use Per-Corpus Mode for document-specific evaluation
2. Use Standard Mode for cross-document evaluation
3. Compare results to understand both capabilities

## Performance Characteristics

### Standard Mode
```
Total Time = Graph Build Time (all docs) + Query Time (all questions)
Memory Peak = All documents + Full graph + Indexes
```

### Per-Corpus Mode
```
Total Time = N × (Graph Build Time (1 doc) + Query Time (questions for doc))
Memory Peak = Single document + Single graph + Indexes
```

Where N = number of corpus documents

## Data Requirements

Both modes use the same data format, but Per-Corpus Mode requires:

**Question.json** must include `doc_id` or `corpus_id` field:
```json
{"question": "...", "answer": "...", "doc_id": 0}
```

If questions lack this field:
- Standard Mode: Works normally
- Per-Corpus Mode: Questions will be skipped (no corpus association)

## Migration Guide

### From Standard to Per-Corpus

If you're currently using Standard Mode and want to try Per-Corpus Mode:

1. **Update your Question.json** to include `doc_id` or `corpus_id`:
   ```python
   # Add doc_id to your questions
   for i, question in enumerate(questions):
       question['doc_id'] = determine_source_doc(question)
   ```

2. **Run with new script**:
   ```bash
   python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name YourDataset
   ```

3. **Compare results** between modes to ensure correctness

### From Per-Corpus to Standard

Simply use `main.py` instead - no data changes needed!

## Best Practices

### For Both Modes
- Configure your LLM settings in `Option/Config2.yaml`
- Use appropriate chunk sizes for your document types
- Monitor memory usage for large datasets

### For Per-Corpus Mode Specifically
- Ensure all questions have valid `doc_id`/`corpus_id` references
- Check for questions with no corpus association (they'll be skipped)
- Consider processing order if debugging specific documents
- Review individual corpus results for detailed analysis
- Use the combined results file for overall metrics

## Troubleshooting

### Per-Corpus Mode Issues

**Problem**: "No questions found for corpus X, skipping..."
- **Cause**: Questions lack `doc_id`/`corpus_id` or values don't match
- **Solution**: Verify Question.json has correct linking fields

**Problem**: Very slow processing
- **Cause**: Many corpus samples, each requires graph build
- **Solution**: Consider Standard Mode, or process subset of corpus

**Problem**: Different results than Standard Mode
- **Cause**: Expected! Graph isolation changes context
- **Solution**: This is by design - each mode serves different purposes
