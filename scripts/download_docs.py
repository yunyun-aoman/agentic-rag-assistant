from pathlib import Path
import re
from html.parser import HTMLParser
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from urllib.parse import urljoin


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "raw" / "web_docs"

SOURCES = [
    ("langchain_docs_index", "https://docs.langchain.com/llms.txt"),
    ("qdrant_docs", "https://qdrant.tech/documentation/overview/"),
]


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = False
        self.current = ""
        self.items = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "nav", "footer", "header"}:
            self.skip = True
        if tag in {"h1", "h2", "h3", "p", "li", "pre", "title"}:
            self.current = tag

    def handle_endtag(self, tag):
        if tag in {"script", "style", "nav", "footer", "header"}:
            self.skip = False
        if tag == self.current:
            self.current = ""

    def handle_data(self, data):
        if self.skip or not self.current:
            return
        text = re.sub(r"\s+", " ", data.strip())
        if len(text) >= 20:
            self.items.append((self.current, text))


def html_to_markdown(url: str, html: str) -> str:
    parser = TextExtractor()
    parser.feed(html)
    if not parser.items:
        return f"---\ntitle: {url}\nsource: {url}\ntags: public, web_doc\n---\n\n# {url}\n\n{html}"
    title_text = next((text for tag, text in parser.items if tag in {"h1", "title"}), url)
    parts = [f"---\ntitle: {title_text}\nsource: {url}\ntags: public, web_doc\n---\n", f"# {title_text}\n"]
    for tag, text in parser.items:
        if tag in {"h1", "title"}:
            continue
        if tag == "h2":
            parts.append(f"\n## {text}\n")
        elif tag == "h3":
            parts.append(f"\n### {text}\n")
        elif tag == "li":
            parts.append(f"- {text}\n")
        elif tag == "pre":
            parts.append(f"\n```text\n{text}\n```\n")
        else:
            parts.append(text + "\n")
    return "\n".join(parts)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, url in SOURCES:
        try:
            current_url = url
            for _ in range(3):
                req = Request(current_url, headers={"User-Agent": "agentic-rag-demo/1.0"})
                try:
                    with urlopen(req, timeout=20) as resp:
                        html = resp.read().decode("utf-8", errors="ignore")
                    break
                except HTTPError as exc:
                    if exc.code == 308 and exc.headers.get("Location"):
                        current_url = urljoin(current_url, exc.headers["Location"])
                        continue
                    raise
            else:
                raise RuntimeError("too many redirects")
            text = html_to_markdown(url, html)
            path = OUT_DIR / f"{name}.md"
            path.write_text(text, encoding="utf-8")
            print(f"downloaded {url} -> {path}")
        except Exception as exc:
            print(f"skip {url}: {exc}")


if __name__ == "__main__":
    main()
