# Per-Corpus Processing Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    main_per_corpus.py Workflow                          │
└─────────────────────────────────────────────────────────────────────────┘

                              START
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Load Configuration   │
                    │  (Config2.yaml +      │
                    │   Method/*.yaml)      │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Load Dataset         │
                    │  • Corpus.json        │
                    │  • Question.json      │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  Get Corpus List      │
                    │  [Doc0, Doc1, Doc2,..] │
                    └───────────┬───────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │   FOR EACH CORPUS SAMPLE      │
                └───────────┬───────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
   ┌────────────────────┐      ┌────────────────────────┐
   │ Corpus Sample N    │      │ Get Questions for      │
   │ • title            │      │ Corpus N               │
   │ • content          │      │ (filter by doc_id)     │
   │ • doc_id: N        │      └──────────┬─────────────┘
   └────────┬───────────┘                 │
            │                             │
            │         ┌───────────────────┘
            │         │
            ▼         ▼
   ┌─────────────────────────────┐
   │  Create Unique Namespace    │
   │  index_name_corpus_N        │
   └────────────┬────────────────┘
                │
                ▼
   ┌─────────────────────────────┐
   │  Initialize GraphRAG        │
   │  (new instance)             │
   └────────────┬────────────────┘
                │
                ▼
   ┌─────────────────────────────┐
   │  Build Graph                │
   │  digimon.insert([corpus])   │
   └────────────┬────────────────┘
                │
                ▼
   ┌─────────────────────────────┐
   │  Query All Questions        │
   │  for this Corpus            │
   └────────────┬────────────────┘
                │
                ▼
   ┌─────────────────────────────┐
   │  Save Results               │
   │  • corpus_N_results.json    │
   │  • Add corpus_id, title     │
   └────────────┬────────────────┘
                │
                └────────────┐
                             │
                ┌────────────▼───────────┐
                │  Next Corpus Sample?   │
                │  Yes → Loop            │
                │  No  → Continue        │
                └────────────┬───────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │  Combine All Results   │
                │  all_results.json      │
                └────────────┬───────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │  Run Evaluation        │
                │  metrics.json          │
                └────────────┬───────────┘
                             │
                             ▼
                           END


Output Structure:
─────────────────
working_dir/
└── exp_name/
    ├── Configs/
    │   ├── RAPTOR.yaml
    │   └── Config2.yaml
    ├── Results/
    │   ├── corpus_0_results.json    ← Questions & answers for Corpus 0
    │   ├── corpus_1_results.json    ← Questions & answers for Corpus 1
    │   ├── corpus_2_results.json    ← Questions & answers for Corpus 2
    │   └── all_results.json         ← Combined results
    ├── Metrics/
    │   └── metrics.json             ← Evaluation metrics
    └── Graph Storage/
        ├── tree_graph_corpus_0/     ← Separate graph for Corpus 0
        ├── tree_graph_corpus_1/     ← Separate graph for Corpus 1
        └── tree_graph_corpus_2/     ← Separate graph for Corpus 2


Key Benefits:
─────────────
✓ Complete isolation: Each corpus has its own graph
✓ No cross-contamination: Questions answered using only relevant corpus
✓ Per-document analysis: Easy to identify performance per corpus
✓ Memory efficient: Process one corpus at a time
✓ Scalable: Works with any number of corpus samples
```
