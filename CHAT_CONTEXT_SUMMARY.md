# 当前对话上下文总结

## 已完成事项

1. 创建了 `Agentic RAG Knowledge Base Assistant` 项目。
2. 项目已迁移到 `F:\codex\projects\agentic-rag-assistant`。
3. 用户偏好：以后类似 agent/demo/practice 项目优先放到 C 盘以外，例如 `F:\codex\projects\...`。
4. 已接入阿里云 DashScope。
5. 模型配置为 `qwen3.7-plus`。
6. DashScope Anthropic 兼容接口已真实跑通。
7. 发现本机代理 `127.0.0.1:10808` 会导致 DashScope TLS 握手失败，代码已改为调用 DashScope 时绕过系统代理。
8. Web UI 已可运行，状态显示为 `DashScope qwen3.7-plus`。

## 当前版本能力

```text
Markdown 模拟知识库
  ↓
文档切分与本地索引
  ↓
本地检索器
  ↓
LangGraph Agent
  ↓
DashScope qwen3.7-plus
  ↓
Web UI + 来源引用
```

## 当前关键限制

当前版本仍偏 MVP：

- 向量库还是本地 JSONL 检索器。
- Web 服务还是标准库 HTTP server。
- 没有 FastAPI。
- 没有 Qdrant。
- 没有真实 embedding。
- 没有 reranker。
- 没有文档管理 API。
- 没有检索评估体系。

## 新目标

用户明确表示不想只做 demo，而是想做实际实践项目。

新项目定位：

```text
面向 AI 工程团队的企业知识库 Agentic RAG Assistant
```

推荐升级路线：

```text
Web UI
  ↓
FastAPI Backend
  ↓
LangGraph Agent
  ↓
Retriever Layer
  ↓
Qdrant Vector Database
  ↓
Document Ingestion Pipeline
  ↓
Markdown / PDF / TXT / Web Docs / 模拟企业文档
```

## 技术选择

推荐 Qdrant，而不是 Milvus：

- Qdrant 比 Chroma 更工程化。
- Qdrant 比 Milvus 更轻，适合个人电脑实践。
- 支持 payload metadata filter。
- 支持 dense/sparse/hybrid retrieval。
- 有 REST API、gRPC、Dashboard 和 Python client。

Milvus 后续可作为大规模生产方案对比，不建议现在直接上。

## 本次开始实施内容

第一阶段实施目标：

1. 新增实践版项目路线文档。
2. 新增 `docker-compose.yml` 启动 Qdrant。
3. 新增 FastAPI 后端骨架。
4. 新增 Qdrant HTTP retriever/indexer 原型。
5. 保留原 `src/` 版本作为可运行 fallback。

## 权限说明

当前会话没有 `F:\codex\projects\agentic-rag-assistant` 写权限，所以本次先在当前可写工作区 staging：

```text
C:\Users\86185\Documents\Codex\2026-09-29\rag-chatgpt-conversation-6aba04e9-9774-83e8\work\agentic-rag-assistant-practical-20260929-125429
```

等 F 盘项目写权限恢复后，再把 staging 里的新增文件同步到正式项目目录。
