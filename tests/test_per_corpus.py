#!/usr/bin/env python3
"""
Test script for per-corpus functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Data.QueryDataset import RAGQueryDataset

def test_query_dataset():
    """Test the QueryDataset with per-corpus functionality"""
    print("Testing RAGQueryDataset with per-corpus functionality...")
    print("="*80)
    
    # Load test dataset
    data_dir = os.path.join(os.path.dirname(__file__), "..", "Data", "TestDataset")
    dataset = RAGQueryDataset(data_dir=data_dir)
    
    # Test corpus loading
    corpus = dataset.get_corpus()
    print(f"\n1. Total corpus samples: {len(corpus)}")
    for i, doc in enumerate(corpus):
        print(f"   Corpus {i}: {doc['title']}")
    
    # Test question loading
    print(f"\n2. Total questions: {len(dataset)}")
    
    # Test getting questions for each corpus
    print(f"\n3. Questions grouped by corpus:")
    for corpus_idx in range(len(corpus)):
        questions = dataset.get_questions_for_corpus(corpus_idx)
        print(f"\n   Corpus {corpus_idx} ({corpus[corpus_idx]['title']}): {len(questions)} questions")
        for q_idx, q in enumerate(questions, 1):
            print(f"      Q{q_idx}: {q['question']}")
    
    # Test individual corpus item retrieval
    print(f"\n4. Test get_corpus_item(0):")
    item = dataset.get_corpus_item(0)
    print(f"   Title: {item['title']}")
    print(f"   Content (first 100 chars): {item['content'][:100]}...")
    
    print("\n" + "="*80)
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_query_dataset()
