---
title: RAG 知识库开发规范
source: fake_company
department: AI Platform
access_level: internal
tags: rag, ingestion, citation
---

# RAG 知识库开发规范

## 文档入库规则

所有进入知识库的文档必须包含 metadata，包括 document_id、title、source、author、department、created_at、tags、access_level。缺少 title 或 source 的文档不能进入正式索引。

## Chunk 切分规范

技术文档优先按照标题层级切分，单个 chunk 建议控制在 500 到 800 tokens。代码块、表格和配置片段不能被切断。每个 chunk 必须保留 parent_doc_id、section_title 和 chunk_id。

## 检索策略

默认使用语义检索 top_k=8。复杂问题需要先进行 query rewrite，将用户口语化问题改写成适合检索的关键词和子问题。涉及多个主题的问题应拆成多个检索查询。

## 引用要求

知识库回答必须附带来源引用，至少包含文档标题、章节标题和 chunk_id。无法在知识库中找到依据时，系统应明确说明没有检索到可靠依据。

## 质量排查

每次问答应记录原始问题、改写问题、召回 chunk、相似度分数和最终引用，便于后续分析召回失败、幻觉和答案不完整问题。
