---
title: Agent 工具调用安全规范
source: fake_company
department: AI Platform
access_level: internal
tags: agent, tools, security
---

# Agent 工具调用安全规范

## 工具分级

Agent 工具分为只读工具、低风险写工具和高风险写工具。知识库搜索、文档读取、摘要生成属于只读工具。创建草稿、保存临时文件属于低风险写工具。删除数据、发送邮件、修改数据库、调用支付接口属于高风险写工具。

## 人工确认

高风险写工具必须经过用户确认后才能执行。确认信息必须包含操作对象、影响范围、关键参数和可回滚方案。用户只提出意图但未明确确认时，Agent 不得执行高风险操作。

## 最小权限

Agent 只能访问完成当前任务所需的数据源和工具。不同部门文档需要通过 access_level 和 department 字段进行权限过滤。

## 审计日志

所有工具调用都要记录 tool_name、input、output_summary、status、created_at 和 operator。失败调用也必须记录，便于排查安全问题。
