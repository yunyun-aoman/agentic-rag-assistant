import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .graph_agent import ask
from .ingest import build_index
from .retriever import LocalVectorStore


HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Agentic RAG Knowledge Base</title>
  <style>
    :root {
      --bg: #f6f7f9;
      --panel: #ffffff;
      --line: #dfe3ea;
      --text: #17202a;
      --muted: #667085;
      --accent: #2563eb;
      --accent-soft: #e8f0ff;
      --good: #0f766e;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
    }
    .app {
      min-height: 100vh;
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr);
    }
    aside {
      border-right: 1px solid var(--line);
      background: #fbfcfe;
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    main {
      display: grid;
      grid-template-rows: auto minmax(0, 1fr) auto;
      min-width: 0;
    }
    header {
      padding: 18px 26px;
      border-bottom: 1px solid var(--line);
      background: rgba(255,255,255,.94);
    }
    h1 {
      font-size: 20px;
      margin: 0 0 4px;
      letter-spacing: 0;
    }
    .sub { color: var(--muted); font-size: 13px; line-height: 1.5; }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
    }
    .label {
      font-size: 13px;
      font-weight: 700;
      margin-bottom: 10px;
    }
    .status {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px;
      align-items: center;
      font-size: 13px;
      color: var(--muted);
    }
    .pill {
      border: 1px solid #b7d7d3;
      color: var(--good);
      background: #edf8f6;
      border-radius: 999px;
      padding: 3px 9px;
      font-size: 12px;
      white-space: nowrap;
    }
    .examples { display: grid; gap: 8px; }
    button {
      border: 1px solid var(--line);
      background: #fff;
      color: var(--text);
      border-radius: 8px;
      padding: 10px 12px;
      cursor: pointer;
      font: inherit;
      text-align: left;
    }
    button:hover { border-color: #adc6ff; background: #f8fbff; }
    .primary {
      background: var(--accent);
      color: white;
      border-color: var(--accent);
      text-align: center;
      font-weight: 700;
    }
    .primary:hover { background: #1d4ed8; }
    .chat {
      padding: 24px 26px;
      overflow: auto;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .msg {
      max-width: 920px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px 16px;
      background: #fff;
      white-space: pre-wrap;
      line-height: 1.65;
      font-size: 14px;
    }
    .user {
      margin-left: auto;
      background: var(--accent-soft);
      border-color: #c7d7fe;
    }
    .meta {
      margin-top: 12px;
      display: grid;
      gap: 8px;
    }
    .source {
      border-left: 3px solid var(--accent);
      background: #f8fafc;
      padding: 9px 10px;
      font-size: 12px;
      color: #344054;
    }
    .source strong { display: block; color: #101828; margin-bottom: 3px; }
    form {
      border-top: 1px solid var(--line);
      background: #fff;
      padding: 14px 26px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 110px;
      gap: 10px;
    }
    textarea {
      resize: none;
      min-height: 46px;
      max-height: 160px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      font: inherit;
      line-height: 1.5;
      outline: none;
    }
    textarea:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(37,99,235,.12);
    }
    .flow { display: grid; gap: 8px; font-size: 13px; color: var(--muted); }
    .step { padding: 8px 10px; background: #fff; border: 1px solid var(--line); border-radius: 8px; }
    @media (max-width: 860px) {
      .app { grid-template-columns: 1fr; }
      aside { border-right: 0; border-bottom: 1px solid var(--line); }
      form { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="app">
    <aside>
      <div>
        <h1>Agentic RAG 助手</h1>
        <div class="sub">模拟 AI 工程团队内部知识库，支持检索、回答和来源引用。</div>
      </div>
      <div class="panel">
        <div class="label">知识库状态</div>
        <div class="status"><span>索引 chunk 数</span><span class="pill" id="chunkCount">读取中</span></div>
        <div class="status"><span>运行模式</span><span class="pill" id="mode">本地演示</span></div>
        <button style="width:100%;margin-top:12px;text-align:center" onclick="reindex()">重建索引</button>
      </div>
      <div class="panel">
        <div class="label">Agent 流程</div>
        <div class="flow">
          <div class="step">1. 识别问题类型</div>
          <div class="step">2. 改写检索查询</div>
          <div class="step">3. 召回知识片段</div>
          <div class="step">4. 生成回答与引用</div>
        </div>
      </div>
      <div class="panel">
        <div class="label">示例问题</div>
        <div class="examples" id="examples"></div>
      </div>
    </aside>
    <main>
      <header>
        <h1>知识库问答</h1>
        <div class="sub">回答会展示来源文档、章节和 chunk_id，适合演示 RAG 可追溯性。</div>
      </header>
      <section class="chat" id="chat">
        <div class="msg">你好，我是 Agentic RAG 知识库助手。可以问我文档入库规范、Agent 工具安全、向量数据库选型或 LangGraph 架构设计。</div>
      </section>
      <form id="form">
        <textarea id="question" placeholder="输入你的问题，例如：RAG 文档入库需要哪些 metadata？"></textarea>
        <button class="primary" type="submit">发送</button>
      </form>
    </main>
  </div>
  <script>
    const examples = [
      "RAG 文档入库需要哪些 metadata？",
      "Agent 哪些工具调用需要人工确认？",
      "对比 Qdrant、Milvus 和 pgvector 的适用场景。",
      "如何设计一个基于 LangGraph 的 RAG 流程？"
    ];
    const chat = document.getElementById("chat");
    const question = document.getElementById("question");
    const form = document.getElementById("form");

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    }
    function addMessage(text, cls, sources) {
      const el = document.createElement("div");
      el.className = "msg " + (cls || "");
      el.textContent = text;
      if (sources && sources.length) {
        const meta = document.createElement("div");
        meta.className = "meta";
        sources.slice(0, 5).forEach(src => {
          const s = document.createElement("div");
          s.className = "source";
          s.innerHTML = `<strong>${escapeHtml(src.title)} / ${escapeHtml(src.section)}</strong>${escapeHtml(src.chunk_id)} · score ${Number(src.score).toFixed(3)}`;
          meta.appendChild(s);
        });
        el.appendChild(meta);
      }
      chat.appendChild(el);
      chat.scrollTop = chat.scrollHeight;
      return el;
    }
    async function askAgent(text) {
      addMessage(text, "user");
      const pending = addMessage("正在检索知识库...");
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question: text})
      });
      const data = await res.json();
      pending.remove();
      addMessage(data.answer || "没有返回答案。", "", data.sources || []);
      document.getElementById("mode").textContent = data.provider_label || (data.llm_enabled ? "LLM 生成" : "本地演示");
    }
    async function loadStatus() {
      const res = await fetch("/api/status");
      const data = await res.json();
      document.getElementById("chunkCount").textContent = data.chunks;
      document.getElementById("mode").textContent = data.provider_label || (data.llm_enabled ? "LLM 生成" : "本地演示");
    }
    async function reindex() {
      document.getElementById("chunkCount").textContent = "构建中";
      const res = await fetch("/api/reindex", {method: "POST"});
      const data = await res.json();
      document.getElementById("chunkCount").textContent = data.chunks;
      addMessage(`索引已重建，共 ${data.chunks} 个 chunks。`);
    }
    document.getElementById("examples").innerHTML = examples.map(q => `<button type="button">${escapeHtml(q)}</button>`).join("");
    document.getElementById("examples").addEventListener("click", e => {
      if (e.target.tagName === "BUTTON") {
        question.value = e.target.textContent;
        question.focus();
      }
    });
    form.addEventListener("submit", e => {
      e.preventDefault();
      const text = question.value.trim();
      if (!text) return;
      question.value = "";
      askAgent(text).catch(err => addMessage("请求失败：" + err.message));
    });
    loadStatus();
  </script>
</body>
</html>"""


def provider_status() -> dict:
    from .config import DASHSCOPE_MODEL, LLM_PROVIDER, OPENAI_MODEL

    labels = {
        "dashscope_anthropic": f"DashScope {DASHSCOPE_MODEL}",
        "openai": f"OpenAI {OPENAI_MODEL}",
        "local": "本地演示",
    }
    return {
        "llm_enabled": LLM_PROVIDER != "local",
        "provider": LLM_PROVIDER,
        "provider_label": labels.get(LLM_PROVIDER, LLM_PROVIDER),
    }


class Handler(BaseHTTPRequestHandler):
    def send_body(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, payload: dict, status: int = 200) -> None:
        self.send_body(status, json.dumps(payload, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self) -> None:
        if self.path == "/":
            self.send_body(200, HTML.encode("utf-8"), "text/html; charset=utf-8")
        elif self.path == "/api/status":
            self.send_json({"chunks": len(LocalVectorStore().rows), **provider_status()})
        else:
            self.send_json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(raw or "{}")
        except json.JSONDecodeError:
            self.send_json({"error": "invalid json"}, 400)
            return

        if self.path == "/api/ask":
            question = str(payload.get("question", "")).strip()
            if not question:
                self.send_json({"error": "question is required"}, 400)
                return
            result = ask(question)
            sources = [
                {
                    "title": c["title"],
                    "section": c["section"],
                    "chunk_id": c["chunk_id"],
                    "score": float(c.get("score", 0)),
                }
                for c in result.get("contexts", [])
            ]
            self.send_json({"answer": result.get("answer", ""), "sources": sources, **provider_status()})
        elif self.path == "/api/reindex":
            self.send_json({"chunks": build_index()})
        else:
            self.send_json({"error": "not found"}, 404)

    def log_message(self, fmt: str, *args) -> None:
        print("%s - %s" % (self.address_string(), fmt % args))


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Web UI running at http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()
