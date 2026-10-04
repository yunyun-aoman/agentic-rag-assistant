# Agentic RAG Knowledge Base Assistant

基于 LangGraph 的轻量 Agentic RAG 知识库助手。它用公开技术资料和自建模拟企业文档来模拟企业内部知识库，适合学习、课程项目和面试展示。

## 功能

- 本地 Markdown 知识库入库
- Chunk 切分、metadata 管理、本地向量索引
- LangGraph 节点编排：问题分析 -> 查询改写 -> 检索 -> 生成回答
- 无 API key 也能演示检索与引用
- 有 `OPENAI_API_KEY` 时自动调用 LLM 生成更自然的答案
- 可下载公开技术文档作为扩展知识库

## 快速开始

```bash
cd outputs/agentic-rag-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/download_docs.py
python -m src.ingest
python -m src.cli
```

如果不想配置 API key，可以直接运行，系统会用检索片段生成演示答案。

如需 LLM 生成：

```bash
copy .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY
python -m src.cli
```

## 示例问题

```text
RAG 文档入库需要哪些 metadata？
Agent 哪些工具调用需要人工确认？
如何设计一个带查询改写的 RAG 流程？
对比 Qdrant、Milvus 和 pgvector 的适用场景。
为什么知识库回答需要来源引用？
```

## 目录

```text
data/raw/fake_company/  自建模拟企业文档
data/raw/notes/         学习笔记
data/raw/web_docs/      在线下载的公开文档
data/index/             本地索引
scripts/download_docs.py 下载公开资料
src/ingest.py           文档入库与索引构建
src/retriever.py        本地向量检索
src/graph_agent.py      LangGraph Agent 编排
src/cli.py              命令行交互入口
```

## 面试表述

本项目没有使用真实公司数据，而是采用公开技术资料和自建模拟企业规范文档，构建一个 AI 工程团队内部知识库。系统覆盖文档入库、切分、向量化、检索、Agent 编排、答案生成和来源引用等 RAG 核心流程。后续接入真实企业数据时，只需要替换数据连接器、权限控制和向量数据库后端。
