---
title: 向量数据库选型记录
source: fake_company
department: AI Platform
access_level: internal
tags: vector database, qdrant, milvus, pgvector
---

# 向量数据库选型记录

## Qdrant

Qdrant 易于部署，过滤条件表达能力强，适合中小型团队快速构建 RAG 服务。它适合需要 metadata 过滤、服务化部署和较低运维成本的场景。

## Milvus

Milvus 适合较大规模向量检索和更复杂的集群部署。它适合数据规模较大、并发要求较高、需要专业向量数据库能力的场景。

## pgvector

pgvector 可以直接复用 PostgreSQL，适合已有关系型数据库体系、数据规模不大、希望降低系统复杂度的项目。

## 本项目选择

学习和原型阶段使用本地向量索引，便于快速理解 RAG 流程。生产环境可根据规模迁移到 Qdrant、Milvus 或 pgvector。
