# 选择题支持 - 常见问题解答

## 如何在 GraphRAG 中使用选择题进行测试？

### 问题背景
项目目前支持 QA 问题，但如果数据集中包含选择题，应该如何进行测试？

### 答案
**GraphRAG 已经完全支持选择题！** 系统使用 **close-set 评估模式** 来处理选择题。

---

## 快速开始

### 1. 准备数据

#### Corpus.json（文档文件）
每行一个 JSON 对象，包含文档标题和内容：
```json
{"title": "Python 编程语言", "context": "Python 是一种高级编程语言..."}
```

#### Question.json（问题文件）
**关键：** 选择题需要包含 `answer_idx` 字段！

```json
{
  "question": "谁创建了 Python 编程语言？\nA: James Gosling\nB: Guido van Rossum\nC: Dennis Ritchie\nD: Bjarne Stroustrup",
  "answer": "Guido van Rossum",
  "answer_idx": "B",
  "doc_id": 0
}
```

**必需字段：**
- `question`: 问题文本，包含选项（格式：选项字母 + 冒号 + 选项内容）
- `answer`: 正确答案的文本内容
- `answer_idx`: **正确答案的选项字母（A/B/C/D）** ← 这是选择题的关键字段！
- `doc_id`: 关联的文档编号（从 0 开始）

### 2. 设置数据集名称

**重要：** 数据集名称需要包含 "quality" 关键词以启用 close-set 评估模式。

#### 方法 1：将数据集目录命名为包含 "quality" 的名称
```bash
# 示例：将数据集放在 Data/quality_test/ 目录下
Data/
└── quality_test/
    ├── Corpus.json
    └── Question.json
```

#### 方法 2：使用符号链接
```bash
# 如果已有数据集，创建符号链接
ln -s MyDataset Data/quality_mytest
```

### 3. 运行测试

```bash
# 标准模式
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_test

# Per-corpus 模式（如果每个问题对应特定文档）
python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_test
```

### 4. 查看结果

```bash
# 查看评估指标
cat working_dir/your_exp_name/Metrics/metrics.json

# 查看详细结果（包含提取的选项）
cat working_dir/your_exp_name/Results/results.score.json
```

---

## 示例数据集

我们提供了一个完整的示例数据集：`Data/MultipleChoiceExample/`

### 查看示例

```bash
# 查看示例文档
cat Data/MultipleChoiceExample/Corpus.json

# 查看示例问题
cat Data/MultipleChoiceExample/Question.json

# 运行测试脚本验证格式
python tests/test_multiple_choice.py

# 运行示例脚本
bash run_multiple_choice_example.sh
```

---

## 工作原理

1. **构建图谱**：系统为文档构建知识图谱
2. **生成答案**：使用 GraphRAG 方法回答每个选择题
3. **提取选项**：使用 LLM 从模型输出中提取预测的选项字母（A/B/C/D）
4. **计算准确率**：将提取的选项与 `answer_idx` 比较

---

## 常见问题

### Q1: 为什么需要 answer_idx 字段？
**A**: `answer_idx` 字段是选择题评估的关键。系统会提取模型预测的选项字母，然后与 `answer_idx` 进行比较以计算准确率。

### Q2: 数据集名称一定要包含 "quality" 吗？
**A**: 是的，系统通过数据集名称判断评估模式。如果不包含 "quality"，系统会使用其他评估模式（如 short-form）。

**替代方案**：如果不想修改数据集名称，可以修改 `Core/Utils/Evaluation.py` 文件：
```python
self.dataset_mode_map = {
    "hotpotqa": "short-form",
    "quality": "close-set",
    "你的数据集名称": "close-set",  # 添加这一行
}
```

### Q3: 选项格式有什么要求？
**A**: 推荐格式：
```
问题文本？
A: 选项 A
B: 选项 B
C: 选项 C
D: 选项 D
```

也支持其他格式，只要 LLM 能够从中提取出选项字母即可。

### Q4: 如何查看模型预测的选项？
**A**: 查看 `results.score.json` 文件，其中的 `extract_output` 字段显示提取的选项。

### Q5: 能否混合使用选择题和开放式问题？
**A**: 不建议。不同类型的问题需要不同的评估模式。建议为选择题和开放式问题分别创建数据集。

### Q6: 准确率为 0 或很低怎么办？
**A**: 检查以下几点：
1. LLM 配置是否正确（在 `Option/Config2.yaml` 中）
2. `answer_idx` 格式是否正确（应为单个字母：A/B/C/D）
3. 问题中的选项格式是否清晰
4. 查看 `results.score.json` 中的 `extract_output` 字段，确认 LLM 是否正确提取了选项

---

## 完整示例

### 1. 创建数据集

创建目录：`Data/quality_python_test/`

**Corpus.json**:
```json
{"title": "Python 基础", "context": "Python 是由 Guido van Rossum 创建的编程语言，于 1991 年首次发布..."}
```

**Question.json**:
```json
{"question": "Python 的创建者是谁？\nA: Dennis Ritchie\nB: Guido van Rossum\nC: James Gosling\nD: Bjarne Stroustrup", "answer": "Guido van Rossum", "answer_idx": "B", "doc_id": 0}
{"question": "Python 首次发布于哪一年？\nA: 1985\nB: 1991\nC: 1995\nD: 2000", "answer": "1991", "answer_idx": "B", "doc_id": 0}
```

### 2. 配置 LLM

编辑 `Option/Config2.yaml`:
```yaml
llm:
  api_type: "openai"
  model: "gpt-4"
  api_key: "你的 API 密钥"
```

### 3. 运行测试

```bash
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_python_test
```

### 4. 查看结果

```bash
# 查看准确率
cat working_dir/your_exp_name/Metrics/metrics.json
# 输出：{"accuracy": 100.0}

# 查看详细结果
cat working_dir/your_exp_name/Results/results.score.json
```

---

## 技术细节

### 评估模式判断
在 `Core/Utils/Evaluation.py` 中：
```python
self.dataset_mode_map = {
    "hotpotqa": "short-form",     # 短答案 QA
    "multihop-rag": "short-form",
    "popqa": "short-form",
    "ALCE": "long-asqa",          # 长答案 QA
    "quality": "close-set",       # 选择题 ← 这个就是选择题模式
}
```

### 选项提取
系统使用特殊的提示词让 LLM 从模型输出中提取选项字母。提示词模板在 `Core/Utils/Evaluation.py` 中的 `CLOSE_EXTRACT_OPTION_PORMPT` 变量。

---

## 相关文档

- **完整英文文档**: `Doc/MULTIPLE_CHOICE_SUPPORT.md`
- **示例数据集**: `Data/MultipleChoiceExample/`
- **测试脚本**: `tests/test_multiple_choice.py`
- **示例运行脚本**: `run_multiple_choice_example.sh`

---

## 总结

GraphRAG 完全支持选择题！关键步骤：

✅ 1. 在 Question.json 中添加 `answer_idx` 字段（值为 A/B/C/D）
✅ 2. 将数据集名称设置为包含 "quality"（如 `quality_test`）
✅ 3. 使用标准命令运行测试
✅ 4. 查看结果中的准确率

如有问题，请参考示例数据集或运行测试脚本！
