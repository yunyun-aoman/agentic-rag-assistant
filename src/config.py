from pathlib import Path

import os

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INDEX_DIR = DATA_DIR / "index"
INDEX_FILE = INDEX_DIR / "chunks.jsonl"

try:
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except Exception:
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


LLM_PROVIDER = _env("LLM_PROVIDER")
LLM_API_KEY = _env("LLM_API_KEY")
LLM_MODEL = _env("LLM_MODEL")
LLM_BASE_URL = _env("LLM_BASE_URL")
LLM_TIMEOUT_SECONDS = float(_env("LLM_TIMEOUT_SECONDS", "120") or "120")

OPENAI_API_KEY = _env("OPENAI_API_KEY")
OPENAI_MODEL = _env("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_BASE_URL = _env("OPENAI_BASE_URL")

DASHSCOPE_API_KEY = _env("DASHSCOPE_API_KEY") or _env("ALIYUN_API_KEY")
DASHSCOPE_BASE_URL = _env("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
DASHSCOPE_MODEL = _env("DASHSCOPE_MODEL", "qwen-plus")

if not LLM_PROVIDER:
    if LLM_API_KEY:
        LLM_PROVIDER = "openai_compatible"
    elif DASHSCOPE_API_KEY:
        LLM_PROVIDER = "dashscope"
    elif OPENAI_API_KEY:
        LLM_PROVIDER = "openai"
    else:
        LLM_PROVIDER = "local"

if LLM_PROVIDER == "openai_compatible":
    LLM_API_KEY = LLM_API_KEY or OPENAI_API_KEY or DASHSCOPE_API_KEY
    LLM_MODEL = LLM_MODEL or OPENAI_MODEL or DASHSCOPE_MODEL
    LLM_BASE_URL = LLM_BASE_URL or OPENAI_BASE_URL or DASHSCOPE_BASE_URL
elif LLM_PROVIDER == "dashscope":
    LLM_API_KEY = DASHSCOPE_API_KEY
    LLM_MODEL = DASHSCOPE_MODEL
    LLM_BASE_URL = DASHSCOPE_BASE_URL
elif LLM_PROVIDER == "openai":
    LLM_API_KEY = OPENAI_API_KEY
    LLM_MODEL = OPENAI_MODEL
    LLM_BASE_URL = OPENAI_BASE_URL
