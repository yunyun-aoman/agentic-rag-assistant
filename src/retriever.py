import json
import math
import re
from collections import Counter
from pathlib import Path

from .config import INDEX_FILE


EN_RE = re.compile(r"[A-Za-z0-9_]+")
ZH_RE = re.compile(r"[\u4e00-\u9fff]+")


def tokenize(text: str) -> list[str]:
    tokens = [t.lower() for t in EN_RE.findall(text)]
    for seq in ZH_RE.findall(text):
        tokens.append(seq)
        tokens.extend(seq[i : i + 2] for i in range(max(0, len(seq) - 1)))
        if len(seq) <= 8:
            tokens.extend(seq)
    return tokens


def embed(text: str, dims: int = 512) -> list[float]:
    counts = Counter(tokenize(text))
    vec = [0.0] * dims
    for token, count in counts.items():
        vec[hash(token) % dims] += float(count)
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


class LocalVectorStore:
    def __init__(self, index_file: Path = INDEX_FILE):
        self.index_file = index_file
        self.rows = []
        if index_file.exists():
            with index_file.open("r", encoding="utf-8") as f:
                self.rows = [json.loads(line) for line in f if line.strip()]

    def search(self, query: str, top_k: int = 6) -> list[dict]:
        qvec = embed(query)
        qtokens = set(tokenize(query))
        english_query = set(t.lower() for t in EN_RE.findall(query))
        scored = []
        for row in self.rows:
            title_section = row["title"] + " " + row["section"]
            full_text = title_section + " " + row["text"]
            text_tokens = set(tokenize(full_text))
            overlap = len(qtokens & text_tokens) / max(1, len(qtokens))
            heading_overlap = len(qtokens & set(tokenize(title_section))) / max(1, len(qtokens))
            english_text = set(t.lower() for t in EN_RE.findall(full_text))
            english_overlap = len(english_query & english_text) / max(1, len(english_query))
            score = cosine(qvec, row["vector"]) + overlap + 1.5 * heading_overlap + 2.0 * english_overlap
            scored.append({**row, "score": score})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
