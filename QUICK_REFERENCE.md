# Quick Reference Guide - GraphRAG Advanced Features

## 快速参考指南 - GraphRAG 高级功能

This guide covers the main advanced features added to GraphRAG.

本指南涵盖添加到 GraphRAG 的主要高级功能。

---

## Feature 1: Multiple-Choice Question Support / 功能1：选择题支持

### What it does / 功能说明
Support evaluation of multiple-choice questions using close-set evaluation mode.

支持使用 close-set 评估模式评估选择题。

### When to use / 使用场景
- Testing with multiple-choice questions / 使用选择题进行测试
- Evaluating model's option selection ability / 评估模型的选项选择能力
- Comparing with standardized test datasets / 与标准化测试数据集进行比较

### Usage / 使用方法
```bash
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name quality_example
```

### Requirements / 要求
Questions must have `answer_idx` field with the option letter:
```json
{
  "question": "Who created Python?\nA: James\nB: Guido\nC: Dennis\nD: Bjarne",
  "answer": "Guido van Rossum",
  "answer_idx": "B",
  "doc_id": 0
}
```

### Key Points / 要点
- Dataset name should include "quality" to trigger close-set mode
- 数据集名称应包含 "quality" 以触发 close-set 模式
- See example: `Data/MultipleChoiceExample/`
- 查看示例：`Data/MultipleChoiceExample/`

📖 **Documentation**: `Doc/MULTIPLE_CHOICE_SUPPORT.md`

---

## Feature 2: Per-Corpus Graph Processing / 功能2：按语料库样本独立建图

### What it does / 功能说明
Build separate graphs for each corpus document and answer only the questions related to that document.

为每个语料库文档构建独立的图，并仅回答与该文档相关的问题。

### When to use / 使用场景
- Each question relates to a specific document / 每个问题都与特定文档相关
- You want to avoid cross-document interference / 想避免跨文档干扰
- Need per-document performance analysis / 需要按文档分析性能

### Usage / 使用方法
```bash
python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name your_dataset
```

### Requirements / 要求
Questions must have `doc_id` or `corpus_id` field:
```json
{"question": "...", "answer": "...", "doc_id": 0}
```

### Output / 输出
```
Results/
├── corpus_0_results.json  # Per-corpus results
├── corpus_1_results.json
└── all_results.json       # Combined
```

📖 **Documentation**: `Doc/PER_CORPUS_MODE.md`

---

## Feature 3: Separate LLMs for Building and Querying / 功能3：建图和查询使用不同的大模型

### What it does / 功能说明
Use different LLM models for graph construction vs. question answering.

在图构建和问题回答中使用不同的大模型。

### When to use / 使用场景
- Use powerful model for graphs, cheaper model for queries / 用强大模型建图，便宜模型查询
- Use cloud for building, local (Ollama) for answering / 云端建图，本地(Ollama)回答
- Privacy: keep answers on local machine / 隐私：答案保留在本地机器

### Configuration / 配置
```yaml
# Graph building LLM / 建图大模型
llm:
  api_type: "openai"
  model: "gpt-4"
  api_key: "sk-..."

# Query answering LLM / 查询大模型
query_llm:
  api_type: "ollama"
  base_url: "http://localhost:11434/v1"
  model: "qwen2.5:14b"
  api_key: "ollama"
```

### Usage / 使用方法
```bash
# Works with both main.py and main_per_corpus.py
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name your_dataset
```

📖 **Documentation**: `Doc/SEPARATE_LLMS.md`

---

## Combining Both Features / 组合使用两个功能

You can use both features together!

可以同时使用两个功能！

### Example: Per-Corpus + Dual LLM / 示例：独立建图 + 双模型

**Config2.yaml:**
```yaml
llm:
  api_type: "openai"
  model: "gpt-4"
  api_key: "sk-..."

query_llm:
  api_type: "ollama"
  base_url: "http://localhost:11434/v1"
  model: "qwen2.5:14b"
  api_key: "ollama"
```

**Run:**
```bash
python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name your_dataset
```

**Result:**
- Each corpus gets its own graph (built with GPT-4)
- Each corpus's questions answered by local Ollama
- Complete isolation + cost savings + privacy

结果：
- 每个语料库都有自己的图（用 GPT-4 构建）
- 每个语料库的问题由本地 Ollama 回答
- 完全隔离 + 节省成本 + 保护隐私

---

## Quick Start Checklist / 快速开始检查清单

### For Per-Corpus Mode / 独立建图模式

- [ ] Prepare data with `Corpus.json` and `Question.json`
- [ ] Ensure questions have `doc_id` or `corpus_id` field
- [ ] Use `main_per_corpus.py` instead of `main.py`
- [ ] Check results in `Results/corpus_*_results.json`

### For Dual LLM Mode / 双模型模式

- [ ] Configure `llm` in `Config2.yaml`
- [ ] Add `query_llm` configuration (optional)
- [ ] If using Ollama:
  - [ ] Install Ollama (`curl -fsSL https://ollama.com/install.sh | sh`)
  - [ ] Pull model (`ollama pull qwen2.5:14b`)
  - [ ] Verify running (`curl http://localhost:11434/v1/models`)
- [ ] Run as normal with either `main.py` or `main_per_corpus.py`

---

## Common Configurations / 常用配置

### Config 1: All Cloud / 全部云端
```yaml
llm:
  api_type: "openai"
  model: "gpt-4"

query_llm:
  api_type: "openai"
  model: "gpt-3.5-turbo"  # Cheaper for queries
```

### Config 2: Cloud + Local / 云端 + 本地
```yaml
llm:
  api_type: "openai"
  model: "gpt-4"

query_llm:
  api_type: "ollama"
  base_url: "http://localhost:11434/v1"
  model: "qwen2.5:14b"
```

### Config 3: All Local / 全部本地
```yaml
llm:
  api_type: "ollama"
  base_url: "http://localhost:11434/v1"
  model: "qwen2.5:14b"

# No query_llm needed - will use same model
```

### Config 4: Default (Single Model) / 默认（单模型）
```yaml
llm:
  api_type: "openai"
  model: "gpt-4"

# No query_llm - uses llm for everything
```

---

## Troubleshooting / 常见问题

### Per-Corpus Mode Issues

**Q**: No questions found for corpus X  
**A**: Check that questions have matching `doc_id` field

**Q**: Questions in Question.json missing doc_id field / Question.json 中的问题缺少 doc_id 字段  
**A**: Add doc_id field to each question / 为每个问题添加 doc_id 字段

### Dual LLM Mode Issues

**Q**: Ollama not responding  
**A**: Run `ollama serve` and check `http://localhost:11434`

**Q**: Model not found  
**A**: Pull the model: `ollama pull qwen2.5:14b`

**Q**: Still using same model for queries  
**A**: Check that `query_llm` is properly configured in Config2.yaml

---

## File Locations / 文件位置

```
GraphRAG/
├── main.py                          # Standard mode
├── main_per_corpus.py               # Per-corpus mode
├── Option/
│   ├── Config2.yaml                 # Main config (add query_llm here)
│   └── Method/
│       ├── RAPTOR.yaml              # Standard RAPTOR
│       └── RAPTOR_DualLLM.yaml      # Example with dual LLM
├── Doc/
│   ├── PER_CORPUS_MODE.md           # Per-corpus docs
│   ├── SEPARATE_LLMS.md             # Dual LLM docs
│   ├── MODES_COMPARISON.md          # Comparison guide
│   └── WORKFLOW_DIAGRAM.md          # Visual workflow
└── Data/
    └── TestDataset/                 # Example dataset
```

---

## Support / 支持

- Per-corpus feature docs: `Doc/PER_CORPUS_MODE.md`
- Dual LLM feature docs: `Doc/SEPARATE_LLMS.md`
- Mode comparison: `Doc/MODES_COMPARISON.md`
- Workflow diagram: `Doc/WORKFLOW_DIAGRAM.md`

For questions, check the documentation or review the example configurations.

有问题请查看文档或参考示例配置。
