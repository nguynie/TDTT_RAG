import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=False)

FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "").strip()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "").strip()

OLLAMA_BASE_URL = (os.getenv("OLLAMA_BASE_URL") or "http://localhost:11434").strip().rstrip("/")
EMBEDDING_MODEL = (os.getenv("EMBEDDING_MODEL") or "embeddinggemma").strip()
CHAT_MODEL = (os.getenv("CHAT_MODEL") or "qwen3:4b").strip()

def _parse_int(val: str | None, default: int) -> int:
    try:
        return int(val.strip()) if val and val.strip() else default
    except (ValueError, AttributeError):
        return default

def _parse_float(val: str | None, default: float) -> float:
    try:
        return float(val.strip()) if val and val.strip() else default
    except (ValueError, AttributeError):
        return default

TOP_K = _parse_int(os.getenv("TOP_K"), 3)
SIMILARITY_THRESHOLD = _parse_float(os.getenv("SIMILARITY_THRESHOLD"), 0.25)
