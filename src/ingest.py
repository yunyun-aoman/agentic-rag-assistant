import hashlib
import json
import re
from pathlib import Path

from .config import RAW_DIR, INDEX_DIR, INDEX_FILE
from .retriever import embed


def read_markdown(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    meta = {"title": path.stem, "source": "local", "path": str(path)}
    if text.startswith("---"):
        _, frontmatter, body = text.split("---", 2)
        text = body.strip()
        for line in frontmatter.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()
    return meta, text


def split_by_heading(text: str, max_chars: int = 1200) -> list[tuple[str, str]]:
    sections = []
    current_title = "正文"
    current = []
    for line in text.splitlines():
        if line.startswith("#"):
            if current:
                sections.append((current_title, "\n".join(current).strip()))
            current_title = line.lstrip("#").strip() or current_title
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append((current_title, "\n".join(current).strip()))

    chunks = []
    for title, body in sections:
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        while len(body) > max_chars:
            cut = body.rfind("\n\n", 0, max_chars)
            if cut < 300:
                cut = max_chars
            chunks.append((title, body[:cut].strip()))
            body = body[cut:].strip()
        if body:
            chunks.append((title, body))
    return chunks


def build_index() -> int:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    with INDEX_FILE.open("w", encoding="utf-8") as out:
        for path in sorted(RAW_DIR.rglob("*.md")):
            meta, text = read_markdown(path)
            doc_hash = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
            for i, (section, chunk_text) in enumerate(split_by_heading(text)):
                chunk_id = f"{path.stem}-{doc_hash}-{i}"
                row = {
                    "chunk_id": chunk_id,
                    "title": meta.get("title", path.stem),
                    "source": meta.get("source", "local"),
                    "path": str(path.relative_to(RAW_DIR)),
                    "section": section,
                    "text": chunk_text,
                    "metadata": meta,
                    "vector": embed(chunk_text),
                }
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                count += 1
    return count


if __name__ == "__main__":
    n = build_index()
    print(f"Indexed {n} chunks -> {INDEX_FILE}")
