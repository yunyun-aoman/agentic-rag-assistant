# Practical Runbook

## 1. Start Qdrant

This project uses Qdrant as the vector database.

```powershell
cd F:\codex\projects\agentic-rag-assistant
docker compose up -d qdrant
```

Qdrant Dashboard:

```text
http://localhost:6333/dashboard
```

Default settings:

```text
VECTOR_DB=qdrant
QDRANT_URL=http://127.0.0.1:6333
QDRANT_COLLECTION=agentic_rag_chunks
```

## 2. Install dependencies

```powershell
cd F:\codex\projects\agentic-rag-assistant
$env:PIP_CACHE_DIR="F:\codex\pip-cache"
$env:TEMP="F:\Temp"
$env:TMP="F:\Temp"
.\.venv\Scripts\python.exe -m pip install -r requirements-core.txt -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```

## 3. Build the local JSONL index

```powershell
.\.venv\Scripts\python.exe -m src.ingest
```

## 4. Reindex into Qdrant

```powershell
.\.venv\Scripts\python.exe -m app.ingestion.qdrant_indexer
```

## 5. Run API

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --host 127.0.0.1 --port 8010
```

Status:

```text
GET http://127.0.0.1:8010/api/status
```

Reindex:

```text
POST http://127.0.0.1:8010/api/reindex/qdrant
```

Ask:

```text
POST http://127.0.0.1:8010/api/ask
```
