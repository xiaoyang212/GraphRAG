# 如何在 GraphRAG 中测试选择题 - 完整解决方案

## 问题
**原问题**: "现在项目仅支持qa问题，如果数据集中含有选择题，我该如何进行测试"

**翻译**: The project currently only supports QA questions. If the dataset contains multiple-choice questions, how should I test them?

## 答案

**好消息**: GraphRAG **已经完全支持选择题测试**！系统内置了 **close-set 评估模式** 专门用于处理选择题。

**Good News**: GraphRAG **already fully supports multiple-choice question testing**! The system has a built-in **close-set evaluation mode** specifically designed for multiple-choice questions.

---

## 解决方案概述

### 三个简单步骤

1. **准备数据**: 在 Question.json 中添加 `answer_idx` 字段
2. **命名数据集**: 数据集名称包含 "quality" 关键词
3. **运行测试**: 使用标准命令运行

---

## 详细步骤

### 步骤 1: 准备选择题数据

创建 Question.json，每个问题需要包含以下字段：

```json
{
  "question": "谁创建了 Python？\nA: James Gosling\nB: Guido van Rossum\nC: Dennis Ritchie\nD: Bjarne Stroustrup",
  "answer": "Guido van Rossum",
  "answer_idx": "B",
  "doc_id": 0
}
```

**关键字段说明**:
- `question`: 问题文本，包含所有选项（建议格式：A: 选项A\nB: 选项B...）
- `answer`: 正确答案的完整文本
- `answer_idx`: **正确答案的选项字母（A/B/C/D）** ← **这是选择题的关键！**
- `doc_id`: 问题对应的文档编号

### 步骤 2: 设置数据集名称

**方法 1: 直接命名数据集目录**
```bash
# 将数据集放在名称包含 "quality" 的目录中
Data/
└── quality_test/          # ← 名称包含 "quality"
    ├── Corpus.json
    └── Question.json
```

**方法 2: 使用符号链接**
```bash
# 如果已有数据集目录，创建符号链接
ln -s MyExistingDataset Data/quality_mytest
```

**方法 3: 修改配置文件**（如果不想修改数据集名称）
编辑 `Core/Utils/Evaluation.py`，在 `__init__` 方法中添加：
```python
self.dataset_mode_map = {
    "hotpotqa": "short-form",
    "quality": "close-set",
    "your_dataset_name": "close-set",  # ← 添加你的数据集名称
}
```

### 步骤 3: 运行测试

**标准模式**:
```bash
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_test
```

**Per-Corpus 模式**（如果每个问题对应特定文档）:
```bash
python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_test
```

### 步骤 4: 查看结果

```bash
# 查看评估指标（准确率）
cat working_dir/your_exp_name/Metrics/metrics.json

# 查看详细结果（包含每个问题的预测选项）
cat working_dir/your_exp_name/Results/results.score.json
```

---

## 示例数据集

我们为您准备了一个完整的示例数据集，可以直接使用：

### 位置
`Data/MultipleChoiceExample/`

### 内容

**Corpus.json** - 3个文档:
- Python Programming Language
- Artificial Intelligence and Machine Learning
- Database Management Systems

**Question.json** - 7个选择题:
- 每个问题都包含完整的选项（A/B/C/D）
- 每个问题都有 `answer_idx` 字段
- 每个问题通过 `doc_id` 关联到对应文档

### 快速测试

```bash
# 1. 创建符号链接（或重命名）
ln -s MultipleChoiceExample Data/quality_example

# 2. 验证数据格式
python tests/test_multiple_choice.py

# 3. 运行示例（需要先配置 LLM）
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_example
```

---

## 工作原理

### 评估流程

1. **构建知识图谱**
   - 系统为 Corpus.json 中的文档构建知识图谱
   
2. **生成答案**
   - 对每个选择题，GraphRAG 生成答案（可能包含解释）
   - 例如："Based on the knowledge graph, the answer is B: Guido van Rossum"
   
3. **提取选项**
   - 使用 LLM 从模型输出中提取预测的选项字母
   - 系统使用特殊的提示词让 LLM 识别并提取 A/B/C/D
   
4. **计算准确率**
   - 将提取的选项与 `answer_idx` 进行比较
   - 计算整体准确率

### 技术细节

- **评估模式**: close-set（专门用于选择题）
- **提取方法**: 使用 LLM 理解并提取选项字母
- **容错处理**: 如果无法提取选项，标记为 "-1"

---

## 常见问题

### Q1: 我的数据集已经有了，但没有 answer_idx 字段怎么办？

**A**: 需要为每个选择题添加 `answer_idx` 字段。可以手动添加或编写脚本批量处理：

```python
import json

# 读取现有数据
with open('Question.json', 'r') as f:
    questions = [json.loads(line) for line in f]

# 添加 answer_idx（这里需要手动指定每个问题的正确选项）
answer_mapping = {
    0: "B",  # 第1个问题的答案是 B
    1: "A",  # 第2个问题的答案是 A
    # ... 继续添加
}

# 更新并保存
with open('Question_updated.json', 'w') as f:
    for i, q in enumerate(questions):
        q['answer_idx'] = answer_mapping[i]
        f.write(json.dumps(q, ensure_ascii=False) + '\n')
```

### Q2: 评估时显示使用了 short-form 模式而不是 close-set？

**A**: 检查数据集名称是否包含 "quality"。如果不包含，有两个选择：
1. 重命名数据集目录（推荐）
2. 修改 `Core/Utils/Evaluation.py` 添加数据集映射

### Q3: 准确率为 0 或异常低？

**A**: 检查：
1. **LLM 配置**: 确保 `Option/Config2.yaml` 中的 LLM 配置正确
2. **answer_idx 格式**: 应该是单个字母（A/B/C/D），不要有其他字符
3. **选项格式**: 问题中的选项应该清晰（推荐格式：A: xxx\nB: xxx）
4. **提取结果**: 查看 `results.score.json` 中的 `extract_output` 字段

### Q4: 能否同时测试选择题和开放式问题？

**A**: 不建议在同一个数据集中混合。建议：
- 为选择题创建单独的数据集（名称包含 "quality"）
- 为开放式问题创建单独的数据集

### Q5: 支持多少个选项？只能是 A/B/C/D 吗？

**A**: 当前实现主要针对标准的 4 选项（A/B/C/D）设计。如果需要更多选项（如 E/F），提取提示词应该也能处理，但建议测试验证。

---

## 完整工作示例

### 1. 准备数据

创建目录：`Data/quality_python_quiz/`

**Corpus.json**:
```json
{"title": "Python 编程语言", "context": "Python 是由 Guido van Rossum 于 1991 年创建的高级编程语言。Python 强调代码可读性，使用显著的缩进。"}
```

**Question.json**:
```json
{"question": "谁创建了 Python 编程语言？\nA: Dennis Ritchie\nB: Guido van Rossum\nC: James Gosling\nD: Bjarne Stroustrup", "answer": "Guido van Rossum", "answer_idx": "B", "doc_id": 0}
{"question": "Python 首次发布于哪一年？\nA: 1985\nB: 1989\nC: 1991\nD: 1995", "answer": "1991", "answer_idx": "C", "doc_id": 0}
{"question": "Python 的主要特点是什么？\nA: 使用大括号定义代码块\nB: 静态类型\nC: 强调代码可读性和缩进\nD: 低级内存操作", "answer": "强调代码可读性和缩进", "answer_idx": "C", "doc_id": 0}
```

### 2. 配置 LLM

编辑 `Option/Config2.yaml`:
```yaml
llm:
  api_type: "openai"
  model: "gpt-4"
  api_key: "sk-your-api-key-here"
  base_url: "https://api.openai.com/v1"
```

### 3. 运行测试

```bash
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_python_quiz
```

### 4. 预期输出

控制台输出：
```
Loaded 3 records from working_dir/exp_name/Results/results.json
Evaluating close-set mode.
In this evaluation, the following metrics are used:
accuracy 

LLM extract option completed.
accuracy: 100.0000
```

结果文件 `metrics.json`:
```json
{"accuracy": 100.0}
```

---

## 相关资源

### 文档
- **完整英文文档**: `Doc/MULTIPLE_CHOICE_SUPPORT.md` - 包含所有技术细节
- **中文 FAQ**: `Doc/MULTIPLE_CHOICE_FAQ_CN.md` - 快速问答
- **快速参考**: `QUICK_REFERENCE.md` - Feature 1

### 示例和脚本
- **示例数据集**: `Data/MultipleChoiceExample/` - 可直接使用
- **测试脚本**: `tests/test_multiple_choice.py` - 验证数据格式
- **运行脚本**: `run_multiple_choice_example.sh` - 自动化设置和测试

### 相关代码
- **评估实现**: `Core/Utils/Evaluation.py` - `close_eval()` 方法
- **数据加载**: `Data/QueryDataset.py` - RAGQueryDataset 类

---

## 总结

✅ **GraphRAG 已经支持选择题！** 不需要修改任何核心代码。

✅ **三步即可使用**:
1. 在 Question.json 中添加 `answer_idx` 字段
2. 数据集名称包含 "quality"
3. 运行标准测试命令

✅ **完整的支持**:
- 自动提取选项
- 准确率评估
- 详细的结果输出

✅ **丰富的文档和示例**:
- 中英文文档
- 可运行的示例数据集
- 测试和验证脚本

**现在就可以开始使用选择题测试 GraphRAG！**

如有任何问题，请参考文档或查看示例数据集。
