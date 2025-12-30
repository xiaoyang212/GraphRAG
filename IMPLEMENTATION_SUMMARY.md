# Per-Corpus Graph Processing - Implementation Summary

## 实现概要 (Implementation Summary)

本次更新实现了针对 corpus 每条样本单独建图、保存并回答对应问题的功能。

This update implements the functionality to build separate graphs for each corpus sample, save them individually, and answer only the questions corresponding to each corpus sample.

## 新增文件 (New Files)

### 1. `main_per_corpus.py` - 主处理脚本
核心功能文件，实现每个 corpus 样本的独立处理：
- 为每个 corpus 文档创建独立的图
- 使用唯一的命名空间保存每个图
- 只查询属于该 corpus 的问题
- 保存每个 corpus 的结果和汇总结果

Core functionality file for processing each corpus sample independently:
- Creates separate graphs for each corpus document
- Saves each graph with unique namespace
- Queries only questions belonging to that corpus
- Saves individual and combined results

### 2. `Doc/PER_CORPUS_MODE.md` - 详细使用文档
完整的使用指南，包括：
- 数据格式要求
- 使用方法和示例
- 输出结构说明
- 与标准模式的对比

Complete usage guide including:
- Data format requirements
- Usage methods and examples
- Output structure explanation
- Comparison with standard mode

### 3. `Doc/MODES_COMPARISON.md` - 模式对比文档
详细对比两种处理模式：
- 功能对比表
- 使用场景建议
- 性能特征分析
- 最佳实践

Detailed comparison of both processing modes:
- Feature comparison table
- Use case recommendations
- Performance characteristics
- Best practices

### 4. `run_per_corpus_example.sh` - 示例运行脚本
可执行的示例脚本，展示如何运行新功能

Executable example script showing how to run the new functionality

### 5. `Data/TestDataset/` - 测试数据集
包含示例数据用于测试：
- `Corpus.json`: 3个示例文档
- `Question.json`: 6个问题（每个文档2个）

Sample test dataset:
- `Corpus.json`: 3 sample documents
- `Question.json`: 6 questions (2 per document)

### 6. `tests/test_per_corpus.py` - 测试脚本
验证 QueryDataset 新功能的测试脚本

Test script to verify new QueryDataset functionality

## 修改文件 (Modified Files)

### 1. `Data/QueryDataset.py`
新增方法：
- `get_corpus_item(doc_id)`: 获取单个 corpus 样本
- `get_questions_for_corpus(doc_id)`: 获取特定 corpus 的所有问题
- 增加错误处理和边界检查

Added methods:
- `get_corpus_item(doc_id)`: Get single corpus sample
- `get_questions_for_corpus(doc_id)`: Get all questions for specific corpus
- Added error handling and bounds checking

### 2. `README.md`
添加了 Per-Corpus 模式的使用说明

Added usage instructions for Per-Corpus mode

### 3. `.gitignore`
改进了忽略规则，排除实验输出文件

Improved ignore rules to exclude experiment outputs

## 使用方法 (Usage)

### 基本命令 (Basic Command)
```bash
python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name your_dataset
```

### 数据格式要求 (Data Format Requirements)

#### Corpus.json
每行一个JSON对象，包含：
- `title`: 文档标题
- `context`: 文档内容

Each line is a JSON object with:
- `title`: Document title
- `context`: Document content

```json
{"title": "Python Programming", "context": "Python is a high-level..."}
```

#### Question.json
每行一个JSON对象，包含：
- `question`: 问题文本
- `answer`: 答案
- `doc_id` 或 `corpus_id`: 关联到 corpus 的索引（从0开始）

Each line is a JSON object with:
- `question`: Question text
- `answer`: Answer
- `doc_id` or `corpus_id`: Index linking to corpus (0-indexed)

```json
{"question": "Who created Python?", "answer": "Guido van Rossum", "doc_id": 0}
```

## 工作流程 (Workflow)

1. **加载数据集** (Load Dataset)
   - 读取所有 corpus 文档和问题

2. **逐个处理 corpus** (Process Each Corpus)
   - 提取一个 corpus 文档
   - 获取该文档的所有问题
   - 创建新的 GraphRAG 实例
   - 为该文档建图
   - 查询该文档的所有问题
   - 保存结果

3. **汇总结果** (Aggregate Results)
   - 合并所有 corpus 的结果
   - 运行评估

## 输出结构 (Output Structure)

```
working_dir/
└── exp_name/
    ├── Results/
    │   ├── corpus_0_results.json      # 第一个corpus的结果
    │   ├── corpus_1_results.json      # 第二个corpus的结果
    │   └── all_results.json           # 合并结果
    ├── Metrics/
    │   └── metrics.json               # 评估指标
    └── [index_name]_corpus_[N]/       # 每个corpus的图存储
```

## 关键特性 (Key Features)

✅ **完全隔离** - 每个 corpus 样本完全独立处理
✅ **独立存储** - 每个图都有唯一的命名空间
✅ **问题过滤** - 只查询属于对应 corpus 的问题  
✅ **详细日志** - 全程记录处理过程
✅ **错误处理** - 完善的错误检查和处理
✅ **安全检查** - 通过 CodeQL 安全扫描

✅ **Complete Isolation** - Each corpus sample processed independently
✅ **Separate Storage** - Each graph has unique namespace
✅ **Question Filtering** - Only queries questions for corresponding corpus
✅ **Detailed Logging** - Comprehensive processing logs
✅ **Error Handling** - Robust error checking and handling
✅ **Security Checked** - Passed CodeQL security scan

## 与标准模式对比 (Comparison with Standard Mode)

| 特性 | 标准模式 | Per-Corpus 模式 |
|------|---------|----------------|
| 图构建 | 所有文档一个图 | 每个文档独立图 |
| 问题过滤 | 无过滤 | 按 doc_id 过滤 |
| 隔离性 | 文档间可能有连接 | 完全隔离 |
| 内存使用 | 较高 | 较低（逐个处理） |

## 测试验证 (Testing)

✅ 代码审查通过
✅ 安全扫描通过（0个漏洞）
✅ 逻辑验证完成
✅ 文档完整

✅ Code review passed
✅ Security scan passed (0 vulnerabilities)
✅ Logic validation completed
✅ Documentation complete

## 下一步使用 (Next Steps)

1. 配置 LLM 设置在 `Option/Config2.yaml`
2. 准备数据集（包含 Corpus.json 和 Question.json，且问题需要有 doc_id 字段）
3. 运行命令：`python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name your_dataset`
4. 查看结果在 `Results/` 目录

1. Configure LLM settings in `Option/Config2.yaml`
2. Prepare dataset (with Corpus.json and Question.json, questions must have doc_id field)
3. Run: `python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name your_dataset`
4. Check results in `Results/` directory

## 文档链接 (Documentation Links)

- 详细使用指南: `Doc/PER_CORPUS_MODE.md`
- 模式对比: `Doc/MODES_COMPARISON.md`
- 测试数据: `Data/TestDataset/`
- 示例脚本: `run_per_corpus_example.sh`

## 技术说明 (Technical Notes)

- 每个 corpus 使用唯一的 index_name: `{original_index_name}_corpus_{idx}`
- 图存储在独立的命名空间，避免冲突
- 内存占用稳定，不会随 corpus 数量线性增长
- 支持 `doc_id` 和 `corpus_id` 两种字段名

- Each corpus uses unique index_name: `{original_index_name}_corpus_{idx}`
- Graphs stored in separate namespaces to avoid conflicts
- Stable memory usage, doesn't grow linearly with corpus count
- Supports both `doc_id` and `corpus_id` field names

---

**Implementation Complete! 实现完成！** 🎉
