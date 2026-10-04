# 环境安装指南

## 当前项目必需环境

### Python

建议：

```text
Python 3.10 或 3.11
```

当前检测到：

```text
Python 3.10.6
```

可用。

### Python 核心依赖

核心依赖在：

```text
requirements-core.txt
```

包括：

- `langgraph`：Agent 工作流编排
- `openai`：OpenAI-compatible SDK fallback
- `python-dotenv`：读取 `.env`
- `requests`：网页下载与 HTTP 请求
- `beautifulsoup4`：网页解析
- `fastapi`：实践版后端 API
- `uvicorn`：FastAPI 本地服务
- `qdrant-client`：Qdrant Python client

安装：

```powershell
.\scripts\setup_env.ps1
```

或手动：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-core.txt
```

## Qdrant 环境

实践版推荐使用 Qdrant。

推荐安装：

```text
Docker Desktop for Windows
```

安装 Docker 后启动：

```powershell
docker compose up -d qdrant
```

Qdrant 地址：

```text
REST API: http://127.0.0.1:6333
Dashboard: http://127.0.0.1:6333/dashboard
```

当前检测结果：

```text
docker: 未安装或不在 PATH
```

## 以后 Agent/RAG 开发推荐环境

### 基础 Agent 开发

- `langgraph`
- `langchain`
- `openai`
- `anthropic`
- `python-dotenv`
- `pydantic`
- `fastapi`
- `uvicorn`

### RAG 和向量库

- `qdrant-client`
- `chromadb`
- `pymilvus`
- `pgvector`
- `sentence-transformers`
- `rank-bm25`
- `FlagEmbedding`

建议优先：

```text
Qdrant + sentence-transformers + rank-bm25 + reranker
```

### 文档解析

- `pypdf`
- `python-docx`
- `unstructured`
- `beautifulsoup4`
- `markdown`

### 评估与工程质量

- `pytest`
- `ruff`
- `ragas`
- `pandas`
- `scikit-learn`

### 系统工具

- Docker Desktop
- Git
- VS Code 或 PyCharm
- Postman / Bruno / Hoppscotch

## 推荐安装策略

先装核心依赖：

```powershell
.\scripts\setup_env.ps1
```

等核心项目跑通后，再装扩展依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-rag-extra.txt
```

不要一开始就装全部大依赖，尤其是 `sentence-transformers`、`FlagEmbedding`、`unstructured`，这些包较大，安装时间更长。
