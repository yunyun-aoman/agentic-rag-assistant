---
title: 文档入库流程说明
source: fake_company
department: Knowledge Management
access_level: internal
tags: ingestion, metadata, chunking
---

# 文档入库流程说明

## 入库步骤

文档入库包括采集、格式转换、清洗、切分、metadata 生成、embedding、写入索引和抽样验证。抽样验证需要检查标题、来源、章节、chunk 边界和引用是否正确。

## 文档清洗

清洗阶段需要去除导航栏、页脚、重复空行和无意义版权声明。保留标题层级、代码块、表格和关键列表。

## Metadata 字段

标准 metadata 包含 title、source、path、section、chunk_id、created_at、tags 和 access_level。面向企业场景时还应加入 department、owner 和 confidentiality。

## 更新策略

同一文档重复入库时，应根据 path 和内容 hash 判断是否更新。过期 chunk 需要从索引中删除或标记为 inactive。
