import json

from app.retriever.qdrant_http import QdrantHttpStore
from src.config import INDEX_FILE
from src.ingest import build_index


def reindex_qdrant() -> int:
    build_index()
    chunks = []
    with INDEX_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                row.pop("vector", None)
                chunks.append(row)

    store = QdrantHttpStore()
    store.ensure_collection()
    store.upsert_chunks(chunks)
    return len(chunks)


if __name__ == "__main__":
    count = reindex_qdrant()
    print(f"Indexed {count} chunks into Qdrant")
