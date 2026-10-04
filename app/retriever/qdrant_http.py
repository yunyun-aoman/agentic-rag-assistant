import json
from typing import Any
from urllib.request import ProxyHandler, Request, build_opener

from app.core.settings import QDRANT_COLLECTION, QDRANT_URL
from src.retriever import embed


class QdrantHttpStore:
    def __init__(self, url: str = QDRANT_URL, collection: str = QDRANT_COLLECTION):
        self.url = url.rstrip("/")
        self.collection = collection
        self.opener = build_opener(ProxyHandler({}))

    def _request(self, method: str, path: str, payload: dict | None = None) -> dict:
        body = None
        headers = {"Content-Type": "application/json"}
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = Request(
            self.url + path,
            data=body,
            headers=headers,
            method=method,
        )
        with self.opener.open(req, timeout=60) as resp:
            text = resp.read().decode("utf-8")
        return json.loads(text) if text else {}

    def ensure_collection(self, vector_size: int = 512) -> None:
        payload = {
            "vectors": {
                "size": vector_size,
                "distance": "Cosine",
            }
        }
        self._request("PUT", f"/collections/{self.collection}", payload)

    def upsert_chunks(self, chunks: list[dict[str, Any]]) -> None:
        points = []
        for i, chunk in enumerate(chunks):
            chunk_id = chunk["chunk_id"]
            point_id = abs(hash(chunk_id)) % (2**63)
            points.append(
                {
                    "id": point_id,
                    "vector": embed(chunk["text"]),
                    "payload": {
                        "chunk_id": chunk_id,
                        "title": chunk["title"],
                        "source": chunk["source"],
                        "path": chunk["path"],
                        "section": chunk["section"],
                        "text": chunk["text"],
                        "metadata": chunk.get("metadata", {}),
                    },
                }
            )
            if len(points) >= 64:
                self._upsert_points(points)
                points = []
        if points:
            self._upsert_points(points)

    def _upsert_points(self, points: list[dict]) -> None:
        self._request(
            "PUT",
            f"/collections/{self.collection}/points?wait=true",
            {"points": points},
        )

    def search(self, query: str, top_k: int = 6, filters: dict | None = None) -> list[dict]:
        payload: dict[str, Any] = {
            "vector": embed(query),
            "limit": top_k,
            "with_payload": True,
        }
        if filters:
            payload["filter"] = filters
        data = self._request(
            "POST",
            f"/collections/{self.collection}/points/search",
            payload,
        )
        rows = []
        for item in data.get("result", []):
            p = item.get("payload", {})
            rows.append(
                {
                    "chunk_id": p.get("chunk_id", ""),
                    "title": p.get("title", ""),
                    "source": p.get("source", ""),
                    "path": p.get("path", ""),
                    "section": p.get("section", ""),
                    "text": p.get("text", ""),
                    "metadata": p.get("metadata", {}),
                    "score": item.get("score", 0.0),
                }
            )
        return rows
