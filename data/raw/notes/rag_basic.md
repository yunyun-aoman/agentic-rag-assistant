# RAG 基础学习笔记

RAG 是 Retrieval-Augmented Generation 的缩写，核心思想是先从外部知识库检索相关内容，再让大语言模型基于检索内容生成答案。它可以降低幻觉、接入私有知识，并让回答带有来源。

一个基础 RAG pipeline 包括文档加载、文本清洗、chunk 切分、embedding、向量存储、用户查询、语义检索、上下文拼接、LLM 生成和来源引用。

Agentic RAG 在普通 RAG 上加入了任务判断、查询改写、多轮检索、工具调用、反思和路由能力。LangGraph 适合表达这种带状态、带分支、可观察的工作流。
