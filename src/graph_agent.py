import os
from typing import TypedDict

from .config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MODEL,
    LLM_PROVIDER,
    LLM_TIMEOUT_SECONDS,
)
from .retriever import LocalVectorStore


class AgentState(TypedDict, total=False):
    question: str
    task_type: str
    rewritten_query: str
    contexts: list[dict]
    answer: str


def classify_question(state: AgentState) -> AgentState:
    q = state["question"].lower()
    if any(x in q for x in ["compare", "difference", "vs", "\u5bf9\u6bd4", "\u6bd4\u8f83", "\u533a\u522b", "\u5dee\u5f02"]):
        task_type = "compare"
    elif any(x in q for x in ["summary", "summarize", "overview", "\u603b\u7ed3", "\u6982\u62ec", "\u5f52\u7eb3"]):
        task_type = "summarize"
    elif any(x in q for x in ["design", "architecture", "plan", "workflow", "\u8bbe\u8ba1", "\u65b9\u6848", "\u67b6\u6784", "\u6d41\u7a0b"]):
        task_type = "design"
    else:
        task_type = "lookup"
    return {**state, "task_type": task_type}


def rewrite_query(state: AgentState) -> AgentState:
    q = state["question"]
    task_type = state.get("task_type", "lookup")
    lowered = q.lower()
    safety_terms = [
        "tool", "confirm", "safety", "permission", "delete", "email", "send",
        "\u5de5\u5177", "\u786e\u8ba4", "\u5b89\u5168", "\u6743\u9650", "\u5220\u9664", "\u90ae\u4ef6", "\u53d1\u9001",
    ]
    if any(x in lowered for x in safety_terms):
        rewritten = f"{q} tool policy confirmation permissions safety"
    elif task_type == "compare":
        rewritten = f"{q} comparison differences tradeoffs"
    elif task_type == "summarize":
        rewritten = f"{q} summary key points"
    elif task_type == "design":
        rewritten = f"{q} architecture workflow implementation"
    else:
        rewritten = q
    return {**state, "rewritten_query": rewritten}


def _search_qdrant(query: str, top_k: int) -> list[dict]:
    from app.retriever.qdrant_http import QdrantHttpStore

    store = QdrantHttpStore()
    return store.search(query=query, top_k=top_k)


def retrieve_context(state: AgentState) -> AgentState:
    query = state.get("rewritten_query") or state["question"]
    vector_db = os.getenv("VECTOR_DB", "qdrant").lower()

    contexts: list[dict] = []
    if vector_db == "qdrant":
        try:
            contexts = _search_qdrant(query, top_k=6)
        except Exception as exc:
            print(f"Qdrant retrieval failed; falling back to local JSONL: {exc}")

    if not contexts:
        store = LocalVectorStore()
        contexts = store.search(query=query, top_k=6)

    return {**state, "contexts": contexts}


def _format_context(contexts: list[dict]) -> str:
    lines = []
    for i, item in enumerate(contexts, start=1):
        title = item.get("title") or item.get("source") or f"chunk {i}"
        text = item.get("text") or item.get("content") or ""
        lines.append(f"[{i}] {title}\n{text}")
    return "\n\n".join(lines)


def _call_openai_compatible(prompt: str) -> str:
    from openai import OpenAI

    if not LLM_API_KEY:
        raise RuntimeError("LLM_API_KEY is not configured")
    if not LLM_MODEL:
        raise RuntimeError("LLM_MODEL is not configured")

    kwargs = {"api_key": LLM_API_KEY, "timeout": LLM_TIMEOUT_SECONDS}
    if LLM_BASE_URL:
        kwargs["base_url"] = LLM_BASE_URL
    client = OpenAI(**kwargs)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "\u4f60\u662f\u4e00\u4e2a\u8c28\u614e\u7684\u4f01\u4e1a\u77e5\u8bc6\u5e93 RAG \u52a9\u624b\u3002"
                    "\u4f18\u5148\u6839\u636e\u68c0\u7d22\u5230\u7684\u4e0a\u4e0b\u6587\u56de\u7b54\uff0c"
                    "\u5982\u679c\u4fe1\u606f\u4e0d\u8db3\u8981\u660e\u786e\u8bf4\u660e\u3002"
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def _fallback_answer(contexts: list[dict], reason: str = "") -> str:
    snippets = "\n\n".join(
        f"- {item.get('title') or item.get('source') or 'source'}: "
        f"{(item.get('text') or item.get('content') or '')[:300]}"
        for item in contexts[:3]
    )
    prefix = "\u5df2\u5b8c\u6210\u77e5\u8bc6\u5e93\u68c0\u7d22\uff0c\u4f46\u5927\u6a21\u578b\u8c03\u7528\u6682\u65f6\u6ca1\u6709\u6210\u529f\u3002"
    if reason:
        prefix += f"\n\u539f\u56e0\uff1a{reason}"
    return f"{prefix}\n\n\u76f8\u5173\u7247\u6bb5\uff1a\n{snippets}"


def generate_answer(state: AgentState) -> AgentState:
    question = state["question"]
    contexts = state.get("contexts", [])
    context_text = _format_context(contexts)
    prompt = f"""\u8bf7\u57fa\u4e8e\u68c0\u7d22\u5230\u7684\u4e0a\u4e0b\u6587\u56de\u7b54\u95ee\u9898\u3002

\u95ee\u9898\uff1a
{question}

\u68c0\u7d22\u4e0a\u4e0b\u6587\uff1a
{context_text}

\u8981\u6c42\uff1a
- \u7528\u4e2d\u6587\u56de\u7b54\u3002
- \u5982\u679c\u4e0a\u4e0b\u6587\u4e0d\u8db3\uff0c\u8bf7\u660e\u786e\u8bf4\u660e\u3002
- \u56de\u7b54\u8981\u7b80\u6d01\u3001\u5b9e\u7528\u3002
- \u5fc5\u8981\u65f6\u7528 [1]\u3001[2] \u6807\u6ce8\u6765\u6e90\u3002
"""

    try:
        if LLM_PROVIDER in {"openai_compatible", "openai", "dashscope"} and LLM_API_KEY:
            answer = _call_openai_compatible(prompt)
        else:
            answer = _fallback_answer(contexts, "\u672a\u914d\u7f6e LLM_API_KEY")
    except Exception as exc:
        answer = _fallback_answer(contexts, str(exc))

    return {**state, "answer": answer}


def build_graph():
    def run(question: str) -> AgentState:
        state: AgentState = {"question": question}
        state = classify_question(state)
        state = rewrite_query(state)
        state = retrieve_context(state)
        state = generate_answer(state)
        return state

    return run


def ask(question: str) -> AgentState:
    return build_graph()(question)
