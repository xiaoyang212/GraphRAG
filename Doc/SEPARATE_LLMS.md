# Using Separate LLMs for Graph Building and Query Answering

## 使用不同的大模型进行建图和回答问题

## Overview / 概述

GraphRAG now supports using **different LLMs** for different stages of the pipeline:
- **Graph Building LLM**: Used for extracting entities, relationships, and building the knowledge graph
- **Query LLM**: Used for answering questions based on the retrieved context

GraphRAG 现在支持在不同阶段使用**不同的大模型**：
- **建图大模型**：用于提取实体、关系和构建知识图谱
- **查询大模型**：用于基于检索到的上下文回答问题

This is useful when you want to:
- Use a powerful cloud-based model for graph construction (better quality)
- Use a local/cheaper model for query answering (lower cost, privacy)
- Use specialized models for different tasks

这在以下场景很有用：
- 使用强大的云端模型进行图构建（更高质量）
- 使用本地/更便宜的模型进行查询回答（降低成本，保护隐私）
- 针对不同任务使用专门的模型

## Configuration / 配置方法

### Basic Configuration / 基础配置

Edit your `Config2.yaml` file:

编辑你的 `Config2.yaml` 文件：

```yaml
# Main LLM for graph building / 用于建图的主模型
llm:
  api_type: "openai"  # or "open_llm"
  base_url: 'https://api.openai.com/v1'
  model: "gpt-4"
  api_key: "YOUR_OPENAI_API_KEY"

# Optional: Separate LLM for query answering / 可选：用于回答问题的独立模型
query_llm:
  api_type: "ollama"  # Use local Ollama
  base_url: 'http://localhost:11434/v1'
  model: "qwen2.5:14b"  # Your Ollama model
  api_key: "ollama"  # Ollama doesn't need a real API key
```

### Example Configurations / 配置示例

#### Example 1: Cloud for Building, Local for Querying / 示例1：云端建图，本地查询

```yaml
# Use GPT-4 for high-quality graph construction
llm:
  api_type: "openai"
  base_url: 'https://api.openai.com/v1'
  model: "gpt-4-turbo"
  api_key: "sk-..."
  temperature: 0.0

# Use local Ollama for query answering (privacy + cost savings)
query_llm:
  api_type: "ollama"
  base_url: 'http://localhost:11434/v1'
  model: "llama3:8b"
  api_key: "ollama"
  temperature: 0.0
```

#### Example 2: Different Cloud Models / 示例2：不同的云端模型

```yaml
# Use GPT-4 for graph building (better reasoning)
llm:
  api_type: "openai"
  base_url: 'https://api.openai.com/v1'
  model: "gpt-4"
  api_key: "sk-..."

# Use GPT-3.5 for query answering (faster, cheaper)
query_llm:
  api_type: "openai"
  base_url: 'https://api.openai.com/v1'
  model: "gpt-3.5-turbo"
  api_key: "sk-..."
```

#### Example 3: Same Model (Default Behavior) / 示例3：相同模型（默认行为）

```yaml
# Single LLM for both stages
llm:
  api_type: "openai"
  model: "gpt-4"
  api_key: "sk-..."

# No query_llm specified = use main llm for everything
# 不指定 query_llm = 所有阶段都使用主模型
```

## Which LLM is Used Where / 不同阶段使用的模型

### Graph Building Stage (uses `llm`) / 建图阶段（使用 `llm`）

The main `llm` is used for:
- Entity extraction / 实体提取
- Relationship extraction / 关系提取
- Graph construction / 图构建
- Community detection (if enabled) / 社区检测（如果启用）
- Summary generation / 摘要生成

### Query Stage (uses `query_llm` if set, otherwise `llm`) / 查询阶段（使用 `query_llm`，如未设置则使用 `llm`）

The `query_llm` (or `llm` if not set) is used for:
- Question answering / 问题回答
- Context-based generation / 基于上下文的生成
- Query refinement / 查询优化

## Setting Up Ollama Locally / 本地设置 Ollama

If you want to use Ollama for query answering:

如果你想使用 Ollama 进行查询回答：

### 1. Install Ollama / 安装 Ollama

```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Or download from https://ollama.com/download
```

### 2. Pull a Model / 下载模型

```bash
# Chinese models / 中文模型
ollama pull qwen2.5:14b
ollama pull qwen2.5:7b

# English models / 英文模型
ollama pull llama3:8b
ollama pull mistral:7b
```

### 3. Verify Ollama is Running / 验证 Ollama 运行

```bash
# Check if Ollama is running
curl http://localhost:11434/v1/models

# Or start Ollama
ollama serve
```

### 4. Configure in Config2.yaml / 在 Config2.yaml 中配置

```yaml
query_llm:
  api_type: "ollama"
  base_url: 'http://localhost:11434/v1'
  model: "qwen2.5:14b"  # Your model name
  api_key: "ollama"
```

## Supported API Types / 支持的 API 类型

Both `llm` and `query_llm` support:
- `openai` - OpenAI API
- `open_llm` - Generic OpenAI-compatible API
- `ollama` - Local Ollama
- `fireworks` - Fireworks.ai
- And others (see `LLMConfig`)

## Cost and Performance Considerations / 成本和性能考虑

### Cost Optimization / 成本优化

| Strategy | Graph Building | Query Answering | Benefit |
|----------|----------------|-----------------|---------|
| High-Low | GPT-4 | GPT-3.5-turbo | Better graphs, lower query cost |
| Cloud-Local | GPT-4 | Ollama (local) | Best graphs, minimal query cost |
| All-Local | Ollama | Ollama | No API costs |

### Performance Trade-offs / 性能权衡

- **Graph Quality**: Better LLM for graph building = better entity/relationship extraction
- **Query Quality**: Better LLM for querying = better answer quality
- **Speed**: Local models (Ollama) = faster response time, no network latency
- **Privacy**: Local models = data stays on your machine

## Example Usage / 使用示例

```bash
# Standard mode with separate LLMs
python main.py -opt Option/Method/RAPTOR.yaml -dataset_name your_dataset

# Per-corpus mode with separate LLMs
python main_per_corpus.py -opt Option/Method/RAPTOR.yaml -dataset_name your_dataset
```

The system will automatically:
1. Use `llm` for graph building / 使用 `llm` 进行建图
2. Use `query_llm` (if set) for answering questions / 使用 `query_llm`（如果设置）回答问题
3. Log which model is being used / 记录使用的模型

## Troubleshooting / 故障排除

### Issue: Ollama not responding / 问题：Ollama 无响应

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### Issue: Model not found / 问题：模型未找到

```bash
# List available models
ollama list

# Pull the model you need
ollama pull qwen2.5:14b
```

### Issue: Wrong API key error / 问题：API 密钥错误

For Ollama, you can use any string as the API key:
```yaml
query_llm:
  api_key: "ollama"  # or "not-needed" or any string
```

## Advanced Configuration / 高级配置

You can configure different parameters for each LLM:

```yaml
llm:
  model: "gpt-4"
  temperature: 0.0  # Deterministic for graph building
  max_token: 4096

query_llm:
  model: "qwen2.5:14b"
  temperature: 0.3  # Slightly creative for answering
  max_token: 2048
  timeout: 300
```

## Notes / 注意事项

- If `query_llm` is not specified, the system will use `llm` for both stages
- Both LLMs must be accessible when running the system
- You can mix and match different API types (OpenAI + Ollama, etc.)
- Cost tracking works for both LLMs separately

如果未指定 `query_llm`，系统将在两个阶段都使用 `llm`
运行系统时两个大模型都必须可访问
可以混合使用不同的 API 类型（OpenAI + Ollama 等）
成本跟踪对两个大模型分别工作
