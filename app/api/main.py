from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.core.settings import QDRANT_COLLECTION, QDRANT_URL, VECTOR_DB
from app.ingestion.qdrant_indexer import reindex_qdrant
from src.graph_agent import ask
from src.retriever import LocalVectorStore


class AskRequest(BaseModel):
    question: str


app = FastAPI(
    title="\u667a\u80fd\u4f53 RAG \u52a9\u624b",
    version="1.0.0-qdrant",
    description="\u57fa\u4e8e Qdrant \u7684\u4f01\u4e1a\u77e5\u8bc6\u5e93\u95ee\u7b54 API",
)


HOME_HTML = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>&#26234;&#33021;&#20307; RAG &#21161;&#25163;</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --text: #1f2937;
      --muted: #6b7280;
      --line: #d9dee7;
      --accent: #0f766e;
      --accent-dark: #115e59;
      --soft: #e6f4f1;
      --danger: #b42318;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    header {
      border-bottom: 1px solid var(--line);
      background: var(--panel);
    }
    .wrap {
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
    }
    .topbar {
      min-height: 72px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    h1 {
      margin: 0;
      font-size: 24px;
      line-height: 1.2;
    }
    .subtitle {
      margin-top: 6px;
      color: var(--muted);
      font-size: 14px;
    }
    .links {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }
    a, button {
      border-radius: 6px;
      font: inherit;
    }
    a {
      color: var(--accent-dark);
      text-decoration: none;
    }
    .link-button {
      border: 1px solid var(--line);
      background: #fff;
      padding: 9px 12px;
    }
    main {
      padding: 24px 0 40px;
    }
    .grid {
      display: grid;
      grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.8fr);
      gap: 18px;
      align-items: start;
    }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }
    .panel h2 {
      margin: 0 0 12px;
      font-size: 18px;
    }
    label {
      display: block;
      font-weight: 600;
      margin-bottom: 8px;
    }
    textarea {
      width: 100%;
      min-height: 150px;
      resize: vertical;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 12px;
      font: inherit;
      line-height: 1.5;
      outline: none;
    }
    textarea:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--soft);
    }
    .actions {
      display: flex;
      gap: 10px;
      align-items: center;
      margin-top: 12px;
      flex-wrap: wrap;
    }
    button {
      border: 1px solid var(--accent);
      background: var(--accent);
      color: #fff;
      padding: 10px 14px;
      cursor: pointer;
      font-weight: 600;
    }
    button.secondary {
      background: #fff;
      color: var(--accent-dark);
    }
    button:disabled {
      opacity: 0.65;
      cursor: wait;
    }
    .hint, .status-line {
      color: var(--muted);
      font-size: 13px;
    }
    .answer {
      margin-top: 16px;
      border-top: 1px solid var(--line);
      padding-top: 16px;
      white-space: pre-wrap;
      line-height: 1.65;
    }
    .error {
      color: var(--danger);
    }
    dl {
      margin: 0;
      display: grid;
      gap: 10px;
    }
    .row {
      display: grid;
      grid-template-columns: 110px minmax(0, 1fr);
      gap: 10px;
      align-items: baseline;
      border-bottom: 1px solid #eef1f5;
      padding-bottom: 10px;
    }
    dt {
      color: var(--muted);
      font-size: 13px;
    }
    dd {
      margin: 0;
      overflow-wrap: anywhere;
    }
    .sources {
      margin-top: 14px;
      display: grid;
      gap: 8px;
    }
    .source {
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px;
      background: #fbfcfd;
      font-size: 13px;
    }
    @media (max-width: 820px) {
      .grid { grid-template-columns: 1fr; }
      .topbar { align-items: flex-start; flex-direction: column; padding: 16px 0; }
      .links { justify-content: flex-start; }
    }
  </style>
</head>
<body>
  <header>
    <div class="wrap topbar">
      <div>
        <h1>&#26234;&#33021;&#20307; RAG &#21161;&#25163;</h1>
        <div class="subtitle">&#20351;&#29992; Qdrant &#26816;&#32034;&#20225;&#19994;&#30693;&#35782;&#24211;&#65292;&#20877;&#30001; Agent &#29983;&#25104;&#22238;&#31572;</div>
      </div>
      <nav class="links">
        <a class="link-button" href="/docs">&#24320;&#21457;&#25509;&#21475;</a>
        <a class="link-button" href="/openapi.json">OpenAPI JSON</a>
      </nav>
    </div>
  </header>
  <main class="wrap">
    <div class="grid">
      <section class="panel">
        <h2>&#25552;&#38382;</h2>
        <label for="question">&#36755;&#20837;&#20320;&#35201;&#38382;&#30340;&#38382;&#39064;</label>
        <textarea id="question" placeholder="&#20363;&#22914;&#65306;&#36825;&#20010;&#39033;&#30446;&#30340;&#20027;&#35201;&#21151;&#33021;&#26159;&#20160;&#20040;&#65311;"></textarea>
        <div class="actions">
          <button id="askBtn">&#21457;&#36865;&#38382;&#39064;</button>
          <button id="clearBtn" class="secondary">&#28165;&#31354;</button>
          <span id="askState" class="hint"></span>
        </div>
        <div id="answer" class="answer"></div>
        <div id="sources" class="sources"></div>
      </section>
      <aside class="panel">
        <h2>&#31995;&#32479;&#29366;&#24577;</h2>
        <dl>
          <div class="row"><dt>&#21518;&#31471;</dt><dd id="status">-</dd></div>
          <div class="row"><dt>&#21521;&#37327;&#24211;</dt><dd id="vectorDb">-</dd></div>
          <div class="row"><dt>Qdrant</dt><dd id="qdrant">-</dd></div>
          <div class="row"><dt>&#38598;&#21512;</dt><dd id="collection">-</dd></div>
          <div class="row"><dt>&#26412;&#22320;&#20998;&#22359;</dt><dd id="chunks">-</dd></div>
        </dl>
        <div class="actions">
          <button id="refreshBtn" class="secondary">&#21047;&#26032;&#29366;&#24577;</button>
          <button id="reindexBtn" class="secondary">&#37325;&#24314;&#32034;&#24341;</button>
        </div>
        <p id="sideNote" class="status-line"></p>
      </aside>
    </div>
  </main>
  <script>
    const $ = (id) => document.getElementById(id);

    async function loadStatus() {
      $("sideNote").textContent = "";
      try {
        const res = await fetch("/api/status");
        const data = await res.json();
        $("status").textContent = data.status || "-";
        $("vectorDb").textContent = data.vector_db || "-";
        $("qdrant").textContent = data.qdrant && data.qdrant.available
          ? "\u6b63\u5e38\uff0c\u6570\u636e\u70b9 " + data.qdrant.points
          : "\u4e0d\u53ef\u7528";
        $("collection").textContent = data.qdrant_collection || "-";
        $("chunks").textContent = data.local_chunks ?? "-";
      } catch (err) {
        $("status").textContent = "\u5f02\u5e38";
        $("sideNote").textContent = String(err);
      }
    }

    async function askQuestion() {
      const question = $("question").value.trim();
      if (!question) {
        $("askState").textContent = "\u8bf7\u5148\u8f93\u5165\u95ee\u9898";
        return;
      }
      $("askBtn").disabled = true;
      $("askState").textContent = "\u6b63\u5728\u68c0\u7d22\u548c\u751f\u6210\u56de\u7b54...";
      $("answer").textContent = "";
      $("sources").innerHTML = "";
      try {
        const res = await fetch("/api/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(JSON.stringify(data));
        $("answer").textContent = data.answer || "\u6ca1\u6709\u8fd4\u56de\u56de\u7b54";
        const sources = data.sources || [];
        $("sources").innerHTML = sources.map((s, i) => `
          <div class="source">
            <strong>[${i + 1}] ${s.title || "source"}</strong><br />
            section: ${s.section || "-"}<br />
            score: ${Number(s.score || 0).toFixed(4)}
          </div>
        `).join("");
        $("askState").textContent = "\u5b8c\u6210";
      } catch (err) {
        $("answer").innerHTML = `<span class="error">\u8bf7\u6c42\u5931\u8d25\uff1a${String(err)}</span>`;
        $("askState").textContent = "";
      } finally {
        $("askBtn").disabled = false;
      }
    }

    async function reindex() {
      $("reindexBtn").disabled = true;
      $("sideNote").textContent = "\u6b63\u5728\u91cd\u5efa\u7d22\u5f15...";
      try {
        const res = await fetch("/api/reindex/qdrant", { method: "POST" });
        const data = await res.json();
        $("sideNote").textContent = "\u5df2\u91cd\u5efa\u7d22\u5f15\uff1a" + data.indexed_chunks + " chunks";
        await loadStatus();
      } catch (err) {
        $("sideNote").textContent = String(err);
      } finally {
        $("reindexBtn").disabled = false;
      }
    }

    $("askBtn").addEventListener("click", askQuestion);
    $("clearBtn").addEventListener("click", () => {
      $("question").value = "";
      $("answer").textContent = "";
      $("sources").innerHTML = "";
      $("askState").textContent = "";
    });
    $("refreshBtn").addEventListener("click", loadStatus);
    $("reindexBtn").addEventListener("click", reindex);
    $("question").addEventListener("keydown", (event) => {
      if (event.ctrlKey && event.key === "Enter") askQuestion();
    });
    loadStatus();
  </script>
</body>
</html>
"""


def _qdrant_status() -> dict:
    try:
        from app.retriever.qdrant_http import QdrantHttpStore

        store = QdrantHttpStore()
        data = store._request("GET", f"/collections/{QDRANT_COLLECTION}")
        result = data.get("result", {})
        points = result.get("points_count") or result.get("vectors_count") or 0
        return {"available": True, "points": points}
    except Exception as exc:
        return {"available": False, "error": str(exc)}


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return HOME_HTML


@app.get("/api/status")
def status() -> dict:
    local_chunks = len(LocalVectorStore().rows)
    return {
        "status": "ok",
        "vector_db": VECTOR_DB,
        "local_chunks": local_chunks,
        "qdrant_url": QDRANT_URL,
        "qdrant_collection": QDRANT_COLLECTION,
        "qdrant": _qdrant_status(),
    }


@app.post("/api/ask")
def ask_api(req: AskRequest) -> dict:
    result = ask(req.question)
    if isinstance(result, str):
        return {
            "answer": result,
            "sources": [],
            "task_type": "",
            "rewritten_query": "",
        }

    sources = [
        {
            "title": c.get("title", ""),
            "section": c.get("section", ""),
            "chunk_id": c.get("chunk_id", ""),
            "score": c.get("score", 0),
        }
        for c in result.get("contexts", [])
    ]
    return {
        "answer": result.get("answer", ""),
        "sources": sources,
        "task_type": result.get("task_type", ""),
        "rewritten_query": result.get("rewritten_query", ""),
    }


@app.post("/api/reindex/qdrant")
def reindex_qdrant_api() -> dict:
    count = reindex_qdrant()
    return {"indexed_chunks": count, "url": QDRANT_URL, "collection": QDRANT_COLLECTION}
