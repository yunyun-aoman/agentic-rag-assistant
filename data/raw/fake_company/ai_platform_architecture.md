---
title: AI 平台知识库架构说明
source: fake_company
department: AI Platform
access_level: internal
tags: architecture, rag, langgraph
---

# AI 平台知识库架构说明

## 总体架构

知识库助手由文档接入层、处理层、索引层、检索层、Agent 编排层和应用层组成。文档接入层负责读取 Markdown、PDF、网页和内部知识文档。处理层负责清洗、切分和 metadata 标准化。索引层负责 embedding 和向量存储。

## Agent 编排

Agent 使用 LangGraph 编排，核心节点包括 classify_question、rewrite_query、retrieve_context、generate_answer 和 cite_sources。复杂任务可以增加 plan_subquestions、multi_retrieve 和 reflect_answer 节点。

## 检索增强生成

系统先检索相关 chunk，再将检索内容注入 prompt。回答必须只基于知识库上下文生成，不允许编造来源。上下文不足时应提示用户补充资料或扩大检索范围。

## 可扩展能力

后续可以接入 reranker、hybrid search、权限过滤、评估集和反馈闭环。向量数据库可以从本地索引迁移到 Qdrant、Milvus 或 pgvector。
