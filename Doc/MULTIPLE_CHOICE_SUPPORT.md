# Multiple-Choice Question Support / 选择题支持

## 选择题支持文档

本文档介绍如何在 GraphRAG 中使用选择题（多选题）进行测试和评估。

This document explains how to use multiple-choice questions in GraphRAG for testing and evaluation.

---

## 概述 (Overview)

GraphRAG 已经支持选择题（Multiple-Choice Questions）评估。系统使用 **close-set 模式** 来处理选择题，该模式会：
1. 使用 LLM 从模型输出中提取选项字母（A/B/C/D）
2. 将提取的选项与正确答案进行比较
3. 计算准确率

GraphRAG already supports multiple-choice question evaluation. The system uses **close-set mode** to handle multiple-choice questions, which:
1. Uses LLM to extract the option letter (A/B/C/D) from the model output
2. Compares the extracted option with the correct answer
3. Calculates accuracy

---

## 数据格式要求 (Data Format Requirements)

### Corpus.json 格式

与普通 QA 问题相同，每行一个 JSON 对象：

Same as regular QA questions, one JSON object per line:

```json
{"title": "Document Title", "context": "Document content..."}
```

### Question.json 格式 (重要！)

选择题的 Question.json 需要包含以下字段：

For multiple-choice questions, Question.json must include these fields:

```json
{
  "question": "Question text with options\nA: Option A\nB: Option B\nC: Option C\nD: Option D",
  "answer": "The answer text",
  "answer_idx": "B",
  "doc_id": 0
}
```

**必需字段 (Required Fields):**
- `question`: 问题文本，包含选项（格式：选项字母 + 冒号 + 选项内容）
  - Question text with options (format: option letter + colon + option content)
- `answer`: 正确答案的文本内容
  - Text content of the correct answer
- `answer_idx`: 正确答案的选项字母（A/B/C/D）**（选择题特有）**
  - Option letter of the correct answer (A/B/C/D) **(Required for multiple-choice)**
- `doc_id` 或 `corpus_id`: 关联的文档ID（从0开始）
  - Associated document ID (0-indexed)

---

## 完整示例 (Complete Example)

### 示例数据集位置
Example dataset location: `Data/MultipleChoiceExample/`

### Corpus.json
```json
{"title": "Python Programming Language", "context": "Python is a high-level, interpreted programming language created by Guido van Rossum. It was first released in 1991..."}
```

### Question.json
```json
{"question": "Who created the Python programming language?\nA: James Gosling\nB: Guido van Rossum\nC: Dennis Ritchie\nD: Bjarne Stroustrup", "answer": "Guido van Rossum", "answer_idx": "B", "doc_id": 0}
{"question": "When was Python first released?\nA: 1985\nB: 1991\nC: 1995\nD: 2000", "answer": "1991", "answer_idx": "B", "doc_id": 0}
```

---

## 使用方法 (Usage)

### 方法 1: 标准模式 (Standard Mode)

使用标准的 `main.py` 运行选择题测试：

Use standard `main.py` to run multiple-choice tests:

```bash
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name MultipleChoiceExample
```

**重要提示**: 需要在配置中设置 dataset 为 "quality" 或包含 "quality" 关键词，以启用 close-set 评估模式。

**Important**: You need to set the dataset name to "quality" or include "quality" keyword in the configuration to enable close-set evaluation mode.

或者，将数据集名称改为包含 "quality" 的名称：

Or, rename your dataset to include "quality":

```bash
# 将数据集目录重命名
mv Data/MultipleChoiceExample Data/quality_test

# 运行测试
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_test
```

### 方法 2: Per-Corpus 模式 (Per-Corpus Mode)

如果每个选择题对应特定的文档（通过 doc_id 关联），可以使用 per-corpus 模式：

If each multiple-choice question corresponds to a specific document (linked via doc_id), use per-corpus mode:

```bash
python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_test
```

---

## 评估指标 (Evaluation Metrics)

选择题使用 **close-set 模式**，评估指标包括：

Multiple-choice questions use **close-set mode** with the following metrics:

- **Accuracy (准确率)**: 正确预测的选项数量 / 总问题数量
  - Number of correctly predicted options / Total number of questions

---

## 工作流程 (Workflow)

1. **构建图** (Build Graph)
   - 系统为 corpus 文档构建知识图谱
   - System builds knowledge graph for corpus documents

2. **查询问题** (Query Questions)
   - 系统使用 GraphRAG 方法回答每个选择题
   - System answers each multiple-choice question using GraphRAG methods

3. **提取选项** (Extract Options)
   - 使用 LLM 从模型输出中提取预测的选项字母（A/B/C/D）
   - Use LLM to extract predicted option letter (A/B/C/D) from model output
   - 提示词模板见 `Core/Utils/Evaluation.py` 中的 `CLOSE_EXTRACT_OPTION_PORMPT` 变量
   - Prompt template in `CLOSE_EXTRACT_OPTION_PORMPT` variable in `Core/Utils/Evaluation.py`
   - Note: The variable name has a typo (PORMPT instead of PROMPT) in the original code

4. **计算准确率** (Calculate Accuracy)
   - 比较提取的选项与 answer_idx 字段
   - Compare extracted option with answer_idx field
   - 计算整体准确率
   - Calculate overall accuracy

---

## 输出结果 (Output Results)

### 结果文件 (Result Files)

运行后会在以下位置生成结果：

After running, results are generated at:

```
working_dir/
└── exp_name/
    ├── Results/
    │   ├── results.json           # 原始结果（包含模型输出）
    │   └── results.score.json     # 评估结果（包含提取的选项和准确率）
    └── Metrics/
        └── metrics.json           # 评估指标
```

### results.json 格式
```json
{
  "question": "Who created Python?\nA: ...\nB: ...",
  "answer": "Guido van Rossum",
  "answer_idx": "B",
  "output": "Based on the knowledge graph, the answer is B: Guido van Rossum",
  "extract_output": "B",
  "accuracy": 1
}
```

### metrics.json 格式
```json
{
  "accuracy": 85.71
}
```

---

## 配置说明 (Configuration)

### 确保评估模式正确

在 `Core/Utils/Evaluation.py` 中，系统通过 dataset_name 判断评估模式：

In `Core/Utils/Evaluation.py`, the system determines evaluation mode by dataset_name:

```python
self.dataset_mode_map = {
    "hotpotqa": "short-form",
    "multihop-rag": "short-form",
    "popqa": "short-form",
    "ALCE": "long-asqa",
    "quality": "close-set",  # 选择题模式
}
```

**方法 1**: 使用预定义的数据集名称 "quality"

**Method 1**: Use predefined dataset name "quality"

```bash
# 将数据集目录命名为 quality 或包含 quality
mv Data/MultipleChoiceExample Data/quality_mc
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_mc
```

**方法 2**: 修改 Evaluation.py 添加自定义数据集名称映射

**Method 2**: Modify Evaluation.py to add custom dataset name mapping

在 `Core/Utils/Evaluation.py` 的 `__init__` 方法中添加：

Add to the `__init__` method in `Core/Utils/Evaluation.py`:

```python
self.dataset_mode_map = {
    "hotpotqa": "short-form",
    "multihop-rag": "short-form",
    "popqa": "short-form",
    "ALCE": "long-asqa",
    "quality": "close-set",
    "MultipleChoiceExample": "close-set",  # 添加您的数据集
}
```

---

## 测试脚本 (Test Script)

我们提供了一个测试脚本来验证选择题功能：

We provide a test script to verify multiple-choice functionality:

### `tests/test_multiple_choice.py`

运行测试：
```bash
python tests/test_multiple_choice.py
```

该脚本会：
1. 加载选择题数据集
2. 验证数据格式
3. 检查必需字段（answer_idx）
4. 确认评估模式设置

---

## 常见问题 (FAQ)

### Q1: 评估时没有使用 close-set 模式？
**A**: 确保数据集名称包含 "quality" 或在 `Evaluation.py` 中添加数据集名称映射。

### Q2: Question.json 缺少 answer_idx 字段？
**A**: 选择题必须包含 `answer_idx` 字段，值为正确答案的选项字母（A/B/C/D）。

### Q3: 选项格式要求是什么？
**A**: 推荐格式为：
```
Question text?
A: Option A
B: Option B
C: Option C
D: Option D
```

也支持其他格式，只要 LLM 能从模型输出中提取出选项字母即可。

### Q4: 如何查看提取的选项？
**A**: 查看 `results.score.json` 文件中的 `extract_output` 字段。

### Q5: 准确率为 0？
**A**: 检查：
- LLM 是否正确配置
- answer_idx 格式是否正确
- 问题中的选项格式是否清晰

### Q6: 能否混合使用选择题和开放式问题？
**A**: 不建议。不同类型的问题需要不同的评估模式。建议分别创建数据集。

---

## 最佳实践 (Best Practices)

1. **数据集命名**: 将选择题数据集命名为包含 "quality" 的名称
   - Name multiple-choice datasets with "quality" in the name

2. **选项格式**: 使用清晰的选项格式（A:, B:, C:, D:）
   - Use clear option format (A:, B:, C:, D:)

3. **答案字段**: 同时提供 `answer`（文本）和 `answer_idx`（字母）
   - Provide both `answer` (text) and `answer_idx` (letter)

4. **文档关联**: 使用 `doc_id` 将问题关联到对应的文档
   - Use `doc_id` to link questions to corresponding documents

5. **验证数据**: 运行测试脚本验证数据格式
   - Run test script to validate data format

---

## 完整示例命令 (Complete Example Commands)

### 1. 准备数据
```bash
# 数据已在 Data/MultipleChoiceExample/ 目录下
# Data is already in Data/MultipleChoiceExample/

# 重命名以启用 close-set 模式
mv Data/MultipleChoiceExample Data/quality_example
```

### 2. 配置 LLM
编辑 `Option/Config2.yaml`:
```yaml
llm:
  api_type: "openai"
  model: "gpt-4"
  api_key: "your-api-key"
```

### 3. 运行测试（标准模式）
```bash
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_example
```

### 4. 运行测试（Per-Corpus 模式）
```bash
python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_example
```

### 5. 查看结果
```bash
# 查看评估指标
cat working_dir/exp_name/Metrics/metrics.json

# 查看详细结果
cat working_dir/exp_name/Results/results.score.json
```

---

## 技术细节 (Technical Details)

### 选项提取机制

系统使用 LLM 提取选项，提示词模板在 `Core/Utils/Evaluation.py`:

```python
# Note: Variable name has a typo in original code (PORMPT instead of PROMPT)
CLOSE_EXTRACT_OPTION_PORMPT = """
You are given a model output which is a string...
...extract the option letter from the model output...
"""
```

### 评估流程

1. 模型生成答案（可能包含解释）
2. LLM 提取选项字母（A/B/C/D 或 -1 表示无法提取）
3. 比较提取的选项与 answer_idx
4. 计算准确率

---

## 相关文件 (Related Files)

- `Core/Utils/Evaluation.py` - 评估逻辑，包含 close-set 模式
- `Data/QueryDataset.py` - 数据集加载
- `Data/MultipleChoiceExample/` - 示例数据集
- `tests/test_multiple_choice.py` - 测试脚本

---

## 总结 (Summary)

GraphRAG 完全支持选择题评估！您只需要：

GraphRAG fully supports multiple-choice question evaluation! You just need to:

✅ 准备包含 `answer_idx` 字段的 Question.json
✅ 将数据集命名为包含 "quality" 的名称（或修改配置）
✅ 使用标准命令运行测试
✅ 查看评估结果中的准确率

✅ Prepare Question.json with `answer_idx` field
✅ Name dataset with "quality" (or modify configuration)
✅ Run tests with standard commands
✅ Check accuracy in evaluation results

如有问题，请参考示例数据集 `Data/MultipleChoiceExample/` 或运行测试脚本 `tests/test_multiple_choice.py`。

For questions, refer to the example dataset `Data/MultipleChoiceExample/` or run the test script `tests/test_multiple_choice.py`.
