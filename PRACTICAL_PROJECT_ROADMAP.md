# Agentic RAG Assistant 实践项目路线

## 项目定位

本项目升级为：

```text
面向 AI 工程团队的企业知识库 Agentic RAG Assistant
```

它不是单纯 demo，而是一个可持续迭代的实践项目，目标是接近真实企业知识库助手的工程形态。

## 实践版架构

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

## 阶段规划

### V1 工程化闭环

- FastAPI 后端
- Qdrant Docker
- Qdrant collection 初始化
- 文档入库写入 Qdrant
- 问答接口调用 LangGraph Agent
- 保留来源引用

### V2 检索质量增强

- 真实 embedding 模型
- metadata filter
- query rewrite
- 多路检索
- reranker
- 检索日志

### V3 准生产能力

- PDF / Word / Web 文档解析
- 文档管理页面
- 用户会话管理
- 评估集
- Docker Compose 一键启动
- 错误日志和调用追踪

### V4 高级 Agentic RAG

- hybrid search
- multi-query retrieval
- route by task type
- answer reflection
- citation verification
- tool permission guard

## 为什么选择 Qdrant

Qdrant 适合当前实践项目：

- 比本地 JSONL 检索器更真实。
- 比 Chroma 更有工程感。
- 比 Milvus 更轻，适合个人电脑和 Docker。
- 支持 payload metadata filter。
- 支持 dense/sparse/hybrid retrieval。
- 有 REST API、gRPC、Dashboard 和 Python client。

## 面试表述

这个项目最初是一个 Agentic RAG MVP，用于验证文档入库、检索、LangGraph 编排和来源引用。后续我将它升级为实践项目，引入 Qdrant 作为向量数据库，使用 FastAPI 提供后端服务，并逐步加入 metadata filter、hybrid search、reranker、文档管理和评估体系，使它更接近企业知识库助手的真实工程形态。
