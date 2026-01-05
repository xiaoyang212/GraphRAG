#!/usr/bin/env python3
"""
Test script for multiple-choice question functionality
测试选择题功能的脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Data.QueryDataset import RAGQueryDataset
import json

def test_multiple_choice_dataset():
    """Test the QueryDataset with multiple-choice questions"""
    print("Testing Multiple-Choice Question Dataset")
    print("测试选择题数据集")
    print("="*80)
    
    # Load multiple-choice dataset
    data_dir = os.path.join(os.path.dirname(__file__), "..", "Data", "MultipleChoiceExample")
    
    if not os.path.exists(data_dir):
        print(f"❌ Error: Dataset directory not found: {data_dir}")
        print(f"❌ 错误：未找到数据集目录：{data_dir}")
        return False
    
    try:
        dataset = RAGQueryDataset(data_dir=data_dir)
        print(f"✅ Successfully loaded dataset from {data_dir}")
        print(f"✅ 成功加载数据集：{data_dir}\n")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        print(f"❌ 加载数据集失败：{e}")
        return False
    
    # Test corpus loading
    corpus = dataset.get_corpus()
    print(f"1. Total corpus samples: {len(corpus)}")
    print(f"   总文档数：{len(corpus)}")
    for i, doc in enumerate(corpus):
        print(f"   Corpus {i}: {doc['title']}")
    
    # Test question loading
    print(f"\n2. Total questions: {len(dataset)}")
    print(f"   总问题数：{len(dataset)}")
    
    # Verify multiple-choice specific fields
    print(f"\n3. Verifying multiple-choice question format:")
    print(f"   验证选择题格式：")
    
    all_valid = True
    missing_answer_idx = []
    
    for i in range(len(dataset)):
        question = dataset[i]
        
        # Check required fields
        has_question = 'question' in question
        has_answer = 'answer' in question
        has_answer_idx = 'answer_idx' in question
        has_doc_id = 'doc_id' in question or 'corpus_id' in question
        
        if not has_answer_idx:
            missing_answer_idx.append(i)
            all_valid = False
        
        # Display first question as example
        if i == 0:
            print(f"\n   Example question {i}:")
            print(f"   示例问题 {i}:")
            print(f"   - Question: {question['question'][:100]}...")
            print(f"   - Answer: {question['answer']}")
            print(f"   - Answer Index: {question.get('answer_idx', 'MISSING')}")
            print(f"   - Doc ID: {question.get('doc_id', question.get('corpus_id', 'MISSING'))}")
    
    if missing_answer_idx:
        print(f"\n   ❌ WARNING: {len(missing_answer_idx)} questions missing 'answer_idx' field")
        print(f"   ❌ 警告：{len(missing_answer_idx)} 个问题缺少 'answer_idx' 字段")
        print(f"   Missing in questions: {missing_answer_idx}")
    else:
        print(f"\n   ✅ All questions have 'answer_idx' field")
        print(f"   ✅ 所有问题都包含 'answer_idx' 字段")
    
    # Test grouping by corpus
    print(f"\n4. Questions grouped by corpus:")
    print(f"   按文档分组的问题：")
    for corpus_idx in range(len(corpus)):
        questions = dataset.get_questions_for_corpus(corpus_idx)
        print(f"\n   Corpus {corpus_idx} ({corpus[corpus_idx]['title']}): {len(questions)} questions")
        for q_idx, q in enumerate(questions, 1):
            # Show question and answer index
            q_text = q['question'].split('\n')[0]  # First line only
            print(f"      Q{q_idx}: {q_text}")
            print(f"           Answer: {q.get('answer_idx', 'N/A')}")
    
    # Check evaluation mode
    print(f"\n5. Evaluation mode check:")
    print(f"   评估模式检查：")
    
    dataset_name = os.path.basename(data_dir)
    print(f"   Dataset name: {dataset_name}")
    print(f"   数据集名称：{dataset_name}")
    
    # Check if dataset name will trigger close-set mode
    if "quality" in dataset_name.lower():
        print(f"   ✅ Dataset name contains 'quality' - will use close-set mode")
        print(f"   ✅ 数据集名称包含 'quality' - 将使用 close-set 模式")
    else:
        print(f"   ⚠️  Dataset name doesn't contain 'quality'")
        print(f"   ⚠️  数据集名称不包含 'quality'")
        print(f"   💡 Recommendation: Rename dataset to include 'quality' (e.g., 'quality_test')")
        print(f"   💡 建议：重命名数据集以包含 'quality'（例如 'quality_test'）")
        print(f"   💡 Or add '{dataset_name}': 'close-set' to dataset_mode_map in Core/Utils/Evaluation.py")
        print(f"   💡 或在 Core/Utils/Evaluation.py 的 dataset_mode_map 中添加 '{dataset_name}': 'close-set'")
    
    print("\n" + "="*80)
    if all_valid:
        print("✅ All tests passed! Dataset is ready for multiple-choice evaluation.")
        print("✅ 所有测试通过！数据集已准备好进行选择题评估。")
        return True
    else:
        print("⚠️  Some issues found. Please review the warnings above.")
        print("⚠️  发现一些问题。请查看上述警告。")
        return False

if __name__ == "__main__":
    success = test_multiple_choice_dataset()
    sys.exit(0 if success else 1)
